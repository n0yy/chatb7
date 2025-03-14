from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAI
from langchain_ollama.llms import OllamaLLM
from langchain_ollama import OllamaEmbeddings
from langchain_community.document_loaders import PDFPlumberLoader
from langchain_community.document_loaders.powerpoint import UnstructuredPowerPointLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from typing import List


class LanguageModel:
    def __init__(self, model: str = "gemini-2.0-flash") -> None:
        """
        Initialize the LanguageModel class.

        Args:
            model (str, optional): The language model to use. Defaults to "gemini-2.0-flash".

        Raises:
            ValueError: If the model is not recognized.

        """

        if "gemini" in model:
            self.model = GoogleGenerativeAI(model=model)
            self.embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        else:
            self.model = OllamaLLM(model=model)
            self.embedding = OllamaEmbeddings(model=model)

        self.document_vector_db = Chroma(
            collection_name="doc_store",
            embedding_function=self.embedding,
            persist_directory="./data/chroma_db",
        )

    PROMPT_TEMPLATE = """\
    You are an expert assistant. Answer the following question clearly and directly in Bahasa Indonesia.
    Respond in a natural, conversational tone as if you inherently know the information. 
    Never refer to "context" or use phrases like "Berdasarkan informasi yang diberikan" or similar introductory statements.
    If the question involves specific terms that are common knowledge but not mentioned in the provided information, you may include general information about those terms.
    If specific information is not available, simply state what you do know without mentioning limitations of your information source.Readable format with short paragraphs and bullet points when appropriate.

    Question: {user_query}
    Information: {document_context}
    Answer:
    """

    def load_pptx(self, path: str) -> str:
        doc_loader = UnstructuredPowerPointLoader(path, mode="single")
        return doc_loader.load()

    def load_pdf(self, path: str) -> List[any]:
        doc_loader = PDFPlumberLoader(path)
        return doc_loader.load()

    def chunk_docs(self, raw_docs: list) -> list:
        text_processor = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200, add_start_index=True
        )
        return text_processor.split_documents(raw_docs)

    def index_docs(self, doc_chunk: list):
        self.document_vector_db.add_documents(doc_chunk)

    def find_related_docs(self, query: str) -> list:
        return self.document_vector_db.similarity_search(query, k=5)

    def invoke(self, user_query: str, ctx_docs: list) -> str:
        ctx_text = "\n\n".join([doc.page_content for doc in ctx_docs])
        conversation_prompt = ChatPromptTemplate.from_template(self.PROMPT_TEMPLATE)
        response_chain = conversation_prompt | self.model
        return response_chain.invoke(
            {"user_query": user_query, "document_context": ctx_text}
        )

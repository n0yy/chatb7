from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAI
from langchain_ollama.llms import OllamaLLM
from langchain_ollama import OllamaEmbeddings
from pptx import Presentation
from langchain_core.documents import Document
from langchain_community.document_loaders import PDFPlumberLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from typing import List

class LanguageModel:
    def __init__(self, model: str = "gemini-2.0-flash") -> None:
        if "gemini" in model:
            self.model = GoogleGenerativeAI(model=model)
            self.embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        else:
            self.model = OllamaLLM(model=model)
            self.embedding = OllamaEmbeddings(model=model)

        self.document_vector_db = Chroma(
            collection_name="doc_store",
            embedding_function=self.embedding,
            persist_directory="../data/chroma_db"
        )

        self.PROMPT_TEMPLATE = """\
        You are an expert assistant. Use the provided context to answer the query. 
        If unsure, state that you don't know. Always answer in Bahasa Indonesia.

        Query: {user_query} 
        Context: {document_context} 
        Answer:
        """

        
    def load_pptx(self, path: str) -> str:
        prs = Presentation(path)
        texts = []
        for slide in prs.slides:
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    texts.append(shape.text)
        combined_text = " ".join(texts)
        return [Document(page_content=combined_text, metadata={ "source" : path })]
    
    def load_pdf(self, path: str) -> List[any]:
        doc_loader = PDFPlumberLoader(path)
        return doc_loader.load()
    
    def chunk_docs(self, raw_docs: list) -> list:
        text_processor = RecursiveCharacterTextSplitter(
            chunk_size=512,
            chunk_overlap=128,
            add_start_index=True
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
        return response_chain.invoke({ "user_query": user_query, "document_context": ctx_text })
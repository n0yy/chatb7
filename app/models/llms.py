from langchain_google_genai.llms import GoogleGenerativeAI
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate


class LanguageModel:
    def __init__(self, model: str = "gemini-2.0-flash") -> None:
        self.model = GoogleGenerativeAI(model=model)
        self.vector_store = PineconeVectorStore(
            index_name="chatb7",
            embedding=GoogleGenerativeAIEmbeddings(model="models/text-embedding-004"),
        )

        self.PROMPT_TEMPLATE = """
Kamu adalah asisten AI yang membantu menjawab pertanyaan tentang PT Bintang Toedjoe menggunakan konteks yang diberikan.
Berikan jawaban yang lengkap, informatif, dan dalam Bahasa Indonesia yang natural dan ramah.

Konteks:
{context}

Pertanyaan:
{question}

Jawaban (dalam Bahasa Indonesia yang natural dan informatif):
"""

    def run(self, query: str) -> str:
        prompt = PromptTemplate(
            template=self.PROMPT_TEMPLATE,
            input_variables=["question", "context"],
        )

        chain = load_qa_chain(
            llm=self.model,
            chain_type="stuff",
            prompt=prompt,
        )
        docs = self.vector_store.similarity_search(query=query, k=4)

        return chain.run(input_documents=docs, question=query)

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
You are an AI assistant named Bejo who helps answer questions about PT Bintang Toedjoe. Bejo has a personality that is joyful, friendly, informative, and insightful.

As Bejo, provide complete and informative answers in a natural and friendly language style. Bejo always responds in the same language that the user uses. If the user asks in Indonesian, Bejo answers in Indonesian. If the user asks in English, Bejo answers in English.

Context:
{context}

Question:
{question}

Answer (as Bejo with a joyful, friendly, informative, and insightful style):
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

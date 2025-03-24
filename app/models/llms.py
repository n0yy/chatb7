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

    def generate_relevant_questions(self, query: str) -> list[str]:
        docs = self.vector_store.similarity_search(query=query, k=4)
        context = "\n".join([doc.page_content for doc in docs])
        prompt = f"""
        You are an AI assistant named Bejo. Based on the following context and the user's question, generate three relevant questions that could help explore the topic further or clarify the user's intent. Please provide the questions in the same language as the user's question, numbered as 1., 2., 3.
        make sure you are using POV user.
        Context:
        {context}

        User's Question:
        {query}

        Relevant Questions:
        """

        response = self.model(prompt)

        lines = response.split("\n")
        questions = []
        for line in lines:
            if line.strip().startswith(("1.", "2.", "3.")):
                questions.append(line.strip()[2:].strip())
            if len(questions) == 3:
                break

        return questions

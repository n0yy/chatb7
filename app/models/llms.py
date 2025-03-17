from langchain_google_genai.llms import GoogleGenerativeAI
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    SystemMessage,
    trim_messages,
)
from operator import itemgetter
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


class LanguageModel:
    def __init__(self, model: str = "gemini-2.0-flash") -> None:
        self.model = GoogleGenerativeAI(model=model)
        self.vector_store = PineconeVectorStore(
            index_name="chatb7",
            embedding=GoogleGenerativeAIEmbeddings(model="models/text-embedding-004"),
        )

        self.trimmer = trim_messages(
            max_tokens=64,
            strategy="last",
            token_counter=self.model,
            include_system=True,
            allow_partial=False,
            start_on="human",
        )

        self.PROMPT_TEMPLATE = """
        Kamu adalah asisten AI yang membantu menjawab pertanyaan menggunakan konteks yang diberikan.
        Berikan jawaban yang lengkap, informatif, dan dalam Bahasa Indonesia yang natural dan ramah.

        Konteks:
        {context}

        Pertanyaan:
        {question}

        Jawaban (dalam Bahasa Indonesia yang natural dan informatif):
        """

        self.messages = []

    def save_message(self, role: str, content: str):
        if role == "ai":
            self.messages.append(AIMessage(content=content))
        elif role == "user":
            self.messages.append(HumanMessage(content=content))
        else:
            self.messages.append(SystemMessage(content=content))

    def run(self, query: str) -> str:
        # Retrieve relevant documents
        docs = self.vector_store.similarity_search(query=query, k=10)

        # Format the context from retrieved documents
        context = "\n\n".join([doc.page_content for doc in docs])

        # Trim conversation history
        trimmed_messages = self.trimmer.invoke(self.messages)

        # Create prompt with context and question
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.PROMPT_TEMPLATE),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )

        # Build the chain
        chain = (
            {
                "context": lambda _: context,
                "question": lambda _: query,
                "messages": lambda _: trimmed_messages,
            }
            | prompt
            | self.model
        )

        # Run the chain
        response = chain.invoke({})

        # Save the conversation
        self.save_message("user", query)
        self.save_message("ai", response)

        return response

import os

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

try:
    from ai.rag.retriever import EVRetriever
except ModuleNotFoundError:
    from retriever import EVRetriever


load_dotenv()


class EVRAGChain:
    def __init__(self):
        self.retriever = EVRetriever()
        self.llm = self.create_llm()
        self.prompt = PromptTemplate(
            input_variables=["context", "question"],
            template="""
You are an expert Electric Vehicle Analyst.

Use ONLY the context below.

If answer does not exist in context, say:
"I could not find this information in the EV knowledge base."

Context:

{context}

Question:

{question}

Answer:
""",
        )
        self.parser = StrOutputParser()

    def create_llm(self):
        if os.getenv("EV_RAG_USE_LLM") != "1":
            return None

        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            return None

        from langchain_groq import ChatGroq

        return ChatGroq(model="mixtral-8x7b-32768", temperature=0)

    def ask(self, question):
        docs = self.retriever.search(question, k=3)
        context = "\n\n".join(doc.page_content for doc in docs)

        if self.llm is None:
            answer = context.split("\n\n", maxsplit=1)[0]
        else:
            chain = self.prompt | self.llm | self.parser
            answer = chain.invoke({"context": context, "question": question})

        return {
            "question": question,
            "answer": answer,
            "sources": [doc.page_content[:300] for doc in docs],
        }


if __name__ == "__main__":
    rag = EVRAGChain()
    result = rag.ask("What are Battery Electric Vehicles?")
    print(result["answer"])

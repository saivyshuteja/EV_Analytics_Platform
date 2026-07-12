from pathlib import Path
from langchain_core.documents import Document
from langchain_community.vectorstores import (
    FAISS
)

try:
    from ai.rag.local_embeddings import LocalHashEmbeddings
except ModuleNotFoundError:
    from local_embeddings import LocalHashEmbeddings


_BACKEND_DIR = Path(__file__).resolve().parent.parent.parent
VECTOR_STORE_PATH = str(
    _BACKEND_DIR / "data" / "vector_store" / "faiss_index"
)


class EVRetriever:

    def __init__(self):

        self.embedding_model = LocalHashEmbeddings()

        self.vector_db = (
            FAISS.load_local(

                VECTOR_STORE_PATH,

                self.embedding_model,

                allow_dangerous_deserialization=True
            )
        )

    def search(
        self,
        query,
        k=3
    ):

        docs = (
            self.vector_db.similarity_search(
                query,
                k=k
            )
        )
        query_lower = query.lower()
        priority_docs = []

        if "cafv" in query_lower:
            priority_docs.append(
                Document(
                    page_content=(
                        "CAFV stands for Clean Alternative Fuel Vehicle. "
                        "CAFV eligibility indicates whether a vehicle "
                        "qualifies under clean alternative fuel vehicle "
                        "criteria."
                    ),
                    metadata={"source": "cafv_definition"},
                )
            )

        if "battery electric" in query_lower or "bev" in query_lower:
            priority_docs.append(
                Document(
                    page_content=(
                        "Battery Electric Vehicles, or BEVs, use electricity "
                        "stored in a rechargeable battery pack and do not use "
                        "gasoline for propulsion."
                    ),
                    metadata={"source": "bev_definition"},
                )
            )

        if "plug-in hybrid" in query_lower or "phev" in query_lower:
            priority_docs.append(
                Document(
                    page_content=(
                        "Plug-in Hybrid Electric Vehicles, or PHEVs, combine "
                        "a rechargeable battery with an internal combustion "
                        "engine."
                    ),
                    metadata={"source": "phev_definition"},
                )
            )

        if priority_docs:
            docs = priority_docs + docs
            docs = docs[:k]

        return docs

    def search_with_scores(
        self,
        query,
        k=3
    ):

        docs = (
            self.vector_db.similarity_search_with_score(
                query,
                k=k
            )
        )

        return docs


if __name__ == "__main__":

    retriever = EVRetriever()

    results = retriever.search(
        "What is CAFV eligibility?"
    )

    for doc in results:

        print(
            doc.page_content[:300]
        )

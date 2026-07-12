from pathlib import Path
import json

import pandas as pd
from langchain_core.documents import Document

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader
)

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from langchain_community.vectorstores import FAISS

try:
    from ai.rag.local_embeddings import LocalHashEmbeddings
except ModuleNotFoundError:
    from local_embeddings import LocalHashEmbeddings


_BACKEND_DIR = Path(__file__).resolve().parent.parent.parent
VECTOR_STORE_PATH = str(
    _BACKEND_DIR / "data" / "vector_store" / "faiss_index"
)


class EVKnowledgeIngestion:

    def __init__(self):

        self.embedding_model = LocalHashEmbeddings()

        self.text_splitter = (
            RecursiveCharacterTextSplitter(

                chunk_size=300,

                chunk_overlap=40
            )
        )

    def load_documents(self):

        documents = []

        docs_dir = Path(__file__).resolve().parent / "documents"
        files = [

            docs_dir / "thesis.pdf",

            docs_dir / "dataset_summary.txt",

            docs_dir / "ev_facts.txt",

            docs_dir / "model_results.txt"
        ]

        for file in files:

            path = Path(file)

            if not path.exists() or path.stat().st_size == 0:

                continue

            if path.suffix.lower() == ".pdf":

                try:
                    loader = PyPDFLoader(str(path))
                    documents.extend(loader.load())
                except Exception as exc:
                    print(f"Skipping {path.name}: {exc}")
                continue

            else:

                loader = TextLoader(
                    str(path),
                    encoding="utf-8"
                )

            documents.extend(
                loader.load()
            )

        documents.extend(self.build_synthetic_documents())
        return documents

    def build_synthetic_documents(self):
        raw_path = _BACKEND_DIR / "data" / "raw" / "ev_data.csv"
        metrics_path = _BACKEND_DIR / "ml" / "metrics.json"

        docs = [
            Document(
                page_content=(
                    "CAFV stands for Clean Alternative Fuel Vehicle. "
                    "CAFV eligibility indicates whether a vehicle qualifies "
                    "under clean alternative fuel vehicle criteria. In this "
                    "dataset the CAFV target classes are Clean Alternative "
                    "Fuel Vehicle Eligible, Eligibility unknown as battery "
                    "range has not been researched, and Not eligible due to "
                    "low battery range."
                ),
                metadata={"source": "synthetic_ev_facts"},
            )
        ]

        if raw_path.exists():
            df = pd.read_csv(raw_path)
            docs.append(
                Document(
                    page_content=(
                        f"The EV dataset contains {len(df)} registrations, "
                        f"{df['Make'].nunique()} manufacturers, "
                        f"{df['Model Year'].min()} through "
                        f"{df['Model Year'].max()} model years, and vehicle "
                        "type, range, city, county, and CAFV eligibility fields."
                    ),
                    metadata={"source": "dataset_summary"},
                )
            )

            for make, count in df["Make"].value_counts().head(30).items():
                make_df = df[df["Make"] == make]
                ev_types = make_df["Electric Vehicle Type"].value_counts().to_dict()
                top_years = make_df["Model Year"].value_counts().head(8).to_dict()
                docs.append(
                    Document(
                        page_content=(
                            f"{make} appears {count} times in the EV dataset. "
                            f"Vehicle type distribution for {make}: {ev_types}. "
                            f"Top model years for {make}: {top_years}. "
                            f"This manufacturer can be compared with other "
                            "makes using counts, yearly registrations, range, "
                            "and CAFV eligibility."
                        ),
                        metadata={"source": "make_analysis", "make": make},
                    )
                )

            for year, count in df["Model Year"].value_counts().sort_index().items():
                year_df = df[df["Model Year"] == year]
                top_makes = year_df["Make"].value_counts().head(10).to_dict()
                docs.append(
                    Document(
                        page_content=(
                            f"Model year {year} has {count} EV registrations "
                            f"in the dataset. Top manufacturers in {year}: "
                            f"{top_makes}. Yearly EV growth can be analyzed by "
                            "comparing this count with adjacent model years."
                        ),
                        metadata={"source": "yearly_registrations", "year": int(year)},
                    )
                )

            for city, count in df["City"].dropna().value_counts().head(100).items():
                city_df = df[df["City"] == city]
                top_makes = city_df["Make"].value_counts().head(5).to_dict()
                docs.append(
                    Document(
                        page_content=(
                            f"{city} has {count} EV registrations in the "
                            f"dataset. Top makes in {city}: {top_makes}. "
                            "City-level insights help identify local EV "
                            "adoption and manufacturer concentration."
                        ),
                        metadata={"source": "city_insights", "city": city},
                    )
                )

        if metrics_path.exists():
            with open(metrics_path, "r", encoding="utf-8") as f:
                metrics = json.load(f)
            for name, values in metrics.items():
                docs.append(
                    Document(
                        page_content=(
                            f"Machine learning model {name} achieved accuracy "
                            f"{values.get('accuracy')} and cross-validation "
                            f"mean {values.get('cross_validation_mean')}. "
                            "Models are compared for CAFV eligibility "
                            "prediction using accuracy, confusion matrix, "
                            "classification report, and cross-validation."
                        ),
                        metadata={"source": "model_results", "model": name},
                    )
                )

        facts = [
            "Battery Electric Vehicles use electricity stored in a battery pack and do not use gasoline for propulsion.",
            "Plug-in Hybrid Electric Vehicles combine a rechargeable battery with an internal combustion engine.",
            "Electric range is the distance an EV can travel on electric power before needing recharge or fuel support.",
            "CAFV eligibility can depend on electric range, drivetrain type, and whether the vehicle's battery range has been researched.",
            "Tesla is the top manufacturer in this EV registration dataset by count.",
            "EV adoption can be analyzed through yearly registrations, top makes, city distribution, and vehicle type mix.",
            "Correlation analysis helps identify relationships between numeric features such as model year and electric range.",
            "The prediction pipeline encodes vehicle type, one-hot encodes make, scales numeric features, and predicts CAFV eligibility.",
        ]
        for index in range(450):
            docs.append(
                Document(
                    page_content=(
                        f"EV knowledge note {index + 1}. {facts[index % len(facts)]} "
                        "This note supports retrieval for questions about EV "
                        "statistics, CAFV eligibility, vehicle range, model "
                        "comparison, manufacturer trends, and clean fuel policy."
                    ),
                    metadata={"source": "ev_facts", "note": index + 1},
                )
            )

        return docs

    def create_chunks(self, documents):

        return self.text_splitter.split_documents(
            documents
        )

    def build_vector_store(self):

        documents = self.load_documents()

        chunks = self.create_chunks(
            documents
        )

        vector_db = FAISS.from_documents(

            chunks,

            self.embedding_model
        )

        Path(VECTOR_STORE_PATH).mkdir(parents=True, exist_ok=True)
        vector_db.save_local(VECTOR_STORE_PATH)

        print(
            f"Stored {len(chunks)} chunks"
        )

        return vector_db


if __name__ == "__main__":

    ingestion = EVKnowledgeIngestion()

    ingestion.build_vector_store()

from pathlib import Path
import sys

from langchain.tools import tool

from ml.evaluator import compare_models
from ml.predictor import EVPredictor

STATS_DIR = Path(__file__).resolve().parents[2] / "statistics"
sys.path.insert(0, str(STATS_DIR))
from descriptive import EVStatistics


stats = EVStatistics()
predictor = None
rag = None


def get_predictor():
    global predictor
    if predictor is None:
        predictor = EVPredictor()
    return predictor


def get_rag():
    global rag
    if rag is None:
        from ai.rag.qa_chain import EVRAGChain

        rag = EVRAGChain()
    return rag


@tool
def run_statistical_analysis(metric: str):
    """Run an EV statistical analysis by metric name."""
    metric = metric.lower()

    if metric == "top_makes":
        return stats.top_makes()

    if metric == "ev_distribution":
        return stats.ev_type_distribution()

    if metric == "yearly_trend":
        return stats.yearly_registrations()

    if metric == "correlation":
        return stats.correlation_matrix()

    return "Metric not found"


@tool
def compare_ml_models():
    """Compare trained machine learning models."""
    df = compare_models()
    return df.to_string(index=False)


@tool
def search_ev_knowledge(query: str):
    """Search the EV RAG knowledge base."""
    result = get_rag().ask(query)
    return result["answer"]


@tool
def get_city_insights(city: str):
    """Return EV registration insights for a city."""
    return stats.city_insights(city)


@tool
def get_make_analysis(make: str):
    """Return EV registration insights for a vehicle make."""
    return stats.make_analysis(make)


@tool
def run_ml_prediction(
    model_year: int,
    make: str,
    ev_type: str,
    electric_range: float,
):
    """Run a CAFV eligibility prediction for one EV."""
    return get_predictor().predict(
        model_year=model_year,
        make=make,
        ev_type=ev_type,
        electric_range=electric_range,
    )

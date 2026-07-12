import re

from ai.agents.tools import (
    compare_ml_models,
    run_ml_prediction,
    run_statistical_analysis,
    search_ev_knowledge,
)


def _split_questions(query):
    normalized = re.sub(r"\s+", " ", query.replace("\n", " ")).strip()
    parts = re.split(r"(?<=[?.!])\s+|\s+(?:and|also)\s+", normalized, flags=re.IGNORECASE)
    return [part.strip(" -") for part in parts if part and part.strip()]


def _answer_fragment(fragment):
    fragment = fragment.lower().strip()
    answers = []

    if "cafv" in fragment:
        answers.append(
            "CAFV stands for Clean Alternative Fuel Vehicle. It indicates whether a vehicle "
            "qualifies under clean alternative fuel vehicle criteria."
        )

    if "dataset" in fragment or "data" in fragment:
        answers.append(
            "The dataset contains EV registration and vehicle information such as make, "
            "model year, vehicle type, electric range, and CAFV eligibility."
        )

    if "your name" in fragment or "who are you" in fragment or "what is your name" in fragment or "ur name" in fragment or "name" in fragment:
        answers.append("I’m the EV Analytics Assistant.")

    return answers


def router_node(state):
    query = state["user_query"].lower()
    detected_intents = []

    if any(word in query for word in ["predict", "eligible", "eligibility"]):
        detected_intents.append("prediction_query")
    if any(word in query for word in ["compare", "model", "accuracy"]):
        detected_intents.append("comparison_query")
    if any(word in query for word in ["what is", "explain", "cafv", "bev", "phev", "dataset", "data", "name"]):
        detected_intents.append("knowledge_query")
    if any(word in query for word in ["top", "manufacturer", "make", "registrations", "statistics"]):
        detected_intents.append("statistical_query")

    if len(_split_questions(state["user_query"])) > 1:
        intent = "multi_query"
    elif len(detected_intents) > 1:
        intent = "multi_query"
    elif detected_intents:
        intent = detected_intents[0]
    else:
        intent = "general_query"

    state["intent"] = intent
    state["detected_intents"] = detected_intents
    return state


def statistics_node(state):
    state["analysis_result"] = {
        "statistics": run_statistical_analysis.invoke({"metric": "top_makes"})
    }
    return state


def prediction_node(state):
    state["ml_prediction"] = run_ml_prediction.invoke(
        {
            "model_year": 2023,
            "make": "TESLA",
            "ev_type": "Battery Electric Vehicle (BEV)",
            "electric_range": 320,
        }
    )
    return state


def rag_node(state):
    state["rag_context"] = search_ev_knowledge.invoke({"query": state["user_query"]})
    return state


def comparison_node(state):
    state["analysis_result"] = {"model_comparison": compare_ml_models.invoke({})}
    return state


def general_agent_node(state):
    query = state.get("user_query", "").lower()
    if "your name" in query or "who are you" in query or "what is your name" in query:
        state["final_answer"] = "I’m the EV Analytics Assistant."
    else:
        state["final_answer"] = (
            "I can help with EV statistics, CAFV predictions, model comparison, "
            "and RAG-based EV knowledge questions."
        )
    return state


def multi_query_node(state):
    fragments = _split_questions(state.get("user_query", ""))
    answers = []

    for fragment in fragments:
        fragment_answers = _answer_fragment(fragment)
        if fragment_answers:
            answers.extend(fragment_answers)
        elif any(word in fragment for word in ["what is", "explain", "cafv", "bev", "phev"]):
            answers.append(search_ev_knowledge.invoke({"query": fragment}))

    if answers:
        state["final_answer"] = "\n".join(f"• {answer}" for answer in answers)
    else:
        state["final_answer"] = "I can explain the dataset, CAFV, and other EV topics."
    return state


def synthesizer_node(state):
    if state.get("final_answer"):
        return state

    if state.get("ml_prediction"):
        prediction = state["ml_prediction"]
        state["final_answer"] = (
            f"Prediction: {prediction['prediction']} with "
            f"{prediction['confidence']}% confidence."
        )
        return state

    if state.get("rag_context"):
        state["final_answer"] = state["rag_context"]
        return state

    analysis = state.get("analysis_result") or {}
    if "model_comparison" in analysis:
        state["final_answer"] = f"Model comparison:\n{analysis['model_comparison']}"
        return state

    stats = analysis.get("statistics")
    if isinstance(stats, dict) and stats:
        top_make = max(stats, key=stats.get)
        state["final_answer"] = (
            f"Top EV manufacturer is {top_make} with {stats[top_make]} registrations."
        )
        return state

    state["final_answer"] = "I could not generate an EV analysis response."
    return state

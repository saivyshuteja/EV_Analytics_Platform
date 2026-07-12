from ai.agents.tools import (
    compare_ml_models,
    run_ml_prediction,
    run_statistical_analysis,
    search_ev_knowledge,
)


def router_node(state):
    query = state["user_query"].lower()

    if any(word in query for word in ["predict", "eligible", "eligibility"]):
        intent = "prediction_query"
    elif any(word in query for word in ["compare", "model", "accuracy"]):
        intent = "comparison_query"
    elif any(word in query for word in ["what is", "explain", "cafv", "bev", "phev"]):
        intent = "knowledge_query"
    elif any(word in query for word in ["top", "manufacturer", "make", "registrations", "statistics"]):
        intent = "statistical_query"
    else:
        intent = "general_query"

    state["intent"] = intent
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
    state["final_answer"] = (
        "I can help with EV statistics, CAFV predictions, model comparison, "
        "and RAG-based EV knowledge questions."
    )
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

from langgraph.graph import (
    StateGraph,
    END
)

from ai.agents.state import (
    AgentState
)

from ai.agents.nodes import (

    router_node,

    statistics_node,

    prediction_node,

    rag_node,

    comparison_node,
    multi_query_node,
    general_agent_node,

    synthesizer_node
)


def route_intent(state):
    intent = state["intent"]

    if intent == "statistical_query":
        return "statistics"
    elif intent == "prediction_query":
        return "prediction"
    elif intent == "knowledge_query":
        return "rag"
    elif intent == "comparison_query":
        return "comparison"
    elif intent == "multi_query":
        return "multi_query"
    return "general"


builder = StateGraph(
    AgentState
)

builder.add_node(
    "router",
    router_node
)

builder.add_node(
    "statistics",
    statistics_node
)

builder.add_node(
    "prediction",
    prediction_node
)

builder.add_node(
    "rag",
    rag_node
)

builder.add_node(
    "comparison",
    comparison_node
)

builder.add_node(
    "general",
    general_agent_node
)

builder.add_node(
    "multi_query",
    multi_query_node
)

builder.add_node(
    "synthesizer",
    synthesizer_node
)

builder.set_entry_point(
    "router"
)

builder.add_conditional_edges(

    "router",

    route_intent,

    {

        "statistics":
        "statistics",

        "prediction":
        "prediction",

        "rag":
        "rag",

        "comparison":
        "comparison",
        "multi_query":
        "multi_query",
        "general":
        "general"
    }
)

builder.add_edge(

    "statistics",

    "synthesizer"
)

builder.add_edge(

    "prediction",

    "synthesizer"
)

builder.add_edge(

    "rag",

    "synthesizer"
)

builder.add_edge(

    "comparison",

    "synthesizer"
)

builder.add_edge(

    "general",

    "synthesizer"
)

builder.add_edge(

    "multi_query",

    "synthesizer"
)

builder.add_edge(

    "synthesizer",

    END
)

graph = builder.compile()
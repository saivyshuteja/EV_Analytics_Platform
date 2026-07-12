from ai.agents.nodes import router_node


def test_router_detects_multiple_intents_for_mixed_questions():
    state = {
        "user_query": "what is a bev and which manufacturer has the most registrations",
        "intent": "",
        "detected_intents": [],
    }

    router_node(state)

    assert state["intent"] == "multi_query"
    assert state["detected_intents"] == ["knowledge_query", "statistical_query"]

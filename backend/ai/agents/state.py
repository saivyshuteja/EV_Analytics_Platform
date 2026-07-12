from typing import TypedDict
from typing import Annotated

from langgraph.graph.message import (
    add_messages
)


class AgentState(TypedDict):

    messages: Annotated[
        list,
        add_messages
    ]

    user_query: str

    intent: str

    analysis_result: dict | None

    ml_prediction: dict | None

    rag_context: str | None

    final_answer: str | None

    current_node: str

    iteration_count: int

    detected_intents: list[str]
from pathlib import Path
import sys


BACKEND_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BACKEND_DIR))

from ai.agents.graph import (
    graph
)

response = graph.invoke(

    {

        "messages": [],

        "user_query":
        "Which EV manufacturer has highest registrations?",

        "intent": "",

        "analysis_result": None,

        "ml_prediction": None,

        "rag_context": None,

        "final_answer": None,

        "current_node": "",

        "iteration_count": 0
    }
)

print(

    response["final_answer"]
)

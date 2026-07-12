from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class AgentRequest(BaseModel):
    query: str

@router.post("/chat")
def chat(request: AgentRequest):
    from ai.agents.graph import graph

    result = graph.invoke(
        {
            "messages": [],
            "user_query": request.query,
            "intent": "",
            "analysis_result": None,
            "ml_prediction": None,
            "rag_context": None,
            "final_answer": None,
            "current_node": "",
            "iteration_count": 0,
        }
    )
    return {"response": result.get("final_answer")}

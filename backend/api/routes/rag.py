from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()
rag = None

class QuestionRequest(BaseModel):
    question: str

@router.post("/ask")
def ask_question(request: QuestionRequest):
    global rag
    if rag is None:
        from ai.rag.qa_chain import EVRAGChain

        rag = EVRAGChain()

    return rag.ask(request.question)

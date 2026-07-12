from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes.agent import router as agent_router
from api.routes.analytics import router as analytics_router
from api.routes.health import router as health_router
from api.routes.ml import router as ml_router
from api.routes.rag import router as rag_router


app = FastAPI(
    title="EV Analytics AI Platform",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "EV Analytics AI Platform Running"}


app.include_router(health_router, prefix="/api")
app.include_router(analytics_router, prefix="/api/stats", tags=["Statistics"])
app.include_router(ml_router, prefix="/api/ml", tags=["Machine Learning"])
app.include_router(rag_router, prefix="/api/rag", tags=["RAG"])
app.include_router(agent_router, prefix="/api/agent", tags=["AI Agent"])

from fastapi import FastAPI

from app.models.schemas import (
    ChatRequest,
    ChatResponse
)

from app.services.orchestrator import handle_query


app = FastAPI(
    title="SHL Assessment Recommendation API"
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    return handle_query(request.messages)
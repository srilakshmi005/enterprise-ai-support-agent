from fastapi import FastAPI
from pydantic import BaseModel

from app.agent import generate_answer


app = FastAPI(
    title="Enterprise AI Support Agent",
    description="RAG-powered AI support agent",
    version="1.0.0"
)


class SupportRequest(BaseModel):
    query: str


@app.get("/")
def home():
    return {
        "message": "Enterprise AI Support Agent is running"
    }


@app.post("/support")
def support(request: SupportRequest):

    result = generate_answer(request.query)

    if not result["sources"]:
        return {
            "type": "human_escalation",
            "answer": result["answer"],
            "sources": []
        }

    return {
        "type": "knowledge_answer",
        "answer": result["answer"],
        "sources": result["sources"]
    }

from fastapi import FastAPI
from pydantic import BaseModel

from agent import generate_answer
from tools import create_support_ticket


app = FastAPI(
    title="Enterprise AI Support Agent",
    description="RAG-powered AI support agent with human escalation",
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

    # Escalate when the knowledge base cannot answer
    if not result["sources"]:
        ticket = create_support_ticket(request.query)

        return {
            "type": "human_escalation",
            "answer": result["answer"],
            "ticket": ticket
        }

    return {
        "type": "knowledge_answer",
        "answer": result["answer"],
        "sources": result["sources"]
    }
    

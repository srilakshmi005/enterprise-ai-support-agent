import os
from google import genai

from rag import retrieve_documents


# Gemini client
client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY")
)


def generate_answer(query):
    """Generate an answer using retrieved knowledge."""

    documents = retrieve_documents(
        query,
        top_k=3,
        min_score=0.30
    )

    if not documents:
        return {
            "answer": (
                "I don't have enough information in the knowledge base. "
                "Please contact human IT support."
            ),
            "sources": []
        }

    context = "\n\n".join(
        [
            f"Source: {doc['title']}\n{doc['content']}"
            for doc in documents
        ]
    )

    prompt = f"""
You are an Enterprise IT Support AI Agent.

Answer the user's question using ONLY the knowledge base below.

Do not invent information.

KNOWLEDGE BASE:
{context}

USER QUESTION:
{query}

Give a concise and helpful answer.
At the end, mention the source used.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return {
        "answer": response.text,
        "sources": [doc["title"] for doc in documents]
    }

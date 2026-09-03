
import os
import re

from google import genai

from app.rag import retrieve_documents


# ============================================================
# GEMINI CLIENT
# ============================================================

client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY")
)


# ============================================================
# SUPPORTED SUPPORT TOPICS
# ============================================================

SUPPORTED_TOPICS = {
    "password": [
        "password",
        "forgot password",
        "reset password",
        "password expired",
        "forgotten password"
    ],

    "wifi": [
        "wifi",
        "wi-fi",
        "wireless",
        "internet connection"
    ],

    "vpn": [
        "vpn",
        "remote access",
        "work from home",
        "working remotely",
        "company systems from home"
    ],

    "laptop": [
        "laptop",
        "computer",
        "keyboard",
        "screen",
        "device",
        "won't turn on",
        "does not turn on"
    ],

    "printer": [
        "printer",
        "printing",
        "print",
        "paper jam"
    ],

    "security": [
        "phishing",
        "suspicious email",
        "suspicious link",
        "security email"
    ],

    "account": [
        "login",
        "log in",
        "account locked",
        "locked out",
        "username",
        "account"
    ]
}


# ============================================================
# NORMALIZE
# ============================================================

def normalize(text):

    text = text.lower()

    text = re.sub(
        r"[^a-z0-9\s-]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ============================================================
# DETECT SUPPORT TOPIC
# ============================================================

def detect_support_topic(query):

    query = normalize(query)

    for topic, phrases in SUPPORTED_TOPICS.items():

        for phrase in phrases:

            if normalize(phrase) in query:
                return topic

    return None


# ============================================================
# GENERATE ANSWER
# ============================================================

def generate_answer(query):

    # Explicitly handle unsupported employee ID-card questions
    normalized_query = query.lower()

    id_card_phrases = [
        "employee id card",
        "employee id",
        "id card",
        "lost id card",
        "lost employee card",
        "badge",
        "lost badge"
    ]

    if any(phrase in normalized_query for phrase in id_card_phrases):
        return {
            "answer": (
                "I don't have enough information in the knowledge base. "
                "Please contact human IT support."
            ),
            "sources": []
        }


    if not query or not query.strip():
        return {
            "answer": "Please provide your support question.",
            "sources": []
        }

    topic = detect_support_topic(query)

    documents = retrieve_documents(
        query,
        top_k=3,
        min_score=0.50
    )

    # Reject unrelated questions
    if topic is None:

        if not documents or documents[0]["score"] < 0.60:
            return {
                "answer": (
                    "I don't have enough information in the "
                    "knowledge base. Please contact human IT support."
                ),
                "sources": []
            }

    # No knowledge found
    if not documents:
        return {
            "answer": (
                "I don't have enough information in the "
                "knowledge base. Please contact human IT support."
            ),
            "sources": []
        }

    # Use the best retrieved knowledge-base answer directly.
    # This avoids unnecessary Gemini API calls and quota usage.
    best = documents[0]

    answer = (
        f"{best['content']}\n\n"
        f"Source: {best['title']}"
    )

    sources = [
        doc["title"]
        for doc in documents
    ]

    return {
        "answer": answer,
        "sources": sources
    }

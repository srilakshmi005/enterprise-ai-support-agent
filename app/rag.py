
import json
import os
import re
import numpy as np

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# ============================================================
# LOAD KNOWLEDGE BASE
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

DATA_FILE = os.path.join(
    BASE_DIR,
    "data",
    "knowledge_base.json"
)

with open(DATA_FILE, "r", encoding="utf-8") as file:
    documents = json.load(file)


# ============================================================
# SEMANTIC MODEL
# ============================================================

model = SentenceTransformer("all-MiniLM-L6-v2")

texts = [
    f"{doc['title']}. {doc['content']}"
    for doc in documents
]

document_embeddings = model.encode(
    texts,
    normalize_embeddings=True,
    show_progress_bar=False
)


# ============================================================
# INTENT PHRASES
# ============================================================

LOCKOUT_PHRASES = [
    "too many attempts",
    "multiple failed attempts",
    "wrong password too many times",
    "wrong password many times",
    "account locked",
    "account lockout",
    "locked out",
    "unlock account",
    "unlock my account"
]

VPN_PHRASES = [
    "vpn",
    "remote access",
    "work from home",
    "working remotely",
    "company systems from home",
    "remote company access",
    "access company systems from home"
]

WIFI_PHRASES = [
    "wifi",
    "wi-fi",
    "wireless",
    "wireless internet",
    "wireless network"
]

PASSWORD_RESET_PHRASES = [
    "reset password",
    "forgot password",
    "forgotten password",
    "lost password",
    "can't remember my password",
    "cannot remember my password"
]


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
# SPECIFIC INTENT
# ============================================================

def detect_specific_intent(query):

    query = normalize(query)

    for phrase in LOCKOUT_PHRASES:
        if normalize(phrase) in query:
            return "account_lockout"

    for phrase in VPN_PHRASES:
        if normalize(phrase) in query:
            return "vpn"

    for phrase in WIFI_PHRASES:
        if normalize(phrase) in query:
            return "wifi"

    for phrase in PASSWORD_RESET_PHRASES:
        if normalize(phrase) in query:
            return "password_reset"

    return None


# ============================================================
# DOCUMENT INTENT MATCHING
# ============================================================

def matches_intent(title, content, intent):

    title_text = normalize(title)
    content_text = normalize(content)

    text = f"{title_text} {content_text}"

    if intent == "account_lockout":
        return (
            "account lockout" in title_text
            or "unlock company account" in title_text
            or "account locked" in text
            or ("unlock" in text and "account" in text)
        )

    if intent == "vpn":
        return (
            "vpn" in text
            or "remote access" in text
        )

    if intent == "wifi":
        return (
            "wifi" in text
            or "wireless" in text
        )

    if intent == "password_reset":
        return (
            "password reset" in title_text
            or "forgotten password" in title_text
            or "forgot password" in title_text
        )

    return False


# ============================================================
# RETRIEVE DOCUMENTS
# ============================================================

def retrieve_documents(
    query,
    top_k=3,
    min_score=0.50
):

    if not query or not query.strip():
        return []

    specific_intent = detect_specific_intent(query)

    # --------------------------------------------------------
    # HARD INTENT ROUTING
    # --------------------------------------------------------

    if specific_intent:

        matching_indices = []

        for idx, doc in enumerate(documents):

            if matches_intent(
                doc["title"],
                doc["content"],
                specific_intent
            ):
                matching_indices.append(idx)

        if matching_indices:

            query_embedding = model.encode(
                [query],
                normalize_embeddings=True
            )

            candidate_embeddings = (
                document_embeddings[matching_indices]
            )

            scores = cosine_similarity(
                query_embedding,
                candidate_embeddings
            )[0]

            ranked = np.argsort(scores)[::-1]

            results = []

            for position in ranked[:top_k]:

                idx = matching_indices[position]

                score = float(scores[position])

                if score >= min_score:
                    results.append({
                        "title": documents[idx]["title"],
                        "content": documents[idx]["content"],
                        "score": score
                    })

            return results

    # --------------------------------------------------------
    # NORMAL SEMANTIC SEARCH
    # --------------------------------------------------------

    query_embedding = model.encode(
        [query],
        normalize_embeddings=True
    )

    scores = cosine_similarity(
        query_embedding,
        document_embeddings
    )[0]

    ranked_indices = np.argsort(scores)[::-1]

    results = []

    for idx in ranked_indices[:top_k]:

        score = float(scores[idx])

        if score >= min_score:

            results.append({
                "title": documents[idx]["title"],
                "content": documents[idx]["content"],
                "score": score
            })

    return results

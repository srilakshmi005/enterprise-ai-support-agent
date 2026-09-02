import json
import os

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ============================================================
# LOAD KNOWLEDGE BASE
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "data", "knowledge_base.json")

with open(DATA_FILE, "r", encoding="utf-8") as file:
    documents = json.load(file)


# ============================================================
# PREPARE KNOWLEDGE
# ============================================================

texts = []

for doc in documents:
    texts.append(
        f"{doc['title']} {doc['content']}"
    )


# ============================================================
# LIGHTWEIGHT RAG RETRIEVER
# ============================================================

word_vectorizer = TfidfVectorizer(
    lowercase=True,
    stop_words="english",
    ngram_range=(1, 2),
    sublinear_tf=True
)

word_matrix = word_vectorizer.fit_transform(texts)


# Character-level matching helps handle
# different ways users type words.

char_vectorizer = TfidfVectorizer(
    lowercase=True,
    analyzer="char_wb",
    ngram_range=(3, 5),
    sublinear_tf=True
)

char_matrix = char_vectorizer.fit_transform(texts)


# ============================================================
# RETRIEVE DOCUMENTS
# ============================================================

def retrieve_documents(query, top_k=3, min_score=0.60):
    """
    Retrieve relevant company knowledge.

    Users do not need to use the exact wording
    from the knowledge base.
    """

    if not query or not query.strip():
        return []

    # Convert user's question into vectors
    word_query = word_vectorizer.transform([query])
    char_query = char_vectorizer.transform([query])

    # Calculate similarity
    word_scores = cosine_similarity(
        word_query,
        word_matrix
    )[0]

    char_scores = cosine_similarity(
        char_query,
        char_matrix
    )[0]

    # Combine both similarity scores
    scores = (
        0.70 * word_scores +
        0.30 * char_scores
    )

    # Select the best documents
    ranked_indices = np.argsort(scores)[::-1][:top_k]

    results = []

    for idx in ranked_indices:

        score = float(scores[idx])

        if score >= min_score:
            results.append({
                "title": documents[idx]["title"],
                "content": documents[idx]["content"],
                "score": score
            })

    return results

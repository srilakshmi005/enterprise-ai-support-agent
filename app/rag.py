import json
import os

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from google import genai


# Load knowledge base
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "data", "knowledge_base.json")

with open(DATA_FILE, "r", encoding="utf-8") as file:
    documents = json.load(file)


# Load embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


# Create document embeddings
texts = [doc["content"] for doc in documents]

embeddings = embedding_model.encode(
    texts,
    normalize_embeddings=True
)


# Create FAISS index
dimension = embeddings.shape[1]

index = faiss.IndexFlatIP(dimension)

index.add(
    np.array(embeddings).astype("float32")
)


def retrieve_documents(query, top_k=3, min_score=0.60):
    """Find the most relevant knowledge-base documents."""

    query_embedding = embedding_model.encode(
        [query],
        normalize_embeddings=True
    )

    scores, indices = index.search(
        np.array(query_embedding).astype("float32"),
        top_k
    )

    results = []

    for score, idx in zip(scores[0], indices[0]):

        if float(score) >= min_score:
            results.append({
                "title": documents[idx]["title"],
                "content": documents[idx]["content"],
                "score": float(score)
            })

    return results

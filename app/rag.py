import json
import os
import numpy as np
from sentence_transformers import SentenceTransformer

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, 'data', 'knowledge_base.json')

with open(DATA_FILE, 'r', encoding='utf-8') as file:
    documents = json.load(file)

# Semantic model understands meaning instead of exact wording
model = SentenceTransformer('all-MiniLM-L6-v2')

texts = [
    f"{doc['title']}. {doc['content']}"
    for doc in documents
]

document_embeddings = model.encode(
    texts,
    normalize_embeddings=True,
    show_progress_bar=False
)

def retrieve_documents(query, top_k=3, min_score=0.40):
    if not query or not query.strip():
        return []

    query_embedding = model.encode(
        [query],
        normalize_embeddings=True,
        show_progress_bar=False
    )[0]

    scores = np.dot(document_embeddings, query_embedding)
    ranked_indices = np.argsort(scores)[::-1][:top_k]

    results = []

    for idx in ranked_indices:
        score = float(scores[idx])

        if score >= min_score:
            results.append({
                'title': documents[idx]['title'],
                'content': documents[idx]['content'],
                'score': score
            })

    return results
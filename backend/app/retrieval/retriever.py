import pickle
import faiss

from pathlib import Path
from sentence_transformers import SentenceTransformer

from app.retrieval.reranker import rerank_results


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

BASE_DIR = Path(__file__).resolve().parents[2]

FAISS_PATH = BASE_DIR / "data" / "faiss.index"
METADATA_PATH = BASE_DIR / "data" / "metadata.pkl"

model = SentenceTransformer(MODEL_NAME)

index = faiss.read_index(str(FAISS_PATH))

with open(METADATA_PATH, "rb") as f:
    metadata = pickle.load(f)


def retrieve_assessments(query: str, top_k: int = 5):

    query_embedding = model.encode([query])

    candidate_pool = max(top_k * 3, 15)

    distances, indices = index.search(
        query_embedding,
        candidate_pool
    )

    results = []

    for idx in indices[0]:
        results.append(metadata[idx])

    reranked = rerank_results(query, results)

    return reranked[:top_k]


if __name__ == "__main__":

    test_query = "Executive leadership benchmark"

    results = retrieve_assessments(test_query)

    for i, item in enumerate(results, start=1):
        print(f"{i}. {item['name']}")
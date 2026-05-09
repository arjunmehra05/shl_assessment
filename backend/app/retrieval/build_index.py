import json
import pickle
import faiss
import numpy as np
from pathlib import Path

from sentence_transformers import SentenceTransformer


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

BASE_DIR = Path(__file__).resolve().parents[2]

CATALOG_PATH = BASE_DIR / "data" / "catalog.json"
FAISS_PATH = BASE_DIR / "data" / "faiss.index"
METADATA_PATH = BASE_DIR / "data" / "metadata.pkl"


def build_embedding_text(item):
    return f"""
    Assessment Name: {item['name']}

    Description:
    {item['description']}

    Job Levels:
    {', '.join(item['job_levels'])}

    Categories:
    {', '.join(item['categories'])}

    Remote Testing:
    {'Yes' if item['remote'] else 'No'}

    Adaptive Testing:
    {'Yes' if item['adaptive'] else 'No'}
    """


def main():
    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    texts = [build_embedding_text(item) for item in catalog]

    model = SentenceTransformer(MODEL_NAME)

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        show_progress_bar=True
    )

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(np.array(embeddings))

    faiss.write_index(index, str(FAISS_PATH))

    with open(METADATA_PATH, "wb") as f:
        pickle.dump(catalog, f)

    print("FAISS index saved")
    print(f"Indexed {len(catalog)} assessments")


if __name__ == "__main__":
    main()
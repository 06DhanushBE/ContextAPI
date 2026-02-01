from qdrant_client.models import VectorParams, Distance
from app.db.qdrant import qdrant

COLLECTION_NAME = "chatbot_docs"

def create_collection():
    collections = qdrant.get_collections().collections
    if any(c.name == COLLECTION_NAME for c in collections):
        print(" Collection already exists")
        return

    qdrant.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=384,   # embedding size
            distance=Distance.COSINE
        )
    )

    print(" Collection created:", COLLECTION_NAME)

if __name__ == "__main__":
    create_collection()

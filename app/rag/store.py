import uuid
from app.db.qdrant import qdrant
from app.rag.embeddings import embed_text

COLLECTION_NAME = "chatbot_docs"

def store_text(text: str, client_id: int, doc_id: str):
    vector = embed_text(text)

    qdrant.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            {
                "id": str(uuid.uuid4()),
                "vector": vector,
                "payload": {
                    "client_id": client_id,   # ✅ INTEGER
                    "doc_id": doc_id,
                    "text": text
                }
            }
        ]
    )

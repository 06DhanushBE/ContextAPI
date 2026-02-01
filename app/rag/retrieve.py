from app.db.qdrant import qdrant
from app.rag.embeddings import embed_text
from qdrant_client.models import Filter, FieldCondition, MatchValue

COLLECTION_NAME = "chatbot_docs"

def retrieve_text(query: str, client_id: int, limit: int = 3):
    query_vector = embed_text(query)

    results = qdrant.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=limit,
        with_payload=True,
        query_filter=Filter(
            must=[
                FieldCondition(
                    key="client_id",
                    match=MatchValue(value=client_id)  # ✅ INTEGER MATCH
                )
            ]
        )
    )

    return [point.payload["text"] for point in results.points]

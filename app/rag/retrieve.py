from app.db.qdrant import qdrant
from app.rag.embeddings import embed_text
from qdrant_client.models import Filter, FieldCondition, MatchValue

COLLECTION_NAME = "chatbot_docs"

def retrieve_text(query: str, api_key_id: int, limit: int = 3):
    """Retrieve relevant text chunks for a specific API key's knowledge base"""
    query_vector = embed_text(query)

    results = qdrant.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=limit,
        with_payload=True,
        query_filter=Filter(
            must=[
                FieldCondition(
                    key="api_key_id",
                    match=MatchValue(value=api_key_id)
                )
            ]
        )
    )

    return [point.payload["text"] for point in results.points]

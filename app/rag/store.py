import uuid
from app.db.qdrant import qdrant
from app.rag.embeddings import embed_text

COLLECTION_NAME = "chatbot_docs"

def store_text(text: str, api_key_id: int, document_id: int):
    """Store text chunk in Qdrant with api_key_id and document_id for isolation"""
    vector = embed_text(text)

    qdrant.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            {
                "id": str(uuid.uuid4()),
                "vector": vector,
                "payload": {
                    "api_key_id": api_key_id,
                    "document_id": document_id,
                    "text": text
                }
            }
        ]
    )

def delete_document_vectors(document_id: int):
    """Delete all vectors for a specific document"""
    from qdrant_client.models import Filter, FieldCondition, MatchValue
    
    qdrant.delete(
        collection_name=COLLECTION_NAME,
        points_selector=Filter(
            must=[
                FieldCondition(
                    key="document_id",
                    match=MatchValue(value=document_id)
                )
            ]
        )
    )

def delete_api_key_vectors(api_key_id: int):
    """Delete all vectors for a specific API key"""
    from qdrant_client.models import Filter, FieldCondition, MatchValue
    
    qdrant.delete(
        collection_name=COLLECTION_NAME,
        points_selector=Filter(
            must=[
                FieldCondition(
                    key="api_key_id",
                    match=MatchValue(value=api_key_id)
                )
            ]
        )
    )

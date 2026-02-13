from app.db.qdrant import qdrant

COLLECTION_NAME = "chatbot_docs"

def create_index():
    # Create index for api_key_id filtering
    qdrant.create_payload_index(
        collection_name=COLLECTION_NAME,
        field_name="api_key_id",
        field_schema="integer"
    )
    
    # Also create index for document_id for deletion
    qdrant.create_payload_index(
        collection_name=COLLECTION_NAME,
        field_name="document_id",
        field_schema="integer"
    )
    
    print("Payload indexes created for api_key_id and document_id")

if __name__ == "__main__":
    create_index()

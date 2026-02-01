from app.db.qdrant import qdrant

COLLECTION_NAME = "chatbot_docs"

def create_index():
    qdrant.create_payload_index(
        collection_name=COLLECTION_NAME,
        field_name="client_id",
        field_schema="keyword"
    )
    print("Payload index created for client_id")

if __name__ == "__main__":
    create_index()

from app.db.base import SessionLocal
from app.db.models import APIKey
from app.core.security import generate_api_key, hash_api_key

def create_api_key():
    db = SessionLocal()

    raw_key = generate_api_key()
    print("\n SAVE THIS API KEY (YOU WON'T SEE IT AGAIN):\n")
    print(raw_key)

    record = APIKey(
        key_hash=hash_api_key(raw_key),
        client_id="client_demo",
        is_active=True
    )

    db.add(record)
    db.commit()
    db.close()

if __name__ == "__main__":
    create_api_key()

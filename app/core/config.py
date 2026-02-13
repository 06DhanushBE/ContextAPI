import os
from dotenv import load_dotenv

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.db.base import SessionLocal
from app.db.models import APIKey
from app.core.security import hash_api_key

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

# -----------------------
# DB dependency
# -----------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -----------------------
# API Key Security
# -----------------------
security = HTTPBearer(auto_error=True)

def get_api_key_record(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> APIKey:
    api_key = credentials.credentials
    key_hash = hash_api_key(api_key)

    record = (
        db.query(APIKey)
        .filter(
            APIKey.key_hash == key_hash,
            APIKey.is_active == True
        )
        .first()
    )

    if not record:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    return record

# Backward compatibility - returns user_id (client_id)
def get_client_id(
    api_key: APIKey = Depends(get_api_key_record),
) -> int:
    return api_key.user_id

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.core.deps import get_current_user, get_db
from app.db.models import APIKey, Document
from app.core.apikey import generate_api_key
from app.rag.store import delete_api_key_vectors

router = APIRouter(prefix="/keys", tags=["API Keys"])


class CreateKeyRequest(BaseModel):
    llm_provider: str = "groq"


@router.post("")
def create_key(
    data: CreateKeyRequest,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    if data.llm_provider not in ["groq", "openai"]:
        raise HTTPException(status_code=400, detail="Invalid LLM provider. Choose 'groq' or 'openai'")

    raw_key, key_hash = generate_api_key()

    record = APIKey(
        key_hash=key_hash,
        user_id=user.id,
        llm_provider=data.llm_provider
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    return {
        "id": record.id,
        "api_key": raw_key,
        "llm_provider": data.llm_provider,
        "message": "Save this key now. You won’t see it again."
    }

@router.get("")
def list_keys(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    keys = (
        db.query(APIKey)
        .filter(APIKey.user_id == user.id)
        .all()
    )

    return [
        {
            "id": k.id,
            "is_active": k.is_active,
            "llm_provider": k.llm_provider,
            "document_count": db.query(Document).filter(Document.api_key_id == k.id).count()
        }
        for k in keys
    ]

@router.post("/{key_id}/toggle")
def toggle_key(
    key_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    """Toggle API key active/inactive status"""
    key = (
        db.query(APIKey)
        .filter(APIKey.id == key_id, APIKey.user_id == user.id)
        .first()
    )

    if not key:
        raise HTTPException(status_code=404, detail="Key not found")

    key.is_active = not key.is_active
    db.commit()

    return {
        "message": f"API key {'activated' if key.is_active else 'deactivated'}",
        "is_active": key.is_active
    }

@router.delete("/{key_id}")
def delete_key(
    key_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    """Permanently delete an API key and all its documents/vectors"""
    key = (
        db.query(APIKey)
        .filter(APIKey.id == key_id, APIKey.user_id == user.id)
        .first()
    )

    if not key:
        raise HTTPException(status_code=404, detail="API key not found")

    # Count documents before deletion
    doc_count = db.query(Document).filter(Document.api_key_id == key_id).count()

    # Delete all vectors for this API key
    try:
        delete_api_key_vectors(key_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete vectors: {str(e)}")

    # Delete all documents (cascade)
    db.query(Document).filter(Document.api_key_id == key_id).delete()

    # Delete the API key
    db.delete(key)
    db.commit()

    return {
        "status": "deleted",
        "documents_deleted": doc_count
    }

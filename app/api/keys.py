from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, get_db
from app.db.models import APIKey
from app.core.apikey import generate_api_key

router = APIRouter(prefix="/keys", tags=["API Keys"])

@router.post("")
def create_key(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    raw_key, key_hash = generate_api_key()

    record = APIKey(
        key_hash=key_hash,
        user_id=user.id
    )
    db.add(record)
    db.commit()

    return {
        "api_key": raw_key,
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
            "is_active": k.is_active
        }
        for k in keys
    ]

@router.delete("/{key_id}")
def revoke_key(
    key_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    key = (
        db.query(APIKey)
        .filter(APIKey.id == key_id, APIKey.user_id == user.id)
        .first()
    )

    if not key:
        return {"detail": "Not found"}

    key.is_active = False
    db.commit()

    return {"status": "revoked"}

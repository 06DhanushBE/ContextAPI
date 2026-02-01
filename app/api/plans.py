from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.db.models import Plan

router = APIRouter(prefix="/plans", tags=["Plans"])


@router.get("")
def list_plans(db: Session = Depends(get_db)):
    plans = db.query(Plan).all()

    return [
        {
            "id": p.id,
            "name": p.name,
            "price_usd": p.price_usd,
            "limits": {
                "ingested_chars": p.max_ingested_chars,
                "stored_chars": p.max_stored_chars,
                "chat_tokens": p.max_chat_tokens,
            }
        }
        for p in plans
    ]

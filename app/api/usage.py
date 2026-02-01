from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, get_db
from app.db.models import Plan, UserPlan, Usage

router = APIRouter(prefix="/usage", tags=["Usage"])


@router.get("")
def get_usage(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    user_plan = db.query(UserPlan).filter(UserPlan.user_id == user.id).first()
    plan = db.query(Plan).filter(Plan.id == user_plan.plan_id).first()
    usage = db.query(Usage).filter(Usage.user_id == user.id).first()

    return {
        "plan": plan.name,
        "limits": {
            "max_ingested_chars": plan.max_ingested_chars,
            "max_stored_chars": plan.max_stored_chars,
            "max_chat_tokens": plan.max_chat_tokens,
        },
        "usage": {
            "ingested_chars": usage.ingested_chars,
            "stored_chars": usage.stored_chars,
            "chat_tokens": usage.chat_tokens,
        },
        "remaining": {
            "ingested_chars": max(0, plan.max_ingested_chars - usage.ingested_chars),
            "stored_chars": max(0, plan.max_stored_chars - usage.stored_chars),
            "chat_tokens": max(0, plan.max_chat_tokens - usage.chat_tokens),
        }
    }

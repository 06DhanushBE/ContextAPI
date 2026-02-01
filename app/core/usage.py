from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db.models import Plan, UserPlan, Usage

# Approx token estimation (industry-accepted)
def approx_tokens_from_chars(chars: int) -> int:
    return max(1, chars // 4)

def get_user_plan_and_usage(db: Session, user_id: int):
    user_plan = db.query(UserPlan).filter(UserPlan.user_id == user_id).first()
    if not user_plan:
        raise HTTPException(500, "User plan not configured")

    plan = db.query(Plan).filter(Plan.id == user_plan.plan_id).first()
    usage = db.query(Usage).filter(Usage.user_id == user_id).first()

    if not plan or not usage:
        raise HTTPException(500, "Plan or usage missing")

    return plan, usage

def check_ingest_quota(db: Session, user_id: int, new_chars: int):
    plan, usage = get_user_plan_and_usage(db, user_id)

    if usage.ingested_chars + new_chars > plan.max_ingested_chars:
        raise HTTPException(
            status_code=402,
            detail="Monthly ingestion limit exceeded. Upgrade your plan."
        )

    if usage.stored_chars + new_chars > plan.max_stored_chars:
        raise HTTPException(
            status_code=402,
            detail="Knowledge base storage limit reached. Upgrade your plan."
        )

def record_ingest(db: Session, user_id: int, chars: int):
    usage = db.query(Usage).filter(Usage.user_id == user_id).first()
    usage.ingested_chars += chars
    usage.stored_chars += chars
    db.commit()

def check_chat_quota(db: Session, user_id: int, input_chars: int, output_chars: int):
    plan, usage = get_user_plan_and_usage(db, user_id)

    tokens = approx_tokens_from_chars(input_chars + output_chars)

    if usage.chat_tokens + tokens > plan.max_chat_tokens:
        raise HTTPException(
            status_code=402,
            detail="Chat token limit exceeded. Upgrade your plan."
        )

def record_chat(db: Session, user_id: int, input_chars: int, output_chars: int):
    usage = db.query(Usage).filter(Usage.user_id == user_id).first()
    tokens = approx_tokens_from_chars(input_chars + output_chars)
    usage.chat_tokens += tokens
    db.commit()

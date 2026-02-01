from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, get_db
from app.db.models import Plan, UserPlan

router = APIRouter(prefix="/billing", tags=["Billing"])


@router.post("/upgrade/{plan_id}")
def upgrade_plan(
    plan_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    plan = db.query(Plan).filter(Plan.id == plan_id).first()
    if not plan:
        raise HTTPException(404, "Plan not found")

    user_plan = db.query(UserPlan).filter(UserPlan.user_id == user.id).first()
    user_plan.plan_id = plan.id
    db.commit()

    return {
        "status": "upgraded",
        "plan": plan.name,
        "note": "Payment handled externally (Stripe-ready)"
    }

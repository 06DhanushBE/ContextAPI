from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from pydantic import BaseModel

from app.core.deps import get_db, get_current_user
from app.db.models import User, APIKey, Document, UserPlan, Plan, Usage

router = APIRouter(prefix="/admin", tags=["Admin"])


class UserStats(BaseModel):
    id: int
    email: str
    is_active: bool
    plan: str
    api_keys_count: int
    documents_count: int
    total_usage_chars: int


class AdminDashboard(BaseModel):
    total_users: int
    total_api_keys: int
    total_documents: int
    total_vectors: int
    users: List[UserStats]


def is_admin(user: User) -> bool:
    """Check if user is admin (for now, check if email contains 'admin')"""
    return "admin" in user.email.lower()


@router.get("/dashboard", response_model=AdminDashboard)
def get_admin_dashboard(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """Admin dashboard with system statistics"""
    if not is_admin(user):
        raise HTTPException(status_code=403, detail="Admin access required")
    
    # Get total counts
    total_users = db.query(User).count()
    total_api_keys = db.query(APIKey).count()
    total_documents = db.query(Document).count()
    
    # Get all users with their stats
    users_data = []
    all_users = db.query(User).all()
    
    for u in all_users:
        # Get user's plan
        user_plan = db.query(UserPlan).filter(UserPlan.user_id == u.id).first()
        plan_name = "free"
        if user_plan:
            plan = db.query(Plan).filter(Plan.id == user_plan.plan_id).first()
            if plan:
                plan_name = plan.name
        
        # Count API keys
        keys_count = db.query(APIKey).filter(APIKey.user_id == u.id).count()
        
        # Count documents
        docs_count = db.query(Document).join(APIKey).filter(APIKey.user_id == u.id).count()
        
        # Get total usage
        usage = db.query(func.sum(Usage.input_chars + Usage.output_chars)).filter(
            Usage.user_id == u.id
        ).scalar() or 0
        
        users_data.append(UserStats(
            id=u.id,
            email=u.email,
            is_active=u.is_active,
            plan=plan_name,
            api_keys_count=keys_count,
            documents_count=docs_count,
            total_usage_chars=usage
        ))
    
    return AdminDashboard(
        total_users=total_users,
        total_api_keys=total_api_keys,
        total_documents=total_documents,
        total_vectors=0,  # Would need Qdrant query
        users=users_data
    )


@router.post("/users/{user_id}/toggle-active")
def toggle_user_active(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_user)
):
    """Toggle user active status"""
    if not is_admin(admin):
        raise HTTPException(status_code=403, detail="Admin access required")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_active = not user.is_active
    db.commit()
    
    return {"message": f"User {'activated' if user.is_active else 'deactivated'}", "is_active": user.is_active}


@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_user)
):
    """Delete user and all associated data"""
    if not is_admin(admin):
        raise HTTPException(status_code=403, detail="Admin access required")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Delete cascades through API keys -> documents -> vectors
    db.delete(user)
    db.commit()
    
    return {"message": "User deleted successfully"}

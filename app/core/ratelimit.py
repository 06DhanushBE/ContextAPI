from fastapi import Request, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from collections import defaultdict
import time

from app.db.models import User, UserPlan, Plan
from app.core.deps import get_db


# In-memory rate limit tracking (use Redis in production)
rate_limit_store = defaultdict(lambda: {"count": 0, "reset_time": time.time() + 60})


class RateLimiter:
    """Rate limiter based on user's plan"""
    
    PLAN_LIMITS = {
        "free": {
            "requests_per_minute": 10,
            "requests_per_hour": 100,
            "requests_per_day": 500
        },
        "pro": {
            "requests_per_minute": 60,
            "requests_per_hour": 1000,
            "requests_per_day": 10000
        },
        "enterprise": {
            "requests_per_minute": 300,
            "requests_per_hour": 10000,
            "requests_per_day": 100000
        }
    }
    
    @staticmethod
    def check_rate_limit(user_id: int, db: Session, window: str = "minute"):
        """Check if user has exceeded rate limit for their plan"""
        # Get user's plan
        user_plan = db.query(UserPlan).filter(UserPlan.user_id == user_id).first()
        if not user_plan:
            plan_name = "free"
        else:
            plan = db.query(Plan).filter(Plan.id == user_plan.plan_id).first()
            plan_name = plan.name if plan else "free"
        
        # Get limits for this plan
        limits = RateLimiter.PLAN_LIMITS.get(plan_name, RateLimiter.PLAN_LIMITS["free"])
        
        # Check rate limit (simplified in-memory version)
        key = f"{user_id}:{window}"
        now = time.time()
        
        if now > rate_limit_store[key]["reset_time"]:
            # Reset window
            rate_limit_store[key] = {
                "count": 1,
                "reset_time": now + 60 if window == "minute" else now + 3600
            }
            return True
        
        # Check limit
        limit_key = f"requests_per_{window}"
        max_requests = limits.get(limit_key, limits["requests_per_minute"])
        
        if rate_limit_store[key]["count"] >= max_requests:
            raise HTTPException(
                status_code=429,
                detail=f"Rate limit exceeded for {plan_name} plan. Limit: {max_requests} requests per {window}. Upgrade your plan for higher limits."
            )
        
        rate_limit_store[key]["count"] += 1
        return True


async def rate_limit_middleware(request: Request, call_next):
    """Middleware to apply rate limiting on protected routes"""
    # Skip rate limiting for public routes
    if request.url.path in ["/", "/auth/signup", "/auth/login", "/health", "/docs", "/openapi.json"]:
        return await call_next(request)
    
    # Get user_id from request state (set by auth middleware)
    user_id = getattr(request.state, "user_id", None)
    
    if user_id:
        # Get DB session
        db = next(get_db())
        try:
            RateLimiter.check_rate_limit(user_id, db, window="minute")
        finally:
            db.close()
    
    response = await call_next(request)
    return response

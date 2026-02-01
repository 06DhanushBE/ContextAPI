from fastapi import APIRouter, Depends
from app.core.config import get_client_id

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("")
def health_check():
    return {"status": "healthy"}

@router.get("/secure")
def secure_health(client_id: str = Depends(get_client_id)):
    return {"status": "ok", "client": client_id}

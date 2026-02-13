from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from datetime import datetime

from app.core.deps import get_db, get_current_user
from app.db.models import Document, APIKey
from app.rag.store import delete_document_vectors

router = APIRouter(prefix="/documents", tags=["Documents"])


class DocumentResponse(BaseModel):
    id: int
    api_key_id: int
    filename: str
    char_count: int
    chunk_count: int
    created_at: datetime

    class Config:
        from_attributes = True


@router.get("/api-key/{api_key_id}", response_model=List[DocumentResponse])
def list_documents(
    api_key_id: int,
    user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all documents for a specific API key"""
    # Verify API key belongs to user
    api_key = db.query(APIKey).filter(
        APIKey.id == api_key_id,
        APIKey.user_id == user.id
    ).first()
    
    if not api_key:
        raise HTTPException(status_code=404, detail="API key not found")

    documents = db.query(Document).filter(
        Document.api_key_id == api_key_id
    ).order_by(Document.created_at.desc()).all()

    return documents


@router.delete("/{document_id}")
def delete_document(
    document_id: int,
    user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a document and all its vectors"""
    # Get document and verify ownership
    document = db.query(Document).filter(Document.id == document_id).first()
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Verify user owns the API key
    api_key = db.query(APIKey).filter(
        APIKey.id == document.api_key_id,
        APIKey.user_id == user.id
    ).first()
    
    if not api_key:
        raise HTTPException(status_code=403, detail="Not authorized")

    # Delete vectors from Qdrant
    try:
        delete_document_vectors(document.id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete vectors: {str(e)}")

    # Delete document record
    db.delete(document)
    db.commit()

    return {
        "status": "success",
        "message": f"Document '{document.filename}' deleted",
        "chars_freed": document.char_count
    }

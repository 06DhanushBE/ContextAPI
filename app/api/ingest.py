import hashlib
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from app.core.config import get_api_key_record, get_client_id
from app.core.deps import get_db
from app.core.usage import check_ingest_quota, record_ingest
from app.ingest.pdf import extract_text_from_pdf
from app.ingest.chunk import chunk_text
from app.rag.store import store_text
from app.db.models import APIKey, Document

security = HTTPBearer()

router = APIRouter(
    prefix="/ingest",
    tags=["Ingestion"],
    dependencies=[Depends(security)]
)

# Hard guardrail (prevents abuse)
MAX_SINGLE_UPLOAD_CHARS = 500_000  # ~125k tokens


@router.post("")
def ingest_pdf(
    file: UploadFile = File(...),
    api_key: APIKey = Depends(get_api_key_record),
    db: Session = Depends(get_db)
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files supported")

    text = extract_text_from_pdf(file.file)

    if not text.strip():
        raise HTTPException(status_code=400, detail="Empty PDF")

    char_count = len(text)
    file_hash = hashlib.md5(text.encode()).hexdigest()

    # Check for duplicate
    existing = db.query(Document).filter(
        Document.api_key_id == api_key.id,
        Document.file_hash == file_hash
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Document already uploaded")

    # Single-file guardrail
    if char_count > MAX_SINGLE_UPLOAD_CHARS:
        raise HTTPException(
            status_code=402,
            detail="File too large for your current plan"
        )

    # Enforce quota BEFORE chunking / embedding
    check_ingest_quota(db, api_key.user_id, char_count)

    chunks = chunk_text(text)

    # Create document record
    document = Document(
        api_key_id=api_key.id,
        filename=file.filename,
        file_hash=file_hash,
        char_count=char_count,
        chunk_count=len(chunks)
    )
    db.add(document)
    db.commit()
    db.refresh(document)

    # Store chunks with document_id
    for chunk in chunks:
        store_text(
            text=chunk,
            api_key_id=api_key.id,
            document_id=document.id
        )

    # Record usage AFTER success
    record_ingest(db, api_key.user_id, char_count)

    return {
        "status": "success",
        "document_id": document.id,
        "filename": file.filename,
        "chars_added": char_count,
        "chunks_added": len(chunks)
    }

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from app.core.config import get_client_id
from app.core.deps import get_db
from app.core.usage import check_ingest_quota, record_ingest
from app.ingest.pdf import extract_text_from_pdf
from app.ingest.chunk import chunk_text
from app.rag.store import store_text

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
    client_id: str = Depends(get_client_id),
    db: Session = Depends(get_db)
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files supported")

    text = extract_text_from_pdf(file.file)

    if not text.strip():
        raise HTTPException(status_code=400, detail="Empty PDF")

    char_count = len(text)

    # Single-file guardrail
    if char_count > MAX_SINGLE_UPLOAD_CHARS:
        raise HTTPException(
            status_code=402,
            detail="File too large for your current plan"
        )

    # Enforce quota BEFORE chunking / embedding
    check_ingest_quota(db, client_id, char_count)

    chunks = chunk_text(text)

    for chunk in chunks:
        store_text(
            text=chunk,
            client_id=client_id,
            doc_id=file.filename
        )

    # Record usage AFTER success
    record_ingest(db, client_id, char_count)

    return {
        "status": "success",
        "chars_added": char_count,
        "chunks_added": len(chunks),
        "document": file.filename
    }

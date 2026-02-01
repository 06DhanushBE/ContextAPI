from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.config import get_client_id
from app.core.deps import get_db
from app.core.usage import check_chat_quota, record_chat
from app.rag.retrieve import retrieve_text
from app.rag.prompt import build_prompt
from app.llm.ollama import generate_answer

router = APIRouter(prefix="/chat", tags=["Chat"])


class ChatRequest(BaseModel):
    query: str


class ChatResponse(BaseModel):
    answer: str


@router.post("", response_model=ChatResponse)
def chat(
    data: ChatRequest,
    client_id: str = Depends(get_client_id),
    db: Session = Depends(get_db)
):
    if not data.query.strip():
        raise HTTPException(status_code=400, detail="Empty query")

    input_chars = len(data.query)

    # Retrieve context (retrieval itself is not billed)
    context = retrieve_text(
        query=data.query,
        client_id=client_id
    )

    prompt = build_prompt(context, data.query)

    # Generate answer using local LLM
    answer = generate_answer(prompt)

    output_chars = len(answer)

    # Enforce quota BEFORE recording
    check_chat_quota(
        db,
        client_id,
        input_chars=input_chars,
        output_chars=output_chars
    )

    # Record usage AFTER success
    record_chat(
        db,
        client_id,
        input_chars=input_chars,
        output_chars=output_chars
    )

    return {"answer": answer}

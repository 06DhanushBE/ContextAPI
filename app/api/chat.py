from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.config import get_api_key_record
from app.core.deps import get_db
from app.core.usage import check_chat_quota, record_chat
from app.rag.retrieve import retrieve_text
from app.rag.prompt import build_prompt
from app.llm.provider import get_llm_provider
from app.db.models import APIKey

router = APIRouter(prefix="/chat", tags=["Chat"])


class ChatRequest(BaseModel):
    query: str


class ChatResponse(BaseModel):
    answer: str


@router.post("", response_model=ChatResponse)
def chat(
    data: ChatRequest,
    api_key: APIKey = Depends(get_api_key_record),
    db: Session = Depends(get_db)
):
    if not data.query.strip():
        raise HTTPException(status_code=400, detail="Empty query")

    input_chars = len(data.query)

    # Retrieve context from THIS API key's knowledge base
    context = retrieve_text(
        query=data.query,
        api_key_id=api_key.id
    )

    if not context:
        raise HTTPException(
            status_code=404,
            detail="No documents found. Please upload documents first."
        )

    prompt = build_prompt(context, data.query)

    # Generate answer using THIS API key's configured LLM provider
    llm = get_llm_provider(api_key.llm_provider)
    answer = llm.generate(prompt)

    output_chars = len(answer)

    # Enforce quota BEFORE recording
    check_chat_quota(
        db,
        api_key.user_id,
        input_chars=input_chars,
        output_chars=output_chars
    )

    # Record usage AFTER success
    record_chat(
        db,
        api_key.user_id,
        input_chars=input_chars,
        output_chars=output_chars
    )

    return {"answer": answer}

@router.post("/stream")
async def chat_stream(
    data: ChatRequest,
    api_key: APIKey = Depends(get_api_key_record),
    db: Session = Depends(get_db)
):
    """Streaming chat endpoint for real-time responses"""
    if not data.query.strip():
        raise HTTPException(status_code=400, detail="Empty query")

    input_chars = len(data.query)

    # Retrieve context from THIS API key's knowledge base
    context = retrieve_text(
        query=data.query,
        api_key_id=api_key.id
    )

    if not context:
        raise HTTPException(
            status_code=404,
            detail="No documents found. Please upload documents first."
        )

    prompt = build_prompt(context, data.query)

    # Check quota before streaming
    check_chat_quota(db, api_key.user_id, input_chars=input_chars, output_chars=512)

    # Generate streaming response using THIS API key's LLM provider
    llm = get_llm_provider(api_key.llm_provider)

    async def stream_generator():
        full_response = ""
        try:
            for chunk in llm.generate_stream(prompt):
                full_response += chunk
                yield f"data: {chunk}\n\n"
            
            # Record actual usage after streaming
            output_chars = len(full_response)
            record_chat(db, api_key.user_id, input_chars=input_chars, output_chars=output_chars)
            
            yield "data: [DONE]\n\n"
        except Exception as e:
            yield f"data: [ERROR] {str(e)}\n\n"

    return StreamingResponse(stream_generator(), media_type="text/event-stream")
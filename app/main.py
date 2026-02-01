from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.chat import router as chat_router
from app.db.base import Base, engine
from app.db import models  # REQUIRED for table creation
from app.api.ingest import router as ingest_router
from app.api.auth import router as auth_router
from app.api.keys import router as keys_router
from app.api import usage, plans, billing

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Multi-Tenant Chatbot API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # SvelteKit dev
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers AFTER app is created
app.include_router(health_router)
app.include_router(chat_router)
app.include_router(ingest_router)
app.include_router(auth_router)
app.include_router(keys_router)
app.include_router(usage.router)
app.include_router(plans.router)
app.include_router(billing.router)


# Create tables
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"status": "ok"}

from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlalchemy import text
from api.endpoints import grading, knowledge
from core.database import engine, Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    # In a real production app, use migrations (Alembic)
    # This will create tables if they don't exist
    async with engine.begin() as conn:
        # Enable pgvector extension if not exists
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title="Gemini Exam Grading System", lifespan=lifespan)

app.include_router(grading.router, prefix="/api/v1", tags=["grading"])
app.include_router(knowledge.router, prefix="/api/v1", tags=["knowledge"])

@app.get("/")
async def root():
    return {"message": "Welcome to Gemini Exam Grading System API"}

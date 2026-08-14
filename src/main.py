from fastapi import FastAPI
from src.api.v1.router import router as v1_router
from src.search import ensure_index
from src.database import engine
from src.models import Base
import asyncio

app = FastAPI(title="SearchCraft", version="1.0.0")

app.include_router(v1_router, prefix="/api/v1")

@app.on_event("startup")
async def startup():
    # Create tables if not exist (in production we use migrations)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    # Ensure Meilisearch index exists
    ensure_index()
    # Note: triggers are created via migrations, not here.

@app.get("/health")
async def health():
    return {"status": "ok"}

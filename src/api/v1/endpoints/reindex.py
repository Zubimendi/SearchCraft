from fastapi import APIRouter, BackgroundTasks
from src.reindex import reindex

router = APIRouter(prefix="/reindex", tags=["reindex"])

@router.post("/")
async def start_reindex(background_tasks: BackgroundTasks):
    """Trigger a full reindex with zero downtime. Returns immediately."""
    background_tasks.add_task(reindex)
    return {"message": "Reindex started in background. Check logs for progress."}

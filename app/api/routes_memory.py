"""Memory endpoint routes."""

from fastapi import APIRouter, Depends, HTTPException

from app.core.config import get_settings
from app.core.security import require_local_api_token
from app.models.memory import MemoryListResponse, MemoryRecord
from app.services.memory_service import MemoryService

router = APIRouter(tags=["memory"], dependencies=[Depends(require_local_api_token)])


@router.get("/memory", response_model=MemoryListResponse)
def list_memory() -> MemoryListResponse:
    """Return all allowed memory-bank records."""
    settings = get_settings()
    memory_service = MemoryService(settings.memory_bank_dir)

    return MemoryListResponse(records=memory_service.list_records())


@router.get("/memory/{record_id}", response_model=MemoryRecord)
def get_memory_record(record_id: str) -> MemoryRecord:
    """Return a single memory-bank record by ID."""
    settings = get_settings()
    memory_service = MemoryService(settings.memory_bank_dir)
    record = memory_service.get_record(record_id)

    if record is None:
        raise HTTPException(status_code=404, detail="Memory record not found")

    return record

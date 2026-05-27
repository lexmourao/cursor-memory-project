"""Health endpoint routes."""

from fastapi import APIRouter

from app.core.config import get_settings
from app.models.health import HealthResponse
from app.services.memory_service import MemoryService


router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    """Return service health and memory-bank status."""
    settings = get_settings()
    memory_service = MemoryService(settings.memory_bank_dir)
    records = memory_service.list_records()

    return HealthResponse(
        status="ok",
        service=settings.service_name,
        mode=settings.runtime_mode,
        memory_bank_exists=memory_service.memory_bank_exists(),
        memory_record_count=len(records),
    )

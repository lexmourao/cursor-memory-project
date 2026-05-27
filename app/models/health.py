"""Health-check response models."""

from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Response returned by the health endpoint."""

    status: str
    service: str
    mode: str
    memory_bank_exists: bool
    memory_record_count: int

"""Memory API response models."""

from pydantic import BaseModel


class MemoryRecord(BaseModel):
    """A markdown memory record loaded from the memory-bank."""

    id: str
    source: str
    type: str
    content: str


class MemoryListResponse(BaseModel):
    """Response returned by the memory list endpoint."""

    records: list[MemoryRecord]

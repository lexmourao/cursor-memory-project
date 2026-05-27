"""Chunk metadata models for retrieval and memory inspection workflows."""

from pydantic import BaseModel, Field


class ChunkMetadata(BaseModel):
    """Metadata that identifies where a retrieved chunk came from."""

    source: str = Field(..., min_length=1)
    chunk_idx: int = Field(..., ge=0)


class RetrievedChunk(ChunkMetadata):
    """A retrieved chunk with score and text content."""

    score: float
    text: str

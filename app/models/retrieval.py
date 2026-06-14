"""Retrieval API request and response models."""

from typing import Literal

from pydantic import BaseModel, Field

from app.models.chunk import RetrievedChunk

EmbeddingMode = Literal["openai", "zero_vector_fallback", "missing_index", "unknown"]


class RetrievalRequest(BaseModel):
    """Request body for retrieval queries."""

    query: str = Field(..., min_length=1)
    top_k: int = Field(default=5, ge=1, le=20)


class RetrievalResult(RetrievedChunk):
    """Single retrieval result returned by the retrieval API."""


class RetrievalResponse(BaseModel):
    """Response returned by the retrieval query endpoint."""

    query: str
    results: list[RetrievalResult]


class RetrievalStatusResponse(BaseModel):
    """Response returned by the retrieval status endpoint."""

    index_exists: bool
    metadata_exists: bool
    json_export_exists: bool
    index_vector_count: int
    metadata_record_count: int
    json_record_count: int
    ready: bool
    embedding_mode: EmbeddingMode

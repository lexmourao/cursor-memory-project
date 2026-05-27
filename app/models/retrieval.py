"""Retrieval API request and response models."""

from pydantic import BaseModel, Field


class RetrievalRequest(BaseModel):
    """Request body for retrieval queries."""

    query: str = Field(..., min_length=1)
    top_k: int = Field(default=5, ge=1, le=20)


class RetrievalResult(BaseModel):
    """Single retrieval result returned by the retrieval API."""

    score: float
    source: str
    text: str


class RetrievalResponse(BaseModel):
    """Response returned by the retrieval query endpoint."""

    query: str
    results: list[RetrievalResult]

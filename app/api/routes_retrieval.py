"""Retrieval endpoint routes."""

from fastapi import APIRouter

from app.models.retrieval import (
    RetrievalRequest,
    RetrievalResponse,
    RetrievalStatusResponse,
)
from app.services.retrieval_service import RetrievalService


router = APIRouter(prefix="/retrieval", tags=["retrieval"])


@router.get("/status", response_model=RetrievalStatusResponse)
def retrieval_status() -> RetrievalStatusResponse:
    """Return retrieval index and metadata readiness status."""
    service = RetrievalService()
    return service.status()


@router.post("/query", response_model=RetrievalResponse)
def query_retrieval(request: RetrievalRequest) -> RetrievalResponse:
    """Query the memory retrieval index and return top matching chunks."""
    service = RetrievalService()
    results = service.query(request.query, top_k=request.top_k)

    return RetrievalResponse(query=request.query, results=results)

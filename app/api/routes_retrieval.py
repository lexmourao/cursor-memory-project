"""Retrieval endpoint routes."""

from fastapi import APIRouter

from app.models.retrieval import RetrievalRequest, RetrievalResponse
from app.services.retrieval_service import RetrievalService


router = APIRouter(prefix="/retrieval", tags=["retrieval"])


@router.post("/query", response_model=RetrievalResponse)
def query_retrieval(request: RetrievalRequest) -> RetrievalResponse:
    """Query the memory retrieval index and return top matching chunks."""
    service = RetrievalService()
    results = service.query(request.query, top_k=request.top_k)

    return RetrievalResponse(query=request.query, results=results)

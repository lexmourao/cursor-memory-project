"""Summarization endpoint routes."""

from fastapi import APIRouter

from app.models.summarization import SummarizationRequest, SummarizationResponse
from app.services.summarization_service import SummarizationService


router = APIRouter(prefix="/summarization", tags=["summarization"])


@router.post("/summarize", response_model=SummarizationResponse)
def summarize_text(request: SummarizationRequest) -> SummarizationResponse:
    """Summarize text and optionally update active memory context."""
    service = SummarizationService()
    return service.summarize(
        text=request.text,
        model=request.model,
        manual=request.manual,
        embed=request.embed,
    )

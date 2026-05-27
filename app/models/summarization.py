"""Summarization API request and response models."""

from pydantic import BaseModel, Field


class SummarizationRequest(BaseModel):
    """Request body for summarization workflows."""

    text: str = Field(..., min_length=1)
    model: str = Field(default="gpt-4o", min_length=1)
    manual: bool = False
    embed: bool = True


class SummarizationResponse(BaseModel):
    """Response returned after summarizing text."""

    summary: str
    word_count: int
    model: str
    used_fallback: bool
    wrote_active_context: bool
    embedded: bool

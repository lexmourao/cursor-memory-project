"""Retrieval service for memory-bank query workflows."""

from app.models.retrieval import RetrievalResult
from scripts.retrieve_context import query_with_metadata


class RetrievalService:
    """Query the existing retrieval index and return typed results."""

    def query(self, text: str, top_k: int = 5) -> list[RetrievalResult]:
        """Return top retrieval results for the provided query text."""
        raw_results = query_with_metadata(text, top_k=top_k)

        return [
            RetrievalResult(
                score=match["score"],
                source=match["file"],
                chunk_idx=match["chunk_idx"],
                text=match["text"],
            )
            for match in raw_results
        ]

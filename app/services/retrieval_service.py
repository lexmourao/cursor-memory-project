"""Retrieval service for memory-bank query workflows."""

from app.models.retrieval import RetrievalResult
from scripts.retrieve_context import query as query_retrieval_index


class RetrievalService:
    """Query the existing retrieval index and return typed results."""

    def query(self, text: str, top_k: int = 5) -> list[RetrievalResult]:
        """Return top retrieval results for the provided query text."""
        raw_results = query_retrieval_index(text, top_k=top_k)

        return [
            RetrievalResult(
                score=score,
                source="memory-bank",
                text=chunk_text,
            )
            for score, chunk_text in raw_results
        ]

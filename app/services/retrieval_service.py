"""Retrieval service for memory-bank query workflows."""

import json

from app.models.retrieval import RetrievalResult, RetrievalStatusResponse
import scripts.retrieve_context as retrieve_context


class RetrievalService:
    """Query the existing retrieval index and return typed results."""

    def query(self, text: str, top_k: int = 5) -> list[RetrievalResult]:
        """Return top retrieval results for the provided query text."""
        raw_results = retrieve_context.query_with_metadata(text, top_k=top_k)

        return [
            RetrievalResult(
                score=match["score"],
                source=match["file"],
                chunk_idx=match["chunk_idx"],
                text=match["text"],
            )
            for match in raw_results
        ]

    def status(self) -> RetrievalStatusResponse:
        """Return retrieval index and metadata readiness status."""
        index_exists = retrieve_context.INDEX_FILE.exists()
        metadata_exists = retrieve_context.META_FILE.exists()
        json_export_exists = retrieve_context.META_JSON_FILE.exists()

        index_vector_count = self._index_vector_count() if index_exists else 0
        metadata_record_count = self._metadata_record_count() if metadata_exists else 0
        json_record_count = self._json_record_count() if json_export_exists else 0

        ready = (
            index_exists
            and metadata_exists
            and index_vector_count > 0
            and metadata_record_count > 0
            and index_vector_count == metadata_record_count
        )

        return RetrievalStatusResponse(
            index_exists=index_exists,
            metadata_exists=metadata_exists,
            json_export_exists=json_export_exists,
            index_vector_count=index_vector_count,
            metadata_record_count=metadata_record_count,
            json_record_count=json_record_count,
            ready=ready,
        )

    def _index_vector_count(self) -> int:
        """Return the number of vectors in the FAISS index."""
        try:
            index = retrieve_context.faiss.read_index(str(retrieve_context.INDEX_FILE))
        except RuntimeError:
            return 0

        return int(index.ntotal)

    def _metadata_record_count(self) -> int:
        """Return the number of records in the pickle metadata file."""
        try:
            return len(retrieve_context._load_meta())
        except (EOFError, OSError, ValueError):
            return 0

    def _json_record_count(self) -> int:
        """Return the number of records in the JSON metadata export."""
        try:
            payload = json.loads(retrieve_context.META_JSON_FILE.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return 0

        record_count = payload.get("record_count")
        if isinstance(record_count, int):
            return record_count

        records = payload.get("records")
        if isinstance(records, list):
            return len(records)

        return 0

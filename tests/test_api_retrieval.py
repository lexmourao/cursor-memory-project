"""API tests for backend retrieval endpoint."""

from pathlib import Path

from fastapi.testclient import TestClient
import pytest

from app.main import app
import scripts.retrieve_context as retrieve_context


client = TestClient(app)


def test_retrieval_query_endpoint_returns_response_shape() -> None:
    """Retrieval endpoint should return the query and a results list."""
    response = client.post(
        "/retrieval/query",
        json={"query": "What is the project architecture?", "top_k": 5},
    )

    assert response.status_code == 200

    payload = response.json()
    assert payload["query"] == "What is the project architecture?"
    assert "results" in payload
    assert isinstance(payload["results"], list)

    for result in payload["results"]:
        assert "score" in result
        assert "source" in result
        assert "chunk_idx" in result
        assert "text" in result
        assert isinstance(result["score"], float)
        assert isinstance(result["source"], str)
        assert isinstance(result["chunk_idx"], int)
        assert isinstance(result["text"], str)


def test_retrieval_query_endpoint_handles_missing_index(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Retrieval endpoint should return an empty result list if no index exists."""
    monkeypatch.setattr(retrieve_context, "INDEX_FILE", tmp_path / "missing.faiss")
    monkeypatch.setattr(retrieve_context, "META_FILE", tmp_path / "missing_meta.pkl")

    response = client.post(
        "/retrieval/query",
        json={"query": "What is the project architecture?", "top_k": 5},
    )

    assert response.status_code == 200

    payload = response.json()
    assert payload["query"] == "What is the project architecture?"
    assert payload["results"] == []


def test_retrieval_query_endpoint_rejects_empty_query() -> None:
    """Retrieval endpoint should reject empty query text."""
    response = client.post(
        "/retrieval/query",
        json={"query": "", "top_k": 5},
    )

    assert response.status_code == 422


def test_retrieval_query_endpoint_rejects_invalid_top_k_low() -> None:
    """Retrieval endpoint should reject top_k values below the allowed range."""
    response = client.post(
        "/retrieval/query",
        json={"query": "memory", "top_k": 0},
    )

    assert response.status_code == 422


def test_retrieval_query_endpoint_rejects_invalid_top_k_high() -> None:
    """Retrieval endpoint should reject top_k values above the allowed range."""
    response = client.post(
        "/retrieval/query",
        json={"query": "memory", "top_k": 21},
    )

    assert response.status_code == 422

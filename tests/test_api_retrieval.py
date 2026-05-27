"""API tests for backend retrieval endpoint."""

from fastapi.testclient import TestClient

from app.main import app


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

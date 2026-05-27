"""API tests for backend memory endpoints."""

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_memory_endpoint_returns_records_list() -> None:
    """Memory endpoint should return a records list."""
    response = client.get("/memory")

    assert response.status_code == 200

    payload = response.json()
    assert "records" in payload
    assert isinstance(payload["records"], list)


def test_memory_endpoint_includes_memory_bank_readme() -> None:
    """Memory endpoint should include the memory-bank README record."""
    response = client.get("/memory")

    assert response.status_code == 200

    records = response.json()["records"]
    record_ids = {record["id"] for record in records}

    assert "README" in record_ids


def test_memory_record_endpoint_returns_single_record() -> None:
    """Single memory record endpoint should return one record by ID."""
    response = client.get("/memory/README")

    assert response.status_code == 200

    payload = response.json()
    assert payload["id"] == "README"
    assert payload["type"] == "markdown"
    assert "memory-bank/README.md" in payload["source"]
    assert isinstance(payload["content"], str)


def test_memory_record_endpoint_returns_404_for_missing_record() -> None:
    """Single memory record endpoint should return 404 for missing records."""
    response = client.get("/memory/not-a-real-record")

    assert response.status_code == 404
    assert response.json()["detail"] == "Memory record not found"

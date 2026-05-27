"""API tests for backend health endpoint."""

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint_returns_service_status() -> None:
    """Health endpoint should return service and memory-bank status."""
    response = client.get("/health")

    assert response.status_code == 200

    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["service"] == "cursor-memory-project"
    assert payload["mode"] == "local"
    assert isinstance(payload["memory_bank_exists"], bool)
    assert isinstance(payload["memory_record_count"], int)

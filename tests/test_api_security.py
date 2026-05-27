"""API security tests for optional local token protection."""

from fastapi.testclient import TestClient
import pytest

from app.main import app


client = TestClient(app)


def test_protected_routes_remain_open_when_local_token_disabled(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Protected routes should remain open by default for local-first development."""
    monkeypatch.delenv("ENABLE_LOCAL_API_TOKEN", raising=False)
    monkeypatch.delenv("LOCAL_API_TOKEN", raising=False)

    response = client.get("/memory")

    assert response.status_code == 200
    assert "records" in response.json()


def test_protected_routes_reject_missing_token_when_enabled(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Protected routes should reject requests without Authorization when token mode is enabled."""
    monkeypatch.setenv("ENABLE_LOCAL_API_TOKEN", "true")
    monkeypatch.setenv("LOCAL_API_TOKEN", "test-token")

    response = client.get("/memory")

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid or missing local API token."


def test_protected_routes_reject_wrong_token_when_enabled(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Protected routes should reject incorrect Bearer tokens."""
    monkeypatch.setenv("ENABLE_LOCAL_API_TOKEN", "true")
    monkeypatch.setenv("LOCAL_API_TOKEN", "test-token")

    response = client.get(
        "/memory",
        headers={"Authorization": "Bearer wrong-token"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid or missing local API token."


def test_protected_routes_allow_correct_token_when_enabled(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Protected routes should allow requests with the configured Bearer token."""
    monkeypatch.setenv("ENABLE_LOCAL_API_TOKEN", "true")
    monkeypatch.setenv("LOCAL_API_TOKEN", "test-token")

    response = client.get(
        "/memory",
        headers={"Authorization": "Bearer test-token"},
    )

    assert response.status_code == 200
    assert "records" in response.json()


def test_token_enabled_without_configured_token_returns_server_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Token mode should fail closed when enabled without LOCAL_API_TOKEN."""
    monkeypatch.setenv("ENABLE_LOCAL_API_TOKEN", "true")
    monkeypatch.delenv("LOCAL_API_TOKEN", raising=False)

    response = client.get("/memory")

    assert response.status_code == 500
    assert (
        response.json()["detail"]
        == "Local API token protection is enabled but LOCAL_API_TOKEN is not configured."
    )


def test_retrieval_query_requires_token_when_enabled(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Retrieval query route should be protected when token mode is enabled."""
    monkeypatch.setenv("ENABLE_LOCAL_API_TOKEN", "true")
    monkeypatch.setenv("LOCAL_API_TOKEN", "test-token")

    response = client.post(
        "/retrieval/query",
        json={"query": "project architecture", "top_k": 1},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid or missing local API token."


def test_summarization_route_requires_token_when_enabled(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Summarization route should be protected when token mode is enabled."""
    monkeypatch.setenv("ENABLE_LOCAL_API_TOKEN", "true")
    monkeypatch.setenv("LOCAL_API_TOKEN", "test-token")

    response = client.post(
        "/summarization/summarize",
        json={
            "text": "Manual summary for security route test.",
            "model": "gpt-4o",
            "manual": True,
            "embed": False,
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid or missing local API token."


def test_metrics_route_requires_token_when_enabled(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Metrics route should be protected when token mode is enabled."""
    monkeypatch.setenv("ENABLE_LOCAL_API_TOKEN", "true")
    monkeypatch.setenv("LOCAL_API_TOKEN", "test-token")

    response = client.get("/metrics")

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid or missing local API token."


def test_metrics_route_allows_correct_token_when_enabled(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Metrics route should allow requests with the configured Bearer token."""
    monkeypatch.setenv("ENABLE_LOCAL_API_TOKEN", "true")
    monkeypatch.setenv("LOCAL_API_TOKEN", "test-token")

    response = client.get(
        "/metrics",
        headers={"Authorization": "Bearer test-token"},
    )

    assert response.status_code == 200
    assert "cursor_memory_backend_requests_total" in response.text


def test_health_route_remains_public_when_token_enabled(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Health route should remain public for local readiness checks."""
    monkeypatch.setenv("ENABLE_LOCAL_API_TOKEN", "true")
    monkeypatch.setenv("LOCAL_API_TOKEN", "test-token")

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"

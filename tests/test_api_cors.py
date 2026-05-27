"""API CORS tests for configurable local-first CORS behavior."""

from fastapi.testclient import TestClient

from app.core.config import Settings
from app.main import create_app


def test_cors_headers_absent_by_default() -> None:
    """CORS headers should be absent when CORS is disabled by default."""
    app = create_app(
        Settings(
            enable_cors=False,
            cors_allow_origins=(),
        )
    )
    client = TestClient(app)

    response = client.get(
        "/health",
        headers={"Origin": "http://localhost:3000"},
    )

    assert response.status_code == 200
    assert "access-control-allow-origin" not in response.headers


def test_allowed_origin_receives_cors_header_when_enabled() -> None:
    """Allowed origins should receive access-control-allow-origin when CORS is enabled."""
    app = create_app(
        Settings(
            enable_cors=True,
            cors_allow_origins=("http://localhost:3000",),
        )
    )
    client = TestClient(app)

    response = client.get(
        "/health",
        headers={"Origin": "http://localhost:3000"},
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:3000"


def test_disallowed_origin_does_not_receive_cors_header_when_enabled() -> None:
    """Disallowed origins should not receive access-control-allow-origin."""
    app = create_app(
        Settings(
            enable_cors=True,
            cors_allow_origins=("http://localhost:3000",),
        )
    )
    client = TestClient(app)

    response = client.get(
        "/health",
        headers={"Origin": "http://evil.example"},
    )

    assert response.status_code == 200
    assert "access-control-allow-origin" not in response.headers


def test_allowed_origin_preflight_request_succeeds_when_enabled() -> None:
    """Allowed origins should pass CORS preflight requests."""
    app = create_app(
        Settings(
            enable_cors=True,
            cors_allow_origins=("http://localhost:3000",),
        )
    )
    client = TestClient(app)

    response = client.options(
        "/retrieval/query",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "Authorization, Content-Type",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:3000"
    assert "POST" in response.headers["access-control-allow-methods"]
    assert "Authorization" in response.headers["access-control-allow-headers"]
    assert "Content-Type" in response.headers["access-control-allow-headers"]

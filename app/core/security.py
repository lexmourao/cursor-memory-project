"""Security helpers for the Cursor Memory Project backend."""

from fastapi import Header, HTTPException, status

from app.core.config import get_settings


def require_local_api_token(authorization: str | None = Header(default=None)) -> None:
    """Validate optional local API token when token protection is enabled.

    Token authentication is disabled by default for local-first development.
    When ENABLE_LOCAL_API_TOKEN is true, requests must include:

        Authorization: Bearer <LOCAL_API_TOKEN>
    """
    settings = get_settings()

    if not settings.enable_local_api_token:
        return

    if not settings.local_api_token:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Local API token protection is enabled but LOCAL_API_TOKEN is not configured.",
        )

    expected_header = f"Bearer {settings.local_api_token}"

    if authorization != expected_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing local API token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

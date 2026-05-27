"""Runtime configuration for the Cursor Memory Project backend."""

from dataclasses import dataclass
from pathlib import Path
import os


def _env_flag(name: str, default: bool = False) -> bool:
    """Return a boolean setting from an environment variable."""
    raw_value = os.getenv(name)

    if raw_value is None:
        return default

    return raw_value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    """Local-first backend settings.

    Defaults are intentionally safe for local development. External exposure,
    production deployment, and secret-dependent workflows should be configured
    explicitly by the operator.
    """

    service_name: str = "cursor-memory-project"
    runtime_mode: str = "local"
    memory_bank_dir: Path = Path("memory-bank")
    host: str = "127.0.0.1"
    port: int = 7331
    enable_local_api_token: bool = False
    local_api_token: str | None = None


def get_settings() -> Settings:
    """Return backend settings from environment variables with safe defaults."""
    return Settings(
        service_name=os.getenv("SERVICE_NAME", "cursor-memory-project"),
        runtime_mode=os.getenv("RUNTIME_MODE", "local"),
        memory_bank_dir=Path(os.getenv("MEMORY_BANK_DIR", "memory-bank")),
        host=os.getenv("HOST", "127.0.0.1"),
        port=int(os.getenv("PORT", "7331")),
        enable_local_api_token=_env_flag("ENABLE_LOCAL_API_TOKEN", default=False),
        local_api_token=os.getenv("LOCAL_API_TOKEN"),
    )

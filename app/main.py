"""FastAPI application entry point for the Cursor Memory Project backend."""

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest

from app.api.routes_health import router as health_router
from app.api.routes_memory import router as memory_router
from app.api.routes_retrieval import router as retrieval_router
from app.api.routes_summarization import router as summarization_router
from app.core.config import Settings, get_settings
from app.core.logging import configure_logging, get_logger
from app.core.security import require_local_api_token


REQUEST_COUNT = Counter(
    "cursor_memory_backend_requests_total",
    "Total HTTP requests handled by the backend",
    ["endpoint"],
)


def create_app(settings: Settings | None = None) -> FastAPI:
    """Create and configure the FastAPI app."""
    active_settings = settings or get_settings()
    configure_logging(active_settings)
    logger = get_logger(__name__)

    configured_app = FastAPI(
        title="Cursor Memory Project Backend",
        description=(
            "Local-first backend API for Cursor Memory Project memory-bank access, "
            "health checks, metrics, retrieval workflows, and summarization workflows."
        ),
        version="0.3.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    logger.info(
        "Starting backend service=%s runtime_mode=%s token_protection=%s cors_enabled=%s",
        active_settings.service_name,
        active_settings.runtime_mode,
        active_settings.enable_local_api_token,
        active_settings.enable_cors,
    )

    if active_settings.enable_cors and active_settings.cors_allow_origins:
        configured_app.add_middleware(
            CORSMiddleware,
            allow_origins=list(active_settings.cors_allow_origins),
            allow_credentials=False,
            allow_methods=["GET", "POST", "OPTIONS"],
            allow_headers=["Authorization", "Content-Type"],
        )
        logger.info(
            "CORS enabled for %s configured origin(s)",
            len(active_settings.cors_allow_origins),
        )
    else:
        logger.info("CORS disabled")

    @configured_app.middleware("http")
    async def count_requests(request, call_next):
        """Count backend requests by endpoint path."""
        response = await call_next(request)
        REQUEST_COUNT.labels(endpoint=request.url.path).inc()
        return response

    @configured_app.get("/metrics", dependencies=[Depends(require_local_api_token)])
    def metrics() -> Response:
        """Return Prometheus-compatible metrics."""
        return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

    configured_app.include_router(health_router)
    configured_app.include_router(memory_router)
    configured_app.include_router(retrieval_router)
    configured_app.include_router(summarization_router)

    return configured_app


app = create_app()

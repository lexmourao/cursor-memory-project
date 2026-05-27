"""FastAPI application entry point for the Cursor Memory Project backend."""

from fastapi import FastAPI
from fastapi.responses import Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest

from app.api.routes_health import router as health_router
from app.api.routes_memory import router as memory_router
from app.api.routes_retrieval import router as retrieval_router
from app.api.routes_summarization import router as summarization_router


app = FastAPI(
    title="Cursor Memory Project Backend",
    description=(
        "Local-first backend API for Cursor Memory Project memory-bank access, "
        "health checks, metrics, retrieval workflows, and summarization workflows."
    ),
    version="0.3.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

REQUEST_COUNT = Counter(
    "cursor_memory_backend_requests_total",
    "Total HTTP requests handled by the backend",
    ["endpoint"],
)


@app.middleware("http")
async def count_requests(request, call_next):
    """Count backend requests by endpoint path."""
    response = await call_next(request)
    REQUEST_COUNT.labels(endpoint=request.url.path).inc()
    return response


@app.get("/metrics")
def metrics() -> Response:
    """Return Prometheus-compatible metrics."""
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


app.include_router(health_router)
app.include_router(memory_router)
app.include_router(retrieval_router)
app.include_router(summarization_router)


def create_app() -> FastAPI:
    """Return the configured FastAPI app for tests or ASGI servers."""
    return app

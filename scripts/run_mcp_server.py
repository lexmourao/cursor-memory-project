import argparse
from pathlib import Path
from typing import List, Dict

from fastapi import FastAPI
import uvicorn
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response

MEMORY_BANK_DIR = Path("memory-bank")

# Local-only MCP-style memory stub: not a full production MCP protocol server.
# Binds to 127.0.0.1 by default and does not enable wildcard CORS because it
# exposes local project memory-bank content to trusted local development only.
app = FastAPI(title="Cursor Memory Bank MCP Stub", docs_url=None, redoc_url=None)

REQUEST_COUNT = Counter("mcp_requests_total", "Total HTTP requests", ["endpoint"])


@app.middleware("http")
async def count_requests(request, call_next):
    response = await call_next(request)
    REQUEST_COUNT.labels(endpoint=request.url.path).inc()
    return response


@app.get("/metrics")
async def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


def load_memory() -> List[Dict[str, str]]:
    """Load all markdown files as simple context records."""
    records: List[Dict[str, str]] = []
    for md_file in sorted(MEMORY_BANK_DIR.glob("*.md")):
        content = md_file.read_text(encoding="utf-8")
        records.append(
            {
                "id": md_file.stem,
                "type": "markdown",
                "source": str(md_file),
                "content": content,
            }
        )
    return records


memory_cache: List[Dict[str, str]] = load_memory()


class _ReloadHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        global memory_cache
        memory_cache = load_memory()
        print("[mcp_server] Memory-bank change detected → reloaded cache")


def _start_watcher():
    observer = Observer()
    handler = _ReloadHandler()
    observer.schedule(handler, str(MEMORY_BANK_DIR), recursive=False)
    observer.start()


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/memory")
async def memory():
    return {"memory": memory_cache}


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser for the MCP-style local memory stub."""
    parser = argparse.ArgumentParser(
        description="Run local MCP stub server for memory bank"
    )
    parser.add_argument("--port", type=int, default=7331)
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host interface to bind. Defaults to local-only 127.0.0.1.",
    )
    return parser


def main():
    args = build_parser().parse_args()

    _start_watcher()
    print(
        f"[mcp_server] Serving memory bank with hot-reload on http://{args.host}:{args.port}/memory"
    )
    uvicorn.run(app, host=args.host, port=args.port)


if __name__ == "__main__":
    main()

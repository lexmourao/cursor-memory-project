# Backend Design – Cursor Memory Project

> This document describes the backend architecture and evolution path for the Cursor Memory Project as a local-first memory and retrieval service for Cursor, ChatGPT, Codex, and AI-assisted development workflows.

---

## 1. Purpose

The Cursor Memory Project provides a local-first memory system using markdown files, Python automation scripts, retrieval, summarization, and an MCP-oriented memory server.

The backend layer is being evolved into a clearer FastAPI service structure with typed contracts, explicit routes, reusable services, configuration management, tests, and operational boundaries.

The goal is not to turn this repository into a full production SaaS platform. The goal is to show how a local AI-assisted development memory system can evolve toward production-grade backend architecture while remaining useful as a developer tool.

---

## 2. Current Backend Status

The first and second backend slices have been implemented and tested.

Implemented:

```text
app/
  __init__.py
  main.py
  api/
    __init__.py
    routes_health.py
    routes_memory.py
    routes_retrieval.py
  core/
    __init__.py
    config.py
  models/
    __init__.py
    health.py
    memory.py
    retrieval.py
  services/
    __init__.py
    memory_service.py
    retrieval_service.py
```

Implemented endpoints:

```text
GET /health
GET /memory
GET /memory/{record_id}
GET /metrics
POST /retrieval/query
```

Implemented tests:

```text
tests/test_api_health.py
tests/test_api_memory.py
tests/test_api_retrieval.py
```

The backend now has:

- a FastAPI application entry point
- typed health response model
- typed memory response models
- typed retrieval request and response models
- centralized local-first configuration
- reusable memory service
- reusable retrieval service
- route modules for health, memory, and retrieval
- Prometheus-compatible metrics endpoint
- API tests using FastAPI TestClient
- green public CI for implemented backend slices

---

## 3. Backend Goals

The backend layer should provide:

- a clean API for memory access
- retrieval query endpoints
- health and readiness endpoints
- metrics endpoint
- typed request and response models
- reusable service modules
- centralized configuration
- structured logging
- local-first security defaults
- testable business logic
- clear separation between CLI scripts and backend services

The implemented backend slices currently cover:

- memory access
- health status
- metrics
- typed response models
- typed retrieval request/response models
- configuration
- service separation
- retrieval API route
- API tests

Future backend work should focus on summarization service extraction, structured logging, local security hardening, and deeper retrieval evaluation.

---

## 4. Non-Goals

This backend design does not currently include:

- multi-tenant SaaS authentication
- hosted production deployment
- paid user accounts
- frontend dashboard
- enterprise RBAC
- managed production database
- managed vector database
- cloud-native job orchestration
- large-scale distributed processing

These may be added later as production-evolution paths.

---

## 5. Backend Structure

### Current Structure

```text
app/
  __init__.py
  main.py
  api/
    __init__.py
    routes_health.py
    routes_memory.py
    routes_retrieval.py
  core/
    __init__.py
    config.py
  models/
    __init__.py
    health.py
    memory.py
    retrieval.py
  services/
    __init__.py
    memory_service.py
    retrieval_service.py
```

### Planned Future Structure

```text
app/
  main.py
  api/
    routes_health.py
    routes_memory.py
    routes_retrieval.py
    routes_metrics.py
    routes_summarization.py
  core/
    config.py
    logging.py
    security.py
  models/
    health.py
    memory.py
    retrieval.py
    summarization.py
  services/
    memory_service.py
    retrieval_service.py
    summarization_service.py
  repositories/
    memory_repository.py
```

Existing `scripts/` remain useful as CLI entry points. Over time, scripts can call reusable services from `app/services/` rather than duplicating logic.

---

## 6. API Surface

### Health

```text
GET /health
```

Status:

```text
Implemented
```

Purpose:

- confirm service is running
- confirm memory-bank directory is readable
- confirm basic runtime configuration
- return memory record count

Current response shape:

```json
{
  "status": "ok",
  "service": "cursor-memory-project",
  "mode": "local",
  "memory_bank_exists": true,
  "memory_record_count": 7
}
```

---

### Memory List

```text
GET /memory
```

Status:

```text
Implemented
```

Purpose:

- return available memory records
- expose allowed markdown memory files as structured records
- support Cursor or AI-assisted tools loading project context
- avoid exposing generated indexes, pickles, or non-memory files

Current response shape:

```json
{
  "records": [
    {
      "id": "projectbrief",
      "source": "memory-bank/projectbrief.md",
      "type": "markdown",
      "content": "..."
    }
  ]
}
```

---

### Memory Record

```text
GET /memory/{record_id}
```

Status:

```text
Implemented
```

Purpose:

- return one memory record by ID
- support targeted context loading
- return 404 for missing records

Supported record IDs include:

- `README`
- `projectbrief`
- `productContext`
- `activeContext`
- `systemPatterns`
- `techContext`
- `progress`

---

### Metrics

```text
GET /metrics
```

Status:

```text
Implemented
```

Purpose:

- expose Prometheus-compatible metrics
- support local monitoring
- track request counts and service health indicators

---

### Retrieval Query

```text
POST /retrieval/query
```

Status:

```text
Implemented
```

Purpose:

- accept a query
- search the retrieval index
- return top-K relevant memory chunks
- validate query text and `top_k` bounds

Example request:

```json
{
  "query": "What is the project architecture?",
  "top_k": 5
}
```

Example response:

```json
{
  "query": "What is the project architecture?",
  "results": [
    {
      "score": 0.82,
      "source": "memory-bank",
      "text": "..."
    }
  ]
}
```

Validation behavior:

- empty query returns validation error
- `top_k` below 1 returns validation error
- `top_k` above 20 returns validation error

---

## 7. Typed Models

The backend uses typed models for API contracts.

Implemented model concepts:

```python
class HealthResponse(BaseModel):
    status: str
    service: str
    mode: str
    memory_bank_exists: bool
    memory_record_count: int


class MemoryRecord(BaseModel):
    id: str
    source: str
    type: str
    content: str


class MemoryListResponse(BaseModel):
    records: list[MemoryRecord]


class RetrievalRequest(BaseModel):
    query: str = Field(..., min_length=1)
    top_k: int = Field(default=5, ge=1, le=20)


class RetrievalResult(BaseModel):
    score: float
    source: str
    text: str


class RetrievalResponse(BaseModel):
    query: str
    results: list[RetrievalResult]
```

Typed contracts make the API easier to test, document, and evolve.

---

## 8. Service Layer

The backend separates route handling from business logic.

### Memory Service

Status:

```text
Implemented
```

Responsibilities:

- load memory-bank markdown files
- validate allowed memory files
- return memory records
- return one memory record by ID
- prevent generated index files or unrelated files from being exposed as memory records

Allowed memory files:

```text
README.md
projectbrief.md
productContext.md
activeContext.md
systemPatterns.md
techContext.md
progress.md
```

### Retrieval Service

Status:

```text
Implemented
```

Responsibilities:

- wrap the existing `scripts.retrieve_context.query` workflow
- query memory chunks through the existing retrieval index logic
- return typed retrieval result models
- support the backend retrieval route without breaking the CLI workflow

Current implementation intentionally reuses the existing retrieval script instead of rewriting the retrieval system. This keeps the CLI workflow working while exposing retrieval through the backend API.

### Summarization Service

Status:

```text
Planned for later backend slice
```

Responsibilities:

- summarize chat logs when configured
- support manual/fallback mode
- update `activeContext.md`
- optionally update the retrieval index
- preserve compatibility with `scripts/summarize_chat.py`

---

## 9. Configuration

Configuration is centralized in:

```text
app/core/config.py
```

Current settings:

```text
SERVICE_NAME=cursor-memory-project
RUNTIME_MODE=local
MEMORY_BANK_DIR=memory-bank
HOST=127.0.0.1
PORT=7331
```

Defaults favor local-first security:

- bind to `127.0.0.1` by default
- require explicit configuration for external exposure
- avoid requiring private secrets in public CI
- keep `env.template` safe to commit

Future configuration may include:

```text
EMBED_MODEL=text-embedding-3-small
EMBED_DIM=1536
OPENAI_API_KEY=
CORS_ORIGINS=http://localhost
LOCAL_API_TOKEN=
```

---

## 10. Security Posture

The backend is local-first.

Default assumptions:

- local usage does not require public exposure
- memory-bank must not contain secrets, PII, PHI, credentials, or client-confidential data
- `.env` files must not be committed
- `env.template` is safe to commit
- public CI should not require private secrets
- Nginx is a starter reverse-proxy example, not a fully hardened production gateway

Current safety behavior:

- only explicitly allowed memory-bank markdown files are exposed through the memory service
- generated FAISS and pickle files are not exposed as memory records
- retrieval API uses typed request validation for query and `top_k`
- public CI remains secret-free
- dependency checks remain active
- GitHub code scanning remains enabled through the repository security configuration

Future hardening may include:

- optional bearer token for non-localhost usage
- configurable CORS
- rate limiting
- structured audit logs
- managed secret storage
- encrypted storage
- workspace-level access boundaries

---

## 11. Testing Strategy

### Implemented Tests

```text
tests/test_api_health.py
tests/test_api_memory.py
tests/test_api_retrieval.py
```

Current backend tests cover:

- `GET /health`
- health response shape
- service status
- memory-bank existence field
- memory record count field
- `GET /memory`
- memory list response shape
- expected memory-bank README record
- `GET /memory/{record_id}`
- single record retrieval
- 404 behavior for missing memory record
- `POST /retrieval/query`
- retrieval response shape
- empty query validation
- invalid low `top_k` validation
- invalid high `top_k` validation

### Planned Tests

Future tests should cover:

- retrieval behavior after an index rebuild
- missing retrieval index behavior
- empty retrieval index behavior
- fallback mode without OpenAI key
- retrieval result source metadata
- summarization service behavior after backend extraction
- configured API token behavior if enabled later

---

## 12. Migration Path from Current Scripts

Current scripts remain valuable.

Planned evolution:

1. Keep scripts working as CLI tools.
2. Move reusable logic into `app/services/`.
3. Update scripts to call service functions.
4. Add API routes that call the same services.
5. Add tests for both CLI and API behavior.
6. Keep public CI focused and secret-free.

This avoids a risky rewrite and preserves the working current system.

Current progress:

```text
Step 1: app package created
Step 2: configuration layer created
Step 3: typed health and memory models created
Step 4: memory service created
Step 5: health and memory routes created
Step 6: FastAPI app entry point created
Step 7: API tests for health and memory created
Step 8: retrieval models created
Step 9: retrieval service created
Step 10: retrieval route created
Step 11: retrieval router registered
Step 12: retrieval API tests created
```

Next:

```text
Step 13: update public docs to reflect retrieval API
Step 14: add deeper retrieval behavior tests
Step 15: extract summarization service
```

---

## 13. Senior Engineering Rationale

This backend design demonstrates:

- separation of concerns
- API contract thinking
- local-first security posture
- service-oriented architecture
- typed backend models
- testability
- operational awareness
- clear public CI vs configured integration separation
- realistic evolution from scripts to backend services
- incremental delivery through green, auditable slices

The repository is intentionally scoped as a developer infrastructure project. Its backend value comes from making AI-assisted development memory reliable, inspectable, testable, and extensible.

The first backend slice strengthened the senior-backend signal by moving the repository from documentation and scripts into a tested FastAPI service structure without breaking the existing workflow.

The second backend slice strengthens the AI systems/backend signal further by exposing retrieval through a typed API while preserving the existing CLI retrieval workflow.

---

## 14. Implementation Checklist

### Completed First Backend Slice: Health, Memory, Metrics

- [x] Create `app/` package structure
- [x] Add `app/core/config.py`
- [x] Add typed health model
- [x] Add typed memory models
- [x] Add `memory_service.py`
- [x] Add route module for health
- [x] Add route module for memory
- [x] Add `app/main.py`
- [x] Add FastAPI health endpoint test
- [x] Add FastAPI memory endpoint tests

### Completed Second Backend Slice: Retrieval

- [x] Add `app/models/retrieval.py`
- [x] Add `app/services/retrieval_service.py`
- [x] Add `app/api/routes_retrieval.py`
- [x] Register retrieval router in `app/main.py`
- [x] Add `tests/test_api_retrieval.py`
- [x] Keep existing `scripts/retrieve_context.py` working

### Next Backend Slice: Summarization Service

- [ ] Add `app/models/summarization.py`
- [ ] Add `app/services/summarization_service.py`
- [ ] Add `app/api/routes_summarization.py`
- [ ] Register summarization router in `app/main.py`
- [ ] Add `tests/test_api_summarization.py`
- [ ] Preserve `scripts/summarize_chat.py` CLI workflow
- [ ] Update docs after summarization API is green

### Later Backend Slices

- [ ] Add structured logging module
- [ ] Add optional local API token security
- [ ] Add configurable CORS
- [ ] Add readiness endpoint
- [ ] Add stronger integration tests
- [ ] Add local backend run instructions
- [ ] Consider converting `scripts/run_mcp_server.py` into a wrapper around `app.main`

---

## 15. Summary

The backend evolution is turning the current script-based memory system into a clearer local-first API service without overclaiming production SaaS maturity.

The current direction is:

```text
template memory system
→ local scripts
→ typed FastAPI backend slice
→ tested service layer
→ retrieval API
→ summarization API
→ optional production hardening
```

The first FastAPI backend slice is implemented, tested, documented, and green.

The second retrieval API slice is implemented, tested, documented, and green.

The next meaningful engineering step is to extract summarization into the backend service layer while preserving the existing CLI workflow.

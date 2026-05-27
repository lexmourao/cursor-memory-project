# Backend Design – Cursor Memory Project

> This document describes the backend evolution path for the Cursor Memory Project as a local-first memory and retrieval service for Cursor, ChatGPT, Codex, and AI-assisted development workflows.

---

## 1. Purpose

The Cursor Memory Project currently provides a local-first memory system using markdown files, Python automation scripts, retrieval, summarization, and an MCP-oriented memory server.

The next backend evolution is to organize this functionality into a clearer FastAPI service layer with typed contracts, explicit routes, reusable services, configuration management, tests, and operational boundaries.

The goal is not to turn this repository into a full production SaaS platform. The goal is to show how a local AI-assisted development memory system can evolve toward production-grade backend architecture while remaining useful as a developer tool.

---

## 2. Backend Goals

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

---

## 3. Non-Goals

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

## 4. Proposed Backend Structure

```text
app/
  main.py
  api/
    routes_health.py
    routes_memory.py
    routes_retrieval.py
    routes_metrics.py
  core/
    config.py
    logging.py
    security.py
  models/
    memory.py
    retrieval.py
    health.py
  services/
    memory_service.py
    retrieval_service.py
    summarization_service.py
  repositories/
    memory_repository.py
```

Existing `scripts/` should remain useful as CLI entry points. Over time, scripts can call reusable services from `app/services/` rather than duplicating logic.

---

## 5. API Surface

### Health

```text
GET /health
```

Purpose:

- confirm service is running
- confirm memory-bank directory is readable
- confirm basic runtime configuration

Expected response:

```json
{
  "status": "ok",
  "service": "cursor-memory-project",
  "mode": "local"
}
```

---

### Memory List

```text
GET /memory
```

Purpose:

- return available memory records
- expose markdown memory files as structured records
- support Cursor or AI-assisted tools loading project context

Expected response:

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

Purpose:

- return one memory record by ID
- support targeted context loading

Possible record IDs:

- `projectbrief`
- `productContext`
- `activeContext`
- `systemPatterns`
- `techContext`
- `progress`

---

### Retrieval Query

```text
POST /retrieval/query
```

Purpose:

- accept a query
- search the retrieval index
- return top-K relevant memory chunks

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
      "source": "systemPatterns.md",
      "text": "..."
    }
  ]
}
```

---

### Metrics

```text
GET /metrics
```

Purpose:

- expose Prometheus-compatible metrics
- support local monitoring
- track request counts and service health indicators

---

## 6. Typed Models

The backend should use typed models for API contracts.

Example model concepts:

```python
class MemoryRecord(BaseModel):
    id: str
    source: str
    type: Literal["markdown"]
    content: str

class RetrievalRequest(BaseModel):
    query: str
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

## 7. Service Layer

The backend should separate route handling from business logic.

### Memory Service

Responsibilities:

- load memory-bank markdown files
- validate allowed memory files
- return memory records
- prevent secrets or generated index files from being exposed as memory records

### Retrieval Service

Responsibilities:

- build or load retrieval index
- query memory chunks
- return top-K results
- handle empty index states
- support fallback behavior when embeddings are unavailable

### Summarization Service

Responsibilities:

- summarize chat logs when configured
- support manual/fallback mode
- update `activeContext.md`
- optionally update the retrieval index

---

## 8. Configuration

Configuration should be centralized.

Example settings:

```text
MEMORY_BANK_DIR=memory-bank
EMBED_MODEL=text-embedding-3-small
EMBED_DIM=1536
OPENAI_API_KEY=
HOST=127.0.0.1
PORT=7331
CORS_ORIGINS=http://localhost
LOCAL_API_TOKEN=
```

Defaults should favor local-first security:

- bind to `127.0.0.1` by default
- require explicit configuration for external exposure
- avoid requiring private secrets in public CI
- keep `env.template` safe to commit

---

## 9. Security Posture

The backend is local-first.

Default assumptions:

- local usage does not require public exposure
- memory-bank must not contain secrets, PII, PHI, credentials, or client-confidential data
- `.env` files must not be committed
- `env.template` is safe to commit
- public CI should not require private secrets
- Nginx is a starter reverse-proxy example, not a fully hardened production gateway

Future hardening may include:

- optional bearer token for non-localhost usage
- configurable CORS
- rate limiting
- structured audit logs
- managed secret storage
- encrypted storage
- workspace-level access boundaries

---

## 10. Testing Strategy

Backend tests should cover:

- `GET /health`
- `GET /memory`
- `GET /memory/{record_id}`
- `POST /retrieval/query`
- empty memory-bank behavior
- missing retrieval index behavior
- invalid `top_k`
- fallback mode without OpenAI key
- configured API token behavior if enabled later

Suggested test files:

```text
tests/test_api_health.py
tests/test_api_memory.py
tests/test_api_retrieval.py
```

---

## 11. Migration Path from Current Scripts

Current scripts remain valuable.

Planned evolution:

1. Keep scripts working as CLI tools.
2. Move reusable logic into `app/services/`.
3. Update scripts to call service functions.
4. Add API routes that call the same services.
5. Add tests for both CLI and API behavior.
6. Keep public CI focused and secret-free.

This avoids a risky rewrite and preserves the working current system.

---

## 12. Senior Engineering Rationale

This backend design demonstrates:

- separation of concerns
- API contract thinking
- local-first security posture
- service-oriented architecture
- typed backend models
- testability
- operational awareness
- clear public CI vs configured integration separation
- a realistic evolution path from scripts to backend services

The repository is intentionally scoped as a developer infrastructure project. Its backend value comes from making AI-assisted development memory reliable, inspectable, testable, and extensible.

---

## 13. Next Implementation Steps

1. Create `app/` package structure.
2. Add `app/core/config.py`.
3. Add typed models in `app/models/`.
4. Add `memory_service.py`.
5. Add `retrieval_service.py`.
6. Add route modules for health, memory, and retrieval.
7. Add `app/main.py`.
8. Add FastAPI API tests.
9. Keep `scripts/run_mcp_server.py` working or convert it into a wrapper.
10. Update README and demo workflow after the backend slice is implemented.

---

## 14. Summary

The backend evolution should turn the current script-based memory system into a clearer local-first API service without overclaiming production SaaS maturity.

The correct direction is:

```text
template memory system
→ local scripts
→ typed FastAPI backend slice
→ tested service layer
→ optional production hardening
```

This path supports the repository’s real purpose while making the engineering implementation stronger and easier for technical reviewers to evaluate.

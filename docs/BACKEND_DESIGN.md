# Backend Design – Cursor Memory Project

> This document describes the backend architecture and evolution path for the Cursor Memory Project as a local-first memory, retrieval, summarization, and security-aware backend service for Cursor, ChatGPT, Codex, and AI-assisted development workflows.

---

## 1. Purpose

The Cursor Memory Project provides a local-first memory system using markdown files, Python automation scripts, retrieval, summarization, and an MCP-oriented memory server.

The backend layer has evolved into a clearer FastAPI service structure with typed contracts, explicit routes, reusable services, configuration management, tests, metadata schemas, metadata export workflows, readiness/status reporting, summarization workflows, optional local API token protection, and operational boundaries.

The goal is not to turn this repository into a full production SaaS platform. The goal is to show how a local AI-assisted development memory system can evolve toward production-grade backend architecture while remaining useful as a developer tool.

---

## 2. Current Backend Status

The health/memory, retrieval, summarization, CLI compatibility, and local security backend slices have been implemented and tested.

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
    routes_summarization.py
  core/
    __init__.py
    config.py
    security.py
  models/
    __init__.py
    chunk.py
    health.py
    memory.py
    retrieval.py
    summarization.py
  services/
    __init__.py
    memory_service.py
    retrieval_service.py
    summarization_service.py
```

Implemented endpoints:

```text
GET /health
GET /memory
GET /memory/{record_id}
GET /metrics
GET /retrieval/status
POST /retrieval/query
POST /summarization/summarize
```

Protected when optional local API token mode is enabled:

```text
GET /memory
GET /memory/{record_id}
GET /metrics
GET /retrieval/status
POST /retrieval/query
POST /summarization/summarize
```

Intentionally public for local readiness checks:

```text
GET /health
```

Implemented tests:

```text
tests/test_api_health.py
tests/test_api_memory.py
tests/test_api_retrieval.py
tests/test_api_summarization.py
tests/test_api_security.py
tests/test_cli_summarize_chat.py
```

The backend now has:

- a FastAPI application entry point
- typed health response model
- typed memory response models
- formal chunk metadata models
- typed retrieval request and response models
- typed retrieval status response model
- typed summarization request and response models
- centralized local-first configuration
- optional local API token configuration
- reusable local API token security helper
- reusable memory service
- reusable retrieval service
- reusable summarization service
- route modules for health, memory, retrieval, and summarization
- Prometheus-compatible metrics endpoint
- metadata-aware retrieval responses with source file and chunk index
- retrieval status endpoint for index and metadata readiness
- retrieval reliability coverage for missing and empty indexes
- integration-style retrieval coverage after rebuilding a temporary index
- JSON metadata export for inspectability while preserving pickle runtime compatibility
- summarization endpoint with manual mode and fallback mode
- isolated active context writing tests
- CLI compatibility tests for `scripts/summarize_chat.py`
- optional local API token security tests
- green public CI for implemented backend slices

---

## 3. Backend Goals

The backend layer should provide:

- a clean API for memory access
- retrieval query endpoints
- retrieval status/readiness endpoint
- summarization endpoint
- health and readiness endpoints
- metrics endpoint
- typed request and response models
- reusable metadata schemas
- reusable service modules
- centralized configuration
- optional local API token protection
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
- typed retrieval status model
- typed summarization request/response models
- formal chunk metadata schema
- retrieval metadata JSON export
- configuration
- optional token security configuration
- service separation
- retrieval API route
- retrieval status route
- summarization API route
- retrieval metadata traceability
- missing-index reliability behavior
- empty-index reliability behavior
- retrieval behavior after index rebuild
- summarization manual mode
- summarization fallback mode
- active context writing
- CLI compatibility for summarization
- optional local API token behavior
- API tests

Future backend work should focus on structured logging, configurable CORS, MCP/server security defaults, retrieval/summarization evaluation, backup/restore validation, and final reviewer polish.

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
    routes_summarization.py
  core/
    __init__.py
    config.py
    security.py
  models/
    __init__.py
    chunk.py
    health.py
    memory.py
    retrieval.py
    summarization.py
  services/
    __init__.py
    memory_service.py
    retrieval_service.py
    summarization_service.py
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
    cors.py
  models/
    chunk.py
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

Protection:

```text
Public by design
```

Purpose:

- confirm service is running
- confirm memory-bank directory is readable
- confirm basic runtime configuration
- return memory record count
- remain available for local readiness checks even when optional token protection is enabled

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

Protection:

```text
Protected when ENABLE_LOCAL_API_TOKEN=true
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

Protection:

```text
Protected when ENABLE_LOCAL_API_TOKEN=true
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

Protection:

```text
Protected when ENABLE_LOCAL_API_TOKEN=true
```

Purpose:

- expose Prometheus-compatible metrics
- support local monitoring
- track request counts and service health indicators

Security note:

- `/metrics` remains open by default for local-first development.
- When token protection is enabled, `/metrics` requires `Authorization: Bearer <LOCAL_API_TOKEN>`.
- `/health` remains public for readiness checks.

---

### Retrieval Status

```text
GET /retrieval/status
```

Status:

```text
Implemented
```

Protection:

```text
Protected when ENABLE_LOCAL_API_TOKEN=true
```

Purpose:

- report retrieval index readiness
- report whether FAISS index, pickle metadata, and JSON metadata export exist
- report vector and metadata record counts
- expose a conservative `ready` boolean for operational inspection
- support debugging before querying retrieval

Current response shape:

```json
{
  "index_exists": true,
  "metadata_exists": true,
  "json_export_exists": true,
  "index_vector_count": 2,
  "metadata_record_count": 2,
  "json_record_count": 2,
  "ready": true
}
```

Readiness behavior:

- `ready` is true only when the FAISS index exists
- pickle metadata exists
- index vector count is greater than zero
- metadata record count is greater than zero
- index vector count matches metadata record count
- JSON export is reported but not required for runtime readiness

---

### Retrieval Query

```text
POST /retrieval/query
```

Status:

```text
Implemented
```

Protection:

```text
Protected when ENABLE_LOCAL_API_TOKEN=true
```

Purpose:

- accept a query
- search the retrieval index
- return top-K relevant memory chunks
- validate query text and `top_k` bounds
- expose source file and chunk index for traceability
- return an empty result list when the index is missing
- return an empty result list when the index exists but has no vectors
- return indexed memory after a rebuild from a temporary memory-bank

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
      "chunk_idx": 3,
      "text": "..."
    }
  ]
}
```

Validation behavior:

- empty query returns validation error
- `top_k` below 1 returns validation error
- `top_k` above 20 returns validation error

Traceability behavior:

- `source` returns the memory-bank source filename
- `chunk_idx` returns the source chunk index
- `text` returns the retrieved chunk text
- `score` returns the FAISS similarity score

Reliability behavior:

- missing FAISS index returns an empty `results` list instead of crashing
- empty FAISS index returns an empty `results` list instead of crashing
- rebuilt temporary index returns the expected indexed memory result without polluting the real `memory-bank/`

---

### Summarization

```text
POST /summarization/summarize
```

Status:

```text
Implemented
```

Protection:

```text
Protected when ENABLE_LOCAL_API_TOKEN=true
```

Purpose:

- accept text to summarize
- support manual summary mode
- support OpenAI-backed summarization when configured
- fall back safely when OpenAI is unavailable
- write the summary to `memory-bank/activeContext.md`
- optionally embed the summary through the existing retrieval workflow
- return typed metadata about the summarization result

Example request:

```json
{
  "text": "Manual summary for the current backend slice.",
  "model": "gpt-4o",
  "manual": true,
  "embed": false
}
```

Example response:

```json
{
  "summary": "Manual summary for the current backend slice.",
  "word_count": 7,
  "model": "gpt-4o",
  "used_fallback": false,
  "wrote_active_context": true,
  "embedded": false
}
```

Validation behavior:

- empty `text` returns validation error
- `model` must be a non-empty string
- `manual` defaults to `false`
- `embed` defaults to `true`

Operational behavior:

- manual mode treats the submitted text as the summary
- non-manual mode attempts model-based summarization
- if OpenAI is unavailable or not configured, fallback summarization is used
- active context writing is enabled by the service
- embedding can be disabled for safe tests or workflows

---

## 7. Optional Local API Token Protection

Status:

```text
Implemented
```

The backend supports optional local API token protection for sensitive local routes.

Configuration:

```text
ENABLE_LOCAL_API_TOKEN=false
LOCAL_API_TOKEN=
```

Default behavior:

```text
Token protection disabled.
Routes remain open for local-first development.
```

Enabled behavior:

```text
ENABLE_LOCAL_API_TOKEN=true
LOCAL_API_TOKEN=<token>
```

Protected requests must include:

```text
Authorization: Bearer <LOCAL_API_TOKEN>
```

Protected routes:

```text
GET /memory
GET /memory/{record_id}
GET /metrics
GET /retrieval/status
POST /retrieval/query
POST /summarization/summarize
```

Public route:

```text
GET /health
```

Fail-closed behavior:

- If `ENABLE_LOCAL_API_TOKEN=true` but `LOCAL_API_TOKEN` is missing, protected routes return a server error instead of silently allowing access.
- Missing or invalid bearer tokens return `401 Unauthorized`.
- Correct bearer tokens allow access to protected routes.
- `GET /health` remains public for local readiness checks.

Implemented files:

```text
app/core/config.py
app/core/security.py
app/api/routes_memory.py
app/api/routes_retrieval.py
app/api/routes_summarization.py
app/main.py
tests/test_api_security.py
env.template
```

Security rationale:

- The project is local-first, so token protection is disabled by default.
- When users expose the backend outside trusted localhost usage, token protection can be enabled without changing route code.
- The token is intentionally simple and local-scoped. It is not a replacement for production authentication, RBAC, TLS, or network controls.

---

## 8. Typed Models

The backend uses typed models for API contracts and reusable metadata structures.

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


class ChunkMetadata(BaseModel):
    source: str = Field(..., min_length=1)
    chunk_idx: int = Field(..., ge=0)


class RetrievedChunk(ChunkMetadata):
    score: float
    text: str


class RetrievalRequest(BaseModel):
    query: str = Field(..., min_length=1)
    top_k: int = Field(default=5, ge=1, le=20)


class RetrievalResult(RetrievedChunk):
    pass


class RetrievalResponse(BaseModel):
    query: str
    results: list[RetrievalResult]


class RetrievalStatusResponse(BaseModel):
    index_exists: bool
    metadata_exists: bool
    json_export_exists: bool
    index_vector_count: int
    metadata_record_count: int
    json_record_count: int
    ready: bool


class SummarizationRequest(BaseModel):
    text: str = Field(..., min_length=1)
    model: str = Field(default="gpt-4o", min_length=1)
    manual: bool = False
    embed: bool = True


class SummarizationResponse(BaseModel):
    summary: str
    word_count: int
    model: str
    used_fallback: bool
    wrote_active_context: bool
    embedded: bool
```

Typed contracts make the API easier to test, document, and evolve.

The shared chunk schema now makes retrieval metadata reusable across:

- retrieval API responses
- future metadata storage
- future retrieval dashboards
- future inspection endpoints
- future retrieval evaluation tests

The summarization schema makes active context updates and fallback behavior explicit for API consumers and tests.

---

## 9. Service Layer

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

- wrap the existing `scripts.retrieve_context.query_with_metadata` workflow
- query memory chunks through the existing retrieval index logic
- return typed retrieval result models
- expose source filename and chunk index in API results
- reuse the formal chunk metadata schema through `RetrievedChunk`
- report retrieval index and metadata readiness through `status()`
- support missing and empty retrieval index behavior without API crashes
- support rebuilt index retrieval behavior
- support the backend retrieval route without breaking the CLI workflow

Current implementation intentionally reuses the existing retrieval script instead of rewriting the retrieval system. This keeps the CLI workflow working while exposing retrieval through the backend API.

### Summarization Service

Status:

```text
Implemented
```

Responsibilities:

- summarize text through the backend API
- support manual summary mode
- support OpenAI-backed summarization when configured
- use fallback summarization when OpenAI is unavailable or fails
- write generated content to `memory-bank/activeContext.md`
- optionally embed the summary through the existing retrieval workflow
- return typed summarization response metadata
- support CLI reuse through `scripts/summarize_chat.py`

The summarization service is now reused by the CLI for active context writing and optional embedding while preserving backward-compatible `call_openai_summarize()` behavior for existing tests and scripts.

### Security Helper

Status:

```text
Implemented
```

The backend now includes:

```text
app/core/security.py
```

Responsibilities:

- read local token settings through `get_settings()`
- allow requests when token protection is disabled
- require `Authorization: Bearer <LOCAL_API_TOKEN>` when token protection is enabled
- return `401 Unauthorized` for missing or incorrect tokens
- return a fail-closed server error when token protection is enabled but `LOCAL_API_TOKEN` is not configured

---

## 10. Retrieval Metadata and Storage

### Retrieval Status

Status:

```text
Implemented
```

The retrieval service exposes:

```text
status()
```

This returns:

```text
index_exists
metadata_exists
json_export_exists
index_vector_count
metadata_record_count
json_record_count
ready
```

The status endpoint is useful for:

- operational inspection
- debugging retrieval setup
- confirming whether index rebuild has happened
- confirming whether metadata exists
- checking whether FAISS vector count and metadata record count match
- future dashboard/readiness workflows

### Chunk Metadata Schema

Status:

```text
Implemented
```

The backend includes:

```text
app/models/chunk.py
```

Implemented models:

```text
ChunkMetadata
RetrievedChunk
```

This schema formalizes the source and chunk-level structure used by retrieval results.

Current fields:

```text
source
chunk_idx
score
text
```

This improves:

- model reuse
- metadata consistency
- future JSON/SQLite migration readiness
- dashboard readiness
- retrieval inspection
- source traceability

### Metadata-Aware Retrieval

Status:

```text
Implemented
```

The retrieval script supports:

```text
query_with_metadata()
```

This returns:

```text
score
file
chunk_idx
text
```

The backend maps this into the retrieval API response:

```text
score
source
chunk_idx
text
```

This improves:

- traceability
- debugging
- retrieval inspection
- future dashboard readiness
- auditability of returned context

### Metadata Storage and Export

Status:

```text
Implemented
```

Current runtime metadata storage remains pickle-based for FAISS workflow compatibility:

```text
memory-bank/embeddings_meta.pkl
```

Current vector index remains:

```text
memory-bank/embeddings.faiss
```

The project also supports an inspectable JSON metadata export:

```text
memory-bank/embeddings_meta.json
```

The JSON export is generated by:

```text
export_metadata_json()
```

and exposed through the CLI command:

```bash
python scripts/retrieve_context.py export-meta-json
```

The JSON export includes:

```text
schema_version
source
index_file
record_count
records
```

The JSON export is not the runtime source of truth. It is an inspection and review artifact. Pickle remains the internal runtime metadata format for the current FAISS workflow.

This implements the direction from:

```text
docs/adr/0002-retrieval-metadata-storage.md
```

Current decision:

```text
Keep pickle now.
Add JSON export for inspectability.
Consider SQLite later for queryability and dashboards.
```

---

## 11. Configuration

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
ENABLE_LOCAL_API_TOKEN=false
LOCAL_API_TOKEN=
```

Defaults favor local-first security:

- bind to `127.0.0.1` by default
- require explicit configuration for external exposure
- keep token protection disabled by default for local-first development
- allow token protection to be enabled when exposing protected routes outside trusted localhost usage
- avoid requiring private secrets in public CI
- keep `env.template` safe to commit

Future configuration may include:

```text
EMBED_MODEL=text-embedding-3-small
EMBED_DIM=1536
CORS_ORIGINS=http://localhost
ENABLE_CORS=false
```

---

## 12. Security Posture

The backend is local-first.

Default assumptions:

- local usage does not require public exposure
- memory-bank must not contain secrets, PII, PHI, credentials, or client-confidential data
- `.env` files must not be committed
- `env.template` is safe to commit
- public CI should not require private secrets
- Nginx is a starter reverse-proxy example, not a fully hardened production gateway
- optional local API token protection is useful for non-localhost usage but is not full production authentication

Current safety behavior:

- only explicitly allowed memory-bank markdown files are exposed through the memory service
- generated FAISS and pickle files are not exposed as memory records
- retrieval API uses typed request validation for query and `top_k`
- retrieval API returns source filename and chunk index for traceability
- retrieval metadata has a reusable typed schema
- retrieval API handles missing and empty index states safely
- retrieval status endpoint reports readiness without requiring JSON export for runtime readiness
- retrieval rebuild test uses a temporary memory-bank and temporary FAISS files to avoid polluting real starter memory
- JSON metadata export is inspectable and generated from runtime pickle metadata
- summarization tests isolate active context writes from the real memory-bank
- summarization can disable embedding for safer test and API workflows
- CLI summarization compatibility is tested
- optional local API token protects memory, retrieval, summarization, and metrics routes when enabled
- `/health` remains public for local readiness checks
- public CI remains secret-free
- dependency checks remain active
- GitHub code scanning remains enabled through the repository security configuration

Future hardening may include:

- configurable CORS
- rate limiting
- structured audit logs
- request size limits
- managed secret storage
- encrypted storage
- workspace-level access boundaries
- production authentication and authorization if the project becomes externally hosted

---

## 13. Testing Strategy

### Implemented Tests

```text
tests/test_api_health.py
tests/test_api_memory.py
tests/test_api_retrieval.py
tests/test_api_summarization.py
tests/test_api_security.py
tests/test_cli_summarize_chat.py
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
- `GET /metrics`
- metrics response
- metrics token protection
- `GET /retrieval/status`
- retrieval status missing-state response
- retrieval status ready-state response after rebuild
- retrieval status JSON export existence field
- retrieval status index vector count
- retrieval status metadata record count
- retrieval status JSON record count
- retrieval status readiness boolean
- `POST /retrieval/query`
- retrieval response shape
- retrieval metadata fields when results are returned
- `score` field type
- `source` field type
- `chunk_idx` field type
- `text` field type
- missing retrieval index behavior
- empty retrieval index behavior
- retrieval behavior after temporary index rebuild
- source filename after rebuild
- chunk index after rebuild
- retrieved text content after rebuild
- JSON metadata export schema version
- JSON metadata export source pickle path
- JSON metadata export FAISS index path
- JSON metadata export record count
- JSON metadata export source filename
- JSON metadata export chunk index
- JSON metadata export text content
- `POST /summarization/summarize`
- summarization manual mode
- summarization fallback mode without OpenAI
- summarization active context writing through isolated temporary path
- summarization disabled embedding behavior
- summarization response shape
- summarization empty text validation
- CLI file input behavior for `scripts/summarize_chat.py`
- CLI manual stdin behavior
- CLI empty stdin handling
- CLI `--no-embed` behavior
- CLI isolated `activeContext.md` writing
- backward-compatible `call_openai_summarize()` availability
- optional token default-open behavior
- optional token missing-token rejection
- optional token wrong-token rejection
- optional token correct-token access
- optional token fail-closed misconfiguration behavior
- protected retrieval and summarization routes
- protected metrics route
- public health route behavior
- empty retrieval query validation
- invalid low `top_k` validation
- invalid high `top_k` validation

### Planned Tests

Future tests may cover:

- configurable CORS behavior
- structured logging behavior
- retrieval evaluation metrics
- backup/restore validation
- MCP server exposure defaults
- additional service-level summarization behavior if summarization expands

---

## 14. Migration Path from Current Scripts

Current scripts remain valuable.

Planned evolution:

1. Keep scripts working as CLI tools.
2. Move reusable logic into `app/services/`.
3. Update scripts to call service functions where safe.
4. Preserve backward-compatible helpers when tests or external scripts rely on them.
5. Add API routes that call the same services.
6. Add tests for both CLI and API behavior.
7. Keep public CI focused and secret-free.

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
Step 13: metadata-aware retrieval query created
Step 14: retrieval API model updated with chunk index
Step 15: retrieval service updated to return source metadata
Step 16: retrieval API tests updated to validate metadata fields
Step 17: missing retrieval index test added
Step 18: empty retrieval index test added
Step 19: retrieval-after-rebuild test added
Step 20: formal chunk metadata schema added
Step 21: retrieval model updated to reuse chunk schema
Step 22: retrieval metadata storage ADR added
Step 23: JSON metadata export added
Step 24: JSON metadata export test added
Step 25: generated file expectations documented
Step 26: retrieval status response model added
Step 27: retrieval status service logic added
Step 28: retrieval status route added
Step 29: retrieval status tests added
Step 30: summarization models added
Step 31: summarization service added
Step 32: summarization route added
Step 33: summarization router registered in app
Step 34: summarization API tests added
Step 35: backend design, roadmap, README, and demo workflow updated for summarization
Step 36: summarize_chat.py refactored to reuse SummarizationService
Step 37: call_openai_summarize() compatibility restored
Step 38: CLI compatibility tests added
Step 39: SECURITY.md expanded for local-first security and exposure assumptions
Step 40: optional local API token settings added
Step 41: local API token security helper added
Step 42: memory, retrieval, summarization, and metrics routes protected when token mode is enabled
Step 43: API security tests added and expanded
Step 44: env.template and README updated for local token usage
```

Next:

```text
Step 45: update roadmap for optional local API token implementation
Step 46: update demo workflow with optional token demo
Step 47: consider configurable CORS settings
Step 48: add structured logging
```

---

## 15. Senior Engineering Rationale

This backend design demonstrates:

- separation of concerns
- API contract thinking
- local-first security posture
- service-oriented architecture
- typed backend models
- reusable metadata schema design
- reusable summarization service design
- optional local API token protection
- testability
- operational awareness
- clear public CI vs configured integration separation
- realistic evolution from scripts to backend services
- incremental delivery through green, auditable slices
- traceable retrieval response design
- defensive behavior for missing and empty retrieval indexes
- integration-style retrieval verification after index rebuild
- explicit metadata storage decision-making through ADRs
- inspectable metadata export without breaking runtime compatibility
- operational retrieval readiness reporting
- summarization API behavior with manual and fallback modes
- backward-compatible CLI refactoring
- local security documentation and implementation
- protected sensitive local routes while preserving public readiness checks

The repository is intentionally scoped as a developer infrastructure project. Its backend value comes from making AI-assisted development memory reliable, inspectable, testable, secure-by-configuration, and extensible.

The first backend slice strengthened the senior-backend signal by moving the repository from documentation and scripts into a tested FastAPI service structure without breaking the existing workflow.

The second backend slice strengthened the AI systems/backend signal further by exposing retrieval through a typed API while preserving the existing CLI retrieval workflow.

The retrieval metadata improvement strengthens the system further by making retrieval results easier to inspect, debug, audit, and eventually display in a dashboard.

The retrieval reliability tests strengthen the system by proving the API handles missing and empty local retrieval state safely.

The retrieval-after-rebuild test strengthens the system by proving the API can return actual indexed memory content from an isolated temporary memory-bank without polluting the real starter memory.

The formal chunk metadata schema strengthens the system by making retrieval metadata reusable, typed, and ready for future storage, inspection, and dashboard layers.

The JSON metadata export strengthens the system by giving reviewers and future dashboard workflows an inspectable metadata artifact while preserving pickle as the stable internal runtime format for FAISS compatibility.

The retrieval status endpoint strengthens the system by giving developers and reviewers a clear operational view of whether retrieval storage is present, populated, aligned, and ready.

The summarization API strengthens the system by exposing active context summarization through typed backend contracts while preserving fallback behavior and avoiding real memory-bank pollution in tests.

The CLI compatibility tests strengthen the system by protecting the existing script workflow after refactoring toward shared service logic.

The optional local API token slice strengthens the security posture by documenting and implementing a lightweight local protection mechanism for sensitive endpoints without breaking default local development.

---

## 16. Implementation Checklist

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

### Completed Retrieval Metadata Improvement

- [x] Add `query_with_metadata()` to `scripts/retrieve_context.py`
- [x] Preserve existing `query()` function behavior
- [x] Preserve CLI retrieval behavior
- [x] Add `chunk_idx` to `RetrievalResult`
- [x] Return source filename from retrieval API
- [x] Return chunk index from retrieval API
- [x] Update retrieval API tests to validate metadata fields

### Completed Retrieval Reliability Tests

- [x] Test missing retrieval index behavior
- [x] Test empty retrieval index behavior
- [x] Confirm retrieval API returns empty results safely when local index state is not ready

### Completed Retrieval After Rebuild Test

- [x] Use temporary memory-bank for retrieval rebuild test
- [x] Use temporary FAISS index and metadata file
- [x] Rebuild retrieval index inside isolated test state
- [x] Query retrieval API after rebuild
- [x] Validate returned source filename
- [x] Validate returned chunk index
- [x] Validate returned text content
- [x] Avoid polluting real `memory-bank/`

### Completed Formal Chunk Metadata Schema

- [x] Add `app/models/chunk.py`
- [x] Add `ChunkMetadata`
- [x] Add `RetrievedChunk`
- [x] Update `RetrievalResult` to inherit from `RetrievedChunk`
- [x] Preserve existing retrieval API response shape
- [x] Keep tests green

### Completed Retrieval Metadata Storage ADR

- [x] Add `docs/adr/0002-retrieval-metadata-storage.md`
- [x] Keep pickle as the current internal runtime metadata format
- [x] Document JSON export as the next inspectability step
- [x] Document SQLite as a later option for queryability and dashboards

### Completed JSON Metadata Export

- [x] Add `META_JSON_FILE`
- [x] Add `_metadata_json_payload()`
- [x] Add `export_metadata_json()`
- [x] Add `export-meta-json` CLI command
- [x] Preserve pickle runtime metadata behavior
- [x] Add JSON export test coverage
- [x] Validate JSON schema version
- [x] Validate JSON source pickle path
- [x] Validate JSON FAISS index path
- [x] Validate JSON record count
- [x] Validate JSON exported record fields

### Completed Generated File Documentation

- [x] Update `.gitignore` for generated retrieval metadata exports
- [x] Add `docs/GENERATED_FILES.md`
- [x] Document generated retrieval files
- [x] Document version-control expectations
- [x] Document secrets, logs, backups, caches, and temporary files

### Completed Retrieval Status Endpoint

- [x] Add `RetrievalStatusResponse`
- [x] Add retrieval service `status()`
- [x] Add index, metadata, and JSON export existence checks
- [x] Add vector, metadata, and JSON record counts
- [x] Add conservative readiness calculation
- [x] Add `GET /retrieval/status`
- [x] Add retrieval status API tests
- [x] Keep retrieval query behavior unchanged

### Completed Summarization API Slice

- [x] Add `app/models/summarization.py`
- [x] Add `SummarizationRequest`
- [x] Add `SummarizationResponse`
- [x] Add `app/services/summarization_service.py`
- [x] Add manual summarization mode
- [x] Add fallback summarization mode
- [x] Add active context writing
- [x] Add optional embedding behavior
- [x] Add `app/api/routes_summarization.py`
- [x] Add `POST /summarization/summarize`
- [x] Register summarization router in `app/main.py`
- [x] Add `tests/test_api_summarization.py`
- [x] Test manual mode
- [x] Test fallback mode
- [x] Test empty text validation
- [x] Isolate active context writing in tests
- [x] Keep existing `scripts/summarize_chat.py` workflow intact

### Completed Summarization CLI Compatibility Slice

- [x] Refactor `scripts/summarize_chat.py` to reuse `SummarizationService`
- [x] Preserve `call_openai_summarize()` compatibility
- [x] Add `tests/test_cli_summarize_chat.py`
- [x] Test file input
- [x] Test manual stdin
- [x] Test empty stdin
- [x] Test `--no-embed`
- [x] Test isolated active context writing
- [x] Test backward-compatible helper availability

### Completed Local Security Slice

- [x] Expand `docs/SECURITY.md`
- [x] Add local token settings to `app/core/config.py`
- [x] Add `app/core/security.py`
- [x] Protect memory routes
- [x] Protect retrieval routes
- [x] Protect summarization route
- [x] Protect metrics route
- [x] Keep health route public
- [x] Add `tests/test_api_security.py`
- [x] Test default open local-first behavior
- [x] Test missing token rejection
- [x] Test wrong token rejection
- [x] Test correct token access
- [x] Test fail-closed missing token configuration
- [x] Test protected retrieval route
- [x] Test protected summarization route
- [x] Test protected metrics route
- [x] Update `env.template`
- [x] Update `README.md`

### Next Backend Slices

- [ ] Update roadmap for optional local API token implementation
- [ ] Update demo workflow with optional token demo
- [ ] Add configurable CORS
- [ ] Add structured logging module
- [ ] Add broader readiness endpoint if needed beyond retrieval status
- [ ] Add stronger integration tests
- [ ] Add local backend run instructions
- [ ] Consider converting `scripts/run_mcp_server.py` into a wrapper around `app.main`

---

## 17. Summary

The backend evolution is turning the current script-based memory system into a clearer local-first API service without overclaiming production SaaS maturity.

The current direction is:

```text
template memory system
→ local scripts
→ typed FastAPI backend slice
→ tested service layer
→ retrieval API
→ metadata-aware retrieval
→ retrieval reliability
→ retrieval after rebuild
→ formal chunk metadata schema
→ metadata storage ADR
→ JSON metadata export
→ generated file expectations
→ retrieval status endpoint
→ summarization API
→ CLI compatibility
→ local security documentation
→ optional local API token protection
→ optional production hardening
```

The first FastAPI backend slice is implemented, tested, documented, and green.

The retrieval API slice is implemented, tested, documented, and green.

The retrieval metadata improvement is implemented, tested, documented, and green.

The retrieval reliability tests for missing and empty indexes are implemented, tested, documented, and green.

The retrieval-after-rebuild test is implemented, tested, documented, and green.

The formal chunk metadata schema is implemented, documented, and green.

The retrieval metadata storage ADR is accepted and green.

The JSON metadata export is implemented, tested, documented, and green.

The generated file expectations are documented and green.

The retrieval status endpoint is implemented, tested, documented, and green.

The summarization API is implemented, tested, documented, and green.

The summarization CLI compatibility slice is implemented, tested, documented, and green.

The local security documentation is complete and green.

The optional local API token protection slice is implemented, tested, documented, and green.

The next meaningful engineering steps are to update the roadmap and demo workflow for optional token usage, then add configurable CORS and structured logging as final senior-backend hardening items.

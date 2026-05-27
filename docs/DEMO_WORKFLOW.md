# Demo Workflow – Cursor Memory Project

> This document explains how a technical reviewer can evaluate the Cursor Memory Project as a public demonstration of AI-assisted development workflow infrastructure, persistent memory, retrieval, MCP-oriented context delivery, local-first backend structure, and CI/QA practices.

---

## 1. What This Demo Proves

This repository demonstrates how an AI-assisted development workflow can preserve project context across long-running work without relying only on Cursor chat history, ChatGPT memory, or one-off prompt context.

It shows:

- persistent project memory using structured markdown files
- memory-bank template mode for new projects
- rolling active context summarization
- retrieval-based context loading
- metadata-aware retrieval results with source filename and chunk index
- MCP server structure for exposing memory to Cursor
- Python automation for summarization, retrieval, logging, backups, and status updates
- fallback behavior when external API keys are unavailable
- public CI with linting, type checking, dependency/security checks, and smoke tests
- GitHub code scanning / CodeQL security analysis through repository security configuration
- documentation-first engineering practices
- separation between public smoke tests and environment-specific integration workflows
- tested FastAPI backend slices for health, memory access, metrics, retrieval, and retrieval metadata

This demo is not intended to prove a complete production SaaS product. It is intended to show the technical workflow layer behind AI-assisted development systems and the way this repository can serve as a reusable setup method before a real project begins.

---

## 2. Reviewer Quick Path

A reviewer can inspect the repository in this order:

1. `README.md`  
   Public overview, system purpose, memory-bank template mode, scope, CI strategy, implemented backend slices, and production evolution path.

2. `memory-bank/README.md`  
   Explains why memory-bank files start mostly empty and how they should be populated after real project kickoff.

3. `docs/ARCHITECTURE.md`  
   System architecture, data flow, runtime modes, failure modes, tradeoffs, and production roadmap.

4. `docs/BACKEND_DESIGN.md`  
   Backend architecture, implemented FastAPI slices, service/model structure, API surface, metadata-aware retrieval, tests, and next summarization slice.

5. `docs/adr/0001-public-ci-vs-integration-tests.md`  
   Architecture Decision Record explaining public CI vs secret-dependent integration tests.

6. `.cursor-rules.md`  
   Operational rules for how Cursor should use memory, logs, project rules, and context.

7. `app/main.py`  
   FastAPI backend entry point with health, memory, metrics, and retrieval routes.

8. `app/services/memory_service.py`  
   Reusable service layer for loading allowed memory-bank files.

9. `app/services/retrieval_service.py`  
   Reusable retrieval service that exposes metadata-aware retrieval results through typed backend responses.

10. `app/api/routes_retrieval.py`  
   FastAPI route for `POST /retrieval/query`.

11. `scripts/retrieve_context.py`  
   CLI retrieval workflow for building and querying the memory index, including metadata-aware retrieval through `query_with_metadata()`.

12. `scripts/summarize_chat.py`  
   Summarization workflow for converting recent session logs into active project context.

13. `.github/workflows/ci.yml`  
   Public CI workflow.

14. `tests/test_api_health.py`, `tests/test_api_memory.py`, and `tests/test_api_retrieval.py`  
   FastAPI TestClient tests for the implemented backend slices and retrieval metadata fields.

15. `status/roadmap.md`  
   Roadmap for evolving the project toward a stronger local-first backend/service layer.

---

## 3. Local Demo Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Optional: copy the environment template.

```bash
cp env.template .env
```

If `OPENAI_API_KEY` is available, automated summarization and embeddings can use OpenAI-backed workflows.

If no API key is configured, the system can still run in fallback/manual mode.

---

## 4. Step-by-Step Demo

### Step 1 — Inspect template memory

Inspect the memory-bank folder:

```bash
ls memory-bank
```

The memory-bank stores the starter files for project context, active memory, system patterns, technical notes, and progress.

The files start mostly empty by design. This repository is a setup method for Cursor-based work. Real project knowledge should be added only after project kickoff, real discovery, implementation, decisions, errors, and milestones.

Read:

```text
memory-bank/README.md
```

---

### Step 2 — Inspect the implemented backend structure

Review:

```text
app/
  main.py
  api/
    routes_health.py
    routes_memory.py
    routes_retrieval.py
  core/
    config.py
  models/
    health.py
    memory.py
    retrieval.py
  services/
    memory_service.py
    retrieval_service.py
```

The implemented backend currently supports:

```text
GET /health
GET /memory
GET /memory/{record_id}
GET /metrics
POST /retrieval/query
```

It demonstrates:

- FastAPI application structure
- typed Pydantic response models
- typed retrieval request/response models
- centralized local-first configuration
- service-layer separation
- explicit route modules
- metrics endpoint
- retrieval API
- metadata-aware retrieval results
- API tests

---

### Step 3 — Run the backend API locally

Run:

```bash
uvicorn app.main:app --reload
```

Then open or call:

```text
http://127.0.0.1:8000/health
http://127.0.0.1:8000/memory
http://127.0.0.1:8000/memory/README
http://127.0.0.1:8000/metrics
```

Expected result:

- `/health` returns service status and memory-bank availability
- `/memory` returns allowed memory-bank markdown records
- `/memory/README` returns the memory-bank README record
- `/metrics` exposes Prometheus-compatible metrics

To test the retrieval endpoint, use an API client or curl:

```bash
curl -X POST http://127.0.0.1:8000/retrieval/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the project architecture?", "top_k": 5}'
```

Expected result:

- `/retrieval/query` returns the submitted query and a list of retrieval results
- each retrieval result may include `score`, `source`, `chunk_idx`, and `text`
- `source` identifies the memory-bank source filename
- `chunk_idx` identifies the retrieved chunk position in that source file
- empty query text is rejected
- `top_k` below 1 is rejected
- `top_k` above 20 is rejected

---

### Step 4 — Generate or update active context

Automated mode:

```bash
python scripts/summarize_chat.py --chat-log path/to/chat.txt --max-lines 800
```

Manual/fallback mode:

```bash
cat path/to/chat.txt | python scripts/summarize_chat.py --stdin --manual
```

Expected result:

```text
memory-bank/activeContext.md
```

is created or updated with a rolling summary.

---

### Step 5 — Build the retrieval index

Run:

```bash
python scripts/retrieve_context.py rebuild
```

Expected result:

- memory-bank content is processed
- embeddings are generated or fallback vectors are used
- retrieval index files are created or updated
- retrieval metadata stores source file, chunk index, and text
- generated retrieval files remain excluded from version control

---

### Step 6 — Query memory through the CLI retrieval workflow

Run:

```bash
python scripts/retrieve_context.py query --text "What is the current project architecture?" --top-k 5
```

Expected result:

- the retrieval engine returns relevant memory chunks
- the assistant can use retrieved context to continue work with less information loss

The same retrieval capability is now also exposed through the backend endpoint:

```text
POST /retrieval/query
```

For backend/API usage, retrieval metadata is available through:

```text
source
chunk_idx
score
text
```

---

### Step 7 — Start the legacy/local memory server

Run:

```bash
python scripts/run_mcp_server.py
```

Expected result:

- local memory endpoint becomes available
- Cursor can load project context from the memory server

Example local endpoint:

```text
http://localhost:7331/memory
```

This script remains useful while the backend package evolves. Over time, it may become a wrapper around `app.main`.

---

### Step 8 — Inspect operational status

Review:

```text
status/release_checklist.md
status/roadmap.md
status/checklist_onboarding.md
status/checklist_deployment.md
```

These files show how the project separates template setup, local development, deployment assumptions, release readiness, and future backend evolution.

---

## 5. Public CI Demo

The public CI workflow validates the repository without requiring private secrets.

It runs:

```bash
ruff check .
mypy scripts tests
pip-audit --strict
pytest tests/test_add_chunk.py tests/test_edge_cases.py -q
```

Additional backend API tests exist in:

```text
tests/test_api_health.py
tests/test_api_memory.py
tests/test_api_retrieval.py
```

These demonstrate:

- FastAPI endpoint testing
- response-shape validation
- memory list behavior
- single-record retrieval behavior
- missing-record 404 behavior
- retrieval endpoint response shape
- retrieval metadata field validation
- empty query validation
- `top_k` validation

The public CI demonstrates:

- linting discipline
- type-checking discipline
- dependency/security awareness
- smoke-test coverage for public workflows
- public CI that does not depend on private secrets

Backup and full end-to-end tests are intentionally separated because they require environment-specific secrets such as `GPG_KEY_ID`.

See:

```text
docs/adr/0001-public-ci-vs-integration-tests.md
```

---

## 6. What to Inspect Technically

### AI-assisted development workflow

Inspect:

```text
.cursor-rules.md
README.md
memory-bank/README.md
docs/ARCHITECTURE.md
```

These files show how project memory, documentation, AI-assisted development rules, and template-mode assumptions are structured.

### Backend API structure

Inspect:

```text
app/main.py
app/api/routes_health.py
app/api/routes_memory.py
app/api/routes_retrieval.py
app/core/config.py
app/models/health.py
app/models/memory.py
app/models/retrieval.py
app/services/memory_service.py
app/services/retrieval_service.py
```

These files show the implemented backend slices: health, memory access, retrieval, typed models, service separation, metrics, and metadata-aware retrieval responses.

### Backend API tests

Inspect:

```text
tests/test_api_health.py
tests/test_api_memory.py
tests/test_api_retrieval.py
```

These files demonstrate FastAPI TestClient coverage for the implemented backend routes and retrieval metadata fields.

### Retrieval workflow

Inspect:

```text
scripts/retrieve_context.py
app/services/retrieval_service.py
app/api/routes_retrieval.py
```

These files demonstrate how the existing FAISS-based retrieval logic is preserved while being exposed through the FastAPI backend.

The retrieval flow now supports metadata-aware results through:

```text
query_with_metadata()
```

This supports API-level traceability through:

```text
source
chunk_idx
score
text
```

### Summarization workflow

Inspect:

```text
scripts/summarize_chat.py
```

This file demonstrates how session logs can be transformed into rolling active context.

The next backend slice may extract this into:

```text
app/models/summarization.py
app/services/summarization_service.py
app/api/routes_summarization.py
tests/test_api_summarization.py
```

### MCP/context delivery

Inspect:

```text
scripts/run_mcp_server.py
```

This file demonstrates the local context-serving layer used before or alongside the structured backend API.

### CI and QA workflow

Inspect:

```text
.github/workflows/ci.yml
```

Also review the repository security page for GitHub code scanning / CodeQL status.

These demonstrate public quality and security checks.

### Operational documentation

Inspect:

```text
status/release_checklist.md
status/roadmap.md
docs/DEMO_WORKFLOW.md
docs/BACKEND_DESIGN.md
docs/adr/0001-public-ci-vs-integration-tests.md
```

These files show how the repository documents decisions, release assumptions, backend implementation status, and future backend evolution.

---

## 7. Expected Reviewer Interpretation

This repository is best understood as a public technical artifact for AI-assisted development infrastructure.

It demonstrates:

- system design thinking
- context engineering
- retrieval workflow design
- metadata-aware retrieval traceability
- local automation
- CI and QA discipline
- documentation maturity
- production-evolution awareness
- clear separation between public smoke tests and configured integration tests
- practical Python automation for LLM-assisted development workflows
- tested FastAPI backend structure for local memory access
- typed retrieval API
- incremental backend delivery through green, auditable slices

It should not be interpreted as a complete production SaaS application. Instead, it shows the workflow and infrastructure patterns that can support larger LLM and agent-based systems.

---

## 8. Current Scope vs Future Backend Evolution

### Current Scope

- local-first memory-bank setup
- markdown-based project memory
- summarization workflow
- CLI retrieval workflow
- metadata-aware retrieval workflow
- MCP-oriented local memory server
- tested FastAPI backend slices for health, memory access, metrics, and retrieval
- public CI
- GitHub code scanning / CodeQL through repository security configuration
- Docker/Nginx starter configuration
- documentation and status checklists

### Implemented Backend Slices

Implemented:

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

Implemented retrieval response fields:

```text
score
source
chunk_idx
text
```

### Next Backend Slice

The next backend slice may extract summarization into the backend service layer:

```text
app/models/summarization.py
app/services/summarization_service.py
app/api/routes_summarization.py
tests/test_api_summarization.py
```

The existing CLI workflow should remain available:

```text
scripts/summarize_chat.py
```

### Future Backend Evolution

A stronger backend-oriented version of this workflow could add:

- service layer for summarization
- authenticated API endpoints
- external managed vector database
- user/project isolation
- background jobs for indexing and summarization
- observability and tracing
- retrieval evaluation metrics
- dashboard for memory inspection
- full integration CI using configured secrets
- deployment to cloud infrastructure

---

## 9. Pending Non-Blocking Cleanup

### GitHub Actions Node.js 20 Warning

Some GitHub Actions runs may show a warning that certain actions are running on Node.js 20 and may need future updates.

This is non-blocking because workflows are passing successfully.

Future cleanup may include reviewing stable action versions such as:

```text
actions/checkout@v4 → actions/checkout@v5
actions/setup-python@v5 → actions/setup-python@v6
```

This should be done later, after the backend documentation and first backend slices are stable.

---

## 10. Summary

The demo shows how to structure an AI-assisted development environment that can preserve memory, retrieve context, support human review, maintain documentation, expose a local backend API, and keep public quality checks green.

The main technical value is not a single script. The value is the architecture of the workflow: persistent memory, retrieval, MCP-oriented context delivery, FastAPI backend structure, automation, CI/QA, documentation, production-aware engineering decisions, and metadata-aware traceability.

The health/memory backend slice is implemented, tested, documented, and green.

The retrieval API slice is implemented, tested, documented, and green.

The retrieval metadata improvement is implemented, tested, documented, and green.

The next meaningful engineering step is the summarization service slice.

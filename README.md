# Cursor Memory Project 📚🤖

![CI](https://github.com/lexmourao/cursor-memory-project/actions/workflows/ci.yml/badge.svg)

Maintenance note: This repository is a public demonstration of Cursor-based AI-assisted development workflows, persistent project memory, retrieval, MCP server structure, FastAPI backend structure, local-first security controls, documentation, automated logging, testing, and QA practices.

Welcome to the **Cursor Memory Project**.

The objective of this repository is to provide a turn-key template that empowers the Cursor AI assistant and human collaborators with persistent project context, reproducible workflows, structured documentation, retrieval, local memory APIs, summarization workflows, optional local API token protection, and auditable development practices.

---

## What This Demonstrates

This repository demonstrates my approach to AI-assisted systems development:

- Cursor-based AI-assisted development workflows
- Persistent project memory and rolling context for long-running AI projects
- Retrieval and context-loading patterns for LLM-assisted work
- Metadata-aware retrieval with source filename and chunk index traceability
- Retrieval status/readiness reporting for local index and metadata state
- Summarization API workflows for active context updates
- MCP server structure for exposing project memory to an AI coding environment
- Tested FastAPI backend slices for memory access, retrieval, summarization, health checks, metrics, and optional local token protection
- Python automation for summarization, retrieval, logging, backups, and status updates
- CI practices using linting, type checking, dependency/security checks, and smoke tests
- GitHub code scanning / CodeQL through repository security configuration
- Documentation-first project structure for auditable and reproducible AI workflows
- Human-in-the-loop fallback modes when API keys or external services are unavailable
- Separation between public smoke tests and environment-specific integration tests
- Local-first security assumptions with optional token enforcement for protected routes

---

## Why This Matters for LLM & Agent Systems

LLM and agent-based systems depend heavily on context quality, memory structure, retrieval reliability, summarization, workflow documentation, traceability, security boundaries, and repeatable development practices.

This project explores how an AI-assisted development environment can maintain project memory across long-running work, expose structured context to an AI coding assistant, and support better continuity between human decisions, automated summaries, retrieval workflows, backend APIs, security controls, and implementation tasks.

The repository is not intended to represent a complete production SaaS platform. It is a public technical artifact showing how I structure AI-assisted development infrastructure, retrieval patterns, project memory, backend evolution, CI/QA practices, local-first security assumptions, and documentation workflows that can support larger LLM and agent-based systems.

---

## Core System Concepts

The system is organized around six core ideas:

1. **Persistent project memory**  
   A structured `memory-bank` stores active context, summaries, and project knowledge that can be reused across sessions.

2. **Retrieval and context loading**  
   Scripts and API endpoints support retrieval workflows so relevant project context can be rebuilt, searched, traced to source files, and exposed to the assistant.

3. **MCP server structure**  
   A local MCP-oriented server pattern exposes project memory to Cursor or other AI-assisted development environments.

4. **FastAPI backend slices**  
   The `app/` package exposes tested API endpoints for health, memory access, single memory-record retrieval, retrieval queries, retrieval status, summarization, metadata-aware retrieval results, Prometheus-compatible metrics, and optional local token protection.

5. **Documentation-first workflow**  
   The repo includes docs, diary, status, logs, setup instructions, project rules, generated-file expectations, and security guidance to make work auditable and easier to continue.

6. **Quality, security, and automation practices**  
   CI, linting, type checking, smoke tests, dependency/security checks, GitHub code scanning, local-first security guidance, and optional API token tests help keep the public workflow maintainable.

---

## Implemented Backend Slices

The FastAPI backend slices are implemented, tested, and green.

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

Implemented backend files:

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

Implemented API tests:

```text
tests/test_api_health.py
tests/test_api_memory.py
tests/test_api_retrieval.py
tests/test_api_summarization.py
tests/test_api_security.py
tests/test_cli_summarize_chat.py
```

These backend slices demonstrate:

- FastAPI application structure
- typed Pydantic response models
- typed retrieval request/response models
- typed retrieval status model
- typed summarization request/response models
- local-first configuration
- optional local API token configuration
- reusable security helper
- service-layer separation
- route modules
- memory-bank access through an API
- retrieval query access through an API
- retrieval readiness/status access through an API
- summarization access through an API
- metadata-aware retrieval responses
- missing-record 404 behavior
- request validation for retrieval queries
- request validation for summarization input
- Prometheus-compatible metrics
- optional token protection for sensitive local routes
- public health route for readiness checks
- tested backend behavior with FastAPI TestClient

The retrieval API returns traceable result fields:

```text
score
source
chunk_idx
text
```

This makes retrieval results easier to inspect, debug, audit, and eventually display in a dashboard.

The retrieval status endpoint reports:

```text
index_exists
metadata_exists
json_export_exists
index_vector_count
metadata_record_count
json_record_count
ready
```

The summarization API returns:

```text
summary
word_count
model
used_fallback
wrote_active_context
embedded
```

The existing CLI workflow remains preserved:

```text
scripts/summarize_chat.py
scripts/retrieve_context.py
```

---

## Memory-Bank Template Mode

The `memory-bank/` directory is initialized as a starter template. In a new project, these files begin mostly empty by design and are populated only after real discovery, implementation, decisions, errors, and milestones occur.

This prevents fake or outdated context from contaminating future Cursor, ChatGPT, Codex, or AI-assisted development work.

See:

```text
memory-bank/README.md
```

---

## Quickstart — Full Memory System

These steps get the summarization, retrieval, MCP server, and backend API working locally.

1. Clone the repo and install dependencies:

```bash
pip install -r requirements.txt
```

2. Copy the environment template and optionally add your OpenAI key:

```bash
cp env.template .env
```

If `OPENAI_API_KEY` is present, automated summaries and embeddings can use OpenAI.  
If it is absent, scripts and APIs fall back to manual, fallback, or zero-cost modes.

3. Start the FastAPI backend:

```bash
uvicorn app.main:app --reload
```

Then inspect:

```text
http://127.0.0.1:8000/health
http://127.0.0.1:8000/memory
http://127.0.0.1:8000/memory/README
http://127.0.0.1:8000/metrics
http://127.0.0.1:8000/retrieval/status
```

Test the retrieval API:

```bash
curl -X POST http://127.0.0.1:8000/retrieval/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the project architecture?", "top_k": 5}'
```

Expected retrieval result fields:

```text
score
source
chunk_idx
text
```

Test the summarization API in manual mode:

```bash
curl -X POST http://127.0.0.1:8000/summarization/summarize \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Manual summary for the current backend slice.",
    "model": "gpt-4o",
    "manual": true,
    "embed": false
  }'
```

Expected summarization response fields:

```text
summary
word_count
model
used_fallback
wrote_active_context
embedded
```

4. Optional: enable local API token protection for protected routes.

In `.env`:

```env
ENABLE_LOCAL_API_TOKEN=true
LOCAL_API_TOKEN=replace-with-a-local-dev-token
```

When token mode is enabled, protected routes require:

```text
Authorization: Bearer <LOCAL_API_TOKEN>
```

Example protected retrieval request:

```bash
curl -X POST http://127.0.0.1:8000/retrieval/query \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer replace-with-a-local-dev-token" \
  -d '{"query": "What is the project architecture?", "top_k": 5}'
```

Example protected metrics request:

```bash
curl http://127.0.0.1:8000/metrics \
  -H "Authorization: Bearer replace-with-a-local-dev-token"
```

`GET /health` remains public for local readiness checks.

5. Start the legacy/local MCP-style memory server if needed:

```bash
python scripts/run_mcp_server.py &
```

Cursor can fetch:

```text
http://localhost:7331/memory
```

6. Generate or update the rolling summary through the CLI:

```bash
python scripts/summarize_chat.py --chat-log path/to/chat.txt --max-lines 800
```

Manual mode:

```bash
cat path/to/chat.txt | python scripts/summarize_chat.py --stdin --manual
```

7. Build the retrieval index:

```bash
python scripts/retrieve_context.py rebuild
```

8. Export inspectable retrieval metadata JSON:

```bash
python scripts/retrieve_context.py export-meta-json
```

9. Query memory through the CLI retrieval workflow:

```bash
python scripts/retrieve_context.py query --text "What is the current project architecture?" --top-k 5
```

The CLI keeps the original simple output behavior, while the backend API exposes richer metadata for inspection and future UI/dashboard use.

---

## Generated Files and Version-Control Expectations

Retrieval workflows can generate local runtime artifacts such as:

```text
memory-bank/embeddings.faiss
memory-bank/embeddings_meta.pkl
memory-bank/embeddings_meta.json
```

These files are ignored by `.gitignore` and should not be committed by default.

See:

```text
docs/GENERATED_FILES.md
docs/adr/0002-retrieval-metadata-storage.md
```

Current metadata storage decision:

```text
Keep pickle now.
Add JSON export for inspectability.
Consider SQLite later for queryability and dashboards.
```

---

## Running Tests

Run the local test suite:

```bash
pytest -q
```

The public CI workflow runs:

- `ruff check .` for linting
- `mypy scripts tests` for type checking
- `pip-audit --strict` for dependency/security checks
- focused smoke tests for public workflow validation

Backend API and CLI tests include:

```text
tests/test_api_health.py
tests/test_api_memory.py
tests/test_api_retrieval.py
tests/test_api_summarization.py
tests/test_api_security.py
tests/test_cli_summarize_chat.py
```

The retrieval tests validate response shape, query validation, `top_k` validation, metadata fields, missing/empty index behavior, retrieval after index rebuild, JSON metadata export, and retrieval status readiness.

The summarization tests validate manual mode, fallback mode, active context writing through an isolated temporary path, disabled embedding behavior, response fields, and empty text validation.

The CLI compatibility tests validate file input, manual stdin mode, empty stdin handling, `--no-embed` behavior, isolated `activeContext.md` writing, and backward-compatible `call_openai_summarize()` availability.

The security tests validate default open local-first behavior, missing token rejection, wrong token rejection, correct Bearer token access, fail-closed misconfiguration handling, protected memory/retrieval/summarization/metrics routes, and public health route behavior.

Some backup and end-to-end tests require environment-specific configuration such as `GPG_KEY_ID` for encrypted backups. These are intentionally separated from the public smoke-test workflow and should be run in a configured integration environment.

---

## Environment Variables

The project reads the following variables. See `env.template`.

| Variable | Purpose |
|---|---|
| `OPENAI_API_KEY` | Enables automated summarization and embeddings via OpenAI API. Leaving it blank triggers fallback modes. |
| `OPENAI_API_KEY_FILE` | Path inside container to a file containing the key when using Docker secrets. |
| `ENABLE_LOCAL_API_TOKEN` | Enables optional Bearer token protection for protected local API routes when set to `true`. Defaults to `false`. |
| `LOCAL_API_TOKEN` | Token required in `Authorization: Bearer <LOCAL_API_TOKEN>` when local API token protection is enabled. |
| `GPG_KEY_ID` | Required for encrypted backup workflows. |
| `GPG_KEY_ID_FILE` | Path to a file containing the recipient key ID for encrypted backups. |
| `SERVICE_NAME` | Optional backend service name override. |
| `RUNTIME_MODE` | Optional backend runtime mode, defaults to `local`. |
| `MEMORY_BANK_DIR` | Optional path to memory-bank directory, defaults to `memory-bank`. |
| `HOST` | Optional backend host setting, defaults to `127.0.0.1`. |
| `PORT` | Optional backend port setting, defaults to `7331`. |

Load them with:

```bash
source .env
```

or your preferred shell mechanism.

---

## High-Level Folder Overview

| Path | Purpose |
|---|---|
| `app/` | FastAPI backend package for health, memory access, retrieval, retrieval status, summarization, metadata-aware retrieval results, metrics, and optional local token protection |
| `cursor_setup_instructions/` | Canonical setup guide and Cursor workflow instructions |
| `docs/` | Architecture, backend design, generated-file guidance, security, deployment, and technical documentation |
| `memory-bank/` | Starter memory template for persistent context, active memory, and project knowledge |
| `scripts/` | Automation, summarization, retrieval, backups, logging, and status scripts |
| `tests/` | Unit, smoke, validation, security, CLI compatibility, and backend API tests |
| `status/` | Current status, checklists, and roadmap |
| `diary/` | Project diary and development log |
| `logs/solutions/` | Error logs, fixes, and implementation notes |
| `nginx/` | Web/server configuration examples |
| `.github/` | CI, Dependabot, and workflow automation |
| `Dockerfile` | Container setup |
| `docker-compose.yml` | Local orchestration setup |
| `Makefile` | Common developer commands |
| `PROJECT_RULES.md` | Project operating rules and development constraints |

---

## Technical Review Notes

This repository is designed as a public technical artifact for AI-assisted development workflows. It demonstrates system structure, retrieval logic, summarization workflow, documentation discipline, local automation, backend evolution, security boundaries, and CI/QA practices.

Recommended reviewer path:

```text
README.md
memory-bank/README.md
docs/ARCHITECTURE.md
docs/BACKEND_DESIGN.md
docs/DEMO_WORKFLOW.md
docs/GENERATED_FILES.md
docs/SECURITY.md
docs/TECHNICAL_REVIEW.md
app/main.py
app/core/config.py
app/core/security.py
app/services/memory_service.py
app/services/retrieval_service.py
app/services/summarization_service.py
app/api/routes_health.py
app/api/routes_memory.py
app/api/routes_retrieval.py
app/api/routes_summarization.py
app/models/retrieval.py
app/models/summarization.py
tests/test_api_health.py
tests/test_api_memory.py
tests/test_api_retrieval.py
tests/test_api_summarization.py
tests/test_api_security.py
tests/test_cli_summarize_chat.py
scripts/retrieve_context.py
scripts/summarize_chat.py
.github/workflows/ci.yml
status/roadmap.md
```

Current scope:

- Local-first memory and retrieval workflow
- Cursor-oriented AI-assisted development setup
- MCP server structure for exposing memory context
- FastAPI backend slices for memory access, retrieval, retrieval status, summarization, health, metrics, and optional local token protection
- Metadata-aware retrieval with source file and chunk index traceability
- JSON metadata export for retrieval inspection
- Python automation scripts
- Public CI smoke tests
- Documentation and audit-oriented folder structure
- GitHub code scanning through repository security configuration

Not yet included in this public version:

- Multi-tenant production authentication
- Hosted deployment
- Enterprise observability stack
- Full database migration layer
- External managed vector database
- Production-grade user permissions
- Hosted UI or SaaS frontend

---

## Production Evolution Roadmap

A production version of this architecture could evolve toward:

- authenticated API layer for memory access
- user/project isolation
- scheduled summarization jobs
- retrieval evaluation tests
- structured observability and logging
- configurable CORS
- agent workflow monitoring
- deployment via cloud infrastructure
- frontend dashboard for memory, logs, summaries, retrieval chunks, and retrieval metadata inspection
- stronger integration tests with configured secrets and encrypted backup workflows
- managed vector database integration such as Qdrant, Pinecone, or PgVector

---

## Security and Reliability Considerations

This repository uses environment variables and file-based secrets patterns to avoid hardcoding sensitive credentials. Public CI avoids requiring private secrets for smoke-test execution.

The repo includes security and quality practices such as:

- GitHub code scanning / CodeQL through repository security configuration
- dependency/security auditing with `pip-audit`
- type checking with `mypy`
- linting with `ruff`
- branch protection
- documented fallback behavior when external APIs are unavailable
- explicit separation between public CI and secret-dependent integration workflows
- optional local API token protection for sensitive local backend routes

The memory API exposes only allowed memory-bank markdown files and does not expose generated FAISS or pickle files as memory records.

The retrieval API validates query text and `top_k` bounds before calling the retrieval service.

The retrieval API returns source filename and chunk index fields to improve traceability and auditability of returned context.

The retrieval status API reports index, metadata, JSON export, and readiness state for operational inspection.

The summarization API validates text input, supports fallback behavior, and can disable embedding for safer test or controlled workflows.

The optional local API token protects memory, retrieval, summarization, and metrics routes when `ENABLE_LOCAL_API_TOKEN=true`, while keeping `GET /health` public for local readiness checks.

---

## Pending Non-Blocking Cleanup

Some GitHub Actions runs may show a warning that certain actions are running on Node.js 20 and may need future updates.

This is non-blocking because workflows are passing successfully.

Future cleanup may include reviewing stable action versions such as:

```text
actions/checkout@v4 → actions/checkout@v5
actions/setup-python@v5 → actions/setup-python@v6
```

This should be done later, after the backend documentation and implemented backend slices are stable.

---

## Relationship to AI Agents and LLM Systems

This project is not only about storing notes. It is a context-engineering and workflow-infrastructure pattern for AI-assisted work.

The same principles can support broader LLM and agent systems:

- persistent memory
- retrieval-augmented context
- local memory APIs
- typed retrieval API
- metadata-aware context traceability
- summarization API
- retrieval status/readiness reporting
- tool-access patterns
- human-in-the-loop fallbacks
- system documentation
- workflow traceability
- local-first security boundaries
- optional protected local APIs
- separation between local development, public CI, and production integration

---

## Status

This repository is maintained as a public showcase of AI-assisted development workflow architecture and tooling. Some private/client AI agent systems cannot be fully shared publicly due to confidentiality, so this repository serves as a shareable technical layer demonstrating development workflow, retrieval, summarization, documentation, backend structure, security boundaries, and QA practices.

The health/memory backend slice is implemented, tested, documented, and green. The retrieval API slice is implemented, tested, documented, and green. The retrieval metadata improvement is implemented, tested, documented, and green. The retrieval status endpoint is implemented, tested, documented, and green. The summarization API slice is implemented, tested, documented, and green. The summarization CLI compatibility slice is implemented, tested, documented, and green. The optional local API token protection slice is implemented, tested, documented, and green.

The next meaningful engineering steps are adding configurable CORS settings, structured logging, retrieval evaluation tests, and additional local-first hardening around MCP/server exposure modes.

---

*Generated and maintained with AI-assisted development workflows using Cursor and human review.*

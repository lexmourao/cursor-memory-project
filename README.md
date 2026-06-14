# Cursor Memory Project

![CI](https://github.com/lexmourao/cursor-memory-project/actions/workflows/ci.yml/badge.svg)

This repository is a local-first AI-assisted development methodology project.

It demonstrates how persistent project memory, retrieval workflows, summarization, lightweight backend APIs, documentation discipline, tests, and GitHub workflow hygiene can support long-running AI-assisted software work.

The project is designed as a public technical portfolio artifact. It shows how I structure AI implementation work across context engineering, Python automation, FastAPI slices, retrieval/RAG-oriented workflows, local QA, documentation governance, and supervised AI-assisted development with Cursor, ChatGPT, and Claude.

Best reviewed as: AI-assisted engineering methodology, local developer tooling, RAG/memory workflow, and documentation-governed implementation system.

## What this project is

This project is:

- A local-first Cursor Memory and AI-assisted development methodology repository.
- A working example of persistent project context for long-running AI-assisted work.
- A Python and FastAPI-based implementation layer for memory access, retrieval, summarization, health checks, metrics, optional local token protection, CORS configuration, and structured logging.
- A documentation-first engineering workflow with project rules, status notes, generated-file expectations, architecture docs, tests, and review paths.
- A demonstration of how AI tools can be used as supervised engineering collaborators rather than uncontrolled autopilot.

## What this project is not

This project should not be presented as:

- A production SaaS platform.
- An enterprise compliance system.
- A fully managed security operations system.
- A multi-tenant hosted RAG product.
- A replacement for production-grade authentication, authorization, monitoring, deployment, or compliance review.

Earlier production-style workflows and compliance documents were intentionally moved into archive/ for auditability and future reference.

## What this demonstrates

This repository demonstrates my approach to AI-assisted systems development and engineering workflow design:

- Cursor-based AI-assisted development workflows.
- Persistent project memory and rolling context for long-running AI projects.
- Retrieval and context-loading patterns for LLM-assisted work.
- Metadata-aware retrieval with source filename and chunk index traceability.
- Summarization workflows for active context updates.
- MCP-style local memory server structure.
- Tested FastAPI backend slices for memory, retrieval, summarization, health, metrics, local token protection, CORS, and logging.
- Python automation for summarization, retrieval, logging, backups, and status updates.
- Local test baseline stabilization with pytest.
- CI hygiene with Ruff, mypy, pip-audit, smoke tests, and CodeQL.
- Documentation-first project structure for auditable and reproducible AI workflows.
- Human-in-the-loop fallback modes when API keys or external services are unavailable.
- Explicit separation between public smoke tests and environment-specific integration tests.
- Scope control through archival of overbuilt workflows and production-style documentation.

## Why this matters for LLM and agent systems

LLM and agent-based systems depend on more than prompts. They need context quality, memory structure, retrieval reliability, summarization, workflow documentation, traceability, testing, safety boundaries, and repeatable development practices.

This project explores how an AI-assisted development environment can maintain project memory across long-running work, expose structured context to an AI coding assistant, and support continuity between human decisions, automated summaries, retrieval workflows, backend APIs, tests, and documentation.

The value of this repository is not only the codebase itself. It is the engineering process around it: diagnosing failures, separating concerns, keeping main green, documenting decisions, preserving history, and using AI tools under human review.

## System at a glance

```text
Cursor / ChatGPT / Claude
        ↓
Project Rules + Memory Bank
        ↓
Retrieval + Summarization Scripts
        ↓
FastAPI Local Backend
        ↓
Health / Memory / Retrieval / Summarization / Metrics APIs
        ↓
Tests + CI + Security Checks + Documentation Governance
```

This repository demonstrates a local-first AI-assisted development workflow where AI tools are supervised through persistent project memory, retrieval, summarization, backend API slices, local QA, CI, and documentation governance.

## Reviewer in 3 minutes

1. Read the project scope: what this project is and what it is not.
2. Check the backend implementation: `app/main.py` and `app/api/`.
3. Check the tests: `tests/`.
4. Check CI: `.github/workflows/ci.yml`.
5. Check the documentation: `docs/ARCHITECTURE.md`, `docs/BACKEND_DESIGN.md`, and `docs/TECHNICAL_REVIEW.md`.

This project should be reviewed as a local-first AI-assisted development methodology and tooling repository, not as a production SaaS backend, hosted RAG platform, or enterprise compliance product.

## How I use this workflow in real projects

When I start a new project in Cursor, I use this repository as a reusable setup and methodology reference—not as a finished application to deploy as-is.

1. I copy or include [`cursor_setup_instructions/`](cursor_setup_instructions/) inside the new project folder.
2. In the first prompt, I state the goal of that project in plain language.
3. Cursor reads the setup instructions and generates the **target scaffold**: folders, rules, status files, diary, logs, error tracking, and automation hooks.
4. As work proceeds, **local** diary, logs, errors, and solutions record what happened, what failed, and what was solved.
5. Those local tracking files stay on my machine; they are **not pushed to GitHub** unless I explicitly approve a public change.
6. Memory-bank and context files fill in only after real discovery, implementation, decisions, and milestones—not with placeholder project history.
7. The outcome is modular, versioned, traceable, auditable AI-assisted work where the assistant does not restart from zero every session.

## Quick proof points

- CI badge is visible and workflow is active.
- FastAPI backend slices are implemented and tested.
- Tests cover health, memory, retrieval, summarization, security, CORS, and CLI compatibility.
- Local token protection, CORS controls, safe logging, and retrieval traceability are documented.
- The project clearly separates public smoke tests from secret-dependent integration tests.

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
   The `app/` package exposes tested API endpoints for health, memory access, single memory-record retrieval, retrieval queries, retrieval status, summarization, metadata-aware retrieval results, Prometheus-compatible metrics, optional local token protection, configurable CORS, and structured logging.

5. **Documentation-first workflow**  
   The repo includes docs, diary, status, logs, setup instructions, project rules, generated-file expectations, and security guidance to make work auditable and easier to continue.

6. **Quality, security, and automation practices**  
   CI, linting, type checking, smoke tests, dependency/security checks, GitHub code scanning, local-first security guidance, optional API token tests, CORS tests, and safe logging practices help keep the public workflow maintainable.

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
    logging.py
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
tests/test_api_cors.py
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
- configurable CORS settings
- structured logging settings
- reusable security helper
- reusable logging configuration module
- service-layer separation
- route modules
- app factory pattern through `create_app(settings)`
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
- CORS disabled by default
- explicit allowed origins when CORS is enabled
- safe startup logging for service mode and security posture
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

3. Optional: configure backend logging.

Logging is enabled with safe local defaults:

```env
LOG_LEVEL=INFO
LOG_FORMAT=plain
```

Supported `LOG_LEVEL` values follow standard Python logging levels, such as:

```text
DEBUG
INFO
WARNING
ERROR
```

Supported `LOG_FORMAT` values:

```text
plain
compact
```

Logging intentionally avoids:

```text
tokens
secrets
request bodies
authorization headers
memory-bank content
```

4. Start the FastAPI backend:

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

5. Optional: enable local API token protection for protected routes.

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

6. Optional: enable CORS for a trusted local dashboard or frontend.

CORS is disabled by default.

In `.env`:

```env
ENABLE_CORS=true
CORS_ALLOW_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

When CORS is enabled, only explicitly configured origins receive CORS headers.

Allowed methods are intentionally narrow:

```text
GET
POST
OPTIONS
```

Allowed headers are intentionally narrow:

```text
Authorization
Content-Type
```

Use this only for trusted local dashboards, documentation demos, or known frontends. Do not use wildcard origins for this project unless you intentionally change the security model.

7. Start the legacy/local MCP-style memory server if needed:

```bash
python scripts/run_mcp_server.py &
```

Cursor can fetch:

```text
http://localhost:7331/memory
```

8. Generate or update the rolling summary through the CLI:

```bash
python scripts/summarize_chat.py --chat-log path/to/chat.txt --max-lines 800
```

Manual mode:

```bash
cat path/to/chat.txt | python scripts/summarize_chat.py --stdin --manual
```

9. Build the retrieval index:

```bash
python scripts/retrieve_context.py rebuild
```

10. Export inspectable retrieval metadata JSON:

```bash
python scripts/retrieve_context.py export-meta-json
```

11. Query memory through the CLI retrieval workflow:

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
tests/test_api_cors.py
tests/test_cli_summarize_chat.py
```

The retrieval tests validate response shape, query validation, `top_k` validation, metadata fields, missing/empty index behavior, retrieval after index rebuild, JSON metadata export, and retrieval status readiness.

The summarization tests validate manual mode, fallback mode, active context writing through an isolated temporary path, disabled embedding behavior, response fields, and empty text validation.

The CLI compatibility tests validate file input, manual stdin mode, empty stdin handling, `--no-embed` behavior, isolated `activeContext.md` writing, and backward-compatible `call_openai_summarize()` availability.

The security tests validate default open local-first behavior, missing token rejection, wrong token rejection, correct Bearer token access, fail-closed misconfiguration handling, protected memory/retrieval/summarization/metrics routes, and public health route behavior.

The CORS tests validate that CORS headers are absent by default, allowed origins receive CORS headers when enabled, disallowed origins do not receive allow-origin headers, and configured preflight requests succeed.

Some backup and end-to-end tests require environment-specific configuration such as `GPG_KEY_ID` for encrypted backups. These are intentionally separated from the public smoke-test workflow and should be run in a configured integration environment.

---

## Environment Variables

The project reads the following variables. See `env.template`.

| Variable | Purpose |
|---|---|
| `OPENAI_API_KEY` | Enables automated summarization and embeddings via OpenAI API. Leaving it blank triggers fallback modes. |
| `OPENAI_API_KEY_FILE` | Optional path to a local file containing the OpenAI key when using file-based secret loading. |
| `ENABLE_LOCAL_API_TOKEN` | Enables optional Bearer token protection for protected local API routes when set to `true`. Defaults to `false`. |
| `LOCAL_API_TOKEN` | Token required in `Authorization: Bearer <LOCAL_API_TOKEN>` when local API token protection is enabled. |
| `ENABLE_CORS` | Enables CORS middleware when set to `true`. Defaults to `false`. |
| `CORS_ALLOW_ORIGINS` | Comma-separated list of trusted origins allowed when CORS is enabled, such as `http://localhost:3000,http://127.0.0.1:3000`. |
| `LOG_LEVEL` | Backend logging level. Defaults to `INFO`. Supports standard Python logging levels such as `DEBUG`, `INFO`, `WARNING`, and `ERROR`. |
| `LOG_FORMAT` | Backend logging format. Defaults to `plain`. Supports `plain` and `compact`. |
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
| `app/` | FastAPI backend package for health, memory access, retrieval, retrieval status, summarization, metadata-aware retrieval results, metrics, optional local token protection, configurable CORS, and structured logging |
| `cursor_setup_instructions/` | Canonical setup guide and Cursor workflow instructions |
| `docs/` | Architecture, backend design, generated-file guidance, security, deployment, and technical documentation |
| `memory-bank/` | Starter memory template for persistent context, active memory, and project knowledge |
| `scripts/` | Automation, summarization, retrieval, backups, logging, and status scripts |
| `tests/` | Unit, smoke, validation, security, CORS, CLI compatibility, and backend API tests |
| `status/` | Current status, checklists, and roadmap |
| `diary/` | Project diary and development log |
| `logs/solutions/` | Error logs, fixes, and implementation notes |
| `archive/` | Historical reference: archived workflows, docs, and deployment scaffolding |
| `.github/` | CI, Dependabot, and workflow automation |
| `Makefile` | Common developer commands |
| `PROJECT_RULES.md` | Project operating rules and development constraints |

---

## Technical Review Notes

This repository is designed as a public technical artifact for AI-assisted development workflows. It demonstrates system structure, retrieval logic, summarization workflow, documentation discipline, local automation, backend evolution, security boundaries, configurable CORS, structured logging, and CI/QA practices.

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
app/core/logging.py
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
tests/test_api_cors.py
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
- FastAPI backend slices for memory access, retrieval, retrieval status, summarization, health, metrics, optional local token protection, configurable CORS, and structured logging
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
- more advanced CORS policies by environment
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
- configurable CORS that remains disabled unless explicitly enabled
- structured logging with safe startup/configuration logs

The memory API exposes only allowed memory-bank markdown files and does not expose generated FAISS or pickle files as memory records.

The retrieval API validates query text and `top_k` bounds before calling the retrieval service.

The retrieval API returns source filename and chunk index fields to improve traceability and auditability of returned context.

The retrieval status API reports index, metadata, JSON export, and readiness state for operational inspection.

The summarization API validates text input, supports fallback behavior, and can disable embedding for safer test or controlled workflows.

The optional local API token protects memory, retrieval, summarization, and metrics routes when `ENABLE_LOCAL_API_TOKEN=true`, while keeping `GET /health` public for local readiness checks.

Configurable CORS remains disabled by default. When enabled, only explicitly trusted origins from `CORS_ALLOW_ORIGINS` receive CORS headers. The middleware is intentionally limited to `GET`, `POST`, and `OPTIONS` methods and the `Authorization` and `Content-Type` headers.

Backend logging is configured through `LOG_LEVEL` and `LOG_FORMAT`. Startup logs may report service name, runtime mode, token-protection status, CORS status, and configured-origin count. Logging intentionally avoids token values, request bodies, authorization headers, secrets, and memory-bank content.

---

## Deferred Maintenance Notes

Some GitHub Actions runs may show warnings that certain actions are running on Node.js 20 and may need future updates.

This is non-blocking because workflows are passing successfully and the methodology-applied release is complete.

Future maintenance may include reviewing stable action versions such as:

- actions/checkout@v4 → actions/checkout@v5
- actions/setup-python@v5 → actions/setup-python@v6

This can be handled in a future maintenance cycle if GitHub Actions warnings become noisy, if newer stable action versions are required, or if the repository enters another active development phase.

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
- explicit CORS controls for trusted frontends
- safe logging and operational visibility
- separation between local development, public CI, and production integration

---

## Status

This repository is maintained as a public showcase of AI-assisted development workflow architecture and tooling. Some private/client AI agent systems cannot be fully shared publicly due to confidentiality, so this repository serves as a shareable technical layer demonstrating development workflow, retrieval, summarization, documentation, backend structure, security boundaries, and QA practices.

The health/memory backend slice is implemented, tested, documented, and green. The retrieval API slice is implemented, tested, documented, and green. The retrieval metadata improvement is implemented, tested, documented, and green. The retrieval status endpoint is implemented, tested, documented, and green. The summarization API slice is implemented, tested, documented, and green. The summarization CLI compatibility slice is implemented, tested, documented, and green. The optional local API token protection slice is implemented, tested, documented, and green. The configurable CORS slice is implemented, tested, documented, and green. The structured logging slice is implemented, documented, and green.

The next meaningful engineering steps are backend logging documentation closure, retrieval evaluation tests, and additional local-first hardening around MCP/server exposure modes.

---

*Generated and maintained with AI-assisted development workflows using Cursor and human review.*

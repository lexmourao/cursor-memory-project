# Cursor Memory Project 📚🤖

![CI](https://github.com/lexmourao/cursor-memory-project/actions/workflows/ci.yml/badge.svg)

Maintenance note: This repository is a public demonstration of Cursor-based AI-assisted development workflows, persistent project memory, retrieval, MCP server structure, FastAPI backend structure, documentation, automated logging, testing, and QA practices.

Welcome to the **Cursor Memory Project**.

The objective of this repository is to provide a turn-key template that empowers the Cursor AI assistant and human collaborators with persistent project context, reproducible workflows, structured documentation, retrieval, local memory APIs, and auditable development practices.

---

## What This Demonstrates

This repository demonstrates my approach to AI-assisted systems development:

- Cursor-based AI-assisted development workflows
- Persistent project memory and rolling context for long-running AI projects
- Retrieval and context-loading patterns for LLM-assisted work
- Metadata-aware retrieval with source filename and chunk index traceability
- MCP server structure for exposing project memory to an AI coding environment
- Tested FastAPI backend slices for memory access, retrieval, health checks, and metrics
- Python automation for summarization, retrieval, logging, backups, and status updates
- CI practices using linting, type checking, dependency/security checks, and smoke tests
- GitHub code scanning / CodeQL through repository security configuration
- Documentation-first project structure for auditable and reproducible AI workflows
- Human-in-the-loop fallback modes when API keys or external services are unavailable
- Separation between public smoke tests and environment-specific integration tests

---

## Why This Matters for LLM & Agent Systems

LLM and agent-based systems depend heavily on context quality, memory structure, retrieval reliability, workflow documentation, traceability, and repeatable development practices.

This project explores how an AI-assisted development environment can maintain project memory across long-running work, expose structured context to an AI coding assistant, and support better continuity between human decisions, automated summaries, retrieval workflows, backend APIs, and implementation tasks.

The repository is not intended to represent a complete production SaaS platform. It is a public technical artifact showing how I structure AI-assisted development infrastructure, retrieval patterns, project memory, backend evolution, CI/QA practices, and documentation workflows that can support larger LLM and agent-based systems.

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
   The `app/` package exposes tested API endpoints for health, memory access, single memory-record retrieval, retrieval queries, metadata-aware retrieval results, and Prometheus-compatible metrics.

5. **Documentation-first workflow**  
   The repo includes docs, diary, status, logs, setup instructions, and project rules to make work auditable and easier to continue.

6. **Quality and automation practices**  
   CI, linting, type checking, smoke tests, dependency/security checks, and GitHub code scanning help keep the public workflow maintainable.

---

## Implemented Backend Slices

The FastAPI backend slices are implemented, tested, and green.

Implemented endpoints:

```text
GET /health
GET /memory
GET /memory/{record_id}
GET /metrics
POST /retrieval/query
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

Implemented API tests:

```text
tests/test_api_health.py
tests/test_api_memory.py
tests/test_api_retrieval.py
```

These backend slices demonstrate:

- FastAPI application structure
- typed Pydantic response models
- typed retrieval request/response models
- local-first configuration
- service-layer separation
- route modules
- memory-bank access through an API
- retrieval query access through an API
- metadata-aware retrieval responses
- missing-record 404 behavior
- request validation for retrieval queries
- Prometheus-compatible metrics
- tested backend behavior with FastAPI TestClient

The retrieval API returns traceable result fields:

```text
score
source
chunk_idx
text
```

This makes retrieval results easier to inspect, debug, audit, and eventually display in a dashboard.

The next backend slice may extract summarization into the backend service layer while preserving the existing CLI workflow:

```text
scripts/summarize_chat.py
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
If it is absent, scripts fall back to manual or zero-cost modes.

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

4. Start the legacy/local MCP-style memory server if needed:

```bash
python scripts/run_mcp_server.py &
```

Cursor can fetch:

```text
http://localhost:7331/memory
```

5. Generate or update the rolling summary:

```bash
python scripts/summarize_chat.py --chat-log path/to/chat.txt --max-lines 800
```

Manual mode:

```bash
cat path/to/chat.txt | python scripts/summarize_chat.py --stdin --manual
```

6. Build the retrieval index:

```bash
python scripts/retrieve_context.py rebuild
```

7. Query memory through the CLI retrieval workflow:

```bash
python scripts/retrieve_context.py query --text "What is the current project architecture?" --top-k 5
```

The CLI keeps the original simple output behavior, while the backend API exposes richer metadata for inspection and future UI/dashboard use.

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

Backend API tests include:

```text
tests/test_api_health.py
tests/test_api_memory.py
tests/test_api_retrieval.py
```

The retrieval tests validate response shape, query validation, `top_k` validation, and metadata fields when results are returned.

Some backup and end-to-end tests require environment-specific configuration such as `GPG_KEY_ID` for encrypted backups. These are intentionally separated from the public smoke-test workflow and should be run in a configured integration environment.

---

## Environment Variables

The project reads the following variables. See `env.template`.

| Variable | Purpose |
|---|---|
| `OPENAI_API_KEY` | Enables automated summarization and embeddings via OpenAI API. Leaving it blank triggers fallback modes. |
| `OPENAI_API_KEY_FILE` | Path inside container to a file containing the key when using Docker secrets. |
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
| `app/` | FastAPI backend package for health, memory access, retrieval, metadata-aware retrieval results, metrics, and future APIs |
| `cursor_setup_instructions/` | Canonical setup guide and Cursor workflow instructions |
| `docs/` | Architecture, backend design, security, deployment, and technical documentation |
| `memory-bank/` | Starter memory template for persistent context, active memory, and project knowledge |
| `scripts/` | Automation, summarization, retrieval, backups, logging, and status scripts |
| `tests/` | Unit, smoke, validation, and backend API tests |
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

This repository is designed as a public technical artifact for AI-assisted development workflows. It demonstrates system structure, retrieval logic, documentation discipline, local automation, backend evolution, and CI/QA practices.

Recommended reviewer path:

```text
README.md
memory-bank/README.md
docs/ARCHITECTURE.md
docs/BACKEND_DESIGN.md
docs/DEMO_WORKFLOW.md
docs/TECHNICAL_REVIEW.md
app/main.py
app/services/memory_service.py
app/services/retrieval_service.py
app/api/routes_health.py
app/api/routes_memory.py
app/api/routes_retrieval.py
app/models/retrieval.py
tests/test_api_health.py
tests/test_api_memory.py
tests/test_api_retrieval.py
scripts/retrieve_context.py
scripts/summarize_chat.py
.github/workflows/ci.yml
status/roadmap.md
```

Current scope:

- Local-first memory and retrieval workflow
- Cursor-oriented AI-assisted development setup
- MCP server structure for exposing memory context
- FastAPI backend slices for memory access, retrieval, health, and metrics
- Metadata-aware retrieval with source file and chunk index traceability
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
- Summarization API endpoint

---

## Production Evolution Roadmap

A production version of this architecture could evolve toward:

- summarization API endpoint
- managed vector database integration such as Qdrant, Pinecone, or PgVector
- authenticated API layer for memory access
- user/project isolation
- scheduled summarization jobs
- retrieval evaluation tests
- structured observability and logging
- agent workflow monitoring
- deployment via cloud infrastructure
- frontend dashboard for memory, logs, retrieval chunks, and retrieval metadata inspection
- stronger integration tests with configured secrets and encrypted backup workflows

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

The memory API exposes only allowed memory-bank markdown files and does not expose generated FAISS or pickle files as memory records.

The retrieval API validates query text and `top_k` bounds before calling the retrieval service.

The retrieval API returns source filename and chunk index fields to improve traceability and auditability of returned context.

---

## Pending Non-Blocking Cleanup

Some GitHub Actions runs may show a warning that certain actions are running on Node.js 20 and may need future updates.

This is non-blocking because workflows are passing successfully.

Future cleanup may include reviewing stable action versions such as:

```text
actions/checkout@v4 → actions/checkout@v5
actions/setup-python@v5 → actions/setup-python@v6
```

This should be done later, after the backend documentation and first backend slices are stable.

---

## Relationship to AI Agents and LLM Systems

This project is not only about storing notes. It is a context-engineering and workflow-infrastructure pattern for AI-assisted work.

The same principles can support broader LLM and agent systems:

- persistent memory
- retrieval-augmented context
- local memory APIs
- typed retrieval API
- metadata-aware context traceability
- tool-access patterns
- human-in-the-loop fallbacks
- system documentation
- workflow traceability
- separation between local development, public CI, and production integration

---

## Status

This repository is maintained as a public showcase of AI-assisted development workflow architecture and tooling. Some private/client AI agent systems cannot be fully shared publicly due to confidentiality, so this repository serves as a shareable technical layer demonstrating development workflow, retrieval, documentation, backend structure, and QA practices.

The health/memory backend slice is implemented, tested, documented, and green. The retrieval API slice is implemented, tested, documented, and green. The retrieval metadata improvement is implemented, tested, documented, and green.

The next meaningful engineering step is the summarization service slice.

---

*Generated and maintained with AI-assisted development workflows using Cursor and human review.*

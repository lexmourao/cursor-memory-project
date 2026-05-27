# System Architecture – Cursor Memory Project

> **Scope:** Defines the technical architecture for implementing continuous context engineering, persistent project memory, retrieval, MCP-oriented context delivery, automation, and QA practices in this repository.

---

## 1. Purpose

The Cursor Memory Project is a local-first AI-assisted development framework designed to help long-running projects preserve context across sessions.

The system gives Cursor and human collaborators a structured way to maintain:

- persistent project memory
- rolling active context
- retrieval-based context loading
- repeatable summarization workflows
- audit-friendly logs and status tracking
- local automation scripts
- public CI, type checking, linting, and security checks

The project is not intended to be a complete production SaaS platform. It is a public technical artifact showing how AI-assisted development infrastructure can be structured, documented, tested, and evolved toward larger LLM and agent-based systems.

---

## 2. System Boundaries

### In Scope

This repository covers:

- local project memory stored in markdown files
- active context summarization
- FAISS-based retrieval index generation
- MCP server structure for exposing context to Cursor
- Python automation scripts for logging, status updates, retrieval, summarization, and backups
- local-first developer workflows
- CI smoke tests, linting, type checking, dependency/security checks, and CodeQL
- documentation-first project governance

### Out of Scope

This public version does not include:

- multi-tenant authentication
- hosted SaaS deployment
- frontend dashboard
- enterprise observability stack
- managed production vector database
- role-based access control
- production permission model
- large-scale user/project isolation
- cloud-hosted background jobs
- full production incident-response automation

These are intentionally documented as production-evolution paths rather than represented as completed capabilities.

---

## 3. High-Level Component Diagram

```mermaid
graph TD
    subgraph IDE
        C[Cursor IDE]
    end

    subgraph MemorySystem
        MB[Memory-Bank Markdown Files]
        AC[activeContext.md]
        Embed[Embedding & Vector DB]
        Sum[Summarization Engine]
        Ret[Retrieval Engine]
    end

    subgraph Automation
        Log[log_action.py]
        Stat[update_status.py]
        Backup[backup_data.sh]
        Sched[Cron / Git hooks / Manual CLI]
    end

    subgraph Integration
        MCP[MCP Server]
    end

    subgraph Quality
        CI[GitHub Actions CI]
        Ruff[Ruff]
        Mypy[Mypy]
        Audit[pip-audit]
        CodeQL[CodeQL]
        Tests[Smoke Tests]
    end

    C -->|reads context| MCP
    MCP -->|loads| MB

    C -->|recent chat/session log| Sum
    Sum -->|writes rolling context| AC
    AC -->|embedded into| Embed

    C -->|needs relevant context| Ret
    Ret -->|queries| Embed
    Ret -->|returns top-K context| C

    Log -->|append events| MB
    Stat -->|update checklists/status| MB
    Backup -->|archive memory/logs/status| MB
    Sched --> Log
    Sched --> Stat
    Sched --> Backup

    CI --> Ruff
    CI --> Mypy
    CI --> Audit
    CI --> Tests
    CodeQL -->|security analysis| CI
```

### Legend

- **Cursor IDE:** User-facing AI-assisted development environment.
- **MCP Server:** Local server pattern that exposes memory-bank content as structured context.
- **Memory-Bank:** Persistent markdown-based project memory.
- **activeContext.md:** Rolling summary of recent context and decisions.
- **Summarization Engine:** Converts recent chat or session logs into updated project memory.
- **Embedding & Vector DB:** Local FAISS-based retrieval index.
- **Retrieval Engine:** Fetches relevant memory chunks for new prompts or tasks.
- **Automation Scripts:** Maintain logs, status, backups, and project continuity.
- **CI/QA Layer:** Runs linting, type checking, dependency/security checks, smoke tests, and CodeQL.

---

## 4. Data Flow

### 4.1 Startup Flow

1. The developer opens the repository in Cursor.
2. `.cursor-rules.md` defines how Cursor should interact with project memory.
3. The MCP server can be started locally.
4. The MCP server reads memory-bank files and exposes structured context.
5. Cursor can retrieve project context before the first major interaction.

### 4.2 Summarization Flow

1. A session log or chat history is provided to `scripts/summarize_chat.py`.
2. If `OPENAI_API_KEY` is available, the script can use OpenAI for summarization.
3. If no API key is available, the script falls back to manual or zero-cost summarization modes.
4. The generated summary is written to `memory-bank/activeContext.md`.
5. The summary can be embedded and added to the retrieval index.

### 4.3 Retrieval Flow

1. A new user prompt or task requires context.
2. `scripts/retrieve_context.py` embeds the query text.
3. The FAISS index is searched for relevant memory chunks.
4. Top-K chunks are returned as context.
5. The developer or AI assistant uses the retrieved context to continue work with less information loss.

### 4.4 Logging and Status Flow

1. `scripts/log_action.py` records major events, implementation notes, and errors.
2. `scripts/update_status.py` refreshes checklists, status files, and roadmap-style documentation.
3. Logs and status updates help maintain continuity across sessions.

### 4.5 Backup Flow

1. `scripts/backup_data.sh` archives memory, logs, and status directories.
2. Encrypted backup flows require `GPG_KEY_ID`.
3. Because GPG configuration is environment-specific, backup integration tests are separated from public CI smoke tests.

---

## 5. Runtime Modes

### 5.1 Local Development Mode

Used when a developer runs the system locally with optional API keys.

Capabilities:

- summarize logs
- build retrieval index
- start MCP server
- query memory
- run local tests
- run manual backups if GPG is configured

### 5.2 Zero-Cost / Manual Mode

Used when no OpenAI API key is available.

Capabilities:

- fallback summarization
- manual context updates
- local memory-bank usage
- documentation and logging workflows
- smoke testing without external API dependencies

### 5.3 Public CI Mode

Used by GitHub Actions for public repository validation.

Capabilities:

- linting with `ruff`
- type checking with `mypy`
- dependency/security checks with `pip-audit`
- focused smoke tests
- CodeQL security checks

Public CI intentionally avoids secret-dependent backup and E2E flows.

### 5.4 Configured Integration Mode

Used when required secrets and environment variables are configured.

Capabilities:

- encrypted backup tests
- full E2E backup/restore workflows
- external API-backed summarization
- deeper integration testing

---

## 6. Directory Structure

```text
cursor-memory-project/
  ├── .github/                       # CI, CodeQL, Dependabot, workflows
  ├── cursor_setup_instructions/     # Canonical setup guide
  ├── diary/                         # Project diary and development log
  ├── docs/                          # Architecture, security, deployment docs
  ├── logs/solutions/                # Error logs and implementation notes
  ├── memory-bank/                   # Persistent project memory
  ├── nginx/                         # Server/web configuration examples
  ├── scripts/                       # Automation, retrieval, summarization, backup scripts
  ├── status/                        # Roadmap, checklists, project status
  ├── tests/                         # Unit, smoke, and validation tests
  ├── Dockerfile                     # Container setup
  ├── docker-compose.yml             # Local orchestration setup
  ├── Makefile                       # Developer commands
  ├── PROJECT_RULES.md               # Operating rules
  └── README.md                      # Public project overview
```

---

## 7. Memory-Bank Structure

```text
memory-bank/
  ├── projectbrief.md         # Why the project exists
  ├── productContext.md       # User goals and pain points
  ├── activeContext.md        # Rolling summary, generated or updated
  ├── systemPatterns.md       # Architecture and design patterns
  ├── techContext.md          # Tech stack and constraints
  └── progress.md             # Current status, blockers, and next steps
```

The memory-bank is intentionally markdown-based to keep the system:

- inspectable
- portable
- versionable
- easy for humans and AI tools to read
- compatible with Git-based workflows

---

## 8. Technology Choices

| Layer | Current Choice | Rationale |
|---|---|---|
| AI-assisted IDE | Cursor | Native AI coding workflow and project context support |
| Memory format | Markdown | Human-readable, versionable, easy to parse |
| Summarization | OpenAI or fallback/manual mode | Supports both automated and zero-cost workflows |
| Embeddings | OpenAI embedding model when configured | Lightweight retrieval workflow |
| Vector store | FAISS | Local-first, fast, no external server required |
| MCP/context exposure | Local MCP server structure | Allows memory to be exposed to AI coding environment |
| Automation | Python and shell scripts | Simple, inspectable, portable |
| CI | GitHub Actions | Public validation of repo health |
| Linting | Ruff | Fast Python linting |
| Type checking | Mypy | Static type confidence |
| Dependency/security checks | pip-audit | Dependency vulnerability detection |
| Security analysis | CodeQL | GitHub-native code scanning |
| Containers | Docker / docker-compose | Local reproducibility and deployment evolution path |

---

## 9. Testing Strategy

### 9.1 Local Test Suite

Developers can run:

```bash
pytest -q
```

This may include tests that depend on local configuration, such as encrypted backup behavior.

### 9.2 Public CI Smoke Tests

The public CI workflow validates the repository without requiring private secrets.

It runs:

- `ruff check .`
- `mypy scripts tests`
- `pip-audit --strict`
- focused smoke tests

This keeps the public workflow useful, reviewable, and green without pretending that secret-dependent integration flows can run in an unconfigured environment.

### 9.3 Integration Tests

Backup and end-to-end tests require environment-specific configuration, including:

- `GPG_KEY_ID`
- backup directories
- local encryption setup
- optional external API keys

These should run in a configured integration environment, not in the public smoke-test workflow.

---

## 10. Failure Modes and Recovery

| Failure Mode | Cause | Recovery |
|---|---|---|
| Missing `OPENAI_API_KEY` | API key not configured | Use fallback/manual summarization mode |
| Empty FAISS index | Retrieval index not built | Run `python scripts/retrieve_context.py rebuild` |
| Missing `GPG_KEY_ID` | Encrypted backup key not configured | Configure key or skip backup integration tests |
| Stale memory context | activeContext not updated | Re-run summarization workflow |
| CI import error | Python path/package issue | Ensure package imports and `PYTHONPATH` are configured |
| Type mismatch in FAISS helpers | FAISS returns generic index type | Use broader `faiss.Index` annotation |
| Failed dependency audit | Vulnerable dependency | Upgrade or pin dependency |
| MCP server unavailable | Server not running | Start `python scripts/run_mcp_server.py` |
| External API unavailable | Network/API/service issue | Use fallback/manual mode |

---

## 11. Security and Reliability Considerations

### Secrets

- Secrets should not be committed to the repository.
- API keys are loaded through environment variables or file-based secret paths.
- Backup encryption uses `GPG_KEY_ID` or `GPG_KEY_ID_FILE`.

### Localhost Binding

The MCP server should bind to `localhost` by default. Remote exposure requires additional authentication, firewall, and access-control review.

### Backups

Backup workflows should be encrypted when sensitive project memory is included. Public CI does not execute secret-dependent backup flows.

### Public CI

The public workflow is intentionally limited to checks that do not require secrets. This prevents leaking sensitive configuration while still showing repository quality.

### Dependency and Code Scanning

The repository uses:

- `pip-audit` for dependency checks
- CodeQL for code scanning
- branch protection for safer repository maintenance
- focused smoke tests for public workflow validation

---

## 12. Architecture Tradeoffs

### Markdown Memory vs Database

**Decision:** Use markdown files for the public/local-first version.

**Why:** Markdown is inspectable, easy to version, AI-readable, and simple to maintain.

**Tradeoff:** It is not ideal for multi-tenant production systems, complex permissions, or high-volume writes.

### FAISS vs Managed Vector Database

**Decision:** Use FAISS locally.

**Why:** FAISS is simple, fast, offline, and does not require external infrastructure.

**Tradeoff:** Production systems may require Qdrant, Pinecone, PgVector, or another managed retrieval layer.

### Public Smoke Tests vs Full Integration Tests

**Decision:** Public CI runs smoke tests, while secret-dependent backup/E2E tests are reserved for configured environments.

**Why:** Public CI cannot safely run encrypted backup tests without secrets.

**Tradeoff:** Full integration validation requires a separate configured workflow.

### Local MCP Structure vs Hosted Agent Service

**Decision:** Use local MCP server structure.

**Why:** It is appropriate for Cursor-based AI-assisted development and local project memory.

**Tradeoff:** A hosted agent memory service would require authentication, authorization, observability, scaling, and user isolation.

---

## 13. Production Evolution Path

A production-grade version of this architecture could evolve into:

1. **API Layer**
   - FastAPI or similar framework
   - authenticated memory access
   - query endpoints
   - project/user-scoped retrieval

2. **Managed Retrieval Layer**
   - Qdrant, Pinecone, PgVector, or managed FAISS service
   - chunk metadata
   - retrieval evaluation
   - hybrid search

3. **User and Project Isolation**
   - tenant-aware memory
   - permissioned context access
   - workspace-level boundaries

4. **Observability**
   - structured logs
   - tracing
   - latency metrics
   - retrieval quality metrics
   - agent/tool-call monitoring

5. **Job Scheduling**
   - scheduled summarization
   - background indexing
   - backup/restore automation
   - data retention policies

6. **Security Hardening**
   - auth layer
   - secrets manager
   - access control
   - encrypted storage
   - audit logs

7. **Frontend / Review Dashboard**
   - inspect memory-bank files
   - review retrieved chunks
   - approve summaries
   - audit context changes
   - monitor system health

---

## 14. Non-Goals

This repository does not claim to be:

- a complete enterprise agent platform
- a hosted production SaaS
- a multi-user permissioned knowledge system
- a replacement for managed vector databases
- a replacement for formal production observability
- a fully autonomous agent system

Its purpose is to demonstrate how AI-assisted development workflows can be structured with persistent memory, retrieval, MCP-oriented context delivery, automation, documentation, and quality practices.

---

## 15. Open Questions / Next Design Tasks

1. Define exact summarization cadence: fixed number of turns, token threshold, or event-based trigger.
2. Add retrieval evaluation tests.
3. Decide whether FAISS index should be committed, generated on demand, or stored externally.
4. Define metadata schema for chunks.
5. Add a configured integration workflow for encrypted backups.
6. Add local observability examples.
7. Add production API proof of concept.
8. Add workspace/project-level isolation strategy.
9. Define memory retention and pruning policy.
10. Add documentation for MCP server extension points.

---

## 16. Reviewer Summary

This architecture demonstrates a local-first, AI-assisted development memory system with:

- persistent context
- retrieval-based memory access
- MCP-oriented context delivery
- summarization and fallback modes
- Python automation
- documentation-first project governance
- CI, type checking, linting, dependency auditing, and CodeQL
- clear separation between public smoke tests and configured integration tests
- documented production evolution path

The project is intentionally scoped as a public technical artifact, but the architecture shows how the same design principles can evolve into production-grade LLM and agent infrastructure.

---

*Last updated: 2026-05-27*

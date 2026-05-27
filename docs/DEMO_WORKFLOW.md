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
- MCP server structure for exposing memory to Cursor
- Python automation for summarization, retrieval, logging, backups, and status updates
- fallback behavior when external API keys are unavailable
- public CI with linting, type checking, dependency/security checks, and smoke tests
- CodeQL security analysis
- documentation-first engineering practices
- separation between public smoke tests and environment-specific integration workflows

This demo is not intended to prove a complete production SaaS product. It is intended to show the technical workflow layer behind AI-assisted development systems and the way this repository can serve as a reusable setup method before a real project begins.

---

## 2. Reviewer Quick Path

A reviewer can inspect the repository in this order:

1. `README.md`  
   Public overview, system purpose, memory-bank template mode, scope, CI strategy, and production evolution path.

2. `memory-bank/README.md`  
   Explains why memory-bank files start mostly empty and how they should be populated after real project kickoff.

3. `docs/ARCHITECTURE.md`  
   System architecture, data flow, runtime modes, failure modes, tradeoffs, and production roadmap.

4. `docs/adr/0001-public-ci-vs-integration-tests.md`  
   Architecture Decision Record explaining public CI vs secret-dependent integration tests.

5. `.cursor-rules.md`  
   Operational rules for how Cursor should use memory, logs, project rules, and context.

6. `scripts/summarize_chat.py`  
   Summarization workflow for converting recent session logs into active project context.

7. `scripts/retrieve_context.py`  
   Retrieval workflow for building and querying the memory index.

8. `scripts/run_mcp_server.py`  
   Local server structure for exposing project memory.

9. `.github/workflows/ci.yml`  
   Public CI workflow.

10. `status/roadmap.md`  
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

### Step 2 — Generate or update active context

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

### Step 3 — Build the retrieval index

Run:

```bash
python scripts/retrieve_context.py rebuild
```

Expected result:

- memory-bank content is processed
- embeddings are generated or fallback vectors are used
- retrieval index files are created or updated
- generated retrieval files remain excluded from version control

---

### Step 4 — Query memory

Run:

```bash
python scripts/retrieve_context.py query --text "What is the current project architecture?" --top-k 5
```

Expected result:

- the retrieval engine returns relevant memory chunks
- the assistant can use retrieved context to continue work with less information loss

---

### Step 5 — Start the local memory server

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

---

### Step 6 — Inspect operational status

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

This demonstrates:

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

### Retrieval workflow

Inspect:

```text
scripts/retrieve_context.py
```

This file demonstrates FAISS-based retrieval logic, embedding fallback behavior, memory index rebuilds, chunk metadata, and query operations.

### Summarization workflow

Inspect:

```text
scripts/summarize_chat.py
```

This file demonstrates how session logs can be transformed into rolling active context.

### MCP/context delivery

Inspect:

```text
scripts/run_mcp_server.py
```

This file demonstrates the local context-serving layer.

### CI and QA workflow

Inspect:

```text
.github/workflows/ci.yml
.github/workflows/codeql.yml
```

These files demonstrate public quality and security checks.

### Operational documentation

Inspect:

```text
status/release_checklist.md
status/roadmap.md
docs/DEMO_WORKFLOW.md
docs/adr/0001-public-ci-vs-integration-tests.md
```

These files show how the repository documents decisions, release assumptions, and future backend evolution.

---

## 7. Expected Reviewer Interpretation

This repository is best understood as a public technical artifact for AI-assisted development infrastructure.

It demonstrates:

- system design thinking
- context engineering
- retrieval workflow design
- local automation
- CI and QA discipline
- documentation maturity
- production-evolution awareness
- clear separation between public smoke tests and configured integration tests
- practical Python automation for LLM-assisted development workflows

It should not be interpreted as a complete production SaaS application. Instead, it shows the workflow and infrastructure patterns that can support larger LLM and agent-based systems.

---

## 8. Current Scope vs Future Backend Evolution

### Current Scope

- local-first memory-bank setup
- markdown-based project memory
- summarization workflow
- retrieval workflow
- MCP-oriented local memory server
- public CI and CodeQL
- Docker/Nginx starter configuration
- documentation and status checklists

### Future Backend Evolution

A stronger backend-oriented version of this workflow could add:

- typed FastAPI application structure under `app/`
- request/response models for memory and retrieval endpoints
- service layer for memory, retrieval, summarization, and status
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

## 9. Summary

The demo shows how to structure an AI-assisted development environment that can preserve memory, retrieve context, support human review, maintain documentation, and keep public quality checks green.

The main technical value is not a single script. The value is the architecture of the workflow: persistent memory, retrieval, MCP-oriented context delivery, automation, CI/QA, documentation, and production-aware engineering decisions.

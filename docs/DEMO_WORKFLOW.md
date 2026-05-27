# Demo Workflow – Cursor Memory Project

> This document explains how a technical reviewer can evaluate the Cursor Memory Project as a public demonstration of AI-assisted development workflow infrastructure, persistent memory, retrieval, MCP-oriented context delivery, and CI/QA practices.

---

## 1. What This Demo Proves

This repository demonstrates how an AI-assisted development workflow can preserve project context across long-running work.

It shows:

- persistent project memory using markdown files
- rolling active context summarization
- retrieval-based context loading
- MCP server structure for exposing memory to Cursor
- Python automation for summarization, retrieval, logging, backups, and status updates
- fallback behavior when external API keys are unavailable
- public CI with linting, type checking, dependency/security checks, and smoke tests
- documentation-first engineering practices

This demo is not intended to prove a complete production SaaS product. It is intended to show the technical workflow layer behind AI-assisted development systems.

---

## 2. Reviewer Quick Path

A reviewer can inspect the repository in this order:

1. `README.md`  
   Public overview, system purpose, scope, CI strategy, and production evolution path.

2. `docs/ARCHITECTURE.md`  
   System architecture, data flow, runtime modes, failure modes, tradeoffs, and production roadmap.

3. `docs/adr/0001-public-ci-vs-integration-tests.md`  
   Architecture Decision Record explaining public CI vs secret-dependent integration tests.

4. `scripts/summarize_chat.py`  
   Summarization workflow for converting recent session logs into active project context.

5. `scripts/retrieve_context.py`  
   Retrieval workflow for building and querying the memory index.

6. `scripts/run_mcp_server.py`  
   Local server structure for exposing project memory.

7. `.github/workflows/ci.yml`  
   Public CI workflow.

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

### Step 1 — Prepare project memory

Inspect the memory-bank folder:

```bash
ls memory-bank
```

The memory-bank stores project context, active memory, system patterns, technical notes, and progress.

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

is created or updated.

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

---

### Step 4 — Query memory

Run:

```bash
echo "What is the current project architecture?" | python scripts/retrieve_context.py query --top-k 5
```

Expected result:

- the retrieval engine returns relevant memory chunks
- the assistant can use retrieved context to continue work with less information loss

---

### Step 5 — Start MCP server

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
docs/ARCHITECTURE.md
```

These files show how project memory, documentation, and AI-assisted development rules are structured.

### Retrieval workflow

Inspect:

```text
scripts/retrieve_context.py
```

This file demonstrates FAISS-based retrieval logic, embedding fallback behavior, and memory index operations.

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
```

This file demonstrates public quality checks.

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

It should not be interpreted as a complete production SaaS application. Instead, it shows the workflow and infrastructure patterns that can support larger LLM and agent-based systems.

---

## 8. Production Evolution

A production-grade version of this workflow could add:

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

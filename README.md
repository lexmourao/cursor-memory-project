# Cursor Memory Project 📚🤖

![CI](https://github.com/lexmourao/cursor-memory-project/actions/workflows/ci.yml/badge.svg)
![CodeQL](https://github.com/lexmourao/cursor-memory-project/actions/workflows/codeql.yml/badge.svg)

Maintenance note: This repository is a public demonstration of Cursor-based AI-assisted development workflows, persistent project memory, retrieval, MCP server structure, documentation, automated logging, testing, and QA practices.

Welcome to the **Cursor Memory Project**.

The objective of this repository is to provide a turn-key template that empowers the Cursor AI assistant and human collaborators with persistent project context, reproducible workflows, structured documentation, retrieval, and auditable development practices.

## What This Demonstrates

This repository demonstrates my approach to AI-assisted systems development:

- Cursor-based AI-assisted development workflows
- Persistent project memory and rolling context for long-running AI projects
- Retrieval and context-loading patterns for LLM-assisted work
- MCP server structure for exposing project memory to an AI coding environment
- Python automation for summarization, retrieval, logging, backups, and status updates
- CI practices using linting, type checking, dependency/security checks, and smoke tests
- Documentation-first project structure for auditable and reproducible AI workflows
- Human-in-the-loop fallback modes when API keys or external services are unavailable
- Separation between public smoke tests and environment-specific integration tests

## Why This Matters for LLM & Agent Systems

LLM and agent-based systems depend heavily on context quality, memory structure, retrieval reliability, workflow documentation, and repeatable development practices.

This project explores how an AI-assisted development environment can maintain project memory across long-running work, expose structured context to an AI coding assistant, and support better continuity between human decisions, automated summaries, retrieval workflows, and implementation tasks.

The repository is not intended to represent a complete production SaaS platform. It is a public technical artifact showing how I structure AI-assisted development infrastructure, retrieval patterns, project memory, CI/QA practices, and documentation workflows that can support larger LLM and agent-based systems.

## Core System Concepts

The system is organized around five core ideas:

1. **Persistent project memory**  
   A structured `memory-bank` stores active context, summaries, and project knowledge that can be reused across sessions.

2. **Retrieval and context loading**  
   Scripts support embedding and retrieval workflows so relevant project context can be rebuilt, searched, and exposed to the assistant.

3. **MCP server structure**  
   A local MCP-oriented server pattern exposes project memory to Cursor or other AI-assisted development environments.

4. **Documentation-first workflow**  
   The repo includes docs, diary, status, logs, setup instructions, and project rules to make work auditable and easier to continue.

5. **Quality and automation practices**  
   CI, linting, type checking, smoke tests, dependency/security checks, and CodeQL help keep the public workflow maintainable.

## Quickstart — Full Memory System

These steps get the summarization, retrieval, and MCP server working locally. Cursor can automatically load memory via `.cursor-rules.md`.

1. Clone the repo and install dependencies:

```bash
pip install -r requirements.txt
```

2. Copy the environment template and optionally add your OpenAI key:

```bash
cp .env.example .env
```

If `OPENAI_API_KEY` is present, automated summaries and embeddings can use OpenAI.  
If it is absent, scripts fall back to manual or zero-cost modes.

3. Start the MCP server:

```bash
python scripts/run_mcp_server.py &
```

4. Generate or update the rolling summary:

```bash
python scripts/summarize_chat.py --chat-log path/to/chat.txt --max-lines 800
```

Manual mode:

```bash
cat path/to/chat.txt | python scripts/summarize_chat.py --stdin --manual
```

5. Build the retrieval index:

```bash
python scripts/retrieve_context.py rebuild
```

6. Launch Cursor in the repo. On first chat turn, it can fetch:

```text
http://localhost:7331/memory
```

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

Some backup and end-to-end tests require environment-specific configuration such as `GPG_KEY_ID` for encrypted backups. These are intentionally separated from the public smoke-test workflow and should be run in a configured integration environment.

## Environment Variables

The project reads the following variables. See `.env.example` or `env.template`.

| Variable | Purpose |
|---|---|
| `OPENAI_API_KEY` | Enables automated summarization and embeddings via OpenAI API. Leaving it blank triggers fallback modes. |
| `OPENAI_API_KEY_FILE` | Path inside container to a file containing the key when using Docker secrets. |
| `GPG_KEY_ID` | Required for encrypted backup workflows. |
| `GPG_KEY_ID_FILE` | Path to a file containing the recipient key ID for encrypted backups. |

Load them with:

```bash
source .env
```

or your preferred shell mechanism.

## High-Level Folder Overview

| Path | Purpose |
|---|---|
| `cursor_setup_instructions/` | Canonical setup guide and Cursor workflow instructions |
| `docs/` | Architecture, security, deployment, and technical documentation |
| `memory-bank/` | Persistent context, active memory, and project knowledge |
| `scripts/` | Automation, summarization, retrieval, backups, logging, and status scripts |
| `tests/` | Unit, smoke, and validation tests |
| `status/` | Current status, checklists, and roadmap |
| `diary/` | Project diary and development log |
| `logs/solutions/` | Error logs, fixes, and implementation notes |
| `nginx/` | Web/server configuration examples |
| `.github/` | CI, CodeQL, Dependabot, and workflow automation |
| `Dockerfile` | Container setup |
| `docker-compose.yml` | Local orchestration setup |
| `Makefile` | Common developer commands |
| `PROJECT_RULES.md` | Project operating rules and development constraints |

## Technical Review Notes

This repository is designed as a public technical artifact for AI-assisted development workflows. It demonstrates system structure, retrieval logic, documentation discipline, local automation, and CI/QA practices.

Current scope:

- Local-first memory and retrieval workflow
- Cursor-oriented AI-assisted development setup
- MCP server structure for exposing memory context
- Python automation scripts
- Public CI smoke tests
- Documentation and audit-oriented folder structure

Not yet included in this public version:

- Multi-tenant production authentication
- Hosted deployment
- Enterprise observability stack
- Full database migration layer
- External managed vector database
- Production-grade user permissions
- Hosted UI or SaaS frontend

## Production Evolution Roadmap

A production version of this architecture could evolve toward:

- managed vector database integration such as Qdrant, Pinecone, or PgVector
- authenticated API layer for memory access
- user/project isolation
- scheduled summarization jobs
- retrieval evaluation tests
- structured observability and logging
- agent workflow monitoring
- deployment via cloud infrastructure
- frontend dashboard for memory, logs, and retrieval inspection
- stronger integration tests with configured secrets and encrypted backup workflows

## Security and Reliability Considerations

This repository uses environment variables and file-based secrets patterns to avoid hardcoding sensitive credentials. Public CI avoids requiring private secrets for smoke-test execution.

The repo includes security and quality practices such as:

- CodeQL checks
- dependency/security auditing with `pip-audit`
- type checking with `mypy`
- linting with `ruff`
- branch protection
- documented fallback behavior when external APIs are unavailable

## Relationship to AI Agents and LLM Systems

This project is not only about storing notes. It is a context-engineering and workflow-infrastructure pattern for AI-assisted work.

The same principles can support broader LLM and agent systems:

- persistent memory
- retrieval-augmented context
- tool-access patterns
- human-in-the-loop fallbacks
- system documentation
- workflow traceability
- separation between local development, public CI, and production integration

## Status

This repository is maintained as a public showcase of AI-assisted development workflow architecture and tooling. Some private/client AI agent systems cannot be fully shared publicly due to confidentiality, so this repository serves as a shareable technical layer demonstrating development workflow, retrieval, documentation, and QA practices.

---

*Generated and maintained with AI-assisted development workflows using Cursor and human review.*

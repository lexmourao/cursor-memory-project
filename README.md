# Cursor Memory Project 📚🤖

Welcome to the **Cursor Memory Project**.

The objective of this repository is to provide a turn-key template that empowers the Cursor AI assistant (and all human collaborators) with:

1. Persistent project memory & rolling context
2. Clear, opinionated folder & documentation structure
3. Automated logging, status tracking, and backups
4. Reproducible, auditable research workflows that can be reused across disciplines

The canonical setup guide lives in `cursor_setup_instructions/README_CURSOR_SETUP.md`.  Most of the content in this repository is derived from that document.

---

## Quickstart (Full Memory System)

> These steps get the summarization, retrieval, and MCP server working locally.  Cursor will automatically load the memory via `.cursor-rules.md`.

1. Clone the repo and install deps
   ```bash
   pip install -r requirements.txt
   ```
2. Copy the environment template and (optionally) add your OpenAI key
   ```bash
   cp .env.example .env       # then edit .env to add OPENAI_API_KEY
   ```
   • If `OPENAI_API_KEY` is **present** → automated summaries & embeddings use OpenAI.  
   • If **absent** → scripts will fall back to manual / zero-cost modes.
3. Start the MCP server (serves the memory-bank to Cursor)
   ```bash
   python scripts/run_mcp_server.py &
   ```
4. Generate or update the rolling summary
   • Automated (requires key):
     ```bash
     python scripts/summarize_chat.py --chat-log path/to/chat.txt --max-lines 800
     ```
   • Manual (no key):
     ```bash
     cat path/to/chat.txt | python scripts/summarize_chat.py --stdin --manual
     ```
5. Build the retrieval index
   ```bash
   python scripts/retrieve_context.py rebuild
   ```
6. Launch Cursor in the repo.  On first chat turn, it will fetch `http://localhost:7331/memory` and gain full context.

---

## Running Tests
```bash
pytest -q
```
CI runs these tests on every push/PR to `main`.

---

## Environment Variables
The project reads the following variables (see `.env.example`):

| Variable | Purpose |
|----------|---------|
| `OPENAI_API_KEY` | Enables automated summarization & embeddings via OpenAI API. Leaving it blank triggers fallback modes. |
| `OPENAI_API_KEY_FILE` | Path (inside container) to file containing the key when using Docker secrets. |
| `GPG_KEY_ID` | Mandatory for backups; backup script encrypts archives with this recipient. |
| `GPG_KEY_ID_FILE` | Path to file containing recipient key ID for encrypted backups. |

Load them with `source .env` or your preferred shell mechanism.

---

## High-level folder overview

| Path | Purpose |
|------|---------|
| `data/raw/` | Immutable source data |
| `data/processed/` | Cleaned / transformed data outputs |
| `docs/` | Architecture, security, deployment, and other documentation |
| `status/` | Current status, checklists, and roadmap |
| `diary/` | Project log & daily diary |
| `scripts/` | Automation, backups, and logging scripts |
| `logs/` | Error logs and solutions |
| `notebooks/` | Jupyter/Colab notebooks |
| `tests/` | Unit & data validation tests |
| `scripts_library/` | Finalised reusable scripts/templates |
| `inspiration/` | Inspirational references |
| `archive-cursor_memory_project/` | Archived files (never delete) |
| `backups/` | Automated backups |

For a full explanation of every folder, consult the setup guide.

---

*Generated automatically by the Cursor AI assistant* 
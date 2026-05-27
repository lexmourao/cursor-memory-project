# Roadmap

> Roadmap for evolving the Cursor Memory Project as a reusable Cursor/Codex/ChatGPT memory setup template and local-first AI-assisted development backend.

## Current Focus

- Keep the repository internally consistent as a public technical artifact.
- Preserve the distinction between template mode and active project mode.
- Maintain green public CI and CodeQL.
- Avoid adding fake project knowledge to `memory-bank/`.
- Improve the backend/service layer only through small, auditable steps.

## Next

- [ ] Keep `memory-bank/README.md` aligned with template-mode behavior.
- [ ] Keep README references aligned with `env.template`.
- [ ] Keep `.cursor-rules.md` aligned with existing scripts and docs.
- [ ] Add a backend design document for the local-first memory API.
- [ ] Add a clearer FastAPI application structure under `app/`.
- [ ] Add typed request/response models for memory and retrieval endpoints.
- [ ] Add API tests for `/health`, `/memory`, and retrieval workflows.
- [ ] Improve backup/restore validation for encrypted archives.
- [ ] Improve benchmark isolation so synthetic data does not pollute real memory-bank files.
- [ ] Review MCP server defaults for local-first security.

## Backend Evolution

- [ ] Introduce `app/main.py` as the main FastAPI entry point.
- [ ] Add `app/core/config.py` for environment and path configuration.
- [ ] Add `app/models/` for typed API contracts.
- [ ] Add `app/services/` for memory, retrieval, and summarization logic.
- [ ] Add `app/api/` route modules for health, memory, retrieval, and metrics.
- [ ] Keep existing scripts as CLI wrappers around reusable services where practical.
- [ ] Add structured logging for backend service events.
- [ ] Add configurable host/CORS settings for local vs Docker/Nginx modes.

## Retrieval & Memory

- [ ] Add retrieval evaluation tests.
- [ ] Add chunk metadata schema.
- [ ] Decide whether retrieval metadata should remain pickle-based or move to JSON/SQLite.
- [ ] Evaluate local embedding fallback instead of zero-vector fallback.
- [ ] Add example populated memory-bank documentation under `docs/examples/` without filling the real starter memory-bank.

## Security & Reliability

- [ ] Document local CORS assumptions.
- [ ] Document localhost vs Docker/Nginx exposure modes.
- [ ] Add optional local API token authentication for non-localhost usage.
- [ ] Improve encrypted backup restore workflow.
- [ ] Evaluate `age` as an alternative to current GPG-encrypted backup flow.
- [ ] Add configured integration CI examples that use GitHub Actions secrets.

## Later

- [ ] Add cloud deployment template.
- [ ] Add Terraform or infrastructure-as-code example.
- [ ] Add multi-project memory dashboard.
- [ ] Add dashboard for inspecting memory records, retrieval chunks, and summaries.
- [ ] Add observability examples for logs, traces, and retrieval quality metrics.
- [ ] Add release packaging or tagged demo version.
- [ ] Add optional managed vector database integration such as Qdrant, Pinecone, or PgVector.

## Non-Goals

- Do not turn the starter memory-bank into fake project memory.
- Do not represent this repository as a complete production SaaS platform.
- Do not require private secrets in public CI.
- Do not add complex infrastructure before the local-first backend is clean and tested.

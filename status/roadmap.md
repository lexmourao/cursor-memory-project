# Roadmap

> Roadmap for evolving the Cursor Memory Project as a reusable Cursor/Codex/ChatGPT memory setup template and local-first AI-assisted development backend.

## Current Focus

- Keep the repository internally consistent as a public technical artifact.
- Preserve the distinction between template mode and active project mode.
- Maintain green public CI and GitHub code scanning.
- Avoid adding fake project knowledge to `memory-bank/`.
- Improve the backend/service layer only through small, auditable, green steps.
- Preserve existing CLI workflows while exposing selected capabilities through the FastAPI backend.

## Completed Foundation

- [x] Add `memory-bank/README.md` to explain template-mode behavior.
- [x] Align README references with `env.template`.
- [x] Align `.cursor-rules.md` with existing scripts and docs.
- [x] Add backend design document for the local-first memory API.
- [x] Add technical review guide for recruiters and engineering reviewers.
- [x] Add demo workflow documentation for reviewer inspection.
- [x] Clarify status checklists as starter templates.
- [x] Fix Docker Compose service structure.
- [x] Clarify Nginx as a starter local/single-VM reverse proxy.
- [x] Keep public CI green without requiring private secrets.
- [x] Keep GitHub code scanning active through repository security configuration.

## Completed Backend Slices

### Slice 1 — Health, Memory, Metrics

- [x] Introduce `app/main.py` as the main FastAPI entry point.
- [x] Add `app/core/config.py` for local-first environment and path configuration.
- [x] Add `app/models/health.py`.
- [x] Add `app/models/memory.py`.
- [x] Add `app/services/memory_service.py`.
- [x] Add `app/api/routes_health.py`.
- [x] Add `app/api/routes_memory.py`.
- [x] Add `GET /health`.
- [x] Add `GET /memory`.
- [x] Add `GET /memory/{record_id}`.
- [x] Add `GET /metrics`.
- [x] Add `tests/test_api_health.py`.
- [x] Add `tests/test_api_memory.py`.

### Slice 2 — Retrieval API

- [x] Add `app/models/retrieval.py`.
- [x] Add `app/services/retrieval_service.py`.
- [x] Add `app/api/routes_retrieval.py`.
- [x] Register retrieval router in `app/main.py`.
- [x] Add `POST /retrieval/query`.
- [x] Add validation for empty query text.
- [x] Add validation for `top_k` lower and upper bounds.
- [x] Add `tests/test_api_retrieval.py`.
- [x] Preserve existing `scripts/retrieve_context.py` CLI workflow.
- [x] Update `docs/BACKEND_DESIGN.md`.
- [x] Update `docs/DEMO_WORKFLOW.md`.
- [x] Update `README.md`.

## Next

- [ ] Update `status/roadmap.md` after each completed backend slice.
- [ ] Add deeper retrieval behavior tests after index rebuild.
- [ ] Test missing retrieval index behavior explicitly.
- [ ] Test empty retrieval index behavior explicitly.
- [ ] Improve retrieval result source metadata beyond the current `"memory-bank"` placeholder.
- [ ] Add chunk metadata schema.
- [ ] Decide whether retrieval metadata should remain pickle-based or move to JSON/SQLite.
- [ ] Improve benchmark isolation so synthetic data does not pollute real memory-bank files.
- [ ] Improve backup/restore validation for encrypted archives.
- [ ] Review MCP server defaults for local-first security.

## Next Backend Slice — Summarization Service

- [ ] Add `app/models/summarization.py`.
- [ ] Add `app/services/summarization_service.py`.
- [ ] Add `app/api/routes_summarization.py`.
- [ ] Register summarization router in `app/main.py`.
- [ ] Add `tests/test_api_summarization.py`.
- [ ] Preserve existing `scripts/summarize_chat.py` CLI workflow.
- [ ] Support manual/fallback summarization mode.
- [ ] Document summarization API behavior after implementation.
- [ ] Update README after summarization API is green.
- [ ] Update demo workflow after summarization API is green.
- [ ] Update backend design after summarization API is green.

## Retrieval & Memory Improvements

- [ ] Add retrieval evaluation tests.
- [ ] Add explicit retrieval index status endpoint or readiness check.
- [ ] Add chunk metadata schema.
- [ ] Add source filename to retrieval API results.
- [ ] Add chunk index to retrieval API results.
- [ ] Evaluate local embedding fallback instead of zero-vector fallback.
- [ ] Add example populated memory-bank documentation under `docs/examples/` without filling the real starter memory-bank.
- [ ] Consider JSON or SQLite metadata instead of pickle for safer inspectability.

## Security & Reliability

- [ ] Document local CORS assumptions.
- [ ] Document localhost vs Docker/Nginx exposure modes.
- [ ] Add optional local API token authentication for non-localhost usage.
- [ ] Add configurable CORS settings for local vs Docker/Nginx modes.
- [ ] Improve encrypted backup restore workflow.
- [ ] Evaluate `age` as an alternative to current GPG-encrypted backup flow.
- [ ] Add configured integration CI examples that use GitHub Actions secrets.
- [ ] Add structured logging for backend service events.
- [ ] Add readiness endpoint.
- [ ] Add stronger integration tests.

## Pending Non-Blocking Cleanup

- [ ] Review GitHub Actions Node.js 20 deprecation warnings.
- [ ] Consider updating stable actions when appropriate:
  - [ ] `actions/checkout@v4` → `actions/checkout@v5`
  - [ ] `actions/setup-python@v5` → `actions/setup-python@v6`
- [ ] Keep this cleanup non-blocking while workflows remain green.

## Later

- [ ] Add cloud deployment template.
- [ ] Add Terraform or infrastructure-as-code example.
- [ ] Add multi-project memory dashboard.
- [ ] Add dashboard for inspecting memory records, retrieval chunks, and summaries.
- [ ] Add observability examples for logs, traces, and retrieval quality metrics.
- [ ] Add release packaging or tagged demo version.
- [ ] Add optional managed vector database integration such as Qdrant, Pinecone, or PgVector.
- [ ] Consider converting `scripts/run_mcp_server.py` into a wrapper around `app.main`.

## Non-Goals

- Do not turn the starter memory-bank into fake project memory.
- Do not represent this repository as a complete production SaaS platform.
- Do not require private secrets in public CI.
- Do not add complex infrastructure before the local-first backend is clean and tested.
- Do not break existing CLI workflows while adding backend APIs.

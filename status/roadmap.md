# Roadmap

> Roadmap for evolving the Cursor Memory Project as a reusable Cursor/Codex/ChatGPT memory setup template and local-first AI-assisted development backend.

## Current Focus

- Keep the repository internally consistent as a public technical artifact.
- Preserve the distinction between template mode and active project mode.
- Maintain green public CI and GitHub code scanning.
- Avoid adding fake project knowledge to `memory-bank/`.
- Improve the backend/service layer only through small, auditable, green steps.
- Preserve existing CLI workflows while exposing selected capabilities through the FastAPI backend.
- Record important architecture decisions through ADRs before making risky storage, security, or infrastructure changes.
- Keep generated runtime artifacts out of version control unless intentionally curated as safe examples.

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
- [x] Update `.gitignore` for generated retrieval metadata exports.
- [x] Add `docs/GENERATED_FILES.md`.
- [x] Document generated metadata files and version-control expectations.

## Completed Architecture Decisions

- [x] Add `docs/adr/0001-public-ci-vs-integration-tests.md`.
- [x] Separate public CI smoke tests from secret-dependent integration workflows.
- [x] Add `docs/adr/0002-retrieval-metadata-storage.md`.
- [x] Decide to keep pickle for current FAISS metadata compatibility.
- [x] Document JSON metadata export as the next inspectability step.
- [x] Document SQLite as a later option for queryable dashboards or multi-project retrieval.

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

### Slice 2B — Metadata-Aware Retrieval

- [x] Add `query_with_metadata()` to `scripts/retrieve_context.py`.
- [x] Preserve existing `query()` function behavior.
- [x] Preserve CLI retrieval behavior.
- [x] Add source filename to retrieval API results.
- [x] Add chunk index to retrieval API results.
- [x] Add `chunk_idx` to `app/models/retrieval.py`.
- [x] Update `app/services/retrieval_service.py` to return source metadata.
- [x] Update `tests/test_api_retrieval.py` to validate metadata fields.
- [x] Update `docs/BACKEND_DESIGN.md`.
- [x] Update `docs/DEMO_WORKFLOW.md`.
- [x] Update `README.md`.

### Slice 2C — Retrieval Reliability

- [x] Test missing retrieval index behavior explicitly.
- [x] Test missing metadata file behavior with missing index state.
- [x] Test empty retrieval index behavior explicitly.
- [x] Confirm retrieval API returns empty results safely when local retrieval state is not ready.
- [x] Update `docs/BACKEND_DESIGN.md`.
- [x] Update `status/roadmap.md`.

### Slice 2D — Retrieval After Rebuild

- [x] Add deeper retrieval behavior test after index rebuild.
- [x] Use temporary memory-bank for retrieval rebuild test.
- [x] Use temporary FAISS index and metadata file.
- [x] Rebuild retrieval index inside isolated test state.
- [x] Query retrieval API after rebuild.
- [x] Validate returned source filename after rebuild.
- [x] Validate returned chunk index after rebuild.
- [x] Validate returned text content after rebuild.
- [x] Avoid polluting real `memory-bank/`.
- [x] Update `docs/BACKEND_DESIGN.md`.
- [x] Update `status/roadmap.md`.

### Slice 2E — Formal Chunk Metadata Schema

- [x] Add `app/models/chunk.py`.
- [x] Add `ChunkMetadata`.
- [x] Add `RetrievedChunk`.
- [x] Update `RetrievalResult` to inherit from `RetrievedChunk`.
- [x] Preserve existing retrieval API response shape.
- [x] Keep retrieval API tests green.
- [x] Update `docs/BACKEND_DESIGN.md`.
- [x] Update `status/roadmap.md`.

### Slice 2F — JSON Metadata Export

- [x] Add `META_JSON_FILE` to `scripts/retrieve_context.py`.
- [x] Add `_metadata_json_payload()`.
- [x] Add `export_metadata_json()`.
- [x] Add `export-meta-json` CLI command.
- [x] Preserve pickle as the internal FAISS runtime metadata format.
- [x] Add JSON metadata export test coverage.
- [x] Validate JSON `schema_version`.
- [x] Validate JSON source pickle path.
- [x] Validate JSON FAISS index path.
- [x] Validate JSON record count.
- [x] Validate JSON exported records.
- [x] Validate exported source filename, chunk index, and text content.
- [x] Update `docs/BACKEND_DESIGN.md`.
- [x] Update `status/roadmap.md`.

## Next

- [ ] Update `status/roadmap.md` after each completed backend slice.
- [ ] Add explicit retrieval index status endpoint or readiness check.
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
- [ ] Update roadmap after summarization API is green.

## Retrieval & Memory Improvements

- [ ] Add retrieval evaluation tests.
- [ ] Add explicit retrieval index status endpoint or readiness check.
- [x] Add JSON metadata export for inspectability.
- [x] Validate JSON metadata export against current retrieval metadata shape.
- [x] Document generated metadata files and version-control expectations.
- [ ] Evaluate local embedding fallback instead of zero-vector fallback.
- [ ] Add example populated memory-bank documentation under `docs/examples/` without filling the real starter memory-bank.
- [ ] Consider SQLite metadata storage only after dashboard, queryability, or multi-project requirements become real.
- [ ] Add dashboard-ready retrieval metadata notes for future UI work.

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
- [ ] Add dashboard for inspecting memory records, retrieval chunks, summaries, and retrieval metadata.
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
- Do not migrate retrieval metadata storage before documenting and testing a safe transition path.
- Do not commit generated retrieval indexes, pickle metadata, JSON metadata exports, logs, backups, secrets, caches, or temporary files unless intentionally curated as safe examples.

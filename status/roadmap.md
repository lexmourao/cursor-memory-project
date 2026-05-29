# Roadmap

> Roadmap for the Cursor Memory Project as a local-first AI-assisted development methodology repository.

## Current Version Scope

This repository is complete for its current public scope: a local-first AI-assisted development system that demonstrates persistent project memory, retrieval, summarization, metadata traceability, optional local API protection, configurable CORS, structured logging, CLI compatibility, documentation, and public CI/QA discipline.

The project should be presented as a technical portfolio and methodology artifact, not as a production SaaS platform, enterprise compliance system, or fully managed hosted service.

## Current Focus

- Keep the repository internally consistent as a public technical artifact.
- Preserve the distinction between template mode and active project mode.
- Maintain green public CI and GitHub code scanning.
- Keep generated runtime artifacts out of version control unless intentionally curated as safe examples.
- Keep security and exposure controls explicit, local-first, and tested.
- Preserve historical material through `archive/` instead of deleting it.
- Keep future production-evolution items clearly separated from current release completeness.

## Completed Methodology Milestones

### Foundation and Positioning

- [x] Clarified the repository as a local-first AI-assisted development methodology project.
- [x] Clarified that the repository is not a production SaaS platform.
- [x] Updated README positioning.
- [x] Aligned reviewer-facing guides with the methodology scope.
- [x] Added and updated the methodology cleanup checkpoint.
- [x] Preserved historical material through `archive/`.

### Test and QA Baseline

- [x] Stabilized the local pytest baseline.
- [x] Kept public CI green.
- [x] Verified `ruff check .`.
- [x] Verified `bandit -q -ll -r scripts tests`.
- [x] Verified `pytest -q` with 42 passed and 2 skipped.
- [x] Kept GitHub code scanning active.

### Workflow and Deployment Scope Cleanup

- [x] Archived overbuilt GitHub Actions workflows under `archive/deprecated-workflows/`.
- [x] Kept only `.github/workflows/ci.yml` active.
- [x] Archived production-style compliance and incident-response docs under `archive/deprecated-docs/`.
- [x] Archived Docker, Docker Compose, Nginx, and Prometheus deployment scaffolding under `archive/deprecated-deployment/`.
- [x] Updated active docs so archived deployment material is described as reference-only.

### Code Safety and Local Security

- [x] Replaced shell-based bootstrap git calls with `subprocess.run(...)`.
- [x] Defaulted the MCP stub server host to `127.0.0.1`.
- [x] Documented the trusted local retrieval metadata pickle boundary with a narrow Bandit suppression.
- [x] Kept Bandit passing without medium/high findings.
- [x] Preserved local-first security assumptions in active documentation.

### Backend and Memory System

- [x] Preserved the local FastAPI backend for health, memory, retrieval, retrieval status, summarization, metrics, optional local token protection, configurable CORS, and structured logging.
- [x] Preserved CLI workflows for summarization and retrieval.
- [x] Preserved FAISS-based local retrieval.
- [x] Preserved pickle as the internal FAISS runtime metadata format for now.
- [x] Preserved JSON metadata export for inspection and review.
- [x] Preserved tests for API, CLI, retrieval, summarization, edge cases, and local security behavior.

## Current Verified State

Latest verified cleanup state:

- `main` is up to date with `origin/main`.
- Working tree is clean.
- Active workflow surface is minimal.
- Active deployment scaffolding has been archived.
- `ruff check .` passes.
- `bandit -q -ll -r scripts tests` passes.
- `pytest -q` passes with 42 passed and 2 skipped.
- Known warnings are dependency/runtime deprecation warnings and are not blocking.

## Remaining Work for This Cleanup Cycle

- [ ] Add a final methodology cleanup release note.
- [ ] Run one final stale-reference scan before tagging or calling the cleanup complete.
- [ ] Decide whether to tag a methodology cleanup release.

## Deferred Future Evolution

These items are intentionally deferred. They are not required for the current local-first public scope.

- Retrieval evaluation tests and quality scoring.
- SQLite or another queryable metadata store if dashboard or multi-project retrieval becomes necessary.
- A memory/retrieval dashboard.
- Hosted or containerized deployment templates after separate operational review.
- Backup/restore hardening if real operational usage requires it.
- More formal type checking gates.
- Dependency update automation beyond the current public CI scope.
- Additional API hardening before any public or multi-user exposure.

## Archive Policy

Do not delete historical scaffolding unless there is a clear reason. Prefer moving files to `archive/` with a README explaining:

- what was archived,
- why it was archived,
- whether it is reference-only,
- and what must be reviewed before restoring it.

Current archived areas include:

- `archive/deprecated-workflows/`
- `archive/deprecated-docs/`
- `archive/deprecated-deployment/`

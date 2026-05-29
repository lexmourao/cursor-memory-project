# Methodology Cleanup Release Note

Date: 2026-05-29  
Branch base: main  
Release note purpose: summarize the methodology cleanup cycle that repositioned the Cursor Memory Project as a clear local-first AI-assisted development methodology repository.

## Summary

This cleanup cycle reduced overbuilt production-style framing, archived inactive operational scaffolding, clarified the repository's public scope, and preserved the technical value of the project as a local-first AI-assisted development methodology artifact.

The project should now be presented as:

- a local-first AI-assisted development methodology repository,
- a public technical portfolio artifact,
- a memory, retrieval, summarization, documentation, QA, and workflow-governance system,
- and a demonstration of disciplined AI-assisted engineering practice.

It should not be presented as:

- a production SaaS platform,
- an enterprise compliance system,
- a hardened hosted deployment,
- or a fully managed security operations system.

## What Changed

### Positioning and Documentation

- Clarified README positioning.
- Aligned reviewer-facing documentation with the methodology scope.
- Simplified the roadmap into a concise methodology-focused status document.
- Updated the methodology cleanup checkpoint.
- Preserved detailed historical context through Git history and archive folders.

### Workflow Scope

- Reduced active GitHub Actions to the public CI workflow.
- Archived overbuilt scheduled workflows under `archive/deprecated-workflows/`.
- Archived the scheduled OpenAI smoke workflow.
- Archived the scheduled nightly integration workflow.
- Kept GitHub code scanning active.

### Deployment Scope

- Archived Docker, Docker Compose, Nginx, and Prometheus deployment scaffolding under `archive/deprecated-deployment/`.
- Updated active documentation so deployment scaffolding is reference-only.
- Removed active root-level deployment files that made the repo look more production-oriented than its current scope.

### Security and Code Safety

- Replaced shell-based bootstrap git calls with `subprocess.run(...)`.
- Defaulted the MCP stub server host to `127.0.0.1`.
- Documented the trusted local retrieval metadata pickle boundary with a narrow Bandit suppression.
- Kept Bandit passing without medium/high findings.

### Archive Policy

Historical scaffolding was preserved instead of deleted.

Current archived areas include:

- `archive/deprecated-workflows/`
- `archive/deprecated-docs/`
- `archive/deprecated-deployment/`

Archived material should be treated as reference-only unless it is intentionally reviewed, updated, and restored in a future scoped PR.

## Current Verified State

At the end of this cleanup cycle:

- `main` is up to date with `origin/main`.
- Working tree is clean.
- Active workflow surface is minimal.
- Active deployment scaffolding has been archived.
- `status/roadmap.md` is simplified.
- `ruff check .` passes.
- `bandit -q -ll -r scripts tests` passes.
- `pytest -q` passes with 42 passed and 2 skipped.
- Existing warnings are known dependency/runtime deprecation warnings and are not blocking.

## Remaining Optional Follow-Up

Before tagging or calling the cleanup fully complete, run one final stale-reference scan across active docs and decide whether to tag a methodology cleanup release.

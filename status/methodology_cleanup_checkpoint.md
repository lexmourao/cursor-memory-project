# Methodology Cleanup Checkpoint

Date: 2026-05-29
Branch base: main
Checkpoint purpose: record the stable repository state after the first methodology-focused cleanup cycle.

## Summary

This checkpoint marks the transition of the Cursor Memory Project from an overbuilt production-style technical artifact toward a clearer local-first AI-assisted development methodology repository.

The cleanup preserved historical material through archive/ instead of deleting it, reduced active CI noise, and stabilized the local test baseline.

## Completed before this checkpoint

### PR #11 - Local pytest baseline stabilization

Merged commit:

- test: stabilize local pytest baseline

Purpose:

- Add pytest import-path configuration.
- Skip encrypted backup tests when GPG_KEY_ID is not configured.
- Align mocked summarization expectations.
- Make local pytest runnable from a clean local clone.

Verification after merge:

- ruff check . passed
- pytest -q passed with 42 passed and 2 skipped

### PR #13 - Archive overbuilt workflows and production-style docs

Merged PR:

- chore: archive overbuilt workflows and production-style docs

Purpose:

- Move overbuilt active GitHub Actions workflows out of .github/workflows/.
- Preserve deprecated workflows under archive/deprecated-workflows/.
- Move production-style incident response and compliance documentation out of active docs.
- Preserve deprecated docs under archive/deprecated-docs/.
- Update docs/SECURITY.md so the archived incident response plan is reference-only.

## Current active workflows

After the cleanup, the active GitHub Actions workflows are:

- .github/workflows/ci.yml

The following workflows were archived:

- archive/deprecated-workflows/backup.yml
- archive/deprecated-workflows/health.yml
- archive/deprecated-workflows/performance.yml
- archive/deprecated-workflows/security.yml
- archive/deprecated-workflows/nightly-integration.yml
- archive/deprecated-workflows/weekly-openai.yml

## Current archived documentation

The following production-style documentation was moved out of the active docs surface:

- archive/deprecated-docs/INCIDENT_RESPONSE.md
- archive/deprecated-docs/compliance_templates/

These files are preserved for auditability and future reference.

## Current verification state

The repository was verified locally after the cleanup:

- git status: clean
- ruff check .: passed
- pytest -q: 42 passed, 2 skipped

Existing warnings are known dependency/runtime warnings and are not blocking this checkpoint.

## Scope clarification

This repository should now be treated as:

- A local-first Cursor Memory / AI-assisted development methodology project.

It should not be presented as:

- A production SaaS platform.
- An enterprise compliance system.
- A fully managed security operations system.

## Post-checkpoint update

PR #17 later archived the scheduled nightly integration workflow. The workflow is now preserved at `archive/deprecated-workflows/nightly-integration.yml` and is no longer part of the active `.github/workflows/` set.

This follow-up cleanup later archived the scheduled OpenAI smoke workflow. The workflow is now preserved at `archive/deprecated-workflows/weekly-openai.yml` and is no longer part of the active `.github/workflows/` set.

## Next recommended work

1. Clarify README positioning.
2. Align docs/TECHNICAL_REVIEW.md and docs/DEMO_WORKFLOW.md with the methodology scope.
3. Run stale-reference cleanup across active docs.
4. Fix the real bootstrap script shell-call issue in a dedicated code-safety commit.
5. Review Docker, Nginx, Prometheus, and deployment scaffolding for scope fit.
6. Simplify the roadmap around methodology milestones.
7. Add a final methodology cleanup release note.

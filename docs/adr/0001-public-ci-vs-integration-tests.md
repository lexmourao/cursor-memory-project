# ADR 0001: Separate Public CI Smoke Tests from Secret-Dependent Integration Tests

## Status

Accepted

## Date

2026-05-27

## Context

This repository includes both public validation workflows and environment-specific integration workflows.

Some tests can run safely in public CI without secrets, such as linting, type checking, dependency/security checks, and smoke tests. Other tests depend on local or private configuration, such as encrypted backup workflows that require `GPG_KEY_ID`.

Running secret-dependent integration tests in public CI would either fail consistently or require exposing sensitive configuration. Neither option is appropriate for a public technical repository.

## Decision

The public CI workflow will run:

- `ruff check .`
- `mypy scripts tests`
- `pip-audit --strict`
- focused smoke tests for public workflow validation

Secret-dependent backup tests and full end-to-end workflows will be treated as configured integration tests. They should run only in environments where required secrets and local configuration are available.

## Rationale

This decision keeps the public repository reviewable, honest, and maintainable.

The goal of public CI is to prove that the repository has a healthy baseline:

- code can be checked for linting issues
- Python typing is validated
- dependency/security checks run
- core smoke tests pass
- public workflow does not require private secrets

The goal of configured integration testing is different. It validates deeper operational flows such as encrypted backup and restore behavior, which require environment-specific setup.

Separating these concerns prevents false CI failures while preserving the ability to test deeper workflows in the right environment.

## Consequences

### Positive

- Public CI remains green and useful for reviewers.
- Secret-dependent tests are not forced into an unconfigured public environment.
- The repository communicates a clearer testing strategy.
- Integration workflows can be strengthened later without weakening public CI.
- The project avoids exposing private keys or sensitive environment configuration.

### Negative

- Public CI does not prove every backup or end-to-end workflow.
- Reviewers must read the documentation to understand which tests are smoke tests and which require configured integration environments.
- A separate integration workflow should be added later for full operational validation.

## Future Work

- Add a dedicated integration workflow for backup and restore tests.
- Document local GPG setup for encrypted backup validation.
- Add retrieval evaluation tests.
- Add environment-specific CI examples using GitHub Actions secrets.
- Add release checks before publishing a public version.

## Senior Engineering Note

This decision reflects a deliberate separation between public repository health checks and environment-specific operational validation. It avoids pretending that secret-dependent production-like workflows can run safely in public CI without configuration.

The current public CI demonstrates repository quality and maintainability, while configured integration testing remains the appropriate place for full backup, restore, and secret-dependent workflows.

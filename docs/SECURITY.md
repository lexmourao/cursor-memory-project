# Security & Compliance

> This document describes the security posture, local exposure assumptions, data-handling expectations, and compliance boundaries for the Cursor Memory Project.

---

## 1. Purpose

The Cursor Memory Project is designed as a local-first developer infrastructure project for AI-assisted development workflows, persistent memory, retrieval, summarization, and backend API experimentation.

The project is not currently designed as a public multi-tenant SaaS platform.

Security expectations are therefore based on:

- local development usage
- localhost-first backend access
- explicit avoidance of secrets and sensitive personal data in project memory
- public CI that does not require private credentials
- clear separation between safe public workflows and configured integration workflows

---

## 2. Local-First Security Model

The default security model is local-first.

Default assumptions:

- The backend is intended to run on a developer machine or controlled local environment.
- The API should bind to localhost by default.
- The memory-bank should be treated as local project context, not as a secure secrets store.
- Public exposure requires additional security controls before use.
- Docker and Nginx examples are starter infrastructure patterns, not proof of production hardening.

The backend configuration should favor:

```text
HOST=127.0.0.1
RUNTIME_MODE=local
MEMORY_BANK_DIR=memory-bank
```

Running the backend on `0.0.0.0`, behind Nginx, or inside a publicly reachable Docker host changes the threat model and should only be done after adding appropriate access controls.

---

## 3. API Exposure Assumptions

Implemented backend endpoints include:

```text
GET /health
GET /memory
GET /memory/{record_id}
GET /metrics
GET /retrieval/status
POST /retrieval/query
POST /summarization/summarize
```

These endpoints are intended for local development and controlled inspection.

Security-sensitive considerations:

- `GET /memory` exposes allowed memory-bank markdown content.
- `GET /memory/{record_id}` exposes a specific memory record.
- `POST /retrieval/query` returns retrieved memory chunks.
- `GET /retrieval/status` exposes local retrieval index readiness and metadata counts.
- `POST /summarization/summarize` can write to `memory-bank/activeContext.md`.
- `GET /metrics` exposes Prometheus-compatible service metrics.

These endpoints should not be exposed publicly without authentication, authorization, network controls, and review of the memory-bank contents.

---

## 4. CORS Assumptions

The current project does not require broad CORS access for the local-first backend.

Default assumption:

```text
No public browser client should need unrestricted cross-origin access.
```

If a frontend dashboard is added later, CORS should be configured explicitly and narrowly.

Recommended future approach:

```text
Local development:
- allow only localhost origins used by the local dashboard

Docker/Nginx mode:
- allow only the configured dashboard domain or local hostnames

Public deployment:
- require authentication before enabling cross-origin browser access
- avoid wildcard origins
```

Wildcard CORS should not be used for a backend that exposes memory records, retrieval results, summaries, or project context.

---

## 5. Localhost vs Docker/Nginx Exposure

### Localhost Mode

Recommended default:

```text
127.0.0.1 only
```

Use this mode for:

- local development
- technical review
- API testing
- retrieval inspection
- summarization workflow testing

### Docker Mode

Docker may expose ports beyond localhost depending on compose and host configuration.

Before using Docker beyond local development:

- confirm which ports are exposed
- confirm whether the service is reachable from the network
- confirm `.env` and secrets are not baked into images
- confirm generated memory and retrieval files are not accidentally mounted into public contexts

### Nginx Mode

The Nginx configuration is a starter example.

It should not be interpreted as complete production security.

Before using Nginx in a public or shared environment, add:

- TLS
- authentication
- request size limits
- rate limiting
- access logs
- security headers
- upstream timeout review
- explicit routing rules
- review of exposed endpoints

---

## 6. Authentication Boundary

The current backend does not yet implement API authentication.

Current assumption:

```text
Safe only for local or controlled environments.
```

Future recommended enhancement:

```text
Optional local API token authentication for non-localhost usage.
```

A future API token should protect at least:

```text
GET /memory
GET /memory/{record_id}
POST /retrieval/query
POST /summarization/summarize
GET /retrieval/status
GET /metrics
```

The token should be configured through environment variables or secrets, not hardcoded.

Example future configuration:

```text
LOCAL_API_TOKEN=
ENABLE_LOCAL_API_TOKEN=true
```

---

## 7. Data Handling

The project handles local text and generated retrieval artifacts.

Rules:

- Do not commit secrets.
- Do not store credentials in `memory-bank/`.
- Do not store private API keys in markdown files.
- Do not store client-confidential information in the public repository.
- Do not store personal data, PHI, or regulated health data in the public memory-bank.
- Use `env.template` for safe configuration examples.
- Use `.env` for local secrets and keep it ignored by Git.

The `memory-bank/` directory must not contain:

```text
API keys
passwords
tokens
private client data
regulated health data
personal identifying information
financial account data
production credentials
```

---

## 8. Generated Files

Retrieval workflows generate local runtime files such as:

```text
memory-bank/embeddings.faiss
memory-bank/embeddings_meta.pkl
memory-bank/embeddings_meta.json
```

These are generated artifacts and should not be committed by default.

The JSON metadata export is intended for local inspection and debugging. It should still be treated carefully because it may contain excerpts from memory-bank content.

See:

```text
docs/GENERATED_FILES.md
docs/adr/0002-retrieval-metadata-storage.md
```

---

## 9. Logs and Backups

Logs are stored locally in:

```text
logs/
```

Backup workflows may create archives of project state.

Security expectations:

- Review logs before sharing publicly.
- Do not commit logs containing secrets or sensitive data.
- Do not include private `.env` files in public artifacts.
- Treat encrypted backups as sensitive operational artifacts.
- Validate restore workflows before relying on backups for recovery.

Backup and restore workflows that require secrets should run only in configured environments.

---

## 10. Public CI and Secret-Dependent Workflows

Public CI should remain safe without private credentials.

Public CI should run:

- linting
- type checking
- dependency/security checks
- smoke tests
- deterministic tests that do not require private secrets

Secret-dependent integration workflows should remain separate.

Examples of secret-dependent workflows:

- OpenAI-backed live summarization
- real embedding generation with private API keys
- encrypted backup workflows requiring `GPG_KEY_ID`
- deployment workflows requiring cloud credentials

See:

```text
docs/adr/0001-public-ci-vs-integration-tests.md
```

---

## 11. Compliance Posture

The project aligns with GDPR/LGPD principles by avoiding the storage of personal data by default.

Current compliance posture:

- The public repository should not contain personal data.
- The starter memory-bank should remain mostly empty until real project use.
- Private project data should not be committed.
- Generated retrieval artifacts should remain local and ignored.
- Public CI should not require or expose secrets.
- Data deletion and redaction workflows should be used if sensitive local data is accidentally introduced.

Data deletion helper:

```bash
python scripts/data_deletion_cli.py <regex>
```

This can redact matching content and create a new encrypted backup for local compliance workflows.

---

## 12. Incident Response

For incidents involving accidental exposure, leaked secrets, sensitive memory-bank content, or unsafe generated artifacts:

1. Stop further sharing or deployment.
2. Remove the sensitive content from the working tree.
3. Rotate any exposed credentials.
4. Review Git history if the data was committed.
5. Create a clean commit removing the exposure.
6. Document the incident and remediation.
7. Review whether `.gitignore`, docs, or tests need updates.

Refer to:

```text
docs/INCIDENT_RESPONSE.md
```

for roles, severity levels, and procedures.

---

## 13. Current Security Controls

Current controls include:

- local-first default posture
- `.env` ignored by Git
- safe `env.template`
- generated retrieval files ignored by Git
- memory API exposing only allowed markdown memory records
- retrieval query validation
- summarization input validation
- retrieval status reporting
- public CI without required secrets
- dependency/security audit with `pip-audit`
- type checking with `mypy`
- linting with `ruff`
- GitHub code scanning / CodeQL through repository security configuration
- documentation of generated-file expectations
- ADR separation for public CI vs integration workflows

---

## 14. Future Security Improvements

Planned or recommended improvements:

```text
[ ] Add optional local API token authentication for non-localhost usage.
[ ] Add configurable CORS settings.
[ ] Document Docker/Nginx deployment security assumptions in more detail.
[ ] Add structured security-related logging.
[ ] Add rate limiting for non-localhost usage.
[ ] Add request size limits for summarization input.
[ ] Add configured integration CI examples using GitHub Actions secrets.
[ ] Improve encrypted backup restore validation.
[ ] Evaluate age as an alternative to GPG-encrypted backup flow.
```

---

## 15. Summary

The Cursor Memory Project is currently safest when used as a local-first developer tool.

It is appropriate for:

- local AI-assisted development workflows
- technical review
- memory-bank experimentation
- retrieval and summarization API development
- documentation and CI/QA demonstration

It should not be treated as publicly deployable without additional hardening.

Before any public exposure, the project should add authentication, explicit CORS controls, network restrictions, request limits, logging review, and a careful audit of memory-bank contents and generated artifacts.

# Deprecated Deployment Scaffolding

This folder preserves optional deployment scaffolding that was moved out of the active repository root during the local-first methodology cleanup.

These files are archived for auditability and future reference. They are not part of the active local-first development workflow.

Archived files include:

- Dockerfile
- docker-compose.yml
- nginx/
- prometheus.yml

Why these files were archived:

- The current project scope is a local-first AI-assisted development methodology repository.
- The active repo should not imply production SaaS deployment readiness.
- Docker, Nginx, Prometheus, Grafana, TLS proxy, and single-VM assumptions require separate operational review before active use.
- Deployment scaffolding remains available for future adaptation if the project intentionally evolves toward hosted or containerized runtime usage.

Before restoring any file from this archive, review and revalidate:

- local vs public exposure assumptions
- secrets handling
- TLS and authentication model
- network binding
- logging and monitoring requirements
- backup and restore behavior
- dependency and container hardening

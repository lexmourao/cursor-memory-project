# Release Checklist

> Starter release checklist for projects created from the Cursor Memory Project template.  
> Use this before tagging a new version, sharing the repository publicly, or deploying a configured project environment.

## Code & Tests

- [ ] Public CI workflow is green
- [ ] GitHub code scanning (CodeQL) is green on the repository security page
- [ ] `ruff check .` passes
- [ ] `mypy app scripts tests` passes
- [ ] `pip-audit --strict` passes
- [ ] Focused public smoke tests pass
- [ ] Integration and coverage gates pass in the configured environment, if enabled

## Documentation

- [ ] `README.md` reflects the current project scope
- [ ] `memory-bank/README.md` explains template mode
- [ ] `docs/ARCHITECTURE.md` reflects the current architecture
- [ ] `docs/DEMO_WORKFLOW.md` reflects the current reviewer/demo path
- [ ] `docs/SECURITY.md` reflects the current security posture
- [ ] `docs/DEPLOYMENT.md` reflects the current deployment assumptions
- [ ] `status/roadmap.md` reflects current next steps

## Memory & Data Integrity

- [ ] `memory-bank/` contains only template or real project context
- [ ] No fake project knowledge has been added to memory-bank files
- [ ] No secrets, credentials, PII, PHI, or client-confidential data are stored in `memory-bank/`
- [ ] Generated retrieval files are excluded from version control
- [ ] `scripts/retrieve_context.py rebuild` runs successfully in the intended environment

## Backup & Restore

- [ ] Backup strategy is documented for the intended environment
- [ ] `GPG_KEY_ID` or configured secret path is available when encrypted backups are required
- [ ] `scripts/backup_data.sh` runs successfully in the configured environment
- [ ] If backups are encrypted, decrypt in a safe temporary location before validating archive contents
- [ ] Restore validation is tested in the configured integration environment, if enabled

## Security

- [ ] Secret scan shows no committed secrets
- [ ] Dependency/security checks are green
- [ ] Public CI does not require private secrets
- [ ] Local `.env` files are ignored
- [ ] `env.template` remains committed as the safe setup template
- [ ] Nginx configuration is understood as a starter local/single-VM reverse proxy, not a fully hardened production gateway

## Deployment

- [ ] Local MCP server starts successfully
- [ ] `/health` endpoint returns expected status
- [ ] `/memory` endpoint returns expected memory records
- [ ] Docker Compose configuration is valid, if used
- [ ] Production deployment assumptions are documented before exposing the service beyond local development

## Sign-Off

- [ ] Project owner approval
- [ ] Technical review completed
- [ ] Documentation review completed
- [ ] Security assumptions reviewed

---

After all required items are checked, tag the release if applicable:

```bash
git tag -a vX.Y.Z -m "Release vX.Y.Z" && git push --tags

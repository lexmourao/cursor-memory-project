# Deployment Checklist

> Starter deployment checklist for projects created from the Cursor Memory Project template.  
> Use this when the memory server is deployed beyond local development or exposed through Docker, Nginx, or a production-like environment.

## Local Development

- [ ] Dependencies installed from `requirements.txt`
- [ ] Environment file created from `env.template` if needed
- [ ] Local MCP server starts successfully
- [ ] `/health` endpoint returns expected status
- [ ] `/memory` endpoint returns expected memory records
- [ ] `memory-bank/` contains template files or real project context
- [ ] Generated retrieval files are excluded from version control

## Docker / Single-VM Deployment

- [ ] Docker image builds successfully
- [ ] Docker Compose file validates successfully
- [ ] `memory` service starts successfully
- [ ] Mounted volumes are available for `memory-bank/`, `logs/`, and `backups/`
- [ ] Container runs without hardcoded secrets
- [ ] Docker secrets or approved environment configuration are available if needed
- [ ] Read-only filesystem assumptions are tested before production-like use

## Nginx / Reverse Proxy

- [ ] Nginx configuration is understood as a starter local/single-VM reverse proxy
- [ ] TLS certificate paths exist
- [ ] Basic-auth file exists if Nginx basic auth is enabled
- [ ] HTTP-to-HTTPS redirect works if enabled
- [ ] Forwarded headers are configured
- [ ] Firewall rules restrict direct access to the memory service when exposed beyond localhost
- [ ] Production deployments add managed TLS, stronger authentication, rate limiting, structured logs, and monitoring

## Backups

- [ ] Backup directory exists
- [ ] `GPG_KEY_ID` or configured secret path is available when encrypted backups are required
- [ ] `scripts/backup_data.sh` runs successfully in the configured environment
- [ ] Backup archive is created
- [ ] Encrypted backups are decrypted in a safe temporary location before archive validation
- [ ] Restore validation is tested in the configured integration environment, if enabled
- [ ] Backup retention policy is documented

## Monitoring

- [ ] `/metrics` endpoint is available if Prometheus monitoring is enabled
- [ ] Prometheus configuration points to the correct service target
- [ ] Grafana starts successfully if enabled
- [ ] Health-check workflow or external monitoring is configured for production-like use
- [ ] Alerting assumptions are documented before relying on them

## Security

- [ ] `.env` and local secret files are ignored by Git
- [ ] `env.template` remains committed as the safe setup template
- [ ] No API keys, credentials, PII, PHI, or client-confidential data are stored in `memory-bank/`
- [ ] Public CI does not require private secrets
- [ ] Dependency/security checks are green
- [ ] External exposure is reviewed before binding services beyond localhost

## Documentation

- [ ] `README.md` reflects the current setup flow
- [ ] `docs/DEPLOYMENT.md` reflects the current deployment assumptions
- [ ] `docs/SECURITY.md` reflects the current security assumptions
- [ ] `docs/ARCHITECTURE.md` reflects current runtime modes
- [ ] `status/release_checklist.md` has been reviewed before tagging or sharing

## Sign-Off

- [ ] Project owner review completed
- [ ] Technical assumptions reviewed
- [ ] Security assumptions reviewed
- [ ] Deployment assumptions reviewed

# Security & Compliance

This project handles local text files only; nevertheless we follow best practices to protect any sensitive data.

## Data Handling
* `data/raw/` holds immutable source data; never commit secrets.
* `memory-bank/` must not contain credentials or personal data.
* Logs are stored locally in `logs/` and included in backups.
* Data deletion: Use `scripts/data_deletion_cli.py <regex>` to redact and create new encrypted backup in compliance with GDPR Art. 17 and LGPD Art. 18 VI.

## Access Control
* Contributors are given least-privilege access.
* Production deployment runs under dedicated `cursor` user.

## Incident Response
Refer to [INCIDENT_RESPONSE.md](INCIDENT_RESPONSE.md) for roles, severity levels, and procedures.

## Compliance
* Aligns with GDPR/LGPD principles by avoiding personal data storage.
* Backups retained 7 days in GitHub artifacts. 
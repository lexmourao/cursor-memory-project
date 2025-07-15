# Deployment Guide

This document outlines how to run the MCP server and nightly backups in a production environment.

## 1. Prerequisites
* Python 3.11
* `pip install -r requirements.txt`
* Clone this repository at `/opt/cursor-memory` (example path)

## 2. Systemd Service
Create `/etc/systemd/system/cursor-mcp.service`:
```ini
[Unit]
Description=Cursor Memory MCP Server
After=network.target

[Service]
WorkingDirectory=/opt/cursor-memory
ExecStart=/usr/bin/python scripts/run_mcp_server.py
Restart=on-failure
User=cursor

[Install]
WantedBy=multi-user.target
```
Then enable & start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now cursor-mcp.service
```

## 3. Nightly Backup Cron
Add in root's crontab (`sudo crontab -e`):
```
0 2 * * * /opt/cursor-memory/scripts/backup_data.sh >> /var/log/cursor_backup.log 2>&1
```
This runs every day at 02:00 and stores archives in `/opt/cursor-memory/backups`.

Backups are **always encrypted**. Set `GPG_KEY_ID` in the service environment (`/etc/systemd/system/cursor-mcp.service` `Environment=` line). The backup script will fail if the variable is missing.

## 4. Restore Procedure
```bash
cd /opt/cursor-memory
# pick archive
tar -xzf backups/project_backup_YYYYMMDD_HHMMSS.tar.gz
```

## 5. GitHub Actions Nightly Artifact
Nightly backups can also be uploaded as workflow artifacts. See `.github/workflows/backup.yml`. 

## 6. Docker Compose (single-VM)

### TLS & Basic Auth Proxy
Run once to generate self-signed cert & basic-auth credentials:
```bash
./scripts/gen_self_signed.sh
```
Then start the stack:
```bash
docker compose up -d --build
```
Access the API at https://localhost (credentials you set). In production replace certs with valid TLS certificates. 

### Docker Secrets Setup
Create `secrets/` folder and add two files:
```
secrets/openai_api_key   # contains only the key string
secrets/gpg_key_id       # GPG recipient key ID (email or fingerprint)
```
Docker compose mounts these into `/run/secrets/` for the `memory` service. Remove plaintext keys from `.env` in production. 

### Metrics & Monitoring
Prometheus and Grafana services are included in `docker-compose.yml`.

1. Start stack: `docker compose up -d --build`
2. Prometheus UI: http://localhost:9090 (scrapes MCP `/metrics`)
3. Grafana UI: http://localhost:3000 (default admin/admin). Add Prometheus data source at `http://prometheus:9090` and import dashboard as needed. 
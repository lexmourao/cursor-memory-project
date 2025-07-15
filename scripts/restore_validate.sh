#!/usr/bin/env bash
set -euo pipefail

BACKUP_DIR="backups"
LATEST=$(ls -1t $BACKUP_DIR/project_backup_* | head -n1 || true)
if [[ -z "$LATEST" ]]; then
  echo "[restore] No backup archive found" >&2
  exit 1
fi

echo "[restore] Using archive $LATEST"

rm -rf memory-bank
mkdir memory-bank

tar -xzf "$LATEST"

python scripts/retrieve_context.py rebuild
python scripts/health_check.py

echo "[restore] Restore validation OK" 
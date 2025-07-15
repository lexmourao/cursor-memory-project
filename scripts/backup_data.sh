#!/usr/bin/env bash
set -euo pipefail

BACKUP_DIR="backups"
DATE=$(date +"%Y%m%d_%H%M%S")
ARCHIVE="$BACKUP_DIR/project_backup_$DATE.tar.gz"

mkdir -p "$BACKUP_DIR"

tar -czf "$ARCHIVE" memory-bank logs status || {
  echo "[backup] Tar failed" >&2
  exit 1
}

# prune >30d
find "$BACKUP_DIR" -name 'project_backup_*.tar.gz.gpg' -mtime +30 -delete

if [[ -z "${GPG_KEY_ID-}" ]]; then
  echo "[backup] Error: GPG_KEY_ID environment variable must be set for encrypted backups." >&2
  exit 1
fi

# encrypt archive
gpg --output "$ARCHIVE.gpg" --encrypt --recipient "$GPG_KEY_ID" "$ARCHIVE"
rm "$ARCHIVE"
ARCHIVE="$ARCHIVE.gpg"

echo "[backup] Final archive: $ARCHIVE" 
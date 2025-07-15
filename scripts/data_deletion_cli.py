import argparse
import re
from pathlib import Path
import subprocess
import shutil
import tarfile
from datetime import datetime
import os

MEMORY_DIR = Path("memory-bank")
BACKUP_DIR = Path("backups")

REDACTION_TOKEN = "[[REDACTED]]"

def redact_file(path: Path, pattern: re.Pattern) -> bool:
    text = path.read_text(encoding="utf-8")
    new_text, n = pattern.subn(REDACTION_TOKEN, text)
    if n:
        path.write_text(new_text, encoding="utf-8")
    return n > 0

def scan_and_redact(pattern_str: str):
    pattern = re.compile(pattern_str, re.IGNORECASE)
    changed = False
    for md in MEMORY_DIR.glob("*.md"):
        if redact_file(md, pattern):
            print(f"[delete] Redacted matches in {md}")
            changed = True
    if not changed:
        print("[delete] No matches found in memory-bank.")
    return changed

def create_backup():
    # rely on existing backup script
    subprocess.check_call(["scripts/backup_data.sh"])


def main():
    parser = argparse.ArgumentParser(description="Redact personal data across memory-bank and create new encrypted backup.")
    parser.add_argument("pattern", help="Regex pattern to search (e.g., email or name)")
    args = parser.parse_args()
    if scan_and_redact(args.pattern):
        print("[delete] Creating new backup after redaction...")
        create_backup()
        print("[delete] Done.")
    else:
        print("[delete] Nothing redacted; backup not created.")

if __name__ == "__main__":
    main() 
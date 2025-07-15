import subprocess
from datetime import datetime
from pathlib import Path
import re

PROGRESS_FILE = Path("memory-bank/progress.md")
INDEX_FILE = Path("memory-bank/embeddings.faiss")

STATUS_PATTERN = re.compile(r"^\| (Memory Bank|Summarization Engine|Retrieval Engine) .*", re.MULTILINE)


def derive_status() -> dict[str, str]:
    status = {}
    status["Memory Bank"] = "OK" if any(Path("memory-bank").glob("*.md")) else "EMPTY"
    status["Summarization Engine"] = "OK" if PROGRESS_FILE.exists() else "UNKNOWN"
    status["Retrieval Engine"] = "OK" if INDEX_FILE.exists() else "NOT BUILT"
    return status


def update_table(lines: list[str], status_map: dict[str, str]) -> list[str]:
    new_lines = []
    for line in lines:
        m = STATUS_PATTERN.match(line)
        if m:
            key = m.group(1)
            parts = line.split("|")
            parts[2] = f" {status_map.get(key, 'UNKNOWN')} "
            new_lines.append("|".join(parts))
        else:
            new_lines.append(line)
    return new_lines


def main():
    if not PROGRESS_FILE.exists():
        print("progress.md not found; skipping update.")
        return
    text = PROGRESS_FILE.read_text(encoding="utf-8")
    lines = text.splitlines()
    status_map = derive_status()
    updated = update_table(lines, status_map)
    # update last updated comment
    updated.append(f"\n<!-- Last updated: {datetime.utcnow().strftime('%Y-%m-%d')} -->")
    PROGRESS_FILE.write_text("\n".join(updated), encoding="utf-8")
    print("[update_status] progress.md updated.")

if __name__ == "__main__":
    main() 
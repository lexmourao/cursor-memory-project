import os
import shutil
import sys
import textwrap
from datetime import datetime
from pathlib import Path
from typing import List

TEMPLATE_ROOT = Path(__file__).resolve().parents[1]
EXCLUDE = {".git", "backups", "benchmarks", "__pycache__"}
TIERS = {
    "1": "Cursor-only (offline)",
    "2": "Cursor + OpenAI key (no Docker)",
    "3": "Full Docker stack (TLS, Prometheus)"
}

BANNER = """
===========================
 Cursor Memory Bootstrap 🧠
===========================
"""

def prompt(msg: str) -> str:
    return input(f"{msg.strip()} ").strip()

def choose_tier() -> str:
    print("Select setup tier:")
    for k, v in TIERS.items():
        print(f"  {k}) {v}")
    while True:
        tier = prompt("Enter 1, 2, or 3:")
        if tier in TIERS:
            return tier
        print("Invalid choice.")

def copy_template(dest: Path, tier: str):
    def _ignore(dirpath: str, names: List[str]):
        ignored = set()
        for n in names:
            if n in EXCLUDE:
                ignored.add(n)
            if tier == "1" and n in {"docker-compose.yml", "Dockerfile", "nginx", "prometheus.yml"}:
                ignored.add(n)
            if tier != "3" and n in {"docker-compose.yml", "nginx", "prometheus.yml"}:
                if n not in ignored:
                    ignored.add(n)
        return ignored
    shutil.copytree(TEMPLATE_ROOT, dest, ignore=_ignore, dirs_exist_ok=True)


def init_git(dest: Path):
    if (dest / ".git").exists():
        return
    os.system(f"git init {dest}")
    os.chdir(dest)
    os.system("git add . && git commit -m 'Initial commit via bootstrap'")


def write_env(dest: Path, openai_key: str, gpg_id: str):
    if openai_key or gpg_id:
        with (dest / ".env").open("w", encoding="utf-8") as fh:
            if openai_key:
                fh.write(f"OPENAI_API_KEY={openai_key}\n")
            if gpg_id:
                fh.write(f"GPG_KEY_ID={gpg_id}\n")


def main():
    print(BANNER)
    target_dir = Path(prompt("Destination folder (will be created if missing):"))
    if target_dir.exists() and any(target_dir.iterdir()):
        print("Destination not empty; aborting.")
        sys.exit(1)
    tier = choose_tier()

    openai_key = ""
    gpg_id = ""
    if tier in {"2", "3"}:
        openai_key = prompt("Optional OPENAI_API_KEY (press Enter to skip):")
    gpg_id = prompt("GPG_KEY_ID for encrypted backups (required, press Enter to skip & disable backups):")

    print("\nCopying template…")
    copy_template(target_dir, tier)
    write_env(target_dir, openai_key, gpg_id)
    init_git(target_dir)

    # Append diary entry
    diary = target_dir / "diary/project_log.md"
    diary.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.utcnow().strftime("%Y-%m-%dT%H:%MZ")
    entry = f"\n## {now} UTC\n- **Bootstrap** – Project created from template with tier {tier} ({TIERS[tier]}).\n"
    if diary.exists():
        content = diary.read_text(encoding="utf-8")
        diary.write_text(entry + content, encoding="utf-8")
    else:
        diary.write_text(f"# Project Log\n{entry}\n", encoding="utf-8")

    print("\n✔ Project bootstrapped successfully!")
    print(textwrap.dedent(f"""
        Next steps:
        1. cd {target_dir}
        2. python -m venv .venv && source .venv/bin/activate
        3. make install
        4. {'docker compose up -d --build' if tier=='3' else 'make dev'}
    """))

if __name__ == "__main__":
    main() 
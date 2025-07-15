import argparse
from datetime import datetime
from pathlib import Path

LOG_ROOT = Path("logs")
ERRORS_DIR = LOG_ROOT / "errors"
SOLUTIONS_DIR = LOG_ROOT / "solutions"
LOG_ROOT.mkdir(exist_ok=True)
ERRORS_DIR.mkdir(exist_ok=True)
SOLUTIONS_DIR.mkdir(exist_ok=True)

def write_log(entry_type: str, message: str) -> None:
    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    fname = datetime.utcnow().strftime("%Y-%m-%d") + ".md"
    target_dir = ERRORS_DIR if entry_type == "error" else SOLUTIONS_DIR
    path = target_dir / fname
    with path.open("a", encoding="utf-8") as fh:
        fh.write(f"### {ts}\n{message}\n\n")
    print(f"[log_action] Logged {entry_type} -> {path}")

def main():
    parser = argparse.ArgumentParser(description="Log an error or solution entry.")
    parser.add_argument("--type", choices=["error", "solution"], required=True)
    parser.add_argument("--message", required=True, help="Markdown message to log")
    args = parser.parse_args()
    write_log(args.type, args.message)

if __name__ == "__main__":
    main() 
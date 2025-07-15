"""summarize_chat.py

Generates an abstractive summary of the most recent conversation turns and writes the
result to `memory-bank/activeContext.md`.

Design notes (see docs/ARCHITECTURE.md):
1. The script is invoked automatically (via cron, git hook, or manual CLI).
2. Input can be either:
   • A markdown/plain-text chat log file, OR
   • Stdin (e.g. piping cursor chat history)
3. Summary model defaults to OpenAI GPT-4o with `text-davinci-004` summarization system
   prompt. Can be swapped out for a local model via `--model`.
4. The new summary **replaces** the previous `activeContext.md` contents.
5. After writing, the file is embedded (optional) and vector DB updated (to be handled
   by `embed_active_context()` stub).

Usage examples:

    python scripts/summarize_chat.py --chat-log logs/session_2025-07-14.txt
    cat logs/current_chat.txt | python scripts/summarize_chat.py --stdin
"""

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import List
from retrieve_context import add_chunk


MEMORY_BANK_PATH = Path("memory-bank/activeContext.md")

try:
    import openai  # type: ignore
except ImportError:
    openai = None  # type: ignore[assignment]  # Will trigger fallback summarizer later


# ---------------------------- Helper functions ----------------------------- #

def read_chat_lines_from_file(path: Path, max_lines: int | None = None) -> List[str]:
    """Load the chat log file and return the most recent `max_lines` lines."""
    lines = path.read_text(encoding="utf-8").splitlines()
    return lines[-max_lines:] if max_lines else lines


def read_chat_lines_from_stdin() -> List[str]:
    """Read full stdin buffer as list of lines."""
    return sys.stdin.read().splitlines()


def call_openai_summarize(chat_lines: List[str], model: str = "gpt-3.5-turbo") -> str:
    """Summarize the chat via OpenAI ChatCompletion. Falls back to naive summary if
    the `openai` package is unavailable or the API key is missing.
    """
    if openai is None or os.getenv("OPENAI_API_KEY") is None:
        print("[summarize_chat] OpenAI not configured; using fallback summarizer.")
        return "\n".join(chat_lines[-10:])

    prompt_system = (
        "You are an expert summarization engine. Produce a concise (<= 200 words) "
        "markdown summary capturing key decisions, open questions, and next steps. "
        "Emphasize technical details needed for future context."
    )
    prompt_user = "\n".join(chat_lines)

    try:
        response = openai.ChatCompletion.create(  # type: ignore[attr-defined]
            model=model,
            messages=[
                {"role": "system", "content": prompt_system},
                {"role": "user", "content": prompt_user},
            ],
            temperature=0.3,
            max_tokens=400,
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        print(f"[summarize_chat] OpenAI request failed: {e}. Falling back to naive summary.")
        return "\n".join(chat_lines[-10:])


def embed_active_context(summary_text: str) -> None:
    """Embed the summary and update vector DB (FAISS). Placeholder for now."""
    # TODO: Add embedding code and FAISS index update.
    pass


# ----------------------------- Main routine -------------------------------- #

def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize recent chat and update activeContext.md")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--chat-log", type=Path, help="Path to chat log file")
    group.add_argument("--stdin", action="store_true", help="Read chat log from stdin")
    parser.add_argument("--max-lines", type=int, default=2000, help="Limit to last N lines of chat")
    parser.add_argument("--model", default="gpt-4o", help="OpenAI model name or local model identifier")
    parser.add_argument("--manual", action="store_true", help="Provide summary via stdin instead of model")
    args = parser.parse_args()

    # Load chat lines
    if args.stdin:
        chat_lines = read_chat_lines_from_stdin()
    else:
        chat_lines = read_chat_lines_from_file(args.chat_log, max_lines=args.max_lines)

    if not chat_lines:
        print("[summarize_chat] No chat lines provided – nothing to summarize.")
        return

    if args.manual:
        print("[summarize_chat] Enter summary text, end with EOF (Ctrl-D):")
        summary_md = sys.stdin.read().strip()
        if not summary_md:
            print("No manual summary provided. Aborting.")
            return
    else:
        summary_md = call_openai_summarize(chat_lines, model=args.model)

    # Write to activeContext.md
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    header = "# Active Context (Auto-Generated)\n\n> **Generated:** " + timestamp + "\n\n---\n\n"
    MEMORY_BANK_PATH.write_text(header + summary_md, encoding="utf-8")
    print(f"[summarize_chat] Wrote summary to {MEMORY_BANK_PATH} (length: {len(summary_md.split())} words)")

    # Embed & update vector DB (stub)
    add_chunk(summary_md, source="activeContext")


if __name__ == "__main__":
    main() 
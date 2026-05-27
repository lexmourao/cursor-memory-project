"""summarize_chat.py

CLI entry point for summarizing recent conversation turns and writing the result to
`memory-bank/activeContext.md`.

Design notes:
1. The script is invoked automatically or manually through the CLI.
2. Input can be either:
   • A markdown/plain-text chat log file, OR
   • Stdin, such as piping Cursor chat history.
3. The CLI now delegates summarization, active context writing, and optional embedding
   to `SummarizationService` so the CLI and FastAPI endpoint share the same core logic.
4. The generated summary replaces the previous `activeContext.md` contents.
5. The existing CLI workflow remains preserved while backend logic is centralized.

Usage examples:

    python scripts/summarize_chat.py --chat-log logs/session_2025-07-14.txt
    cat logs/current_chat.txt | python scripts/summarize_chat.py --stdin
    cat logs/current_chat.txt | python scripts/summarize_chat.py --stdin --no-embed
"""

import argparse
from pathlib import Path
import sys

from app.services.summarization_service import SummarizationService


def read_chat_lines_from_file(path: Path, max_lines: int | None = None) -> list[str]:
    """Load the chat log file and return the most recent `max_lines` lines."""
    lines = path.read_text(encoding="utf-8").splitlines()
    return lines[-max_lines:] if max_lines else lines


def read_chat_lines_from_stdin() -> list[str]:
    """Read full stdin buffer as list of lines."""
    return sys.stdin.read().splitlines()


def main() -> None:
    """Summarize recent chat and update activeContext.md."""
    parser = argparse.ArgumentParser(description="Summarize recent chat and update activeContext.md")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--chat-log", type=Path, help="Path to chat log file")
    group.add_argument("--stdin", action="store_true", help="Read chat log from stdin")
    parser.add_argument("--max-lines", type=int, default=2000, help="Limit to last N lines of chat")
    parser.add_argument("--model", default="gpt-4o", help="OpenAI model name or local model identifier")
    parser.add_argument("--manual", action="store_true", help="Treat provided input as the summary")
    parser.add_argument(
        "--no-embed",
        action="store_true",
        help="Write activeContext.md without embedding the summary into retrieval",
    )
    args = parser.parse_args()

    if args.stdin:
        chat_lines = read_chat_lines_from_stdin()
    else:
        chat_lines = read_chat_lines_from_file(args.chat_log, max_lines=args.max_lines)

    if not chat_lines:
        print("[summarize_chat] No chat lines provided – nothing to summarize.")
        return

    input_text = "\n".join(chat_lines).strip()
    service = SummarizationService()
    result = service.summarize(
        text=input_text,
        model=args.model,
        manual=args.manual,
        embed=not args.no_embed,
    )

    print(
        "[summarize_chat] Wrote summary to memory-bank/activeContext.md "
        f"(length: {result.word_count} words)"
    )

    if result.used_fallback:
        print("[summarize_chat] OpenAI unavailable or failed; fallback summarizer was used.")

    if result.embedded:
        print("[summarize_chat] Embedded summary into retrieval index.")
    elif args.no_embed:
        print("[summarize_chat] Skipped embedding because --no-embed was provided.")


if __name__ == "__main__":
    main()

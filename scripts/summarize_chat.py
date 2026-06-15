"""summarize_chat.py

CLI entry point for summarizing recent conversation turns and writing the result to
`memory-bank/activeContext.md`.

Design notes:
1. The script is invoked automatically or manually through the CLI.
2. Input can be either:
   • A markdown/plain-text chat log file, OR
   • Stdin, such as piping Cursor chat history.
3. The CLI preserves backward-compatible helper functions used by existing tests.
4. The CLI delegates active context writing and optional embedding to SummarizationService.
5. The generated summary replaces the previous `activeContext.md` contents.

Usage examples:

    python scripts/summarize_chat.py --chat-log logs/session_2025-07-14.txt
    cat logs/current_chat.txt | python scripts/summarize_chat.py --stdin
    cat logs/current_chat.txt | python scripts/summarize_chat.py --stdin --no-embed
"""

import argparse
import os
from pathlib import Path
import sys
from typing import Any

from app.services.summarization_service import SummarizationService

OpenAIClient: Any
try:
    from openai import OpenAI as OpenAIClient
except ImportError:
    OpenAIClient = None


def read_chat_lines_from_file(path: Path, max_lines: int | None = None) -> list[str]:
    """Load the chat log file and return the most recent `max_lines` lines."""
    lines = path.read_text(encoding="utf-8").splitlines()
    return lines[-max_lines:] if max_lines else lines


def read_chat_lines_from_stdin() -> list[str]:
    """Read full stdin buffer as list of lines."""
    return sys.stdin.read().splitlines()


def call_openai_summarize(chat_lines: list[str], model: str = "gpt-4o") -> str:
    """Summarize chat lines through OpenAI when configured, otherwise use fallback.

    This function is intentionally preserved for existing tests and scripts that
    monkeypatch or import it directly.
    """
    if OpenAIClient is None or os.getenv("OPENAI_API_KEY") is None:
        print("[summarize_chat] OpenAI not configured; using fallback summarizer.")
        return "\n".join(chat_lines[-10:])

    prompt_system = (
        "You are an expert summarization engine. Produce a concise (<= 200 words) "
        "markdown summary capturing key decisions, open questions, and next steps. "
        "Emphasize technical details needed for future context."
    )
    prompt_user = "\n".join(chat_lines)

    try:
        client = OpenAIClient()
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": prompt_system},
                {"role": "user", "content": prompt_user},
            ],
            temperature=0.3,
            max_tokens=400,
        )
        content = response.choices[0].message.content or ""
        return content.strip()
    except Exception as exc:
        print(
            f"[summarize_chat] OpenAI request failed: {exc}. Falling back to naive summary."
        )
        return "\n".join(chat_lines[-10:])


def main() -> None:
    """Summarize recent chat and update activeContext.md."""
    parser = argparse.ArgumentParser(
        description="Summarize recent chat and update activeContext.md"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--chat-log", type=Path, help="Path to chat log file")
    group.add_argument("--stdin", action="store_true", help="Read chat log from stdin")
    parser.add_argument(
        "--max-lines", type=int, default=2000, help="Limit to last N lines of chat"
    )
    parser.add_argument(
        "--model", default="gpt-4o", help="OpenAI model name or local model identifier"
    )
    parser.add_argument(
        "--manual", action="store_true", help="Treat provided input as the summary"
    )
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

    if args.manual:
        summary_md = "\n".join(chat_lines).strip()
    else:
        summary_md = call_openai_summarize(chat_lines, model=args.model)

    if not summary_md:
        print("[summarize_chat] Empty summary generated – nothing to write.")
        return

    service = SummarizationService()
    result = service.summarize(
        text=summary_md,
        model=args.model,
        manual=True,
        embed=not args.no_embed,
    )

    print(
        "[summarize_chat] Wrote summary to memory-bank/activeContext.md "
        f"(length: {result.word_count} words)"
    )

    if result.embedded:
        print("[summarize_chat] Embedded summary into retrieval index.")
    elif args.no_embed:
        print("[summarize_chat] Skipped embedding because --no-embed was provided.")


if __name__ == "__main__":
    main()

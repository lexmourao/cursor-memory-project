"""CLI compatibility tests for scripts/summarize_chat.py."""

from pathlib import Path
import io
import sys

import pytest

import scripts.summarize_chat as summarize_chat


def test_summarize_chat_cli_file_input_preserves_legacy_summary_helper(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """CLI file input should keep legacy summary helper compatibility."""
    active_context_file = tmp_path / "activeContext.md"
    chat_log = tmp_path / "chat.txt"

    chat_log.write_text(
        "Line one\nLine two\nLine three\n",
        encoding="utf-8",
    )

    monkeypatch.setenv("MEMORY_BANK_DIR", str(tmp_path))
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "summarize_chat.py",
            "--chat-log",
            str(chat_log),
            "--max-lines",
            "2",
            "--no-embed",
        ],
    )

    summarize_chat.main()

    output = capsys.readouterr().out
    written_text = active_context_file.read_text(encoding="utf-8")

    assert active_context_file.exists()
    assert "# Active Context (Auto-Generated)" in written_text
    assert "FAKE SUMMARY GENERATED FOR TESTING" in written_text
    assert "[summarize_chat] Wrote summary to memory-bank/activeContext.md" in output
    assert (
        "[summarize_chat] Skipped embedding because --no-embed was provided." in output
    )


def test_summarize_chat_cli_manual_stdin_writes_active_context(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """CLI manual stdin mode should write provided text as active context."""
    active_context_file = tmp_path / "activeContext.md"

    monkeypatch.setenv("MEMORY_BANK_DIR", str(tmp_path))
    monkeypatch.setattr(sys, "stdin", io.StringIO("Manual summary\nSecond line"))
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "summarize_chat.py",
            "--stdin",
            "--manual",
            "--no-embed",
        ],
    )

    summarize_chat.main()

    output = capsys.readouterr().out
    written_text = active_context_file.read_text(encoding="utf-8")

    assert active_context_file.exists()
    assert "# Active Context (Auto-Generated)" in written_text
    assert "Manual summary" in written_text
    assert "Second line" in written_text
    assert "[summarize_chat] Wrote summary to memory-bank/activeContext.md" in output
    assert (
        "[summarize_chat] Skipped embedding because --no-embed was provided." in output
    )


def test_summarize_chat_cli_empty_stdin_does_not_write_active_context(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """CLI should exit safely when stdin input is empty."""
    active_context_file = tmp_path / "activeContext.md"

    monkeypatch.setenv("MEMORY_BANK_DIR", str(tmp_path))
    monkeypatch.setattr(sys, "stdin", io.StringIO(""))
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "summarize_chat.py",
            "--stdin",
            "--no-embed",
        ],
    )

    summarize_chat.main()

    output = capsys.readouterr().out

    assert not active_context_file.exists()
    assert "[summarize_chat] No chat lines provided – nothing to summarize." in output


def test_call_openai_summarize_legacy_helper_remains_available() -> None:
    """Legacy call_openai_summarize helper should remain importable and callable."""
    summary = summarize_chat.call_openai_summarize(
        ["Line one", "Line two"], model="gpt-test"
    )

    assert summary == "FAKE SUMMARY GENERATED FOR TESTING"

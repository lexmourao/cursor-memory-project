"""API tests for backend summarization endpoint."""

from pathlib import Path

from fastapi.testclient import TestClient
import pytest

from app.main import app

client = TestClient(app)


def test_summarization_endpoint_manual_mode(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Summarization endpoint should accept manual summaries and write active context."""
    monkeypatch.setenv("MEMORY_BANK_DIR", str(tmp_path))
    active_context_file = tmp_path / "activeContext.md"

    response = client.post(
        "/summarization/summarize",
        json={
            "text": "Manual summary for the current backend slice.",
            "model": "gpt-4o",
            "manual": True,
            "embed": False,
        },
    )

    assert response.status_code == 200

    payload = response.json()
    assert payload["summary"] == "Manual summary for the current backend slice."
    assert payload["word_count"] == 7
    assert payload["model"] == "gpt-4o"
    assert payload["used_fallback"] is False
    assert payload["wrote_active_context"] is True
    assert payload["embedded"] is False

    assert active_context_file.exists()
    written_text = active_context_file.read_text(encoding="utf-8")
    assert "# Active Context (Auto-Generated)" in written_text
    assert "Manual summary for the current backend slice." in written_text


def test_summarization_endpoint_fallback_mode(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Summarization endpoint should use fallback mode when OpenAI is unavailable."""
    monkeypatch.setenv("MEMORY_BANK_DIR", str(tmp_path))
    active_context_file = tmp_path / "activeContext.md"

    import app.services.summarization_service as summarization_service

    monkeypatch.setattr(summarization_service, "OpenAIClient", None)

    response = client.post(
        "/summarization/summarize",
        json={
            "text": "Line one\nLine two\nLine three",
            "model": "gpt-4o",
            "manual": False,
            "embed": False,
        },
    )

    assert response.status_code == 200

    payload = response.json()
    assert payload["summary"] == "Line one\nLine two\nLine three"
    assert payload["word_count"] == 6
    assert payload["model"] == "gpt-4o"
    assert payload["used_fallback"] is True
    assert payload["wrote_active_context"] is True
    assert payload["embedded"] is False

    assert active_context_file.exists()


def test_summarization_respects_memory_bank_dir_setting(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Summarization should write activeContext.md under MEMORY_BANK_DIR."""
    memory_bank_dir = tmp_path / "custom-memory-bank"
    memory_bank_dir.mkdir()
    monkeypatch.setenv("MEMORY_BANK_DIR", str(memory_bank_dir))

    response = client.post(
        "/summarization/summarize",
        json={
            "text": "Custom memory bank path test.",
            "model": "gpt-4o",
            "manual": True,
            "embed": False,
        },
    )

    assert response.status_code == 200

    active_context_file = memory_bank_dir / "activeContext.md"
    assert active_context_file.exists()
    written_text = active_context_file.read_text(encoding="utf-8")
    assert "Custom memory bank path test." in written_text


def test_summarization_endpoint_rejects_empty_text() -> None:
    """Summarization endpoint should reject empty text."""
    response = client.post(
        "/summarization/summarize",
        json={
            "text": "",
            "model": "gpt-4o",
            "manual": True,
            "embed": False,
        },
    )

    assert response.status_code == 422

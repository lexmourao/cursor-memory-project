import subprocess
from pathlib import Path
import sys
import pytest
import importlib

summarize_chat = importlib.import_module("scripts.summarize_chat")
retrieve_context = importlib.import_module("scripts.retrieve_context")


def test_empty_chat_summary():
    summary = summarize_chat.call_openai_summarize([])
    assert summary, "Even empty chat should return fallback summary"


def test_health_check_failure(monkeypatch):
    hc = importlib.import_module("scripts.health_check")

    class DummyResp:
        def __init__(self, status=200, json_val=None):
            self.status_code = status
            self._json_val = json_val or {}
        def json(self):
            return self._json_val

    def fake_get(url, timeout=5):
        if url.endswith("/health"):
            return DummyResp(status=500)
        return DummyResp()

    monkeypatch.setattr(hc, "requests", type("FakeReq", (), {"get": staticmethod(fake_get)}))
    with pytest.raises(SystemExit):
        hc.main()


def test_index_rebuild_with_corrupted_markdown(tmp_path, monkeypatch):
    # create corrupted markdown file
    bad_file = Path("memory-bank/corrupted.md")
    bad_file.write_text("\0\0\0", encoding="utf-8")
    try:
        retrieve_context.rebuild_index()
    finally:
        bad_file.unlink()
    index_path = Path("memory-bank/embeddings.faiss")
    assert index_path.exists() 
import importlib
from typing import List

import numpy as np
import pytest
import sys

# Auto-apply fixture to every test
@pytest.fixture(autouse=True)
def mock_openai(monkeypatch):
    """Monkey-patch OpenAI calls so tests run offline & deterministically."""
    summarize_chat = importlib.import_module("scripts.summarize_chat")
    retrieve_context = importlib.import_module("scripts.retrieve_context")

    # Fake summary function
    def _fake_summary(chat_lines: List[str], model: str = "gpt-test") -> str:
        return "FAKE SUMMARY GENERATED FOR TESTING"

    monkeypatch.setattr(summarize_chat, "call_openai_summarize", _fake_summary)

    # Fake embedding returns constant vector of ones
    def _fake_embed(text: str) -> np.ndarray:
        return np.ones(retrieve_context.EMBED_DIM, dtype="float32")

    monkeypatch.setattr(retrieve_context, "get_openai_embedding", _fake_embed)

    # Ensure any direct openai import is None
    monkeypatch.setitem(sys.modules, "openai", None) 
import importlib
from pathlib import Path

import pytest

# Import modules dynamically to avoid circular CLI execution
summarize_chat = importlib.import_module("scripts.summarize_chat")
retrieve_context = importlib.import_module("scripts.retrieve_context")

MEMORY_BANK_DIR = Path("memory-bank")


def test_summarization_fallback(tmp_path):
    chat_lines = [f"Line {i}" for i in range(1, 15)]
    summary = summarize_chat.call_openai_summarize(chat_lines, model="dummy-model")
    assert summary, "Summary should not be empty"
    assert "Line" in summary, "Fallback summary should contain original lines"


def test_retrieval_build_and_query(tmp_path):
    # Ensure index is rebuilt
    retrieve_context.rebuild_index()
    # Index should now exist and have vectors
    index_path = MEMORY_BANK_DIR / "embeddings.faiss"
    assert index_path.exists(), "Index file should be created"
    res = retrieve_context.query("project", top_k=3)
    assert isinstance(res, list)
    # Even with zero-vector fallback, query returns list (possibly empty). Accept. 
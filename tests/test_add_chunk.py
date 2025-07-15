import importlib
from pathlib import Path

retrieve_context = importlib.import_module("scripts.retrieve_context")


def test_add_chunk_increments_index(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (Path("memory-bank")).mkdir()
    # initial rebuild no chunks
    retrieve_context.rebuild_index()
    # add chunk
    retrieve_context.add_chunk("test chunk")
    # ensure index file exists and not empty
    idx_path = tmp_path / "memory-bank" / "embeddings.faiss"
    assert idx_path.exists()
    # Size >0
    assert idx_path.stat().st_size > 0 
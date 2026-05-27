"""API tests for backend retrieval endpoint."""

import json
from pathlib import Path

from fastapi.testclient import TestClient
import pytest

from app.main import app
import scripts.retrieve_context as retrieve_context


client = TestClient(app)


def test_retrieval_query_endpoint_returns_response_shape() -> None:
    """Retrieval endpoint should return the query and a results list."""
    response = client.post(
        "/retrieval/query",
        json={"query": "What is the project architecture?", "top_k": 5},
    )

    assert response.status_code == 200

    payload = response.json()
    assert payload["query"] == "What is the project architecture?"
    assert "results" in payload
    assert isinstance(payload["results"], list)

    for result in payload["results"]:
        assert "score" in result
        assert "source" in result
        assert "chunk_idx" in result
        assert "text" in result
        assert isinstance(result["score"], float)
        assert isinstance(result["source"], str)
        assert isinstance(result["chunk_idx"], int)
        assert isinstance(result["text"], str)


def test_retrieval_query_endpoint_returns_indexed_memory_after_rebuild(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Retrieval endpoint should return indexed memory after rebuilding an index."""
    memory_bank = tmp_path / "memory-bank"
    memory_bank.mkdir()

    memory_file = memory_bank / "projectbrief.md"
    memory_file.write_text(
        "Project vision: build a local-first Cursor memory backend.\n\n"
        "Architecture note: FastAPI exposes memory and retrieval endpoints.",
        encoding="utf-8",
    )

    monkeypatch.setattr(retrieve_context, "MEMORY_BANK_DIR", memory_bank)
    monkeypatch.setattr(retrieve_context, "INDEX_FILE", tmp_path / "test.faiss")
    monkeypatch.setattr(retrieve_context, "META_FILE", tmp_path / "test_meta.pkl")

    retrieve_context.rebuild_index()

    response = client.post(
        "/retrieval/query",
        json={"query": "local-first Cursor memory backend", "top_k": 1},
    )

    assert response.status_code == 200

    payload = response.json()
    assert payload["query"] == "local-first Cursor memory backend"
    assert len(payload["results"]) == 1

    result = payload["results"][0]
    assert result["source"] == "projectbrief.md"
    assert result["chunk_idx"] == 0
    assert "local-first Cursor memory backend" in result["text"]
    assert isinstance(result["score"], float)


def test_retrieval_metadata_json_export(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Metadata export should create inspectable JSON without replacing pickle runtime metadata."""
    memory_bank = tmp_path / "memory-bank"
    memory_bank.mkdir()

    memory_file = memory_bank / "projectbrief.md"
    memory_file.write_text(
        "Project vision: build a local-first Cursor memory backend.\n\n"
        "Architecture note: FastAPI exposes memory and retrieval endpoints.",
        encoding="utf-8",
    )

    index_file = tmp_path / "test.faiss"
    meta_file = tmp_path / "test_meta.pkl"
    json_file = tmp_path / "test_meta.json"

    monkeypatch.setattr(retrieve_context, "MEMORY_BANK_DIR", memory_bank)
    monkeypatch.setattr(retrieve_context, "INDEX_FILE", index_file)
    monkeypatch.setattr(retrieve_context, "META_FILE", meta_file)
    monkeypatch.setattr(retrieve_context, "META_JSON_FILE", json_file)

    retrieve_context.rebuild_index()
    exported_path = retrieve_context.export_metadata_json()

    assert exported_path == json_file
    assert meta_file.exists()
    assert json_file.exists()

    payload = json.loads(json_file.read_text(encoding="utf-8"))

    assert payload["schema_version"] == 1
    assert payload["source"] == str(meta_file)
    assert payload["index_file"] == str(index_file)
    assert payload["record_count"] == 2
    assert len(payload["records"]) == 2

    first_record = payload["records"][0]
    assert first_record["file"] == "projectbrief.md"
    assert first_record["chunk_idx"] == 0
    assert "local-first Cursor memory backend" in first_record["text"]


def test_retrieval_query_endpoint_handles_missing_index(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Retrieval endpoint should return an empty result list if no index exists."""
    monkeypatch.setattr(retrieve_context, "INDEX_FILE", tmp_path / "missing.faiss")
    monkeypatch.setattr(retrieve_context, "META_FILE", tmp_path / "missing_meta.pkl")

    response = client.post(
        "/retrieval/query",
        json={"query": "What is the project architecture?", "top_k": 5},
    )

    assert response.status_code == 200

    payload = response.json()
    assert payload["query"] == "What is the project architecture?"
    assert payload["results"] == []


def test_retrieval_query_endpoint_handles_empty_index(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Retrieval endpoint should return an empty result list if the index is empty."""
    index_file = tmp_path / "empty.faiss"
    meta_file = tmp_path / "empty_meta.pkl"

    empty_index = retrieve_context.faiss.IndexFlatIP(retrieve_context.EMBED_DIM)
    retrieve_context.faiss.write_index(empty_index, str(index_file))

    monkeypatch.setattr(retrieve_context, "INDEX_FILE", index_file)
    monkeypatch.setattr(retrieve_context, "META_FILE", meta_file)

    response = client.post(
        "/retrieval/query",
        json={"query": "What is the project architecture?", "top_k": 5},
    )

    assert response.status_code == 200

    payload = response.json()
    assert payload["query"] == "What is the project architecture?"
    assert payload["results"] == []


def test_retrieval_query_endpoint_rejects_empty_query() -> None:
    """Retrieval endpoint should reject empty query text."""
    response = client.post(
        "/retrieval/query",
        json={"query": "", "top_k": 5},
    )

    assert response.status_code == 422


def test_retrieval_query_endpoint_rejects_invalid_top_k_low() -> None:
    """Retrieval endpoint should reject top_k values below the allowed range."""
    response = client.post(
        "/retrieval/query",
        json={"query": "memory", "top_k": 0},
    )

    assert response.status_code == 422


def test_retrieval_query_endpoint_rejects_invalid_top_k_high() -> None:
    """Retrieval endpoint should reject top_k values above the allowed range."""
    response = client.post(
        "/retrieval/query",
        json={"query": "memory", "top_k": 21},
    )

    assert response.status_code == 422

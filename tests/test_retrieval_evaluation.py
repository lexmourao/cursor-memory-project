"""Deterministic retrieval evaluation tests.

These tests evaluate retrieval wiring, fixture indexing, and metadata traceability
under controlled deterministic test embeddings. They do not evaluate OpenAI
embedding quality, do not make network calls, and do not claim semantic ranking
quality for production embedding services.
"""

from __future__ import annotations

import shutil
from pathlib import Path

import numpy as np
import pytest

import scripts.retrieve_context as retrieve_context
from app.services.retrieval_service import RetrievalService

FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures" / "retrieval_eval"

# Fixed unit-vector slots keep top-1 retrieval stable under IndexFlatIP.
_TOPIC_SLOTS: dict[str, int] = {
    "fastapi architecture": 42,
    "service modules": 43,
    "local api token": 84,
    "wildcard cors": 85,
    "faiss retrieval index": 126,
    "metadata traceability": 127,
}


def _deterministic_embed(text: str) -> np.ndarray:
    """Map chunk or query text to a stable unit vector for evaluation only."""
    vec = np.zeros(retrieve_context.EMBED_DIM, dtype="float32")
    normalized = " ".join(text.lower().split())

    for phrase, slot in _TOPIC_SLOTS.items():
        if phrase in normalized:
            vec[slot] = 1.0
            return vec

    fallback = abs(hash(normalized)) % 200
    vec[fallback] = 1.0
    return vec


@pytest.fixture
def eval_retrieval_env(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> Path:
    """Isolate retrieval paths and copy evaluation fixtures into a temp memory bank."""
    memory_bank = tmp_path / "memory-bank"
    memory_bank.mkdir()
    shutil.copytree(FIXTURE_DIR, memory_bank, dirs_exist_ok=True)

    monkeypatch.setattr(retrieve_context, "MEMORY_BANK_DIR", memory_bank)
    monkeypatch.setattr(retrieve_context, "INDEX_FILE", tmp_path / "eval.faiss")
    monkeypatch.setattr(retrieve_context, "META_FILE", tmp_path / "eval_meta.pkl")
    monkeypatch.setattr(retrieve_context, "META_JSON_FILE", tmp_path / "eval_meta.json")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setattr(retrieve_context, "get_openai_embedding", _deterministic_embed)

    retrieve_context.rebuild_index()
    return memory_bank


GOLDEN_CASES = [
    (
        "What is the FastAPI architecture layers setup?",
        "architecture.md",
        0,
        "FastAPI architecture layers",
    ),
    (
        "Where are service modules defined?",
        "architecture.md",
        1,
        "Service modules separate",
    ),
    (
        "How does local API token protection work?",
        "security.md",
        0,
        "Local API token protection",
    ),
    (
        "Is wildcard CORS enabled by default?",
        "security.md",
        1,
        "Wildcard CORS is disabled",
    ),
    (
        "Explain the FAISS retrieval index rebuild flow.",
        "retrieval.md",
        0,
        "FAISS retrieval index",
    ),
    (
        "What metadata traceability fields are stored?",
        "retrieval.md",
        1,
        "Metadata traceability records",
    ),
]


@pytest.mark.parametrize(
    ("query", "expected_source", "expected_chunk_idx", "expected_substring"),
    GOLDEN_CASES,
)
def test_golden_query_returns_expected_top_result(
    eval_retrieval_env: Path,
    query: str,
    expected_source: str,
    expected_chunk_idx: int,
    expected_substring: str,
) -> None:
    """Deterministic top-1 retrieval should return the expected source and chunk."""
    results = retrieve_context.query_with_metadata(query, top_k=1)

    assert len(results) >= 1
    top = results[0]
    assert top["file"] == expected_source
    assert top["chunk_idx"] == expected_chunk_idx
    assert expected_substring in top["text"]
    assert isinstance(top["score"], float)


def test_evaluation_index_contains_all_fixture_chunks(
    eval_retrieval_env: Path,
) -> None:
    """Fixture rebuild should index two chunks from each evaluation markdown file."""
    meta = retrieve_context._load_meta()

    assert len(meta) == 6
    assert {record["file"] for record in meta} == {
        "architecture.md",
        "security.md",
        "retrieval.md",
    }


def test_results_include_traceability_fields(eval_retrieval_env: Path) -> None:
    """Every retrieval match should expose source, chunk index, text, and score."""
    results = retrieve_context.query_with_metadata("FAISS retrieval index", top_k=3)

    assert results
    for match in results:
        assert isinstance(match["file"], str)
        assert isinstance(match["chunk_idx"], int)
        assert isinstance(match["text"], str)
        assert isinstance(match["score"], float)


def test_retrieval_service_returns_typed_results(eval_retrieval_env: Path) -> None:
    """RetrievalService should preserve metadata traceability from the script layer."""
    service = RetrievalService()
    results = service.query("local API token protection", top_k=1)

    assert len(results) == 1
    result = results[0]
    assert result.source == "security.md"
    assert result.chunk_idx == 0
    assert "Local API token protection" in result.text
    assert isinstance(result.score, float)


def test_status_reports_zero_vector_fallback_without_api_key(
    eval_retrieval_env: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Evaluation fixtures run without OpenAI and should report fallback embedding mode."""
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    status = RetrievalService().status()

    assert status.ready is True
    assert status.embedding_mode == "zero_vector_fallback"

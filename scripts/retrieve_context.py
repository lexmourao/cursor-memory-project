import argparse
import os
import pickle
from pathlib import Path
from typing import List, Tuple
import sys

import numpy as np

try:
    import faiss  # type: ignore
except ImportError as e:
    raise SystemExit("faiss is required. Install faiss-cpu via pip.") from e

try:
    import openai  # type: ignore
except ImportError:
    openai = None  # type: ignore[assignment]

MEMORY_BANK_DIR = Path("memory-bank")
INDEX_FILE = MEMORY_BANK_DIR / "embeddings.faiss"
META_FILE = MEMORY_BANK_DIR / "embeddings_meta.pkl"
EMBED_MODEL = "text-embedding-3-small"
EMBED_DIM = 1536  # per OpenAI docs for model above

def get_openai_embedding(text: str) -> np.ndarray:
    """Return embedding vector (np.float32). Falls back to zeros if unavailable."""
    if openai is None or os.getenv("OPENAI_API_KEY") is None:
        # fallback zero vector
        return np.zeros(EMBED_DIM, dtype="float32")
    response = openai.Embedding.create(input=[text], model=EMBED_MODEL)  # type: ignore[attr-defined]
    vec = np.array(response["data"][0]["embedding"], dtype="float32")
    return vec


def _load_meta() -> List[dict]:
    if META_FILE.exists():
        with META_FILE.open("rb") as fh:
            return pickle.load(fh)
    return []


def _save_meta(meta: List[dict]) -> None:
    with META_FILE.open("wb") as fh:
        pickle.dump(meta, fh)


def _init_index() -> faiss.IndexFlatIP:
    if INDEX_FILE.exists():
        index = faiss.read_index(str(INDEX_FILE))
    else:
        index = faiss.IndexFlatIP(EMBED_DIM)
    return index


def _save_index(index: faiss.IndexFlatIP) -> None:
    faiss.write_index(index, str(INDEX_FILE))

# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def rebuild_index() -> None:
    """Embed all markdown files in memory-bank and rebuild FAISS index."""
    index = faiss.IndexFlatIP(EMBED_DIM)
    meta: List[dict] = []

    md_files = sorted(MEMORY_BANK_DIR.glob("*.md"))
    for fp in md_files:
        text = fp.read_text(encoding="utf-8")
        chunks = [p.strip() for p in text.split("\n\n") if p.strip()]
        for idx, chunk in enumerate(chunks):
            vec = get_openai_embedding(chunk)
            index.add(vec.reshape(1, -1))
            meta.append({"file": fp.name, "chunk_idx": idx, "text": chunk})
    _save_index(index)
    _save_meta(meta)
    print(f"[retrieve_context] Rebuilt index with {index.ntotal} vectors from {len(md_files)} files.")


def add_chunk(text: str, source: str = "activeContext") -> None:
    """Embed a new chunk and append to existing index."""
    index = _init_index()
    meta = _load_meta()

    vec = get_openai_embedding(text)
    index.add(vec.reshape(1, -1))
    meta.append({"file": source, "chunk_idx": len(meta), "text": text})

    _save_index(index)
    _save_meta(meta)


def query(text: str, top_k: int = 5) -> List[Tuple[float, str]]:
    """Return list of (score, chunk_text) for top_k matches."""
    index = _init_index()
    meta = _load_meta()
    if index.ntotal == 0:
        print("[retrieve_context] Index empty. Rebuild index first.")
        return []

    qvec = get_openai_embedding(text).reshape(1, -1)
    scores, ids = index.search(qvec, top_k)
    results: List[Tuple[float, str]] = []
    for score, idx in zip(scores[0], ids[0]):
        if idx == -1:
            continue
        results.append((float(score), meta[idx]["text"]))
    return results

# ---------------------------------------------------------------------------
# CLI Interface
# ---------------------------------------------------------------------------

def _cli() -> None:
    parser = argparse.ArgumentParser(description="Context retrieval over Memory Bank")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # cmd_rebuild = sub.add_parser("rebuild", help="Rebuild vector index from scratch")

    cmd_add = sub.add_parser("add", help="Add a new chunk to the index (stdin)")
    cmd_add.add_argument("--source", default="activeContext", help="Source label for chunk")

    cmd_query = sub.add_parser("query", help="Query context")
    cmd_query.add_argument("--text", help="Query text (if omitted, read from stdin)")
    cmd_query.add_argument("--top-k", type=int, default=5)

    args = parser.parse_args()

    if args.cmd == "rebuild":
        rebuild_index()
    elif args.cmd == "add":
        chunk_text = sys.stdin.read().strip()
        if not chunk_text:
            print("Provide chunk text via stdin.")
            return
        add_chunk(chunk_text, source=args.source)
        print("[retrieve_context] Chunk added to index.")
    elif args.cmd == "query":
        qtext = args.text or sys.stdin.read().strip()
        if not qtext:
            print("Provide query text via --text or stdin.")
            return
        results = query(qtext, top_k=args.top_k)
        for score, chunk in results:
            print(f"--- score: {score:.3f}\n{chunk}\n")

if __name__ == "__main__":
    _cli() 
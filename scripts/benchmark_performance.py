import time
import argparse
from pathlib import Path
import random
import string
import json
import subprocess

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MEMORY_BANK = PROJECT_ROOT / "memory-bank"
RESULTS_DIR = PROJECT_ROOT / "benchmarks"
RESULTS_DIR.mkdir(exist_ok=True)


def random_sentence(n: int = 12) -> str:
    return " ".join(random.choice(string.ascii_lowercase) for _ in range(n))


def generate_chunks(count: int) -> None:
    synthetic = MEMORY_BANK / "synthetic.md"
    with synthetic.open("w", encoding="utf-8") as fh:
        for _ in range(count):
            fh.write(random_sentence(20) + "\n\n")


def run_benchmark(chunk_count: int, output_file: Path):
    generate_chunks(chunk_count)

    # Measure rebuild index time
    start = time.perf_counter()
    subprocess.check_call(["python", "scripts/retrieve_context.py", "rebuild"], cwd=PROJECT_ROOT, stdout=subprocess.DEVNULL)
    rebuild_sec = time.perf_counter() - start

    # Measure single query
    import requests, subprocess as sp

    q_start = time.perf_counter()
    subprocess.check_call(["python", "scripts/retrieve_context.py", "query", "--text", "test"], cwd=PROJECT_ROOT, stdout=subprocess.DEVNULL)
    query_sec = time.perf_counter() - q_start

    # store JSON
    output_file.write_text(json.dumps({"chunks": chunk_count, "rebuild_sec": rebuild_sec, "query_sec": query_sec}, indent=2))
    print(f"[benchmark] chunks={chunk_count} rebuild={rebuild_sec:.2f}s query={query_sec:.2f}s saved to {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--chunks", type=int, default=10000)
    args = parser.parse_args()
    out = RESULTS_DIR / f"benchmark_{args.chunks}.json"
    run_benchmark(args.chunks, out) 
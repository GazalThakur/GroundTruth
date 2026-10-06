#!/usr/bin/env python3
"""Sample real Indian SC judgments, extract text, chunk, write candidate corpus.

Usage:
    python scripts/sample_indian_sc.py --year 2023 --n 15 --chunk-size 800
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from groundtruth.indian_sc import passages_from_sample
from groundtruth.schema import save_corpus


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", type=int, default=2023)
    parser.add_argument("--n", type=int, default=15, help="number of judgments")
    parser.add_argument("--chunk-size", type=int, default=800)
    parser.add_argument("--overlap", type=int, default=100)
    parser.add_argument(
        "--out",
        default="data/golden/candidates_corpus_batch_01.jsonl",
        help="candidate passages for human review (not the golden corpus yet)",
    )
    args = parser.parse_args()

    print(f"Sampling {args.n} judgments from year={args.year} ...")
    passages = passages_from_sample(
        year=args.year,
        n_judgments=args.n,
        chunk_size=args.chunk_size,
        overlap=args.overlap,
    )
    save_corpus(passages, args.out)
    print(f"Wrote {len(passages)} passages → {args.out}")
    print("Next: review passages, write queries, human-approve into corpus.jsonl + seed.jsonl")


if __name__ == "__main__":
    main()
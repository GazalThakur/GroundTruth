#!/usr/bin/env python3
"""Run retrieval evaluation on the v1 span-labeled golden set.

Examples:
  python scripts/run_eval.py
  python scripts/run_eval.py --mode hybrid --rerank --chunk-size 800
  python scripts/run_eval.py --chunk-size 400 --out results/chunk400.json
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

# project root on path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from groundtruth.eval import run_from_config, print_results, save_results
from groundtruth.factory import load_config


def main() -> None:
    ap = argparse.ArgumentParser(description="Groundtruth retrieval eval (span gold)")
    ap.add_argument("--config", default="config.yaml")
    ap.add_argument("--mode", choices=["dense", "hybrid", "bm25"], default=None)
    ap.add_argument("--rerank", action="store_true", default=None)
    ap.add_argument("--no-rerank", action="store_true")
    ap.add_argument("--chunk-size", type=int, default=None)
    ap.add_argument("--chunk-overlap", type=int, default=None)
    ap.add_argument("--top-k", type=int, default=None)
    ap.add_argument("--out", default=None, help="Write full results JSON")
    args = ap.parse_args()

    cfg = load_config(args.config)
    ret = cfg.setdefault("retrieval", {})

    if args.mode is not None:
        ret["mode"] = args.mode
    if args.rerank:
        ret["rerank"] = True
    if args.no_rerank:
        ret["rerank"] = False
    if args.chunk_size is not None:
        ret["chunk_size"] = args.chunk_size
    if args.chunk_overlap is not None:
        ret["chunk_overlap"] = args.chunk_overlap
    if args.top_k is not None:
        ret["top_k"] = args.top_k

    results = run_from_config(cfg)
    print_results(results)

    out = args.out
    if out is None:
        mode = ret.get("mode", "dense")
        cs = ret.get("chunk_size", 800)
        rr = "rerank" if ret.get("rerank") else "norerank"
        out = f"results/eval_{mode}_c{cs}_{rr}.json"
    save_results(results, out)
    print(f"\nFull results written to {out}")


if __name__ == "__main__":
    main()

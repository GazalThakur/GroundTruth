#!/usr/bin/env python3
"""CI regression gate for Groundtruth.

Fails (exit 1) when recall@10 drops by more than THRESHOLD relative to the
locked baseline in results/baseline.json.

Usage:
    # Run eval + gate (default: dense, no rerank — matches baseline)
    python scripts/ci_gate.py

    # Gate only against an existing results file
    python scripts/ci_gate.py --results results/dense_seed.json

    # Update the locked baseline after a confirmed improvement
    python scripts/ci_gate.py --update-baseline

    # Stricter / looser threshold
    python scripts/ci_gate.py --threshold 0.01
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from groundtruth.eval import run_from_config, save_results
from groundtruth.factory import load_config
import yaml

BASELINE_PATH = ROOT / "results" / "baseline.json"
DEFAULT_THRESHOLD = 0.01  # 1 point of recall@10


def load_baseline(path: Path = BASELINE_PATH) -> dict:
    if not path.exists():
        print(f"ERROR: baseline not found at {path}")
        print("Create one with: python scripts/ci_gate.py --update-baseline")
        sys.exit(2)
    with path.open() as f:
        return json.load(f)


def run_eval_matching_baseline(baseline: dict, config_path: str = "config.yaml") -> dict:
    """Run eval with the same mode/rerank settings the baseline used."""
    cfg = load_config(config_path)
    ret = cfg.setdefault("retrieval", {})
    base_cfg = baseline.get("config", {})
    ret["mode"] = base_cfg.get("mode", "dense")
    ret["rerank"] = base_cfg.get("rerank", False)
    ret["top_k"] = base_cfg.get("top_k", 10)

    tmp = Path("/tmp/gt_ci_config.yaml")
    with tmp.open("w") as f:
        yaml.dump(cfg, f)

    print(f"Running eval: mode={ret['mode']}  rerank={ret['rerank']}")
    return run_from_config(cfg=cfg)


def check_gate(
    current_metrics: dict,
    baseline_metrics: dict,
    threshold: float = DEFAULT_THRESHOLD,
    metric: str = "recall@10",
) -> tuple[bool, str]:
    """
    Return (passed, message).
    Fail when current[metric] < baseline[metric] - threshold.
    """
    base_val = baseline_metrics.get(metric)
    curr_val = current_metrics.get(metric)
    if base_val is None or curr_val is None:
        return False, f"Missing metric '{metric}' in baseline or current results"

    drop = base_val - curr_val
    if drop > threshold:
        msg = (
            f"GATE FAILED: {metric} dropped by {drop:.4f} "
            f"(baseline={base_val:.4f}, current={curr_val:.4f}, "
            f"threshold={threshold:.4f})"
        )
        return False, msg

    msg = (
        f"GATE PASSED: {metric}={curr_val:.4f} "
        f"(baseline={base_val:.4f}, drop={drop:.4f}, threshold={threshold:.4f})"
    )
    return True, msg


def update_baseline(results: dict, path: Path = BASELINE_PATH) -> None:
    """Write current results as the new locked baseline."""
    payload = {
        "description": "Locked baseline for CI regression gate. Update deliberately after a confirmed improvement.",
        "pipeline": results.get("pipeline", "unknown"),
        "config": {
            "mode": "dense",  # will be overwritten by caller if known
            "rerank": False,
            "top_k": results.get("top_k", 10),
        },
        "n_queries": results.get("n_queries"),
        "n_corpus": results.get("n_corpus"),
        "metrics": results.get("aggregate", {}),
        "notes": "Updated via scripts/ci_gate.py --update-baseline",
    }
    # Try to infer mode/rerank from pipeline name
    name = results.get("pipeline", "")
    if "hybrid" in name:
        payload["config"]["mode"] = "hybrid"
    elif "bm25" in name and "dense" not in name:
        payload["config"]["mode"] = "bm25"
    else:
        payload["config"]["mode"] = "dense"
    payload["config"]["rerank"] = "rerank" in name

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        json.dump(payload, f, indent=2)
    print(f"Baseline updated → {path}")
    print(f"  pipeline: {payload['pipeline']}")
    print(f"  recall@10: {payload['metrics'].get('recall@10')}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Groundtruth CI regression gate")
    parser.add_argument("--config", default="config.yaml")
    parser.add_argument("--baseline", default=str(BASELINE_PATH))
    parser.add_argument("--results", default=None,
                        help="Use existing results JSON instead of re-running eval")
    parser.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD,
                        help="Max allowed drop in recall@10 (default 0.01 = 1 point)")
    parser.add_argument("--metric", default="recall@10")
    parser.add_argument("--update-baseline", action="store_true",
                        help="Write current results as the new baseline and exit 0")
    parser.add_argument("--demo-fail", action="store_true",
                        help="Inject an artificial 2-point drop to demonstrate gate failure")
    args = parser.parse_args()

    baseline_path = Path(args.baseline)

    if args.results:
        with open(args.results) as f:
            results = json.load(f)
    else:
        baseline = load_baseline(baseline_path) if baseline_path.exists() else {
            "config": {"mode": "dense", "rerank": False, "top_k": 10}
        }
        results = run_eval_matching_baseline(baseline, args.config)
        # Save a copy for the record
        save_results(results, ROOT / "results" / "ci_latest.json")

    if args.update_baseline:
        update_baseline(results, baseline_path)
        sys.exit(0)

    baseline = load_baseline(baseline_path)
    current_metrics = dict(results.get("aggregate", {}))

    if args.demo_fail:
        # Artificially tank the metric so we can show the gate firing
        original = current_metrics.get(args.metric, 1.0)
        current_metrics[args.metric] = max(0.0, original - 0.02)
        print(f"[demo-fail] Injected artificial drop: {args.metric} "
              f"{original:.4f} → {current_metrics[args.metric]:.4f}")

    passed, message = check_gate(
        current_metrics,
        baseline.get("metrics", {}),
        threshold=args.threshold,
        metric=args.metric,
    )
    print(message)

    # Extra context for CI logs
    print(f"\n  pipeline : {results.get('pipeline')}")
    print(f"  n_queries: {results.get('n_queries')}  n_corpus: {results.get('n_corpus')}")
    print(f"  baseline : {baseline_path}")

    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
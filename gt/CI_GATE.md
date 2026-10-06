# CI Regression Gate

Fails the PR when **recall@10 drops by more than 1 point** relative to the locked baseline.

## Local usage

```bash
# Run eval matching the baseline config, then check the gate
python scripts/ci_gate.py

# Demonstrate a failure (injects a 2-point artificial drop)
python scripts/ci_gate.py --demo-fail

# After a confirmed improvement, lock the new numbers
python scripts/ci_gate.py --update-baseline
```

## How it works

1. Loads `results/baseline.json` (locked metrics + config).
2. Re-runs eval with the **same** mode / rerank settings.
3. Compares `recall@10`. Exit code 1 if drop > 0.01.
4. GitHub Actions workflow (`.github/workflows/retrieval-gate.yml`) runs the same command on every PR.

## Updating the baseline

Only update after you have:
- Expanded / reviewed the golden set, **or**
- Confirmed a real retrieval improvement with the results table.

```bash
python scripts/ci_gate.py --update-baseline
```

Do **not** update the baseline just to make a red PR green.

## Threshold

Default: **0.01** (1 point of recall@10).  
Override with `--threshold 0.02` if needed; keep the ship-gate requirement at 1 point.

## Scope

- Tracks the baseline pipeline only (currently dense, no rerank).
- Does not gate generation metrics — those stay separate.
- Fully local; no API keys.
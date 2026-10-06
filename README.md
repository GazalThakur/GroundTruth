# Groundtruth — Retrieval Evaluation Harness

Prove whether a retrieval change is actually an improvement.  
Default stack is fully local and costs **$0**.

## Why this exists

A 60-attorney firm has a research assistant over 20 years of case files.  
Every week someone changes chunk size, embedding model, or adds a reranker — and nobody can say if last month’s version was better.  
A missed precedent is a malpractice conversation. Opinion is not evidence.

## Ship Gate (v1)

- [x] Compare: chunk sizes, hybrid vs dense, reranker on/off
- [x] Results table + written recommendation with explicit tradeoff
- [x] CI gate that fails when recall@10 drops > 1 point
- [x] Demonstrated CI failure (`--demo-fail`)
- [x] Error analysis of the hardest remaining failures
- [x] Everything runs at $0 by default
- [x] Clean provider interfaces ready for future paid APIs

## v1 Golden Set

| Item | Value |
|------|------:|
| Queries | **60** (human-reviewed) |
| Judgments | 29 full SC bodies |
| Gold spans | 69 (judgment_id + char offsets) |
| Source | Indian Supreme Court (AWS Open Data, CC-BY-4.0) |
| Status | **FROZEN** — see `data/golden/V1_FREEZE.md` |

**Hit rule:** a retrieved chunk counts if it overlaps a gold span by ≥100 characters **or** ≥30% of the span length. Chunking runs at eval time.

## Results (n=60)

Locked baseline: **dense · chunk=800 · no rerank · recall@10 = 0.8000**

| Config | recall@10 | Δ vs base | mrr | ndcg@10 |
|--------|----------:|----------:|----:|--------:|
| dense · c400 | 0.7056 | −0.0944 | 0.5140 | 0.5511 |
| **dense · c800 (BASE / CI)** | **0.8000** | — | 0.5715 | 0.6115 |
| dense · c1200 | 0.7833 | −0.0167 | 0.4878 | 0.5564 |
| hybrid · c800 | 0.8417 | +0.0417 | 0.5932 | 0.6492 |
| **dense + MiniLM rerank · c800** | **0.9083** | **+0.1083** | **0.6308** | **0.6922** |
| hybrid + MiniLM rerank · c800 | 0.8917 | +0.0917 | 0.6271 | 0.6834 |

Stack: BGE-base-en-v1.5 embeddings, rank_bm25, cross-encoder/ms-marco-MiniLM-L-6-v2. No paid APIs.

### Recommendation

| Setting | Choice | Why |
|---------|--------|-----|
| **chunk_size** | **800** | Best among {400, 800, 1200}; 400 fails the gate hard |
| **mode** | dense (with rerank) | Dense+rerank beats hybrid+rerank on this set |
| **rerank** | **on** | Largest single lift (+10.8 pts recall@10) |
| **Default product config** | **dense + MiniLM · c800** | Highest quality at $0 |
| **CI baseline** | dense · c800 · no rerank | Stable, cheaper; gate on recall@10 |

### Tradeoffs (honest)

| Choice | Upside | Cost / downside |
|--------|--------|------------------|
| Rerank on | +10.8 pts r@10 | Latency + CPU/GPU per query |
| Hybrid only (no rerank) | +4.2 pts, almost free | Weaker than dense+rerank |
| chunk 400 | Finer windows | −9.4 pts; fragments holdings |
| chunk 1200 | Fewer chunks | −1.7 pts; worse MRR |
| MiniLM vs BGE-reranker | Fits low RAM | Some headroom left on hard queries |

Hard misses under best config: **5 / 60**. Details: `data/golden/ERROR_ANALYSIS.md`.

## CI regression gate

```bash
# Passes when recall@10 is within 1 point of the locked baseline
python scripts/ci_gate.py

# Demonstrate a failure (injects a 2-point artificial drop)
python scripts/ci_gate.py --demo-fail

# After a confirmed improvement, lock new numbers
python scripts/ci_gate.py --update-baseline
```

- Baseline file: `results/baseline.json` (dense · c800 · recall@10 = **0.8000**)
- Threshold: drop **> 0.01** fails
- Workflow: `.github/workflows/retrieval-gate.yml`
- Docs: `gt/CI_GATE.md`

## How to run retrieval comparisons

```bash
python scripts/run_eval.py --mode dense  --no-rerank --chunk-size 800
python scripts/run_eval.py --mode hybrid --no-rerank --chunk-size 800
python scripts/run_eval.py --mode dense  --rerank    --chunk-size 800
python scripts/run_eval.py --mode hybrid --rerank    --chunk-size 800
```

## Design principles

1. **Golden set quality > quantity.** Human-reviewed only.
2. Retrieval metrics and generation metrics stay strictly separate.
3. Provider abstraction: local is default; paid is a config change.
4. Every experiment produces a numbers table and an explicit tradeoff.

## Layout

```
groundtruth/          # package (providers, retriever, span metrics, eval)
scripts/
  run_eval.py         # retrieval comparisons
  ci_gate.py          # regression gate (exit 1 on recall@10 drop > 1 pt)
data/golden/
  seed.jsonl          # 60 span-labeled queries (v1 frozen)
  corpus.jsonl        # full judgment bodies
  V1_FREEZE.md
  ERROR_ANALYSIS.md   # 5 hard misses under dense+rerank
results/
  baseline.json       # locked CI baseline
  baseline_lock.json  # explicit lock metadata
gt/                   # docs + ship-gate checklist
```

## Status

**Retrieval ship gate: complete for v1.**  
Optional later: generation metrics (faithfulness / answer relevance), golden-set growth to 80–100, multi-judgment queries.

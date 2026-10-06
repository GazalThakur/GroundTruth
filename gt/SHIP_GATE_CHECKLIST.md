# Ship Gate Checklist

### Core Requirements
- [x] 60 high-quality human-reviewed query–span pairs (v1 frozen)
- [x] recall@k, MRR, nDCG (span-overlap scoring)
- [ ] Faithfulness + Answer Relevance kept separate (generation metrics — later)
- [x] Chunk size comparison (400 / 800 / 1200)
- [x] Hybrid vs Dense comparison
- [x] Reranker on vs off
- [x] Results table + clear recommendation + tradeoff
- [x] CI gate that fails on recall@10 drop > 1 point
- [x] Demonstrated CI failure on a bad change (`--demo-fail`)
- [x] Error analysis of remaining hard failures (`data/golden/ERROR_ANALYSIS.md`)

### Architecture
- [x] Clean provider interfaces (Embedding / Reranker / LLM)
- [x] Local providers fully working
- [x] Config-driven switching ready for future API keys
- [x] $0 cost by default

### Locked defaults (v1)
| Setting | Value |
|---------|--------|
| Golden set | 60 queries / 29 judgments |
| Baseline (CI) | dense · c800 · no rerank · **recall@10 = 0.8000** |
| Recommended runtime | dense + MiniLM rerank · c800 · **recall@10 = 0.9083** |
| Chunk size | 800 |
| Gate threshold | drop > 0.01 fails |

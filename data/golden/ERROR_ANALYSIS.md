# Error Analysis — v1 Best Config

**Config:** dense + MiniLM rerank · chunk_size=800  
**Metrics:** recall@10 = 0.9083 · binary_recall@10 = 0.9167  
**Hard misses (binary_recall@10 = 0):** **5 / 60**

Gold labels were not edited after this analysis. Remaining misses are treated as real retrieval hardness, not annotation bugs.

## Miss list

| ID | Difficulty | Area | Failure mode |
|----|------------|------|----------------|
| `q_scst_01` | medium | criminal | Paraphrase / section-cite mismatch |
| `q_udf_01` | medium | tax | Same-judgment competition; weak UDF lexical anchor in span |
| `q_wc_01` | medium | civil | Generic procedural holding; sparse Act anchors |
| `q_cpc_01` | medium | civil | Fragile ranking (operative “no sale” holding) |
| `q_svc4_02` | medium | service | Long multi-part narrative; diffuse match |

## Per-query notes

### q_scst_01 — SC/ST Act s.3(2)(v) ingredients
Query asks for **essential ingredients** and cites **Section 3(2)(v)**.  
Gold is the ratio in paraphrase form (“from a bare perusal of the provision… offence to be constituted…”) without the digit string `3(2)(v)` inside the span.  
Dense and BM25 both under-match. **Gold is correct.**

### q_udf_01 — User Development Fee vs service tax
Query contrasts **statutory levy** vs **consideration for services**.  
Gold holds that UDF is a statutory levy, but sits inside a long airport-fee judgment that also supports `q_udf_02`. First-stage retrieval often lands on neighboring fee discussion. **Gold is correct.**

### q_wc_01 — Scope of s.30 Workmen Compensation appeal
Query is Act- and section-specific. Gold answers with the standard **“substantial questions of law”** formula and little Workmen/s.30 surface form. Easy to confuse with other civil-appeal chunks. **Gold is correct.**

### q_cpc_01 — Auction sale if 25% not deposited
Query is concrete; gold is the holding that there was **no sale** / purchasers acquired no rights. Hybrid RRF can demote a dense hit; under dense+rerank this query still misses top-10 — ranking fragility more than wrong label. **Gold is correct.**

### q_svc4_02 — “No further inquiry” after judicial discipline
Query asks whether proceedings can be **shut down** on that ground. Gold is a long Supreme Court critique of the High Court’s “new jurisprudence” plus restore-penalty direction. Multi-sentence narrative spreads signal across the chunk. **Gold is correct.**

## What these misses are *not*

- Not multi-hop across judgments  
- Not corrupted or headnote-only gold  
- Not CI noise from chunk-size mismatch (all evaluated at 800)

## Implication for v1

Freeze the 60-query set. Do **not** retarget these five spans to chase score.  
Optional later expansion (80–100) should add **new legal areas** and optional multi-judgment items, not more paraphrase stress tests of the same kind.

**Source of miss IDs:** Kaggle GPU run of `scripts/run_eval.py --mode dense --rerank --chunk-size 800` (notebook output, 2026-10-06).

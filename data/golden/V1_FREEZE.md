# Golden Set v1 — FREEZE

**Status:** FROZEN  
**Date:** 2026-10-05  
**Queries:** 60  
**Judgments:** 29  
**Spans:** 69

## Files

| File | Role |
|------|------|
| `seed.jsonl` | 60 span-labeled queries |
| `corpus.jsonl` | 28 full judgment bodies (not pre-chunked) |
| `v1_manifest.json` | Counts, IDs, scoring rule |
| `review_batch_0*_*.jsonl` | Immutable human-review sources |

## Scoring

A retrieved **chunk** is a hit if it overlaps a gold span by:
- ≥ **100 characters**, OR
- ≥ **30%** of the gold span length

Chunking is performed **at evaluation time** so chunk-size experiments stay valid.

## Batches

| Batch | Queries | Source files |
|-------|--------:|--------------|
| 01 | 17 | review_batch_01_v6_* |
| 02 | 15 | review_batch_02_v2_* |
| 03 | 14 | review_batch_03_* |
| 04 | 14 | review_batch_04_* |

## Do not

- Edit query text or gold spans without a new version bump
- Pre-chunk corpus into fixed passages for the default path
- Mix generation metrics into retrieval metrics

License: CC-BY-4.0 (Indian Supreme Court judgments open data).

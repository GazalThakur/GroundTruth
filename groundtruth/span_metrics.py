"""Span-overlap relevance for v1 Indian SC golden set.

A retrieved chunk is relevant if it overlaps a gold span by:
  - at least `min_chars` characters (default 100), OR
  - at least `min_frac` of the gold span length (default 0.30).

Query-level metrics:
  - span_recall@k : fraction of gold spans hit by top-k chunks
  - binary_recall@k : 1 if any gold span is hit in top-k, else 0
  - mrr : reciprocal rank of first overlapping chunk
  - ndcg@k : binary DCG over chunks that hit any gold span
"""

from __future__ import annotations

from typing import Dict, List, Sequence, Tuple
import math

from .schema import GoldSpan, Passage


def _overlap_len(a0: int, a1: int, b0: int, b1: int) -> int:
    return max(0, min(a1, b1) - max(a0, b0))


def chunk_hits_span(
    chunk: Passage,
    span: GoldSpan,
    min_chars: int = 100,
    min_frac: float = 0.30,
) -> bool:
    """True if chunk overlaps span enough to count as a hit."""
    jid = chunk.metadata.get("judgment_id") or chunk.id.split("__")[0]
    if jid != span.judgment_id:
        return False
    c0 = int(chunk.metadata.get("char_start", 0))
    c1 = int(chunk.metadata.get("char_end", c0 + len(chunk.text)))
    ov = _overlap_len(c0, c1, span.char_start, span.char_end)
    if ov <= 0:
        return False
    if ov >= min_chars:
        return True
    span_len = max(1, span.length)
    return (ov / span_len) >= min_frac


def relevant_chunk_ids(
    chunks: Sequence[Passage],
    spans: Sequence[GoldSpan],
    min_chars: int = 100,
    min_frac: float = 0.30,
) -> List[str]:
    """Return IDs of chunks that hit at least one gold span."""
    hits = []
    for ch in chunks:
        if any(chunk_hits_span(ch, sp, min_chars, min_frac) for sp in spans):
            hits.append(ch.id)
    return hits


def span_hit_mask(
    retrieved: Sequence[Passage],
    spans: Sequence[GoldSpan],
    min_chars: int = 100,
    min_frac: float = 0.30,
) -> List[bool]:
    """Per-retrieved-item: whether that chunk hits any gold span."""
    return [
        any(chunk_hits_span(ch, sp, min_chars, min_frac) for sp in spans)
        for ch in retrieved
    ]


def evaluate_span_query(
    spans: Sequence[GoldSpan],
    retrieved_chunks: Sequence[Passage],
    ks: Sequence[int] = (1, 5, 10),
    min_chars: int = 100,
    min_frac: float = 0.30,
) -> Dict[str, float]:
    """
    Metrics for one query under span-overlap relevance.

    span_recall@k  = (# gold spans hit by ≥1 chunk in top-k) / (# gold spans)
    binary_recall@k = 1 if any gold span hit in top-k else 0
    mrr            = 1/rank of first hitting chunk
    ndcg@k         = binary nDCG treating hitting chunks as relevant
    """
    if not spans:
        return {**{f"recall@{k}": 0.0 for k in ks},
                **{f"binary_recall@{k}": 0.0 for k in ks},
                **{f"ndcg@{k}": 0.0 for k in ks},
                "mrr": 0.0}

    hit_flags = span_hit_mask(retrieved_chunks, spans, min_chars, min_frac)

    # MRR
    mrr = 0.0
    for rank, flag in enumerate(hit_flags, start=1):
        if flag:
            mrr = 1.0 / rank
            break

    result: Dict[str, float] = {"mrr": mrr}

    for k in ks:
        top = retrieved_chunks[:k]
        # which gold spans are covered?
        covered = 0
        for sp in spans:
            if any(chunk_hits_span(ch, sp, min_chars, min_frac) for ch in top):
                covered += 1
        result[f"recall@{k}"] = covered / len(spans)
        result[f"binary_recall@{k}"] = 1.0 if covered > 0 else 0.0

        # nDCG binary over hit_flags
        dcg = sum(1.0 / math.log2(i + 2) for i, f in enumerate(hit_flags[:k]) if f)
        ideal_hits = min(len(spans), k)  # at most one ideal hit slot per span
        # For binary chunk-level nDCG, ideal is putting as many relevant chunks
        # as exist at the top. Cap by k.
        n_rel_chunks = sum(1 for ch in retrieved_chunks if any(
            chunk_hits_span(ch, sp, min_chars, min_frac) for sp in spans
        ))
        # Use ideal = min(k, max(1, covered potential)) — standard binary:
        # ideal DCG assumes min(k, number of relevant items in ranking universe)
        # Approximate with min(k, max(covered, 1) if any else 0)
        idcg = sum(1.0 / math.log2(i + 2) for i in range(min(k, max(n_rel_chunks, 0))))
        result[f"ndcg@{k}"] = (dcg / idcg) if idcg > 0 else 0.0

    return result

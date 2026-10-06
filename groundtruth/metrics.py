"""Retrieval metrics only.

Generation metrics (faithfulness, answer relevance) live elsewhere and are
never mixed into these numbers.
"""

from __future__ import annotations

from typing import List, Sequence
import math


def recall_at_k(
    relevant_ids: Sequence[str],
    retrieved_ids: Sequence[str],
    k: int,
) -> float:
    """Fraction of relevant passages found in the top-k retrieved results."""
    if not relevant_ids:
        return 0.0
    top = set(retrieved_ids[:k])
    hits = sum(1 for r in relevant_ids if r in top)
    return hits / len(relevant_ids)


def mrr(
    relevant_ids: Sequence[str],
    retrieved_ids: Sequence[str],
) -> float:
    """Mean Reciprocal Rank — 1 / rank of the first relevant hit (0 if none)."""
    relevant = set(relevant_ids)
    for rank, pid in enumerate(retrieved_ids, start=1):
        if pid in relevant:
            return 1.0 / rank
    return 0.0


def ndcg_at_k(
    relevant_ids: Sequence[str],
    retrieved_ids: Sequence[str],
    k: int,
) -> float:
    """
    Normalized Discounted Cumulative Gain at k.
    Binary relevance (1 if in relevant set, else 0).
    """
    if not relevant_ids:
        return 0.0

    relevant = set(relevant_ids)
    dcg = 0.0
    for i, pid in enumerate(retrieved_ids[:k]):
        if pid in relevant:
            # rank is 1-based → discount log2(i+2)
            dcg += 1.0 / math.log2(i + 2)

    # Ideal DCG: all relevant items ranked at the top
    ideal_hits = min(len(relevant_ids), k)
    idcg = sum(1.0 / math.log2(i + 2) for i in range(ideal_hits))
    if idcg == 0.0:
        return 0.0
    return dcg / idcg


def evaluate_query(
    relevant_ids: Sequence[str],
    retrieved_ids: Sequence[str],
    ks: Sequence[int] = (1, 5, 10),
) -> dict[str, float]:
    """Return a flat dict of metrics for one query."""
    result: dict[str, float] = {
        "mrr": mrr(relevant_ids, retrieved_ids),
    }
    for k in ks:
        result[f"recall@{k}"] = recall_at_k(relevant_ids, retrieved_ids, k)
        result[f"ndcg@{k}"] = ndcg_at_k(relevant_ids, retrieved_ids, k)
    return result


def aggregate(results: List[dict[str, float]]) -> dict[str, float]:
    """Macro-average metrics across queries."""
    if not results:
        return {}
    keys = results[0].keys()
    return {
        k: sum(r[k] for r in results) / len(results)
        for k in keys
    }
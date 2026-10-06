"""End-to-end retrieval evaluation loop.

v1: full-judgment corpus + span gold. Chunking is an eval-time parameter.
Retrieval metrics only — generation metrics stay out of this module.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence
import json

from .schema import load_golden, load_corpus, GoldenExample, Passage
from .chunking import chunk_judgments
from .retriever import (
    DenseRetriever,
    BM25Retriever,
    HybridRetriever,
    RetrievalPipeline,
)
from .span_metrics import evaluate_span_query
from .metrics import aggregate
from .providers.base import EmbeddingProvider, RerankerProvider
from .factory import (
    build_embedding,
    build_reranker,
    load_config,
)


def build_pipeline(
    cfg: dict,
    embedding: Optional[EmbeddingProvider] = None,
    reranker: Optional[RerankerProvider] = None,
) -> RetrievalPipeline:
    """
    Construct a RetrievalPipeline from config.

    Config keys (under retrieval:):
      mode:      "dense" | "hybrid" | "bm25"   (default: dense)
      hybrid:    bool  (legacy alias for mode=hybrid)
      rerank:    bool
      top_k:     final number of results
      candidate_k: how many to fetch before reranking (default 20)
    """
    ret_cfg = cfg.get("retrieval", {})
    mode = ret_cfg.get("mode")
    if mode is None:
        mode = "hybrid" if ret_cfg.get("hybrid") else "dense"

    if embedding is None:
        embedding = build_embedding(cfg.get("embedding", {}))

    dense = DenseRetriever(embedding)

    if mode == "dense":
        first_stage = dense
    elif mode == "bm25":
        first_stage = BM25Retriever()
    elif mode == "hybrid":
        first_stage = HybridRetriever(dense=dense, bm25=BM25Retriever())
    else:
        raise ValueError(f"Unknown retrieval mode: {mode}. Use dense|hybrid|bm25")

    use_rerank = ret_cfg.get("rerank", False)
    if use_rerank and reranker is None:
        reranker = build_reranker(cfg.get("reranker", {}))
    if not use_rerank:
        reranker = None

    candidate_k = ret_cfg.get("candidate_k", 20)
    return RetrievalPipeline(
        retriever=first_stage,
        reranker=reranker,
        candidate_k=candidate_k,
    )


def run_retrieval_eval(
    golden: Sequence[GoldenExample],
    judgments: Sequence[Passage],
    pipeline: RetrievalPipeline,
    top_k: int = 10,
    ks: Sequence[int] = (1, 5, 10),
    chunk_size: int = 800,
    chunk_overlap: int = 100,
    min_chars: int = 100,
    min_frac: float = 0.30,
) -> Dict[str, Any]:
    """
    Chunk judgments → index → retrieve → span-overlap metrics.
    """
    chunks = chunk_judgments(judgments, chunk_size=chunk_size, overlap=chunk_overlap)
    chunk_by_id = {c.id: c for c in chunks}

    pipeline.index(chunks)

    per_query: List[Dict[str, Any]] = []
    metric_rows: List[Dict[str, float]] = []

    for ex in golden:
        retrieved_ids = pipeline.retrieve(ex.query, top_k=top_k)
        retrieved_chunks = [chunk_by_id[i] for i in retrieved_ids if i in chunk_by_id]
        metrics = evaluate_span_query(
            ex.relevant,
            retrieved_chunks,
            ks=ks,
            min_chars=min_chars,
            min_frac=min_frac,
        )
        metric_rows.append(metrics)
        per_query.append({
            "id": ex.id,
            "query": ex.query,
            "category": ex.category,
            "difficulty": ex.difficulty,
            "n_gold_spans": len(ex.relevant),
            "retrieved": retrieved_ids,
            **metrics,
        })

    agg = aggregate(metric_rows)
    return {
        "pipeline": getattr(pipeline, "name", pipeline.__class__.__name__),
        "n_queries": len(golden),
        "n_judgments": len(judgments),
        "n_chunks": len(chunks),
        "chunk_size": chunk_size,
        "chunk_overlap": chunk_overlap,
        "top_k": top_k,
        "aggregate": agg,
        "per_query": per_query,
    }


def run_from_config(
    cfg: Optional[dict] = None,
    config_path: str | Path = "config.yaml",
    embedding: Optional[EmbeddingProvider] = None,
    reranker: Optional[RerankerProvider] = None,
) -> Dict[str, Any]:
    if cfg is None:
        cfg = load_config(config_path)

    data_cfg = cfg.get("data", {})
    golden = load_golden(data_cfg.get("golden", "data/golden/seed.jsonl"))
    judgments = load_corpus(data_cfg.get("corpus", "data/golden/corpus.jsonl"))

    ret_cfg = cfg.get("retrieval", {})
    pipeline = build_pipeline(cfg, embedding=embedding, reranker=reranker)
    top_k = ret_cfg.get("top_k", 10)

    return run_retrieval_eval(
        golden=golden,
        judgments=judgments,
        pipeline=pipeline,
        top_k=top_k,
        chunk_size=int(ret_cfg.get("chunk_size", 800)),
        chunk_overlap=int(ret_cfg.get("chunk_overlap", 100)),
        min_chars=int(ret_cfg.get("span_min_chars", 100)),
        min_frac=float(ret_cfg.get("span_min_frac", 0.30)),
    )


def print_results(results: Dict[str, Any]) -> None:
    agg = results["aggregate"]
    print(
        f"\n=== Retrieval Eval  [{results.get('pipeline', '?')}]  "
        f"(n={results['n_queries']} queries, "
        f"judgments={results.get('n_judgments')}, "
        f"chunks={results.get('n_chunks')}, "
        f"chunk_size={results.get('chunk_size')}, "
        f"top_k={results['top_k']}) ===\n"
    )
    print("Aggregate metrics:")
    for k in sorted(agg.keys()):
        print(f"  {k:20s}  {agg[k]:.4f}")

    misses = [r for r in results["per_query"] if r.get("binary_recall@10", r.get("recall@10", 0)) == 0]
    if misses:
        print(f"\nHard misses (binary_recall@10 = 0): {len(misses)}")
        for m in misses[:8]:
            print(f"  [{m['id']}] {m['query'][:80]}")
    else:
        print("\nNo hard misses (all queries had ≥1 gold span hit in top-10).")


def save_results(results: Dict[str, Any], path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

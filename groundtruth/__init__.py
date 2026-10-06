"""Groundtruth — Retrieval Evaluation Harness.

Prove retrieval changes with numbers, not opinions.
Default stack is fully local and $0.
"""

__version__ = "0.1.0"

from .schema import GoldenExample, Passage, load_golden, load_corpus
from .metrics import recall_at_k, mrr, ndcg_at_k, evaluate_query, aggregate
from .retriever import DenseRetriever, BM25Retriever, HybridRetriever, RetrievalPipeline
from .eval import run_retrieval_eval, run_from_config, print_results, build_pipeline

__all__ = [
    "GoldenExample",
    "Passage",
    "load_golden",
    "load_corpus",
    "recall_at_k",
    "mrr",
    "ndcg_at_k",
    "evaluate_query",
    "aggregate",
    "DenseRetriever",
    "BM25Retriever",
    "HybridRetriever",
    "RetrievalPipeline",
    "run_retrieval_eval",
    "run_from_config",
    "print_results",
    "build_pipeline",
]
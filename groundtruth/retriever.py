"""Retrievers built on provider interfaces.

Dense  — EmbeddingProvider (BGE by default)
BM25   — pure lexical (rank_bm25)
Hybrid — Reciprocal Rank Fusion of dense + BM25

All implement the same minimal surface so the eval loop stays identical.
"""

from __future__ import annotations

from typing import List, Sequence, Optional, Protocol
import re
import numpy as np

from .providers.base import EmbeddingProvider
from .schema import Passage


# ---------------------------------------------------------------------------
# Shared protocol (duck-typed; no ABC needed)
# ---------------------------------------------------------------------------

class Retriever(Protocol):
    def index(self, passages: Sequence[Passage]) -> None: ...
    def retrieve(self, query: str, top_k: int = 10) -> List[str]: ...
    def retrieve_with_scores(
        self, query: str, top_k: int = 10
    ) -> List[tuple[str, float]]: ...
    @property
    def size(self) -> int: ...
    @property
    def name(self) -> str: ...


def _tokenize(text: str) -> List[str]:
    """Minimal whitespace + lower-case tokenizer. Good enough for legal English."""
    return re.findall(r"[a-z0-9]+", text.lower())


# ---------------------------------------------------------------------------
# Dense
# ---------------------------------------------------------------------------

class DenseRetriever:
    """Cosine similarity over EmbeddingProvider vectors."""

    def __init__(self, embedding_provider: EmbeddingProvider):
        self.embedding = embedding_provider
        self._ids: List[str] = []
        self._texts: List[str] = []
        self._matrix: Optional[np.ndarray] = None

    def index(self, passages: Sequence[Passage]) -> None:
        if not passages:
            self._ids, self._texts, self._matrix = [], [], None
            return
        self._ids = [p.id for p in passages]
        self._texts = [p.text for p in passages]
        # Encode in batches via provider; assemble matrix row-wise to limit peak RAM
        batch = 32
        rows = []
        for i in range(0, len(self._texts), batch):
            vecs = self.embedding.embed(self._texts[i : i + batch])
            rows.append(np.array(vecs, dtype=np.float32))
        self._matrix = np.vstack(rows) if rows else None

    def retrieve(self, query: str, top_k: int = 10) -> List[str]:
        return [pid for pid, _ in self.retrieve_with_scores(query, top_k)]

    def retrieve_with_scores(
        self, query: str, top_k: int = 10
    ) -> List[tuple[str, float]]:
        if self._matrix is None or len(self._ids) == 0:
            return []
        q_vec = np.array(self.embedding.embed_query(query), dtype=np.float32)
        scores = self._matrix @ q_vec
        if top_k >= len(scores):
            ranked_idx = np.argsort(-scores)
        else:
            part = np.argpartition(-scores, top_k)[:top_k]
            ranked_idx = part[np.argsort(-scores[part])]
        return [(self._ids[i], float(scores[i])) for i in ranked_idx]

    @property
    def size(self) -> int:
        return len(self._ids)

    @property
    def name(self) -> str:
        return f"dense[{self.embedding.model_name}]"


# ---------------------------------------------------------------------------
# BM25
# ---------------------------------------------------------------------------

class BM25Retriever:
    """Lexical BM25 (Okapi). Fully local, zero cost."""

    def __init__(self):
        self._ids: List[str] = []
        self._texts: List[str] = []
        self._bm25 = None

    def index(self, passages: Sequence[Passage]) -> None:
        if not passages:
            self._ids, self._texts, self._bm25 = [], [], None
            return
        self._ids = [p.id for p in passages]
        self._texts = [p.text for p in passages]
        tokenized = [_tokenize(t) for t in self._texts]
        from rank_bm25 import BM25Okapi
        self._bm25 = BM25Okapi(tokenized)

    def retrieve(self, query: str, top_k: int = 10) -> List[str]:
        return [pid for pid, _ in self.retrieve_with_scores(query, top_k)]

    def retrieve_with_scores(
        self, query: str, top_k: int = 10
    ) -> List[tuple[str, float]]:
        if self._bm25 is None or len(self._ids) == 0:
            return []
        tokens = _tokenize(query)
        scores = self._bm25.get_scores(tokens)
        if top_k >= len(scores):
            ranked_idx = np.argsort(-scores)
        else:
            part = np.argpartition(-scores, top_k)[:top_k]
            ranked_idx = part[np.argsort(-scores[part])]
        return [(self._ids[i], float(scores[i])) for i in ranked_idx]

    @property
    def size(self) -> int:
        return len(self._ids)

    @property
    def name(self) -> str:
        return "bm25"


# ---------------------------------------------------------------------------
# Hybrid (Reciprocal Rank Fusion)
# ---------------------------------------------------------------------------

class HybridRetriever:
    """
    Fuse dense + BM25 with Reciprocal Rank Fusion.

    RRF score = Σ 1 / (k + rank_i)   (k=60 is the standard constant)
    No score normalization required; ranks only.
    """

    def __init__(
        self,
        dense: DenseRetriever,
        bm25: Optional[BM25Retriever] = None,
        rrf_k: int = 60,
        candidate_multiplier: int = 2,
    ):
        self.dense = dense
        self.bm25 = bm25 or BM25Retriever()
        self.rrf_k = rrf_k
        # Pull more candidates from each retriever before fusion
        self.candidate_multiplier = candidate_multiplier

    def index(self, passages: Sequence[Passage]) -> None:
        self.dense.index(passages)
        self.bm25.index(passages)

    def retrieve(self, query: str, top_k: int = 10) -> List[str]:
        return [pid for pid, _ in self.retrieve_with_scores(query, top_k)]

    def retrieve_with_scores(
        self, query: str, top_k: int = 10
    ) -> List[tuple[str, float]]:
        fetch = top_k * self.candidate_multiplier
        dense_hits = self.dense.retrieve_with_scores(query, top_k=fetch)
        bm25_hits = self.bm25.retrieve_with_scores(query, top_k=fetch)

        rrf: dict[str, float] = {}
        for rank, (pid, _) in enumerate(dense_hits, start=1):
            rrf[pid] = rrf.get(pid, 0.0) + 1.0 / (self.rrf_k + rank)
        for rank, (pid, _) in enumerate(bm25_hits, start=1):
            rrf[pid] = rrf.get(pid, 0.0) + 1.0 / (self.rrf_k + rank)

        ranked = sorted(rrf.items(), key=lambda x: x[1], reverse=True)
        return ranked[:top_k]

    @property
    def size(self) -> int:
        return self.dense.size

    @property
    def name(self) -> str:
        return f"hybrid[{self.dense.name}+bm25]"


# ---------------------------------------------------------------------------
# Pipeline: retrieve → optional rerank
# ---------------------------------------------------------------------------

class RetrievalPipeline:
    """
    Thin orchestration layer.

    1. First-stage retrieval (dense or hybrid) → candidate_k passages
    2. Optional cross-encoder rerank → final top_k
    """

    def __init__(
        self,
        retriever: Retriever,
        reranker=None,          # RerankerProvider | None
        candidate_k: int = 20,  # how many to fetch before reranking
    ):
        self.retriever = retriever
        self.reranker = reranker
        self.candidate_k = candidate_k
        self._id_to_text: dict[str, str] = {}

    def index(self, passages: Sequence[Passage]) -> None:
        self.retriever.index(passages)
        self._id_to_text = {p.id: p.text for p in passages}

    def retrieve(self, query: str, top_k: int = 10) -> List[str]:
        # First stage
        fetch_k = max(top_k, self.candidate_k) if self.reranker else top_k
        candidates = self.retriever.retrieve(query, top_k=fetch_k)

        if not self.reranker or not candidates:
            return candidates[:top_k]

        # Rerank
        texts = [self._id_to_text[pid] for pid in candidates]
        ranked = self.reranker.rerank(query, texts, top_k=top_k)
        return [candidates[idx] for idx, _ in ranked]

    @property
    def name(self) -> str:
        base = self.retriever.name
        if self.reranker:
            return f"{base}+rerank[{self.reranker.model_name}]"
        return base

    @property
    def size(self) -> int:
        return self.retriever.size
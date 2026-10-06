"""Local (fully free) provider implementations.

Embeddings: BAAI/bge-base-en-v1.5 via sentence-transformers
Reranker:   BAAI/bge-reranker-base via sentence-transformers CrossEncoder
LLM:        Ollama (llama3.1:8b or whatever is configured)
"""

from __future__ import annotations

from typing import List, Sequence

from .base import EmbeddingProvider, RerankerProvider, LLMProvider


class LocalBGEEmbedding(EmbeddingProvider):
    """BGE-base embeddings. Runs entirely on CPU/GPU via sentence-transformers."""

    def __init__(self, model_name: str = "BAAI/bge-base-en-v1.5", device: str = "cpu"):
        # Lazy import so the rest of the package can be imported without the heavy deps
        from sentence_transformers import SentenceTransformer

        self._model_name = model_name
        self._model = SentenceTransformer(model_name, device=device)
        # Prefer new API name; fall back for older sentence-transformers
        if hasattr(self._model, "get_embedding_dimension"):
            self._dim = self._model.get_embedding_dimension()
        else:
            self._dim = self._model.get_sentence_embedding_dimension()

    def embed(self, texts: Sequence[str]) -> List[List[float]]:
        # Batch to stay within small-RAM hosts (~1–2 GB).
        texts = list(texts)
        if not texts:
            return []
        batch_size = 8
        out: List[List[float]] = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i : i + batch_size]
            vectors = self._model.encode(
                batch,
                normalize_embeddings=True,
                show_progress_bar=False,
                batch_size=batch_size,
            )
            out.extend(vectors.tolist())
        return out

    def embed_query(self, query: str) -> List[float]:
        # Same model; for pure retrieval we keep it simple.
        # If we later switch to bge-m3 or asymmetric models we can special-case here.
        return self.embed([query])[0]

    @property
    def dimension(self) -> int:
        return self._dim

    @property
    def model_name(self) -> str:
        return self._model_name


class LocalBGEReranker(RerankerProvider):
    """Local cross-encoder reranker.

    Default is MiniLM (fits in ~1 GB RAM). For higher quality when you have
    more memory / a GPU, set model to BAAI/bge-reranker-base in config.
    """

    def __init__(
        self,
        model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2",
        device: str = "cpu",
    ):
        from sentence_transformers import CrossEncoder

        self._model_name = model_name
        self._model = CrossEncoder(model_name, device=device)

    def rerank(
        self,
        query: str,
        passages: Sequence[str],
        top_k: int | None = None,
    ) -> List[tuple[int, float]]:
        if not passages:
            return []

        pairs = [[query, p] for p in passages]
        scores = self._model.predict(pairs, show_progress_bar=False)

        ranked = sorted(
            enumerate(scores.tolist()),
            key=lambda x: x[1],
            reverse=True,
        )
        if top_k is not None:
            ranked = ranked[:top_k]
        return ranked

    @property
    def model_name(self) -> str:
        return self._model_name


class OllamaLLM(LLMProvider):
    """Ollama-backed LLM. Requires a running Ollama server."""

    def __init__(
        self,
        model_name: str = "llama3.1:8b",
        base_url: str = "http://localhost:11434",
        temperature: float = 0.0,
    ):
        self._model_name = model_name
        self._base_url = base_url.rstrip("/")
        self._temperature = temperature

    def generate(self, prompt: str, max_tokens: int = 512) -> str:
        import requests

        resp = requests.post(
            f"{self._base_url}/api/generate",
            json={
                "model": self._model_name,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": self._temperature,
                    "num_predict": max_tokens,
                },
            },
            timeout=120,
        )
        resp.raise_for_status()
        return resp.json().get("response", "").strip()

    @property
    def model_name(self) -> str:
        return self._model_name
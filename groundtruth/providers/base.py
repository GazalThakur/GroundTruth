"""Provider interfaces.

All external dependencies go through these three interfaces.
Local implementations are the default. Paid providers can be added later
without touching evaluation or experiment code.
"""

from abc import ABC, abstractmethod
from typing import List, Sequence


class EmbeddingProvider(ABC):
    """Embed text into dense vectors."""

    @abstractmethod
    def embed(self, texts: Sequence[str]) -> List[List[float]]:
        """Return one embedding vector per input text."""
        ...

    @abstractmethod
    def embed_query(self, query: str) -> List[float]:
        """Embed a single query. Some models use asymmetric encoding."""
        ...

    @property
    @abstractmethod
    def dimension(self) -> int:
        """Embedding dimensionality."""
        ...

    @property
    @abstractmethod
    def model_name(self) -> str:
        """Human-readable model identifier for logging / results tables."""
        ...


class RerankerProvider(ABC):
    """Score (query, passage) pairs and reorder candidates."""

    @abstractmethod
    def rerank(
        self,
        query: str,
        passages: Sequence[str],
        top_k: int | None = None,
    ) -> List[tuple[int, float]]:
        """
        Return list of (original_index, score) sorted by descending relevance.
        If top_k is None, return all passages reordered.
        """
        ...

    @property
    @abstractmethod
    def model_name(self) -> str:
        ...


class LLMProvider(ABC):
    """Text generation and (later) LLM-as-judge."""

    @abstractmethod
    def generate(self, prompt: str, max_tokens: int = 512) -> str:
        """Generate a completion. Used for generation metrics only."""
        ...

    @property
    @abstractmethod
    def model_name(self) -> str:
        ...
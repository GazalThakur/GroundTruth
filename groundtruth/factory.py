"""Config-driven provider factory.

Switching from local → paid is a config change, not a code change.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .providers.base import EmbeddingProvider, RerankerProvider, LLMProvider
from .providers.local import LocalBGEEmbedding, LocalBGEReranker, OllamaLLM


def load_config(path: str | Path = "config.yaml") -> dict[str, Any]:
    with open(path) as f:
        return yaml.safe_load(f)


def build_embedding(cfg: dict[str, Any] | None = None) -> EmbeddingProvider:
    cfg = cfg or {}
    provider = cfg.get("provider", "local_bge")
    if provider == "local_bge":
        return LocalBGEEmbedding(
            model_name=cfg.get("model", "BAAI/bge-base-en-v1.5"),
            device=cfg.get("device", "cpu"),
        )
    raise ValueError(
        f"Unknown embedding provider: {provider}. "
        "Add a new implementation and register it here when you want paid APIs."
    )


def build_reranker(cfg: dict[str, Any] | None = None) -> RerankerProvider:
    cfg = cfg or {}
    provider = cfg.get("provider", "local_bge")
    if provider == "local_bge":
        return LocalBGEReranker(
            model_name=cfg.get("model", "cross-encoder/ms-marco-MiniLM-L-6-v2"),
            device=cfg.get("device", "cpu"),
        )
    raise ValueError(f"Unknown reranker provider: {provider}")


def build_llm(cfg: dict[str, Any] | None = None) -> LLMProvider:
    cfg = cfg or {}
    provider = cfg.get("provider", "ollama")
    if provider == "ollama":
        return OllamaLLM(
            model_name=cfg.get("model", "llama3.1:8b"),
            base_url=cfg.get("base_url", "http://localhost:11434"),
            temperature=cfg.get("temperature", 0.0),
        )
    raise ValueError(f"Unknown LLM provider: {provider}")


def build_all(config_path: str | Path = "config.yaml"):
    """Convenience: return (embedding, reranker, llm) from a config file."""
    cfg = load_config(config_path)
    return (
        build_embedding(cfg.get("embedding", {})),
        build_reranker(cfg.get("reranker", {})),
        build_llm(cfg.get("llm", {})),
    )
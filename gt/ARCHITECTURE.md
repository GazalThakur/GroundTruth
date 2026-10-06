# Architecture Principles

## Provider Abstraction

All external dependencies go through clean interfaces:

- `EmbeddingProvider`
- `RerankerProvider`
- `LLMProvider` (used for both generation and judging)

Default implementations are fully local.
Paid providers can be added later without touching evaluation or experiment code.

## Configuration

Prefer a simple `config.yaml` or environment-based factory so switching looks like:

```yaml
embedding:
  provider: "local_bge"     # → "openai" later
reranker:
  provider: "local_bge"     # → "cohere" later
llm:
  provider: "ollama"        # → "openai" or "anthropic" later
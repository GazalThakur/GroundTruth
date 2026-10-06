# Groundtruth — Retrieval Evaluation Harness

**Level**: Foundational  
**Effort**: One weekend  
**Constraint**: Fully cost-free by default (local models), with clean path to paid APIs later

## The Use Case

A 60-attorney firm has a research assistant over 20 years of case files and filings. Every week someone changes a chunk size, swaps an embedding model or adds a reranker, and nobody can say whether last month’s version was better. A missed precedent is a malpractice conversation, so opinion is not an acceptable form of evidence.

## What It Proves

You can prove a retrieval change was an improvement instead of asserting it — using a clean, swappable provider architecture.

## The Build

- High-quality golden set of 60–100 human-reviewed query–passage pairs
- Retrieval metrics: recall@k, MRR, nDCG (broken out by category)
- Generation metrics (faithfulness + answer relevance) kept strictly separate
- CI regression harness that fails the PR when recall@10 drops > 1 point
- Provider abstraction so local ↔ paid APIs can be swapped via config

## Default Free Stack

| Component     | Default (Free)                          | Future Options                  |
|---------------|-----------------------------------------|---------------------------------|
| Embeddings    | `BAAI/bge-base-en-v1.5` (local)        | OpenAI, Voyage, Cohere         |
| Reranker      | `BAAI/bge-reranker-base` (local)       | Cohere, Jina, etc.             |
| Vector Store  | Chroma (local) or FAISS                | —                              |
| LLM           | Ollama (`llama3.1:8b` or better)       | OpenAI, Anthropic, Groq, etc.  |

## Ship Gate

- [ ] Three configurations compared (chunk size / hybrid vs dense / reranker on-off)
- [ ] Results table + written recommendation with clear tradeoff
- [ ] CI gate demonstrated failing on a bad change
- [ ] Error analysis of the 5 hardest remaining failures
- [ ] Everything runs with $0 cost by default
- [ ] Provider interface cleanly supports future API keys
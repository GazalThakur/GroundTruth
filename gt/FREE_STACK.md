# Free Stack + Future Extensibility

## Current Default (Cost = $0)

- Embeddings: `BAAI/bge-base-en-v1.5` via sentence-transformers
- Reranker: `cross-encoder/ms-marco-MiniLM-L-6-v2` (default; fits low-RAM)
  - Prefer `BAAI/bge-reranker-base` when you have ≥2 GB RAM or a GPU (set in config)
- Lexical: BM25 (rank_bm25)
- Hybrid: Dense + BM25 via Reciprocal Rank Fusion (k=60)
- Vector store: in-memory (swap to Chroma/FAISS later without touching eval)
- LLM: Ollama (`llama3.1:8b` recommended)

## Quality Trade-offs (Honest)

| Choice                              | Impact on Quality              | Acceptable? |
|-------------------------------------|--------------------------------|-------------|
| Local BGE vs OpenAI embeddings      | Very small                     | Yes         |
| MiniLM reranker vs BGE-reranker     | Noticeable on hard queries     | Yes for $0 / low-RAM; config switch when resources allow |
| MiniLM / BGE vs Cohere Rerank       | Small–medium                   | Yes         |
| RRF hybrid vs learned fusion        | Small for legal text           | Yes         |
| 8B–14B local LLM as judge           | Noticeable but solid           | Yes (with good rubric) |
| Excellent small golden set          | Often better than large noisy  | Yes — expand to 60–100 human-reviewed |

## Future API Integration

Because of the provider abstraction, adding OpenAI / Anthropic / Cohere later is just:
1. Implement the new provider class
2. Change config
3. Add API key to environment

No rewriting of experiments or metrics needed.
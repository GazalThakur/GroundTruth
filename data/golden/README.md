# Golden Set — Indian Supreme Court judgments

**Source:** Real judgments from `s3://indian-supreme-court-judgments/` (CC-BY-4.0).  
**Not** synthetic / LLM-generated. Every query–passage pair is human-reviewed.

## Process

1. Download English judgment PDFs from the AWS Open Data bucket (no account needed).
2. Extract text → chunk into passages (`groundtruth/indian_sc.py`).
3. Write realistic Indian legal-research queries against those passages.
4. **Human review** — keep / edit / drop.
5. Only approved pairs go into `corpus.jsonl` + `seed.jsonl`.

## Files

| File | Role |
|------|------|
| `corpus.jsonl` | Approved passages (empty until first review batch lands) |
| `seed.jsonl` | Approved query → passage_id pairs |
| `archive_us_seed/` | Previous US-style synthetic seed (archived, not used) |
| `../indian_sc/` | Raw PDFs, extracted text, metadata |

## Categories (Indian law)

Use these for the `category` field:

- `constitutional`
- `criminal`
- `civil`
- `service`
- `tax`
- `property`
- `family`
- `procedure`
- `precedent`
- `statutory_interpretation`

Difficulty: `easy` | `medium` | `hard`

## Attribution

Indian Supreme Court Judgments was accessed from  
https://registry.opendata.aws/indian-supreme-court-judgments  
License: CC-BY-4.0.

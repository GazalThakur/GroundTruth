# Indian Supreme Court golden-set pipeline

## Source
- Bucket: `s3://indian-supreme-court-judgments/` (ap-south-1)
- License: **CC-BY-4.0**
- Registry: https://registry.opendata.aws/indian-supreme-court-judgments/
- Access: `aws s3 ... --no-sign-request` (no account required)
- ~35K English judgments, 1950–present

## What we archived
Previous US-style synthetic seed → `data/golden/archive_us_seed/`

## Modules
- `groundtruth/indian_sc.py` — list / download / extract / chunk
- `scripts/sample_indian_sc.py` — CLI to sample N judgments → candidate passages

## Recommended workflow (quality over quantity)

1. **Sample judgments** (already done for 2023, n=8 → candidate corpus)
2. **Curate passages** — do *not* use every auto-chunk. Pick holdings, ratio, key statutory interpretation paragraphs (aim ~2–4 strong passages per judgment).
3. **Write realistic Indian research queries** an associate would type (e.g. “Does the right to be heard under Forest Act s.4 extend beyond Adivasi communities?”).
4. **Human review** — keep / edit / drop.
5. **Promote** approved pairs only into `data/golden/corpus.jsonl` + `seed.jsonl`.
6. Re-run eval + update CI baseline after the set stabilizes.

## Categories
constitutional | criminal | civil | service | tax | property | family | procedure | precedent | statutory_interpretation

## Attribution required
Cite the AWS Open Data dataset (CC-BY-4.0) in any public write-up.

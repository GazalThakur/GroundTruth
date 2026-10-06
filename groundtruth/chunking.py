"""Eval-time chunking of full judgment bodies.

Corpus stores full judgments. Chunk size / overlap are experiment parameters.
Passage IDs encode judgment + character offsets so span-overlap scoring works.
"""

from __future__ import annotations

from typing import List, Sequence

from .schema import Passage


def chunk_judgments(
    judgments: Sequence[Passage],
    chunk_size: int = 800,
    overlap: int = 100,
) -> List[Passage]:
    """
    Split each full-judgment Passage into overlapping character windows.

    Args:
        judgments: corpus records (one per judgment body)
        chunk_size: target character length per chunk
        overlap: character overlap between consecutive chunks

    Returns:
        List of Passage chunks with metadata:
          judgment_id, char_start, char_end, chunk_index
    """
    if chunk_size <= 0:
        raise ValueError(f"chunk_size must be positive, got {chunk_size}")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError(f"overlap must be in [0, chunk_size), got {overlap}")

    step = chunk_size - overlap
    chunks: List[Passage] = []

    for j in judgments:
        text = j.text or ""
        jid = j.metadata.get("judgment_id") or j.id
        n = len(text)
        if n == 0:
            continue
        if n <= chunk_size:
            chunks.append(
                Passage(
                    id=f"{jid}__c000",
                    text=text,
                    source=j.source,
                    metadata={
                        **j.metadata,
                        "judgment_id": jid,
                        "char_start": 0,
                        "char_end": n,
                        "chunk_index": 0,
                        "record_type": "chunk",
                    },
                )
            )
            continue

        idx = 0
        start = 0
        while start < n:
            end = min(start + chunk_size, n)
            # Prefer breaking near whitespace if not last chunk
            if end < n:
                window = text[start:end]
                # search last space in final 20% of window
                search_from = int(len(window) * 0.8)
                rel = window.rfind(" ", search_from)
                if rel != -1 and rel > 0:
                    end = start + rel

            piece = text[start:end]
            if piece.strip():
                chunks.append(
                    Passage(
                        id=f"{jid}__c{idx:03d}",
                        text=piece,
                        source=j.source,
                        metadata={
                            **{k: v for k, v in j.metadata.items() if k not in ("char_start", "char_end", "chunk_index")},
                            "judgment_id": jid,
                            "char_start": start,
                            "char_end": end,
                            "chunk_index": idx,
                            "record_type": "chunk",
                        },
                    )
                )
                idx += 1

            if end >= n:
                break
            start = end - overlap if overlap else end
            if start <= 0 and end >= n:
                break
            # prevent infinite loop on pathological cases
            if end == start:
                start = end + 1

    return chunks

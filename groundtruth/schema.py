"""Golden-set schema.

v1 (Indian SC): gold is judgment_id + character spans on full judgment body text.
Chunking is an eval-time parameter — corpus stores full judgments, not fixed passages.

Legacy fields (relevant_passage_ids) are retained for backward compatibility but
are empty for the v1 span-labeled set.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional
import json
from pathlib import Path


@dataclass
class GoldSpan:
    """Character span into a judgment body."""

    judgment_id: str
    char_start: int
    char_end: int

    def to_dict(self) -> dict:
        return {
            "judgment_id": self.judgment_id,
            "char_start": self.char_start,
            "char_end": self.char_end,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "GoldSpan":
        return cls(
            judgment_id=d["judgment_id"],
            char_start=int(d["char_start"]),
            char_end=int(d["char_end"]),
        )

    @property
    def length(self) -> int:
        return max(0, self.char_end - self.char_start)


@dataclass
class GoldenExample:
    """One query with ground-truth relevant evidence."""

    id: str
    query: str
    category: str
    difficulty: str = "medium"
    notes: str = ""
    relevant: List[GoldSpan] = field(default_factory=list)
    relevant_passage_ids: List[str] = field(default_factory=list)
    scoring: str = (
        "hit = retrieved chunk overlaps a gold span by at least 100 chars "
        "OR 30% of the span length"
    )
    batch: str = ""

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "query": self.query,
            "category": self.category,
            "difficulty": self.difficulty,
            "notes": self.notes,
            "relevant": [s.to_dict() for s in self.relevant],
            "relevant_passage_ids": list(self.relevant_passage_ids),
            "scoring": self.scoring,
            "batch": self.batch,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "GoldenExample":
        spans = [GoldSpan.from_dict(s) for s in d.get("relevant") or []]
        return cls(
            id=d["id"],
            query=d["query"],
            category=d.get("category", ""),
            difficulty=d.get("difficulty", "medium"),
            notes=d.get("notes", ""),
            relevant=spans,
            relevant_passage_ids=list(d.get("relevant_passage_ids") or []),
            scoring=d.get("scoring", cls.__dataclass_fields__["scoring"].default),
            batch=d.get("batch", ""),
        )


@dataclass
class Passage:
    """A retrieval unit — full judgment or an eval-time chunk."""

    id: str
    text: str
    source: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "Passage":
        pid = d.get("id") or d.get("judgment_id")
        if not pid:
            raise ValueError(f"Passage missing id/judgment_id: keys={list(d.keys())}")
        meta = dict(d.get("metadata") or {})
        if "judgment_id" in d and "judgment_id" not in meta:
            meta["judgment_id"] = d["judgment_id"]
        return cls(
            id=str(pid),
            text=d.get("text", ""),
            source=d.get("source", ""),
            metadata=meta,
        )


def load_golden(path: str | Path) -> List[GoldenExample]:
    path = Path(path)
    examples: List[GoldenExample] = []
    with path.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            examples.append(GoldenExample.from_dict(json.loads(line)))
    return examples


def save_golden(examples: List[GoldenExample], path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        for ex in examples:
            f.write(json.dumps(ex.to_dict(), ensure_ascii=False) + "\n")


def load_corpus(path: str | Path) -> List[Passage]:
    path = Path(path)
    passages: List[Passage] = []
    with path.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            passages.append(Passage.from_dict(json.loads(line)))
    return passages


def save_corpus(passages: List[Passage], path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        for p in passages:
            f.write(json.dumps(p.to_dict(), ensure_ascii=False) + "\n")

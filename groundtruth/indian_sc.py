"""Load real Indian Supreme Court judgments from the AWS Open Data bucket.

Source: s3://indian-supreme-court-judgments/  (CC-BY-4.0)
Registry: https://registry.opendata.aws/indian-supreme-court-judgments/

No AWS account required — use --no-sign-request.
"""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from typing import Iterator, List, Optional

from .schema import Passage


BUCKET = "s3://indian-supreme-court-judgments"
DEFAULT_RAW_DIR = Path("data/indian_sc/raw")
DEFAULT_TEXT_DIR = Path("data/indian_sc/text")


def _aws_cp(s3_uri: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["aws", "s3", "cp", s3_uri, str(dest), "--no-sign-request"]
    subprocess.run(cmd, check=True, capture_output=True)


def list_english_pdfs(year: int) -> List[str]:
    """Return PDF filenames for a year from the public index."""
    index_uri = f"{BUCKET}/data/tar/year={year}/english/english.index.json"
    local = DEFAULT_RAW_DIR / f"english_{year}.index.json"
    if not local.exists():
        _aws_cp(index_uri, local)
    idx = json.loads(local.read_text())
    files: List[str] = []
    for part in idx.get("parts", []):
        files.extend(part.get("files", []))
    return files


def download_pdf(year: int, filename: str, dest_dir: Path = DEFAULT_RAW_DIR) -> Path:
    """Download one English judgment PDF."""
    s3_uri = f"{BUCKET}/data/pdf/year={year}/english/{filename}"
    dest = dest_dir / filename
    if not dest.exists():
        _aws_cp(s3_uri, dest)
    return dest


def extract_text(pdf_path: Path) -> str:
    """Extract plain text from a judgment PDF via pypdf."""
    from pypdf import PdfReader

    reader = PdfReader(str(pdf_path))
    parts = []
    for page in reader.pages:
        t = page.extract_text()
        if t:
            parts.append(t)
    # Normalize whitespace a bit
    text = "\n".join(parts)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def judgment_id_from_filename(filename: str) -> str:
    """2023_10_1001_1009_EN.pdf → 2023_10_1001_1009"""
    stem = Path(filename).stem
    if stem.endswith("_EN"):
        stem = stem[:-3]
    return stem


def load_judgment(
    year: int,
    filename: str,
    raw_dir: Path = DEFAULT_RAW_DIR,
    text_dir: Path = DEFAULT_TEXT_DIR,
    force: bool = False,
) -> dict:
    """
    Download (if needed), extract text, cache as .txt, return metadata + text.

    Returns:
        {
          "id": "2023_10_1001_1009",
          "year": 2023,
          "filename": "...",
          "text": "...",
          "char_count": int,
          "source": "s3://.../filename",
        }
    """
    pdf_path = download_pdf(year, filename, raw_dir)
    jid = judgment_id_from_filename(filename)
    text_path = text_dir / f"{jid}.txt"
    text_dir.mkdir(parents=True, exist_ok=True)

    if text_path.exists() and not force:
        text = text_path.read_text(encoding="utf-8")
    else:
        text = extract_text(pdf_path)
        text_path.write_text(text, encoding="utf-8")

    return {
        "id": jid,
        "year": year,
        "filename": filename,
        "text": text,
        "char_count": len(text),
        "source": f"{BUCKET}/data/pdf/year={year}/english/{filename}",
    }


def chunk_judgment(
    judgment: dict,
    chunk_size: int = 800,
    overlap: int = 100,
) -> List[Passage]:
    """
    Split judgment text into overlapping character windows.

    chunk_size / overlap are in characters (simple, deterministic).
    For legal text, ~600–1000 chars ≈ 1–2 paragraphs — good first default.
    Passage IDs: {judgment_id}__c{n:03d}
    """
    text = judgment["text"]
    jid = judgment["id"]
    source = judgment["source"]
    if not text:
        return []

    passages: List[Passage] = []
    start = 0
    n = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        # Prefer to break on paragraph or sentence boundary when possible
        if end < len(text):
            # look back for a paragraph break
            window = text[start:end]
            br = window.rfind("\n\n")
            if br > chunk_size // 2:
                end = start + br
            else:
                br = window.rfind(". ")
                if br > chunk_size // 2:
                    end = start + br + 1

        chunk = text[start:end].strip()
        if chunk:
            passages.append(
                Passage(
                    id=f"{jid}__c{n:03d}",
                    text=chunk,
                    source=source,
                    metadata={
                        "judgment_id": jid,
                        "year": judgment["year"],
                        "chunk_index": n,
                        "char_start": start,
                        "char_end": end,
                    },
                )
            )
            n += 1
        if end >= len(text):
            break
        start = max(end - overlap, start + 1)

    return passages


def sample_judgments(
    year: int,
    n: int = 10,
    raw_dir: Path = DEFAULT_RAW_DIR,
) -> List[dict]:
    """Download and extract the first n English judgments for a year."""
    files = list_english_pdfs(year)
    out = []
    for filename in files[:n]:
        try:
            out.append(load_judgment(year, filename, raw_dir=raw_dir))
        except Exception as e:
            print(f"skip {filename}: {e}")
    return out


def passages_from_sample(
    year: int,
    n_judgments: int = 10,
    chunk_size: int = 800,
    overlap: int = 100,
) -> List[Passage]:
    """End-to-end: sample judgments → extract → chunk → Passage list."""
    judgments = sample_judgments(year, n=n_judgments)
    passages: List[Passage] = []
    for j in judgments:
        passages.extend(chunk_judgment(j, chunk_size=chunk_size, overlap=overlap))
    return passages

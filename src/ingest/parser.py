"""PDF parsing: extract text page by page, keeping source file and page number."""

import unicodedata
from dataclasses import dataclass
from pathlib import Path

import pymupdf


@dataclass(frozen=True)
class Page:
    source: str  # PDF filename, used for citations
    page: int  # 1-based page number
    text: str
    language: str = "unknown"


def clean_text(text: str) -> str:
    """Normalize Unicode (fixes Arabic presentation forms) and drop blank lines."""
    text = unicodedata.normalize("NFKC", text)
    lines = [line.strip() for line in text.splitlines()]
    return "\n".join(line for line in lines if line)


def extract_pages(pdf_path: Path) -> list[Page]:
    pages = []
    with pymupdf.open(pdf_path) as doc:
        for number, page in enumerate(doc, start=1):
            pages.append(
                Page(
                    source=pdf_path.name,
                    page=number,
                    text=clean_text(page.get_text("text")),
                    language=pdf_path.parent.name,
                )
            )
    return pages

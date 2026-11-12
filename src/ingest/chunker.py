"""Split parsed pages into overlapping chunks that keep source and page metadata."""

from collections.abc import Iterator
from dataclasses import dataclass

from ingest.parser import Page

MIN_PAGE_CHARS = 50  # pages shorter than this are covers/blank pages


@dataclass(frozen=True)
class Chunk:
    chunk_id: str  # e.g. "labor_law_en.pdf:p12:c0"
    source: str
    page: int
    text: str
    language: str = "unknown"


def _units(text: str, limit: int) -> Iterator[str]:
    """Yield lines; break any line longer than `limit` on word boundaries."""
    for line in text.splitlines():
        if len(line) <= limit:
            yield line
            continue
        current = ""
        for word in line.split():
            if current and len(current) + 1 + len(word) > limit:
                yield current
                current = word
            else:
                current = f"{current} {word}".strip()
        if current:
            yield current


def split_text(text: str, chunk_size: int = 1200, overlap: int = 200) -> list[str]:
    """Group lines into chunks of about `chunk_size` characters.

    The end of each chunk is repeated at the start of the next one (`overlap`),
    so an idea cut at a boundary still appears whole in one of the chunks.
    """
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    chunks: list[str] = []
    current: list[str] = []
    for unit in _units(text, chunk_size):
        length = len("\n".join(current + [unit]))
        if current and length > chunk_size:
            chunks.append("\n".join(current))
            tail: list[str] = []
            tail_len = 0
            for previous in reversed(current):
                if tail_len + len(previous) + 1 > overlap:
                    break
                tail.insert(0, previous)
                tail_len += len(previous) + 1
            current = tail
        current.append(unit)
    if current:
        chunks.append("\n".join(current))
    return chunks


def chunk_pages(pages: list[Page], chunk_size: int = 1200, overlap: int = 200) -> list[Chunk]:
    chunks = []
    for page in pages:
        if len(page.text) < MIN_PAGE_CHARS:
            continue
        for index, text in enumerate(split_text(page.text, chunk_size, overlap)):
            chunks.append(
                Chunk(
                    chunk_id=f"{page.source}:p{page.page}:c{index}",
                    source=page.source,
                    page=page.page,
                    text=text,
                    language=page.language,
                )
            )
    return chunks

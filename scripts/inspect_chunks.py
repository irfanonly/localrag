from pathlib import Path

from ingest.chunker import chunk_pages
from ingest.parser import extract_pages

SCRATCH = Path("scratch")
SCRATCH.mkdir(exist_ok=True)

for pdf in sorted(Path("data/samples").rglob("*.pdf")):
    chunks = chunk_pages(extract_pages(pdf))
    sizes = [len(c.text) for c in chunks]
    print(
        f"{pdf.name}: {len(chunks)} chunks, "
        f"min {min(sizes)} / avg {sum(sizes) // len(sizes)} / max {max(sizes)} chars"
    )
    sample = chunks[len(chunks) // 2]
    (SCRATCH / f"{pdf.stem}_chunk.txt").write_text(
        f"{sample.chunk_id}\n\n{sample.text}", encoding="utf-8"
    )

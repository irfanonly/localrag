from pathlib import Path

from ingest.parser import extract_pages

SAMPLES = Path("data/samples")
SCRATCH = Path("scratch")
SCRATCH.mkdir(exist_ok=True)

for pdf in sorted(SAMPLES.rglob("*.pdf")):
    pages = extract_pages(pdf)
    empty = sum(1 for p in pages if len(p.text) < 20)
    chars = sum(len(p.text) for p in pages)
    print(f"{pdf.name}: {len(pages)} pages, {chars} chars, {empty} near-empty pages")

    # Save page 5 (or the last page) so we can read it in an editor
    sample = pages[min(4, len(pages) - 1)]
    (SCRATCH / f"{pdf.stem}_sample.txt").write_text(sample.text, encoding="utf-8")

import time
from pathlib import Path

from ingest.chunker import chunk_pages
from ingest.parser import extract_pages
from retrieval.store import add_chunks, get_collection

start = time.perf_counter()
chunks = []
for pdf in sorted(Path("data/samples").rglob("*.pdf")):
    chunks.extend(chunk_pages(extract_pages(pdf)))
print(f"{len(chunks)} chunks from documents")

collection = get_collection(reset=True)
add_chunks(collection, chunks)
print(f"Indexed {collection.count()} chunks in {time.perf_counter() - start:.0f}s")

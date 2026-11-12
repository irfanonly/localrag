"""Chroma vector store: add chunks, search by meaning, filter by language."""

import chromadb
from chromadb.config import Settings

from ingest.chunker import Chunk
from retrieval.embedder import embed

DB_PATH = "chroma_db"
COLLECTION = "labor_law"


def get_collection(reset: bool = False):
    # Telemetry is disabled so nothing is reported outside the machine.
    client = chromadb.PersistentClient(path=DB_PATH, settings=Settings(anonymized_telemetry=False))
    if reset:
        try:
            client.delete_collection(COLLECTION)
        except Exception:  # the collection may not exist yet
            pass
    return client.get_or_create_collection(COLLECTION, metadata={"hnsw:space": "cosine"})


def add_chunks(collection, chunks: list[Chunk], batch_size: int = 64) -> None:
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i : i + batch_size]
        collection.add(
            ids=[c.chunk_id for c in batch],
            documents=[c.text for c in batch],
            embeddings=embed([c.text for c in batch]),
            metadatas=[{"source": c.source, "page": c.page, "language": c.language} for c in batch],
        )


def search(collection, query: str, k: int = 5, language: str | None = None) -> list[dict]:
    where = {"language": language} if language else None
    result = collection.query(query_embeddings=embed([query]), n_results=k, where=where)
    return [
        {
            "text": doc,
            "source": meta["source"],
            "page": meta["page"],
            "language": meta["language"],
            "score": 1 - dist,  # cosine similarity, higher is better
        }
        for doc, meta, dist in zip(
            result["documents"][0], result["metadatas"][0], result["distances"][0], strict=True
        )
    ]

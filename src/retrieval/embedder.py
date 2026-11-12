"""Turn text into vectors with a local multilingual model (no data leaves the machine)."""

from functools import lru_cache

from sentence_transformers import SentenceTransformer

MODEL_NAME = "BAAI/bge-m3"


@lru_cache(maxsize=1)
def get_model() -> SentenceTransformer:
    model = SentenceTransformer(MODEL_NAME)
    model.max_seq_length = 512  # limits memory use; our chunks fit comfortably
    return model


def embed(texts: list[str], batch_size: int = 16) -> list[list[float]]:
    vectors = get_model().encode(
        texts,
        batch_size=batch_size,
        normalize_embeddings=True,  # lets us use cosine similarity
        show_progress_bar=len(texts) > 32,
    )
    return vectors.tolist()

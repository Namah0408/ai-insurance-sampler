from functools import lru_cache

from sentence_transformers import SentenceTransformer

from app.core.config import settings


@lru_cache
def get_embedding_model() -> SentenceTransformer:

    return SentenceTransformer(
        settings.rag_embedding_model
    )


def generate_embeddings(
    texts: list[str],
) -> list[list[float]]:

    if not texts:
        return []

    model = get_embedding_model()

    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=False,
    )

    return embeddings.tolist()


def generate_query_embedding(
    query: str,
) -> list[float]:

    model = get_embedding_model()

    embedding = model.encode(
        query,
        normalize_embeddings=True,
        show_progress_bar=False,
    )

    return embedding.tolist()
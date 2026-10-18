from typing import Any

from app.core.config import settings
from app.rag.embeddings import generate_query_embedding
from app.rag.vector_store import search_documents


def retrieve_knowledge(
    query: str,
    top_k: int | None = None,
) -> list[dict[str, Any]]:

    if not query.strip():
        return []

    top_k = (
        top_k
        if top_k is not None
        else settings.rag_top_k
    )

    query_embedding = generate_query_embedding(
        query
    )

    result = search_documents(
        query_embedding=query_embedding,
        top_k=top_k,
    )

    documents = result.get(
        "documents",
        [[]],
    )[0]

    metadatas = result.get(
        "metadatas",
        [[]],
    )[0]

    distances = result.get(
        "distances",
        [[]],
    )[0]

    retrieved = []

    for index, document in enumerate(documents):

        metadata = (
            metadatas[index]
            if index < len(metadatas)
            else {}
        )

        distance = (
            distances[index]
            if index < len(distances)
            else None
        )

        retrieved.append(
            {
                "text": document,
                "metadata": metadata,
                "distance": distance,
            }
        )

    return retrieved
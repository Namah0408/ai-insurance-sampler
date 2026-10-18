from functools import lru_cache
from typing import Any

import chromadb

from app.core.config import settings


@lru_cache
def get_chroma_client():

    return chromadb.PersistentClient(
        path=settings.rag_vector_store_path
    )


@lru_cache
def get_collection():

    client = get_chroma_client()

    return client.get_or_create_collection(
        name=settings.rag_collection_name,
        metadata={
            "description": (
                "AI Insurance Sampler knowledge base"
            )
        },
    )


def add_documents(
    ids: list[str],
    documents: list[str],
    embeddings: list[list[float]],
    metadatas: list[dict[str, Any]],
):

    collection = get_collection()

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )


def search_documents(
    query_embedding: list[float],
    top_k: int,
):

    collection = get_collection()

    result = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=[
            "documents",
            "metadatas",
            "distances",
        ],
    )

    return result


def get_collection_count() -> int:

    collection = get_collection()

    return collection.count()
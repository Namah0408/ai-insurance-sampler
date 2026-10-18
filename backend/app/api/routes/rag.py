import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.knowledge_document import KnowledgeDocument
from app.rag.ingestion import ingest_knowledge_document
from app.rag.retrieval import retrieve_knowledge
from app.rag.vector_store import get_collection_count
from app.schemas.rag import (
    KnowledgeDocumentResponse,
    KnowledgeIngestResponse,
    KnowledgeSearchRequest,
    KnowledgeSearchResponse,
    KnowledgeSearchResult,
)


router = APIRouter(
    prefix="/rag",
    tags=["RAG Knowledge"],
)


@router.post(
    "/ingest",
    response_model=KnowledgeIngestResponse,
)
def ingest_document(
    file_path: str,
    document_name: str,
    document_type: str,
    version: str,
    source: str,
    description: str | None = None,
    effective_date: datetime | None = None,
    db: Session = Depends(get_db),
):

    try:

        result = ingest_knowledge_document(
            file_path=file_path,
            document_name=document_name,
            document_type=document_type,
            version=version,
            source=source,
            description=description,
            effective_date=effective_date,
            db=db,
        )

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Knowledge ingestion failed: {error}",
        )

    return KnowledgeIngestResponse(
        document=result["document"],
        chunk_count=result["chunk_count"],
    )


@router.post(
    "/search",
    response_model=KnowledgeSearchResponse,
)
def search_knowledge(
    request: KnowledgeSearchRequest,
):

    try:

        results = retrieve_knowledge(
            query=request.query,
            top_k=request.top_k,
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Knowledge retrieval failed: {error}",
        )

    return KnowledgeSearchResponse(
        query=request.query,
        results=[
            KnowledgeSearchResult(**result)
            for result in results
        ],
    )


@router.get(
    "/documents",
    response_model=list[
        KnowledgeDocumentResponse
    ],
)
def list_knowledge_documents(
    db: Session = Depends(get_db),
):

    return (
        db.query(KnowledgeDocument)
        .order_by(
            KnowledgeDocument.created_at.desc()
        )
        .all()
    )


@router.get(
    "/stats",
)
def get_rag_stats():

    return {
        "collection_count": get_collection_count(),
    }
import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class KnowledgeDocumentResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: uuid.UUID
    document_name: str
    document_type: str
    version: str
    effective_date: datetime | None
    source: str
    description: str | None
    file_path: str
    active: bool
    chunk_count: int
    created_at: datetime


class KnowledgeIngestResponse(BaseModel):

    document: KnowledgeDocumentResponse
    chunk_count: int


class KnowledgeSearchRequest(BaseModel):

    query: str
    top_k: int | None = None


class KnowledgeSearchResult(BaseModel):

    text: str
    metadata: dict[str, Any]
    distance: float | None


class KnowledgeSearchResponse(BaseModel):

    query: str
    results: list[KnowledgeSearchResult]
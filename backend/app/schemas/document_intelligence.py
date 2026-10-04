import uuid
from datetime import datetime

from pydantic import BaseModel


class ExtractedFieldResponse(BaseModel):
    id: uuid.UUID
    field_name: str
    field_value: str | None
    confidence: float
    source_page: int | None
    source_text: str | None
    validation_status: str
    created_at: datetime


class DocumentIntelligenceResponse(BaseModel):
    document_id: uuid.UUID
    document_type: str
    status: str
    extracted_text: str
    fields: list[ExtractedFieldResponse]
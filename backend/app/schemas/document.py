import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class DocumentCreate(BaseModel):
    document_type: str = Field(
        min_length=1,
        max_length=50,
    )

    file_name: str = Field(
        min_length=1,
        max_length=255,
    )

    file_path: str | None = Field(
        default=None,
        max_length=500,
    )


class DocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    proposal_id: uuid.UUID
    document_type: str
    file_name: str
    file_path: str | None
    status: str
    created_at: datetime
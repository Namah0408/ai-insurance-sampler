import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class IntegrationResultResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    proposal_id: uuid.UUID
    provider: str
    status: str
    response_data: dict[str, Any]
    error_message: str | None
    created_at: datetime


class IntegrationRunResponse(BaseModel):

    proposal_id: uuid.UUID
    results: list[IntegrationResultResponse]
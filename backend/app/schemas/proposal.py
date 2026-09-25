import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ProposalCreate(BaseModel):
    customer_id: uuid.UUID

    proposal_number: str = Field(
        min_length=1,
        max_length=50,
    )

    product_name: str = Field(
        min_length=1,
        max_length=150,
    )

    sum_assured: float = Field(
        gt=0,
    )

    annual_premium: float = Field(
        gt=0,
    )


class ProposalStatusUpdate(BaseModel):
    status: str = Field(
        min_length=1,
        max_length=30,
    )


class ProposalResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    proposal_number: str
    customer_id: uuid.UUID
    product_name: str
    sum_assured: float
    annual_premium: float
    status: str
    created_at: datetime
    updated_at: datetime
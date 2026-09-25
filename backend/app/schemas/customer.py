import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CustomerCreate(BaseModel):
    customer_reference: str = Field(
        min_length=1,
        max_length=50,
    )

    full_name: str = Field(
        min_length=1,
        max_length=150,
    )

    date_of_birth: datetime | None = None


class CustomerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    customer_reference: str
    full_name: str
    date_of_birth: datetime | None
    created_at: datetime
    updated_at: datetime
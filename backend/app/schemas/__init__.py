from app.schemas.customer import CustomerCreate, CustomerResponse
from app.schemas.document import DocumentCreate, DocumentResponse
from app.schemas.proposal import (
    ProposalCreate,
    ProposalResponse,
    ProposalStatusUpdate,
)

__all__ = [
    "CustomerCreate",
    "CustomerResponse",
    "DocumentCreate",
    "DocumentResponse",
    "ProposalCreate",
    "ProposalResponse",
    "ProposalStatusUpdate",
]
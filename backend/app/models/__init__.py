from app.models.customer import Customer
from app.models.document import Document
from app.models.document_field import DocumentField
from app.models.integration_result import IntegrationResult
from app.models.proposal import Proposal
from app.models.risk_assessment import RiskAssessment
from app.models.risk_flag import RiskFlag


__all__ = [
    "Customer",
    "Proposal",
    "Document",
    "DocumentField",
    "IntegrationResult",
    "RiskAssessment",
    "RiskFlag",
]
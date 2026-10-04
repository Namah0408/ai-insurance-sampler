import re
import uuid
from typing import Any

from sqlalchemy.orm import Session

from app.integrations.base import ExternalIntegration
from app.models.customer import Customer
from app.models.document import Document
from app.models.document_field import DocumentField
from app.models.proposal import Proposal


class KarzaIntegration(ExternalIntegration):

    @property
    def provider_name(self) -> str:
        return "KARZA"

    def __init__(self, db: Session):
        self.db = db

    def _get_field(
        self,
        document_id: uuid.UUID,
        field_name: str,
    ) -> str | None:

        field = (
            self.db.query(DocumentField)
            .filter(
                DocumentField.document_id == document_id,
                DocumentField.field_name == field_name,
            )
            .first()
        )

        if not field:
            return None

        return field.field_value

    def check(self, proposal_id: uuid.UUID) -> dict[str, Any]:

        proposal = (
            self.db.query(Proposal)
            .filter(Proposal.id == proposal_id)
            .first()
        )

        if not proposal:
            raise ValueError("Proposal not found.")

        customer = (
            self.db.query(Customer)
            .filter(Customer.id == proposal.customer_id)
            .first()
        )

        if not customer:
            raise ValueError("Customer not found.")

        documents = (
            self.db.query(Document)
            .filter(Document.proposal_id == proposal_id)
            .all()
        )

        pan_number = None
        aadhaar_number = None
        pan_name = None
        aadhaar_name = None

        for document in documents:

            if document.document_type == "PAN":

                pan_number = self._get_field(
                    document.id,
                    "pan_number",
                )

                pan_name = self._get_field(
                    document.id,
                    "full_name",
                )

            elif document.document_type == "AADHAAR":

                aadhaar_number = self._get_field(
                    document.id,
                    "aadhaar_number",
                )

                aadhaar_name = self._get_field(
                    document.id,
                    "full_name",
                )

        normalized_pan = (
            pan_number.upper().strip()
            if pan_number
            else None
        )

        normalized_aadhaar = (
            re.sub(r"\s+", "", aadhaar_number)
            if aadhaar_number
            else None
        )

        normalized_pan_name = (
            pan_name.upper().strip()
            if pan_name
            else None
        )

        normalized_aadhaar_name = (
            aadhaar_name.upper().strip()
            if aadhaar_name
            else None
        )

        name_match = False

        if normalized_pan_name and normalized_aadhaar_name:
            name_match = (
                normalized_pan_name == normalized_aadhaar_name
            )

        identity_available = bool(
            normalized_pan and normalized_aadhaar
        )

        verification_status = (
            "verified"
            if identity_available and name_match
            else "refer"
        )

        return {
            "provider": self.provider_name,
            "mode": "mock",
            "success": True,
            "proposal_id": str(proposal_id),
            "verification_status": verification_status,
            "pan": {
                "available": bool(normalized_pan),
                "value": normalized_pan,
            },
            "aadhaar": {
                "available": bool(normalized_aadhaar),
                "value": normalized_aadhaar,
            },
            "checks": {
                "pan_aadhaar_linked": identity_available,
                "name_match": name_match,
                "pan_issue_date_available": False,
            },
            "message": "Mock Karza KYC verification completed.",
        }
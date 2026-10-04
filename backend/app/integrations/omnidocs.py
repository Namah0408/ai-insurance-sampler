import uuid
from typing import Any

from sqlalchemy.orm import Session

from app.models.document import Document
from app.models.proposal import Proposal
from app.integrations.base import ExternalIntegration


class OmniDocsIntegration(ExternalIntegration):

    @property
    def provider_name(self) -> str:
        return "OMNIDOCS"

    def __init__(self, db: Session):
        self.db = db

    def check(self, proposal_id: uuid.UUID) -> dict[str, Any]:

        proposal = (
            self.db.query(Proposal)
            .filter(Proposal.id == proposal_id)
            .first()
        )

        if not proposal:
            raise ValueError("Proposal not found.")

        documents = (
            self.db.query(Document)
            .filter(Document.proposal_id == proposal_id)
            .all()
        )

        document_list = []

        for document in documents:
            document_list.append(
                {
                    "document_id": str(document.id),
                    "document_type": document.document_type,
                    "file_name": document.file_name,
                    "status": document.status,
                }
            )

        return {
            "provider": self.provider_name,
            "mode": "mock",
            "success": True,
            "proposal_id": str(proposal_id),
            "documents": document_list,
            "document_count": len(document_list),
            "message": "Mock OmniDocs document retrieval successful.",
        }
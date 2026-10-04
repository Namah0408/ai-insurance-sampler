import uuid
from typing import Any

from sqlalchemy.orm import Session

from app.integrations.base import ExternalIntegration
from app.models.customer import Customer
from app.models.proposal import Proposal


class IIBIntegration(ExternalIntegration):

    @property
    def provider_name(self) -> str:
        return "IIB"

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

        customer = (
            self.db.query(Customer)
            .filter(Customer.id == proposal.customer_id)
            .first()
        )

        if not customer:
            raise ValueError("Customer not found.")

        # -----------------------------------------------------
        # MOCK DATA ONLY
        # -----------------------------------------------------

        existing_policies = [
            {
                "insurer": "Demo Life Insurance",
                "policy_number": "DEMO-IIB-001",
                "sum_assured": 2000000,
                "status": "active",
            }
        ]

        total_sum_assured = sum(
            policy["sum_assured"]
            for policy in existing_policies
        )

        return {
            "provider": self.provider_name,
            "mode": "mock",
            "success": True,
            "proposal_id": str(proposal_id),
            "existing_policy_count": len(existing_policies),
            "total_existing_sum_assured": total_sum_assured,
            "policies": existing_policies,
            "multiple_insurer_flag": False,
            "message": "Mock IIB insurance exposure check completed.",
        }
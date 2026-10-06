import uuid
from typing import Any

from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.integration_result import IntegrationResult
from app.models.proposal import Proposal


def analyze_kyc(
    proposal_id: uuid.UUID,
    db: Session,
) -> dict[str, Any]:

    proposal = (
        db.query(Proposal)
        .filter(Proposal.id == proposal_id)
        .first()
    )

    if not proposal:
        raise ValueError("Proposal not found.")

    customer = (
        db.query(Customer)
        .filter(Customer.id == proposal.customer_id)
        .first()
    )

    if not customer:
        raise ValueError("Customer not found.")

    karza_result = (
        db.query(IntegrationResult)
        .filter(
            IntegrationResult.proposal_id == proposal_id,
            IntegrationResult.provider == "KARZA",
            IntegrationResult.status == "success",
        )
        .order_by(IntegrationResult.created_at.desc())
        .first()
    )

    findings = []
    flags = []

    if not karza_result:
        return {
            "analysis_type": "KYC",
            "status": "insufficient_data",
            "risk_level": "UNKNOWN",
            "findings": [
                "No successful Karza verification result is available."
            ],
            "flags": [
                "KARZA_RESULT_MISSING"
            ],
        }

    response = karza_result.response_data

    verification_status = response.get(
        "verification_status",
        "unknown",
    )

    checks = response.get("checks", {})

    pan_aadhaar_linked = checks.get(
        "pan_aadhaar_linked",
        False,
    )

    name_match = checks.get(
        "name_match",
        False,
    )

    if verification_status == "verified":
        findings.append(
            "Identity verification returned a verified status."
        )
    else:
        findings.append(
            "Identity verification requires review."
        )
        flags.append("IDENTITY_VERIFICATION_REVIEW")

    if pan_aadhaar_linked:
        findings.append(
            "PAN and Aadhaar information is available for verification."
        )
    else:
        flags.append("PAN_AADHAAR_DATA_INCOMPLETE")
        findings.append(
            "PAN/Aadhaar linkage information is incomplete."
        )

    if name_match:
        findings.append(
            "Name consistency check passed."
        )
    else:
        flags.append("NAME_MISMATCH")
        findings.append(
            "Name consistency check did not pass."
        )

    if verification_status == "verified" and not flags:
        risk_level = "LOW"
        status = "completed"
    elif flags:
        risk_level = "MEDIUM"
        status = "completed"
    else:
        risk_level = "UNKNOWN"
        status = "completed"

    return {
        "analysis_type": "KYC",
        "status": status,
        "risk_level": risk_level,
        "findings": findings,
        "flags": flags,
        "customer_id": str(customer.id),
        "provider": "KARZA",
    }
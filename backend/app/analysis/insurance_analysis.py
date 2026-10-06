import uuid
from typing import Any

from sqlalchemy.orm import Session

from app.models.integration_result import IntegrationResult
from app.models.proposal import Proposal


def analyze_insurance_exposure(
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

    iib_result = (
        db.query(IntegrationResult)
        .filter(
            IntegrationResult.proposal_id == proposal_id,
            IntegrationResult.provider == "IIB",
            IntegrationResult.status == "success",
        )
        .order_by(
            IntegrationResult.created_at.desc()
        )
        .first()
    )

    if not iib_result:

        return {
            "analysis_type": "INSURANCE_EXPOSURE",
            "status": "insufficient_data",
            "risk_level": "UNKNOWN",
            "existing_policy_count": None,
            "total_existing_sum_assured": None,
            "multiple_insurer_flag": None,
            "findings": [
                "No successful IIB result is available."
            ],
            "flags": [
                "IIB_RESULT_MISSING"
            ],
        }

    response = iib_result.response_data

    existing_policy_count = response.get(
        "existing_policy_count",
        0,
    )

    total_existing_sum_assured = response.get(
        "total_existing_sum_assured",
        0,
    )

    multiple_insurer_flag = response.get(
        "multiple_insurer_flag",
        False,
    )

    findings = []
    flags = []

    findings.append(
        f"Existing insurance policies found: "
        f"{existing_policy_count}."
    )

    findings.append(
        f"Total existing sum assured: "
        f"INR {total_existing_sum_assured:,.2f}."
    )

    if multiple_insurer_flag:

        flags.append("MULTIPLE_INSURER_EXPOSURE")

        findings.append(
            "Multiple insurer exposure was reported."
        )

    if existing_policy_count == 0:

        risk_level = "LOW"

    elif flags:

        risk_level = "MEDIUM"

    else:

        risk_level = "LOW"

    return {
        "analysis_type": "INSURANCE_EXPOSURE",
        "status": "completed",
        "risk_level": risk_level,
        "existing_policy_count": existing_policy_count,
        "total_existing_sum_assured": total_existing_sum_assured,
        "multiple_insurer_flag": multiple_insurer_flag,
        "findings": findings,
        "flags": flags,
    }
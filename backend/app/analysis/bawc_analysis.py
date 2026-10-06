import uuid
from typing import Any

from sqlalchemy.orm import Session

from app.models.document import Document
from app.models.proposal import Proposal


def analyze_bawc(
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

    bawc_documents = (
        db.query(Document)
        .filter(
            Document.proposal_id == proposal_id,
            Document.document_type == "BAWC",
        )
        .all()
    )

    findings = []
    flags = []

    if not bawc_documents:

        findings.append(
            "No BAWC document/evidence was found for this proposal."
        )

        flags.append("BAWC_EVIDENCE_MISSING")

        return {
            "analysis_type": "BAWC",
            "status": "insufficient_data",
            "risk_level": "MEDIUM",
            "documents_found": 0,
            "processed_documents": 0,
            "findings": findings,
            "flags": flags,
        }

    processed_documents = 0

    for document in bawc_documents:

        if document.status == "processed":
            processed_documents += 1

    findings.append(
        f"BAWC documents found: {len(bawc_documents)}."
    )

    findings.append(
        f"BAWC documents processed: {processed_documents}."
    )

    if processed_documents == 0:

        flags.append("BAWC_NOT_PROCESSED")

        risk_level = "MEDIUM"

    elif processed_documents < len(bawc_documents):

        flags.append("BAWC_PARTIALLY_PROCESSED")

        risk_level = "MEDIUM"

    else:

        risk_level = "LOW"

    return {
        "analysis_type": "BAWC",
        "status": "completed",
        "risk_level": risk_level,
        "documents_found": len(bawc_documents),
        "processed_documents": processed_documents,
        "findings": findings,
        "flags": flags,
    }
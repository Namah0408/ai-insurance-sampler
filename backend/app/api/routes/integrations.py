import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.integrations.service import run_all_integrations
from app.models.integration_result import IntegrationResult
from app.models.proposal import Proposal
from app.schemas.integration import (
    IntegrationResultResponse,
    IntegrationRunResponse,
)


router = APIRouter(
    prefix="/proposals",
    tags=["External Integrations"],
)


@router.post(
    "/{proposal_id}/integrations/run",
    response_model=IntegrationRunResponse,
)
def run_integrations(
    proposal_id: uuid.UUID,
    db: Session = Depends(get_db),
):

    proposal = (
        db.query(Proposal)
        .filter(Proposal.id == proposal_id)
        .first()
    )

    if not proposal:
        raise HTTPException(
            status_code=404,
            detail="Proposal not found",
        )

    results = run_all_integrations(
        proposal_id=proposal_id,
        db=db,
    )

    saved_results = []

    for result in results:

        response_data = result.get(
            "response",
            {},
        )

        error_message = None

        if result["status"] == "failed":
            error_message = response_data.get("error")

        db_result = IntegrationResult(
            proposal_id=proposal_id,
            provider=result["provider"],
            status=result["status"],
            response_data=response_data,
            error_message=error_message,
        )

        db.add(db_result)
        saved_results.append(db_result)

    db.commit()

    for result in saved_results:
        db.refresh(result)

    return IntegrationRunResponse(
        proposal_id=proposal_id,
        results=saved_results,
    )


@router.get(
    "/{proposal_id}/integrations",
    response_model=list[IntegrationResultResponse],
)
def get_integration_results(
    proposal_id: uuid.UUID,
    db: Session = Depends(get_db),
):

    proposal = (
        db.query(Proposal)
        .filter(Proposal.id == proposal_id)
        .first()
    )

    if not proposal:
        raise HTTPException(
            status_code=404,
            detail="Proposal not found",
        )

    results = (
        db.query(IntegrationResult)
        .filter(
            IntegrationResult.proposal_id == proposal_id
        )
        .order_by(
            IntegrationResult.created_at.desc()
        )
        .all()
    )

    return results
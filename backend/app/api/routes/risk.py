import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.risk_assessment import RiskAssessment
from app.schemas.risk import (
    RiskAssessmentInput,
    RiskAssessmentResponse,
)
from app.services.risk_service import (
    assess_proposal,
    get_assessment,
)


router = APIRouter(
    prefix="/proposals",
    tags=["Risk Assessment"],
)


@router.post(
    "/{proposal_id}/assess",
    response_model=RiskAssessmentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_risk_assessment(
    proposal_id: uuid.UUID,
    assessment_data: RiskAssessmentInput,
    db: Session = Depends(get_db),
):
    assessment = assess_proposal(
        proposal_id=proposal_id,
        data=assessment_data,
        db=db,
    )

    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proposal not found",
        )

    return assessment


@router.get(
    "/{proposal_id}/risk",
    response_model=RiskAssessmentResponse,
)
def get_risk_assessment(
    proposal_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    assessment = get_assessment(
        proposal_id=proposal_id,
        db=db,
    )

    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Risk assessment not found",
        )

    return assessment
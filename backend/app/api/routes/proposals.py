import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.customer import Customer
from app.models.proposal import Proposal
from app.schemas.proposal import (
    ProposalCreate,
    ProposalResponse,
    ProposalStatusUpdate,
)


router = APIRouter(
    prefix="/proposals",
    tags=["Proposals"],
)


@router.post(
    "/",
    response_model=ProposalResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_proposal(
    proposal_data: ProposalCreate,
    db: Session = Depends(get_db),
):
    customer = (
        db.query(Customer)
        .filter(Customer.id == proposal_data.customer_id)
        .first()
    )

    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )

    existing_proposal = (
        db.query(Proposal)
        .filter(
            Proposal.proposal_number
            == proposal_data.proposal_number
        )
        .first()
    )

    if existing_proposal:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Proposal number already exists",
        )

    proposal = Proposal(
        proposal_number=proposal_data.proposal_number,
        customer_id=proposal_data.customer_id,
        product_name=proposal_data.product_name,
        sum_assured=proposal_data.sum_assured,
        annual_premium=proposal_data.annual_premium,
        status="draft",
    )

    db.add(proposal)
    db.commit()
    db.refresh(proposal)

    return proposal


@router.get(
    "/",
    response_model=list[ProposalResponse],
)
def get_proposals(
    db: Session = Depends(get_db),
):
    return db.query(Proposal).order_by(
        Proposal.created_at.desc()
    ).all()


@router.get(
    "/{proposal_id}",
    response_model=ProposalResponse,
)
def get_proposal(
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
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proposal not found",
        )

    return proposal


@router.patch(
    "/{proposal_id}/status",
    response_model=ProposalResponse,
)
def update_proposal_status(
    proposal_id: uuid.UUID,
    status_data: ProposalStatusUpdate,
    db: Session = Depends(get_db),
):
    proposal = (
        db.query(Proposal)
        .filter(Proposal.id == proposal_id)
        .first()
    )

    if not proposal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proposal not found",
        )

    proposal.status = status_data.status

    db.commit()
    db.refresh(proposal)

    return proposal


@router.delete(
    "/{proposal_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_proposal(
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
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proposal not found",
        )

    db.delete(proposal)
    db.commit()
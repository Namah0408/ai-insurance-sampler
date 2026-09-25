import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.document import Document
from app.models.proposal import Proposal
from app.schemas.document import DocumentCreate, DocumentResponse


router = APIRouter(
    prefix="/proposals",
    tags=["Documents"],
)


@router.post(
    "/{proposal_id}/documents",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_document(
    proposal_id: uuid.UUID,
    document_data: DocumentCreate,
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

    document = Document(
        proposal_id=proposal_id,
        document_type=document_data.document_type,
        file_name=document_data.file_name,
        file_path=document_data.file_path,
        status="uploaded",
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document


@router.get(
    "/{proposal_id}/documents",
    response_model=list[DocumentResponse],
)
def get_documents(
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

    return (
        db.query(Document)
        .filter(Document.proposal_id == proposal_id)
        .order_by(Document.created_at.desc())
        .all()
    )
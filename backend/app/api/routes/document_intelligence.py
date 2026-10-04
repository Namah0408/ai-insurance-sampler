import uuid

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    status,
)
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.document import Document
from app.models.document_field import DocumentField
from app.models.proposal import Proposal
from app.schemas.document import DocumentResponse
from app.schemas.document_intelligence import (
    DocumentIntelligenceResponse,
    ExtractedFieldResponse,
)
from app.services.document_intelligence import (
    process_document,
)
from app.services.document_service import (
    save_uploaded_document,
)


router = APIRouter(
    prefix="/proposals",
    tags=["Document Intelligence"],
)


@router.post(
    "/{proposal_id}/documents/upload",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_document(
    proposal_id: uuid.UUID,
    file: UploadFile,
    db: Session = Depends(get_db),
):
    proposal = (
        db.query(Proposal)
        .filter(
            Proposal.id == proposal_id
        )
        .first()
    )

    if not proposal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proposal not found",
        )

    try:
        (
            original_name,
            file_path,
            file_size,
        ) = await save_uploaded_document(
            proposal_id,
            file,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )

    document = Document(
        proposal_id=proposal_id,
        document_type="UNKNOWN",
        file_name=original_name,
        file_path=file_path,
        status="uploaded",
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document


@router.post(
    "/documents/{document_id}/process",
    response_model=DocumentIntelligenceResponse,
)
def process_uploaded_document(
    document_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    try:
        result = process_document(
            document_id=document_id,
            db=db,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Document processing failed: {error}",
        )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )

    return DocumentIntelligenceResponse(
        document_id=result["document"].id,
        document_type=result["document"].document_type,
        status=result["document"].status,
        extracted_text=result["extracted_text"],
        fields=[
            ExtractedFieldResponse.model_validate(
                field
            )
            for field in result["fields"]
        ],
    )


@router.get(
    "/documents/{document_id}/intelligence",
    response_model=DocumentIntelligenceResponse,
)
def get_document_intelligence(
    document_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    document = (
        db.query(Document)
        .filter(
            Document.id == document_id
        )
        .first()
    )

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )

    fields = (
        db.query(DocumentField)
        .filter(
            DocumentField.document_id
            == document_id
        )
        .order_by(
            DocumentField.created_at
        )
        .all()
    )

    return DocumentIntelligenceResponse(
        document_id=document.id,
        document_type=document.document_type,
        status=document.status,
        extracted_text="",
        fields=[
            ExtractedFieldResponse.model_validate(
                field
            )
            for field in fields
        ],
    )
import uuid
from pathlib import Path

from sqlalchemy.orm import Session

from app.models.document import Document
from app.models.document_field import DocumentField
from app.services.document_classifier import (
    classify_document,
)
from app.services.field_extractor import (
    extract_fields,
)
from app.services.field_validator import (
    validate_field,
)
from app.services.ocr_service import (
    extract_text,
)


def process_document(
    document_id: uuid.UUID,
    db: Session,
):

    document = (
        db.query(Document)
        .filter(
            Document.id == document_id
        )
        .first()
    )

    if not document:
        return None

    if not document.file_path:
        raise ValueError(
            "Document does not have a file path."
        )

    file_path = Path(
        document.file_path
    )

    if not file_path.exists():
        raise ValueError(
            "Document file does not exist."
        )

    document.status = "processing"
    db.commit()

    try:
        text, page_count = extract_text(
            str(file_path)
        )

        detected_type, type_confidence = (
            classify_document(
                text,
                document.file_name,
            )
        )

        extracted_fields = extract_fields(
            text,
            detected_type,
        )

        document.document_type = (
            detected_type
        )

        old_fields = (
            db.query(DocumentField)
            .filter(
                DocumentField.document_id
                == document_id
            )
            .all()
        )

        for old_field in old_fields:
            db.delete(old_field)

        db.flush()

        saved_fields = []

        for field in extracted_fields:

            validation_status = (
                validate_field(
                    field.name,
                    field.value,
                )
            )

            db_field = DocumentField(
                document_id=document.id,
                field_name=field.name,
                field_value=field.value,
                confidence=field.confidence,
                source_page=field.source_page,
                source_text=field.source_text,
                validation_status=validation_status,
            )

            db.add(db_field)
            saved_fields.append(db_field)

        document.status = "processed"

        db.commit()

        for field in saved_fields:
            db.refresh(field)

        db.refresh(document)

        return {
            "document": document,
            "document_type_confidence": (
                type_confidence
            ),
            "extracted_text": text,
            "page_count": page_count,
            "fields": saved_fields,
        }

    except Exception:
        document.status = "failed"
        db.commit()
        raise
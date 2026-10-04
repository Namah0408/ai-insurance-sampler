import os
import uuid
from pathlib import Path

from fastapi import UploadFile

from app.core.config import settings


ALLOWED_EXTENSIONS = {
    ".pdf",
    ".png",
    ".jpg",
    ".jpeg",
}


async def save_uploaded_document(
    proposal_id: uuid.UUID,
    file: UploadFile,
) -> tuple[str, str, int]:

    original_name = Path(
        file.filename or "document"
    ).name

    extension = Path(
        original_name
    ).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError(
            "Unsupported file type. "
            "Only PDF, PNG, JPG and JPEG are allowed."
        )

    max_size = (
        settings.max_document_size_mb
        * 1024
        * 1024
    )

    content = await file.read()

    if len(content) > max_size:
        raise ValueError(
            f"File size exceeds "
            f"{settings.max_document_size_mb} MB."
        )

    proposal_folder = (
        Path(settings.document_storage_path)
        / str(proposal_id)
    )

    proposal_folder.mkdir(
        parents=True,
        exist_ok=True,
    )

    document_id = uuid.uuid4()

    safe_name = (
        f"{document_id}{extension}"
    )

    file_path = (
        proposal_folder
        / safe_name
    )

    with open(
        file_path,
        "wb",
    ) as output_file:
        output_file.write(content)

    return (
        original_name,
        str(file_path),
        len(content),
    )
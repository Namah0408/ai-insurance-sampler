from pathlib import Path

import fitz
import pytesseract
from PIL import Image

from app.core.config import settings


def configure_tesseract():
    pytesseract.pytesseract.tesseract_cmd = (
        settings.tesseract_path
    )


def extract_text_from_pdf(
    file_path: str,
) -> tuple[str, int]:

    configure_tesseract()

    document = fitz.open(file_path)

    pages_text = []

    for page in document:
        text = page.get_text("text")

        if text.strip():
            pages_text.append(text)
            continue

        pixmap = page.get_pixmap(
            matrix=fitz.Matrix(2, 2),
            alpha=False,
        )

        image = Image.frombytes(
            "RGB",
            [
                pixmap.width,
                pixmap.height,
            ],
            pixmap.samples,
        )

        ocr_text = pytesseract.image_to_string(
            image,
            lang="eng",
        )

        pages_text.append(ocr_text)

    document.close()

    return (
        "\n".join(pages_text),
        len(pages_text),
    )


def extract_text_from_image(
    file_path: str,
) -> tuple[str, int]:

    configure_tesseract()

    image = Image.open(file_path)

    text = pytesseract.image_to_string(
        image,
        lang="eng",
    )

    return text, 1


def extract_text(
    file_path: str,
) -> tuple[str, int]:

    extension = Path(
        file_path
    ).suffix.lower()

    if extension == ".pdf":
        return extract_text_from_pdf(
            file_path
        )

    return extract_text_from_image(
        file_path
    )
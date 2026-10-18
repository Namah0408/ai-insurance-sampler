from pathlib import Path

import fitz


def load_pdf(file_path: str) -> str:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Knowledge document not found: {file_path}"
        )

    if path.suffix.lower() != ".pdf":
        raise ValueError(
            "Only PDF knowledge documents are supported."
        )

    document = fitz.open(file_path)

    pages = []

    try:
        for page in document:
            text = page.get_text("text")

            if text.strip():
                pages.append(text.strip())

    finally:
        document.close()

    return "\n\n".join(pages)
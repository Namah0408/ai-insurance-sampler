from pathlib import Path


DOCUMENT_KEYWORDS = {
    "PAN": [
        "permanent account number",
        "income tax department",
        "pan card",
    ],
    "AADHAAR": [
        "aadhaar",
        "unique identification",
        "uidai",
    ],
    "APPLICATION_FORM": [
        "proposal form",
        "application form",
        "life insurance proposal",
        "policy proposal",
    ],
    "BANK_STATEMENT": [
        "bank statement",
        "account statement",
        "opening balance",
        "closing balance",
        "transaction date",
    ],
    "BAWC": [
        "bawc",
        "welcome call",
        "verification call",
        "customer verification",
    ],
}


def classify_document(
    text: str,
    file_name: str,
) -> tuple[str, float]:

    combined_text = (
        f"{file_name}\n{text}"
    ).lower()

    scores = {}

    for document_type, keywords in (
        DOCUMENT_KEYWORDS.items()
    ):
        score = sum(
            1
            for keyword in keywords
            if keyword in combined_text
        )

        scores[document_type] = score

    if not any(scores.values()):
        return "UNKNOWN", 0.20

    document_type = max(
        scores,
        key=scores.get,
    )

    matched_keywords = scores[
        document_type
    ]

    confidence = min(
        0.50 + (matched_keywords * 0.15),
        0.95,
    )

    return (
        document_type,
        confidence,
    )
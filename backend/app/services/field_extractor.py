import re
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ExtractedField:
    name: str
    value: str | None
    confidence: float
    source_page: int | None
    source_text: str | None


PAN_PATTERN = re.compile(
    r"\b[A-Z]{5}[0-9]{4}[A-Z]\b",
    re.IGNORECASE,
)

AADHAAR_PATTERN = re.compile(
    r"\b\d{4}\s?\d{4}\s?\d{4}\b",
)

DATE_PATTERN = re.compile(
    r"\b"
    r"(?:"
    r"\d{2}[-/]\d{2}[-/]\d{4}"
    r"|"
    r"\d{4}[-/]\d{2}[-/]\d{2}"
    r")"
    r"\b"
)


def normalize_text(text: str) -> str:
    return re.sub(
        r"[ \t]+",
        " ",
        text,
    )


def extract_pan(
    text: str,
) -> ExtractedField:

    match = PAN_PATTERN.search(
        text.upper()
    )

    if not match:
        return ExtractedField(
            name="pan_number",
            value=None,
            confidence=0.0,
            source_page=None,
            source_text=None,
        )

    return ExtractedField(
        name="pan_number",
        value=match.group(0).upper(),
        confidence=0.95,
        source_page=1,
        source_text=match.group(0),
    )


def extract_aadhaar(
    text: str,
) -> ExtractedField:

    match = AADHAAR_PATTERN.search(
        text
    )

    if not match:
        return ExtractedField(
            name="aadhaar_number",
            value=None,
            confidence=0.0,
            source_page=None,
            source_text=None,
        )

    normalized = re.sub(
        r"\s",
        "",
        match.group(0),
    )

    return ExtractedField(
        name="aadhaar_number",
        value=normalized,
        confidence=0.90,
        source_page=1,
        source_text=match.group(0),
    )


def extract_dates(
    text: str,
) -> list[ExtractedField]:

    matches = DATE_PATTERN.findall(
        text
    )

    fields = []

    for index, value in enumerate(
        matches[:5]
    ):
        try:
            parsed_date = parse_date(
                value
            )

            field_name = (
                "date_1"
                if index == 0
                else f"date_{index + 1}"
            )

            fields.append(
                ExtractedField(
                    name=field_name,
                    value=parsed_date,
                    confidence=0.75,
                    source_page=1,
                    source_text=value,
                )
            )

        except ValueError:
            continue

    return fields


def parse_date(
    value: str,
) -> str:

    formats = [
        "%d/%m/%Y",
        "%d-%m-%Y",
        "%Y/%m/%d",
        "%Y-%m-%d",
    ]

    for date_format in formats:
        try:
            parsed = datetime.strptime(
                value,
                date_format,
            )

            return parsed.date().isoformat()

        except ValueError:
            continue

    raise ValueError(
        "Unsupported date format"
    )


def extract_name(
    text: str,
) -> ExtractedField:

    patterns = [
        r"(?:name|full name)\s*[:\-]\s*([A-Za-z ]{3,100})",
        r"name of customer\s*[:\-]\s*([A-Za-z ]{3,100})",
    ]

    for pattern in patterns:
        match = re.search(
            pattern,
            text,
            re.IGNORECASE,
        )

        if match:
            name = (
                match.group(1)
                .strip()
            )

            return ExtractedField(
                name="full_name",
                value=name,
                confidence=0.80,
                source_page=1,
                source_text=match.group(0),
            )

    return ExtractedField(
        name="full_name",
        value=None,
        confidence=0.0,
        source_page=None,
        source_text=None,
    )


def extract_fields(
    text: str,
    document_type: str,
) -> list[ExtractedField]:

    normalized_text = normalize_text(
        text
    )

    fields = []

    if document_type == "PAN":
        fields.append(
            extract_pan(
                normalized_text
            )
        )

        fields.append(
            extract_name(
                normalized_text
            )
        )

        fields.extend(
            extract_dates(
                normalized_text
            )
        )

    elif document_type == "AADHAAR":
        fields.append(
            extract_aadhaar(
                normalized_text
            )
        )

        fields.append(
            extract_name(
                normalized_text
            )
        )

    elif document_type == "APPLICATION_FORM":
        fields.append(
            extract_name(
                normalized_text
            )
        )

        fields.extend(
            extract_dates(
                normalized_text
            )
        )

    elif document_type == "BANK_STATEMENT":
        fields.extend(
            extract_dates(
                normalized_text
            )
        )

    else:
        fields.append(
            ExtractedField(
                name="raw_text_available",
                value="true"
                if normalized_text.strip()
                else "false",
                confidence=0.50,
                source_page=1,
                source_text=None,
            )
        )

    return fields
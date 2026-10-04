from app.services.document_classifier import (
    classify_document,
)
from app.services.field_extractor import (
    extract_fields,
)
from app.services.field_validator import (
    validate_field,
)


def test_pan_classification():
    text = """
    INCOME TAX DEPARTMENT
    PERMANENT ACCOUNT NUMBER
    Name: Aarav Sharma
    PAN: ABCDE1234F
    """

    document_type, confidence = (
        classify_document(
            text,
            "demo_pan.pdf",
        )
    )

    assert document_type == "PAN"
    assert confidence > 0.5


def test_pan_extraction():
    text = """
    INCOME TAX DEPARTMENT
    PERMANENT ACCOUNT NUMBER
    Name: Aarav Sharma
    PAN: ABCDE1234F
    Date of Birth: 15/05/1990
    """

    fields = extract_fields(
        text,
        "PAN",
    )

    pan_field = next(
        field
        for field in fields
        if field.name == "pan_number"
    )

    assert pan_field.value == "ABCDE1234F"
    assert pan_field.confidence > 0.9


def test_pan_validation():
    result = validate_field(
        "pan_number",
        "ABCDE1234F",
    )

    assert result == "valid"


def test_invalid_pan_validation():
    result = validate_field(
        "pan_number",
        "INVALID123",
    )

    assert result == "invalid"
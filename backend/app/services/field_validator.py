import re


def validate_pan(
    value: str | None,
) -> str:

    if not value:
        return "missing"

    if re.fullmatch(
        r"[A-Z]{5}[0-9]{4}[A-Z]",
        value.upper(),
    ):
        return "valid"

    return "invalid"


def validate_aadhaar(
    value: str | None,
) -> str:

    if not value:
        return "missing"

    normalized = re.sub(
        r"\s",
        "",
        value,
    )

    if re.fullmatch(
        r"\d{12}",
        normalized,
    ):
        return "valid"

    return "invalid"


def validate_field(
    field_name: str,
    value: str | None,
) -> str:

    if field_name == "pan_number":
        return validate_pan(value)

    if field_name == "aadhaar_number":
        return validate_aadhaar(value)

    if value is None:
        return "missing"

    if not value.strip():
        return "missing"

    return "not_validated"
import uuid
from datetime import datetime
from typing import Any

from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.proposal import Proposal
from app.models.document import Document
from app.models.document_field import DocumentField


def calculate_age(date_of_birth: datetime | None) -> int | None:

    if not date_of_birth:
        return None

    today = datetime.now().date()

    age = (
        today.year
        - date_of_birth.year
        - (
            (today.month, today.day)
            < (date_of_birth.month, date_of_birth.day)
        )
    )

    return age


def _get_document_field(
    db: Session,
    proposal_id: uuid.UUID,
    document_type: str,
    field_names: list[str],
) -> str | None:

    document = (
        db.query(Document)
        .filter(
            Document.proposal_id == proposal_id,
            Document.document_type == document_type,
        )
        .first()
    )

    if not document:
        return None

    for field_name in field_names:

        field = (
            db.query(DocumentField)
            .filter(
                DocumentField.document_id == document.id,
                DocumentField.field_name == field_name,
            )
            .first()
        )

        if field and field.field_value:
            return field.field_value

    return None


def _parse_amount(value: str | None) -> float | None:

    if not value:
        return None

    cleaned = (
        value.replace(",", "")
        .replace("INR", "")
        .replace("₹", "")
        .strip()
    )

    try:
        return float(cleaned)
    except ValueError:
        return None


def analyze_financials(
    proposal_id: uuid.UUID,
    db: Session,
) -> dict[str, Any]:

    proposal = (
        db.query(Proposal)
        .filter(Proposal.id == proposal_id)
        .first()
    )

    if not proposal:
        raise ValueError("Proposal not found.")

    customer = (
        db.query(Customer)
        .filter(Customer.id == proposal.customer_id)
        .first()
    )

    if not customer:
        raise ValueError("Customer not found.")

    annual_premium = float(proposal.annual_premium or 0)
    sum_assured = float(proposal.sum_assured or 0)

    annual_income_raw = _get_document_field(
        db,
        proposal_id,
        "APPLICATION_FORM",
        [
            "annual_income",
            "income",
            "declared_income",
        ],
    )

    annual_income = _parse_amount(annual_income_raw)

    findings = []
    flags = []

    premium_to_income_ratio = None
    sum_assured_to_income_ratio = None

    if annual_income and annual_income > 0:

        premium_to_income_ratio = (
            annual_premium / annual_income
        )

        sum_assured_to_income_ratio = (
            sum_assured / annual_income
        )

        findings.append(
            f"Annual premium to declared income ratio: "
            f"{premium_to_income_ratio:.2f}"
        )

        findings.append(
            f"Sum assured to declared income ratio: "
            f"{sum_assured_to_income_ratio:.2f}"
        )

    else:

        flags.append("INCOME_DATA_MISSING")

        findings.append(
            "Declared annual income could not be determined."
        )

    account_opening_date_raw = _get_document_field(
        db,
        proposal_id,
        "BANK_STATEMENT",
        [
            "account_opening_date",
            "opening_date",
        ],
    )

    account_age_days = None

    if account_opening_date_raw:

        for date_format in (
            "%d/%m/%Y",
            "%d-%m-%Y",
            "%Y-%m-%d",
        ):

            try:

                opening_date = datetime.strptime(
                    account_opening_date_raw,
                    date_format,
                ).date()

                account_age_days = (
                    datetime.now().date()
                    - opening_date
                ).days

                break

            except ValueError:
                continue

    if account_age_days is None:

        findings.append(
            "Bank account age could not be determined."
        )

    else:

        findings.append(
            f"Bank account age: {account_age_days} days."
        )

        if account_age_days < 180:

            flags.append("RECENT_BANK_ACCOUNT")

            findings.append(
                "Bank account appears to be recently opened."
            )

    age = calculate_age(customer.date_of_birth)

    if age is not None:

        findings.append(
            f"Customer age based on date of birth: {age}."
        )

    if not flags:

        risk_level = "LOW"

    elif len(flags) == 1:

        risk_level = "MEDIUM"

    else:

        risk_level = "HIGH"

    return {
        "analysis_type": "FINANCIAL",
        "status": "completed",
        "risk_level": risk_level,
        "customer_id": str(customer.id),
        "annual_income": annual_income,
        "annual_premium": annual_premium,
        "sum_assured": sum_assured,
        "premium_to_income_ratio": premium_to_income_ratio,
        "sum_assured_to_income_ratio": sum_assured_to_income_ratio,
        "account_age_days": account_age_days,
        "findings": findings,
        "flags": flags,
    }
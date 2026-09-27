from app.rules.engine import run_rules
from app.schemas.risk import RiskAssessmentInput


def test_low_risk_case():
    data = RiskAssessmentInput(
        age=36,
        documents_present=[
            "PAN",
            "AADHAAR",
            "APPLICATION_FORM",
            "BANK_STATEMENT",
        ],
        required_documents_missing=[],
        kyc_verified=True,
        pan_aadhaar_match=True,
        bawc_completed=True,
        bawc_identity_match=True,
        bank_account_age_months=48,
        declared_annual_income=800000,
        annual_premium=50000,
        existing_policy_count=1,
        existing_sum_assured=500000,
        application_data_consistent=True,
    )

    result = run_rules(data)

    assert result["risk_level"] == "LOW"
    assert result["risk_score"] == 0
    assert result["recommendation"] == "REVIEW"


def test_medium_risk_case():
    data = RiskAssessmentInput(
        age=39,
        documents_present=[
            "PAN",
            "AADHAAR",
            "APPLICATION_FORM",
            "BANK_STATEMENT",
        ],
        required_documents_missing=[],
        kyc_verified=True,
        pan_aadhaar_match=True,
        bawc_completed=True,
        bawc_identity_match=True,
        bank_account_age_months=4,
        declared_annual_income=700000,
        annual_premium=150000,
        existing_policy_count=3,
        existing_sum_assured=1500000,
        application_data_consistent=True,
    )

    result = run_rules(data)

    assert result["risk_level"] == "MEDIUM"
    assert result["risk_score"] == 35
    assert result["recommendation"] == "REVIEW"


def test_high_risk_case():
    data = RiskAssessmentInput(
        age=44,
        documents_present=[
            "PAN",
            "APPLICATION_FORM",
        ],
        required_documents_missing=[
            "AADHAAR",
            "BANK_STATEMENT",
        ],
        kyc_verified=False,
        pan_aadhaar_match=False,
        bawc_completed=True,
        bawc_identity_match=False,
        bank_account_age_months=2,
        declared_annual_income=800000,
        annual_premium=400000,
        existing_policy_count=6,
        existing_sum_assured=8000000,
        application_data_consistent=False,
    )

    result = run_rules(data)

    assert result["risk_level"] == "HIGH"
    assert result["risk_score"] == 100
    assert result["recommendation"] == "REVIEW"
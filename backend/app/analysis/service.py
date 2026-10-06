import uuid
from typing import Any

from sqlalchemy.orm import Session

from app.analysis.bawc_analysis import analyze_bawc
from app.analysis.financial_analysis import analyze_financials
from app.analysis.insurance_analysis import analyze_insurance_exposure
from app.analysis.kyc_analysis import analyze_kyc
from app.models.bawc_analysis import BAWCAnalysis
from app.models.financial_analysis import FinancialAnalysis
from app.models.insurance_analysis import InsuranceAnalysis
from app.models.kyc_analysis import KYCAnalysis


def run_all_analysis(
    proposal_id: uuid.UUID,
    db: Session,
) -> dict[str, Any]:

    kyc = analyze_kyc(
        proposal_id,
        db,
    )

    financial = analyze_financials(
        proposal_id,
        db,
    )

    bawc = analyze_bawc(
        proposal_id,
        db,
    )

    insurance = analyze_insurance_exposure(
        proposal_id,
        db,
    )

    kyc_record = KYCAnalysis(
        proposal_id=proposal_id,
        status=kyc["status"],
        risk_level=kyc["risk_level"],
        findings=kyc["findings"],
        flags=kyc["flags"],
    )

    financial_record = FinancialAnalysis(
        proposal_id=proposal_id,
        status=financial["status"],
        risk_level=financial["risk_level"],
        annual_income=financial["annual_income"],
        annual_premium=financial["annual_premium"],
        sum_assured=financial["sum_assured"],
        premium_to_income_ratio=financial[
            "premium_to_income_ratio"
        ],
        sum_assured_to_income_ratio=financial[
            "sum_assured_to_income_ratio"
        ],
        account_age_days=financial["account_age_days"],
        findings=financial["findings"],
        flags=financial["flags"],
    )

    bawc_record = BAWCAnalysis(
        proposal_id=proposal_id,
        status=bawc["status"],
        risk_level=bawc["risk_level"],
        documents_found=bawc["documents_found"],
        processed_documents=bawc["processed_documents"],
        findings=bawc["findings"],
        flags=bawc["flags"],
    )

    insurance_record = InsuranceAnalysis(
        proposal_id=proposal_id,
        status=insurance["status"],
        risk_level=insurance["risk_level"],
        existing_policy_count=insurance[
            "existing_policy_count"
        ],
        total_existing_sum_assured=insurance[
            "total_existing_sum_assured"
        ],
        multiple_insurer_flag=insurance[
            "multiple_insurer_flag"
        ],
        findings=insurance["findings"],
        flags=insurance["flags"],
    )

    db.add_all(
        [
            kyc_record,
            financial_record,
            bawc_record,
            insurance_record,
        ]
    )

    db.commit()

    for record in [
        kyc_record,
        financial_record,
        bawc_record,
        insurance_record,
    ]:
        db.refresh(record)

    return {
        "kyc": kyc_record,
        "financial": financial_record,
        "bawc": bawc_record,
        "insurance": insurance_record,
    }
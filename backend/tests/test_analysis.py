def test_analysis_modules_import():

    from app.analysis.kyc_analysis import analyze_kyc
    from app.analysis.financial_analysis import analyze_financials
    from app.analysis.bawc_analysis import analyze_bawc
    from app.analysis.insurance_analysis import (
        analyze_insurance_exposure,
    )

    assert analyze_kyc is not None
    assert analyze_financials is not None
    assert analyze_bawc is not None
    assert analyze_insurance_exposure is not None


def test_financial_amount_parser():

    from app.analysis.financial_analysis import _parse_amount

    assert _parse_amount("INR 1,200,000") == 1200000
    assert _parse_amount("₹75000") == 75000
    assert _parse_amount("invalid") is None
    assert _parse_amount(None) is None
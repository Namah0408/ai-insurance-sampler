from app.rules.types import RuleResult


def rule_missing_documents(data) -> RuleResult:
    missing = data.required_documents_missing

    if missing:
        return RuleResult(
            rule_code="DOC-001",
            triggered=True,
            severity="HIGH",
            score=25,
            title="Required documents missing",
            description=(
                "One or more required documents are missing: "
                + ", ".join(missing)
            ),
        )

    return RuleResult(
        rule_code="DOC-001",
        triggered=False,
        severity="NONE",
        score=0,
        title="Required documents available",
        description="No required documents are missing.",
    )


def rule_kyc_verification(data) -> RuleResult:
    if not data.kyc_verified:
        return RuleResult(
            rule_code="KYC-001",
            triggered=True,
            severity="HIGH",
            score=40,
            title="KYC verification failed",
            description=(
                "The KYC verification result indicates "
                "that the customer could not be verified."
            ),
        )

    return RuleResult(
        rule_code="KYC-001",
        triggered=False,
        severity="NONE",
        score=0,
        title="KYC verification successful",
        description="KYC verification passed.",
    )


def rule_pan_aadhaar_match(data) -> RuleResult:
    if not data.pan_aadhaar_match:
        return RuleResult(
            rule_code="KYC-002",
            triggered=True,
            severity="HIGH",
            score=35,
            title="PAN and Aadhaar mismatch",
            description=(
                "PAN and Aadhaar identity information "
                "did not match."
            ),
        )

    return RuleResult(
        rule_code="KYC-002",
        triggered=False,
        severity="NONE",
        score=0,
        title="PAN and Aadhaar match",
        description="PAN and Aadhaar information matched.",
    )


def rule_bawc(data) -> RuleResult:
    if not data.bawc_completed:
        return RuleResult(
            rule_code="BAWC-001",
            triggered=True,
            severity="MEDIUM",
            score=15,
            title="BAWC not completed",
            description=(
                "The required BAWC process has not been "
                "completed."
            ),
        )

    return RuleResult(
        rule_code="BAWC-001",
        triggered=False,
        severity="NONE",
        score=0,
        title="BAWC completed",
        description="BAWC process is marked as completed.",
    )


def rule_bawc_identity(data) -> RuleResult:
    if data.bawc_completed and not data.bawc_identity_match:
        return RuleResult(
            rule_code="BAWC-002",
            triggered=True,
            severity="HIGH",
            score=35,
            title="BAWC identity mismatch",
            description=(
                "The identity observed during BAWC "
                "did not match the expected customer identity."
            ),
        )

    return RuleResult(
        rule_code="BAWC-002",
        triggered=False,
        severity="NONE",
        score=0,
        title="BAWC identity match",
        description="BAWC identity check passed.",
    )


def rule_bank_account_age(data) -> RuleResult:
    if data.bank_account_age_months < 6:
        return RuleResult(
            rule_code="FIN-001",
            triggered=True,
            severity="MEDIUM",
            score=15,
            title="Recently opened bank account",
            description=(
                "The bank account is less than six months old."
            ),
        )

    return RuleResult(
        rule_code="FIN-001",
        triggered=False,
        severity="NONE",
        score=0,
        title="Bank account age acceptable",
        description="The bank account is at least six months old.",
    )


def rule_premium_to_income(data) -> RuleResult:
    premium_ratio = (
        data.annual_premium
        / data.declared_annual_income
    )

    if premium_ratio > 0.30:
        return RuleResult(
            rule_code="FIN-002",
            triggered=True,
            severity="HIGH",
            score=25,
            title="High premium-to-income ratio",
            description=(
                "The annual premium is more than 30% "
                "of the declared annual income."
            ),
        )

    if premium_ratio > 0.20:
        return RuleResult(
            rule_code="FIN-002",
            triggered=True,
            severity="MEDIUM",
            score=10,
            title="Elevated premium-to-income ratio",
            description=(
                "The annual premium is more than 20% "
                "of the declared annual income."
            ),
        )

    return RuleResult(
        rule_code="FIN-002",
        triggered=False,
        severity="NONE",
        score=0,
        title="Premium-to-income ratio acceptable",
        description=(
            "The annual premium is within the demo "
            "income ratio thresholds."
        ),
    )


def rule_existing_policies(data) -> RuleResult:
    if data.existing_policy_count >= 5:
        return RuleResult(
            rule_code="IIB-001",
            triggered=True,
            severity="HIGH",
            score=25,
            title="High existing policy count",
            description=(
                "The customer has five or more existing "
                "policies in the supplied synthetic data."
            ),
        )

    if data.existing_policy_count >= 3:
        return RuleResult(
            rule_code="IIB-001",
            triggered=True,
            severity="MEDIUM",
            score=10,
            title="Multiple existing policies",
            description=(
                "The customer has three or more existing "
                "policies in the supplied synthetic data."
            ),
        )

    return RuleResult(
        rule_code="IIB-001",
        triggered=False,
        severity="NONE",
        score=0,
        title="Existing policy count acceptable",
        description=(
            "The existing policy count is within "
            "the demo threshold."
        ),
    )


def rule_application_consistency(data) -> RuleResult:
    if not data.application_data_consistent:
        return RuleResult(
            rule_code="DATA-001",
            triggered=True,
            severity="HIGH",
            score=30,
            title="Application data inconsistency",
            description=(
                "One or more customer information fields "
                "are inconsistent across the supplied data."
            ),
        )

    return RuleResult(
        rule_code="DATA-001",
        triggered=False,
        severity="NONE",
        score=0,
        title="Application data consistent",
        description=(
            "The supplied application information "
            "is marked as consistent."
        ),
    )


def get_default_rules():
    return [
        rule_missing_documents,
        rule_kyc_verification,
        rule_pan_aadhaar_match,
        rule_bawc,
        rule_bawc_identity,
        rule_bank_account_age,
        rule_premium_to_income,
        rule_existing_policies,
        rule_application_consistency,
    ]
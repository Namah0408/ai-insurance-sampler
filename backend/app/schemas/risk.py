import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class RiskAssessmentInput(BaseModel):
    age: int = Field(
        ge=0,
        le=120,
    )

    documents_present: list[str] = Field(
        default_factory=list,
    )

    required_documents_missing: list[str] = Field(
        default_factory=list,
    )

    kyc_verified: bool = True

    pan_aadhaar_match: bool = True

    bawc_completed: bool = True

    bawc_identity_match: bool = True

    bank_account_age_months: int = Field(
        ge=0,
        default=24,
    )

    declared_annual_income: float = Field(
        gt=0,
    )

    annual_premium: float = Field(
        gt=0,
    )

    existing_policy_count: int = Field(
        ge=0,
        default=0,
    )

    existing_sum_assured: float = Field(
        ge=0,
        default=0,
    )

    application_data_consistent: bool = True


class RiskFlagResponse(BaseModel):
    id: uuid.UUID
    rule_code: str
    severity: str
    score: int
    title: str
    description: str
    created_at: datetime


class RiskAssessmentResponse(BaseModel):
    id: uuid.UUID
    proposal_id: uuid.UUID
    risk_score: int
    risk_level: str
    recommendation: str
    input_snapshot: dict
    created_at: datetime
    updated_at: datetime
    flags: list[RiskFlagResponse]
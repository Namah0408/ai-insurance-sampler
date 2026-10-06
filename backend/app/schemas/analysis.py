import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class KYCAnalysisResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: uuid.UUID
    proposal_id: uuid.UUID
    status: str
    risk_level: str
    findings: list[Any]
    flags: list[Any]
    created_at: datetime


class FinancialAnalysisResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: uuid.UUID
    proposal_id: uuid.UUID
    status: str
    risk_level: str

    annual_income: float | None
    annual_premium: float | None
    sum_assured: float | None

    premium_to_income_ratio: float | None
    sum_assured_to_income_ratio: float | None

    account_age_days: int | None

    findings: list[Any]
    flags: list[Any]

    created_at: datetime


class BAWCAnalysisResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: uuid.UUID
    proposal_id: uuid.UUID
    status: str
    risk_level: str

    documents_found: int
    processed_documents: int

    findings: list[Any]
    flags: list[Any]

    created_at: datetime


class InsuranceAnalysisResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: uuid.UUID
    proposal_id: uuid.UUID
    status: str
    risk_level: str

    existing_policy_count: int | None
    total_existing_sum_assured: float | None
    multiple_insurer_flag: bool | None

    findings: list[Any]
    flags: list[Any]

    created_at: datetime


class AnalysisRunResponse(BaseModel):

    proposal_id: uuid.UUID

    kyc: KYCAnalysisResponse
    financial: FinancialAnalysisResponse
    bawc: BAWCAnalysisResponse
    insurance: InsuranceAnalysisResponse


class AnalysisHistoryResponse(BaseModel):

    proposal_id: uuid.UUID

    kyc: list[KYCAnalysisResponse]
    financial: list[FinancialAnalysisResponse]
    bawc: list[BAWCAnalysisResponse]
    insurance: list[InsuranceAnalysisResponse]
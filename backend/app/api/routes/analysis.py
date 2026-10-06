import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.analysis.service import run_all_analysis
from app.database.session import get_db
from app.models.bawc_analysis import BAWCAnalysis
from app.models.financial_analysis import FinancialAnalysis
from app.models.insurance_analysis import InsuranceAnalysis
from app.models.kyc_analysis import KYCAnalysis
from app.models.proposal import Proposal
from app.schemas.analysis import (
    AnalysisHistoryResponse,
    AnalysisRunResponse,
    BAWCAnalysisResponse,
    FinancialAnalysisResponse,
    InsuranceAnalysisResponse,
    KYCAnalysisResponse,
)


router = APIRouter(
    prefix="/proposals",
    tags=["Analysis"],
)


@router.post(
    "/{proposal_id}/analysis/run",
    response_model=AnalysisRunResponse,
)
def run_analysis(
    proposal_id: uuid.UUID,
    db: Session = Depends(get_db),
):

    proposal = (
        db.query(Proposal)
        .filter(Proposal.id == proposal_id)
        .first()
    )

    if not proposal:
        raise HTTPException(
            status_code=404,
            detail="Proposal not found",
        )

    try:

        results = run_all_analysis(
            proposal_id=proposal_id,
            db=db,
        )

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {error}",
        )

    return AnalysisRunResponse(
        proposal_id=proposal_id,
        kyc=results["kyc"],
        financial=results["financial"],
        bawc=results["bawc"],
        insurance=results["insurance"],
    )


@router.get(
    "/{proposal_id}/analysis",
    response_model=AnalysisHistoryResponse,
)
def get_analysis_history(
    proposal_id: uuid.UUID,
    db: Session = Depends(get_db),
):

    proposal = (
        db.query(Proposal)
        .filter(Proposal.id == proposal_id)
        .first()
    )

    if not proposal:
        raise HTTPException(
            status_code=404,
            detail="Proposal not found",
        )

    kyc_results = (
        db.query(KYCAnalysis)
        .filter(
            KYCAnalysis.proposal_id == proposal_id
        )
        .order_by(
            KYCAnalysis.created_at.desc()
        )
        .all()
    )

    financial_results = (
        db.query(FinancialAnalysis)
        .filter(
            FinancialAnalysis.proposal_id == proposal_id
        )
        .order_by(
            FinancialAnalysis.created_at.desc()
        )
        .all()
    )

    bawc_results = (
        db.query(BAWCAnalysis)
        .filter(
            BAWCAnalysis.proposal_id == proposal_id
        )
        .order_by(
            BAWCAnalysis.created_at.desc()
        )
        .all()
    )

    insurance_results = (
        db.query(InsuranceAnalysis)
        .filter(
            InsuranceAnalysis.proposal_id == proposal_id
        )
        .order_by(
            InsuranceAnalysis.created_at.desc()
        )
        .all()
    )

    return AnalysisHistoryResponse(
        proposal_id=proposal_id,
        kyc=kyc_results,
        financial=financial_results,
        bawc=bawc_results,
        insurance=insurance_results,
    )
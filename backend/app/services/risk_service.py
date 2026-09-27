import uuid

from sqlalchemy.orm import Session

from app.models.proposal import Proposal
from app.models.risk_assessment import RiskAssessment
from app.models.risk_flag import RiskFlag
from app.rules.engine import run_rules
from app.schemas.risk import RiskAssessmentInput


def assess_proposal(
    proposal_id: uuid.UUID,
    data: RiskAssessmentInput,
    db: Session,
):
    proposal = (
        db.query(Proposal)
        .filter(Proposal.id == proposal_id)
        .first()
    )

    if not proposal:
        return None

    existing_assessment = (
        db.query(RiskAssessment)
        .filter(
            RiskAssessment.proposal_id
            == proposal_id
        )
        .first()
    )

    if existing_assessment:
        for flag in existing_assessment.flags:
            db.delete(flag)

        db.delete(existing_assessment)
        db.flush()

    result = run_rules(data)

    assessment = RiskAssessment(
        proposal_id=proposal_id,
        risk_score=result["risk_score"],
        risk_level=result["risk_level"],
        recommendation=result["recommendation"],
        input_snapshot=data.model_dump(),
    )

    db.add(assessment)
    db.flush()

    for rule_result in result["triggered_results"]:
        flag = RiskFlag(
            assessment_id=assessment.id,
            rule_code=rule_result.rule_code,
            severity=rule_result.severity,
            score=rule_result.score,
            title=rule_result.title,
            description=rule_result.description,
        )

        db.add(flag)

    db.commit()
    db.refresh(assessment)

    return assessment


def get_assessment(
    proposal_id: uuid.UUID,
    db: Session,
):
    return (
        db.query(RiskAssessment)
        .filter(
            RiskAssessment.proposal_id
            == proposal_id
        )
        .first()
    )
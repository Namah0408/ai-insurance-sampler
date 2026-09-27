from app.rules.default_rules import get_default_rules
from app.rules.types import RuleResult


def calculate_risk_level(score: int) -> str:
    if score >= 50:
        return "HIGH"

    if score >= 20:
        return "MEDIUM"

    return "LOW"


def calculate_recommendation(risk_level: str) -> str:
    if risk_level == "HIGH":
        return "REVIEW"

    if risk_level == "MEDIUM":
        return "REVIEW"

    return "REVIEW"


def run_rules(data) -> dict:
    results: list[RuleResult] = []

    for rule in get_default_rules():
        result = rule(data)
        results.append(result)

    triggered_results = [
        result
        for result in results
        if result.triggered
    ]

    risk_score = sum(
        result.score
        for result in triggered_results
    )

    risk_score = min(risk_score, 100)

    risk_level = calculate_risk_level(
        risk_score
    )

    recommendation = calculate_recommendation(
        risk_level
    )

    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "recommendation": recommendation,
        "all_results": results,
        "triggered_results": triggered_results,
    }
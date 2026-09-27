from dataclasses import dataclass


@dataclass
class RuleResult:
    rule_code: str
    triggered: bool
    severity: str
    score: int
    title: str
    description: str
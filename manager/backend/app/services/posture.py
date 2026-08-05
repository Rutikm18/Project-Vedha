"""
Posture scoring & patch-comparison — the single source of truth behind the
dashboard scorecard and the report's "Posture & Remediation Progress" section.

Pure and DB-free (mirrors services/sla.py and services/analytics.py): callers
build lightweight FindingView rows and pass them in. Scores use a noisy-OR
aggregate so each open finding adds diminishing marginal risk, every score is
bounded to 0-100, and adding a finding can never lower risk.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from app.vuln.enrichment import _CRIT_WEIGHT  # asset-criticality → 0-1 weight (DRY)

# Posture Score → letter grade. Ordered high-to-low; first threshold met wins.
_GRADE_BANDS = ((90, "A"), (75, "B"), (55, "C"), (35, "D"), (0, "F"))


@dataclass
class FindingView:
    """Duck-typed projection of a Finding + its asset's criticality."""
    id: str
    severity: str
    risk_score: float | None
    epss_score: float | None
    exploitable: bool
    exploit_validated: bool
    asset_criticality: str | None
    first_seen: datetime | None
    last_seen: datetime | None


@dataclass
class Scores:
    risk_index: float
    exploitable_score: float
    posture_score: int
    grade: str


def _clamp01(x: float) -> float:
    return min(max(x, 0.0), 1.0)


def aggregate(probs: list[float]) -> float:
    """Noisy-OR: 100·(1 − ∏(1 − clamp(p))). Empty → 0.0. Always in [0, 100]."""
    prod = 1.0
    for p in probs:
        prod *= (1.0 - _clamp01(float(p)))
    return round(100.0 * (1.0 - prod), 2)


def grade_for(posture_score: int) -> str:
    for threshold, letter in _GRADE_BANDS:
        if posture_score >= threshold:
            return letter
    return "F"


def _risk_prob(f: FindingView) -> float:
    rs = float(f.risk_score) if f.risk_score is not None else 0.0
    return rs / 1000.0


def _exploit_prob(f: FindingView) -> float:
    epss_n = _clamp01(float(f.epss_score) if f.epss_score is not None else 0.0)
    candidates = [epss_n]
    if f.exploitable:
        candidates.append(0.6)
    if f.exploit_validated:
        candidates.append(1.0)
    exploit_xi = max(candidates)
    crit = _CRIT_WEIGHT.get(f.asset_criticality or "", 0.5)
    return exploit_xi * crit


def compute_scores(open_findings: list[FindingView]) -> Scores:
    risk_index = aggregate([_risk_prob(f) for f in open_findings])
    exploitable_score = aggregate([_exploit_prob(f) for f in open_findings])
    blend = 0.6 * risk_index + 0.4 * exploitable_score
    posture_score = round(100 - blend)
    return Scores(
        risk_index=risk_index,
        exploitable_score=exploitable_score,
        posture_score=posture_score,
        grade=grade_for(posture_score),
    )

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


# Task 2: Run-comparison + response builder

# Severity display order for the comparison matrix.
_SEVERITY_ORDER = ("critical", "high", "medium", "low", "info")


def _to_utc(dt: datetime | None) -> datetime | None:
    if dt is None:
        return None
    return dt.replace(tzinfo=timezone.utc) if dt.tzinfo is None else dt.astimezone(timezone.utc)


def _present_in_run(f: FindingView, run_at: datetime | None) -> bool:
    """True when the finding was live as of run_at (first_seen ≤ run_at ≤ last_seen)."""
    if run_at is None:
        return False
    fs = _to_utc(f.first_seen)
    if fs is None:
        return False
    ls = _to_utc(f.last_seen) or fs
    return fs <= run_at and ls >= run_at


def _severity(f: FindingView) -> str:
    return f.severity if f.severity in _SEVERITY_ORDER else "info"


def compare(views: list[FindingView], prev_at: datetime | None, latest_at: datetime) -> dict:
    """Bucket findings across the previous→latest run transition."""
    latest_open = [f for f in views if _present_in_run(f, latest_at)]
    prev_open = [f for f in views if _present_in_run(f, prev_at)]

    latest_ids = {f.id for f in latest_open}
    prev_ids = {f.id for f in prev_open}

    resolved = [f for f in prev_open if f.id not in latest_ids]
    new = [f for f in latest_open if f.id not in prev_ids]
    persisting = [f for f in latest_open if f.id in prev_ids]

    # Per-severity matrix.
    matrix = []
    for sev in _SEVERITY_ORDER:
        p = sum(1 for f in prev_open if _severity(f) == sev)
        nw = sum(1 for f in new if _severity(f) == sev)
        rs = sum(1 for f in resolved if _severity(f) == sev)
        no = sum(1 for f in latest_open if _severity(f) == sev)
        matrix.append({
            "severity": sev, "prev_open": p, "new": nw,
            "resolved": rs, "now_open": no, "net": no - p,
        })

    risk_burned_down = round(
        sum(float(f.risk_score) for f in resolved if f.risk_score is not None), 2
    )

    return {
        "latest_open": latest_open,
        "prev_open": prev_open,
        "matrix": matrix,
        "risk_burned_down": risk_burned_down,
        "resolved_count": len(resolved),
        "new_count": len(new),
        "persisting_count": len(persisting),
    }


def build_posture(
    views: list[FindingView],
    prev_run: dict | None,
    latest_run: dict | None,
) -> dict:
    """Full dashboard/report payload. Degrades gracefully with 0 or 1 run."""
    if latest_run is None:
        return {"has_runs": False}

    prev_at = _to_utc(prev_run["started_at"]) if prev_run else None
    latest_at = _to_utc(latest_run["started_at"])

    cmp = compare(views, prev_at, latest_at)
    scores = compute_scores(cmp["latest_open"])
    scores_prev = compute_scores(cmp["prev_open"]) if prev_run else compute_scores([])

    return {
        "has_runs": True,
        "latest_run": {"id": latest_run["id"], "started_at": latest_at.isoformat()},
        "previous_run": (
            {"id": prev_run["id"], "started_at": prev_at.isoformat()} if prev_run else None
        ),
        "scores": scores.__dict__,
        "scores_prev": scores_prev.__dict__ if prev_run else None,
        "matrix": cmp["matrix"],
        "risk_burned_down": cmp["risk_burned_down"],
        "resolved_count": cmp["resolved_count"],
        "new_count": cmp["new_count"],
        "persisting_count": cmp["persisting_count"],
    }

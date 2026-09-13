"""
Posture scoring & patch-comparison — the single source of truth behind the
dashboard scorecard and the report's "Posture & Remediation Progress" section.

Pure and DB-free (mirrors services/sla.py and services/analytics.py): callers
build lightweight FindingView rows and pass them in. Every score is bounded to
0-100 and adding a finding can never lower risk.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import datetime, timezone

from app.vuln.enrichment import _CRIT_WEIGHT  # asset-criticality → 0-1 weight (DRY)

# Posture Score → letter grade. Ordered high-to-low; first threshold met wins.
_GRADE_BANDS = ((90, "A"), (75, "B"), (55, "C"), (35, "D"), (0, "F"))


# Statuses that still represent a live exposure. Everything else has left the
# queue; `remediated` is the only exit that counts as a FIX (see compare()).
_ACTIVE_STATUSES = frozenset({"open", "confirmed"})


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
    # Current lifecycle status. Defaults to "open" so the many call sites that
    # only ever pass still-open findings keep working unchanged; compare() needs
    # it to tell "still open" from "fixed since the previous run".
    status: str = "open"

    @property
    def is_active(self) -> bool:
        return self.status in _ACTIVE_STATUSES


@dataclass
class Scores:
    risk_index: float
    exploitable_score: float
    posture_score: int
    grade: str


def _clamp01(x: float) -> float:
    return min(max(x, 0.0), 1.0)


# ── The aggregation curve ────────────────────────────────────────────────────
# `mass` is the additive weight of everything still open — one unit is one
# finding at maximum risk. The index is a LOG of that mass:
#
#     index = _DECADE · log10(1 + mass / _KNEE)      clamped to [0, 100]
#
# WHY NOT NOISY-OR. The previous aggregate was 100·(1 − ∏(1 − p)), which answers
# "what is the chance at least one of these is a real problem?". For three open
# criticals the answer is "essentially certain", and it stays essentially
# certain whether you have three or three hundred. So the score pinned at ~100
# (grade F) in any real environment and then stopped moving: the dial showed a
# fixed needle, the scan-over-scan delta read "no change" forever, and fixing
# half your criticals earned about one point. A posture grade that cannot go up
# when you do the work is worse than no grade at all.
#
# WHAT THE LOG BUYS. Every 10× change in open risk mass is worth exactly
# _DECADE points, at any point on the scale. That holds at 5 findings and at
# 500, so remediation is always visible, and it is a property you can say out
# loud to a customer: cut your open risk by 10× and you gain 25 points.
#
# _KNEE keeps the curve steep near zero so one serious finding registers
# immediately rather than being lost in rounding; _DECADE spreads four decades
# of mass (0.1 → 1000) across the full 0-100 range. Severity still dominates
# per finding, because the mass each one contributes is its own 0-1000 risk
# score — a critical brings ~10× what a low does.
_KNEE = 0.1
_DECADE = 25.0


def aggregate(weights: list[float]) -> float:
    """Log-compressed risk mass → 0-100. Empty → 0.0.

    Monotonic by construction: `mass` is a sum of non-negative clamped weights
    and log10 is increasing, so adding a finding can never improve the score.
    """
    mass = 0.0
    for w in weights:
        mass += _clamp01(float(w))
    if mass <= 0.0:
        return 0.0
    index = _DECADE * math.log10(1.0 + mass / _KNEE)
    return round(min(100.0, index), 2)


def grade_for(posture_score: int) -> str:
    for threshold, letter in _GRADE_BANDS:
        if posture_score >= threshold:
            return letter
    return "F"


def _risk_weight(f: FindingView) -> float:
    """This finding's share of risk mass: its 0-1000 composite risk, normalised.
    A critical therefore contributes roughly 10x what a low does."""
    rs = float(f.risk_score) if f.risk_score is not None else 0.0
    return rs / 1000.0


def _exploit_weight(f: FindingView) -> float:
    """Risk mass that is actually reachable: how exploitable the finding is,
    scaled by how much the asset underneath it matters."""
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
    risk_index = aggregate([_risk_weight(f) for f in open_findings])
    exploitable_score = aggregate([_exploit_weight(f) for f in open_findings])
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
    run_at = _to_utc(run_at)
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
    """Bucket findings across the previous→latest run transition.

    `views` must carry both the still-open findings AND the ones remediated since
    the previous run — callers should NOT pre-filter to open/confirmed. That
    filter is why "Patched" used to read zero: a finding that was actually fixed
    has status=remediated (the auto-resolver writes it, and so does an operator
    closing one by hand), so a query restricted to open/confirmed dropped it
    before it could ever reach `resolved`. What survived was only "still open but
    not re-observed", which evaporates the moment auto-resolution confirms it —
    so a customer who fixed everything saw nothing patched and no risk burned
    down. Risk-accepted and false-positive findings are a different matter and
    stay out of `views`: neither is a fix, so neither belongs in a patch ledger.

    Two filters do different jobs here, deliberately:
      * `prev_open` is a pure TIME window — what was live at the previous run,
        whatever its status is today. That is what "Before" means.
      * `latest_open` also requires the finding to be active NOW, so something
        closed after the latest run is not still counted as open.
    """
    latest_open = [f for f in views if f.is_active and _present_in_run(f, latest_at)]
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
    scores_prev = compute_scores(cmp["prev_open"]) if prev_run else None

    return {
        "has_runs": True,
        "latest_run": {"id": latest_run["id"], "started_at": latest_at.isoformat()},
        "previous_run": (
            {"id": prev_run["id"], "started_at": prev_at.isoformat()} if prev_run else None
        ),
        "scores": scores.__dict__,
        "scores_prev": scores_prev.__dict__ if scores_prev is not None else None,
        "matrix": cmp["matrix"],
        "risk_burned_down": cmp["risk_burned_down"],
        "resolved_count": cmp["resolved_count"],
        "new_count": cmp["new_count"],
        "persisting_count": cmp["persisting_count"],
    }

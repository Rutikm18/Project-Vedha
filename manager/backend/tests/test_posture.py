from __future__ import annotations

from datetime import datetime, timezone

from app.routers.ai_report import build_posture_report_section
from app.routers.analytics import _finding_views
from app.services.posture import (
    FindingView, Scores, aggregate, build_posture, compute_scores, grade_for,
)


def _fv(**kw) -> FindingView:
    base = dict(
        id="f", severity="high", risk_score=None, epss_score=None,
        exploitable=False, exploit_validated=False, asset_criticality=None,
        first_seen=None, last_seen=None,
    )
    base.update(kw)
    return FindingView(**base)


def test_aggregate_is_bounded_and_empty_is_zero():
    assert aggregate([]) == 0.0
    assert 0.0 <= aggregate([0.5, 0.5, 0.9]) <= 100.0
    # Weights clamp to [0,1], so one absurd input cannot outrun the scale.
    assert aggregate([5.0]) == aggregate([1.0])
    # Even an extreme portfolio stays inside the dial's range.
    assert aggregate([1.0] * 100_000) == 100.0


def test_aggregate_is_monotonic():
    before = aggregate([0.4, 0.4])
    after = aggregate([0.4, 0.4, 0.3])
    assert after >= before


def test_aggregate_does_not_saturate():
    """The defect this curve exists to fix.

    Noisy-OR answered "is at least one of these a real problem?", which is
    "yes, certainly" at three open criticals and stays there at three hundred.
    The score pinned at F and stopped moving, so the dial showed a fixed needle
    and remediation earned nothing. Every one of these portfolios must be
    distinguishable from the next.
    """
    steps = [aggregate([0.9] * n) for n in (1, 3, 10, 30, 100, 300)]
    assert steps == sorted(steps)
    assert len(set(steps)) == len(steps), "portfolios collapsed onto one value"
    # Still climbing at the top end — not flat-lined.
    assert steps[-1] - steps[-2] > 1.0


def test_every_tenfold_change_in_risk_mass_is_worth_the_same_points():
    """The property that makes the number explainable to a customer: cut open
    risk by 10x and you gain a fixed number of points, wherever you start.

    Asymptotic, not exact — the knee deliberately makes the lowest decade a
    little steeper so a single serious finding registers straight away.
    """
    from app.services.posture import _DECADE

    decades = [aggregate([1.0] * n) for n in (1, 10, 100, 1000)]
    gaps = [b - a for a, b in zip(decades, decades[1:])]
    assert all(abs(g - _DECADE) < 1.0 for g in gaps), gaps


def test_remediation_always_moves_the_score():
    """At any scale, clearing half the queue must be visible on the dial."""
    for n in (4, 10, 40, 100, 400):
        full = compute_scores([_fv(risk_score=900, id=str(i)) for i in range(n)])
        half = compute_scores([_fv(risk_score=900, id=str(i)) for i in range(n // 2)])
        assert half.posture_score > full.posture_score + 1, (
            f"halving {n} findings moved the score by only "
            f"{half.posture_score - full.posture_score}"
        )


def test_grade_spans_the_range_across_realistic_portfolios():
    """A grade that is F for everyone is not a grade. One medium finding must
    not read the same as a thousand exploitable criticals."""
    def grade(n, risk, **kw):
        return compute_scores([_fv(risk_score=risk, id=str(i), **kw) for i in range(n)]).grade

    assert grade(0, 0) == "A"
    assert grade(1, 400) in ("A", "B")
    assert grade(20, 400) in ("B", "C")
    assert grade(100, 900, exploitable=True, asset_criticality="medium") in ("D", "F")
    assert grade(500, 900, exploit_validated=True, asset_criticality="critical") == "F"


def test_grade_bands():
    assert grade_for(95) == "A"
    assert grade_for(90) == "A"
    assert grade_for(80) == "B"
    assert grade_for(60) == "C"
    assert grade_for(40) == "D"
    assert grade_for(35) == "D"
    assert grade_for(34) == "F"
    assert grade_for(10) == "F"


def test_compute_scores_empty_is_perfect():
    s = compute_scores([])
    assert s == Scores(risk_index=0.0, exploitable_score=0.0, posture_score=100, grade="A")


def test_compute_scores_uses_risk_epss_exploit_and_asset_criticality():
    findings = [
        _fv(risk_score=800, epss_score=0.9, exploit_validated=True, asset_criticality="critical"),
        _fv(risk_score=200, epss_score=0.1, exploitable=True, asset_criticality="low"),
    ]
    s = compute_scores(findings)
    # risk mass = 800/1000 + 200/1000 = 1.0 → 25*log10(1 + 1.0/0.1) = 26.03
    assert s.risk_index == 26.03
    # exploit weights: finding 1 = max(0.9, 1.0)*1.0 = 1.0 (validated, critical
    # asset); finding 2 = max(0.1, 0.6)*0.25 = 0.15 (exploitable, low asset).
    # mass 1.15 → 25*log10(1 + 11.5) = 27.42
    assert s.exploitable_score == 27.42
    # blend = 0.6*26.03 + 0.4*27.44 = 26.59 → posture = round(100-26.59) = 73
    assert s.posture_score == 73
    assert s.grade == "C"
    # Both inputs still matter: drop the validated exploit and the score improves.
    milder = compute_scores([
        _fv(risk_score=800, epss_score=0.9, asset_criticality="critical"),
        _fv(risk_score=200, epss_score=0.1, exploitable=True, asset_criticality="low"),
    ])
    assert milder.posture_score > s.posture_score


_T0 = datetime(2026, 1, 1, tzinfo=timezone.utc)   # previous run
_T1 = datetime(2026, 2, 1, tzinfo=timezone.utc)   # latest run


def test_build_posture_no_runs():
    assert build_posture([], None, None) == {"has_runs": False}


def test_build_posture_single_run_has_no_prev():
    # one finding seen only at latest run
    fv = _fv(id="a", severity="high", risk_score=500, first_seen=_T1, last_seen=_T1)
    out = build_posture([fv], None, {"id": "L", "started_at": _T1})
    assert out["has_runs"] is True
    assert out["previous_run"] is None
    assert out["new_count"] == 1
    assert out["resolved_count"] == 0
    # matrix: high row shows new=1, prev_open=0
    high = next(r for r in out["matrix"] if r["severity"] == "high")
    assert high["new"] == 1 and high["prev_open"] == 0 and high["now_open"] == 1


def test_build_posture_buckets_resolved_new_persisting():
    resolved = _fv(id="r", severity="critical", risk_score=900,
                   first_seen=_T0, last_seen=_T0)                 # in P, gone from L
    persisting = _fv(id="p", severity="high", risk_score=400,
                     first_seen=_T0, last_seen=_T1)               # in both
    new = _fv(id="n", severity="medium", risk_score=300,
              first_seen=_T1, last_seen=_T1)                      # only in L
    out = build_posture(
        [resolved, persisting, new],
        {"id": "P", "started_at": _T0},
        {"id": "L", "started_at": _T1},
    )
    assert out["resolved_count"] == 1
    assert out["new_count"] == 1
    assert out["persisting_count"] == 1
    assert out["risk_burned_down"] == 900.0
    crit = next(r for r in out["matrix"] if r["severity"] == "critical")
    assert crit["resolved"] == 1 and crit["now_open"] == 0 and crit["net"] == -1


class _Row:
    def __init__(self, **kw):
        self.__dict__.update(kw)


def test_finding_views_maps_columns_and_asset_criticality():
    rows = [
        _Row(id="1", severity=type("S", (), {"value": "high"})(),
             risk_score=400, epss_score=0.2, exploitable=True,
             exploit_validated=False, asset_criticality="critical",
             first_seen=_T0, last_seen=_T1),
    ]
    views = _finding_views(rows)
    assert views[0].id == "1"
    assert views[0].severity == "high"
    assert views[0].asset_criticality == "critical"
    assert views[0].exploitable is True


def test_finding_views_handles_null_asset_and_scores():
    # OUTER-join case: no asset, and null risk/epss scores.
    rows = [
        _Row(id="2", severity=type("S", (), {"value": "low"})(),
             risk_score=None, epss_score=None, exploitable=False,
             exploit_validated=False, asset_criticality=None,
             first_seen=None, last_seen=None),
    ]
    v = _finding_views(rows)[0]
    assert v.asset_criticality is None
    assert v.risk_score is None
    assert v.epss_score is None
    assert v.severity == "low"


def test_enum_str_passes_through_plain_string():
    from app.routers.analytics import _enum_str
    assert _enum_str("high") == "high"
    assert _enum_str(type("S", (), {"value": "critical"})()) == "critical"


def test_posture_report_section_renders_scores_and_matrix():
    posture = {
        "has_runs": True,
        "scores": {"risk_index": 40.0, "exploitable_score": 20.0, "posture_score": 68, "grade": "C"},
        "scores_prev": {"risk_index": 55.0, "exploitable_score": 30.0, "posture_score": 55, "grade": "C"},
        "matrix": [{"severity": "critical", "prev_open": 2, "new": 0, "resolved": 1, "now_open": 1, "net": -1}],
        "risk_burned_down": 900.0, "resolved_count": 1, "new_count": 0, "persisting_count": 1,
        "previous_run": {"id": "P", "started_at": "2026-01-01T00:00:00+00:00"},
        "latest_run": {"id": "L", "started_at": "2026-02-01T00:00:00+00:00"},
    }
    section = build_posture_report_section(posture)
    assert section["title"] == "Posture & Remediation Progress"
    assert section["kind"] == "posture"
    assert "Posture Score: 68/100 (C)" in section["content"]
    # The customer must be told what scale these numbers live on.
    assert "0–100, lower is better" in section["content"]
    assert "critical" in section["content"]
    assert "900" in section["content"]


def test_posture_report_section_omitted_without_runs():
    assert build_posture_report_section({"has_runs": False}) is None


# ── Remediation actually counts as "Patched" ──────────────────────────────────
# Regression guard for the defect where the dashboard's "Patched" column, the
# "Closed since last scan" percentage and "risk burned down" all read zero no
# matter how much the customer fixed. The routers loaded only open/confirmed
# findings, but a fixed finding's status is `remediated` (written by the
# auto-resolver and by an operator closing one by hand), so it was filtered out
# of the query before compare() could ever bucket it as resolved.


def test_remediated_finding_counts_as_resolved():
    """A finding fixed since the previous run lands in `resolved`, not limbo."""
    fixed = _fv(id="fixed", severity="critical", risk_score=900,
                first_seen=_T0, last_seen=_T0, status="remediated")
    still_open = _fv(id="open", severity="high", risk_score=400,
                     first_seen=_T0, last_seen=_T1, status="open")
    out = build_posture(
        [fixed, still_open],
        {"id": "P", "started_at": _T0},
        {"id": "L", "started_at": _T1},
    )
    assert out["resolved_count"] == 1
    assert out["risk_burned_down"] == 900.0
    crit = next(r for r in out["matrix"] if r["severity"] == "critical")
    assert crit["prev_open"] == 1      # it WAS open at the previous run
    assert crit["resolved"] == 1       # and it has been patched since
    assert crit["now_open"] == 0
    assert crit["net"] == -1


def test_finding_closed_after_the_latest_run_is_not_still_counted_open():
    """Observed in the latest run, then closed. `latest_open` must drop it.

    `_present_in_run` is a pure time window, so this finding still falls inside
    the latest run — only the status tells us it is no longer a live exposure.
    """
    closed_late = _fv(id="late", severity="critical", risk_score=900,
                      first_seen=_T0, last_seen=_T1, status="remediated")
    out = build_posture(
        [closed_late],
        {"id": "P", "started_at": _T0},
        {"id": "L", "started_at": _T1},
    )
    crit = next(r for r in out["matrix"] if r["severity"] == "critical")
    assert crit["now_open"] == 0
    assert crit["resolved"] == 1
    # It must not drag the CURRENT score down either.
    assert out["scores"]["posture_score"] == 100
    # ...but the previous run's score still reflects that it was open then.
    assert out["scores_prev"]["posture_score"] < 100


def test_status_defaults_to_open_for_callers_that_only_pass_live_findings():
    """portal.py and other callers build views without a status; they must not
    silently become inactive and vanish from the score."""
    v = FindingView(
        id="x", severity="high", risk_score=500, epss_score=None,
        exploitable=False, exploit_validated=False, asset_criticality=None,
        first_seen=_T1, last_seen=_T1,
    )
    assert v.status == "open"
    assert v.is_active is True
    out = build_posture([v], None, {"id": "L", "started_at": _T1})
    assert out["new_count"] == 1


def test_posture_statuses_include_remediated_but_not_accepted_or_fp():
    """The query contract compare() depends on. Risk-accepted is not a fix and a
    false positive was never an exposure, so neither belongs in a patch ledger."""
    from app.models.enums import FindingStatus
    from app.routers.analytics import POSTURE_STATUSES

    assert FindingStatus.remediated in POSTURE_STATUSES
    assert FindingStatus.open in POSTURE_STATUSES
    assert FindingStatus.confirmed in POSTURE_STATUSES
    assert FindingStatus.accepted not in POSTURE_STATUSES
    assert FindingStatus.fp not in POSTURE_STATUSES

from __future__ import annotations

from datetime import datetime, timezone

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
    # noisy-OR: two independent 0.5 → 1-(0.5*0.5)=0.75 → 75.0
    assert aggregate([0.5, 0.5]) == 75.0
    # values clamp to [0,1]
    assert aggregate([5.0]) == 100.0


def test_aggregate_is_monotonic():
    before = aggregate([0.4, 0.4])
    after = aggregate([0.4, 0.4, 0.3])
    assert after >= before


def test_grade_bands():
    assert grade_for(95) == "A"
    assert grade_for(90) == "A"
    assert grade_for(80) == "B"
    assert grade_for(60) == "C"
    assert grade_for(40) == "D"
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
    # risk_index = 100*(1-(1-0.8)(1-0.2)) = 100*(1-0.16) = 84.0
    assert s.risk_index == 84.0
    # finding 1 exploit prob = max(0.9,0.6? no,1.0)*1.0 = 1.0 → aggregate saturates to 100
    assert s.exploitable_score == 100.0
    # blend = 0.6*84 + 0.4*100 = 90.4 → posture = round(100-90.4)=10 → grade F
    assert s.posture_score == 10
    assert s.grade == "F"


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


def test_sev_str_passes_through_plain_string():
    from app.routers.analytics import _sev_str
    assert _sev_str("high") == "high"
    assert _sev_str(type("S", (), {"value": "critical"})()) == "critical"


from app.routers.ai_report import build_posture_report_section


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
    assert "Posture Score: 68 (C)" in section["content"]
    assert "critical" in section["content"]
    assert "900" in section["content"]


def test_posture_report_section_omitted_without_runs():
    assert build_posture_report_section({"has_runs": False}) is None

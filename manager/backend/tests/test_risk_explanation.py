"""
The risk explanation must be the calculation, not a story about it.

`explain_risk_rank` is checked three ways:
  1. against a frozen copy of the formula as it stood BEFORE the explanation existed
     (so refactoring cannot silently move anyone's score),
  2. for internal consistency (dimension points add up to the additive score, the
     final rank sits inside the severity band),
  3. for honesty (a value that was not recorded is marked `default`, never `recorded`).
"""
from __future__ import annotations

import itertools

import pytest

from app.services.risk_rank import compute_risk_rank, explain_risk_rank

# ── frozen reference: the original compute_risk_rank, verbatim ────────────────
_SEV = {"critical": 1.0, "high": 0.8, "medium": 0.55, "low": 0.25, "info": 0.05}
_ASSET = {"critical": 1.0, "high": 0.75, "medium": 0.5, "low": 0.25}
_VERIF = {"confirmed": 1.0, "corroborated": 0.75, "inferred": 0.45, "contradicted": 0.0}
_BAND = {"critical": (750, 1000), "high": (500, 749), "medium": (250, 499),
         "low": (100, 249), "info": (0, 99)}


def _b(v, lo=0.0, hi=1.0):
    return max(lo, min(hi, v))


def legacy_rank(*, severity, cvss_score, epss_score, kev, exploit_validated, verification_state,
                confidence, asset_criticality, internet_facing, auth_enforced):
    sev_key = (severity or "info").lower()
    if sev_key not in _BAND:
        sev_key = "info"
    severity_n = _SEV[sev_key]
    impact_n = severity_n if cvss_score is None else _b(float(cvss_score) / 10.0) * 0.8 + severity_n * 0.2
    epss_n = _b(float(epss_score)) if epss_score is not None else 0.0
    exploit_n = epss_n * 0.45 + float(bool(kev)) * 0.35 + float(bool(exploit_validated)) * 0.20
    asset_n = _ASSET.get((asset_criticality or "").lower(), 0.5)
    exposure_n = 0.5 if internet_facing is None else float(internet_facing)
    auth_gap_n = 0.5 if auth_enforced is None else float(not auth_enforced)
    context_n = asset_n * 0.45 + exposure_n * 0.35 + auth_gap_n * 0.20
    verdict_n = _VERIF.get((verification_state or "").lower(), 0.65)
    confidence_n = _b(int(confidence) / 100.0) if confidence is not None else 0.65
    evidence_n = verdict_n * 0.60 + confidence_n * 0.40
    score = (impact_n * 0.40 + exploit_n * 0.25 + context_n * 0.20 + evidence_n * 0.15) * 1000.0
    position = _b(score / 1000.0)
    floor, ceiling = _BAND[sev_key]
    return int(round(floor + position * (ceiling - floor)))


def _grid():
    return itertools.product(
        ["critical", "high", "medium", "low", "info", "bogus", None],
        [None, 0.0, 4.3, 7.5, 9.8, 10.0],
        [None, 0.0, 0.31, 0.97],
        [False, True],
        [False, True],
        [None, "confirmed", "corroborated", "inferred", "contradicted", "weird"],
        [None, 0, 55, 92, 100],
        [None, "critical", "high", "medium", "low", "unknown"],
        [None, True, False],
        [None, True, False],
    )


def _kw(t):
    keys = ("severity", "cvss_score", "epss_score", "kev", "exploit_validated", "verification_state",
            "confidence", "asset_criticality", "internet_facing", "auth_enforced")
    return dict(zip(keys, t))


def test_score_matches_the_pre_explanation_formula_everywhere():
    n = 0
    for t in _grid():
        kw = _kw(t)
        expected = legacy_rank(**kw)
        assert compute_risk_rank(**kw) == expected, kw
        assert explain_risk_rank(**kw)["score"] == expected, kw
        n += 1
    assert n > 100_000     # the grid really is exhaustive enough to mean something


def test_dimension_points_add_up_to_the_additive_score():
    for t in itertools.islice(_grid(), 0, None, 97):
        e = explain_risk_rank(**_kw(t))
        total = sum(d["points"] for d in e["dimensions"])
        assert abs(total - e["additive_score"]) <= 0.25, (t, total, e["additive_score"])


def test_weights_sum_to_one_and_inputs_weight_within_each_dimension():
    e = explain_risk_rank(**_kw(("high", 7.5, 0.4, True, False, "confirmed", 80, "high", True, False)))
    assert round(sum(d["weight"] for d in e["dimensions"]), 6) == 1.0
    for d in e["dimensions"]:
        assert round(sum(i["weight"] for i in d["inputs"]), 6) == 1.0, d["key"]
        # the dimension value is exactly the weighted sum of its inputs
        assert abs(sum(i["normalized"] * i["weight"] for i in d["inputs"]) - d["value"]) < 2e-4, d["key"]


def test_final_rank_sits_inside_the_severity_band():
    for t in itertools.islice(_grid(), 0, None, 211):
        e = explain_risk_rank(**_kw(t))
        assert e["band"]["floor"] <= e["score"] <= e["band"]["ceiling"], e
        expected = round(e["band"]["floor"] + e["band"]["position"] * (e["band"]["ceiling"] - e["band"]["floor"]))
        assert abs(e["score"] - expected) <= 1   # position is rounded to 4 d.p. for display


def test_missing_values_are_marked_default_not_recorded():
    e = explain_risk_rank(**_kw(("critical", None, None, False, False, None, None, None, None, None)))
    assert set(e["defaults_used"]) == {
        "cvss", "epss", "asset_criticality", "internet_facing", "auth_gap", "verification", "confidence"}
    by_key = {i["key"]: i for d in e["dimensions"] for i in d["inputs"]}
    assert by_key["epss"]["source"] == "default" and "not as safe" in by_key["epss"]["note"]
    assert by_key["severity"]["source"] == "recorded"


def test_recorded_values_are_marked_recorded():
    e = explain_risk_rank(**_kw(("high", 8.1, 0.2, True, True, "corroborated", 70, "medium", False, True)))
    assert e["defaults_used"] == []
    by_key = {i["key"]: i for d in e["dimensions"] for i in d["inputs"]}
    assert by_key["cvss"]["raw"] == 8.1 and by_key["cvss"]["normalized"] == 0.81
    assert by_key["kev"]["raw"] is True and by_key["kev"]["normalized"] == 1.0


def test_unrecognised_asset_criticality_is_a_default_not_recorded():
    e = explain_risk_rank(**_kw(("high", 5.0, 0.1, False, False, "inferred", 50, "unknown", None, None)))
    by_key = {i["key"]: i for d in e["dimensions"] for i in d["inputs"]}
    assert by_key["asset_criticality"]["source"] == "default"


def test_the_smbv1_example_from_the_live_console():
    """A critical config finding with no CVE: 911 with neutral asset context."""
    e = explain_risk_rank(**_kw(("critical", None, None, False, False, "confirmed", 92, None, None, None)))
    assert e["score"] == 911
    assert e["band"] == {"floor": 750, "ceiling": 1000, "position": 0.6452}


@pytest.mark.parametrize("sev", ["critical", "high", "medium", "low", "info"])
def test_band_order_never_contradicts_severity_order(sev):
    lows = {s: explain_risk_rank(**_kw((s, None, None, False, False, "contradicted", 0, "low", False, False)))["score"]
            for s in ("critical", "high", "medium", "low", "info")}
    highs = {s: explain_risk_rank(**_kw((s, 10.0, 1.0, True, True, "confirmed", 100, "critical", True, True)))["score"]
             for s in ("critical", "high", "medium", "low", "info")}
    order = ["info", "low", "medium", "high", "critical"]
    for a, b in zip(order, order[1:]):
        assert highs[a] < lows[b]

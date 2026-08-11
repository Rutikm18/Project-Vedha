from __future__ import annotations

from app.detection.active_validation import should_escalate


def _ev(**kw):
    base = {"state": "suspected", "source_confidence": "inferred",
            "priority": "high", "kev": False}
    base.update(kw)
    return base


def test_high_severity_suspected_escalates_when_roe_allows():
    assert should_escalate(_ev(), roe_allows=True, profile="it") is True


def test_kev_escalates_even_if_medium():
    assert should_escalate(_ev(priority="medium", kev=True), roe_allows=True, profile="it") is True


def test_confirmed_authoritative_does_not_escalate():
    assert should_escalate(_ev(state="confirmed", source_confidence="authoritative"),
                           roe_allows=True, profile="it") is False


def test_roe_forbids_blocks_escalation():
    assert should_escalate(_ev(), roe_allows=False, profile="it") is False


def test_ot_profile_never_escalates():
    assert should_escalate(_ev(), roe_allows=True, profile="ot") is False


def test_low_severity_non_kev_does_not_escalate():
    assert should_escalate(_ev(priority="low", kev=False), roe_allows=True, profile="it") is False

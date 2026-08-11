from __future__ import annotations

from app.detection.active_validation import interpret_validation


def test_confirmed_upgrades_and_sets_exploit_validated():
    out = interpret_validation({"outcome": "confirmed"})
    assert out.outcome == "confirmed"
    assert out.verification_state == "confirmed"
    assert out.exploit_validated is True


def test_contradicted_marks_false_positive():
    out = interpret_validation({"outcome": "contradicted"})
    assert out.outcome == "contradicted"
    assert out.verification_state == "contradicted"
    assert out.exploit_validated is False


def test_inconclusive_keeps_state_unchanged():
    out = interpret_validation({"outcome": "inconclusive"})
    assert out.outcome == "inconclusive"
    assert out.verification_state is None   # no change
    assert out.exploit_validated is False


def test_missing_or_garbage_result_is_inconclusive():
    assert interpret_validation({}).outcome == "inconclusive"
    assert interpret_validation({"outcome": "weird"}).outcome == "inconclusive"

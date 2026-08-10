from __future__ import annotations

from app.detection.resolution import decide_resolution, resolution_threshold
from app.models.enums import FindingSeverity


def test_threshold_is_stricter_for_critical_and_high():
    assert resolution_threshold(FindingSeverity.critical) == 2
    assert resolution_threshold(FindingSeverity.high) == 2
    assert resolution_threshold(FindingSeverity.medium) == 1
    assert resolution_threshold(FindingSeverity.low) == 1
    assert resolution_threshold(FindingSeverity.info) == 1


def test_not_covered_is_skipped_and_counter_untouched():
    out = decide_resolution(covered=False, db_changed=False,
                            miss_count=0, severity=FindingSeverity.medium)
    assert out.action == "skip"
    assert out.miss_count == 0


def test_db_change_blocks_resolution():
    out = decide_resolution(covered=True, db_changed=True,
                            miss_count=0, severity=FindingSeverity.medium)
    assert out.action == "skip"
    assert out.miss_count == 0


def test_medium_resolves_on_first_covered_clean_run():
    out = decide_resolution(covered=True, db_changed=False,
                            miss_count=0, severity=FindingSeverity.medium)
    assert out.action == "resolve"
    assert out.miss_count == 1


def test_high_needs_two_covered_clean_runs():
    first = decide_resolution(covered=True, db_changed=False,
                              miss_count=0, severity=FindingSeverity.high)
    assert first.action == "pending"
    assert first.miss_count == 1
    second = decide_resolution(covered=True, db_changed=False,
                               miss_count=1, severity=FindingSeverity.high)
    assert second.action == "resolve"
    assert second.miss_count == 2

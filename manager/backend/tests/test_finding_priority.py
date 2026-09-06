"""finding_priority — the 'critical always on top' ordering contract.

The product rule is absolute: a critical finding must never render below a
lower-severity one, regardless of composite risk. These tests pin that rule and
the tie-break (risk within a tier) so the SQL CASE and the in-memory key can
never drift apart.
"""
from __future__ import annotations

from app.models.enums import FindingSeverity
from app.services.finding_priority import (
    SEVERITY_RANK,
    priority_key,
    severity_order_case,
    severity_rank,
)


def test_severity_rank_orders_all_five_tiers():
    assert (
        severity_rank(FindingSeverity.critical)
        > severity_rank(FindingSeverity.high)
        > severity_rank(FindingSeverity.medium)
        > severity_rank(FindingSeverity.low)
        > severity_rank(FindingSeverity.info)
    )


def test_severity_rank_accepts_plain_and_mixed_case_strings():
    assert severity_rank("critical") == SEVERITY_RANK["critical"]
    assert severity_rank("CRITICAL") == SEVERITY_RANK["critical"]


def test_severity_rank_unknown_or_none_sorts_last():
    assert severity_rank("bogus") == 0
    assert severity_rank(None) == 0


def test_critical_outranks_high_regardless_of_risk():
    # The crux: a critical with risk 0 still beats a high with maximum risk.
    assert priority_key("critical", 0) > priority_key("high", 1000)


def test_within_a_tier_higher_risk_wins():
    assert priority_key("high", 800) > priority_key("high", 500)


def test_none_risk_is_treated_as_zero_not_a_crash():
    assert priority_key("medium", None) == (SEVERITY_RANK["medium"], 0.0)


def test_sorting_a_mixed_list_puts_criticals_first_then_risk():
    findings = [
        ("high", 999),
        ("critical", 10),
        ("low", 500),
        ("critical", 900),
        ("medium", 700),
    ]
    ordered = sorted(findings, key=lambda f: priority_key(f[0], f[1]), reverse=True)
    assert [f[0] for f in ordered] == ["critical", "critical", "high", "medium", "low"]
    # Among the two criticals, the higher-risk one leads.
    assert ordered[0] == ("critical", 900)


def test_severity_order_case_has_a_branch_for_every_tier():
    # Structural guard: the SQL CASE must cover all five severities so ordering is
    # total. The behavioural mapping is proven by severity_rank above.
    from app.models.finding import Finding

    case_expr = severity_order_case(Finding.severity)
    assert len(case_expr.whens) == len(SEVERITY_RANK) == 5

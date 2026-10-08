"""
test_branch_rule_coverage.py — every deep branch must be ASSESSED, not just collected.

THE FAILURE CLASS. Two guards already exist and neither catches this one:

  * test_risk_port_coverage  — a port the manager can flag must be SCANNED.
  * test_fact_contract       — a path a rule READS must be EMITTED.

Both run from the rule inward. Nothing ran the other way: a scanner that emits
facts no rule ever reads. db_scan sat in that blind spot for the entire life of
the project — it ran on every network_va, shipped engine/version/auth facts,
stored them with a trust tier and an evidence record, and produced zero findings.
An unauthenticated Redis was indistinguishable from a hardened one.

That is the worst possible failure mode, because every health signal looks green:
the branch ran, the facts arrived, the detection completed, and the host was
reported clean.

EXEMPTIONS are deliberate and must stay small. A name here is an admission that
the probe is collecting evidence nobody assesses — a backlog item, not a
resolution. Adding a NEW scanner to this list should be argued for in review.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

import posture_rules as P

_PROBE = Path(__file__).resolve().parents[3] / "probe"

# Branch components that legitimately have no posture rule TODAY. Each is a
# known gap with a reason, not a permanent exemption.
KNOWN_UNASSESSED = {
    # Confirms a printer via a real PJL handshake. The facts support findings
    # (unauthenticated PJL control, exposed web admin) but none are written yet.
    "printer_scan",
}


def _branch_components() -> set[str]:
    if not _PROBE.exists():
        pytest.skip(f"probe tree not present at {_PROBE}")
    if str(_PROBE) not in sys.path:
        sys.path.insert(0, str(_PROBE))
    from workflow.branches import BRANCH_COMPONENT
    return set(BRANCH_COMPONENT.values())


def _scanners_with_rules() -> set[str]:
    keyed: set[str] = set()
    for rule in P.RULES:
        keyed.update(rule.scanners)
    return keyed


def test_every_deep_branch_has_at_least_one_rule():
    unassessed = _branch_components() - _scanners_with_rules() - KNOWN_UNASSESSED
    assert not unassessed, (
        "These scanners run on every assessment and emit facts that NO rule "
        f"reads, so they can never produce a finding: {sorted(unassessed)}\n"
        "Every health signal will look green while the weakness goes unreported. "
        "Write a rule, or add the scanner to KNOWN_UNASSESSED with a reason.")


def test_exemptions_are_still_real():
    """An exemption that has since gained a rule must be removed, or the list
    quietly grows into a place where gaps go to be forgotten."""
    stale = KNOWN_UNASSESSED & _scanners_with_rules()
    assert not stale, (
        f"{sorted(stale)} now have rules — remove them from KNOWN_UNASSESSED.")


def test_exemptions_name_real_branches():
    """A typo here would silently exempt nothing and mask a real gap."""
    unknown = KNOWN_UNASSESSED - _branch_components()
    assert not unknown, f"KNOWN_UNASSESSED names non-existent branches: {sorted(unknown)}"


def test_db_scan_is_assessed():
    """The regression this whole file exists for."""
    assert "db_scan" in _scanners_with_rules()

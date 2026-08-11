"""
active_validation.py — manager-side decision core for safe active validation.

PURE: no DB, no network, no probe. should_escalate() decides whether a finding
warrants a live re-check; interpret_validation() maps a probe's safe-check result
back to a verdict transition. The approval gate, job dispatch, and probe-side
validator are wired around this core (see the P3 plan) — this module holds the
logic so it is unit-testable offline.
"""
from __future__ import annotations

from dataclasses import dataclass

_HIGH_STAKES = ("critical", "high")


def should_escalate(evidence: dict, *, roe_allows: bool, profile: str | None) -> bool:
    """True iff this finding warrants an approval-gated active re-check.
    Escalate only uncertain + high-stakes findings, and only when RoE allows and
    the profile isn't OT (structurally passive)."""
    if not roe_allows:
        return False
    if (profile or "").lower() == "ot":
        return False
    state = evidence.get("state")
    source = evidence.get("source_confidence")
    if state == "confirmed" or source == "authoritative":
        return False  # already authoritative — nothing to validate
    high_stakes = (evidence.get("priority") or "").lower() in _HIGH_STAKES or bool(evidence.get("kev"))
    return high_stakes

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


@dataclass
class ValidationOutcome:
    outcome: str                     # confirmed | contradicted | inconclusive
    verification_state: str | None   # new verification_state, or None to leave unchanged
    exploit_validated: bool


def interpret_validation(result: dict) -> ValidationOutcome:
    """Map a probe safe-check result to a verdict transition. Anything that isn't
    an explicit confirm/contradict is inconclusive — which NEVER downgrades a
    finding to resolved and NEVER lowers below its current state."""
    outcome = (result or {}).get("outcome")
    if outcome not in ("confirmed", "contradicted", "inconclusive"):
        if result.get("confirmed") is True:
            outcome = "confirmed"
        elif result.get("contradicted") is True:
            outcome = "contradicted"
        else:
            outcome = "inconclusive"
    if outcome == "confirmed":
        return ValidationOutcome("confirmed", "confirmed", True)
    if outcome == "contradicted":
        return ValidationOutcome("contradicted", "contradicted", False)
    return ValidationOutcome("inconclusive", None, False)

"""
verification.py — normalized, dashboard-facing verification verdict.

The deterministic detection engine already calibrates a 0-100 `confidence` and
an evidence tier per finding (see detection_engine/verifier.py). This module
maps that into a small, human-facing vocabulary and an FP-triage flag:

    confirmed    authoritative/credentialed truth
    corroborated strong network evidence (protocol/multi-signal, high confidence)
    inferred     weak/single-signal, uncorroborated
    contradicted evidence actively refutes (set by the LLM/active tiers, not here)

PURE: no DB, no network, no LLM, no LangGraph. compute_verdict() is the whole
substance of passive verification and is fully unit-tested offline. The optional
LLM rationale (verify_finding) and LangGraph skin (verification_graph.py) wrap
this; they can only lower confidence or flag review — never raise it.
"""
from __future__ import annotations

from dataclasses import dataclass

VERIFICATION_STATES = frozenset({"confirmed", "corroborated", "inferred", "contradicted"})

# Confidence at/above this (for non-authoritative findings) reads as corroborated.
_CORROBORATED_FLOOR = 70


@dataclass
class VerificationVerdict:
    state: str
    confidence: int
    needs_review: bool
    rationale: str
    method: str = "passive"


def _int_confidence(evidence: dict) -> int:
    c = evidence.get("confidence")
    if isinstance(c, (int, float)):
        return max(0, min(100, int(c)))
    # No calibrated confidence recorded → treat as weak evidence.
    return 40


def compute_verdict(evidence: dict) -> VerificationVerdict:
    """Deterministic passive verdict from a detection finding's evidence dict."""
    source = evidence.get("source_confidence")
    state = evidence.get("state")
    conf = _int_confidence(evidence)

    if source == "authoritative" or state == "confirmed":
        vstate, reason = "confirmed", "authoritative/credentialed evidence"
    elif conf >= _CORROBORATED_FLOOR:
        vstate, reason = "corroborated", f"network evidence, confidence {conf}"
    else:
        vstate, reason = "inferred", f"weak/single-signal evidence, confidence {conf}"

    # High-stakes uncertainty → surface for analyst review.
    kev = bool(evidence.get("kev"))
    priority = (evidence.get("priority") or "").lower()
    uncertain = state in ("suspected", "potential") and vstate != "confirmed"
    needs_review = uncertain and (kev or priority in ("critical", "high"))
    if needs_review:
        reason += "; flagged for review (high-stakes + uncertain)"

    return VerificationVerdict(state=vstate, confidence=conf,
                               needs_review=needs_review, rationale=reason)


import structlog  # noqa: E402  (grouped with the LLM entrypoint below)

logger = structlog.get_logger()


def _qualifies_for_llm(verdict: VerificationVerdict, evidence: dict) -> bool:
    """Only spend an LLM call where a rationale / FP-triage is worth it:
    uncertain AND high-stakes. Everything else keeps the cheap verdict."""
    priority = (evidence.get("priority") or "").lower()
    return verdict.needs_review or priority in ("critical", "high")


async def verify_finding(evidence: dict, llm=None) -> VerificationVerdict:
    """Deterministic verdict, optionally enriched by an LLM rationale. The LLM
    (duck-typed: must expose `async verify_rationale(evidence) -> dict`) can only
    add a rationale, flag needs_review, and — when confidence is already low —
    mark the verdict contradicted. It can NEVER raise confidence or override a
    confirmed verdict. Any LLM failure yields the pure deterministic verdict."""
    verdict = compute_verdict(evidence)
    if llm is None or verdict.state == "confirmed" or not _qualifies_for_llm(verdict, evidence):
        return verdict
    try:
        out = await llm.verify_rationale(evidence)
    except Exception as exc:  # noqa: BLE001 — LLM must never break verification
        logger.warning("verification.llm_failed", error=str(exc))
        return verdict
    if not isinstance(out, dict):
        return verdict
    rationale = str(out.get("rationale") or "").strip()
    fp = bool(out.get("suspected_false_positive"))
    new_reason = rationale or verdict.rationale
    needs_review = verdict.needs_review or fp
    # LLM may only DOWNGRADE: an FP flag on an already-weak finding → contradicted.
    new_state = verdict.state
    if fp and verdict.confidence < _CORROBORATED_FLOOR:
        new_state = "contradicted"
    return VerificationVerdict(state=new_state, confidence=verdict.confidence,
                               needs_review=needs_review, rationale=new_reason,
                               method="passive")

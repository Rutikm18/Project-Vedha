"""
agent_policy.py — the deterministic policy engine for the Autonomous Engagement
Agent. Pure (no DB/network/LLM): given a proposed agent action and an engagement's
Rules of Engagement, it decides whether the action may auto-run, needs human
approval, or is denied.

Safety design (see docs/superpowers/specs/2026-08-16-vedha-autonomous-engagement-agent-design.md):
  * Actions are classed by RISK TIER (passive → reversible → intrusive → irreversible).
  * VERDICT-vs-ACTION separation: `authorized` is the hard gate (scope, denylist,
    halt, blast-radius); `requires_approval` is the human gate (tier above the
    autonomy ceiling, or the always-human irreversible tier).
  * FAIL CLOSED: unknown actions are treated as irreversible (highest tier).
  * Scope is delegated to services/scope_targets so the agent gate cannot drift
    from the scan-dispatch gate.
"""
from __future__ import annotations

# Risk tiers (higher = more dangerous / less reversible).
TIER_PASSIVE = 0        # recon, read-only, RAG lookups
TIER_REVERSIBLE = 1     # scans, non-destructive validation, metadata writes
TIER_INTRUSIVE = 2      # exploit execution, credential use, lateral movement
TIER_IRREVERSIBLE = 3   # exfil beyond proof, DoS, egress, state mutation

# The agent's action vocabulary → tier. Anything absent fails closed to the
# highest tier via classify_action's default.
_ACTION_TIERS: dict[str, int] = {
    "no_action": TIER_PASSIVE,
    "recon": TIER_PASSIVE,
    "rag_lookup": TIER_PASSIVE,
    "read_engagement_data": TIER_PASSIVE,
    "run_discovery_scan": TIER_REVERSIBLE,
    "run_targeted_scan": TIER_REVERSIBLE,
    "recheck_finding": TIER_REVERSIBLE,
    "mark_false_positive": TIER_REVERSIBLE,
    "escalate_finding": TIER_REVERSIBLE,
    "request_exploit_validation": TIER_INTRUSIVE,
    "run_exploit": TIER_INTRUSIVE,
    "lateral_move": TIER_INTRUSIVE,
    "post_exploit_enum": TIER_INTRUSIVE,
    "exfiltrate": TIER_IRREVERSIBLE,
    "dos": TIER_IRREVERSIBLE,
}


def classify_action(action: str) -> int:
    """Map an action name to its risk tier; unknown actions fail closed."""
    return _ACTION_TIERS.get(action, TIER_IRREVERSIBLE)

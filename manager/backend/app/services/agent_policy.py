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

from dataclasses import dataclass, field

from app.services.scope_targets import validate_targets_in_scope

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


@dataclass(frozen=True)
class RulesOfEngagement:
    """The deterministic authorization envelope for one engagement's agent."""
    scope_cidrs: tuple[str, ...]
    excluded_cidrs: tuple[str, ...] = ()
    autonomy_ceiling: int = TIER_REVERSIBLE      # auto-authorize up to this tier
    module_denylist: frozenset[str] = field(default_factory=frozenset)
    halted: bool = False                         # kill-switch
    max_hosts: int | None = None                 # blast-radius caps (None = unbounded)
    max_exploit_attempts: int | None = None


@dataclass(frozen=True)
class UsageCounters:
    """Running engagement usage, checked against the blast-radius caps."""
    hosts_touched: int = 0
    exploit_attempts: int = 0


@dataclass(frozen=True)
class Decision:
    action: str
    tier: int
    authorized: bool          # hard gate: may this proceed at all?
    requires_approval: bool   # human gate: must an operator authorize first?
    reason: str


def _deny(action: str, tier: int, reason: str) -> Decision:
    return Decision(action, tier, authorized=False, requires_approval=False, reason=reason)


def evaluate_action(action: str, roe: RulesOfEngagement, *,
                    targets=None, module: str | None = None,
                    counters: UsageCounters = UsageCounters()) -> Decision:
    """Decide whether `action` may proceed under `roe`. Order is deliberate:
    hard denials (halt, denylist, scope, caps) before the human-gate decision."""
    tier = classify_action(action)

    # 1. Kill-switch: a halted engagement authorizes nothing.
    if roe.halted:
        return _deny(action, tier, "engagement halted (kill-switch active)")

    # 2. Denylisted exploit/module.
    if module and module in roe.module_denylist:
        return _deny(action, tier, f"module '{module}' is denylisted by rules of engagement")

    # 3. Scope: any action that touches network targets must stay in scope.
    if targets is not None:
        if validate_targets_in_scope(targets, list(roe.scope_cidrs),
                                     list(roe.excluded_cidrs)) is None:
            return _deny(action, tier, "target is outside the rules-of-engagement scope")

    # 4. Blast-radius caps (hard stop when reached).
    if (roe.max_exploit_attempts is not None and tier >= TIER_INTRUSIVE
            and counters.exploit_attempts >= roe.max_exploit_attempts):
        return _deny(action, tier, "exploit-attempt blast-radius cap reached")
    if (roe.max_hosts is not None and tier >= TIER_REVERSIBLE
            and counters.hosts_touched >= roe.max_hosts):
        return _deny(action, tier, "host blast-radius cap reached")

    # 5. Irreversible tier is ALWAYS human-approved, regardless of ceiling.
    if tier >= TIER_IRREVERSIBLE:
        return Decision(action, tier, authorized=True, requires_approval=True,
                        reason="irreversible action always requires human approval")

    # 6. Autonomy ceiling: auto up to the ceiling, else human-approve.
    requires_approval = tier > roe.autonomy_ceiling
    reason = ("within autonomy ceiling" if not requires_approval
              else f"tier {tier} exceeds autonomy ceiling {roe.autonomy_ceiling}")
    return Decision(action, tier, authorized=True,
                    requires_approval=requires_approval, reason=reason)

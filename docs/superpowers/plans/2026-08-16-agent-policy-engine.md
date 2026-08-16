# Autonomous Agent — Policy Engine & Rules of Engagement Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the pure, deterministic safety-decision core for the Vedha Autonomous Engagement Agent — classify any proposed agent action by risk tier and decide (given an engagement's Rules of Engagement) whether it may auto-run, needs human approval, or is denied.

**Architecture:** A single pure module `services/agent_policy.py` (no DB, no network, no LLM — mirrors the proven `services/remediation_kb.py` pattern). It reuses `services/scope_targets.py::validate_targets_in_scope` as the single source of truth for scope, so the agent's scope gate can never drift from the scan-dispatch gate. It encodes **verdict-vs-action separation**: `authorized` is the hard gate (scope/denylist/halt/blast-radius), `requires_approval` is the human gate (tier above the autonomy ceiling, or an always-human irreversible tier).

**Tech Stack:** Python 3.13, dataclasses, `ipaddress` (via the reused scope helper), pytest.

## Global Constraints

- Pure module: **no** DB, network, LLM, or `app.config` reads in `agent_policy.py`.
- **Fail closed:** unknown/unmapped actions classify as the highest tier (`TIER_IRREVERSIBLE`).
- **Reuse, don't reimplement scope:** call `validate_targets_in_scope`; never re-parse CIDRs here.
- **Tier 3 (irreversible) is ALWAYS human-approved** — never auto, regardless of autonomy ceiling.
- **Verdict ≠ action:** `Decision.authorized` (may it proceed at all) is distinct from `Decision.requires_approval` (must a human authorize first).
- Style: `from __future__ import annotations`, frozen dataclasses, module docstring explaining the safety rationale (match `remediation_kb.py`).
- Tests run focused with the venv from `manager/backend`: `.venv/bin/python -m pytest <file> -p no:cacheprovider -q` (never the whole suite — it hangs).

---

### Task 1: Action risk-tier classification

**Files:**
- Create: `manager/backend/app/services/agent_policy.py`
- Test: `manager/backend/tests/test_agent_policy.py`

**Interfaces:**
- Produces: `TIER_PASSIVE=0`, `TIER_REVERSIBLE=1`, `TIER_INTRUSIVE=2`, `TIER_IRREVERSIBLE=3` (ints); `classify_action(action: str) -> int`.

- [ ] **Step 1: Write the failing test**

Create `manager/backend/tests/test_agent_policy.py`:

```python
"""test_agent_policy.py — the pure deterministic agent policy engine."""
from __future__ import annotations

import pytest

from app.services import agent_policy as ap


class TestClassifyAction:
    @pytest.mark.parametrize("action,tier", [
        ("no_action", ap.TIER_PASSIVE),
        ("recon", ap.TIER_PASSIVE),
        ("read_engagement_data", ap.TIER_PASSIVE),
        ("run_discovery_scan", ap.TIER_REVERSIBLE),
        ("run_targeted_scan", ap.TIER_REVERSIBLE),
        ("recheck_finding", ap.TIER_REVERSIBLE),
        ("run_exploit", ap.TIER_INTRUSIVE),
        ("request_exploit_validation", ap.TIER_INTRUSIVE),
        ("lateral_move", ap.TIER_INTRUSIVE),
        ("exfiltrate", ap.TIER_IRREVERSIBLE),
        ("dos", ap.TIER_IRREVERSIBLE),
    ])
    def test_known_actions_map_to_expected_tier(self, action, tier):
        assert ap.classify_action(action) == tier

    def test_unknown_action_fails_closed_to_highest_tier(self):
        assert ap.classify_action("totally_unknown_action") == ap.TIER_IRREVERSIBLE
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd manager/backend && .venv/bin/python -m pytest tests/test_agent_policy.py -p no:cacheprovider -q`
Expected: FAIL with `ModuleNotFoundError: No module named 'app.services.agent_policy'`.

- [ ] **Step 3: Write minimal implementation**

Create `manager/backend/app/services/agent_policy.py`:

```python
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd manager/backend && .venv/bin/python -m pytest tests/test_agent_policy.py -p no:cacheprovider -q`
Expected: PASS (12 passed).

- [ ] **Step 5: Commit**

```bash
git add manager/backend/app/services/agent_policy.py manager/backend/tests/test_agent_policy.py
git commit -m "feat(agent): risk-tier action classification (fail-closed)"
```

---

### Task 2: Rules-of-Engagement evaluation (`evaluate_action`)

**Files:**
- Modify: `manager/backend/app/services/agent_policy.py`
- Test: `manager/backend/tests/test_agent_policy.py`

**Interfaces:**
- Consumes: `classify_action`, tier constants (Task 1); `validate_targets_in_scope` from `app.services.scope_targets`.
- Produces:
  - `RulesOfEngagement(scope_cidrs: tuple[str,...], excluded_cidrs: tuple[str,...]=(), autonomy_ceiling: int=TIER_REVERSIBLE, module_denylist: frozenset[str]=frozenset(), halted: bool=False, max_hosts: int|None=None, max_exploit_attempts: int|None=None)`
  - `UsageCounters(hosts_touched: int=0, exploit_attempts: int=0)`
  - `Decision(action: str, tier: int, authorized: bool, requires_approval: bool, reason: str)`
  - `evaluate_action(action: str, roe: RulesOfEngagement, *, targets=None, module: str|None=None, counters: UsageCounters=UsageCounters()) -> Decision`

- [ ] **Step 1: Write the failing tests**

Append to `manager/backend/tests/test_agent_policy.py`:

```python
def _roe(**kw):
    base = dict(scope_cidrs=("10.0.0.0/24",))
    base.update(kw)
    return ap.RulesOfEngagement(**base)


class TestEvaluateAction:
    def test_passive_action_auto_authorized(self):
        d = ap.evaluate_action("recon", _roe())
        assert d.authorized and not d.requires_approval

    def test_reversible_within_default_ceiling_auto(self):
        d = ap.evaluate_action("run_discovery_scan", _roe(), targets=["10.0.0.5"])
        assert d.authorized and not d.requires_approval

    def test_intrusive_above_ceiling_needs_approval(self):
        d = ap.evaluate_action("run_exploit", _roe(), targets=["10.0.0.5"])
        assert d.authorized and d.requires_approval  # ceiling defaults to reversible

    def test_intrusive_auto_when_ceiling_raised(self):
        d = ap.evaluate_action("run_exploit", _roe(autonomy_ceiling=ap.TIER_INTRUSIVE),
                               targets=["10.0.0.5"])
        assert d.authorized and not d.requires_approval

    def test_irreversible_always_needs_approval_even_with_max_ceiling(self):
        d = ap.evaluate_action("exfiltrate", _roe(autonomy_ceiling=ap.TIER_IRREVERSIBLE),
                               targets=["10.0.0.5"])
        assert d.authorized and d.requires_approval

    def test_target_out_of_scope_denied(self):
        d = ap.evaluate_action("run_targeted_scan", _roe(), targets=["8.8.8.8"])
        assert not d.authorized and "scope" in d.reason.lower()

    def test_excluded_target_denied(self):
        d = ap.evaluate_action("run_targeted_scan",
                               _roe(excluded_cidrs=("10.0.0.0/28",)), targets=["10.0.0.5"])
        assert not d.authorized

    def test_denylisted_module_denied(self):
        d = ap.evaluate_action("run_exploit", _roe(module_denylist=frozenset({"psexec"})),
                               targets=["10.0.0.5"], module="psexec")
        assert not d.authorized and "denylist" in d.reason.lower()

    def test_halted_engagement_denies_everything(self):
        d = ap.evaluate_action("recon", _roe(halted=True))
        assert not d.authorized and "halt" in d.reason.lower()

    def test_exploit_attempt_cap_denied(self):
        d = ap.evaluate_action("run_exploit", _roe(max_exploit_attempts=3),
                               targets=["10.0.0.5"],
                               counters=ap.UsageCounters(exploit_attempts=3))
        assert not d.authorized and "cap" in d.reason.lower()

    def test_host_cap_denied(self):
        d = ap.evaluate_action("run_targeted_scan", _roe(max_hosts=5),
                               targets=["10.0.0.5"],
                               counters=ap.UsageCounters(hosts_touched=5))
        assert not d.authorized

    def test_no_targets_skips_scope_check(self):
        # A passive action with no network target must not be scope-denied.
        d = ap.evaluate_action("read_engagement_data", _roe())
        assert d.authorized

    def test_decision_carries_action_and_tier(self):
        d = ap.evaluate_action("run_exploit", _roe(), targets=["10.0.0.5"])
        assert d.action == "run_exploit" and d.tier == ap.TIER_INTRUSIVE
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd manager/backend && .venv/bin/python -m pytest tests/test_agent_policy.py::TestEvaluateAction -p no:cacheprovider -q`
Expected: FAIL — `AttributeError: module 'app.services.agent_policy' has no attribute 'RulesOfEngagement'`.

- [ ] **Step 3: Write the implementation**

Append to `manager/backend/app/services/agent_policy.py`:

```python
from dataclasses import dataclass, field

from app.services.scope_targets import validate_targets_in_scope


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
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd manager/backend && .venv/bin/python -m pytest tests/test_agent_policy.py -p no:cacheprovider -q`
Expected: PASS (all Task 1 + Task 2 tests green).

- [ ] **Step 5: Commit**

```bash
git add manager/backend/app/services/agent_policy.py manager/backend/tests/test_agent_policy.py
git commit -m "feat(agent): rules-of-engagement policy evaluation (verdict-vs-action, blast-radius, kill-switch)"
```

---

## Self-Review

**1. Spec coverage (design §4 policy engine, §5 safety):**
- Tier classification (§4 tiers) → Task 1. ✓
- Verdict-vs-action separation (§5) → `authorized` vs `requires_approval` in Task 2. ✓
- Scope/RoE enforcement (§4, §5) → `evaluate_action` scope branch reusing `validate_targets_in_scope`. ✓
- Autonomy ceiling / Tier-2-auto / Tier-3-always-human (§4) → Task 2 steps 5–6. ✓
- Blast-radius caps + kill-switch (§5) → Task 2 branches 1 & 4. ✓
- Deferred to follow-on plans (NOT in this plan, by design): persisted RoE model + migration, kill-switch endpoints, the planner/executor/validator loop, RAG index. Each is its own spec/plan.

**2. Placeholder scan:** none — every step has full code and exact commands.

**3. Type consistency:** `classify_action(str)->int`, tier constants, and the three dataclasses are used consistently across Task 1→2; `evaluate_action` returns `Decision`; `validate_targets_in_scope` called with `list(...)` matching its `Sequence[str]` signature.

---

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-08-16-agent-policy-engine.md`. Two execution options:

1. **Subagent-Driven (recommended)** — I dispatch a fresh subagent per task, review between tasks.
2. **Inline Execution** — I execute the tasks in this session with checkpoints.

Which approach?

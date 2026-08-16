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

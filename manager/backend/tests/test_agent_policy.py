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

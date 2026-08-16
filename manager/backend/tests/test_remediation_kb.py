"""test_remediation_kb.py — the pure deterministic remediation knowledge base."""
from __future__ import annotations

from types import SimpleNamespace

import pytest

from app.services import remediation_kb as kb


def _f(title="", description="", cve_ids=None, remediation=""):
    return SimpleNamespace(title=title, description=description,
                           cve_ids=cve_ids or [], remediation=remediation)


class TestClassify:
    @pytest.mark.parametrize("title,expected", [
        ("SSLv3 supported (POODLE)", "weak_tls"),
        ("Server supports TLS 1.0", "weak_tls"),
        ("SMB signing not required", "smb_signing"),
        ("Remote Desktop (RDP) exposed", "exposed_rdp"),
        ("Anonymous FTP login allowed", "anon_ftp"),
        ("Default credentials on admin panel", "default_credentials"),
        ("OpenSSH weak ciphers (CBC)", "outdated_ssh"),
        ("Telnet service enabled", "open_mgmt_port"),
        ("Unpatched Apache — security update available", "missing_patch"),
    ])
    def test_keyword_categories(self, title, expected):
        assert kb.classify_finding(_f(title=title)) == expected

    def test_cve_without_keyword_is_patch(self):
        assert kb.classify_finding(_f(title="Some product issue",
                                      cve_ids=["CVE-2024-1234"])) == "missing_patch"

    def test_unmatched_is_generic(self):
        assert kb.classify_finding(_f(title="Interesting behaviour observed")) == "generic"

    def test_order_specificity_anon_ftp_beats_generic(self):
        # "anonymous ftp" should win even though "ftp" appears in many findings.
        assert kb.classify_finding(_f(title="Anonymous FTP access")) == "anon_ftp"


class TestRecipeShape:
    def test_every_recipe_step_has_all_os_keys(self):
        for name, recipe in kb.RECIPES.items():
            for step in recipe["steps"]:
                cmds = step["commands"]
                assert set(kb._OS_KEYS) <= set(cmds), f"{name} step missing OS keys"
                # generic is the required fallback and must be non-empty
                assert cmds["generic"], f"{name} step has empty generic"

    def test_every_recipe_has_required_fields(self):
        required = {"summary", "effort", "remediation_risk", "steps",
                    "verification", "long_term_recommendations", "compensating_controls"}
        for name, recipe in kb.RECIPES.items():
            assert required <= set(recipe), f"{name} missing fields"


class TestRecipeForFinding:
    def test_returns_kb_source_and_category(self):
        plan = kb.recipe_for_finding(_f(title="SSLv3 supported"), os="linux")
        assert plan["source"] == "deterministic_kb"
        assert plan["category"] == "weak_tls"
        assert plan["os"] == "linux"

    def test_steps_are_numbered_and_os_filtered(self):
        plan = kb.recipe_for_finding(_f(title="Missing patch"), os="windows")
        assert [s["step"] for s in plan["steps"]] == list(range(1, len(plan["steps"]) + 1))
        # windows commands surface for the patch step
        assert any("Install-WindowsUpdate" in c for c in plan["steps"][0]["commands_for_os"])

    def test_network_os_falls_back_to_generic_guidance(self):
        plan = kb.recipe_for_finding(_f(title="Weak TLS ciphers"), os="network")
        assert plan["os"] == "generic"
        # generic guidance is prose, not a shell command
        assert any("appliance" in c.lower() or "management" in c.lower()
                   for c in plan["steps"][0]["commands_for_os"])

    def test_unknown_finding_yields_generic_plan(self):
        plan = kb.recipe_for_finding(_f(title="mystery"), os="linux")
        assert plan["category"] == "generic"
        assert plan["steps"] and plan["summary"]

    def test_missing_os_defaults_to_generic(self):
        plan = kb.recipe_for_finding(_f(title="SMB signing not required"))
        assert plan["os"] == "generic"

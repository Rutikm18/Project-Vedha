"""test_remediation_recipes.py — the rule-keyed recipe catalogue.

The coverage guard is the point: a detection rule shipped without a recipe
would silently fall back to generic advice, which is exactly the defect this
catalogue replaces.
"""
from __future__ import annotations

import string
from types import SimpleNamespace

import pytest

from app.ai.hallucination import HallucinationGuard
from app.detection import engine_bridge as EB
from app.remediation import recipes
from app.remediation.context import build_context

pytestmark = pytest.mark.skipif(not EB._ensure_importable(),
                                reason="detection_engine not importable in this environment")

_ALLOWED_FIELDS = {"host", "ip", "port", "product", "version", "os", "os_version", "service",
                   "fixed_version", "target", "title"}


def _rules():
    import posture_rules  # noqa: PLC0415 — on sys.path after _ensure_importable
    return posture_rules.RULES


def _categories():
    import port_intel  # noqa: PLC0415
    return set(port_intel.catalog_categories().values())


def test_every_posture_rule_has_a_recipe():
    missing = [r.rule_id for r in _rules() if r.rule_id not in recipes.RECIPES]
    assert missing == []


def test_every_exposed_category_has_a_recipe():
    missing = [c for c in _categories() if f"POSTURE-EXPOSED-{c.upper()}" not in recipes.RECIPES]
    assert missing == []


def test_verification_scanner_is_the_rules_scanner():
    for rule in _rules():
        assert recipes.RECIPES[rule.rule_id].verification.scanner in rule.scanners, rule.rule_id


@pytest.mark.parametrize("rid", sorted(recipes.RECIPES))
def test_recipe_is_well_formed(rid):
    r = recipes.RECIPES[rid]
    assert r.remediation_type in recipes.REMEDIATION_TYPES
    assert r.risk_response in recipes.RISK_RESPONSES
    assert any(s.tier == "fix" for s in r.steps)
    assert all(s.tier in recipes.TIERS for s in r.steps)
    assert all(s.risk in ("low", "medium", "high") for s in r.steps)
    assert r.verification.expected and r.verification.check
    assert r.compensating_controls


@pytest.mark.parametrize("rid", sorted(recipes.RECIPES))
def test_templates_use_only_known_fields(rid):
    r = recipes.RECIPES[rid]
    texts = [r.title, r.target_state, r.compensating_controls, r.verification.check,
             r.verification.expected, *r.verification.manual.values()]
    for s in r.steps:
        texts += [s.title, s.description, *s.pre_checks, s.rollback, s.downtime]
        for cmds in s.commands.values():
            texts += list(cmds)
    for t in texts:
        names = {f for _, f, _, _ in string.Formatter().parse(t) if f}
        assert names <= _ALLOWED_FIELDS, (rid, t, names - _ALLOWED_FIELDS)


def test_no_destructive_commands():
    guard = HallucinationGuard()
    for r in recipes.RECIPES.values():
        for s in r.steps:
            for cmds in s.commands.values():
                for c in cmds:
                    assert guard.validate_remediation_commands(c)["valid"], (r.recipe_id, c)


def _finding(evidence=None, cve_ids=None, title="t", description=""):
    return SimpleNamespace(evidence=evidence or {}, cve_ids=cve_ids or [], title=title,
                           description=description, remediation="", epss_score=None,
                           exploit_validated=False)


class TestResolution:
    def test_rule_id_wins(self):
        f = _finding({"rule_id": "POSTURE-SMB-V1-ENABLED"}, cve_ids=["CVE-2017-0144"])
        assert recipes.resolve_recipe(build_context(f), f).recipe_id == "POSTURE-SMB-V1-ENABLED"

    def test_exposed_category(self):
        f = _finding({"rule_id": "POSTURE-EXPOSED-UNKNOWNCAT", "evidence": {"category": "database"}})
        assert recipes.resolve_recipe(build_context(f), f).recipe_id == "POSTURE-EXPOSED-DATABASE"

    def test_cve_falls_to_patch(self):
        f = _finding(cve_ids=["CVE-2024-6387"])
        assert recipes.resolve_recipe(build_context(f), f).recipe_id == "CVE-PATCH"

    def test_legacy_keyword_mapping(self):
        f = _finding(title="SSLv3 supported (POODLE)")
        assert recipes.resolve_recipe(build_context(f), f).recipe_id == "POSTURE-TLS-DEPRECATED-VERSION"

    def test_generic_last(self):
        f = _finding(title="Interesting behaviour observed")
        assert recipes.resolve_recipe(build_context(f), f).recipe_id == "GENERIC"

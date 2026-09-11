"""
Default-credential CANDIDATE detection.

The biggest real-world IoT risk, and a verified gap: the engine flagged SNMP
default communities but nothing for cameras, NVRs, printers or switches.

The word CANDIDATE is the whole design. Vedha never attempts a login, so it can
never say "admin/12345 works here". What it CAN say, from evidence it already
holds, is: this device is from a vendor that ships documented defaults, and it is
exposing a login. That is an actionable finding on its own — "prove you changed
the default" — and it is honest about what was and wasn't tested. Confirmation is
a separate, RoE-gated active-validation step.

Two false-positive guards these tests pin down:
  * No login surface observed -> no finding, even for a known-defaults vendor.
    A camera with its web UI firewalled off is not the same risk.
  * Unknown vendor -> no finding. The catalog is an allowlist of vendors with
    PUBLISHED defaults, never a guess from a banner that merely looks device-ish.
"""
from __future__ import annotations

from default_creds_catalog import has_known_defaults


class TestCatalog:
    def test_known_vendor_has_defaults(self):
        hit = has_known_defaults("hikvision")
        assert hit is not None
        assert hit["default_login"]
        assert hit["reference"]

    def test_lookup_is_case_and_whitespace_insensitive(self):
        assert has_known_defaults("  HIKVISION ") == has_known_defaults("hikvision")

    def test_unknown_vendor_returns_none(self):
        assert has_known_defaults("acme-nonexistent") is None

    def test_none_and_empty_return_none(self):
        assert has_known_defaults(None) is None
        assert has_known_defaults("") is None


# ── the POSTURE-DEFAULT-CRED-CANDIDATE rule ──────────────────────────────────
from models import Fact, SourceConfidence          # noqa: E402
import posture_rules as P                          # noqa: E402


def _fact(data, scanner="web_scan", port=80, status="open", target="10.0.0.9"):
    """Same shape the other posture-rule tests use (tests/test_posture_rules.py)."""
    return Fact(scanner=scanner, target=target, timestamp="", port=port, proto="tcp",
                status=status, data=data, evidence="e", error=None,
                source_confidence=SourceConfidence.inferred,
                source_file="s.jsonl", source_line=1)


def _rule(rule_id):
    return next(r for r in P.RULES if r.rule_id == rule_id)


RULE_ID = "POSTURE-DEFAULT-CRED-CANDIDATE"


class TestRuleFires:
    def test_known_vendor_with_basic_auth(self):
        ev = _rule(RULE_ID).detect(_fact({
            "auth_surface": {"scheme": "basic", "realm": "Hikvision", "vendor": "hikvision"}}))
        assert ev is not None
        assert ev["default_login"] == "admin/12345"
        assert ev["vendor"] == "hikvision"
        assert ev["auth_scheme"] == "basic"

    def test_known_vendor_with_login_form(self):
        ev = _rule(RULE_ID).detect(_fact({
            "auth_surface": {"scheme": "form", "realm": None, "vendor": "dahua"}}))
        assert ev is not None and ev["vendor"] == "dahua"

    def test_evidence_explains_what_was_not_tested(self):
        """The finding must read as a candidate, not a confirmation."""
        ev = _rule(RULE_ID).detect(_fact({
            "auth_surface": {"scheme": "basic", "realm": "X", "vendor": "netgear"}}))
        assert "Confirm" in ev["detail"] or "confirm" in ev["detail"]

    def test_vendor_falls_back_to_the_fact_when_surface_lacks_one(self):
        """web_scan hints the vendor on the surface; other scanners may carry it
        at the top level instead."""
        ev = _rule(RULE_ID).detect(_fact({
            "vendor": "axis",
            "auth_surface": {"scheme": "basic", "realm": "AXIS", "vendor": None}}))
        assert ev is not None and ev["vendor"] == "axis"


class TestRuleStaysSilent:
    def test_no_auth_surface_at_all(self):
        """Evidence invariant — a vendor name alone proves nothing."""
        assert _rule(RULE_ID).detect(_fact({"vendor": "hikvision"})) is None

    def test_scheme_none_is_not_a_login_surface(self):
        """A camera whose web UI is firewalled off is not this risk."""
        assert _rule(RULE_ID).detect(_fact({
            "vendor": "hikvision",
            "auth_surface": {"scheme": "none", "realm": None, "vendor": None}})) is None

    def test_unknown_vendor_never_fires(self):
        assert _rule(RULE_ID).detect(_fact({
            "auth_surface": {"scheme": "basic", "realm": "AcmeCorp", "vendor": None}})) is None

    def test_malformed_auth_surface_is_survivable(self):
        assert _rule(RULE_ID).detect(_fact({"auth_surface": "not-a-dict"})) is None


class TestRuleMetadata:
    def test_is_registered(self):
        assert _rule(RULE_ID) is not None

    def test_declares_its_required_input(self):
        assert _rule(RULE_ID).requires == ("auth_surface",)

    def test_reads_the_scanners_that_emit_auth_surface(self):
        assert "web_scan" in _rule(RULE_ID).scanners

    def test_severity_and_attack_mapping(self):
        r = _rule(RULE_ID)
        assert r.severity == "high"
        assert r.category == "default_credentials"
        assert r.cwe and r.mitre

    def test_fp_notes_state_it_is_unconfirmed(self):
        """Future maintainers must not mistake this for a proven login."""
        notes = _rule(RULE_ID).fp_notes.lower()
        assert "candidate" in notes or "never attempts" in notes

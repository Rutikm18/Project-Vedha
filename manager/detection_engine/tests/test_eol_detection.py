"""
End-of-life / end-of-support OS detection.

An unsupported OS receives no security patches, so its vulnerability count only
grows and no amount of scanning will ever find a fix to apply. That makes EOL a
first-class posture finding, not a footnote — and it was a verified gap: nothing
in the engine flagged Windows 10 22H2 or Server 2012 as out of support.

Design constraint these tests enforce: the catalog matches a SPECIFIC release
string, never a fuzzy prefix. "Windows 11 24H2" (supported) must never be swept
up by a hypothetical "Windows 11" entry, and an OS absent from the catalog must
stay silent rather than guess. False positives here are expensive: telling a
customer to rebuild a supported fleet destroys trust faster than a missed finding.
"""
from __future__ import annotations

from eol_catalog import lookup_eol


class TestCatalogLookup:
    def test_windows_10_22h2_is_past_eol(self):
        hit = lookup_eol("Windows 10 22H2", "10.0.19045")
        assert hit is not None
        assert hit["product"] == "Windows 10 22H2"
        assert hit["eol_date"] == "2025-10-14"
        assert hit["days_past_eol"] > 0
        assert hit["source"]

    def test_supported_os_returns_none(self):
        assert lookup_eol("Windows 11 24H2", "10.0.26100") is None

    def test_unknown_os_returns_none(self):
        assert lookup_eol("SomeAppliance 1.0", None) is None

    def test_missing_os_release_returns_none(self):
        """Evidence invariant: no input, no verdict."""
        assert lookup_eol(None) is None
        assert lookup_eol("") is None

    def test_longest_match_wins(self):
        """'windows server 2012 r2' must not be shadowed by 'windows server 2012'."""
        hit = lookup_eol("Windows Server 2012 R2 Standard")
        assert hit is not None
        assert hit["eol_date"] == "2023-10-10"

    def test_match_is_case_insensitive(self):
        assert lookup_eol("WINDOWS 7 PROFESSIONAL") is not None

    def test_days_past_eol_is_positive_for_long_dead_os(self):
        """Windows 7 died in 2020; the number must be large and positive, not a
        signed artefact of date maths."""
        hit = lookup_eol("Windows 7")
        assert hit["days_past_eol"] > 2000


# ── the POSTURE-OS-END-OF-LIFE rule ──────────────────────────────────────────
from models import Fact, SourceConfidence          # noqa: E402
import posture_rules as P                          # noqa: E402


def _fact(data, scanner="os_fingerprint", port=None, status="open",
          target="192.168.1.77"):
    """Same shape the other posture-rule tests use (tests/test_posture_rules.py)."""
    return Fact(scanner=scanner, target=target, timestamp="", port=port, proto="tcp",
                status=status, data=data, evidence="e", error=None,
                source_confidence=SourceConfidence.inferred,
                source_file="s.jsonl", source_line=1)


def _rule(rule_id):
    return next(r for r in P.RULES if r.rule_id == rule_id)


class TestEolRule:
    RULE_ID = "POSTURE-OS-END-OF-LIFE"

    def test_rule_is_registered(self):
        assert _rule(self.RULE_ID) is not None

    def test_fires_on_past_eol_os(self):
        ev = _rule(self.RULE_ID).detect(
            _fact({"os_release": "Windows 10 22H2", "os_version": "10.0.19045"}))
        assert ev is not None
        assert ev["eol_date"] == "2025-10-14"
        assert ev["days_past_eol"] > 0
        assert "end-of-support" in ev["detail"]

    def test_silent_on_supported_os(self):
        assert _rule(self.RULE_ID).detect(
            _fact({"os_release": "Windows 11 24H2"})) is None

    def test_silent_without_os_release(self):
        """Evidence invariant: os_guess alone is not enough to claim EOL."""
        assert _rule(self.RULE_ID).detect(_fact({"os_guess": "Windows"})) is None

    def test_declares_its_required_input(self):
        """The `requires` contract makes a missing input report MISSING_INPUT
        (drift) instead of the rule silently looking clean."""
        assert _rule(self.RULE_ID).requires == ("os_release",)

    def test_reads_os_fingerprint_facts(self):
        assert "os_fingerprint" in _rule(self.RULE_ID).scanners

    def test_is_high_severity_with_attack_surface_mapping(self):
        r = _rule(self.RULE_ID)
        assert r.severity == "high"
        assert r.cwe and r.mitre and r.category == "eol_software"

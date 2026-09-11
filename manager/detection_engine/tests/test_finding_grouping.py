"""
Stable grouping keys for fleet-scale findings.

A flat network with 12 identical cameras produces 12 identical findings. Listed
individually they bury the three findings that actually matter, and an operator
reading the report learns nothing from rows 2-12 that row 1 didn't already say.

`group_key_for` gives the presentation layer a stable handle to collapse them
into one row with an asset count. Grouping is PRESENTATION ONLY — every per-asset
finding is still stored and still carries its own evidence, because the moment you
merge the underlying records you lose the ability to say "these 11 are fixed, that
one isn't". This only says what MAY be folded together.
"""
from __future__ import annotations

from posture_rules import group_key_for


class TestGroupKey:
    def test_identical_devices_share_a_key(self):
        a = group_key_for("POSTURE-DEFAULT-CRED-CANDIDATE", {"product": "Hikvision DS-2CD"})
        b = group_key_for("POSTURE-DEFAULT-CRED-CANDIDATE", {"product": "Hikvision DS-2CD"})
        assert a == b

    def test_different_products_do_not_group(self):
        a = group_key_for("POSTURE-DEFAULT-CRED-CANDIDATE", {"product": "Hikvision DS-2CD"})
        b = group_key_for("POSTURE-DEFAULT-CRED-CANDIDATE", {"product": "Axis M3045"})
        assert a != b

    def test_different_rules_do_not_group(self):
        """Same device, different weakness — must stay separate rows."""
        a = group_key_for("POSTURE-SMB-V1-ENABLED", {"product": "X"})
        b = group_key_for("POSTURE-SVC-RDP-EXPOSED", {"product": "X"})
        assert a != b

    def test_product_match_is_case_and_whitespace_insensitive(self):
        """Vendor strings arrive from banners with inconsistent casing/padding;
        cosmetic differences must not split a group."""
        a = group_key_for("R", {"product": "  Hikvision DS-2CD "})
        b = group_key_for("R", {"product": "hikvision ds-2cd"})
        assert a == b

    def test_falls_back_to_service_when_no_product(self):
        a = group_key_for("R", {"service": "rtsp"})
        b = group_key_for("R", {"service": "rtsp"})
        c = group_key_for("R", {"service": "http"})
        assert a == b and a != c

    def test_no_signature_still_groups_by_rule(self):
        """Coarser, but deterministic — never a crash and never a random key."""
        assert group_key_for("R", {}) == group_key_for("R", {})

    def test_missing_evidence_is_survivable(self):
        assert group_key_for("R", None) == group_key_for("R", {})

    def test_key_is_short_and_stable(self):
        k = group_key_for("R", {"product": "X"})
        assert isinstance(k, str) and len(k) == 16
        assert k == group_key_for("R", {"product": "X"})     # deterministic

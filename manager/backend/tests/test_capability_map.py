"""Tests for app/detection/capability_map.py (P2: finding → attacker capability)."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import pytest

from app.detection.capability_map import (
    SyntheticFinding,
    _COMPOUND_RELAY_ID,
    _RULES,
    derive_capabilities,
    list_rules,
)


# ── minimal Finding stand-in ──────────────────────────────────────────────────


@dataclass
class _F:
    """Minimal Finding-like object for testing."""
    id: str
    asset_id: str
    rule_id: str
    severity: str = "medium"
    status: str = "open"
    exploitable: bool = False
    exploit_validated: bool = False
    cvss_score: float = 5.0
    cvss_vector: None = None
    epss_score: float = 0.0
    mitre_techniques: list[str] = field(default_factory=list)
    verification_confidence: float = 70.0
    evidence: dict = field(default_factory=dict)


# ── rule table sanity ─────────────────────────────────────────────────────────


def test_all_rules_have_valid_probabilities():
    for rid, r in _RULES.items():
        assert 0 < r.base_p <= 1.0, f"{rid}: base_p out of range"
        assert 0 < r.confidence <= 100, f"{rid}: confidence out of range"


def test_all_rules_have_technique_id():
    for rid, r in _RULES.items():
        assert r.technique_id.startswith("T"), f"{rid}: technique_id missing"


def test_list_rules_includes_compound():
    rules = list_rules()
    ids = [r["rule_id"] for r in rules]
    assert _COMPOUND_RELAY_ID in ids
    assert "CORR-NTLM-RELAY-PATH" in ids
    assert "POSTURE-EXPOSED-BACKDOOR" in ids


# ── derive_capabilities basic cases ──────────────────────────────────────────


def test_empty_findings_returns_empty():
    assert derive_capabilities([]) == []


def test_unmapped_rule_id_skipped():
    f = _F(id="f1", asset_id="a1", rule_id="UNKNOWN-RULE")
    assert derive_capabilities([f]) == []


def test_known_rule_produces_synthetic_finding():
    f = _F(id="f1", asset_id="a1", rule_id="CORR-DB-UNAUTH-EXPOSED", severity="critical")
    out = derive_capabilities([f])
    assert len(out) == 1
    sf = out[0]
    assert isinstance(sf, SyntheticFinding)
    assert sf.exploitable is True
    assert sf.asset_id == "a1"
    assert sf.epss_score > 0
    assert "T1190" in sf.mitre_techniques
    assert sf.hop_type == "foothold"


def test_severity_critical_boosts_probability():
    f_medium = _F(id="f1", asset_id="a1", rule_id="CORR-NTLM-RELAY-PATH", severity="medium")
    f_critical = _F(id="f2", asset_id="a2", rule_id="CORR-NTLM-RELAY-PATH", severity="critical")
    out_m = derive_capabilities([f_medium])
    out_c = derive_capabilities([f_critical])
    assert out_c[0].epss_score >= out_m[0].epss_score


def test_mgmt_plane_ipmi_boosts_probability():
    f_plain = _F(id="f1", asset_id="a1", rule_id="CORR-MGMT-PLANE-EXPOSED",
                 evidence={})
    f_ipmi = _F(id="f2", asset_id="a2", rule_id="CORR-MGMT-PLANE-EXPOSED",
                evidence={"ipmi_cipher_zero": True})
    out_plain = derive_capabilities([f_plain])
    out_ipmi = derive_capabilities([f_ipmi])
    assert out_ipmi[0].epss_score > out_plain[0].epss_score


def test_deterministic_id_stable_across_calls():
    f = _F(id="f1", asset_id="a1", rule_id="CORR-LEGACY-WINDOWS-SURFACE")
    out1 = derive_capabilities([f])
    out2 = derive_capabilities([f])
    assert out1[0].id == out2[0].id


def test_multiple_findings_different_assets():
    findings = [
        _F(id="f1", asset_id="a1", rule_id="CORR-DB-UNAUTH-EXPOSED"),
        _F(id="f2", asset_id="a2", rule_id="POSTURE-EXPOSED-CONTAINER"),
        _F(id="f3", asset_id="a3", rule_id="UNKNOWN-RULE"),
    ]
    out = derive_capabilities(findings)
    assert len(out) == 2
    asset_ids = {sf.asset_id for sf in out}
    assert "a1" in asset_ids
    assert "a2" in asset_ids
    assert "a3" not in asset_ids


def test_posture_exposed_backdoor_foothold():
    f = _F(id="f1", asset_id="a1", rule_id="POSTURE-EXPOSED-BACKDOOR")
    out = derive_capabilities([f])
    assert len(out) == 1
    assert out[0].hop_type == "foothold"
    assert out[0].epss_score >= 0.85


def test_posture_exposed_container_foothold():
    f = _F(id="f1", asset_id="a1", rule_id="POSTURE-EXPOSED-CONTAINER")
    out = derive_capabilities([f])
    assert out[0].hop_type == "foothold"
    assert out[0].epss_score >= 0.85
    assert "T1610" in out[0].mitre_techniques


def test_cleartext_cluster_credential_access():
    f = _F(id="f1", asset_id="a1", rule_id="CORR-CLEARTEXT-CLUSTER")
    out = derive_capabilities([f])
    assert out[0].hop_type == "credential_access"


def test_ntlm_relay_lateral():
    f = _F(id="f1", asset_id="a1", rule_id="CORR-NTLM-RELAY-PATH")
    out = derive_capabilities([f])
    assert out[0].hop_type == "lateral"
    assert "T1557.001" in out[0].mitre_techniques


# ── compound rule: relay + coercion surface ───────────────────────────────────


def test_compound_relay_emitted_when_signing_off_and_epmap():
    findings = [
        _F(id="f1", asset_id="a1", rule_id="CORR-NTLM-RELAY-PATH"),
        _F(id="f2", asset_id="a1", rule_id="POSTURE-MSRPC-EPMAP-EXPOSED"),
    ]
    out = derive_capabilities(findings)
    rule_ids = {sf.capability_rule_id for sf in out}
    assert _COMPOUND_RELAY_ID in rule_ids
    # compound should have higher probability than bare relay
    bare = next(sf for sf in out if sf.capability_rule_id == "CORR-NTLM-RELAY-PATH")
    compound = next(sf for sf in out if sf.capability_rule_id == _COMPOUND_RELAY_ID)
    assert compound.epss_score > bare.epss_score


def test_compound_relay_not_emitted_without_coerce_surface():
    findings = [
        _F(id="f1", asset_id="a1", rule_id="CORR-NTLM-RELAY-PATH"),
    ]
    out = derive_capabilities(findings)
    rule_ids = {sf.capability_rule_id for sf in out}
    assert _COMPOUND_RELAY_ID not in rule_ids


def test_compound_relay_with_posture_signing_off():
    """POSTURE-SMB-SIGNING-OFF (not the CORR composite) also triggers compound."""
    findings = [
        _F(id="f1", asset_id="a1", rule_id="POSTURE-SMB-SIGNING-OFF"),
        _F(id="f2", asset_id="a1", rule_id="POSTURE-MSRPC-EPMAP-EXPOSED"),
    ]
    out = derive_capabilities(findings)
    rule_ids = {sf.capability_rule_id for sf in out}
    assert _COMPOUND_RELAY_ID in rule_ids


def test_compound_relay_only_on_matching_asset():
    """Compound relay must not bleed across assets."""
    findings = [
        _F(id="f1", asset_id="a1", rule_id="CORR-NTLM-RELAY-PATH"),   # relay on a1
        _F(id="f2", asset_id="a2", rule_id="POSTURE-MSRPC-EPMAP-EXPOSED"),  # coerce on a2
    ]
    out = derive_capabilities(findings)
    rule_ids_by_asset = {}
    for sf in out:
        rule_ids_by_asset.setdefault(str(sf.asset_id), set()).add(sf.capability_rule_id)
    # a1 has relay but no coerce → no compound
    assert _COMPOUND_RELAY_ID not in rule_ids_by_asset.get("a1", set())
    # a2 has coerce but no relay → no compound
    assert _COMPOUND_RELAY_ID not in rule_ids_by_asset.get("a2", set())


# ── all_findings extension test ───────────────────────────────────────────────


def test_status_is_open():
    f = _F(id="f1", asset_id="a1", rule_id="CORR-DB-UNAUTH-EXPOSED")
    out = derive_capabilities([f])
    assert out[0].status == "open"


def test_cvss_score_reasonable():
    for rule_id in list(_RULES):
        f = _F(id="f1", asset_id="a1", rule_id=rule_id)
        out = derive_capabilities([f])
        assert 0 <= out[0].cvss_score <= 10, f"CVSS out of range for {rule_id}"

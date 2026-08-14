"""
test_attack_path_correlation.py — manager-native composite correlation over
probe facts (app/detection/attack_paths.py).

Covers B1 (the three ported composites on the production path), B2 (device-role
amplification), and B3 (exposed-DB+unauth, default-SNMP-on-infra). Fact shapes
mirror what the probe scanners actually emit.
"""
from __future__ import annotations

from app.detection.attack_paths import attack_path_findings
from app.models.enums import FindingSeverity


def _ids(findings):
    return {f["rule_id"] for f in findings}


def _get(findings, rule_id):
    return next(f for f in findings if f["rule_id"] == rule_id)


# ── B1: NTLM relay ───────────────────────────────────────────────────────────
def test_ntlm_relay_medium_when_only_signing_not_required():
    fs = attack_path_findings([
        {"scanner": "smb_scan", "target": "t", "port": 445, "status": "open",
         "data": {"smbv1_enabled": False, "signing_required": False}},
    ])
    hit = _get(fs, "CORR-NTLM-RELAY-PATH")
    assert hit["severity"] == FindingSeverity.medium
    assert hit["evidence"]["correlated"] == ["SMB-SIGNING-NOT-REQUIRED"]


def test_ntlm_relay_high_when_smbv1_also_enabled():
    fs = attack_path_findings([
        {"scanner": "smb_scan", "target": "t", "port": 445, "status": "open",
         "data": {"smbv1_enabled": True, "signing_required": False}},
    ])
    assert _get(fs, "CORR-NTLM-RELAY-PATH")["severity"] == FindingSeverity.high


def test_no_relay_when_signing_required():
    fs = attack_path_findings([
        {"scanner": "smb_scan", "target": "t", "port": 445, "status": "open",
         "data": {"smbv1_enabled": True, "signing_required": True}},
    ])
    assert "CORR-NTLM-RELAY-PATH" not in _ids(fs)


# ── B2: device-role amplification ────────────────────────────────────────────
def test_ntlm_relay_on_domain_controller_is_critical():
    facts = [
        {"scanner": "smb_scan", "target": "10.0.0.5", "port": 445, "status": "open",
         "data": {"smbv1_enabled": True, "signing_required": False}},
    ]
    roles = {"10.0.0.5": {"device_role": "server", "role_detail": "domain_controller"}}
    hit = _get(attack_path_findings(facts, roles), "CORR-NTLM-RELAY-PATH")
    assert hit["severity"] == FindingSeverity.critical
    assert hit["evidence"]["domain_controller"] is True


def test_device_role_from_facts_also_amplifies():
    # role arrives in the SAME result (device_classify fact), not just persisted.
    facts = [
        {"scanner": "smb_scan", "target": "10.0.0.6", "port": 445, "status": "open",
         "data": {"smbv1_enabled": False, "signing_required": False}},
        {"scanner": "device_classify", "target": "10.0.0.6", "status": "observed",
         "data": {"device_type": "server", "role_detail": "domain_controller"}},
    ]
    assert _get(attack_path_findings(facts), "CORR-NTLM-RELAY-PATH")["severity"] == FindingSeverity.critical


# ── B1: legacy Windows + cleartext cluster ───────────────────────────────────
def test_legacy_windows_smbv1_plus_rdp():
    fs = attack_path_findings([
        {"scanner": "smb_scan", "target": "t", "port": 445, "status": "open", "data": {"smbv1_enabled": True}},
        {"scanner": "port_scan", "target": "t", "port": 3389, "proto": "tcp", "status": "open"},
    ])
    assert _get(fs, "CORR-LEGACY-WINDOWS-SURFACE")["severity"] == FindingSeverity.high


def test_cleartext_cluster_needs_two():
    two = attack_path_findings([
        {"scanner": "port_scan", "target": "t", "port": 23, "proto": "tcp", "status": "open"},
        {"scanner": "port_scan", "target": "t", "port": 21, "proto": "tcp", "status": "open"},
    ])
    assert _get(two, "CORR-CLEARTEXT-CLUSTER")["severity"] == FindingSeverity.medium
    one = attack_path_findings([
        {"scanner": "port_scan", "target": "t", "port": 23, "proto": "tcp", "status": "open"},
    ])
    assert "CORR-CLEARTEXT-CLUSTER" not in _ids(one)


# ── B3: new composites ───────────────────────────────────────────────────────
def test_exposed_db_with_unauth_is_critical():
    fs = attack_path_findings([
        {"scanner": "port_scan", "target": "t", "port": 27017, "proto": "tcp", "status": "open"},
        {"scanner": "db_scan", "target": "t", "port": 27017, "status": "open",
         "data": {"unauthenticated": True, "product": "MongoDB"}},
    ])
    hit = _get(fs, "CORR-DB-UNAUTH-EXPOSED")
    assert hit["severity"] == FindingSeverity.critical
    assert 27017 in hit["evidence"]["db_ports"]


def test_exposed_db_without_unauth_does_not_fire():
    fs = attack_path_findings([
        {"scanner": "port_scan", "target": "t", "port": 3306, "proto": "tcp", "status": "open"},
    ])
    assert "CORR-DB-UNAUTH-EXPOSED" not in _ids(fs)


def test_snmp_default_community_on_network_device_is_high():
    facts = [
        {"scanner": "snmp_scan", "target": "t", "port": 161, "proto": "udp", "status": "open",
         "data": {"community": "public"}},
    ]
    roles = {"t": {"device_role": "network_device", "role_detail": None}}
    assert _get(attack_path_findings(facts, roles), "CORR-SNMP-PUBLIC-LATERAL")["severity"] == FindingSeverity.high


def test_snmp_default_community_without_network_role_is_medium():
    fs = attack_path_findings([
        {"scanner": "snmp_scan", "target": "t", "port": 161, "status": "open",
         "data": {"default_community": True}},
    ])
    assert _get(fs, "CORR-SNMP-PUBLIC-LATERAL")["severity"] == FindingSeverity.medium


# ── correlation hygiene ──────────────────────────────────────────────────────
def test_correlation_is_host_scoped():
    fs = attack_path_findings([
        {"scanner": "port_scan", "target": "hostA", "port": 23, "proto": "tcp", "status": "open"},
        {"scanner": "port_scan", "target": "hostB", "port": 21, "proto": "tcp", "status": "open"},
    ])
    assert "CORR-CLEARTEXT-CLUSTER" not in _ids(fs)   # telnet on A, ftp on B


def test_every_composite_cites_and_tags():
    facts = [
        {"scanner": "smb_scan", "target": "t", "port": 445, "status": "open",
         "data": {"smbv1_enabled": True, "signing_required": False}},
        {"scanner": "port_scan", "target": "t", "port": 3389, "proto": "tcp", "status": "open"},
    ]
    findings = attack_path_findings(facts)
    assert findings  # at least relay + legacy-windows
    for f in findings:
        assert f["evidence"].get("correlated")
        assert f["mitre_techniques"]
        assert f["rule_id"].startswith("CORR-")


def test_results_are_sorted_most_severe_first():
    facts = [
        {"scanner": "smb_scan", "target": "t", "port": 445, "status": "open",
         "data": {"smbv1_enabled": True, "signing_required": False}},
        {"scanner": "port_scan", "target": "t", "port": 3389, "proto": "tcp", "status": "open"},
        {"scanner": "port_scan", "target": "t", "port": 23, "proto": "tcp", "status": "open"},
        {"scanner": "port_scan", "target": "t", "port": 21, "proto": "tcp", "status": "open"},
    ]
    sev = [f["severity"] for f in attack_path_findings(facts)]
    order = [FindingSeverity.critical, FindingSeverity.high, FindingSeverity.medium,
             FindingSeverity.low, FindingSeverity.info]
    assert sev == sorted(sev, key=order.index)

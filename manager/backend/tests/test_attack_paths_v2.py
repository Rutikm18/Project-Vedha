"""
test_attack_paths_v2.py — P5 composites (AD exposure, exposed management plane)
and the ATT&CK tactic/technique roll-up (attack_matrix.build_attack_matrix).
"""
from __future__ import annotations

from app.detection.attack_matrix import TECHNIQUES, build_attack_matrix
from app.detection.attack_paths import attack_path_findings
from app.models.enums import FindingSeverity


def _ids(findings):
    return {f["rule_id"] for f in findings}


def _get(findings, rule_id):
    return next(f for f in findings if f["rule_id"] == rule_id)


# ── CORR-AD-EXPOSURE ──────────────────────────────────────────────────────────
def test_ad_exposure_fires_on_anon_ldap_plus_smb():
    facts = [
        {"scanner": "ldap_scan", "target": "10.0.0.5", "port": 389, "status": "open",
         "data": {"ldap": True, "anonymous_search_allowed": True}},
        {"scanner": "smb_scan", "target": "10.0.0.5", "port": 445, "status": "open",
         "data": {"smbv1_enabled": False, "signing_required": True}},
    ]
    hit = _get(attack_path_findings(facts), "CORR-AD-EXPOSURE")
    assert hit["severity"] == FindingSeverity.high        # search = content disclosure
    assert hit["evidence"]["ldap_search"] is True


def test_ad_exposure_critical_on_domain_controller():
    facts = [
        {"scanner": "ldap_scan", "target": "10.0.0.5", "port": 389, "status": "open",
         "data": {"ldap": True, "anonymous_bind": True}},
        {"scanner": "smb_scan", "target": "10.0.0.5", "port": 445, "status": "open",
         "data": {"smbv1_enabled": False, "signing_required": True}},
    ]
    roles = {"10.0.0.5": {"device_role": "server", "role_detail": "domain_controller"}}
    hit = _get(attack_path_findings(facts, roles), "CORR-AD-EXPOSURE")
    assert hit["severity"] == FindingSeverity.critical
    assert hit["evidence"]["domain_controller"] is True


def test_no_ad_exposure_without_ldap_anon():
    facts = [
        {"scanner": "ldap_scan", "target": "10.0.0.5", "port": 389, "status": "open",
         "data": {"ldap": True, "anonymous_bind": False}},
        {"scanner": "smb_scan", "target": "10.0.0.5", "port": 445, "status": "open",
         "data": {"signing_required": True}},
    ]
    assert "CORR-AD-EXPOSURE" not in _ids(attack_path_findings(facts))


# ── CORR-MGMT-PLANE-EXPOSED ───────────────────────────────────────────────────
def test_mgmt_plane_critical_on_ipmi_cipher_zero():
    facts = [
        {"scanner": "ipmi_scan", "target": "10.0.0.6", "port": 623, "proto": "udp",
         "status": "open", "data": {"ipmi": True, "cipher_zero": True}},
    ]
    hit = _get(attack_path_findings(facts), "CORR-MGMT-PLANE-EXPOSED")
    assert hit["severity"] == FindingSeverity.critical
    assert hit["evidence"]["ipmi_cipher_zero"] is True


def test_mgmt_plane_high_on_winrm_plus_rdp():
    facts = [
        {"scanner": "port_scan", "target": "10.0.0.7", "port": 5985, "status": "open", "data": {}},
        {"scanner": "port_scan", "target": "10.0.0.7", "port": 3389, "status": "open", "data": {}},
    ]
    hit = _get(attack_path_findings(facts), "CORR-MGMT-PLANE-EXPOSED")
    assert hit["severity"] == FindingSeverity.high
    assert hit["evidence"]["winrm"] and hit["evidence"]["rdp"]


def test_no_mgmt_plane_on_rdp_alone():
    facts = [{"scanner": "port_scan", "target": "10.0.0.7", "port": 3389, "status": "open", "data": {}}]
    assert "CORR-MGMT-PLANE-EXPOSED" not in _ids(attack_path_findings(facts))


# ── ATT&CK matrix roll-up ─────────────────────────────────────────────────────
def test_matrix_groups_by_tactic_in_killchain_order():
    findings = [
        {"finding_id": "a", "rule_id": "POSTURE-SMB-V1-ENABLED", "asset_ip": "1.1.1.1",
         "severity": "critical", "title": "SMBv1", "mitre": "T1210"},          # Lateral Movement
        {"finding_id": "b", "rule_id": "POSTURE-AV-OFF", "asset_ip": "1.1.1.1",
         "severity": "high", "title": "AV off", "mitre": "T1562.001"},         # Defense Evasion
        {"rule_id": "CORR-AD-EXPOSURE", "target": "1.1.1.1", "severity": "critical",
         "title": "AD", "mitre_techniques": ["T1087.002", "T1557.001"]},       # Discovery + Cred Access
    ]
    m = build_attack_matrix(findings)
    tactics = [t["tactic"] for t in m["tactics"]]
    # kill-chain order: Defense Evasion before Credential Access before Discovery before Lateral Movement
    assert tactics == ["Defense Evasion", "Credential Access", "Discovery", "Lateral Movement"]
    assert m["counts"]["findings_mapped"] == 3
    assert set(m["techniques_seen"]) == {"T1210", "T1562.001", "T1087.002", "T1557.001"}
    assert m["unmapped_techniques"] == []


def test_matrix_keeps_unknown_technique_in_unmapped_bucket():
    m = build_attack_matrix([{"rule_id": "X", "mitre": "T9999"}])
    assert m["unmapped_techniques"] == ["T9999"]
    assert m["tactics"][-1]["tactic"] == "Unmapped"


def test_matrix_ignores_findings_without_techniques():
    m = build_attack_matrix([{"rule_id": "CVE-ONLY", "severity": "high"}])
    assert m["counts"]["findings_mapped"] == 0 and m["tactics"] == []


def test_every_emitted_technique_is_mapped():
    """Guard: every technique any rule emits must be in the curated table, so the
    matrix never silently drops a real finding into 'Unmapped'."""
    import re
    import pathlib
    root = pathlib.Path(__file__).resolve().parents[2]
    srcs = [
        root / "detection_engine" / "posture_rules.py",
        root / "detection_engine" / "host_posture.py",
        root / "detection_engine" / "fingerprint_intel.py",
        root / "detection_engine" / "port_intel.py",
        root / "backend" / "app" / "detection" / "attack_paths.py",
    ]
    emitted: set[str] = set()
    for p in srcs:
        if p.exists():
            emitted |= set(re.findall(r"T\d{4}(?:\.\d{3})?", p.read_text()))
    missing = emitted - set(TECHNIQUES)
    assert not missing, f"techniques emitted by rules but absent from attack_matrix.TECHNIQUES: {sorted(missing)}"

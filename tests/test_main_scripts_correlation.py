"""
test_main_scripts_correlation.py — Epic 2: correlation findings.

Composite, high-signal findings derived from the base findings on the SAME host
(NTLM relay path, legacy-Windows surface, cleartext cluster). Pure over facts;
every composite must cite the base findings it came from.
"""
from __future__ import annotations

from main_scripts import findings as F


def _run(*facts):
    return F.run_findings(list(facts))


def _ids(findings):
    return {f.rule_id for f in findings}


def _get(findings, rule_id):
    return next(f for f in findings if f.rule_id == rule_id)


# ── NTLM relay path ──────────────────────────────────────────────────────────
def test_ntlm_relay_is_medium_when_only_signing_not_required():
    fs = _run({"scanner": "smb_scan", "target": "t", "port": 445, "status": "open",
               "data": {"smbv1_enabled": False, "signing_required": False, "signing_supported": True}})
    hit = _get(fs, "CORR-NTLM-RELAY-PATH")
    assert hit.severity == F.SEV_MEDIUM
    assert hit.data["correlated_findings"] == ["SMB-SIGNING-NOT-REQUIRED"]


def test_ntlm_relay_is_high_when_smbv1_also_enabled():
    fs = _run({"scanner": "smb_scan", "target": "t", "port": 445, "status": "open",
               "data": {"smbv1_enabled": True, "signing_required": False, "signing_supported": True}})
    hit = _get(fs, "CORR-NTLM-RELAY-PATH")
    assert hit.severity == F.SEV_HIGH and hit.data["smbv1"] is True
    assert set(hit.data["correlated_findings"]) == {"SMB-SIGNING-NOT-REQUIRED", "SMB-V1-ENABLED"}


def test_no_relay_finding_when_signing_required():
    fs = _run({"scanner": "smb_scan", "target": "t", "port": 445, "status": "open",
               "data": {"smbv1_enabled": False, "signing_required": True, "signing_supported": True}})
    assert "CORR-NTLM-RELAY-PATH" not in _ids(fs)


# ── legacy Windows surface ───────────────────────────────────────────────────
def test_legacy_windows_surface_smbv1_plus_rdp():
    fs = _run(
        {"scanner": "smb_scan", "target": "t", "port": 445, "status": "open",
         "data": {"smbv1_enabled": True}},
        {"scanner": "port_scan", "target": "t", "port": 3389, "proto": "tcp", "status": "open"},
    )
    hit = _get(fs, "CORR-LEGACY-WINDOWS-SURFACE")
    assert hit.severity == F.SEV_HIGH
    assert hit.data["correlated_findings"] == ["SMB-V1-ENABLED", "SVC-RDP-EXPOSED"]


def test_no_legacy_surface_with_only_smbv1():
    fs = _run({"scanner": "smb_scan", "target": "t", "port": 445, "status": "open",
               "data": {"smbv1_enabled": True}})
    assert "CORR-LEGACY-WINDOWS-SURFACE" not in _ids(fs)


# ── cleartext cluster ────────────────────────────────────────────────────────
def test_cleartext_cluster_fires_on_two_cleartext_services():
    fs = _run(
        {"scanner": "port_scan", "target": "t", "port": 23, "proto": "tcp", "status": "open"},
        {"scanner": "port_scan", "target": "t", "port": 21, "proto": "tcp", "status": "open"},
    )
    hit = _get(fs, "CORR-CLEARTEXT-CLUSTER")
    assert hit.severity == F.SEV_MEDIUM
    assert set(hit.data["correlated_findings"]) == {"SVC-TELNET-CLEARTEXT", "SVC-FTP-CLEARTEXT"}


def test_single_cleartext_service_does_not_cluster():
    fs = _run({"scanner": "port_scan", "target": "t", "port": 23, "proto": "tcp", "status": "open"})
    assert "CORR-CLEARTEXT-CLUSTER" not in _ids(fs)


# ── correlation is host-scoped + evidence-backed ─────────────────────────────
def test_correlation_does_not_cross_hosts():
    fs = _run(
        {"scanner": "port_scan", "target": "hostA", "port": 23, "proto": "tcp", "status": "open"},
        {"scanner": "port_scan", "target": "hostB", "port": 21, "proto": "tcp", "status": "open"},
    )
    assert "CORR-CLEARTEXT-CLUSTER" not in _ids(fs)   # telnet on A, ftp on B — no cluster


def test_correlations_are_evidence_backed():
    fs = _run({"scanner": "smb_scan", "target": "t", "port": 445, "status": "open",
               "data": {"smbv1_enabled": True, "signing_required": False, "signing_supported": True}})
    for f in fs:
        if f.rule_id.startswith("CORR-"):
            assert f.data.get("correlated_findings") and f.evidence
            assert "correlated:" in f.evidence.lower()

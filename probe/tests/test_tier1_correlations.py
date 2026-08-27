"""
test_tier1_correlations.py — enterprise attack-path correlations built from the
Tier-1 capabilities (anonymous data exposure, user enumeration, console exposure).
"""

from __future__ import annotations

from scanner import findings

T = "10.0.0.30"


def _run(facts):
    return {f.rule_id: f for f in findings.run_findings(facts)}


def test_anon_data_exposure_cluster():
    facts = [
        {"scanner": "nfs_scan", "target": T, "port": 2049, "status": "open",
         "data": {"nfs": True, "world_readable_exports": ["/home"], "export_count": 1}},
        {"scanner": "ftp_scan", "target": T, "port": 21, "status": "open",
         "data": {"anonymous_login": True, "anon_read": True, "file_sample": ["x"]}},
    ]
    by = _run(facts)
    assert "CORR-ANON-DATA-EXPOSURE" in by and by["CORR-ANON-DATA-EXPOSURE"].severity == "high"
    used = by["CORR-ANON-DATA-EXPOSURE"].data["correlated_findings"]
    assert "NFS-EXPORT-WORLD-READABLE" in used and "FTP-ANON-ACCESS" in used


def test_single_anon_finding_does_not_correlate():
    facts = [{"scanner": "ftp_scan", "target": T, "port": 21, "status": "open",
              "data": {"anonymous_login": True, "anon_read": True}}]
    assert "CORR-ANON-DATA-EXPOSURE" not in _run(facts)


def test_user_enum_plus_weak_auth():
    facts = [
        {"scanner": "smb_enum_scan", "target": T, "port": 445, "status": "open",
         "data": {"null_session": True, "users": [{"name": "a", "rid": 500}],
                  "user_count": 1, "shares": []}},
        {"scanner": "vnc_scan", "target": T, "port": 5900, "status": "open",
         "data": {"vnc": True, "no_auth": True, "security_types": [{"name": "None"}]}},
    ]
    by = _run(facts)
    assert "CORR-USER-ENUM-PLUS-WEAK-AUTH" in by
    assert by["CORR-USER-ENUM-PLUS-WEAK-AUTH"].severity == "high"


def test_mgmt_plane_exposed_on_cipher_zero_alone():
    facts = [{"scanner": "ipmi_scan", "target": T, "port": 623, "status": "open",
              "data": {"ipmi": True, "cipher_zero": True}}]
    by = _run(facts)
    assert "CORR-MGMT-PLANE-EXPOSED" in by and by["CORR-MGMT-PLANE-EXPOSED"].severity == "high"


def test_mgmt_plane_needs_two_when_no_cipher_zero():
    # A single low IPMI-EXPOSED without a second mgmt finding should not correlate.
    facts = [{"scanner": "ipmi_scan", "target": T, "port": 623, "status": "open",
              "data": {"ipmi": True, "cipher_zero": False, "rmcp_status": 1}}]
    assert "CORR-MGMT-PLANE-EXPOSED" not in _run(facts)

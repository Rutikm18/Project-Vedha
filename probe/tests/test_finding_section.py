"""
test_finding_section.py — the scanner-module trust view + the finding section.

Two product surfaces:
  * scanner_registry — which scanners are VERIFIED (authoritative) vs experimental.
  * findings.summarize — the finding section: the ACTUAL ranked vulnerabilities,
    each tagged with its source scanner and whether that source is verified, shown
    only when found (honest — nothing invented on a clean host).
"""
from __future__ import annotations

from main_scripts import scanner_registry as R
from main_scripts.findings import run_findings, summarize


# ── scanner registry (which scripts are verified) ─────────────────────────────
class TestScannerRegistry:
    def test_user_validated_scanners_are_verified(self):
        for s in ("host_discovery", "port_scan", "syn_scan", "os_fingerprint",
                  "smb_scan", "rdp_scan", "tls_scan", "msrpc_scan",
                  "rpc_reconcile", "udp_scan"):
            assert R.is_verified(s), s

    def test_unvalidated_scanners_are_not_verified(self):
        for s in ("web_scan", "ssh_scan", "snmp_scan", "smb_enum_scan"):
            assert not R.is_verified(s)

    def test_unknown_scanner_is_not_trusted(self):
        assert R.is_verified("totally_made_up") is False
        assert R.is_verified(None) is False

    def test_verification_report_shape(self):
        rep = R.verification_report()
        assert rep["verified_count"] == len(R.VERIFIED)
        assert {e["name"] for e in rep["verified"]} == set(R.VERIFIED)
        assert all("display" in e and "summary" in e for e in rep["verified"])

    def test_registry_aligns_with_manager_validated_set(self):
        # The probe's VERIFIED and the manager's VALIDATED_SCANNERS must agree on the
        # core sensors — probe decides trust, manager confirms only from those.
        core = {"smb_scan", "rdp_scan", "tls_scan", "msrpc_scan", "udp_scan",
                "port_scan", "host_discovery", "rpc_reconcile", "os_fingerprint"}
        assert core <= R.VERIFIED


# ── finding section (show vulnerabilities, if found) ──────────────────────────
class TestFindingSection:
    def _sum(self, facts):
        return summarize(run_findings(facts))

    def test_clean_host_shows_no_findings_honestly(self):
        # A fully hardened SMB host with nothing wrong → empty finding list, not a
        # fabricated one.
        s = self._sum([{"scanner": "smb_scan", "target": "t", "port": 445,
                        "status": "open",
                        "data": {"smbv1_enabled": False, "smb2_supported": True,
                                 "signing_required": True, "negotiated_dialect": "0x0311"}}])
        assert s["has_findings"] is False and s["findings"] == []
        assert s["total"] == 0

    def test_vulnerable_host_shows_ranked_vulnerabilities(self):
        s = self._sum([
            {"scanner": "smb_scan", "target": "t", "port": 445, "status": "open",
             "data": {"smbv1_enabled": True, "smb2_supported": True, "signing_required": False}},
            {"scanner": "rdp_scan", "target": "t", "port": 3389, "status": "open",
             "data": {"rdp_confirmed": True, "nla": False, "tls": False,
                      "standard_rdp_security": True, "nla_required": False, "selected_protocol": 0}},
        ])
        assert s["has_findings"] is True and s["total"] >= 2
        ids = {r["rule_id"] for r in s["findings"]}
        assert "SMB-V1-ENABLED" in ids and "SVC-RDP-NO-NLA" in ids
        # each row carries the vulnerability detail the report needs to SHOW
        row = next(r for r in s["findings"] if r["rule_id"] == "SMB-V1-ENABLED")
        assert row["evidence"] and row["recommendation"] and row["target"] == "t"

    def test_findings_are_ranked_worst_first(self):
        s = self._sum([
            {"scanner": "smb_scan", "target": "t", "port": 445, "status": "open",
             "data": {"smbv1_enabled": True}},                       # high
            {"scanner": "msrpc_scan", "target": "t", "port": 135, "status": "open",
             "data": {"msrpc": True, "endpoint_count": 5, "interface_count": 3}},  # low
        ])
        ranks = [r["severity"] for r in s["findings"]]
        # highest severity appears before the lowest
        from main_scripts.findings import _SEV_RANK
        assert _SEV_RANK[ranks[0]] >= _SEV_RANK[ranks[-1]]

    def test_each_finding_tagged_with_verified_provenance(self):
        s = self._sum([{"scanner": "smb_scan", "target": "t", "port": 445, "status": "open",
                        "data": {"smbv1_enabled": True}}])
        row = s["findings"][0]
        assert row["source_scanner"] == "smb_scan" and row["verified"] is True
        assert s["verified_count"] >= 1

    def test_backward_compatible_keys_kept(self):
        s = self._sum([{"scanner": "smb_scan", "target": "t", "port": 445, "status": "open",
                        "data": {"smbv1_enabled": True}}])
        for k in ("total", "by_severity", "by_category", "actionable"):
            assert k in s

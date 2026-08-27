"""
test_smb_ldap_scanners.py — SMB null-session + LDAP anonymous-bind enumeration.

Like the SSH audit tests, the live impacket/ldap3 network path can't run portably
in CI (it needs a real Samba/AD lab), so these cover:
  * the pure, bounded logic that keeps the scanners safe (RID-range parsing,
    user de-duplication)
  * the ScanResult shaping, via a monkeypatched probe (no network)
  * the findings verdicts (SMB null session / user disclosure; LDAP anon bind /
    anon directory read) and their secure-case silence
  * parity across the scanner/ and main_scripts/ trees (the product path)
"""

from __future__ import annotations

import asyncio

from scanner import smb_enum_scanner as smbe
from scanner import ldap_scanner as ldp
from scanner import findings
from scanner.scanner_base import ScopeGuard


# ── SMB: bounded pure logic (the safety-critical parts) ───────────────────────

class TestRidRanges:
    def test_parses_enum4linux_default(self):
        r = smbe.parse_rid_ranges("500-550,1000-1050")
        assert r[0] == 500 and 550 in r and 1000 in r and r[-1] == 1050
        assert len(r) == 102

    def test_single_and_bad_tokens(self):
        assert smbe.parse_rid_ranges("500") == [500]
        assert smbe.parse_rid_ranges("junk, 5, 7-7") == [5, 7]

    def test_reversed_range_tolerated(self):
        assert smbe.parse_rid_ranges("550-500") == list(range(500, 551))

    def test_is_bounded_no_brute_sweep(self):
        # A pasted huge range must never become a brute-force sweep.
        assert len(smbe.parse_rid_ranges("0-100000000")) <= smbe.MAX_RIDS


class TestMergeUsers:
    def test_dedup_samr_wins(self):
        merged = smbe._merge_users(
            [{"name": "Administrator", "rid": 500, "source": "rid_cycle"}],
            [{"name": "Administrator", "rid": 500, "source": "samr"},
             {"name": "svc", "rid": 1001, "source": "samr"}])
        assert len(merged) == 2
        admin = [u for u in merged if u["rid"] == 500][0]
        assert admin["source"] == "samr"

    def test_decode_strips_nul(self):
        assert smbe._decode(b"WORKGROUP\x00") == "WORKGROUP"


# ── SMB scanner (network isolated via a patched _enumerate) ────────────────────

class TestSMBEnumScanner:
    def _sc(self):
        return smbe.SMBEnumScanner(ScopeGuard.from_list(["10.0.0.0/8"]),
                                   rate=1e9, concurrency=2, timeout=0.1, ports=[445])

    def test_null_session_open_with_shares_and_users(self):
        sc = self._sc()
        sc._enumerate = lambda target, port: {
            "smb": True, "null_session": True, "guest_session": False,
            "server_os": "Windows Server 2019", "server_domain": "CORP",
            "shares": [{"name": "IPC$"}, {"name": "HR"}], "share_count": 2,
            "users": [{"name": "Administrator", "rid": 500}], "user_count": 1}
        r = asyncio.run(sc.scan_target("10.0.0.9"))[0]
        assert r.status == "open" and r.port == 445
        assert r.data["null_session"] is True and r.data["user_count"] == 1

    def test_null_refused_is_open_but_secure(self):
        # SMB present but null session refused: the scanner reports it as OPEN
        # (SMB reachable) with null_session=False — an informative, secure result
        # the finding layer stays silent on. Only "no SMB at all" is filtered.
        sc = self._sc()
        sc._enumerate = lambda target, port: {"smb": True, "null_session": False,
                                              "reason": "null_refused"}
        r = asyncio.run(sc.scan_target("10.0.0.9"))[0]
        assert r.status == "open" and r.data["null_session"] is False

    def test_no_smb_is_filtered(self):
        sc = self._sc()
        sc._enumerate = lambda target, port: {"smb": False, "reason": "no_smb"}
        r = asyncio.run(sc.scan_target("10.0.0.9"))[0]
        assert r.status == "filtered"

    def test_impacket_missing_is_error(self):
        sc = self._sc()
        sc._enumerate = lambda target, port: {"smb": None, "error": "impacket_not_installed"}
        r = asyncio.run(sc.scan_target("10.0.0.9"))[0]
        assert r.status == "error" and "impacket" in (r.error or "")


# ── LDAP scanner (network isolated via a patched _probe) ───────────────────────

class TestLDAPScanner:
    def _sc(self):
        return ldp.LDAPScanner(ScopeGuard.from_list(["10.0.0.0/8"]),
                               rate=1e9, concurrency=2, timeout=0.1, ports=[389])

    def test_anonymous_bind_open(self):
        sc = self._sc()
        sc._probe = lambda target, port: {
            "ldap": True, "ssl": False, "anonymous_bind": True,
            "naming_contexts": ["DC=corp,DC=local"], "dns_host_name": "dc01.corp.local",
            "anonymous_search_allowed": True, "sample_entry_count": 20}
        r = asyncio.run(sc.scan_target("10.0.0.9"))[0]
        assert r.status == "open" and r.data["anonymous_bind"] is True

    def test_anon_refused_is_filtered(self):
        sc = self._sc()
        sc._probe = lambda target, port: {"ldap": True, "anonymous_bind": False,
                                          "reason": "anon_bind_refused"}
        # anonymous_bind False but ldap True -> still "open" (LDAP present), the
        # finding layer decides nothing fires. Verify it is at least not an error.
        r = asyncio.run(sc.scan_target("10.0.0.9"))[0]
        assert r.status == "open" and r.data["anonymous_bind"] is False

    def test_no_ldap_is_filtered(self):
        sc = self._sc()
        sc._probe = lambda target, port: {"ldap": False, "reason": "no_ldap"}
        r = asyncio.run(sc.scan_target("10.0.0.9"))[0]
        assert r.status == "filtered"


# ── findings ──────────────────────────────────────────────────────────────────

class TestSMBLDAPFindings:
    def test_smb_null_session_and_users(self):
        fact = {"scanner": "smb_enum_scan", "target": "10.0.0.5", "port": 445,
                "status": "open",
                "data": {"null_session": True, "guest_session": False,
                         "server_os": "Windows Server 2019", "server_domain": "CORP",
                         "shares": [{"name": "IPC$"}, {"name": "HR_Files"}], "share_count": 2,
                         "users": [{"name": "Administrator", "rid": 500},
                                   {"name": "svc_sql", "rid": 1103}], "user_count": 2}}
        by = {f.rule_id: f for f in findings.run_findings([fact])}
        assert "SMB-NULL-SESSION" in by and by["SMB-NULL-SESSION"].severity == "medium"
        assert "SMB-NULL-SESSION-USERS" in by and by["SMB-NULL-SESSION-USERS"].severity == "high"
        # non-default share surfaced in the null-session finding
        assert "HR_Files" in by["SMB-NULL-SESSION"].data["nondefault_shares"]

    def test_smb_secure_is_silent(self):
        fact = {"scanner": "smb_enum_scan", "target": "10.0.0.5", "port": 445,
                "status": "open", "data": {"null_session": False}}
        assert not any(f.rule_id.startswith("SMB-NULL") for f in findings.run_findings([fact]))

    def test_ldap_anon_bind_and_search(self):
        fact = {"scanner": "ldap_scan", "target": "10.0.0.6", "port": 389,
                "status": "open",
                "data": {"anonymous_bind": True, "naming_contexts": ["DC=corp,DC=local"],
                         "dns_host_name": "dc01.corp.local",
                         "anonymous_search_allowed": True, "sample_entry_count": 20}}
        by = {f.rule_id: f for f in findings.run_findings([fact])}
        assert "LDAP-ANON-BIND" in by and by["LDAP-ANON-BIND"].severity == "low"
        assert "LDAP-ANON-SEARCH" in by and by["LDAP-ANON-SEARCH"].severity == "high"

    def test_ldap_anon_bind_only_no_search(self):
        fact = {"scanner": "ldap_scan", "target": "10.0.0.6", "port": 389,
                "status": "open",
                "data": {"anonymous_bind": True, "naming_contexts": ["DC=corp,DC=local"],
                         "anonymous_search_allowed": False}}
        ids = {f.rule_id for f in findings.run_findings([fact])}
        assert "LDAP-ANON-BIND" in ids and "LDAP-ANON-SEARCH" not in ids

    def test_ldap_secure_is_silent(self):
        fact = {"scanner": "ldap_scan", "target": "10.0.0.6", "port": 389,
                "status": "open", "data": {"anonymous_bind": False}}
        assert not any(f.rule_id.startswith("LDAP-") for f in findings.run_findings([fact]))


# ── parity: wired into the product tree (main_scripts) ─────────────────────────

class TestMainScriptsParity:
    def test_scanners_import_in_both_trees(self):
        from main_scripts.smb_enum_scanner import SMBEnumScanner, parse_rid_ranges
        from main_scripts.ldap_scanner import LDAPScanner
        assert parse_rid_ranges("500-501") == [500, 501]
        assert SMBEnumScanner and LDAPScanner

    def test_main_scripts_findings_derive_smb_and_ldap(self):
        from main_scripts import findings as mf
        smb = {"scanner": "smb_enum_scan", "target": "10.0.0.5", "port": 445,
               "status": "open", "data": {"null_session": True,
                                          "users": [{"name": "a", "rid": 500}], "user_count": 1,
                                          "shares": [], "share_count": 0}}
        ldap = {"scanner": "ldap_scan", "target": "10.0.0.6", "port": 389, "status": "open",
                "data": {"anonymous_bind": True, "anonymous_search_allowed": True,
                         "sample_entry_count": 5, "naming_contexts": ["DC=x"]}}
        ids = {f.rule_id for f in mf.run_findings([smb, ldap])}
        assert {"SMB-NULL-SESSION", "SMB-NULL-SESSION-USERS",
                "LDAP-ANON-BIND", "LDAP-ANON-SEARCH"} <= ids

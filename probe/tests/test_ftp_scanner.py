"""
test_ftp_scanner.py — FTP anonymous-access check.

Pure control-protocol logic + ScanResult shaping via a monkeypatched probe +
findings + parity. (A real control+PASV socket path is exercised separately by the
scratchpad ground-truth; the codebase keeps socket tests out of CI.)
"""

from __future__ import annotations

import asyncio

from scanner import ftp_scanner as ftp
from scanner import findings
from scanner.scanner_base import ScopeGuard


class TestPureLogic:
    def test_parse_pasv(self):
        assert ftp.parse_pasv("227 Entering Passive Mode (192,168,1,1,195,80)") == 50000
        assert ftp.parse_pasv("227 nothing") is None

    def test_banner_software(self):
        assert ftp.banner_software("220 (vsFTPd 3.0.3)") == "(vsFTPd 3.0.3)"
        assert ftp.banner_software("220-FileZilla Server") == "FileZilla Server"


class TestFTPScanner:
    def _sc(self):
        return ftp.FTPScanner(ScopeGuard.from_list(["10.0.0.0/8"]),
                              rate=1e9, concurrency=2, timeout=0.1, ports=[21])

    def test_anon_login_and_read_open(self):
        sc = self._sc()
        sc._probe = lambda t, p: {"ftp": True, "banner": "220 (vsFTPd 3.0.3)",
                                  "software": "(vsFTPd 3.0.3)", "anonymous_login": True,
                                  "anon_read": True, "file_sample": ["pub", "secret.txt"]}
        r = asyncio.run(sc.scan_target("10.0.0.9"))[0]
        assert r.status == "open" and r.data["anonymous_login"] is True

    def test_no_ftp_filtered(self):
        sc = self._sc()
        sc._probe = lambda t, p: {"ftp": None, "reason": "no_ftp"}
        assert asyncio.run(sc.scan_target("10.0.0.9"))[0].status == "filtered"

    def test_ftp_present_anon_denied_open_but_secure(self):
        sc = self._sc()
        sc._probe = lambda t, p: {"ftp": True, "banner": "220 x", "anonymous_login": False}
        r = asyncio.run(sc.scan_target("10.0.0.9"))[0]
        assert r.status == "open" and r.data["anonymous_login"] is False


class TestFTPFindings:
    def _fact(self, **data):
        return {"scanner": "ftp_scan", "target": "10.0.0.3", "port": 21,
                "status": "open", "data": data}

    def test_anon_read_is_high(self):
        by = {f.rule_id: f for f in findings.run_findings([self._fact(
            anonymous_login=True, anon_read=True, software="vsftpd",
            file_sample=["pub", "backup.zip"])])}
        assert by["FTP-ANON-ACCESS"].severity == "high"
        assert "backup.zip" in by["FTP-ANON-ACCESS"].data["file_sample"]

    def test_anon_login_only_is_medium(self):
        by = {f.rule_id: f for f in findings.run_findings([self._fact(
            anonymous_login=True, anon_read=False)])}
        assert by["FTP-ANON-ACCESS"].severity == "medium"

    def test_anon_denied_is_silent(self):
        out = findings.run_findings([self._fact(anonymous_login=False)])
        assert not any(f.rule_id == "FTP-ANON-ACCESS" for f in out)


class TestParity:
    def test_main_scripts(self):
        from main_scripts.ftp_scanner import FTPScanner, parse_pasv
        from main_scripts import findings as mf
        assert parse_pasv("227 (10,0,0,1,4,1)") == 1025
        ids = {f.rule_id for f in mf.run_findings([{
            "scanner": "ftp_scan", "target": "10.0.0.3", "port": 21, "status": "open",
            "data": {"anonymous_login": True, "anon_read": True, "file_sample": ["x"]}}])}
        assert "FTP-ANON-ACCESS" in ids
        assert FTPScanner

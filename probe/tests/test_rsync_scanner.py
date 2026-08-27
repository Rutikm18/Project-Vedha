"""
test_rsync_scanner.py — rsync daemon anonymous-module exposure.

Pure protocol parsing + ScanResult shaping via a monkeypatched probe + findings +
parity. (The daemon handshake over a real socket is simple; kept out of CI per the
codebase convention.)
"""

from __future__ import annotations

import asyncio

from scanner import rsync_scanner as rs
from scanner import findings
from scanner.scanner_base import ScopeGuard


class TestParseModules:
    def test_tab_and_space_separated(self):
        data = "@RSYNCD: 31.0\nbackup\tNightly backups\npublic         Public files\n@RSYNCD: EXIT\n"
        m = rs.parse_modules(data)
        assert [x["name"] for x in m] == ["backup", "public"]
        assert m[0]["comment"] == "Nightly backups" and m[1]["comment"] == "Public files"

    def test_protocol_lines_ignored(self):
        assert rs.parse_modules("@RSYNCD: 31.0\n@RSYNCD: EXIT\n") == []
        assert rs.parse_modules("@ERROR: unknown\n") == []

    def test_bounded(self):
        big = "\n".join(f"mod{i}\tc{i}" for i in range(500))
        assert len(rs.parse_modules(big)) <= rs.MAX_MODULES


class TestRsyncScanner:
    def _sc(self):
        return rs.RsyncScanner(ScopeGuard.from_list(["10.0.0.0/8"]),
                               rate=1e9, concurrency=2, timeout=0.1, ports=[873])

    def test_anon_modules_open(self):
        sc = self._sc()
        sc._probe = lambda t, p: {"rsync": True, "version": "31.0", "module_count": 2,
                                  "modules": [{"name": "backup", "anonymous": True},
                                              {"name": "secure", "anonymous": False}],
                                  "anon_modules": ["backup"]}
        r = asyncio.run(sc.scan_target("10.0.0.9"))[0]
        assert r.status == "open" and r.data["anon_modules"] == ["backup"]

    def test_no_rsync_filtered(self):
        sc = self._sc()
        sc._probe = lambda t, p: {"rsync": None, "reason": "no_rsync"}
        assert asyncio.run(sc.scan_target("10.0.0.9"))[0].status == "filtered"


class TestRsyncFindings:
    def _fact(self, **data):
        return {"scanner": "rsync_scan", "target": "10.0.0.8", "port": 873,
                "status": "open", "data": {"rsync": True, **data}}

    def test_anon_modules_high(self):
        by = {f.rule_id: f for f in findings.run_findings([self._fact(
            modules=[{"name": "backup"}], anon_modules=["backup"])])}
        assert by["RSYNC-ANON-MODULES"].severity == "high"

    def test_auth_only_is_low_disclosure(self):
        by = {f.rule_id: f for f in findings.run_findings([self._fact(
            modules=[{"name": "backup"}, {"name": "secure"}], anon_modules=[])])}
        assert "RSYNC-ANON-MODULES" not in by
        assert by["RSYNC-DAEMON-EXPOSED"].severity == "low"

    def test_no_modules_silent(self):
        out = findings.run_findings([self._fact(modules=[], anon_modules=[])])
        assert not any(f.rule_id.startswith("RSYNC-") for f in out)


class TestParity:
    def test_main_scripts(self):
        from main_scripts.rsync_scanner import RsyncScanner, parse_modules
        from main_scripts import findings as mf
        assert parse_modules("data\tshared\n")[0]["name"] == "data"
        ids = {f.rule_id for f in mf.run_findings([{
            "scanner": "rsync_scan", "target": "10.0.0.8", "port": 873, "status": "open",
            "data": {"rsync": True, "modules": [{"name": "x"}], "anon_modules": ["x"]}}])}
        assert "RSYNC-ANON-MODULES" in ids
        assert RsyncScanner

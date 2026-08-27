"""
test_vnc_scanner.py — VNC/RFB authentication exposure.

Pure RFB parsing/classification + ScanResult shaping via a monkeypatched probe +
findings + parity. (The real RFB handshake is exercised by the scratchpad
ground-truth; socket tests are kept out of CI per the codebase convention.)
"""

from __future__ import annotations

import asyncio

from scanner import vnc_scanner as vnc
from scanner import findings
from scanner.scanner_base import ScopeGuard


class TestPureLogic:
    def test_parse_version(self):
        assert vnc.parse_rfb_version("RFB 003.008") == (3, 8)
        assert vnc.parse_rfb_version(b"RFB 003.003\n") == (3, 3)
        assert vnc.parse_rfb_version("RFB 004.001") == (4, 1)
        assert vnc.parse_rfb_version("not rfb") is None

    def test_classify(self):
        none = vnc.classify_security_types([1, 2])
        assert none["no_auth"] and none["weak_auth"] and not none["has_strong_auth"]
        strong = vnc.classify_security_types([2, 18])
        assert strong["weak_auth"] and strong["has_strong_auth"] and not strong["no_auth"]
        assert [t["name"] for t in strong["security_types"]] == ["VNC", "TLS"]


class TestVNCScanner:
    def _sc(self):
        return vnc.VNCScanner(ScopeGuard.from_list(["10.0.0.0/8"]),
                              rate=1e9, concurrency=2, timeout=0.1, ports=[5900])

    def test_no_auth_open(self):
        sc = self._sc()
        sc._probe = lambda t, p: {"vnc": True, "protocol_version": "3.8",
                                  "security_types": [{"id": 1, "name": "None"}],
                                  "no_auth": True, "weak_auth": False, "has_strong_auth": False}
        r = asyncio.run(sc.scan_target("10.0.0.9"))[0]
        assert r.status == "open" and r.data["no_auth"] is True

    def test_no_vnc_filtered(self):
        sc = self._sc()
        sc._probe = lambda t, p: {"vnc": None, "reason": "no_vnc"}
        assert asyncio.run(sc.scan_target("10.0.0.9"))[0].status == "filtered"


class TestVNCFindings:
    def _fact(self, **d):
        return {"scanner": "vnc_scan", "target": "10.0.0.4", "port": 5900,
                "status": "open", "data": {"vnc": True, **d}}

    def test_no_auth_is_critical(self):
        by = {f.rule_id: f for f in findings.run_findings([self._fact(
            no_auth=True, weak_auth=True, has_strong_auth=False,
            security_types=[{"name": "None"}])])}
        assert by["VNC-NO-AUTH"].severity == "critical"

    def test_weak_only_is_medium(self):
        by = {f.rule_id: f for f in findings.run_findings([self._fact(
            no_auth=False, weak_auth=True, has_strong_auth=False,
            security_types=[{"name": "VNC"}])])}
        assert "VNC-NO-AUTH" not in by and by["VNC-WEAK-AUTH"].severity == "medium"

    def test_strong_auth_silent(self):
        out = findings.run_findings([self._fact(
            no_auth=False, weak_auth=True, has_strong_auth=True,
            security_types=[{"name": "VNC"}, {"name": "TLS"}])])
        assert not any(f.rule_id.startswith("VNC-") for f in out)


class TestParity:
    def test_main_scripts(self):
        from main_scripts.vnc_scanner import VNCScanner, parse_rfb_version
        from main_scripts import findings as mf
        assert parse_rfb_version("RFB 003.008") == (3, 8)
        ids = {f.rule_id for f in mf.run_findings([{
            "scanner": "vnc_scan", "target": "10.0.0.4", "port": 5900, "status": "open",
            "data": {"vnc": True, "no_auth": True, "security_types": [{"name": "None"}]}}])}
        assert "VNC-NO-AUTH" in ids
        assert VNCScanner

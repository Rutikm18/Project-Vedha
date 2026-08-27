"""
test_msrpc_scanner.py — MSRPC endpoint-mapper (EPM) enumeration.

Pure summary logic + ScanResult shaping via a monkeypatched probe + findings +
parity. The live impacket EPM path needs a real Windows host (a lab follow-up);
like the SMB/LDAP scanners, the network path is monkeypatched here.
"""

from __future__ import annotations

import asyncio

from scanner import msrpc_scanner as msrpc
from scanner import findings
from scanner.scanner_base import ScopeGuard


class TestSummarize:
    def test_distinct_interfaces_and_named(self):
        eps = [{"uuid": "aaaa v1.0", "exe": "schedsvc.dll"},
               {"uuid": "aaaa v1.0", "exe": "schedsvc.dll"},
               {"uuid": "bbbb v0.0", "exe": ""}]
        s = msrpc._summarize(eps)
        assert s["interface_count"] == 2 and s["named_services"] == ["schedsvc.dll"]


class TestMSRPCScanner:
    def _sc(self):
        return msrpc.MSRPCScanner(ScopeGuard.from_list(["10.0.0.0/8"]),
                                  rate=1e9, concurrency=2, timeout=0.1, ports=[135])

    def test_open(self):
        sc = self._sc()
        sc._enumerate = lambda t, p: {"msrpc": True, "endpoint_count": 42,
                                      "interface_count": 18,
                                      "endpoints": [], "named_services": ["spoolss"]}
        r = asyncio.run(sc.scan_target("10.0.0.9"))[0]
        assert r.status == "open" and r.data["interface_count"] == 18

    def test_no_msrpc_filtered(self):
        sc = self._sc()
        sc._enumerate = lambda t, p: {"msrpc": None, "reason": "no_msrpc"}
        assert asyncio.run(sc.scan_target("10.0.0.9"))[0].status == "filtered"

    def test_impacket_missing_is_error(self):
        sc = self._sc()
        sc._enumerate = lambda t, p: {"msrpc": None, "error": "impacket_not_installed"}
        r = asyncio.run(sc.scan_target("10.0.0.9"))[0]
        assert r.status == "error" and "impacket" in (r.error or "")


class TestMSRPCFindings:
    def _fact(self, **d):
        return {"scanner": "msrpc_scan", "target": "10.0.0.12", "port": 135,
                "status": "open", "data": {"msrpc": True, **d}}

    def test_endpoints_low(self):
        by = {f.rule_id: f for f in findings.run_findings([self._fact(
            endpoint_count=42, interface_count=18, named_services=["schedsvc.dll"])])}
        assert by["MSRPC-ENDPOINTS-EXPOSED"].severity == "low"
        assert by["MSRPC-ENDPOINTS-EXPOSED"].data["interface_count"] == 18

    def test_zero_endpoints_silent(self):
        out = findings.run_findings([self._fact(endpoint_count=0)])
        assert not any(f.rule_id.startswith("MSRPC-") for f in out)


class TestParity:
    def test_main_scripts(self):
        from main_scripts.msrpc_scanner import MSRPCScanner, _summarize
        from main_scripts import findings as mf
        assert _summarize([{"uuid": "x v1", "exe": "a"}])["interface_count"] == 1
        ids = {f.rule_id for f in mf.run_findings([{
            "scanner": "msrpc_scan", "target": "10.0.0.12", "port": 135, "status": "open",
            "data": {"msrpc": True, "endpoint_count": 5, "interface_count": 3}}])}
        assert "MSRPC-ENDPOINTS-EXPOSED" in ids
        assert MSRPCScanner

"""
test_ipmi_scanner.py — IPMI 2.0 cipher-zero auth-bypass detection.

Byte-exact RMCP+ packet build/parse (the safety-critical wire logic) + ScanResult
shaping via a monkeypatched probe + findings + parity. No network in CI.
"""

from __future__ import annotations

import asyncio
import struct

from scanner import ipmi_scanner as ipmi
from scanner import findings
from scanner.scanner_base import ScopeGuard


def _resp(status: int) -> bytes:
    return (bytes([0x06, 0x00, 0xFF, 0x07]) + bytes([0x06, 0x11]) + b"\x00" * 8
            + struct.pack("<H", 36) + bytes([0x00, status]) + b"\x00" * 16)


class TestWireFormat:
    def test_open_session_request_offers_cipher_zero(self):
        req = ipmi.build_open_session_request()
        assert req[:4] == bytes([0x06, 0x00, 0xFF, 0x07])   # RMCP header
        assert req[4] == 0x06 and req[5] == 0x10            # RMCP+ Open Session Request
        assert len(req) == 48
        assert req[28] == 0x00                              # authentication algorithm = 0

    def test_parse_status_zero_is_cipher_zero(self):
        p = ipmi.parse_open_session_response(_resp(0x00))
        assert p["open_session_response"] and p["cipher_zero"] is True and p["rmcp_status"] == 0

    def test_parse_nonzero_status_is_safe(self):
        p = ipmi.parse_open_session_response(_resp(0x01))
        assert p["cipher_zero"] is False and p["rmcp_status"] == 1

    def test_parse_rejects_non_response(self):
        assert ipmi.parse_open_session_response(b"\x06\x00\xff\x07\x06\x10junk") is None
        assert ipmi.parse_open_session_response(b"") is None


class TestIPMIScanner:
    def _sc(self):
        return ipmi.IPMIScanner(ScopeGuard.from_list(["10.0.0.0/8"]),
                                rate=1e9, concurrency=2, timeout=0.1, ports=[623])

    def test_cipher_zero_open(self):
        sc = self._sc()
        sc._probe = lambda t, p: {"ipmi": True, "open_session_response": True,
                                  "rmcp_status": 0, "cipher_zero": True}
        r = asyncio.run(sc.scan_target("10.0.0.9"))[0]
        assert r.status == "open" and r.data["cipher_zero"] is True and r.proto == "udp"

    def test_no_ipmi_filtered(self):
        sc = self._sc()
        sc._probe = lambda t, p: {"ipmi": None, "reason": "no_ipmi"}
        assert asyncio.run(sc.scan_target("10.0.0.9"))[0].status == "filtered"


class TestIPMIFindings:
    def _fact(self, **d):
        return {"scanner": "ipmi_scan", "target": "10.0.0.10", "port": 623,
                "status": "open", "data": {"ipmi": True, **d}}

    def test_cipher_zero_is_critical(self):
        by = {f.rule_id: f for f in findings.run_findings([self._fact(cipher_zero=True, rmcp_status=0)])}
        assert by["IPMI-CIPHER-ZERO"].severity == "critical" and by["IPMI-CIPHER-ZERO"].proto == "udp"

    def test_reachable_bmc_is_low(self):
        by = {f.rule_id: f for f in findings.run_findings([self._fact(cipher_zero=False, rmcp_status=1)])}
        assert "IPMI-CIPHER-ZERO" not in by and by["IPMI-EXPOSED"].severity == "low"


class TestParity:
    def test_main_scripts(self):
        from main_scripts.ipmi_scanner import IPMIScanner, build_open_session_request
        from main_scripts import findings as mf
        assert len(build_open_session_request()) == 48
        ids = {f.rule_id for f in mf.run_findings([{
            "scanner": "ipmi_scan", "target": "10.0.0.10", "port": 623, "status": "open",
            "data": {"ipmi": True, "cipher_zero": True}}])}
        assert "IPMI-CIPHER-ZERO" in ids
        assert IPMIScanner

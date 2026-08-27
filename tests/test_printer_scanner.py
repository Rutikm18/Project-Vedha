"""
test_printer_scanner.py — network printer exposure (9100 PJL / 631 IPP).

Pure PJL/IPP parsing + ScanResult shaping via a monkeypatched probe + findings +
parity. (The real 9100 socket path is exercised by the scratchpad ground-truth.)
"""

from __future__ import annotations

import asyncio
import struct

from scanner import printer_scanner as pr
from scanner import findings
from scanner.scanner_base import ScopeGuard


class TestPureLogic:
    def test_parse_pjl_id(self):
        assert pr.parse_pjl_id(b'@PJL INFO ID\r\n"HP LaserJet 4250"\r\n\x1b%-12345X') == "HP LaserJet 4250"
        assert pr.parse_pjl_id(b"garbage") == ""

    def test_build_ipp(self):
        req = pr.build_ipp_get_printer_attributes("ipp://10.0.0.1:631/ipp/print")
        assert req[:4] == struct.pack(">HH", 0x0101, 0x000B) and req[-1] == 0x03

    def test_parse_ipp_make_model(self):
        name, val = b"printer-make-and-model", b"HP Color LaserJet"
        body = b"\x02\x00\x00\x00\x00\x00\x00\x01\x04" + b"\x47" + \
            struct.pack(">H", len(name)) + name + struct.pack(">H", len(val)) + val
        assert pr.parse_ipp_make_model(body) == "HP Color LaserJet"


class TestPrinterScanner:
    def _sc(self):
        return pr.PrinterScanner(ScopeGuard.from_list(["10.0.0.0/8"]),
                                 rate=1e9, concurrency=2, timeout=0.1, ports=[9100])

    def test_open(self):
        sc = self._sc()
        sc._probe = lambda t, p: {"printer": True, "protocol": "raw-9100",
                                  "model": "HP LaserJet M602"}
        r = asyncio.run(sc.scan_target("10.0.0.9"))[0]
        assert r.status == "open" and r.data["model"] == "HP LaserJet M602"

    def test_no_printer_filtered(self):
        sc = self._sc()
        sc._probe = lambda t, p: {"printer": None, "reason": "no_printer"}
        assert asyncio.run(sc.scan_target("10.0.0.9"))[0].status == "filtered"


class TestPrinterFindings:
    def test_exposed_low(self):
        by = {f.rule_id: f for f in findings.run_findings([{
            "scanner": "printer_scan", "target": "10.0.0.20", "port": 9100, "status": "open",
            "data": {"printer": True, "protocol": "raw-9100", "model": "HP LaserJet M602"}}])}
        assert by["PRINTER-EXPOSED"].severity == "low"
        assert by["PRINTER-EXPOSED"].data["model"] == "HP LaserJet M602"


class TestParity:
    def test_main_scripts(self):
        from main_scripts.printer_scanner import PrinterScanner, parse_pjl_id
        from main_scripts import findings as mf
        assert parse_pjl_id(b'@PJL INFO ID\r\n"X"\r\n') == "X"
        ids = {f.rule_id for f in mf.run_findings([{
            "scanner": "printer_scan", "target": "10.0.0.20", "port": 631, "status": "open",
            "data": {"printer": True, "protocol": "ipp-631", "model": ""}}])}
        assert "PRINTER-EXPOSED" in ids
        assert PrinterScanner

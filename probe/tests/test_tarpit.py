"""
test_tarpit.py — tarpit / honeypot detection (task C5).

A tarpit (LaBrea), honeypot, or ACK-everything middlebox answers on an implausible
fraction of ports; each "open" is a phantom service that would flood a report with
false positives. assess_tarpit() flags it, and the port scanner surfaces the flag
in its scan_summary. These cover the pure heuristic plus the end-to-end wiring.
"""
from __future__ import annotations

import asyncio

from scanner.scanner_base import assess_tarpit, ScopeGuard
from scanner.port_scanner import PortScanner


class TestAssessTarpit:
    def test_nearly_all_open_large_scan_is_flagged(self):
        r = assess_tarpit(open_count=98, attempted_count=100)
        assert r["likely_tarpit"] is True
        assert r["open_ratio"] == 0.98

    def test_busy_real_host_is_not_flagged(self):
        # 80 real services out of a full 65k scan: high absolute, tiny ratio.
        r = assess_tarpit(open_count=80, attempted_count=65535)
        assert r["likely_tarpit"] is False

    def test_tiny_all_open_scan_is_below_the_floor(self):
        # 2-of-2 open is 100% ratio but nowhere near the absolute floor.
        r = assess_tarpit(open_count=2, attempted_count=2)
        assert r["likely_tarpit"] is False

    def test_boundary_floor_and_ratio_trip_exactly(self):
        r = assess_tarpit(open_count=50, attempted_count=100)   # floor=50, ratio=0.5
        assert r["likely_tarpit"] is True

    def test_zero_attempted_is_safe(self):
        r = assess_tarpit(open_count=0, attempted_count=0)
        assert r["likely_tarpit"] is False and r["open_ratio"] == 0.0


class TestPortScannerTarpitFlag:
    def _scanner(self, ports):
        return PortScanner(ScopeGuard.from_list(["127.0.0.0/8"]),
                           ports=ports, rate=1e9, concurrency=16,
                           adaptive_timeout=False)

    def _summary(self, results):
        return next(r for r in results if r.status == "scan_summary")

    def test_all_open_host_flagged_as_tarpit(self):
        ports = list(range(1, 121))                 # 120 ports, all "open"
        sc = self._scanner(ports)

        async def all_open(target, port, est=None):
            return sc._build(target, port, "open", "connect_success", "forced open")

        sc._scan_port = all_open
        summ = self._summary(asyncio.run(sc.scan_target("127.0.0.1")))
        assert summ.data["tarpit"]["likely_tarpit"] is True
        assert "TARPIT" in summ.evidence

    def test_mostly_closed_host_not_flagged(self):
        ports = list(range(1, 121))
        sc = self._scanner(ports)

        async def one_open(target, port, est=None):
            status = "open" if port == 22 else "closed"
            return sc._build(target, port, status, "reason", "e")

        sc._scan_port = one_open
        summ = self._summary(asyncio.run(sc.scan_target("127.0.0.1")))
        assert summ.data["tarpit"]["likely_tarpit"] is False
        assert "TARPIT" not in summ.evidence

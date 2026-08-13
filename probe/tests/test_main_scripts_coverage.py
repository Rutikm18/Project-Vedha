"""
test_main_scripts_coverage.py — P0 coverage + self-health capabilities added to
probe/main_scripts/port_scanner.py:

  * named scan profiles: quick / top100 / top1000 / full / custom  (item #1)
  * bounded worker-pool scan_target — no 65,535-task fan-out, each port scanned
    exactly once, concurrency bounded by the pool                  (items #2, #6)
  * ScanMetrics — completeness invariant + local-resource health   (item #9)

Pure logic + mocked _attempt; no live network.
"""
from __future__ import annotations

import asyncio
from collections import Counter

import pytest

from main_scripts.port_scanner import PortScanner, resolve_profile
from main_scripts.scanner_base import ScopeGuard, ScanResult


def _scope() -> ScopeGuard:
    return ScopeGuard.from_list(["127.0.0.0/8"])


def _mk_scanner(ports, concurrency=8, **kw) -> PortScanner:
    # rate=1e9 removes the limiter as a test bottleneck; report_closed=True so
    # every state is emitted for inspection.
    kw.setdefault("report_closed", True)
    return PortScanner(_scope(), ports=ports, concurrency=concurrency,
                       rate=1e9, **kw)


def _summary(results):
    return next(r for r in results if r.status == "scan_summary").data


# ── Profiles (item #1) ────────────────────────────────────────────────────────

class TestProfiles:
    def test_full_is_entire_tcp_space(self):
        full = resolve_profile("full")
        assert full[0] == 1
        assert full[-1] == 65535
        assert len(full) == 65535
        assert len(set(full)) == 65535        # unique

    def test_top100_is_100_unique(self):
        top = resolve_profile("top100")
        assert len(top) == 100 == len(set(top))
        assert 3389 in top and 445 in top

    def test_quick_is_small_and_contains_smb(self):
        q = resolve_profile("quick")
        assert 445 in q and len(q) < 30

    def test_top1000_covers_windows_ground_truth_extras(self):
        t = resolve_profile("top1000")
        assert len(t) >= 1000
        for p in (2179, 7680, 5040, 47001, 49664, 445, 3389):
            assert p in t, f"top1000 missing high-value port {p}"

    def test_custom_dedups_and_requires_ports(self):
        assert resolve_profile("custom", [80, 443, 80]) == [80, 443]
        with pytest.raises(ValueError):
            resolve_profile("custom", None)

    def test_unknown_profile_raises(self):
        with pytest.raises(ValueError):
            resolve_profile("banana")


# ── Bounded worker pool + completeness metrics (items #2, #6, #9) ──────────────

def _closed(sc, target, port):
    return ScanResult(sc.name, target, port=port, proto="tcp",
                      status="closed", data={"reason": "connection_refused"})


class TestWorkerPoolAndMetrics:
    def test_every_port_scanned_exactly_once(self):
        ports = list(range(1000, 1500))
        sc = _mk_scanner(ports)
        seen: Counter = Counter()

        async def fake_attempt(target, port):
            seen[port] += 1
            return _closed(sc, target, port)

        sc._attempt = fake_attempt
        results = asyncio.run(sc.scan_target("127.0.0.1"))

        assert set(seen) == set(ports)
        assert all(v == 1 for v in seen.values())          # exactly once, no drops
        d = _summary(results)
        assert d["ports_requested"] == 500
        assert d["ports_attempted"] == 500
        assert d["classified"] == 500
        assert d["closed"] == 500
        assert d["complete"] is True

    def test_all_65535_ports_scheduled_exactly_once(self):
        ports = resolve_profile("full")
        sc = _mk_scanner(ports, concurrency=200)
        seen: Counter = Counter()

        async def fake_attempt(target, port):
            seen[port] += 1
            return _closed(sc, target, port)

        sc._attempt = fake_attempt
        asyncio.run(sc.scan_target("127.0.0.1"))
        assert len(seen) == 65535
        assert all(v == 1 for v in seen.values())

    def test_concurrency_is_bounded_by_the_pool(self):
        # Neutralise the semaphore so ONLY the worker pool can bound concurrency.
        ports = list(range(1, 61))
        sc = _mk_scanner(ports, concurrency=4)
        sc.sem = asyncio.Semaphore(10_000)
        inflight = peak = 0

        async def fake_attempt(target, port):
            nonlocal inflight, peak
            inflight += 1
            peak = max(peak, inflight)
            await asyncio.sleep(0.003)
            inflight -= 1
            return _closed(sc, target, port)

        sc._attempt = fake_attempt
        asyncio.run(sc.scan_target("127.0.0.1"))
        assert peak <= 4, f"worker pool did not bound concurrency: peak={peak}"

    def test_metrics_counts_every_state(self):
        ports = [1, 2, 3, 4, 5]
        sc = _mk_scanner(ports, concurrency=5)
        states = {1: "open", 2: "closed", 3: "filtered", 4: "unreachable", 5: "error"}

        async def fake_attempt(target, port):
            return ScanResult(sc.name, target, port=port, proto="tcp",
                              status=states[port], data={"reason": "x"})

        sc._attempt = fake_attempt
        d = _summary(asyncio.run(sc.scan_target("127.0.0.1")))
        assert (d["open"], d["closed"], d["filtered"], d["unreachable"], d["error"]) == (1, 1, 1, 1, 1)
        assert d["classified"] == 5 and d["complete"] is True

    def test_local_resource_error_marks_scan_degraded(self):
        ports = [1, 2]
        sc = _mk_scanner(ports, concurrency=2)

        async def fake_attempt(target, port):
            if port == 1:
                return ScanResult(sc.name, target, port=port, proto="tcp",
                                  status="error", data={"reason": "local_resource_error"})
            return _closed(sc, target, port)

        sc._attempt = fake_attempt
        d = _summary(asyncio.run(sc.scan_target("127.0.0.1")))
        assert d["local_resource_errors"] == 1
        assert d["health"] == "degraded"

    def test_open_only_output_still_keeps_full_metrics(self):
        # report_closed=False filters OUTPUT to open, but metrics count every port.
        ports = [1, 2, 3]
        sc = PortScanner(_scope(), ports=ports, concurrency=3, rate=1e9,
                         report_closed=False)
        states = {1: "open", 2: "closed", 3: "filtered"}

        async def fake_attempt(target, port):
            return ScanResult(sc.name, target, port=port, proto="tcp",
                              status=states[port], data={"reason": "x"})

        sc._attempt = fake_attempt
        results = asyncio.run(sc.scan_target("127.0.0.1"))
        emitted_ports = [r for r in results if r.status != "scan_summary"]
        assert len(emitted_ports) == 1 and emitted_ports[0].status == "open"
        d = _summary(results)
        assert d["closed"] == 1 and d["filtered"] == 1 and d["classified"] == 3

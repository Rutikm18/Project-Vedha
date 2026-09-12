"""
Congestion state must belong to ONE host, even when one scanner object scans
several hosts at once.

The engine builds a single PortScanner for the whole port stage and calls
`scan_target()` for every host concurrently. The RTT estimator and the AIMD
window are already per-call, but the DELIVERY window — the signal that decides
whether silence means congestion — lived on the instance:

    self._probe_window.clear()      # in scan_target
    self._probe_window.append(...)  # in _note_probe_outcome

So every concurrent host wrote into one deque, and each new host wiped it. One
firewalled host (all silence) therefore dragged the delivery rate below the floor
for HEALTHY hosts scanned beside it, and they were throttled to the minimum
window for a condition that was never theirs. The comment above the field already
said the state is "a property of the path to THIS host"; the implementation made
it a property of the scanner.

The safety property must survive: a genuinely silent host still backs off.
"""
from __future__ import annotations

import asyncio

from scanner.port_scanner import PortScanner
from scanner.scanner_base import ScopeGuard

SILENT = "127.0.0.2"      # a host that answers nothing (firewall drops probes)
HEALTHY = "127.0.0.3"     # a host that refuses every port, promptly


def _scanner():
    return PortScanner(
        ScopeGuard.from_list(["127.0.0.0/8"]),
        ports=list(range(1, 4001)), timeout=0.01, concurrency=256,
        rate=1_000_000, reprobe=False, adaptive_timeout=False)


def _congestion(results):
    return [r for r in results if r.status == "scan_summary"][0].data["congestion"]


def _run_both_hosts_concurrently(scanner):
    """One scanner object, two hosts in flight — exactly what the port stage does.

    The healthy host probes slightly slower so the silent host dominates any
    SHARED window; that is the condition under which cross-host contamination
    shows up, and it is what the field hits (silent hosts are the slow ones).
    """
    async def _attempt(target, port, est=None, min_timeout=None):
        if target == SILENT:
            return scanner._build(target, port, "filtered", "no_response",
                                  "no response within 0.01s")
        await asyncio.sleep(0.001)
        return scanner._build(target, port, "closed", "connection_refused",
                              None, rtt_ms=0.4)

    scanner._attempt = _attempt

    async def _both():
        return await asyncio.gather(
            scanner.scan_target(SILENT),
            asyncio.wait_for(scanner.scan_target(HEALTHY), 120),
        )

    return asyncio.run(_both())


class TestConcurrentHostsDoNotShareDeliveryState:
    def test_a_healthy_host_is_not_throttled_by_a_silent_neighbour(self):
        scanner = _scanner()
        _silent_results, healthy_results = _run_both_hosts_concurrently(scanner)

        congestion = _congestion(healthy_results)
        assert congestion["throttled"] is False, (
            "the healthy host was throttled by another host's silence: "
            f"{congestion}")
        assert congestion["final_window"] == congestion["max_window"]

    def test_a_genuinely_silent_host_still_backs_off(self):
        """The safety property. Isolating the state must not disable it."""
        scanner = _scanner()
        silent_results, _healthy_results = _run_both_hosts_concurrently(scanner)

        assert _congestion(silent_results)["throttled"] is True

    def test_every_port_is_still_classified_for_both_hosts(self):
        """Isolation must not cost coverage."""
        scanner = _scanner()
        silent_results, healthy_results = _run_both_hosts_concurrently(scanner)

        for results in (silent_results, healthy_results):
            summary = [r for r in results if r.status == "scan_summary"][0].data
            assert summary["ports_attempted"] == 4000
            assert summary["complete"] is True

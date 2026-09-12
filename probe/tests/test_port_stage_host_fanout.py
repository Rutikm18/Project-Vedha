"""
The port stage must scan a BOUNDED number of hosts at once.

It fanned out with `max_in_flight=concurrency` — the socket budget, not a host
budget. At the aggressive envelope that is 300, i.e. every live host in a /24
started its port sweep simultaneously and they all finished at the same time,
near the end. Three consequences, all measured:

  * memory scaled with the host count (47 MB per host before the retention fix);
  * no host finished EARLY, so an interrupted job had nothing complete to show;
  * a per-host time budget was meaningless — every host's clock started at once
    while they shared one semaphore, so they all ran out together.

The deep stage already had the right idea (`host_concurrency`, default 8, capped
at 64, overridable with PROBE_HOST_CONCURRENCY). The port stage now uses the same
slots. Total sockets are unchanged — the shared semaphore still bounds them — so
this costs no throughput; it just stops starting work that cannot proceed.

Discovery deliberately keeps its wide fan-out: it is one cheap probe per host and
breadth is the whole point of it.
"""
from __future__ import annotations

import asyncio

from scanner.scanner_base import ScanResult, ScopeGuard
from workflow.workflow_engine import run_engagement

TARGETS = [f"10.0.0.{i}" for i in range(1, 41)]


def _tracking(component_id, tracker, *, port=None, data=None):
    """A stand-in scanner that records peak simultaneous scan_target() calls."""
    class Scanner:
        name = component_id

        def __init__(self, *args, **kwargs):
            pass

        async def scan_target(self, host):
            state = tracker.setdefault(component_id, {"cur": 0, "max": 0})
            state["cur"] += 1
            state["max"] = max(state["max"], state["cur"])
            try:
                await asyncio.sleep(0.01)
                return [ScanResult(scanner=component_id, target=host, port=port,
                                   proto="tcp" if port else None, status="open",
                                   data=data or {})]
            finally:
                state["cur"] -= 1
    return Scanner


def _wire(monkeypatch, tracker):
    monkeypatch.setattr("workflow.workflow_engine.HostDiscoveryScanner",
                        _tracking("host_discovery", tracker,
                                  data={"alive": True}))
    monkeypatch.setattr("workflow.workflow_engine.PortScanner",
                        _tracking("port_scan", tracker, port=445))
    monkeypatch.setattr("workflow.workflow_engine.OSFingerprintScanner",
                        _tracking("os_fingerprint", tracker))


def _run(**kwargs):
    return asyncio.run(run_engagement(
        TARGETS, ScopeGuard.from_list(["10.0.0.0/24"]),
        stage_ceiling="port_scan", port_override=[445], **kwargs))


class TestPortStageFanOut:
    def test_respects_an_explicit_host_concurrency(self, monkeypatch):
        tracker: dict = {}
        _wire(monkeypatch, tracker)

        _run(concurrency=300, host_concurrency=4)

        assert tracker["port_scan"]["max"] <= 4

    def test_default_is_the_deep_stage_slot_count_not_the_socket_budget(
            self, monkeypatch):
        """Default host_concurrency is min(8, concurrency) — 8 here, not 300."""
        tracker: dict = {}
        _wire(monkeypatch, tracker)

        _run(concurrency=300)

        assert tracker["port_scan"]["max"] <= 8

    def test_every_host_is_still_scanned(self, monkeypatch):
        """Bounding the fan-out must not drop hosts."""
        tracker: dict = {}
        _wire(monkeypatch, tracker)

        assets = _run(concurrency=300, host_concurrency=4)

        scanned = [h for h in TARGETS if 445 in assets[h].open_ports_for_deep_scan()]
        assert len(scanned) == len(TARGETS)


class TestDiscoveryStaysWide:
    def test_host_discovery_keeps_its_broad_fan_out(self, monkeypatch):
        """One cheap probe per host, and finding the live set fast is the point."""
        tracker: dict = {}
        _wire(monkeypatch, tracker)

        _run(concurrency=300, host_concurrency=4)

        assert tracker["host_discovery"]["max"] > 8

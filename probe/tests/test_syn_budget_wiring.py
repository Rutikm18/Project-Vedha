"""
The per-host wall-clock budget must reach the DEEP path, which is the only path
that needs it.

`deep` resolves 65,535 ports, which is above `_SYN_PORT_THRESHOLD`, so the port
stage builds a SynScanner — and SynScanner was constructed without
`deadline_seconds` and without `retries`. The 30-minute ceiling therefore applied
to exactly the scans that did not need it (narrow connect scans) and never to the
one that did. Measured consequence: a single RST-suppressing host ran 2,728s of a
job whose ceiling claimed to be 1,800s.

Two shapes of budget, one meaning:
  * connect fallback (off privileged Linux — macOS, and Docker without NET_RAW):
    the budget is PortScanner's own `deadline_seconds`.
  * raw SYN path: stop sending once the clock is out. Ports never sent are simply
    not reported (report_closed is False), so a truncated sweep still cannot
    invent `filtered` evidence out of a clock running out.
"""
from __future__ import annotations

import asyncio
import socket

import pytest

from scanner import syn_scanner as ss
from scanner.scanner_base import ScanResult, ScopeGuard
from workflow.workflow_engine import run_engagement

KEY = b"\x01" * 16


def _scope():
    return ScopeGuard.from_list(["10.0.0.0/8"])


class TestFallbackCarriesTheBudget:
    """Off privileged Linux the SYN scanner IS a connect scanner. A budget that
    stops at the wrapper is not a budget."""

    def test_deadline_reaches_the_fallback_connect_scanner(self):
        sc = ss.SynScanner(_scope(), ports=[80], force_fallback=True,
                           deadline_seconds=90)
        assert sc._fallback.deadline_seconds == 90

    def test_no_deadline_stays_unbounded(self):
        sc = ss.SynScanner(_scope(), ports=[80], force_fallback=True)
        assert sc._fallback.deadline_seconds is None

    def test_retries_reach_the_fallback_connect_scanner(self):
        """`deep` asks for 2 retries; the fallback silently used PortScanner's
        default of 1, so the deep envelope was not what deep promised."""
        sc = ss.SynScanner(_scope(), ports=[80], force_fallback=True, retries=2)
        assert sc._fallback.retries == 2

    def test_mid_run_privilege_loss_keeps_the_budget(self):
        """The second fallback — built when the raw path fails mid-run — is a
        separate construction site and dropped the budget too."""
        sc = ss.SynScanner(_scope(), ports=[80], deadline_seconds=45, retries=2)
        sc._supported = True
        sc._fallback = None

        async def _boom(target, *_):
            raise OSError("privileges dropped")
        sc._syn_scan_target = _boom

        asyncio.run(sc.scan_target("10.0.0.5"))
        assert sc._fallback.deadline_seconds == 45
        assert sc._fallback.retries == 2


class TestRawPathStopsAtTheDeadline:
    """Raw sockets cannot run in CI, so drive `_syn_scan_blocking` with the
    fake-socket harness the retransmit tests already use."""

    def _patch(self, monkeypatch, sent_ports, *, per_send_seconds=0.0):
        monkeypatch.setattr(ss.random, "randint", lambda a, b: 50000)
        monkeypatch.setattr(
            ss, "resolve",
            lambda t, p, proto="tcp", family=None: (socket.AF_INET, (t, 0)))
        monkeypatch.setattr(ss, "_local_source_ip", lambda dst: "10.0.0.1")

        clock = {"now": 0.0}
        real_monotonic = ss.time.monotonic

        def _monotonic():
            return real_monotonic() + clock["now"]
        monkeypatch.setattr(ss.time, "monotonic", _monotonic)

        class _Send:
            def setsockopt(self, *a): pass

            def sendto(self, pkt, addr):
                sent_ports.append(ss.parse_packet(pkt)["dst_port"])
                clock["now"] += per_send_seconds      # advance the virtual clock

            def close(self): pass

        class _Recv:
            def setblocking(self, *a): pass
            def setsockopt(self, *a): pass

            def recv(self, n):
                raise OSError("no data")

            def close(self): pass

        def _factory(family, stype, proto):
            return _Recv() if proto == socket.IPPROTO_TCP else _Send()
        monkeypatch.setattr(ss.socket, "socket", _factory)

    def test_send_loop_stops_once_the_budget_is_spent(self, monkeypatch):
        sent: list[int] = []
        sc = ss.SynScanner(_scope(), ports=list(range(1, 101)), key=KEY,
                           retries=0, timeout=0.01, pace_sends=False,
                           deadline_seconds=10)
        self._patch(monkeypatch, sent, per_send_seconds=1.0)

        sc._syn_scan_blocking("10.0.0.5")

        assert 0 < len(sent) < 100, (
            f"expected a truncated sweep, sent {len(sent)} of 100 ports")

    def test_unsent_ports_are_never_reported_filtered(self, monkeypatch):
        """A clock running out is not evidence of a firewall."""
        sent: list[int] = []
        sc = ss.SynScanner(_scope(), ports=list(range(1, 101)), key=KEY,
                           retries=0, timeout=0.01, pace_sends=False,
                           report_closed=True, deadline_seconds=10)
        self._patch(monkeypatch, sent, per_send_seconds=1.0)

        results = sc._syn_scan_blocking("10.0.0.5")

        # Exclude the per-host scan_summary (port=None, covers the whole
        # host) — this check is about PER-PORT results only.
        reported = {r.port for r in results if r.port is not None}
        assert reported <= set(sent), (
            "ports that were never sent must not appear in the results")

    def test_a_scan_inside_its_budget_is_untouched(self, monkeypatch):
        sent: list[int] = []
        sc = ss.SynScanner(_scope(), ports=list(range(1, 51)), key=KEY,
                           retries=0, timeout=0.01, pace_sends=False,
                           deadline_seconds=3600)
        self._patch(monkeypatch, sent, per_send_seconds=1.0)

        sc._syn_scan_blocking("10.0.0.5")

        assert len(sent) == 50

    def test_no_budget_scans_every_port(self, monkeypatch):
        sent: list[int] = []
        sc = ss.SynScanner(_scope(), ports=list(range(1, 51)), key=KEY,
                           retries=0, timeout=0.01, pace_sends=False)
        self._patch(monkeypatch, sent, per_send_seconds=1.0)

        sc._syn_scan_blocking("10.0.0.5")

        assert len(sent) == 50


class TestEngineWiresTheBudgetIntoTheSynScanner:
    """The whole point: intensity `deep` -> tuning -> run_engagement -> the
    scanner object that actually runs. A kwarg dropped at this seam is why the
    ceiling never applied in the field."""

    def _wire(self, monkeypatch, captured):
        def _fake(component_id, *, port=None, status="open", data=None):
            class Scanner:
                name = component_id

                def __init__(self, *args, **kwargs):
                    captured.setdefault(component_id, []).append(kwargs)

                async def scan_target(self, host):
                    return [ScanResult(scanner=component_id, target=host,
                                       port=port,
                                       proto="tcp" if port else None,
                                       status=status, data=data or {})]
            return Scanner

        monkeypatch.setattr("workflow.workflow_engine.HostDiscoveryScanner",
                            _fake("host_discovery", data={"alive": True}))
        monkeypatch.setattr("workflow.workflow_engine.SynScanner",
                            _fake("syn_scan", port=445))
        monkeypatch.setattr("workflow.workflow_engine.OSFingerprintScanner",
                            _fake("os_fingerprint"))

    @pytest.mark.parametrize("kwarg,expected", [("deadline_seconds", 1800),
                                                ("retries", 2)])
    def test_deep_envelope_reaches_the_syn_scanner(self, monkeypatch, kwarg,
                                                   expected):
        captured: dict = {}
        self._wire(monkeypatch, captured)

        asyncio.run(run_engagement(
            ["10.0.0.1"], ScopeGuard.from_list(["10.0.0.0/24"]),
            stage_ceiling="port_scan", port_override=[445],
            scan_method="syn", retries=2, max_host_seconds=1800))

        assert captured["syn_scan"][0][kwarg] == expected

"""
test_adaptive_rate.py — Tier 1.3: adaptive congestion control + UDP retransmit.

Two independently-tested pieces:
  * AdaptiveRateController — an AIMD (additive-increase / multiplicative-decrease)
    in-flight window: grows on success, halves on loss, bounded [min, max]. This
    self-tunes the send rate to the network and to a host's RFC-1812 ICMP
    rate-limit instead of a fixed token bucket.
  * async_udp_probe_retry — bounded per-port retransmit: returns immediately on a
    definitive result (reply=open or ICMP-unreachable=closed), retries only on
    silence, so a dropped/rate-limited reply is not mislabelled open|filtered.
"""

from __future__ import annotations

import asyncio

import pytest

from scanner.scanner_base import (
    AdaptiveRateController, async_udp_probe_retry, _UDP_CLOSED, ScopeGuard,
)


# ── AdaptiveRateController: window state machine ──────────────────────────────

class TestWindowStateMachine:
    def test_initial_window(self):
        ctl = AdaptiveRateController(init_window=10)
        assert ctl.window == 10

    def test_slow_start_grows_by_one_per_success(self):
        ctl = AdaptiveRateController(init_window=10, ssthresh=300)
        ctl._on_success()
        assert ctl.cwnd == 11
        ctl._on_success()
        assert ctl.cwnd == 12

    def test_congestion_avoidance_grows_sublinearly(self):
        # cwnd >= ssthresh -> linear (per-RTT) growth: +1/cwnd per success.
        ctl = AdaptiveRateController(init_window=10, ssthresh=5)
        ctl._on_success()
        assert 10 < ctl.cwnd < 11

    def test_loss_halves_window(self):
        ctl = AdaptiveRateController(init_window=10, ssthresh=300)
        ctl._on_loss()
        assert ctl.cwnd == 5

    def test_loss_sets_ssthresh_to_half(self):
        ctl = AdaptiveRateController(init_window=20, ssthresh=300)
        ctl._on_loss()
        assert ctl.ssthresh == 10

    def test_window_never_below_min(self):
        ctl = AdaptiveRateController(init_window=1, min_window=1)
        ctl._on_loss()
        ctl._on_loss()
        assert ctl.window == 1
        assert ctl.cwnd >= 1

    def test_window_never_above_max(self):
        ctl = AdaptiveRateController(init_window=9, max_window=10, ssthresh=300)
        for _ in range(50):
            ctl._on_success()
        assert ctl.cwnd <= 10
        assert ctl.window == 10

    def test_recovery_after_loss_enters_congestion_avoidance(self):
        ctl = AdaptiveRateController(init_window=16, ssthresh=300)
        ctl._on_loss()                      # cwnd 8, ssthresh 8
        assert ctl.cwnd == 8 and ctl.ssthresh == 8
        ctl._on_success()                   # cwnd>=ssthresh -> CA, small bump
        assert 8 < ctl.cwnd < 9


# ── AdaptiveRateController: async gating ──────────────────────────────────────

class TestWindowGating:
    def test_acquire_blocks_when_window_full(self):
        async def _run():
            ctl = AdaptiveRateController(init_window=2, max_window=2, ssthresh=2)
            await ctl.acquire()
            await ctl.acquire()             # in_flight == window
            try:
                await asyncio.wait_for(ctl.acquire(), timeout=0.1)
                return "did_not_block"
            except asyncio.TimeoutError:
                return "blocked"
        assert asyncio.run(_run()) == "blocked"

    def test_release_unblocks_waiter(self):
        async def _run():
            ctl = AdaptiveRateController(init_window=1, max_window=4, ssthresh=4)
            await ctl.acquire()             # window full (1 in flight)

            async def waiter():
                await ctl.acquire()
                return "acquired"

            task = asyncio.ensure_future(waiter())
            await asyncio.sleep(0.05)
            assert not task.done()          # blocked
            await ctl.report_success()      # frees a slot + grows window
            return await asyncio.wait_for(task, timeout=1.0)
        assert asyncio.run(_run()) == "acquired"

    def test_report_loss_shrinks_and_releases(self):
        async def _run():
            ctl = AdaptiveRateController(init_window=10, ssthresh=300)
            await ctl.acquire()
            await ctl.report_loss()
            return ctl.cwnd
        assert asyncio.run(_run()) == 5


# ── UDP retransmit wrapper ────────────────────────────────────────────────────

class TestUdpRetransmit:
    def test_returns_immediately_on_reply(self, monkeypatch):
        import scanner.scanner_base as sb
        calls = {"n": 0}

        async def fake(t, p, pl, to):
            calls["n"] += 1
            return b"reply"

        monkeypatch.setattr(sb, "async_udp_probe", fake)
        r = asyncio.run(sb.async_udp_probe_retry("h", 1, b"x", 0.1, max_retries=3))
        assert r == b"reply"
        assert calls["n"] == 1              # no wasted retries on success

    def test_returns_immediately_on_closed(self, monkeypatch):
        import scanner.scanner_base as sb
        calls = {"n": 0}

        async def fake(t, p, pl, to):
            calls["n"] += 1
            return sb._UDP_CLOSED

        monkeypatch.setattr(sb, "async_udp_probe", fake)
        r = asyncio.run(sb.async_udp_probe_retry("h", 1, b"x", 0.1, max_retries=3))
        assert r is sb._UDP_CLOSED
        assert calls["n"] == 1              # closed is definitive, no retry

    def test_retries_exhaust_on_silence(self, monkeypatch):
        import scanner.scanner_base as sb
        calls = {"n": 0}

        async def fake(t, p, pl, to):
            calls["n"] += 1
            return None

        monkeypatch.setattr(sb, "async_udp_probe", fake)
        r = asyncio.run(sb.async_udp_probe_retry("h", 1, b"x", 0.1, max_retries=2))
        assert r is None
        assert calls["n"] == 3              # 1 initial + 2 retries

    def test_retry_recovers_dropped_reply(self, monkeypatch):
        import scanner.scanner_base as sb
        seq = [None, b"late-reply"]
        calls = {"n": 0}

        async def fake(t, p, pl, to):
            r = seq[calls["n"]]
            calls["n"] += 1
            return r

        monkeypatch.setattr(sb, "async_udp_probe", fake)
        r = asyncio.run(sb.async_udp_probe_retry("h", 1, b"x", 0.1, max_retries=2))
        assert r == b"late-reply"           # a lossy UDP drop is recovered
        assert calls["n"] == 2


# ── UDPScanner adaptive integration (real loopback) ───────────────────────────

class _EchoProtocol(asyncio.DatagramProtocol):
    def connection_made(self, transport):
        self._t = transport

    def datagram_received(self, data, addr):
        self._t.sendto(data, addr)


class TestUdpScannerAdaptive:
    def test_adaptive_scanner_creates_controller(self):
        import scanner.udp_scanner as us
        scanner = us.UDPScanner(ScopeGuard.from_list(["127.0.0.0/8"]),
                                ports=[53], adaptive=True)
        assert scanner.rate_ctl is not None

    def test_non_adaptive_scanner_has_no_controller(self):
        import scanner.udp_scanner as us
        scanner = us.UDPScanner(ScopeGuard.from_list(["127.0.0.0/8"]),
                                ports=[53])
        assert scanner.rate_ctl is None

    def test_adaptive_scanner_detects_open_on_loopback(self):
        import scanner.udp_scanner as us

        async def _run():
            loop = asyncio.get_running_loop()
            transport, _ = await loop.create_datagram_endpoint(
                _EchoProtocol, local_addr=("127.0.0.1", 0))
            port = transport.get_extra_info("socket").getsockname()[1]
            us.UDP_PROBES[port] = ("dns", us._dns_probe())
            try:
                scope = ScopeGuard.from_list(["127.0.0.0/8"])
                scanner = us.UDPScanner(scope, ports=[port], timeout=2.0,
                                        adaptive=True)
                return await scanner._probe("127.0.0.1", port)
            finally:
                transport.close()
                us.UDP_PROBES.pop(port, None)

        r = asyncio.run(_run())
        assert r is not None
        assert r.status == "open"

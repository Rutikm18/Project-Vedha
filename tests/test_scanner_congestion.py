"""
test_scanner_congestion.py — proof tests for the offensive-accuracy pass
(RESEARCH_IMPROVEMENTS.md roadmap #5, #6b, #8, #9).

Every test here defends a specific FALSE-NEGATIVE mechanism, because that is the
failure mode these changes exist to remove: a scanner that causes its own packet
loss reports `filtered`, and an operator cannot tell that apart from a firewall.

  * SendPacer      — paced SYN sends + AIMD backoff (#5, #2.2)
  * _wait_readable — event-driven receive instead of a 5ms poll (#8, #2.3)
  * AIMD cwnd      — connect-path congestion window (#5, #1.2)
  * tcp stack      — connect-path OS/link signals, and the deliberate REFUSAL to
                     synthesize an initial window (#6b, #3.2)
  * resolve_candidates — dual-stack fallback (#9, #4.1)

Pure/deterministic: no privileged sockets, no external network.
"""
from __future__ import annotations

import asyncio
import socket
import struct
import time

import pytest

from scanner import port_scanner as ps
from scanner import syn_scanner as ss
from scanner.scanner_base import (
    AdaptiveRateController,
    ScopeGuard,
    SendPacer,
    resolve_candidates,
)


# ── SendPacer: AIMD on the send loop (#5 / #2.2) ─────────────────────────────
class TestSendPacer:
    def test_clean_round_increases_rate_additively(self):
        p = SendPacer(100.0)
        p.observe_round(sent=100, answered=100)
        assert p.rate == pytest.approx(110.0)      # +10% additive increase
        assert p.backoffs == 0

    def test_lossy_round_halves_the_rate(self):
        p = SendPacer(100.0)
        p.observe_round(sent=100, answered=10)     # 90% loss
        assert p.rate == pytest.approx(50.0)       # multiplicative decrease
        assert p.backoffs == 1

    def test_backoff_is_bounded_by_min_rate(self):
        p = SendPacer(100.0, min_rate=25.0)
        for _ in range(10):
            p.observe_round(sent=100, answered=0)
        assert p.rate == 25.0                      # never collapses to zero

    def test_growth_is_bounded_by_max_rate(self):
        p = SendPacer(100.0)
        for _ in range(100):
            p.observe_round(sent=10, answered=10)
        assert p.rate <= p.max_rate
        assert p.max_rate == pytest.approx(400.0)  # 4x the operator's --rate

    def test_loss_just_under_threshold_does_not_back_off(self):
        p = SendPacer(100.0, loss_threshold=0.15)
        p.observe_round(sent=100, answered=90)     # 10% loss < 15%
        assert p.backoffs == 0
        assert p.rate > 100.0

    def test_empty_round_is_ignored_not_treated_as_total_loss(self):
        p = SendPacer(100.0)
        p.observe_round(sent=0, answered=0)
        assert p.rate == 100.0 and p.rounds == 0 and p.backoffs == 0

    def test_pace_actually_spends_wall_time_at_a_low_rate(self):
        # The whole point: sends must be spread out, not emitted back-to-back.
        p = SendPacer(200.0)                       # 5ms per packet
        t0 = time.monotonic()
        for _ in range(6):
            p.pace()
        elapsed = time.monotonic() - t0
        assert elapsed >= 0.015                    # >= 5 intervals, generous slack

    def test_first_pace_does_not_block(self):
        p = SendPacer(1.0)                         # 1s interval
        t0 = time.monotonic()
        p.pace()
        assert time.monotonic() - t0 < 0.2         # schedule starts now, no stall

    def test_rate_zero_disables_pacing(self):
        p = SendPacer(0.0)
        t0 = time.monotonic()
        for _ in range(50):
            p.pace()
        assert time.monotonic() - t0 < 0.2

    def test_stats_expose_throttling(self):
        p = SendPacer(100.0)
        p.observe_round(sent=100, answered=0)
        s = p.stats()
        assert s["initial_rate"] == 100.0 and s["final_rate"] == 50.0
        assert s["backoffs"] == 1 and s["rounds"] == 1


# ── event-driven receive (#8 / #2.3) ─────────────────────────────────────────
class TestWaitReadable:
    def test_returns_false_when_nothing_arrives_before_deadline(self):
        a, b = socket.socketpair()
        try:
            assert ss._wait_readable(a, 0.01) is False
        finally:
            a.close(); b.close()

    def test_returns_true_as_soon_as_data_is_waiting(self):
        a, b = socket.socketpair()
        try:
            b.send(b"x")
            assert ss._wait_readable(a, 1.0) is True
        finally:
            a.close(); b.close()

    def test_zero_timeout_never_blocks(self):
        a, b = socket.socketpair()
        try:
            assert ss._wait_readable(a, 0.0) is False
        finally:
            a.close(); b.close()

    def test_unselectable_object_degrades_to_assume_readable(self):
        # A socket-like without a usable fileno must NOT abort the scan; it falls
        # back to the plain non-blocking read attempt.
        class _NoFileno:
            pass
        assert ss._wait_readable(_NoFileno(), 0.5) is True


# ── connect-path AIMD congestion window (#5 / #1.2) ──────────────────────────
def _scanner(ports, **kw):
    return ps.PortScanner(ScopeGuard.from_list(["127.0.0.0/8"]),
                          ports=ports, timeout=0.01, concurrency=8,
                          rate=10_000, **kw)


class TestConnectCongestionWindow:
    def _silent(self, sc):
        async def _attempt(target, port, est=None, min_timeout=None):
            return sc._build(target, port, "filtered", "no_response", "silence")
        return _attempt

    def test_all_silent_host_shrinks_the_window(self):
        sc = _scanner(list(range(1, 41)), retries=0, reprobe=False)
        sc._attempt = self._silent(sc)
        out = asyncio.run(asyncio.wait_for(sc.scan_target("127.0.0.1"), 30))
        summ = [r for r in out if r.status == "scan_summary"][0]
        cong = summ.data["congestion"]
        # Every probe was lost, so AIMD must have backed the window off the
        # starting concurrency — that backoff is what raises recall on a
        # genuinely lossy path.
        assert cong["throttled"] is True
        assert cong["final_window"] < cong["max_window"]

    def test_responsive_host_is_not_throttled(self):
        sc = _scanner(list(range(1, 41)), retries=0)

        async def _open(target, port, est=None, min_timeout=None):
            return sc._build(target, port, "closed", "connection_refused", "rst")
        sc._attempt = _open
        out = asyncio.run(asyncio.wait_for(sc.scan_target("127.0.0.1"), 30))
        summ = [r for r in out if r.status == "scan_summary"][0]
        # A definitive RST proves the path carries our packets: no backoff, so a
        # healthy LAN scan keeps running at full speed.
        assert summ.data["congestion"]["throttled"] is False

    def test_scan_completes_every_port_under_throttling(self):
        # Proves acquire() and report_*() are balanced. If they leaked, the
        # worker pool would deadlock and this would hit the timeout instead.
        ports = list(range(1, 61))
        sc = _scanner(ports, retries=0, reprobe=False)
        sc._attempt = self._silent(sc)
        out = asyncio.run(asyncio.wait_for(sc.scan_target("127.0.0.1"), 30))
        summ = [r for r in out if r.status == "scan_summary"][0]
        assert summ.data["ports_attempted"] == len(ports)
        assert summ.data["complete"] is True

    def test_congestion_can_be_disabled(self):
        sc = _scanner([80, 443], retries=0, congestion=False, reprobe=False)
        sc._attempt = self._silent(sc)
        out = asyncio.run(asyncio.wait_for(sc.scan_target("127.0.0.1"), 30))
        summ = [r for r in out if r.status == "scan_summary"][0]
        assert "congestion" not in summ.data

    def test_window_never_falls_below_one(self):
        c = AdaptiveRateController(init_window=8, min_window=1, max_window=8)
        for _ in range(20):
            c._on_loss()
        assert c.window >= 1


# ── connect-path TCP stack harvest (#6b / #3.2) ──────────────────────────────
def _tcp_info_buf(*, wscale: int, rtt_us: int, advmss: int) -> bytes:
    """A synthetic Linux `struct tcp_info`: 8 u8 flag bytes then 20 u32 fields."""
    flags = bytearray(8)
    flags[6] = wscale & 0x0F                 # tcpi_snd_wscale = low nibble
    u32 = [0] * 20
    u32[15] = rtt_us                         # tcpi_rtt
    u32[19] = advmss                         # tcpi_advmss
    return bytes(flags) + struct.pack("20I", *u32)


class _FakeSock:
    def __init__(self, maxseg=None, info=None):
        self._maxseg, self._info = maxseg, info

    def getsockopt(self, level, opt, buflen=None):
        if buflen is None:
            if self._maxseg is None:
                raise OSError("no TCP_MAXSEG")
            return self._maxseg
        if self._info is None:
            raise OSError("no TCP_INFO")
        return self._info


class TestHarvestTcpStack:
    def test_none_socket_yields_nothing(self):
        assert ps._harvest_tcp_stack(None) == {}

    def test_object_without_getsockopt_is_survivable(self):
        assert ps._harvest_tcp_stack(object()) == {}

    def test_maxseg_is_reported_but_never_as_advertised_mss(self, monkeypatch):
        """TCP_MAXSEG on an ESTABLISHED socket is the post-options effective
        segment size, not the advertised MSS option. Treating it as advertised
        invents a VPN on plain Ethernet — observed for real against a LAN host
        whose TCP timestamps drop 1460 to 1448 (mtu 1488 -> 'tunnel_or_vpn')."""
        monkeypatch.delattr(ps.socket, "TCP_INFO", raising=False)
        got = ps._harvest_tcp_stack(_FakeSock(maxseg=1448))
        assert got["mss_effective"] == 1448
        assert "mss" not in got            # must not reach the MTU inference

    def test_timestamped_ethernet_host_is_not_mislabelled_a_tunnel(self, monkeypatch):
        """End-to-end form of the same guarantee, through os_fingerprint."""
        from scanner.os_fingerprint import fingerprint_os
        monkeypatch.delattr(ps.socket, "TCP_INFO", raising=False)
        stack = ps._harvest_tcp_stack(_FakeSock(maxseg=1448))
        signals = fingerprint_os(ttl=128, mss=stack.get("mss"))["signals"]
        assert signals.get("link_hint") != "tunnel_or_vpn"

    def test_tcp_info_yields_wscale_rtt_and_advmss(self, monkeypatch):
        monkeypatch.setattr(ps.socket, "TCP_INFO", 11, raising=False)
        buf = _tcp_info_buf(wscale=7, rtt_us=1234, advmss=1460)
        got = ps._harvest_tcp_stack(_FakeSock(maxseg=536, info=buf))
        assert got["wscale"] == 7
        assert got["rtt_us"] == 1234
        assert got["mss"] == 1460          # advertised MSS (tcpi_advmss) only
        assert got["mss_effective"] == 536  # kept separate, never conflated

    def test_short_tcp_info_buffer_is_ignored(self, monkeypatch):
        monkeypatch.setattr(ps.socket, "TCP_INFO", 11, raising=False)
        got = ps._harvest_tcp_stack(_FakeSock(maxseg=1460, info=b"\x00" * 16))
        assert got == {"mss_effective": 1460}   # degrades, does not crash or guess

    def test_never_synthesizes_an_initial_tcp_window(self, monkeypatch):
        """THE accuracy guarantee for #6b.

        os_fingerprint scores `tcp_window` against INITIAL-window tables. A
        post-handshake window has already been scaled and has drifted, so
        emitting one here would produce confident-but-wrong OS attributions.
        The connect path must therefore never supply that key."""
        monkeypatch.setattr(ps.socket, "TCP_INFO", 11, raising=False)
        buf = _tcp_info_buf(wscale=7, rtt_us=999, advmss=1460)
        got = ps._harvest_tcp_stack(_FakeSock(maxseg=1460, info=buf))
        assert "tcp_window" not in got

    def test_absurd_values_are_rejected(self, monkeypatch):
        monkeypatch.setattr(ps.socket, "TCP_INFO", 11, raising=False)
        buf = _tcp_info_buf(wscale=0, rtt_us=0, advmss=0)
        got = ps._harvest_tcp_stack(_FakeSock(maxseg=None, info=buf))
        assert got == {}                   # zeros are "unknown", not facts


# ── dual-stack resolution fallback (#9 / #4.1) ───────────────────────────────
_V6 = (socket.AF_INET6, ("2001:db8::1", 80, 0, 0))
_V4 = (socket.AF_INET, ("192.0.2.1", 80))


def _fake_gai(v6_first=True):
    order = [_V6, _V4] if v6_first else [_V4, _V6]
    def _gai(host, port, family, socktype):
        # getaddrinfo repeats each address per socktype; the helper must dedupe.
        return [(f, socktype, 6, "", sa) for f, sa in order] * 2
    return _gai


class TestResolveCandidates:
    def test_returns_every_family_in_order(self, monkeypatch):
        monkeypatch.setattr(socket, "getaddrinfo", _fake_gai(v6_first=True))
        got = resolve_candidates("host.example", 80)
        assert [f for f, _ in got] == [socket.AF_INET6, socket.AF_INET]

    def test_deduplicates_repeated_addresses(self, monkeypatch):
        monkeypatch.setattr(socket, "getaddrinfo", _fake_gai())
        assert len(resolve_candidates("host.example", 80)) == 2

    def test_v4_is_reachable_even_when_aaaa_sorts_first(self, monkeypatch):
        """The false negative #9 exists to kill: a dual-stack host whose IPv6
        path is black-holed must still expose its IPv4 address to the caller."""
        monkeypatch.setattr(socket, "getaddrinfo", _fake_gai(v6_first=True))
        fams = [f for f, _ in resolve_candidates("host.example", 80)]
        assert socket.AF_INET in fams

    def test_family_filter_restricts_results(self, monkeypatch):
        monkeypatch.setattr(socket, "getaddrinfo", _fake_gai())
        got = resolve_candidates("host.example", 80, family=socket.AF_INET)
        assert [f for f, _ in got] == [socket.AF_INET]

    def test_absent_requested_family_falls_back_rather_than_failing(self, monkeypatch):
        def _only_v6(host, port, family, socktype):
            return [(socket.AF_INET6, socktype, 6, "", _V6[1])]
        monkeypatch.setattr(socket, "getaddrinfo", _only_v6)
        got = resolve_candidates("v6only.example", 80, family=socket.AF_INET)
        assert [f for f, _ in got] == [socket.AF_INET6]

    def test_unresolvable_name_raises(self, monkeypatch):
        monkeypatch.setattr(socket, "getaddrinfo",
                            lambda *a, **k: (_ for _ in ()).throw(socket.gaierror("nope")))
        with pytest.raises(Exception):
            resolve_candidates("nx.invalid", 80)

    def test_literal_ip_resolves_to_itself(self):
        got = resolve_candidates("127.0.0.1", 80)
        assert got and got[0][0] == socket.AF_INET and got[0][1][0] == "127.0.0.1"


# ── cleanup pass over ambiguous ports (measured defect, 192.168.1.65) ────────
class TestReprobeCleanupPass:
    """A host that rate-limits its RSTs answers only when probed gently. The
    fast sweep then reports `filtered` -- a false negative that reads to an
    operator as a firewall. Measured live: 69/69 such ports were really `closed`."""

    def _rate_limited(self, sc, answer_after: int):
        """Silent for the first `answer_after` probes per port, then a real RST."""
        seen: dict = {}

        async def _attempt(target, port, est=None, min_timeout=None):
            seen[port] = seen.get(port, 0) + 1
            if seen[port] <= answer_after:
                return sc._build(target, port, "filtered", "no_response", "silence")
            return sc._build(target, port, "closed", "connection_refused", "rst")
        return _attempt

    def _summary(self, out):
        return [r for r in out if r.status == "scan_summary"][0]

    def test_recovers_ports_the_fast_sweep_called_filtered(self):
        ports = list(range(1, 21))
        sc = _scanner(ports, retries=0, reprobe_rate=5000, reprobe_concurrency=20)
        sc._attempt = self._rate_limited(sc, answer_after=1)   # 1st probe lost
        out = asyncio.run(asyncio.wait_for(sc.scan_target("127.0.0.1"), 30))
        summ = self._summary(out)
        rp = summ.data["reprobe"]
        assert rp["candidates"] == len(ports)
        assert rp["resolved"] == len(ports)      # every false `filtered` corrected
        assert rp["remaining"] == 0
        assert summ.data["filtered"] == 0
        assert summ.data["closed"] == len(ports)

    def test_genuinely_filtered_ports_stay_filtered(self):
        ports = list(range(1, 11))
        sc = _scanner(ports, retries=0, reprobe_rate=5000, reprobe_retries=1)
        sc._attempt = self._silent_attempt(sc)
        out = asyncio.run(asyncio.wait_for(sc.scan_target("127.0.0.1"), 30))
        summ = self._summary(out)
        rp = summ.data["reprobe"]
        assert rp["resolved"] == 0 and rp["remaining"] == len(ports)
        assert summ.data["filtered"] == len(ports)   # never invents a state

    def _silent_attempt(self, sc):
        async def _attempt(target, port, est=None, min_timeout=None):
            return sc._build(target, port, "filtered", "no_response", "silence")
        return _attempt

    def test_completeness_holds_after_correction(self):
        """Corrected ports must be recorded ONCE, with their final state."""
        ports = list(range(1, 31))
        sc = _scanner(ports, retries=0, reprobe_rate=5000, reprobe_concurrency=30)
        sc._attempt = self._rate_limited(sc, answer_after=1)
        out = asyncio.run(asyncio.wait_for(sc.scan_target("127.0.0.1"), 30))
        summ = self._summary(out)
        assert summ.data["ports_attempted"] == len(ports)
        assert summ.data["classified"] == len(ports)
        assert summ.data["duplicates"] == 0
        assert summ.data["missing"] == 0
        assert summ.data["complete"] is True

    def test_disabled_reprobe_leaves_false_filtered_in_place(self):
        ports = list(range(1, 11))
        sc = _scanner(ports, retries=0, reprobe=False)
        sc._attempt = self._rate_limited(sc, answer_after=1)
        out = asyncio.run(asyncio.wait_for(sc.scan_target("127.0.0.1"), 30))
        summ = self._summary(out)
        assert "reprobe" not in summ.data
        assert summ.data["filtered"] == len(ports)   # the old, wrong answer

    def test_no_ambiguous_ports_means_no_cleanup_pass(self):
        sc = _scanner([80, 443], retries=0)

        async def _closed(target, port, est=None, min_timeout=None):
            return sc._build(target, port, "closed", "connection_refused", "rst")
        sc._attempt = _closed
        out = asyncio.run(asyncio.wait_for(sc.scan_target("127.0.0.1"), 30))
        assert "reprobe" not in self._summary(out).data

    def test_cleanup_raises_the_timeout_floor(self):
        """A converged estimator can be tuned to a path that was dropping us."""
        seen = []
        sc = _scanner([80], retries=0, reprobe_rate=5000)

        async def _attempt(target, port, est=None, min_timeout=None):
            seen.append(min_timeout)
            return sc._build(target, port, "filtered", "no_response", "silence")
        sc._attempt = _attempt
        asyncio.run(asyncio.wait_for(sc.scan_target("127.0.0.1"), 30))
        assert seen[0] is None                    # main sweep: no floor
        assert any(f is not None and f >= 3.0 for f in seen[1:])

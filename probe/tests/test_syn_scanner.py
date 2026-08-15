"""
test_syn_scanner.py — stateless SYN scan (Tier 1.1).

The raw-socket send/receive path only works on privileged Linux, so it cannot
run in CI/dev here. These tests therefore cover, deterministically:
  * IP/TCP packet crafting + checksums (round-trip through the parser)
  * the stateless SYN cookie (keyed ISN) and its reply verification
  * TCP flag classification (open/closed/filtered)
  * capability detection + the connect-scan fallback decision (injected)
  * the SynScanner fallback path end-to-end against a real loopback listener
"""

from __future__ import annotations

import asyncio
import socket
import struct

from scanner import syn_scanner as ss
from scanner.scanner_base import ScopeGuard

KEY = b"0123456789abcdef"


# ── checksums ─────────────────────────────────────────────────────────────────

class TestChecksum:
    def test_checksum_of_valid_ip_header_is_zero(self):
        # A header that already contains its own correct checksum must checksum
        # back to 0 (the standard one's-complement verification property).
        hdr = ss.build_ip_header("10.0.0.1", "10.0.0.5", payload_len=20, ident=0x1234)
        assert ss._checksum(hdr) == 0

    def test_checksum_handles_odd_length(self):
        # Must pad odd-length buffers without raising.
        assert isinstance(ss._checksum(b"\x01\x02\x03"), int)

    def test_tcp_checksum_verifies_to_zero(self):
        tcp = ss.build_tcp_syn("10.0.0.1", "10.0.0.5", 50000, 443, seq=0xdeadbeef)
        pseudo = (socket.inet_aton("10.0.0.1") + socket.inet_aton("10.0.0.5") +
                  struct.pack("!BBH", 0, socket.IPPROTO_TCP, len(tcp)))
        assert ss._checksum(pseudo + tcp) == 0


# ── stateless SYN cookie ──────────────────────────────────────────────────────

class TestSynCookie:
    def test_cookie_is_deterministic(self):
        a = ss.syn_cookie("10.0.0.5", 443, 50000, KEY)
        b = ss.syn_cookie("10.0.0.5", 443, 50000, KEY)
        assert a == b

    def test_cookie_is_32_bit(self):
        c = ss.syn_cookie("10.0.0.5", 443, 50000, KEY)
        assert 0 <= c <= 0xFFFFFFFF

    def test_cookie_varies_with_port(self):
        assert ss.syn_cookie("10.0.0.5", 443, 50000, KEY) != \
               ss.syn_cookie("10.0.0.5", 80, 50000, KEY)

    def test_cookie_varies_with_key(self):
        assert ss.syn_cookie("10.0.0.5", 443, 50000, KEY) != \
               ss.syn_cookie("10.0.0.5", 443, 50000, b"different-key----")


# ── packet round-trip ─────────────────────────────────────────────────────────

class TestPacketRoundTrip:
    def test_syn_packet_parses_back_to_fields(self):
        seq = ss.syn_cookie("10.0.0.5", 443, 50000, KEY)
        pkt = ss.build_syn_packet("10.0.0.1", "10.0.0.5", 50000, 443, seq)
        p = ss.parse_packet(pkt)
        assert p["ip_src"] == "10.0.0.1"
        assert p["ip_dst"] == "10.0.0.5"
        assert p["src_port"] == 50000
        assert p["dst_port"] == 443
        assert p["seq"] == seq

    def test_syn_flag_is_set(self):
        pkt = ss.build_syn_packet("10.0.0.1", "10.0.0.5", 50000, 443, seq=1)
        p = ss.parse_packet(pkt)
        assert p["flags"] & 0x02        # SYN

    def test_ip_checksum_valid_in_full_packet(self):
        pkt = ss.build_syn_packet("10.0.0.1", "10.0.0.5", 50000, 443, seq=1)
        assert ss._checksum(pkt[:20]) == 0

    def test_parse_rejects_short_packet(self):
        assert ss.parse_packet(b"\x45" + b"\x00" * 10) is None


# ── flag classification ───────────────────────────────────────────────────────

class TestClassify:
    def test_syn_ack_is_open(self):
        assert ss.classify(0x12) == "open"       # SYN(0x02) | ACK(0x10)

    def test_rst_is_closed(self):
        assert ss.classify(0x04) == "closed"     # RST
        assert ss.classify(0x14) == "closed"     # RST | ACK

    def test_other_flags_are_none(self):
        assert ss.classify(0x10) is None         # bare ACK
        assert ss.classify(0x00) is None


# ── reply cookie verification ─────────────────────────────────────────────────

class TestVerifyReplyCookie:
    def _make_synack_reply(self, dst_ip, dst_port, src_port, seq):
        # The target replies: its src = the scanned (ip, port); ack = our seq + 1.
        ack = (seq + 1) & 0xFFFFFFFF
        tcp = struct.pack("!HHIIBBHHH",
                          dst_port, src_port, 0xAABBCCDD, ack,
                          (5 << 4), 0x12, 1024, 0, 0)
        ip = ss.build_ip_header(dst_ip, "10.0.0.1", payload_len=len(tcp))
        return ss.parse_packet(ip + tcp)

    def test_valid_cookie_verifies(self):
        seq = ss.syn_cookie("10.0.0.5", 443, 50000, KEY)
        reply = self._make_synack_reply("10.0.0.5", 443, 50000, seq)
        assert ss.verify_reply_cookie(reply, our_src_port=50000, key=KEY) is True

    def test_wrong_ack_fails(self):
        seq = ss.syn_cookie("10.0.0.5", 443, 50000, KEY)
        reply = self._make_synack_reply("10.0.0.5", 443, 50000, seq + 99)
        assert ss.verify_reply_cookie(reply, our_src_port=50000, key=KEY) is False

    def test_reply_from_other_host_fails(self):
        seq = ss.syn_cookie("10.0.0.5", 443, 50000, KEY)
        # Same ack, but the responder IP differs -> cookie recomputation misses.
        reply = self._make_synack_reply("10.0.0.9", 443, 50000, seq)
        assert ss.verify_reply_cookie(reply, our_src_port=50000, key=KEY) is False


# ── capability detection + fallback decision ──────────────────────────────────

class TestCapabilityDetection:
    def test_non_linux_is_unsupported(self):
        assert ss.syn_scan_supported(platform="darwin") is False
        assert ss.syn_scan_supported(platform="win32") is False

    def test_linux_without_privilege_is_unsupported(self):
        def _raise():
            raise PermissionError("need CAP_NET_RAW")
        assert ss.syn_scan_supported(platform="linux", socket_factory=_raise) is False

    def test_linux_with_raw_socket_is_supported(self):
        class _FakeSock:
            def close(self): pass
        assert ss.syn_scan_supported(
            platform="linux", socket_factory=lambda: _FakeSock()) is True


# ── SynScanner fallback path (real loopback) ──────────────────────────────────

class TestSynScannerFallback:
    def test_forced_fallback_builds_connect_scanner(self):
        scope = ScopeGuard.from_list(["127.0.0.0/8"])
        scanner = ss.SynScanner(scope, ports=[80], force_fallback=True)
        assert scanner._supported is False
        assert scanner._fallback is not None

    def test_fallback_detects_open_port_on_loopback(self):
        async def _run():
            server = await asyncio.start_server(
                lambda r, w: w.close(), "127.0.0.1", 0)
            port = server.sockets[0].getsockname()[1]
            scope = ScopeGuard.from_list(["127.0.0.0/8"])
            scanner = ss.SynScanner(scope, ports=[port], timeout=2.0,
                                    force_fallback=True)
            try:
                return await scanner.scan_target("127.0.0.1")
            finally:
                server.close()
                await server.wait_closed()

        results = asyncio.run(_run())
        opens = [r for r in results if r.status == "open"]
        assert len(opens) == 1
        assert opens[0].port is not None
        assert opens[0].data.get("method") == "connect_fallback"

    def test_fallback_labels_scanner_name(self):
        async def _run():
            server = await asyncio.start_server(
                lambda r, w: w.close(), "127.0.0.1", 0)
            port = server.sockets[0].getsockname()[1]
            scope = ScopeGuard.from_list(["127.0.0.0/8"])
            scanner = ss.SynScanner(scope, ports=[port], timeout=2.0,
                                    force_fallback=True)
            try:
                return await scanner.scan_target("127.0.0.1")
            finally:
                server.close()
                await server.wait_closed()

        results = asyncio.run(_run())
        assert all(r.scanner == "syn_scan" for r in results)


# ── SYN retransmit on silence (roadmap item 2) ────────────────────────────────

class TestSynRetransmit:
    """The raw SYN path resends ONLY still-silent ports — the direct fix for the
    false negatives a single dropped SYN/SYN-ACK used to manufacture. Raw sockets
    can't run here, so we inject fakes and drive `_syn_scan_blocking` directly."""

    def _patch(self, monkeypatch, recv_impl, sent_ports):
        # Fixed source port so we can craft cookie-valid replies; deterministic
        # resolve/source-IP; fake raw sockets in place of privileged ones.
        monkeypatch.setattr(ss.random, "randint", lambda a, b: 50000)
        monkeypatch.setattr(ss, "resolve",
                            lambda t, p, proto="tcp": (socket.AF_INET, (t, 0)))
        monkeypatch.setattr(ss, "_local_source_ip", lambda dst: "10.0.0.1")

        class _Send:
            def setsockopt(self, *a): pass
            def sendto(self, pkt, addr):
                sent_ports.append(ss.parse_packet(pkt)["dst_port"])
            def close(self): pass

        class _Recv:
            def setblocking(self, *a): pass
            def recv(self, n): return recv_impl()
            def close(self): pass

        def _factory(family, stype, proto):
            return _Recv() if proto == socket.IPPROTO_TCP else _Send()
        monkeypatch.setattr(ss.socket, "socket", _factory)

    def test_silent_ports_are_retried_retries_plus_one_times(self, monkeypatch):
        sent: list[int] = []

        def _silent():
            raise OSError("no data")           # ends each round's recv loop fast

        scope = ScopeGuard.from_list(["10.0.0.0/8"])
        sc = ss.SynScanner(scope, ports=[443, 8080], key=KEY, retries=2,
                           timeout=0.01)
        self._patch(monkeypatch, _silent, sent)
        sc._syn_scan_blocking("10.0.0.5")
        # 1 initial SYN + 2 retransmits = 3 per silent port.
        assert sent.count(443) == 3
        assert sent.count(8080) == 3

    def test_answered_ports_are_not_retransmitted(self, monkeypatch):
        sent: list[int] = []

        def _synack(dst_ip, port, src_port, seq):
            ack = (seq + 1) & 0xFFFFFFFF
            tcp = struct.pack("!HHIIBBHHH", port, src_port, 0xABCD, ack,
                              (5 << 4), 0x12, 1024, 0, 0)
            ip = ss.build_ip_header(dst_ip, "10.0.0.1", payload_len=len(tcp))
            return ip + tcp

        replies = []
        for port in (443, 8080):
            seq = ss.syn_cookie("10.0.0.5", port, 50000, KEY)
            replies.append(_synack("10.0.0.5", port, 50000, seq))

        def _recv():
            if replies:
                return replies.pop(0)
            raise OSError("drained")

        scope = ScopeGuard.from_list(["10.0.0.0/8"])
        sc = ss.SynScanner(scope, ports=[443, 8080], key=KEY, retries=2,
                           timeout=0.01)
        self._patch(monkeypatch, _recv, sent)
        results = sc._syn_scan_blocking("10.0.0.5")
        # Answered on round 1 -> exactly one SYN each, no retransmit.
        assert sent.count(443) == 1
        assert sent.count(8080) == 1
        assert {r.port for r in results if r.status == "open"} == {443, 8080}

    def test_retries_zero_sends_one_syn_per_port(self, monkeypatch):
        sent: list[int] = []
        scope = ScopeGuard.from_list(["10.0.0.0/8"])
        sc = ss.SynScanner(scope, ports=[22, 80], key=KEY, retries=0,
                           timeout=0.01)
        self._patch(monkeypatch, lambda: (_ for _ in ()).throw(OSError()), sent)
        sc._syn_scan_blocking("10.0.0.5")
        assert sent.count(22) == 1 and sent.count(80) == 1


class TestSynDefaults:
    def test_default_ports_are_nmap_top100(self):
        from scanner.port_scanner import _NMAP_TOP_100
        scope = ScopeGuard.from_list(["10.0.0.0/8"])
        sc = ss.SynScanner(scope, force_fallback=True)
        assert sc.ports == list(_NMAP_TOP_100)
        assert len(sc.ports) == 100

    def test_default_retries_is_two(self):
        scope = ScopeGuard.from_list(["10.0.0.0/8"])
        sc = ss.SynScanner(scope, ports=[80], force_fallback=True)
        assert sc.retries == 2


# ── TCP option (MSS) parsing ──────────────────────────────────────────────────

class TestOptionParsing:
    def test_mss_extracted(self):
        assert ss._parse_mss(b"\x02\x04\x05\xb4") == 1460          # kind2 len4 1460

    def test_mss_after_nop_padding(self):
        assert ss._parse_mss(b"\x01\x01\x02\x04\x05\xb4") == 1460  # NOP NOP MSS

    def test_mss_skips_other_options(self):
        # window-scale (3,3,x) then MSS — must step over by length, not misread.
        assert ss._parse_mss(b"\x03\x03\x08\x02\x04\x05\xb4") == 1460

    def test_mss_absent_returns_none(self):
        assert ss._parse_mss(b"\x03\x03\x08") is None              # no MSS

    def test_malformed_options_never_raise(self):
        assert ss._parse_mss(b"\x02") is None                      # truncated kind
        assert ss._parse_mss(b"\x02\x00") is None                  # bogus length
        assert ss._parse_mss(b"\x02\x04\x05") is None              # short value
        assert ss._parse_mss(b"") is None
        assert ss._parse_mss(b"\x00\x02\x04\x05\xb4") is None      # EOL ends walk


def _synack_with_options(dst_ip, dst_port, src_port, *, ttl=64, window=65535,
                         mss=1460):
    """A SYN/ACK carrying an MSS option (data offset 6 = 24-byte TCP header)."""
    opt = b"\x02\x04" + int(mss).to_bytes(2, "big")
    tcp = struct.pack("!HHIIBBHHH", dst_port, src_port, 0xAABBCCDD, 1,
                      (6 << 4), 0x12, window, 0, 0) + opt
    ip = ss.build_ip_header(dst_ip, "10.0.0.1", payload_len=len(tcp), ttl=ttl)
    return ip + tcp


class TestParsePacketSignals:
    def test_window_ttl_mss_surfaced(self):
        p = ss.parse_packet(_synack_with_options("10.0.0.5", 443, 50000,
                                                 ttl=128, window=8192, mss=1460))
        assert p["window"] == 8192 and p["ttl"] == 128 and p["mss"] == 1460

    def test_no_options_gives_none_mss(self):
        p = ss.parse_packet(ss.build_syn_packet("10.0.0.1", "10.0.0.5", 50000, 443, 1))
        assert p["mss"] is None and p["window"] == 1024     # build default window


# ── result enrichment: harvested stack signals + OS guess ─────────────────────

class TestBuildResultsEnrichment:
    def _scanner(self, ports, **kw):
        scope = ScopeGuard.from_list(["10.0.0.0/8"])
        return ss.SynScanner(scope, ports=ports, force_fallback=True, **kw)

    def test_open_result_carries_signals_and_os_guess(self):
        sc = self._scanner([80])
        meta = {80: {"rtt_ms": 12.5, "tcp_window": 65535, "ip_ttl": 64, "mss": 1460}}
        r = sc._build_results("10.0.0.5", {80: "open"}, {80: 1}, meta)[0]
        assert r.data["tcp_window"] == 65535 and r.data["ip_ttl"] == 64
        assert r.data["mss"] == 1460 and r.data["rtt_ms"] == 12.5
        assert r.data["os_guess"] == "Linux/Unix/macOS"      # TTL 64 -> Linux
        assert 0.0 < r.data["os_confidence"] <= 1.0
        assert r.rtt_ms == 12.5                              # promoted to a field

    def test_windows_ttl_maps_to_windows(self):
        sc = self._scanner([3389])
        d = sc._build_results("10.0.0.5", {3389: "open"}, {3389: 1},
                              {3389: {"ip_ttl": 128, "tcp_window": 8192}})[0].data
        assert d["os_guess"] == "Windows"

    def test_open_without_signals_has_no_os_guess(self):
        sc = self._scanner([80])
        d = sc._build_results("10.0.0.5", {80: "open"}, {80: 1}, {})[0].data
        assert "os_guess" not in d and "tcp_window" not in d

    def test_closed_and_filtered_suppressed_by_default(self):
        sc = self._scanner([80, 443, 22])
        out = sc._build_results("10.0.0.5", {80: "open", 443: "closed"},
                                {80: 1, 443: 1, 22: 3}, {})
        assert {r.port for r in out} == {80}                 # only open emitted


class TestAdaptiveTimeoutToggle:
    def test_adaptive_on_by_default(self):
        scope = ScopeGuard.from_list(["10.0.0.0/8"])
        assert ss.SynScanner(scope, force_fallback=True).adaptive_timeout is True

    def test_can_disable(self):
        scope = ScopeGuard.from_list(["10.0.0.0/8"])
        assert ss.SynScanner(scope, force_fallback=True,
                             adaptive_timeout=False).adaptive_timeout is False

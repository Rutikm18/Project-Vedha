"""
test_os_fingerprint.py — Tier 2.1 (OS fingerprinting) + 2.2 (ICMP multi-probe + TTL).

The raw/ICMP socket I/O can't run portably in CI, so these cover the pure logic:
  * ICMP echo/timestamp/address-mask packet construction + checksums
  * ICMP reply parsing incl. TTL extraction from the IP header
  * initial-TTL inference (round up to 64/128/255) and OS-family mapping
  * multi-signal OS fingerprint scoring (TTL + TCP window + MSS)
"""

from __future__ import annotations

import asyncio
import struct

import pytest

from scanner import os_fingerprint as ofp
from scanner.scanner_base import inet_checksum, ScopeGuard


# ── shared checksum ───────────────────────────────────────────────────────────

class TestInetChecksum:
    def test_checksum_verifies_to_zero(self):
        body = struct.pack("!BBHHH", 8, 0, 0, 0x1234, 1) + b"payload!!"
        chk = inet_checksum(body)
        full = struct.pack("!BBHHH", 8, 0, chk, 0x1234, 1) + b"payload!!"
        assert inet_checksum(full) == 0

    def test_checksum_handles_odd_length(self):
        assert isinstance(inet_checksum(b"\x01\x02\x03"), int)


# ── ICMP packet construction ──────────────────────────────────────────────────

class TestIcmpBuilders:
    def test_echo_request_type_and_checksum(self):
        pkt = ofp.build_icmp_echo(0xABCD, 1, payload=b"vedha")
        typ, code, _chk, ident, seq = struct.unpack("!BBHHH", pkt[:8])
        assert typ == 8 and code == 0
        assert ident == 0xABCD and seq == 1
        assert inet_checksum(pkt) == 0        # embedded checksum is valid

    def test_echo_payload_preserved(self):
        pkt = ofp.build_icmp_echo(1, 1, payload=b"PING-DATA")
        assert pkt.endswith(b"PING-DATA")

    def test_timestamp_request_type(self):
        pkt = ofp.build_icmp_timestamp(0x11, 2)
        assert pkt[0] == 13                    # ICMP timestamp request
        assert inet_checksum(pkt) == 0

    def test_address_mask_request_type(self):
        pkt = ofp.build_icmp_addrmask(0x22, 3)
        assert pkt[0] == 17                    # ICMP address-mask request
        assert inet_checksum(pkt) == 0


# ── ICMP reply parsing ────────────────────────────────────────────────────────

class TestIcmpParse:
    def _ip_icmp(self, ttl, icmp_type):
        from scanner.syn_scanner import build_ip_header
        icmp = struct.pack("!BBHHH", icmp_type, 0, 0, 0x1234, 1)
        chk = inet_checksum(icmp)
        icmp = struct.pack("!BBHHH", icmp_type, 0, chk, 0x1234, 1)
        ip = build_ip_header("10.0.0.5", "10.0.0.1", payload_len=len(icmp),
                             ttl=ttl, proto=1)
        return ip + icmp

    def test_parse_extracts_ttl_and_type(self):
        pkt = self._ip_icmp(ttl=57, icmp_type=0)   # echo reply
        parsed = ofp.parse_icmp_reply(pkt)
        assert parsed["type"] == 0
        assert parsed["ttl"] == 57
        assert parsed["id"] == 0x1234

    def test_parse_rejects_short(self):
        assert ofp.parse_icmp_reply(b"\x45\x00") is None

    def test_parse_raw_icmp_without_ip_header(self):
        # SOCK_DGRAM ICMP may deliver ICMP without the IP header -> ttl is None.
        icmp = struct.pack("!BBHHH", 0, 0, 0, 0x1234, 1)
        chk = inet_checksum(icmp)
        icmp = struct.pack("!BBHHH", 0, 0, chk, 0x1234, 1)
        parsed = ofp.parse_icmp_reply(icmp)
        assert parsed is not None
        assert parsed["type"] == 0
        assert parsed["ttl"] is None


# ── ICMP timestamp probe (type 13/14): echo-filter bypass + clock harvest ─────

class TestIcmpTimestamps:
    def _ts_reply(self, transmit, *, ttl=57, with_ip=True):
        body = struct.pack("!BBHHHIII", 14, 0, 0, 0x1234, 1, 0, 0, transmit)
        chk = inet_checksum(body)
        icmp = struct.pack("!BBHHHIII", 14, 0, chk, 0x1234, 1, 0, 0, transmit)
        if not with_ip:
            return icmp
        from scanner.syn_scanner import build_ip_header
        ip = build_ip_header("10.0.0.5", "10.0.0.1", payload_len=len(icmp),
                             ttl=ttl, proto=1)
        return ip + icmp

    def test_parse_extracts_ttl_and_transmit(self):
        parsed = ofp.parse_icmp_timestamps(self._ts_reply(3_723_004, ttl=57))
        assert parsed["type"] == 14
        assert parsed["ttl"] == 57
        assert parsed["transmit"] == 3_723_004

    def test_parse_datagram_delivery_has_no_ttl(self):
        parsed = ofp.parse_icmp_timestamps(self._ts_reply(1234, with_ip=False))
        assert parsed is not None and parsed["ttl"] is None
        assert parsed["transmit"] == 1234

    def test_parse_rejects_short_body(self):
        # An 8-byte echo body is too short to be a 20-byte timestamp message.
        assert ofp.parse_icmp_timestamps(struct.pack("!BBHHH", 14, 0, 0, 1, 1)) is None


class TestRemoteClock:
    def test_standard_value_decodes_to_wall_clock(self):
        # 01:02:03.004 since UTC midnight.
        ms = ((1 * 3600 + 2 * 60 + 3) * 1000) + 4
        clock = ofp.remote_clock(ms)
        assert clock["standard"] is True
        assert clock["utc_time"] == "01:02:03.004"
        assert clock["ms_since_utc_midnight"] == ms

    def test_high_bit_marks_nonstandard_clock(self):
        clock = ofp.remote_clock(0x80000000 | 5)
        assert clock["standard"] is False
        assert "utc_time" not in clock


class TestTimestampFallback:
    def _scanner(self):
        return ofp.OSFingerprintScanner(
            ScopeGuard.from_list(["10.0.0.0/8"]),
            rate=1e9, concurrency=4, timeout=0.1)

    def test_timestamp_reply_when_echo_is_filtered(self):
        sc = self._scanner()
        sc._icmp_echo_ttl = lambda target: "down"          # echo filtered
        sc._icmp_timestamp = lambda target: {"ttl": 57, "transmit": 3_723_004}
        res = asyncio.run(sc.scan_target("10.0.0.9"))
        assert len(res) == 1
        r = res[0]
        assert r.status == "open" and r.data["alive"] is True
        assert r.data["via"] == "icmp_timestamp"
        assert r.data["icmp_echo_reply"] is False
        assert r.data["icmp_timestamp_reply"] is True
        assert r.data["remote_clock"]["utc_time"] == "01:02:03.004"
        assert r.data["os_guess"] == "Linux/Unix/macOS"    # ttl 57 -> initial 64

    def test_both_filtered_reports_no_reply(self):
        sc = self._scanner()
        sc._icmp_echo_ttl = lambda target: "down"
        sc._icmp_timestamp = lambda target: "down"
        res = asyncio.run(sc.scan_target("10.0.0.9"))
        assert res[0].status == "filtered"
        assert res[0].data["icmp_timestamp_reply"] is False


# ── reply-source validation (wrong-host misattribution guard) ─────────────────

class TestAcceptEchoReply:
    def _reply(self, type_=0):
        return {"type": type_, "code": 0, "id": 1, "seq": 1, "ttl": 60}

    def test_accepts_echo_reply_from_target(self):
        assert ofp.accept_echo_reply("10.0.0.5", self._reply(0), "10.0.0.5") is True

    def test_rejects_reply_from_a_different_host(self):
        # a neighbour's reply arriving on a shared/raw ICMP socket must be dropped
        assert ofp.accept_echo_reply("10.0.0.9", self._reply(0), "10.0.0.5") is False

    def test_rejects_non_echo_type(self):
        assert ofp.accept_echo_reply("10.0.0.5", self._reply(3), "10.0.0.5") is False

    def test_rejects_none_parsed(self):
        assert ofp.accept_echo_reply("10.0.0.5", None, "10.0.0.5") is False

    def test_accepts_when_source_unknown(self):
        assert ofp.accept_echo_reply(None, self._reply(0), "10.0.0.5") is True


# ── TTL inference ─────────────────────────────────────────────────────────────

class TestTtlInference:
    def test_round_up_to_64(self):
        assert ofp.infer_initial_ttl(57) == 64
        assert ofp.infer_initial_ttl(64) == 64

    def test_round_up_to_128(self):
        assert ofp.infer_initial_ttl(120) == 128
        assert ofp.infer_initial_ttl(128) == 128

    def test_round_up_to_255(self):
        assert ofp.infer_initial_ttl(250) == 255
        assert ofp.infer_initial_ttl(255) == 255

    def test_hop_estimate(self):
        assert ofp.hop_estimate(57) == 7       # 64 - 57
        assert ofp.hop_estimate(120) == 8      # 128 - 120

    def test_os_family_linux(self):
        assert "Linux" in ofp.os_family_from_ttl(64)

    def test_os_family_windows(self):
        assert ofp.os_family_from_ttl(128) == "Windows"

    def test_os_family_network(self):
        assert "Network" in ofp.os_family_from_ttl(255)

    def test_os_family_unknown_on_none(self):
        assert ofp.os_family_from_ttl(None) == "unknown"


# ── multi-signal OS fingerprint ───────────────────────────────────────────────

class TestFingerprintOs:
    def test_ttl_only_linux(self):
        r = ofp.fingerprint_os(ttl=57)
        assert r["os_guess"].startswith("Linux")
        assert r["signals"]["initial_ttl"] == 64

    def test_ttl_only_windows(self):
        assert ofp.fingerprint_os(ttl=120)["os_guess"] == "Windows"

    def test_ttl_and_window_agree_boosts_confidence(self):
        low = ofp.fingerprint_os(ttl=64)
        high = ofp.fingerprint_os(ttl=64, tcp_window=29200)
        assert high["os_guess"].startswith("Linux")
        assert high["confidence"] >= low["confidence"]

    def test_no_signals_is_unknown(self):
        r = ofp.fingerprint_os()
        assert r["os_guess"] == "unknown"
        assert r["confidence"] == 0.0

    def test_network_device_from_ttl_255(self):
        assert "Network" in ofp.fingerprint_os(ttl=250)["os_guess"]

    def test_signals_recorded(self):
        r = ofp.fingerprint_os(ttl=64, tcp_window=8192, mss=1460)
        assert r["signals"]["tcp_window"] == 8192
        assert r["signals"]["mss"] == 1460

    def test_mss_yields_ethernet_mtu(self):
        s = ofp.fingerprint_os(ttl=64, mss=1460)["signals"]
        assert s["mtu"] == 1500 and s["link_hint"] == "ethernet"

    def test_mss_flags_tunnel_or_vpn(self):
        s = ofp.fingerprint_os(ttl=64, mss=1380)["signals"]
        assert s["mtu"] == 1420 and s["link_hint"] == "tunnel_or_vpn"

    def test_mss_flags_jumbo_even_without_os_signal(self):
        assert ofp.fingerprint_os(mss=8960)["signals"]["link_hint"] == "jumbo"

    def test_mss_is_path_intel_not_an_os_signal(self):
        # a reduced MSS must not change the OS guess — it still tracks TTL
        assert ofp.fingerprint_os(ttl=120, mss=1380)["os_guess"] == "Windows"

    def test_ttl_source_recorded_when_provided(self):
        # A TCP-derived TTL must be traceable as such — never presentable as ICMP.
        s = ofp.fingerprint_os(ttl=120, ttl_source="tcp_synack")["signals"]
        assert s["ttl_source"] == "tcp_synack"
        assert s["observed_ttl"] == 120

    def test_ttl_source_defaults_to_unspecified(self):
        assert ofp.fingerprint_os(ttl=64)["signals"]["ttl_source"] == "unspecified"

    def test_no_ttl_means_no_ttl_source(self):
        # window-only guess carries no TTL, so it must not claim a TTL provenance.
        assert "ttl_source" not in ofp.fingerprint_os(tcp_window=8192)["signals"]


# ── p0f-style TCP/IP stack fingerprint (option layout + TTL + wscale) ─────────

class TestStackSignature:
    def test_windows_8_plus_from_option_layout(self):
        # ttl 128 + Windows SYN/ACK layout (MSS,NOP,WScale,NOP,NOP,SACKOK) + ws 8.
        r = ofp.match_stack_signature(ttl=128, mss=1460, window=64240,
                                      wscale=8, olayout="MNWNNS")
        assert "Windows (NT 6.2+" in r["stack"]
        assert r["stack_confidence"] == 0.90
        assert r["stack_source"] == "p0f_tcp_options"

    def test_windows_layout_without_wscale_is_lower_confidence(self):
        r = ofp.match_stack_signature(ttl=128, olayout="MNWNNS")
        assert "Windows" in r["stack"] and r["stack_confidence"] == 0.80

    def test_linux_from_option_layout_and_wscale(self):
        r = ofp.match_stack_signature(ttl=64, mss=1460, wscale=7, olayout="MSTNW")
        assert "Linux (kernel 3.11+" in r["stack"] and r["stack_confidence"] == 0.90

    def test_macos_darwin_layout(self):
        r = ofp.match_stack_signature(ttl=64, olayout="MNWNNTSE")
        assert "Darwin" in r["stack"]

    def test_ttl255_matches_embedded_regardless_of_layout(self):
        r = ofp.match_stack_signature(ttl=250, olayout="ANYTHING")
        assert "embedded" in r["stack"].lower()

    def test_unknown_layout_yields_no_stack(self):
        # a TTL-64 host whose layout matches no signature → honest None, not a guess
        assert ofp.match_stack_signature(ttl=64, olayout="XYZ") is None

    def test_no_ttl_yields_no_stack(self):
        assert ofp.match_stack_signature(olayout="MNWNNS") is None

    def test_fingerprint_os_folds_in_stack_but_keeps_family(self):
        r = ofp.fingerprint_os(ttl=128, tcp_window=64240, mss=1460, wscale=8,
                               olayout="MNWNNS", ttl_source="tcp_synack")
        assert r["os_guess"] == "Windows"                    # coarse family unchanged
        assert "Windows (NT 6.2+" in r["stack_guess"]        # refined stack added
        assert r["signals"]["stack_source"] == "p0f_tcp_options"

    def test_fingerprint_os_stack_guess_none_without_options(self):
        assert ofp.fingerprint_os(ttl=64)["stack_guess"] is None


# ── SMB2 NTLM build enrichment (standalone os_fingerprint gets the exact build) ─

class TestSmbBuildEnrichment:
    def _scanner(self, **kw):
        return ofp.OSFingerprintScanner(
            ScopeGuard.from_list(["10.0.0.0/8"]), rate=1e9, concurrency=2,
            timeout=0.1, **kw)

    def test_build_lifts_ttl_only_guess_to_authoritative(self, monkeypatch):
        from scanner import smb_scanner as SMB
        sc = self._scanner()
        sc._icmp_echo_ttl = lambda t: 128          # Windows TTL — 0.5 on its own
        monkeypatch.setattr(SMB, "ntlm_os_build", lambda ip, port=445, timeout=5.0: {
            "os_build": 26100, "os_release": "Windows 11 24H2",
            "os_version": "10.0.26100", "target_name": "DESKTOP-34M18MB",
            "os_confidence": 0.97, "method": "smb2_ntlm_version"})
        monkeypatch.setattr(ofp, "resolve", lambda t, p, proto="tcp": (2, (t, p)))
        r = asyncio.run(sc.scan_target("10.0.0.9"))[0]
        assert r.data["os_build"] == 26100
        assert r.data["os_release"] == "Windows 11 24H2"
        assert r.data["confidence"] >= 0.95           # no longer stuck at 0.5
        assert r.data["hostname"] == "DESKTOP-34M18MB"
        assert "smb2_ntlm_version" in r.method        # provenance kept, incl. icmp_echo

    def test_no_smb_leaves_ttl_only_result_untouched(self, monkeypatch):
        from scanner import smb_scanner as SMB
        sc = self._scanner()
        sc._icmp_echo_ttl = lambda t: 128
        monkeypatch.setattr(SMB, "ntlm_os_build", lambda ip, port=445, timeout=5.0: {})
        monkeypatch.setattr(ofp, "resolve", lambda t, p, proto="tcp": (2, (t, p)))
        r = asyncio.run(sc.scan_target("10.0.0.9"))[0]
        assert "os_build" not in r.data and r.method == "icmp_echo"
        assert r.data["confidence"] == 0.5

    def test_smb_build_can_be_disabled(self):
        sc = self._scanner(smb_build=False)
        sc._icmp_echo_ttl = lambda t: 128
        r = asyncio.run(sc.scan_target("10.0.0.9"))[0]
        assert "os_build" not in r.data


# ── OS-claim provenance (never label a TCP TTL as ICMP) ───────────────────────

class TestProvenance:
    def _scanner(self):
        return ofp.OSFingerprintScanner(
            ScopeGuard.from_list(["10.0.0.0/8"]), rate=1e9, concurrency=4, timeout=0.1)

    def test_real_echo_reply_is_method_icmp_echo(self):
        sc = self._scanner()
        sc._icmp_echo_ttl = lambda target: 120           # raw socket delivered a TTL
        r = asyncio.run(sc.scan_target("10.0.0.9"))[0]
        assert r.method == "icmp_echo"
        assert r.data["icmp_echo_reply"] is True
        assert r.data["signals"]["ttl_source"] == "icmp_echo"
        assert "ICMP echo reply ttl=120" in r.evidence

    def test_datagram_echo_without_ttl_does_not_fake_a_ttl(self):
        sc = self._scanner()
        sc._icmp_echo_ttl = lambda target: None          # datagram: alive, no TTL
        r = asyncio.run(sc.scan_target("10.0.0.9"))[0]
        assert r.method == "icmp_echo" and r.data["alive"] is True
        assert r.data["observed_ttl"] is None
        # No fabricated "ttl=128"; evidence is explicit the TTL was unobservable.
        assert "no TTL" in r.evidence
        assert "ttl_source" not in r.data.get("signals", {})

    def test_icmp_unavailable_tcp_hints_is_method_tcp_hints_not_icmp(self):
        sc = ofp.OSFingerprintScanner(
            ScopeGuard.from_list(["10.0.0.0/8"]), rate=1e9, concurrency=4,
            timeout=0.1, tcp_hints={"10.0.0.9": {"tcp_window": 8192}})
        sc._icmp_echo_ttl = lambda target: "unavailable"
        r = asyncio.run(sc.scan_target("10.0.0.9"))[0]
        assert r.method == "tcp_hints"
        assert r.data["icmp"] == "unavailable"
        assert r.data.get("icmp_reply") is not True      # never claim an ICMP reply

    def test_timestamp_reply_tags_ttl_source(self):
        sc = self._scanner()
        sc._icmp_echo_ttl = lambda target: "down"
        sc._icmp_timestamp = lambda target: {"ttl": 57, "transmit": 3_723_004}
        r = asyncio.run(sc.scan_target("10.0.0.9"))[0]
        assert r.method == "icmp_timestamp"
        assert r.data["signals"]["ttl_source"] == "icmp_timestamp"

    def test_no_icmp_but_tcp_ttl_hint_is_method_tcp_ttl(self):
        # FIX 3b: host filters ICMP (echo+timestamp silent) but a TCP SYN/ACK gave a
        # TTL. Must report method=tcp_ttl and NEVER claim an ICMP echo.
        sc = ofp.OSFingerprintScanner(
            ScopeGuard.from_list(["10.0.0.0/8"]), rate=1e9, concurrency=4, timeout=0.1,
            tcp_hints={"10.0.0.9": {"ttl": 128, "tcp_window": 64240, "mss": 1460}})
        sc._icmp_echo_ttl = lambda target: "down"
        sc._icmp_timestamp = lambda target: "down"
        r = asyncio.run(sc.scan_target("10.0.0.9"))[0]
        assert r.method == "tcp_ttl"
        assert r.data["icmp_echo_reply"] is False and r.data["alive"] is True
        assert r.data["os_guess"] == "Windows"
        assert r.data["signals"]["ttl_source"] == "tcp_synack"

    def test_icmp_unavailable_with_tcp_ttl_is_tcp_ttl_not_icmp(self):
        sc = ofp.OSFingerprintScanner(
            ScopeGuard.from_list(["10.0.0.0/8"]), rate=1e9, concurrency=4, timeout=0.1,
            tcp_hints={"10.0.0.9": {"ttl": 64}})
        sc._icmp_echo_ttl = lambda target: "unavailable"
        r = asyncio.run(sc.scan_target("10.0.0.9"))[0]
        assert r.method == "tcp_ttl" and r.data.get("icmp_reply") is False


# ── capability detection ──────────────────────────────────────────────────────

class TestIcmpCapability:
    def test_unavailable_when_socket_raises(self):
        def _raise():
            raise PermissionError("no icmp")
        assert ofp.icmp_supported(socket_factory=_raise) is False

    def test_available_when_socket_ok(self):
        class _S:
            def close(self): pass
        assert ofp.icmp_supported(socket_factory=lambda: _S()) is True

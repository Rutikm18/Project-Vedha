"""
test_os_fingerprint.py — Tier 2.1 (OS fingerprinting) + 2.2 (ICMP multi-probe + TTL).

The raw/ICMP socket I/O can't run portably in CI, so these cover the pure logic:
  * ICMP echo/timestamp/address-mask packet construction + checksums
  * ICMP reply parsing incl. TTL extraction from the IP header
  * initial-TTL inference (round up to 64/128/255) and OS-family mapping
  * multi-signal OS fingerprint scoring (TTL + TCP window + MSS)
"""

from __future__ import annotations

import struct

import pytest

from scanner import os_fingerprint as ofp
from scanner.scanner_base import inet_checksum


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

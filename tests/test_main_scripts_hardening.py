"""
test_main_scripts_hardening.py — verifies the Phase-1 correctness fixes applied
to probe/main_scripts/ (the tree selected for this hardening pass).

These import main_scripts.* directly (probe/ is on sys.path via conftest) because
the standard suite targets the parallel scanner.* tree. Pure-logic + raw-packet
fixture based — no live network, no privileges required.

Covers:
  * Step 14/15 — UDP state model: silence => open|filtered (NOT filtered);
                 ICMP port-unreachable => closed.
  * Step 21    — OS confidence: a single TTL signal is a hint, never absolute 1.0;
                 corroborating signals raise (but never max) confidence.
  * Step 12/13 — SMB2 negotiate parsing: an SMB2 *error* body must not be mined
                 for signing/dialect (the 0x0000 bug); a successful NEGOTIATE is
                 decoded into signing_supported / signing_required / dialect; and
                 the request must not offer 3.1.1 without a preauth context.
"""
from __future__ import annotations

import asyncio
import struct

import pytest

from main_scripts import os_fingerprint as ms_os
from main_scripts import smb_scanner as ms_smb
from main_scripts import udp_scanner as ms_udp
from main_scripts.scanner_base import ScopeGuard, _UDP_CLOSED


def _scope() -> ScopeGuard:
    return ScopeGuard.from_list(["127.0.0.0/8"])


def _run(coro):
    return asyncio.run(coro)


# ── Step 14/15: UDP state model ───────────────────────────────────────────────

class TestUdpStateModel:
    def _scanner(self):
        return ms_udp.UDPScanner(_scope())

    def test_silence_is_open_filtered_not_filtered(self):
        sc = self._scanner()

        async def _silent(*a, **k):
            return None

        sc._gated_probe = _silent
        res = _run(sc._probe("127.0.0.1", 123))  # 123 = NTP, present in UDP_PROBES
        assert res is not None
        # The bug: silence was reported as a definitive "filtered".
        assert res.status == "open|filtered", f"silence must be ambiguous, got {res.status!r}"
        assert res.data.get("reason") == "no_response"
        assert res.data.get("responded") is False

    def test_icmp_port_unreachable_is_closed(self):
        sc = self._scanner()

        async def _closed(*a, **k):
            return _UDP_CLOSED

        sc._gated_probe = _closed
        res = _run(sc._probe("127.0.0.1", 123))
        assert res.status == "closed"


# ── Step 21: OS fingerprint confidence ────────────────────────────────────────

class TestOsConfidence:
    def test_ttl_only_is_not_absolute(self):
        res = ms_os.fingerprint_os(ttl=128)
        assert res["os_guess"] == "Windows"
        assert res["confidence"] < 1.0, "a lone TTL must never yield absolute certainty"
        assert res["confidence"] <= 0.5, "single signal is a hint, capped at medium"
        assert "initial_ttl" in res["signals"]

    def test_two_signals_beat_one(self):
        one = ms_os.fingerprint_os(ttl=128)["confidence"]
        two = ms_os.fingerprint_os(ttl=128, tcp_window=8192)["confidence"]
        assert two > one, "corroborating signals must raise confidence"
        assert two < 1.0, "still never absolute from stack heuristics"

    def test_no_signal_is_unknown(self):
        res = ms_os.fingerprint_os()
        assert res["os_guess"] == "unknown"
        assert res["confidence"] == 0.0

    def test_linux_ttl_only_capped(self):
        res = ms_os.fingerprint_os(ttl=64)
        assert res["os_guess"] == "Linux/Unix/macOS"
        assert res["confidence"] <= 0.5


# ── Step 12/13: SMB2 negotiate parsing ────────────────────────────────────────

def _smb2_header(status: int, command: int = 0x0000) -> bytes:
    """A 64-byte SMB2 header. Caller prepends a 4-byte NBT transport prefix, so
    ProtocolId lands at absolute offset 4 (as it does on the wire)."""
    h = b"\xfeSMB"                    # abs 4  ProtocolId
    h += struct.pack("<H", 64)        # abs 8  StructureSize
    h += b"\x00\x00"                  # abs 10 CreditCharge
    h += struct.pack("<I", status)    # abs 12 Status
    h += struct.pack("<H", command)   # abs 16 Command
    h += b"\x00" * (68 - 18)          # abs 18..68 rest of header
    assert len(h) == 64
    return h


def make_smb2_success(security_mode: int, dialect: int) -> bytes:
    nbt = b"\x00\x00\x00\x00"
    body = (struct.pack("<H", 65) +          # abs 68 body StructureSize (success)
            struct.pack("<H", security_mode) +  # abs 70 SecurityMode
            struct.pack("<H", dialect) +        # abs 72 DialectRevision
            b"\x00" * 40)
    return nbt + _smb2_header(0x00000000) + body


def make_smb2_error(status: int = 0xC000000D) -> bytes:
    """STATUS_INVALID_PARAMETER error response: same header, body StructureSize 9,
    no SecurityMode/DialectRevision. This is what Windows returns to a bare 3.1.1
    negotiate and what produced the 0x0000 / false-signing bug."""
    nbt = b"\x00\x00\x00\x00"
    body = struct.pack("<H", 9) + b"\x00" * 8
    return nbt + _smb2_header(status) + body


class TestSmbParsing:
    def test_error_response_not_trusted(self):
        out = ms_smb.parse_smb2_security_mode(make_smb2_error())
        assert out["signing_parsed"] is False, "error body must not be mined for signing"
        # Must not fabricate signing state or a 0x0000 dialect from the error body.
        assert out.get("signing_supported") in (None, False)
        assert out.get("negotiated_dialect") is None

    def test_success_response_signing_and_dialect(self):
        # SecurityMode 0x0003 = signing supported (bit0) + required (bit1).
        out = ms_smb.parse_smb2_security_mode(make_smb2_success(0x0003, 0x0302))
        assert out["signing_parsed"] is True
        assert out["signing_supported"] is True
        assert out["signing_required"] is True
        assert out["negotiated_dialect"] == "0x0302"

    def test_success_signing_supported_not_required(self):
        out = ms_smb.parse_smb2_security_mode(make_smb2_success(0x0001, 0x0300))
        assert out["signing_supported"] is True
        assert out["signing_required"] is False

    def test_negotiate_request_offers_smb311_with_preauth_context(self):
        # FIX 4: offer 3.1.1 (MS-SMB2 3.3.5.4 — server picks the greatest common
        # dialect) AND carry the mandatory preauth-integrity context so Windows
        # returns a valid negotiate rather than STATUS_INVALID_PARAMETER.
        req = ms_smb._smb2_negotiate()
        count = struct.unpack_from("<H", req, 64 + 2)[0]      # body DialectCount
        dialects = [struct.unpack_from("<H", req, 64 + 36 + 2 * i)[0]
                    for i in range(count)]
        assert 0x0311 in dialects and 0x0302 in dialects, dialects

        ctx_count = struct.unpack_from("<H", req, 64 + 32)[0]  # NegotiateContextCount
        ctx_off = struct.unpack_from("<I", req, 64 + 28)[0]    # NegotiateContextOffset
        assert ctx_count == 2 and ctx_off % 8 == 0
        # A SMB2_PREAUTH_INTEGRITY_CAPABILITIES context (type 0x0001) must be present.
        first_ctx_type = struct.unpack_from("<H", req, ctx_off)[0]
        assert first_ctx_type == 0x0001

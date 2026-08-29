"""
test_smb_ntlm_build.py — Card 5: exact Windows build from the SMB2 pre-auth
NTLMSSP CHALLENGE (Type-2) Version field.

Pure builders/parsers only — no network. A synthesized NTLMSSP CHALLENGE stands
in for the wire response; the live SESSION_SETUP path is a lab follow-up (needs a
real SMB2 host), mirroring how the other protocol scanners are unit-tested.
"""
from __future__ import annotations

import struct

from scanner import smb_scanner as S


def _challenge(major: int, minor: int, build: int, *, with_version: bool = True,
               target_name: str = "DESKTOP-34M18MB", wrap: bytes = b"") -> bytes:
    """Synthesize an NTLMSSP CHALLENGE (Type-2). TargetName payload sits right after
    the 8-byte Version field, i.e. at offset 56. `wrap` prepends bytes to prove the
    parser locates the signature inside a larger (SPNEGO) buffer."""
    tn = target_name.encode("utf-16-le")
    flags = 0x00000001 | (S.NTLMSSP_NEGOTIATE_VERSION if with_version else 0)
    payload_off = 56 if with_version else 48
    msg = bytearray()
    msg += S.NTLMSSP_SIG                                    # 0  signature
    msg += struct.pack("<I", 2)                             # 8  MessageType = 2
    msg += struct.pack("<HHI", len(tn), len(tn), payload_off)  # 12 TargetName fields
    msg += struct.pack("<I", flags)                        # 20 NegotiateFlags
    msg += b"\x11" * 8                                      # 24 ServerChallenge
    msg += b"\x00" * 8                                      # 32 Reserved
    msg += struct.pack("<HHI", 0, 0, 0)                    # 40 TargetInfo fields
    if with_version:
        msg += bytes([major, minor]) + struct.pack("<H", build) + b"\x00\x00\x00" + bytes([0x0f])
    msg += tn                                               # payload
    return bytes(wrap) + bytes(msg)


class TestParseChallenge:
    def test_win11_24h2_build_26100(self):
        # The reference target: DESKTOP-34M18MB, Win 11 24H2, build 26100.
        r = S.parse_ntlm_challenge(_challenge(10, 0, 26100,
                                              wrap=b"\x00\x00spnego-wrapper"))
        assert r["os_build"] == 26100
        assert r["os_release"] == "Windows 11 24H2"
        assert r["os_release_alt"] == "Windows Server 2025"   # shared build; SKU disambiguates
        assert r["os_confidence"] >= 0.95
        assert r["method"] == "smb2_ntlm_version"
        assert r["os_version"] == "10.0.26100"
        assert r["target_name"] == "DESKTOP-34M18MB"

    def test_win10_22h2(self):
        r = S.parse_ntlm_challenge(_challenge(10, 0, 19045))
        assert r["os_release"] == "Windows 10 22H2" and "os_release_alt" not in r

    def test_server_2022_build_20348(self):
        r = S.parse_ntlm_challenge(_challenge(10, 0, 20348))
        assert r["os_release"] == "Windows Server 2022"

    def test_unknown_build_still_classified_win11_vs_win10(self):
        assert S.parse_ntlm_challenge(_challenge(10, 0, 25999))["os_release"].startswith("Windows 11")
        assert S.parse_ntlm_challenge(_challenge(10, 0, 12345))["os_release"].startswith("Windows 10")

    def test_legacy_6_1_is_win7(self):
        assert "Windows 7" in S.parse_ntlm_challenge(_challenge(6, 1, 7601))["os_release"]

    def test_no_version_field_yields_name_but_no_build(self):
        r = S.parse_ntlm_challenge(_challenge(0, 0, 0, with_version=False))
        assert r["ntlm_challenge"] is True
        assert "os_build" not in r and "method" not in r
        assert r["target_name"] == "DESKTOP-34M18MB"

    def test_non_challenge_returns_none(self):
        assert S.parse_ntlm_challenge(b"no ntlmssp here") is None
        # A Type-1 (MessageType 1), not a challenge, must be rejected.
        t1 = S.build_ntlmssp_negotiate()
        assert S.parse_ntlm_challenge(t1) is None


class TestNtlmFingerprintFraming:
    """Regression: _recv_smb_frame STRIPS the 4-byte NBT prefix, so the SMB2 header
    starts at offset 0 — the negotiate guard must check neg[:4], not neg[4:8]. The
    off-by-4 check made _ntlm_fingerprint return {} against a real host even though
    parse_ntlm_challenge worked. Drives the real framing path with a fake socket."""

    def test_end_to_end_framing_extracts_build(self, monkeypatch):
        import socket as _sock
        from scanner.scanner_base import ScopeGuard

        neg = b"\xfeSMB" + b"\x00" * 60 + b"\x00" * 8        # minimal SMB2 msg
        ss = b"\xfeSMB" + b"\x00" * 60 + _challenge(10, 0, 26100)   # carries CHALLENGE
        buf = (struct.pack(">I", len(neg)) + neg +
               struct.pack(">I", len(ss)) + ss)              # two NBT-framed messages

        class _FakeSock:
            def __init__(self):
                self.b = buf
            def settimeout(self, t): pass
            def sendall(self, b): pass
            def recv(self, n):
                c, self.b = self.b[:n], self.b[n:]
                return c
            def close(self): pass

        monkeypatch.setattr(S, "resolve", lambda t, p, proto="tcp": (_sock.AF_INET, (t, p)))
        monkeypatch.setattr(S.socket, "create_connection", lambda addr, timeout=None: _FakeSock())
        sc = S.SMBScanner(ScopeGuard.from_list(["1.0.0.0/8"]),
                          rate=1e9, concurrency=1, timeout=0.1)
        fp = sc._ntlm_fingerprint("1.2.3.4")
        assert fp.get("os_build") == 26100
        assert fp.get("os_release") == "Windows 11 24H2"
        assert fp.get("method") == "smb2_ntlm_version"

    def test_ntlm_os_build_shared_function(self, monkeypatch):
        # os_fingerprint reuses this exact function — assert it stands alone.
        import socket as _sock
        neg = b"\xfeSMB" + b"\x00" * 60 + b"\x00" * 8
        ss = b"\xfeSMB" + b"\x00" * 60 + _challenge(10, 0, 22631)
        buf = struct.pack(">I", len(neg)) + neg + struct.pack(">I", len(ss)) + ss

        class _FakeSock:
            def __init__(self): self.b = buf
            def settimeout(self, t): pass
            def sendall(self, b): pass
            def recv(self, n):
                c, self.b = self.b[:n], self.b[n:]; return c
            def close(self): pass

        monkeypatch.setattr(S.socket, "create_connection", lambda addr, timeout=None: _FakeSock())
        fp = S.ntlm_os_build("1.2.3.4")
        assert fp["os_build"] == 22631 and fp["os_release"] == "Windows 11 23H2"


class TestBuildMap:
    def test_client_server_shared_build_surfaces_both(self):
        r = S.windows_release_from_build(10, 0, 26100)
        assert r["os_release"] == "Windows 11 24H2"
        assert r["os_release_alt"] == "Windows Server 2025"

    def test_confidence_high_on_exact_match(self):
        assert S.windows_release_from_build(10, 0, 22631)["os_confidence"] >= 0.95


class TestType1AndSpnego:
    def test_type1_sets_negotiate_version(self):
        t1 = S.build_ntlmssp_negotiate()
        assert t1[:8] == S.NTLMSSP_SIG
        assert struct.unpack_from("<I", t1, 8)[0] == 1            # MessageType 1
        flags = struct.unpack_from("<I", t1, 12)[0]
        assert flags & S.NTLMSSP_NEGOTIATE_VERSION               # server will disclose Version

    def test_spnego_wraps_and_contains_type1(self):
        t1 = S.build_ntlmssp_negotiate()
        blob = S._spnego_init(t1)
        assert blob[0] == 0x60                                    # GSS-API [APPLICATION 0]
        assert S._NTLMSSP_OID in blob                             # advertises NTLM mech
        assert t1 in blob                                         # carries the Type-1 verbatim

    def test_session_setup_packet_shape(self):
        blob = S._spnego_init(S.build_ntlmssp_negotiate())
        pkt = S._smb2_session_setup(blob)
        assert pkt[:4] == b"\xfeSMB"
        # No NBT prefix here (added at send time): Command@12, MessageId@24.
        assert struct.unpack_from("<H", pkt, 12)[0] == 0x0001     # SESSION_SETUP command
        assert struct.unpack_from("<Q", pkt, 24)[0] == 1          # MessageId 1
        # SecurityBufferOffset (rel. to SMB2 header) points past the fixed body.
        assert struct.unpack_from("<H", pkt, 64 + 12)[0] == 88
        assert struct.unpack_from("<H", pkt, 64 + 14)[0] == len(blob)

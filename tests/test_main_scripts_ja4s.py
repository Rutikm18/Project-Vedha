"""
test_main_scripts_ja4s.py — JA4S TLS ServerHello fingerprint (advanced capability).

Pure assembler + the raw-ServerHello parse path (crafted fixture, reusing the JARM
parser) + the JA4S threat-intel finding rule. No live network.
"""
from __future__ import annotations

import hashlib
import struct

from main_scripts import findings as F
from main_scripts import ja4s


# ── ServerHello fixture builder ──────────────────────────────────────────────
def _ext(t: int, data: bytes) -> bytes:
    return struct.pack("!HH", t, len(data)) + data


def _serverhello(legacy: int, cipher: int, exts: list[tuple[int, bytes]]) -> bytes:
    ext_blob = b"".join(_ext(t, d) for t, d in exts)
    body = (struct.pack("!H", legacy) + b"\x00" * 32 + b"\x00"        # ver + random + sid_len
            + struct.pack("!H", cipher) + b"\x00"                      # cipher + compression
            + struct.pack("!H", len(ext_blob)) + ext_blob)
    hs = b"\x02" + struct.pack("!I", len(body))[1:] + body             # server_hello
    return b"\x16\x03\x03" + struct.pack("!H", len(hs)) + hs           # TLS record


# ── pure assembler ───────────────────────────────────────────────────────────
def test_ja4s_from_fields_shape_and_parts():
    j = ja4s.ja4s_from_fields(protocol="t", version=0x0304, cipher=0x1301,
                              ext_types=[0x002b, 0x0033], alpn=b"h2")
    a, b, c = j.split("_")
    assert a == "t1302h2"                      # t + 13 + 02 exts + h2 alpn
    assert b == "1301"                         # cipher
    assert c == hashlib.sha256(b"002b,0033").hexdigest()[:12]


def test_version_and_alpn_encodings():
    assert ja4s.ja4s_from_fields(protocol="t", version=0x0303, cipher=0x1301,
                                 ext_types=[], alpn=b"").split("_")[0] == "t120000"
    # http/1.1 -> first+last char "h1"; no alpn -> "00"
    assert ja4s.ja4s_from_fields(protocol="t", version=0x0304, cipher=0x1301,
                                 ext_types=[0x0], alpn=b"http/1.1").split("_")[0] == "t1301h1"


def test_empty_extensions_sentinel():
    assert ja4s.ja4s_from_fields(protocol="t", version=0x0304, cipher=0x1301,
                                 ext_types=[], alpn=b"").endswith("_000000000000")


def test_extension_hash_is_order_sensitive():
    a = ja4s.ja4s_from_fields(protocol="t", version=0x0304, cipher=0x1301,
                              ext_types=[0x002b, 0x0033], alpn=b"")
    b = ja4s.ja4s_from_fields(protocol="t", version=0x0304, cipher=0x1301,
                              ext_types=[0x0033, 0x002b], alpn=b"")
    assert a != b


# ── raw ServerHello parse path ───────────────────────────────────────────────
def test_ja4s_from_serverhello_tls13():
    sh = _serverhello(0x0303, 0x1301, [
        (0x002b, b"\x03\x04"),          # supported_versions -> real version 1.3
        (0x0033, b"\x00\x01\x00"),      # key_share (value ignored — types only)
        (0x0010, b"\x00\x03\x02h2"),    # ALPN chosen: h2
    ])
    j = ja4s.ja4s_from_serverhello(sh)
    exp_c = hashlib.sha256(b"002b,0033,0010").hexdigest()[:12]
    assert j == f"t1303h2_1301_{exp_c}"   # t, TLS1.3, 3 exts, alpn h2, cipher 1301


def test_ja4s_from_bad_serverhello_is_none():
    assert ja4s.ja4s_from_serverhello(b"not-a-serverhello") is None


# ── threat-intel finding rule ────────────────────────────────────────────────
def test_suspicious_ja4s_finding_fires_only_on_match():
    ja4s.SUSPICIOUS_JA4S["t1303h2_1301_deadbeefcafe"] = "unit-test C2 server profile"
    try:
        fs = F.run_findings([{
            "scanner": "tls_fingerprint", "target": "10.0.0.9", "port": 443, "status": "open",
            "data": {"ja4s": "t1303h2_1301_deadbeefcafe"}}])
        hit = next(f for f in fs if f.rule_id == "TLS-SUSPICIOUS-SERVER-FINGERPRINT")
        assert hit.severity == F.SEV_HIGH and hit.data["match"] == "unit-test C2 server profile"
        miss = F.run_findings([{
            "scanner": "tls_fingerprint", "target": "t", "port": 443, "status": "open",
            "data": {"ja4s": "t1200_1301_000000000000"}}])
        assert "TLS-SUSPICIOUS-SERVER-FINGERPRINT" not in {f.rule_id for f in miss}
    finally:
        ja4s.SUSPICIOUS_JA4S.pop("t1303h2_1301_deadbeefcafe", None)

"""
test_tls_fingerprint.py — Tier 2.3: active TLS fingerprint (JARM methodology).

Pure/unit coverage of the raw-TLS machinery:
  * ClientHello construction (valid TLS record, SNI, cipher suites)
  * ServerHello parsing (negotiated version + cipher) via synthetic round-trip
  * JARM-style 62-char digest (zero-hash on no response, deterministic, stable)
The live handshake is verified separately in test_tls_fingerprint_integration.
"""

from __future__ import annotations

import struct

import pytest

from scanner import tls_fingerprint as tf


# ── ClientHello construction ──────────────────────────────────────────────────

class TestClientHello:
    def test_is_tls_handshake_record(self):
        hello = tf.build_client_hello("example.com", tf.CIPHER_LIST)
        assert hello[0] == 0x16                     # content type: handshake
        assert hello[1:3] == b"\x03\x01"            # record version TLS 1.0

    def test_contains_client_hello_handshake_type(self):
        hello = tf.build_client_hello("example.com", tf.CIPHER_LIST)
        # record payload starts at offset 5; first handshake byte = 0x01
        assert hello[5] == 0x01                      # ClientHello

    def test_contains_sni_hostname(self):
        hello = tf.build_client_hello("scan.target.local", tf.CIPHER_LIST)
        assert b"scan.target.local" in hello

    def test_declared_lengths_are_consistent(self):
        hello = tf.build_client_hello("example.com", tf.CIPHER_LIST)
        rec_len = struct.unpack("!H", hello[3:5])[0]
        assert rec_len == len(hello) - 5             # record length matches body


# ── ServerHello parsing ───────────────────────────────────────────────────────

def _synthetic_server_hello(version=0x0303, cipher=0xC02F, ext=b""):
    body = (struct.pack("!H", version) + b"\x11" * 32 +   # version + random
            b"\x00" +                                      # session id len 0
            struct.pack("!H", cipher) +                    # cipher suite
            b"\x00")                                        # compression null
    if ext:
        body += struct.pack("!H", len(ext)) + ext
    else:
        body += b"\x00\x00"
    hs = b"\x02" + struct.pack("!I", len(body))[1:] + body   # ServerHello, 3-byte len
    return b"\x16\x03\x03" + struct.pack("!H", len(hs)) + hs


class TestParseServerHello:
    def test_extracts_version_and_cipher(self):
        rec = _synthetic_server_hello(version=0x0303, cipher=0xC02F)
        parsed = tf.parse_server_hello(rec)
        assert parsed["version"] == 0x0303
        assert parsed["cipher"] == 0xC02F

    def test_tls13_version_from_supported_versions_ext(self):
        # ServerHello legacy_version stays 0x0303; real version is in ext 43.
        sv_ext = struct.pack("!HH", 43, 2) + struct.pack("!H", 0x0304)
        rec = _synthetic_server_hello(version=0x0303, cipher=0x1301, ext=sv_ext)
        parsed = tf.parse_server_hello(rec)
        assert parsed["version"] == 0x0304          # TLS 1.3 negotiated

    def test_returns_none_on_alert(self):
        # A TLS alert record (type 0x15) is not a ServerHello.
        alert = b"\x15\x03\x03\x00\x02\x02\x28"
        assert tf.parse_server_hello(alert) is None

    def test_returns_none_on_short(self):
        assert tf.parse_server_hello(b"\x16\x03") is None


# ── code helpers + digest ─────────────────────────────────────────────────────

class TestDigest:
    def test_version_code(self):
        assert tf.version_code(0x0301) == "1"
        assert tf.version_code(0x0303) == "3"
        assert tf.version_code(0x0304) == "4"
        assert tf.version_code(None) == "0"

    def test_cipher_code_known_and_unknown(self):
        assert tf.cipher_code(tf.CIPHER_LIST[0]) == "01"
        assert tf.cipher_code(0xDEAD) == "00"       # not in list
        assert tf.cipher_code(None) == "00"

    def test_zero_hash_when_no_responses(self):
        digest = tf.jarm_style_digest([None] * 10)
        assert digest == "0" * 62

    def test_digest_is_62_chars(self):
        results = [{"version": 0x0303, "cipher": tf.CIPHER_LIST[0],
                    "extensions": b"\x00\x0b"}] * 10
        assert len(tf.jarm_style_digest(results)) == 62

    def test_digest_is_deterministic(self):
        results = [{"version": 0x0303, "cipher": 0xC02F, "extensions": b"\x00\x0a"},
                   None] * 5
        assert tf.jarm_style_digest(results) == tf.jarm_style_digest(results)

    def test_digest_differs_with_cipher(self):
        a = [{"version": 0x0303, "cipher": tf.CIPHER_LIST[0], "extensions": b""}] * 10
        b = [{"version": 0x0303, "cipher": tf.CIPHER_LIST[1], "extensions": b""}] * 10
        assert tf.jarm_style_digest(a) != tf.jarm_style_digest(b)

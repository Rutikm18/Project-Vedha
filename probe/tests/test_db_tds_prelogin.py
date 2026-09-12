"""
test_db_tds_prelogin.py — MSSQL encryption posture from the TDS PRELOGIN reply.

WHY. db_scan identified SQL Server and threw the rest of the reply away, so the
one posture fact TDS volunteers for free — whether the server can encrypt at all
— never reached the manager. A SQL Server answering ENCRYPT_NOT_SUP carries every
credential and every row in cleartext, and Vedha reported it as merely "a
database listener".

The subtlety these tests pin: ENCRYPT_OFF is NOT cleartext credentials. TDS
encrypts the LOGIN packet even when bulk encryption is off, so only
ENCRYPT_NOT_SUP means the password crosses in clear. Conflating the two would
manufacture a critical finding on a normally-configured server.
"""
from __future__ import annotations

import struct

from scanner.db_scanner import (
    _TDS_PRELOGIN_REQUEST, parse_tds_prelogin,
)


def _prelogin_response(encryption: int | None = 0x00,
                       version: bytes | None = b"\x0f\x00\x07\xd0",
                       truncate_table: bool = False) -> bytes:
    """Build a server PRELOGIN reply the way SQL Server actually frames one."""
    opts = []
    if version is not None:
        opts.append((0x00, version + b"\x00\x00"))
    if encryption is not None:
        opts.append((0x01, bytes([encryption])))
    table_len = len(opts) * 5 + 1
    table, blob, off = b"", b"", table_len
    for token, payload in opts:
        table += struct.pack(">BHH", token, off, len(payload))
        blob += payload
        off += len(payload)
    table += b"\xff"
    body = table + blob
    if truncate_table:
        body = body[:3]
    header = struct.pack(">BBHHBB", 0x04, 0x01, 8 + len(body), 0, 0, 0)
    return header + body


class TestEncryptionPosture:
    def test_not_supported_means_no_tls_at_all(self):
        out = parse_tds_prelogin(_prelogin_response(encryption=0x02))
        assert out["encryption_mode"] == "not_supported"
        assert out["ssl_supported"] is False
        assert out["encryption_required"] is False

    def test_required_is_the_hardened_case(self):
        out = parse_tds_prelogin(_prelogin_response(encryption=0x03))
        assert out["encryption_mode"] == "required"
        assert out["ssl_supported"] is True
        assert out["encryption_required"] is True

    def test_off_still_supports_tls(self):
        """ENCRYPT_OFF must NOT be read as 'cannot encrypt' — TDS still encrypts
        the login packet, so credentials are not exposed."""
        out = parse_tds_prelogin(_prelogin_response(encryption=0x00))
        assert out["encryption_mode"] == "off"
        assert out["ssl_supported"] is True
        assert out["encryption_required"] is False


class TestVersion:
    def test_version_is_decoded(self):
        out = parse_tds_prelogin(
            _prelogin_response(version=b"\x0f\x00\x07\xd0"))
        assert out["server_version"] == "15.0.2000"


class TestPositiveEvidenceOnly:
    def test_identification_survives_a_missing_encryption_option(self):
        out = parse_tds_prelogin(_prelogin_response(encryption=None))
        assert out["engine"] == "microsoft sql server"
        assert out["tds_response"] is True
        assert "encryption_mode" not in out
        assert "ssl_supported" not in out

    def test_truncated_table_claims_nothing_extra(self):
        out = parse_tds_prelogin(_prelogin_response(truncate_table=True))
        assert out["tds_response"] is True
        assert "ssl_supported" not in out

    def test_garbage_does_not_raise(self):
        for blob in (b"", b"\x04", b"\x04" + b"\xff" * 40, b"\x12\x01\x00"):
            out = parse_tds_prelogin(blob)
            assert out["engine"] == "microsoft sql server"

    def test_unknown_encryption_value_is_not_invented(self):
        out = parse_tds_prelogin(_prelogin_response(encryption=0x7f))
        assert "encryption_mode" not in out


class TestRequestIsWellFormed:
    """The malformed original could not elicit an ENCRYPTION option at all."""

    def test_header_length_matches_body(self):
        assert int.from_bytes(_TDS_PRELOGIN_REQUEST[2:4], "big") == len(
            _TDS_PRELOGIN_REQUEST)

    def test_option_table_parses_and_offsets_are_in_range(self):
        payload = _TDS_PRELOGIN_REQUEST[8:]
        i, seen = 0, {}
        while payload[i] != 0xFF:
            token = payload[i]
            off = int.from_bytes(payload[i + 1:i + 3], "big")
            ln = int.from_bytes(payload[i + 3:i + 5], "big")
            assert token not in seen, f"duplicate option token {token}"
            assert off + ln <= len(payload), "option data runs past the packet"
            seen[token] = (off, ln)
            i += 5
        assert 0x01 in seen, "no ENCRYPTION option offered — server won't state its stance"

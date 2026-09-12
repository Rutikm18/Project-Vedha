"""
test_db_mysql_greeting.py — MySQL TLS posture from the server's own capability flags.

WHY. The MySQL greeting advertises CLIENT_SSL before authentication, and
db_scan already read the packet to extract the version — then discarded the
flags. A MySQL server that cannot do TLS carries credentials and every query
result in cleartext, and Vedha described it only as "a database listener".

The trap these tests pin: a SHORT read must never be reported as "TLS not
offered". That inverts the finding — it manufactures a cleartext report against
a server that may well be hardened. Absent evidence is absent, not negative.
"""
from __future__ import annotations

import struct

from scanner.db_scanner import _MYSQL_CLIENT_SSL, parse_mysql_greeting


def _greeting(version: bytes = b"8.0.36", caps: int | None = _MYSQL_CLIENT_SSL,
              proto: int = 10, stop_after_version: bool = False) -> bytes:
    payload = bytes([proto]) + version + b"\x00"
    if not stop_after_version:
        payload += b"\x01\x00\x00\x00"          # connection id
        payload += b"A" * 8                      # auth-plugin-data-part-1
        payload += b"\x00"                       # filler
        if caps is not None:
            payload += struct.pack("<H", caps)   # capability_flags_1
    header = len(payload).to_bytes(3, "little") + b"\x00"
    return header + payload


class TestIdentification:
    def test_version_and_protocol(self):
        out = parse_mysql_greeting(_greeting())
        assert out["engine"] == "mysql/mariadb"
        assert out["server_version"] == "8.0.36"
        assert out["protocol_version"] == 10

    def test_non_mysql_is_rejected(self):
        assert parse_mysql_greeting(b"HTTP/1.1 200 OK\r\n\r\n") is None
        assert parse_mysql_greeting(b"") is None
        assert parse_mysql_greeting(b"\x00\x00\x00\x00\x63rest") is None


class TestTLSPosture:
    def test_client_ssl_advertised(self):
        out = parse_mysql_greeting(_greeting(caps=_MYSQL_CLIENT_SSL | 0x0001))
        assert out["ssl_supported"] is True

    def test_client_ssl_absent_means_cleartext(self):
        """Flags present and CLIENT_SSL clear — a real negative, safe to report."""
        out = parse_mysql_greeting(_greeting(caps=0x0001))
        assert out["ssl_supported"] is False

    def test_short_packet_claims_nothing(self):
        """Absent evidence must not become a cleartext finding."""
        out = parse_mysql_greeting(_greeting(stop_after_version=True))
        assert out["server_version"] == "8.0.36"
        assert "ssl_supported" not in out

    def test_protocol_9_has_no_capability_flags(self):
        out = parse_mysql_greeting(_greeting(proto=9))
        assert out["protocol_version"] == 9
        assert "ssl_supported" not in out

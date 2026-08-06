import struct
from scanner.udp_scanner import (
    interpret_ntp_monlist, interpret_dns_recursion, interpret_memcached_stats,
    _ntp_monlist_probe, _memcached_stats_probe,
)


def test_ntp_monlist_enabled():
    reply = bytes([0x17 | 0x80]) + b"\x00" * 100   # mode 7 + response bit
    assert interpret_ntp_monlist(reply) is True


def test_ntp_monlist_absent():
    assert interpret_ntp_monlist(b"") is False
    assert interpret_ntp_monlist(b"\x1c" + b"\x00" * 47) is False  # normal mode-4


def test_dns_open_recursion():
    # flags: QR=1, RD=1, RA=1, RCODE=0 -> 0x8180 ; ANCOUNT=1
    header = b"\x13\x37" + struct.pack(">H", 0x8180) + struct.pack(">HHHH", 1, 1, 0, 0)
    out = interpret_dns_recursion(header + b"\x00" * 4)
    assert out["recursion_available"] is True
    assert out["open_recursion"] is True


def test_memcached_exposed():
    assert interpret_memcached_stats(b"STAT pid 123\r\n") is True
    assert interpret_memcached_stats(b"") is False


def test_probe_builders_are_bytes():
    assert isinstance(_ntp_monlist_probe(), bytes)
    assert _memcached_stats_probe().endswith(b"stats\r\n")

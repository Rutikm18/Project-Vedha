"""Regression tests for db_scanner fingerprint matchers.

Focus: MySQL X Protocol (port 33060) must be identified as such and must NOT be
misread as Oracle TNS. Previously the Oracle probe matched any binary whose 5th
byte was 2/4/11 — MySQL X's NOTICE frame (type 11) tripped it.
"""
from __future__ import annotations

import asyncio
import struct

import pytest

from scanner.db_scanner import _probe_mysqlx, _probe_oracle


class FakeReader:
    def __init__(self, data: bytes):
        self._data = data

    async def read(self, n: int) -> bytes:
        return self._data[:n]


class FakeWriter:
    def write(self, _b: bytes) -> None:  # noqa: D401
        pass

    async def drain(self) -> None:
        pass


def _run(coro):
    return asyncio.new_event_loop().run_until_complete(coro)


# A MySQL X Protocol server frame: [uint32 LE length][1-byte msg type][payload].
# NOTICE = 11 (the exact byte that used to be misread as a TNS resend packet).
def _xproto_frame(msg_type: int = 11, payload: bytes = b"x" * 25) -> bytes:
    return struct.pack("<I", 1 + len(payload)) + bytes([msg_type]) + payload


# A genuine Oracle TNS packet: [uint16 BE length][uint16 checksum=0][1-byte type]...
def _tns_packet(tns_type: int = 2, total: int = 16) -> bytes:
    body = b"\x00" * (total - 8)
    return struct.pack(">HHBBH", total, 0, tns_type, 0, 0) + body


def _probe(fn, data: bytes):
    return _run(fn(FakeReader(data), FakeWriter(), 1.0))


class TestMysqlxVsOracle:
    def test_mysqlx_identified(self):
        r = _probe(_probe_mysqlx, _xproto_frame(msg_type=11))
        assert r is not None and r["engine"] == "mysql x protocol"
        assert r["xproto_msg_type"] == 11

    def test_mysqlx_not_misread_as_oracle(self):
        # The core regression: an X-protocol NOTICE (type 11) must NOT match the
        # (tightened) Oracle probe — its BE length header can't bound the frame.
        assert _probe(_probe_oracle, _xproto_frame(msg_type=11)) is None

    def test_oracle_still_identified(self):
        for t in (2, 4, 5, 11):
            r = _probe(_probe_oracle, _tns_packet(tns_type=t))
            assert r is not None and r["engine"] == "oracle tns", t
            assert r["tns_packet_type"] == t

    def test_oracle_reply_not_misread_as_mysqlx(self):
        assert _probe(_probe_mysqlx, _tns_packet(tns_type=2)) is None

    def test_oracle_rejects_garbage_with_type_byte(self):
        # Loose matcher would have accepted any 5+ bytes with data[4] in {2,4,11};
        # a random blob whose BE length header doesn't match must now be rejected.
        assert _probe(_probe_oracle, b"\xff\xff\x00\x00\x0b\x00\x00\x00") is None

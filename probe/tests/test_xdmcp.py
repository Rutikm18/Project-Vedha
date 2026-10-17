"""
test_xdmcp.py — XDMCP (UDP/177): from the agent's probe to the manager's rule.

The manager's risk catalogue named XDMCP, but no scan ever asked UDP/177, so the rule
could not fire. The agent now sends the standard XDMCP Query (the seven bytes nmap
uses; it opens no session) and parses the reply as hostile input. Willing means the
display manager will hand this host a remote X login; Unwilling means it is running
but declined.

The end-to-end tests drive the real UDPScanner against a loopback display manager
(on a free port, so no privilege is needed) and push its output through the manager's
real ingest and rules, which is the contract the two halves have to agree on.
"""
from __future__ import annotations

import asyncio
import json
import random
import struct
import sys
from dataclasses import asdict
from pathlib import Path

import pytest

import scanner.udp_scanner as us
from scanner.scanner_base import ScopeGuard

_ENGINE = Path(__file__).resolve().parents[2] / "manager" / "detection_engine"


def _array8(value: bytes) -> bytes:
    return struct.pack(">H", len(value)) + value


def _reply(opcode: int, *fields: bytes, version: int = 1, length: int | None = None) -> bytes:
    body = b"".join(_array8(f) for f in fields)
    return struct.pack(">HHH", version, opcode, len(body) if length is None else length) + body


WILLING = _reply(5, b"", b"lab-ws01", b"Linux 6.1.0 load 0.42")
UNWILLING = _reply(6, b"lab-ws01", b"Host unwilling")


# ── the probe ─────────────────────────────────────────────────────────────────

def test_the_query_is_the_standard_seven_byte_xdmcp_query():
    # version 1, opcode Query (2), 1 byte follows: zero authentication names
    assert us._xdmcp_probe() == b"\x00\x01\x00\x02\x00\x01\x00"


def test_udp_177_is_probed_as_xdmcp():
    assert us.UDP_PROBES[177] == ("xdmcp", us._xdmcp_probe())


# ── the parser ────────────────────────────────────────────────────────────────

def test_a_willing_reply_names_the_display_manager():
    assert us.interpret_xdmcp(WILLING) == {
        "xdmcp_opcode": "willing", "xdmcp_auth": "", "xdmcp_hostname": "lab-ws01",
        "xdmcp_status": "Linux 6.1.0 load 0.42"}


def test_an_unwilling_reply_is_still_xdmcp():
    assert us.interpret_xdmcp(UNWILLING) == {
        "xdmcp_opcode": "unwilling", "xdmcp_hostname": "lab-ws01",
        "xdmcp_status": "Host unwilling"}


@pytest.mark.parametrize("reply", [
    b"", b"\x00", WILLING[:5],                                     # shorter than the header
    _reply(5, b"", b"lab-ws01", b"ok", version=2),                 # not XDMCP version 1
    _reply(8, b"", b"lab-ws01", b"ok"),                            # Accept: not an answer to Query
    _reply(2),                                                     # our own Query echoed back
    _reply(5, b"", b"lab-ws01"),                                   # Willing without its status
    _reply(5, b"", b"lab-ws01", b"ok", length=200),                # header claims more than arrived
    WILLING[:-3],                                                  # cut off inside a field
    struct.pack(">HHH", 1, 5, 2) + b"\xff\xff",                    # a field length past the end
    WILLING + b"trailing",                                         # bytes beyond the message
], ids=["empty", "one-byte", "short-header", "version-2", "accept", "echo", "missing-field",
        "length-lies", "truncated", "field-overrun", "trailing"])
def test_anything_that_does_not_add_up_is_not_xdmcp(reply):
    assert us.interpret_xdmcp(reply) == {}


def test_reply_text_is_capped_and_printable():
    hostile = _reply(5, b"", b"A" * 5000 + b"\x1b[31m<script>", b"\x00\x07ok\r\n")
    d = us.interpret_xdmcp(hostile)
    assert d["xdmcp_opcode"] == "willing"
    assert len(d["xdmcp_hostname"]) <= 128
    assert all(ch.isprintable() for value in d.values() for ch in value)


def test_no_byte_string_makes_the_parser_raise():
    rng = random.Random(177)
    for _ in range(5000):
        blob = bytes(rng.getrandbits(8) for _ in range(rng.randint(0, 64)))
        if rng.random() < 0.5:       # look like XDMCP so the deeper paths run too
            blob = b"\x00\x01\x00" + bytes([rng.choice([5, 6])]) + blob
        assert isinstance(us.interpret_xdmcp(blob), dict)


# ── on the wire, then through the manager ─────────────────────────────────────

class _DisplayManager(asyncio.DatagramProtocol):
    """Loopback stand-in for xdm/gdm/lightdm: answers an XDMCP Query, ignores the rest."""

    def __init__(self, reply: bytes):
        self.reply = reply
        self.received: list[bytes] = []

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        self.received.append(data)
        if data == us._xdmcp_probe():
            self.transport.sendto(self.reply, addr)


def _scan(reply: bytes):
    async def _run():
        loop = asyncio.get_running_loop()
        dm = _DisplayManager(reply)
        transport, _ = await loop.create_datagram_endpoint(lambda: dm, local_addr=("127.0.0.1", 0))
        port = transport.get_extra_info("socket").getsockname()[1]
        us.UDP_PROBES[port] = us.UDP_PROBES[177]      # the real probe, on a port a test can bind
        try:
            scanner = us.UDPScanner(ScopeGuard.from_list(["127.0.0.1/32"]), ports=[port],
                                    timeout=2.0)
            return await scanner._probe("127.0.0.1", port), dm.received
        finally:
            transport.close()
            us.UDP_PROBES.pop(port, None)
    return asyncio.run(_run())


def _manager_findings(results) -> dict:
    if not _ENGINE.exists():
        pytest.skip("manager tree not present")
    sys.path.insert(0, str(_ENGINE))
    try:
        import ingest
        import posture_rules
    except ImportError as exc:       # the agent half has already been proven
        pytest.skip(f"manager detection engine not importable here: {exc}")
    finally:
        sys.path.remove(str(_ENGINE))
    path = Path(__file__).parent / ".tmp_xdmcp_facts.jsonl"
    try:
        path.write_text("\n".join(json.dumps(asdict(r)) for r in results) + "\n")
        ingested = ingest.ingest_file(path)
        assert not ingested.quarantined, [q.reason for q in ingested.quarantined]
        return {f.rule_id: f for f in posture_rules.detect_all(ingested)}
    finally:
        path.unlink(missing_ok=True)


def test_the_scanner_reports_what_the_display_manager_said():
    result, received = _scan(WILLING)
    assert received == [us._xdmcp_probe()]          # one read-only Query, nothing else
    assert result.status == "open" and result.proto == "udp"
    assert result.data["service"] == "xdmcp"
    assert result.data["xdmcp_opcode"] == "willing"
    assert result.data["xdmcp_hostname"] == "lab-ws01"


def test_a_willing_display_manager_is_a_high_finding_end_to_end():
    result, _ = _scan(WILLING)
    found = _manager_findings([result])
    assert "POSTURE-XDMCP-WILLING" in found, sorted(found)
    assert found["POSTURE-XDMCP-WILLING"].severity == "high"
    assert "POSTURE-XDMCP-EXPOSED" not in found


def test_an_unwilling_display_manager_is_a_low_finding_end_to_end():
    result, _ = _scan(UNWILLING)
    found = _manager_findings([result])
    assert "POSTURE-XDMCP-EXPOSED" in found, sorted(found)
    assert found["POSTURE-XDMCP-EXPOSED"].severity == "low"
    assert "POSTURE-XDMCP-WILLING" not in found

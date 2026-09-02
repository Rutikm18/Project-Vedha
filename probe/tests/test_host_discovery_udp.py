"""
test_host_discovery_udp.py — the unprivileged UDP liveness tier + name facts.

Covers the pure NBSTAT parser, liveness fusion with UDP signals, and the live
tier against loopback responders: a NetBIOS answer proves life and yields the
hostname + MAC; an ICMP port-unreachable proves the target's stack is up; the
tier is skipped when TCP already proved life; PTR names become asset aliases.
"""

from __future__ import annotations

import asyncio
import struct

import pytest

from scanner import host_discovery as hd
from scanner.host_discovery import (
    HostDiscoveryScanner, fuse_liveness, parse_nbstat, STATE_CONFIRMED,
)
from scanner.scanner_base import ScopeGuard


def _nbstat_reply(names, mac=b"\x00\x0c\x29\xab\xcd\xef") -> bytes:
    """Build a NetBIOS node-status response (RFC 1002 §4.2.18)."""
    header = b"\x80\x00" + struct.pack(">HHHHH", 0x8400, 0, 1, 0, 0)
    rr_name = b"\x20" + b"CKAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" + b"\x00"
    table = b""
    for name, suffix, group in names:
        flags = 0x8400 if group else 0x0400
        table += name.ljust(15).encode()[:15] + bytes([suffix]) + struct.pack(">H", flags)
    stats = mac + b"\x00" * 40
    rdata = bytes([len(names)]) + table + stats
    return header + rr_name + struct.pack(">HHIH", 0x0021, 1, 0, len(rdata)) + rdata


class TestParseNbstat:
    def test_names_hostname_domain_mac(self):
        nb = parse_nbstat(_nbstat_reply([
            ("DESKTOP-7", 0x00, False), ("WORKGROUP", 0x00, True), ("DESKTOP-7", 0x20, False),
        ]))
        assert nb["hostname"] == "DESKTOP-7"
        assert nb["domain"] == "WORKGROUP"
        assert nb["mac"] == "00:0c:29:ab:cd:ef"
        assert [n["suffix"] for n in nb["names"]] == ["0x00", "0x00", "0x20"]
        assert nb["names"][1]["group"] is True

    def test_not_a_response(self):
        assert parse_nbstat(b"\x80\x00\x00\x00" + b"\x00" * 8) is None
        assert parse_nbstat(b"") is None

    def test_msbrowse_control_chars_dropped(self):
        nb = parse_nbstat(_nbstat_reply([("\x01\x02__MSBROWSE__\x02", 0x01, True),
                                         ("HOST1", 0x00, False)]))
        assert nb["hostname"] == "HOST1"
        assert nb["names"][0]["name"] == "__MSBROWSE__"


class TestFuseWithUdp:
    def test_udp_reply_alone_is_confirmed_alive(self):
        v = fuse_liveness([], None, [{"method": "udp_probe", "port": 137,
                                      "result": "reply", "confidence": 0.95}])
        assert v["alive"] is True
        assert v["state"] == STATE_CONFIRMED
        assert v["method"] == "udp"
        assert v["reason"] == "reply"

    def test_icmp_unreachable_alone(self):
        v = fuse_liveness([], None, [{"method": "udp_probe", "port": 33500,
                                      "result": "icmp_port_unreachable", "confidence": 0.90}])
        assert v["alive"] is True
        assert v["confidence"] == 0.9

    def test_tcp_plus_udp_corroborate(self):
        v = fuse_liveness([(80, "open")], None,
                          [{"method": "udp_probe", "port": 137, "result": "reply",
                            "confidence": 0.95}])
        assert v["method"] == "tcp+udp"
        assert v["confidence"] == 0.99          # 0.97 + one corroboration, capped
        assert v["reason"] == "syn_ack"         # TCP stays the headline signal

    def test_no_signals_unchanged(self):
        v = fuse_liveness([], None, [])
        assert v["alive"] is False
        assert v["method"] is None


# ── live loopback behaviour ──────────────────────────────────────────────────

class _Responder(asyncio.DatagramProtocol):
    def __init__(self, reply: bytes):
        self.reply = reply
        self.seen = 0

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        self.seen += 1
        self.transport.sendto(self.reply, addr)


async def _udp_server(reply: bytes):
    loop = asyncio.get_running_loop()
    transport, proto = await loop.create_datagram_endpoint(
        lambda: _Responder(reply), local_addr=("127.0.0.1", 0))
    return transport, proto, transport.get_extra_info("sockname")[1]


def _closed_udp_port() -> int:
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


@pytest.fixture
def no_neighbor(monkeypatch):
    monkeypatch.setattr(hd, "read_neighbor", lambda ip: None)


def _scanner(**kw) -> HostDiscoveryScanner:
    return HostDiscoveryScanner(ScopeGuard.from_list(["127.0.0.0/8"]), timeout=1.0,
                                reverse_dns=False, **kw)


def test_netbios_reply_proves_life_and_names_host(no_neighbor):
    reply = _nbstat_reply([("FILESRV01", 0x00, False), ("CORP", 0x00, True)])

    async def _run():
        transport, proto, port = await _udp_server(reply)
        s = _scanner(ports=[], udp_probes=[(port, "netbios-ns", hd._netbios_probe())],
                     unreach_port=_closed_udp_port())
        try:
            return (await s.scan_target("127.0.0.1"))[0], proto.seen
        finally:
            transport.close()

    res, seen = asyncio.run(_run())
    assert seen == 1
    d = res.data
    assert d["alive"] is True and res.status == "open"
    assert d["netbios_name"] == "FILESRV01"
    assert d["netbios_domain"] == "CORP"
    assert d["mac"] == "00:0c:29:ab:cd:ef"
    assert d["arp_state"] == "nbstat"
    assert "udp" in d["method"]
    assert any(e["result"] == "reply" for e in d["udp_evidence"])
    assert "netbios" not in d["udp_evidence"][0]      # parsed form lives at top level
    assert "FILESRV01" in res.evidence


def test_icmp_unreachable_from_closed_port_proves_stack_is_up(no_neighbor):
    async def _run():
        s = _scanner(ports=[], udp_probes=[], unreach_port=_closed_udp_port())
        return (await s.scan_target("127.0.0.1"))[0]

    res = asyncio.run(_run())
    assert res.data["alive"] is True
    assert res.data["reason"] == "icmp_port_unreachable"
    assert res.data["method"] == "udp"


def test_udp_tier_skipped_when_tcp_proves_life(no_neighbor):
    async def _run():
        server = await asyncio.start_server(lambda r, w: w.close(), "127.0.0.1", 0)
        tcp_port = server.sockets[0].getsockname()[1]
        transport, proto, udp_port = await _udp_server(b"\x00")
        s = _scanner(ports=[tcp_port], udp_probes=[(udp_port, "mdns", b"x")],
                     unreach_port=_closed_udp_port())
        try:
            return (await s.scan_target("127.0.0.1"))[0], proto.seen
        finally:
            transport.close()
            server.close()
            await server.wait_closed()

    res, seen = asyncio.run(_run())
    assert res.data["alive"] is True
    assert res.data["method"] == "tcp"
    assert seen == 0
    assert "udp_evidence" not in res.data


def test_udp_tier_skipped_when_neighbor_vouches(monkeypatch):
    monkeypatch.setattr(hd, "read_neighbor",
                        lambda ip: hd.Neighbor(mac="aa:bb:cc:dd:ee:01",
                                               fresh=hd.FRESH_REACHABLE, raw_state="REACHABLE"))

    async def _run():
        transport, proto, udp_port = await _udp_server(b"\x00")
        s = _scanner(ports=[], udp_probes=[(udp_port, "mdns", b"x")],
                     unreach_port=_closed_udp_port())
        try:
            return (await s.scan_target("127.0.0.1"))[0], proto.seen
        finally:
            transport.close()

    res, seen = asyncio.run(_run())
    assert res.data["alive"] is True and res.data["method"] == "arp"
    assert seen == 0


def test_reverse_dns_name_recorded_and_becomes_alias(monkeypatch):
    monkeypatch.setattr(hd, "read_neighbor", lambda ip: None)
    monkeypatch.setattr(hd, "_reverse_dns", lambda ip: "printer-3f.corp.example")

    async def _run():
        server = await asyncio.start_server(lambda r, w: w.close(), "127.0.0.1", 0)
        port = server.sockets[0].getsockname()[1]
        s = HostDiscoveryScanner(ScopeGuard.from_list(["127.0.0.0/8"]), timeout=1.0,
                                 ports=[port], udp_liveness=False)
        try:
            return (await s.scan_target("127.0.0.1"))[0]
        finally:
            server.close()
            await server.wait_closed()

    res = asyncio.run(_run())
    assert res.data["hostname"] == "printer-3f.corp.example"
    assert "name printer-3f.corp.example" in res.evidence

    from workflow.asset import Asset
    a = Asset(host="127.0.0.1")
    a.merge_result(res)
    assert "printer-3f.corp.example" in a.aliases
    assert a.last_seen_alive is not None


def test_tcp_reset_counts_as_proof_of_life():
    """A RST mid-handshake (ConnectionResetError) is the target's stack talking."""
    async def _run():
        s = _scanner(ports=[1], udp_liveness=False)

        async def boom(*a, **k):
            raise ConnectionResetError()

        import asyncio as _a
        orig = _a.open_connection
        _a.open_connection = boom
        try:
            return await s._probe("127.0.0.1", 1)
        finally:
            _a.open_connection = orig

    assert asyncio.run(_run()) == "refused"


def test_udp_tier_skipped_when_arp_definitively_failed(monkeypatch):
    """On-LAN INCOMPLETE/FAILED = nobody owns the address right now; spending
    datagrams on it only slows a sweep of a mostly-empty /24."""
    monkeypatch.setattr(hd, "read_neighbor",
                        lambda ip: hd.Neighbor(mac=None, fresh=hd.FRESH_FAILED,
                                               raw_state="INCOMPLETE"))

    async def _run():
        transport, proto, udp_port = await _udp_server(b"\x00")
        s = _scanner(ports=[], udp_probes=[(udp_port, "mdns", b"x")],
                     unreach_port=_closed_udp_port())
        try:
            return (await s.scan_target("127.0.0.1"))[0], proto.seen
        finally:
            transport.close()

    res, seen = asyncio.run(_run())
    assert res.data["alive"] is False
    assert res.data["reason"] == "arp_unresolved"
    assert seen == 0

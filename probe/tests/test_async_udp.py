"""
test_async_udp.py — tests for the true-async UDP probe helper in scanner_base.

These use REAL loopback UDP servers (no mocks): the probe helper must be driven
entirely on the asyncio event loop with no thread pool. Each test drives the
coroutine with asyncio.run() so no pytest-asyncio dependency is needed.

Tri-state contract:
    bytes        -> a reply arrived (service OPEN and speaking)
    _UDP_CLOSED  -> ICMP port-unreachable (port definitively CLOSED)
    None         -> no reply within timeout (OPEN|FILTERED, ambiguous)
"""

from __future__ import annotations

import asyncio

from scanner.scanner_base import async_udp_probe, _UDP_CLOSED, _UDPProbeProtocol


# ── loopback helpers ──────────────────────────────────────────────────────────

class _EchoProtocol(asyncio.DatagramProtocol):
    def connection_made(self, transport):
        self._t = transport

    def datagram_received(self, data, addr):
        self._t.sendto(data, addr)   # echo back verbatim


class _SinkProtocol(asyncio.DatagramProtocol):
    def datagram_received(self, data, addr):
        pass                          # receive but never reply


async def _start_server(protocol_cls):
    loop = asyncio.get_running_loop()
    transport, _ = await loop.create_datagram_endpoint(
        protocol_cls, local_addr=("127.0.0.1", 0))
    port = transport.get_extra_info("socket").getsockname()[1]
    return transport, port


# ── tests ─────────────────────────────────────────────────────────────────────

def test_probe_open_returns_reply_bytes():
    async def _run():
        server, port = await _start_server(_EchoProtocol)
        try:
            return await async_udp_probe("127.0.0.1", port, b"ping", timeout=2.0)
        finally:
            server.close()
    assert asyncio.run(_run()) == b"ping"


def test_probe_open_returns_exact_payload():
    async def _run():
        server, port = await _start_server(_EchoProtocol)
        try:
            return await async_udp_probe("127.0.0.1", port,
                                         b"\x00\x01\x02hello", timeout=2.0)
        finally:
            server.close()
    assert asyncio.run(_run()) == b"\x00\x01\x02hello"


def test_probe_no_reply_returns_none_on_timeout():
    async def _run():
        server, port = await _start_server(_SinkProtocol)
        try:
            return await async_udp_probe("127.0.0.1", port, b"ping", timeout=0.3)
        finally:
            server.close()
    assert asyncio.run(_run()) is None


def test_datagram_received_resolves_future_with_bytes():
    async def _run():
        fut = asyncio.get_running_loop().create_future()
        proto = _UDPProbeProtocol(fut)
        proto.datagram_received(b"reply-data", ("127.0.0.1", 9999))
        return await fut
    assert asyncio.run(_run()) == b"reply-data"


def test_error_received_connection_refused_maps_to_closed():
    async def _run():
        fut = asyncio.get_running_loop().create_future()
        proto = _UDPProbeProtocol(fut)
        proto.error_received(ConnectionRefusedError())
        return await fut
    assert asyncio.run(_run()) is _UDP_CLOSED


def test_probe_unbound_loopback_port_is_not_open():
    # Port 1 on loopback is essentially never bound; the OS should send an
    # ICMP port-unreachable (-> _UDP_CLOSED) or the probe times out (-> None).
    # Either way it must NOT be reported as open (bytes).
    async def _run():
        return await async_udp_probe("127.0.0.1", 1, b"x", timeout=0.5)
    result = asyncio.run(_run())
    assert result is _UDP_CLOSED or result is None
    assert not isinstance(result, (bytes, bytearray))


def test_probe_concurrency_all_complete():
    # Fire many probes concurrently at one echo server. If the helper were
    # thread-pool bound this would serialize; on the event loop all resolve.
    async def _run():
        server, port = await _start_server(_EchoProtocol)
        try:
            payloads = [f"probe-{i}".encode() for i in range(50)]
            results = await asyncio.gather(*[
                async_udp_probe("127.0.0.1", port, p, timeout=2.0)
                for p in payloads
            ])
            return payloads, results
        finally:
            server.close()
    payloads, results = asyncio.run(_run())
    # Every probe got a reply back (echo servers echo verbatim); order within a
    # single connected socket is 1:1 so each result equals its payload.
    assert all(r == p for r, p in zip(results, payloads))


def test_probe_unresolvable_host_returns_none():
    async def _run():
        return await async_udp_probe("this-host-does-not-exist.invalid", 53,
                                     b"x", timeout=0.5)
    assert asyncio.run(_run()) is None


# ── UDPScanner integration: the refactor from thread pool to event loop ────────

from scanner.scanner_base import ScopeGuard


def test_udp_scanner_maps_closed_sentinel_to_closed_status(monkeypatch):
    # The new tri-state: an ICMP port-unreachable (_UDP_CLOSED) must surface as
    # status="closed", distinct from the timeout "filtered". Inject at the
    # retransmit boundary so the mapping logic is exercised deterministically.
    import scanner.udp_scanner as us

    async def fake_probe(target, port, payload, timeout, max_retries=0):
        return us._UDP_CLOSED

    monkeypatch.setattr(us, "async_udp_probe_retry", fake_probe)

    async def _run():
        scope = ScopeGuard.from_list(["127.0.0.0/8"])
        scanner = us.UDPScanner(scope, ports=[53], timeout=0.5)
        return await scanner._probe("127.0.0.1", 53)

    r = asyncio.run(_run())
    assert r is not None
    assert r.status == "closed"
    assert r.data["responded"] is False


def test_udp_scanner_probe_open_status_via_event_loop():
    import scanner.udp_scanner as us

    async def _run():
        loop = asyncio.get_running_loop()
        transport, _ = await loop.create_datagram_endpoint(
            _EchoProtocol, local_addr=("127.0.0.1", 0))
        port = transport.get_extra_info("socket").getsockname()[1]
        us.UDP_PROBES[port] = ("dns", us._dns_probe())
        try:
            scope = ScopeGuard.from_list(["127.0.0.0/8"])
            scanner = us.UDPScanner(scope, ports=[port], timeout=2.0)
            return await scanner._probe("127.0.0.1", port)
        finally:
            transport.close()
            us.UDP_PROBES.pop(port, None)

    r = asyncio.run(_run())
    assert r is not None
    assert r.status == "open"
    assert r.data["responded"] is True


def test_udp_scanner_probe_open_filtered_on_timeout():
    # Canonical (main_scripts) semantics: UDP silence is the ambiguous
    # open|filtered pair, never a definitive "filtered" — collapsing it was the
    # prior accuracy bug (see test_main_scripts_hardening). scanner/ is synced
    # from main_scripts, so it now reports the honest state.
    import scanner.udp_scanner as us

    async def _run():
        loop = asyncio.get_running_loop()
        transport, _ = await loop.create_datagram_endpoint(
            _SinkProtocol, local_addr=("127.0.0.1", 0))
        port = transport.get_extra_info("socket").getsockname()[1]
        us.UDP_PROBES[port] = ("dns", us._dns_probe())
        try:
            scope = ScopeGuard.from_list(["127.0.0.0/8"])
            scanner = us.UDPScanner(scope, ports=[port], timeout=0.3)
            return await scanner._probe("127.0.0.1", port)
        finally:
            transport.close()
            us.UDP_PROBES.pop(port, None)

    r = asyncio.run(_run())
    assert r is not None
    assert r.status == "open|filtered"

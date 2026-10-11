"""PortScanner's Windows connect path (fast-fail), exercised for real on any OS.

On Windows the scanner builds each scan socket itself so it can opt it out of
SYN retransmission before connecting. loop.sock_connect works everywhere, so
this path runs here against real local sockets with only the Windows ioctl
replaced: an open port, a closed port, a silent port, IPv6, a source port and
a hostname must all classify exactly as the plain path does.
"""
from __future__ import annotations

import asyncio
import socket

import pytest

from scanner import port_scanner as ps
from scanner.scanner_base import ScopeGuard


@pytest.fixture
def applied(monkeypatch):
    calls = []
    monkeypatch.setattr(ps.win_fast_connect, "enable",
                        lambda sock: calls.append(sock.family) or True)
    return calls


def _scanner(fast_fail: bool, **kw) -> ps.PortScanner:
    sc = ps.PortScanner(ScopeGuard.from_list(["127.0.0.0/8", "::1/128"]),
                        ports=[1], rate=1e6, concurrency=4, timeout=1.0, **kw)
    sc._fast_fail = fast_fail
    return sc


def _listener(family=socket.AF_INET, host="127.0.0.1"):
    srv = socket.socket(family, socket.SOCK_STREAM)
    srv.bind((host, 0))
    srv.listen(8)
    return srv


def _closed_port(family=socket.AF_INET, host="127.0.0.1") -> int:
    s = socket.socket(family, socket.SOCK_STREAM)
    s.bind((host, 0))
    port = s.getsockname()[1]
    s.close()
    return port


def _attempt(sc, target, port):
    return asyncio.run(sc._attempt(target, port))


def test_linux_and_mac_keep_the_plain_path():
    if ps.win_fast_connect.describe()["applies"]:
        pytest.skip("this machine is Windows")
    assert ps.PortScanner(ScopeGuard.from_list(["127.0.0.0/8"]))._fast_fail is False


@pytest.mark.parametrize("fast_fail", [False, True])
def test_open_port_is_open_on_both_paths(fast_fail, applied):
    srv = _listener()
    try:
        r = _attempt(_scanner(fast_fail), "127.0.0.1", srv.getsockname()[1])
    finally:
        srv.close()
    assert r.status == "open"
    assert applied == ([socket.AF_INET] if fast_fail else [])


@pytest.mark.parametrize("fast_fail", [False, True])
def test_closed_port_is_closed_on_both_paths(fast_fail, applied):
    r = _attempt(_scanner(fast_fail), "127.0.0.1", _closed_port())
    assert r.status == "closed"


def test_silence_is_filtered_and_the_socket_is_released(applied, monkeypatch):
    opened = []
    real = socket.socket

    def tracking(*a, **kw):
        s = real(*a, **kw)
        opened.append(s)
        return s

    async def never(_sock, _addr):
        await asyncio.sleep(10)

    sc = _scanner(True)
    monkeypatch.setattr(ps.socket, "socket", tracking)
    loop_cls = asyncio.get_event_loop_policy().new_event_loop().__class__
    monkeypatch.setattr(loop_cls, "sock_connect", lambda self, s, a: never(s, a))
    r = asyncio.run(sc._attempt("127.0.0.1", 9, None, min_timeout=None))
    assert r.status == "filtered"
    # The event loop opens its own AF_UNIX self-pipe; only the scan socket counts.
    scan = [s for s in opened if s.family in (socket.AF_INET, socket.AF_INET6)]
    assert scan and all(s.fileno() == -1 for s in scan)         # closed, not leaked


def test_ipv6_target_gets_an_ipv6_socket(applied):
    if not socket.has_ipv6:
        pytest.skip("no IPv6")
    try:
        srv = _listener(socket.AF_INET6, "::1")
    except OSError:
        pytest.skip("no IPv6 loopback")
    try:
        r = _attempt(_scanner(True), "::1", srv.getsockname()[1])
    finally:
        srv.close()
    assert r.status == "open" and applied == [socket.AF_INET6]


def test_source_port_is_bound(applied):
    srv = _listener()
    source = _closed_port()
    seen = []

    async def go():
        sc = _scanner(True, source_port=source)
        r = await sc._attempt("127.0.0.1", srv.getsockname()[1])
        conn, peer = srv.accept()
        seen.append(peer[1])
        conn.close()
        return r

    try:
        r = asyncio.run(go())
    finally:
        srv.close()
    assert r.status == "open" and seen == [source]


def test_hostname_falls_back_to_the_plain_path(applied):
    srv = _listener()
    try:
        r = _attempt(_scanner(True), "localhost", srv.getsockname()[1])
    finally:
        srv.close()
    assert r.status == "open"
    assert applied == []            # resolution stays with asyncio

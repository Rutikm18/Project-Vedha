"""
P2/D1 — the SYN scanner must drain replies WHILE it is still sending.

THE DEFECT
----------
Each retransmit round was two serial phases:

    for port in pending:  sendto(SYN)      # nothing reads the socket here
    while pending_set:    recv(reply)      # ...only now

Every reply provoked by the send phase therefore waits in SO_RCVBUF until the
whole cohort has gone out. The buffer is 4 MB, but Linux charges `skb->truesize`
— roughly 768 B for a 40-byte TCP segment, not 40 — so it holds on the order of
5,000 packets, NOT the ~40,000 a payload-bytes estimate suggests.

A 65,535-port sweep of a mostly-closed host answers with up to 65,535 RSTs. The
buffer saturates about 5,000 in; the kernel discards the rest **silently**.
Those ports stay unresolved, burn their retransmit rounds hitting the same wall,
and are finally reported `filtered` — ports that answered, reported as
firewalled, with nothing anywhere in the result to say so.

This is rate-independent: the overflow is set by how many ports are in the
round, not how fast they go out. Pacing the sends does not help, and `deep`
intensity resolves all 65,535 ports, which is precisely the configuration that
routes the port stage to THIS scanner.

WHAT THESE TESTS CAN AND CANNOT PROVE
-------------------------------------
Raw sockets do not work on macOS, so the packet path itself is still only
verifiable on Linux with NET_RAW. What is verified here is the part that was
actually wrong: the LOOP STRUCTURE. A fake kernel with a bounded, silently
dropping receive queue reproduces the false `filtered` exactly, and the same
fixture proves the interleaved drain removes it. Byte-level correctness is
unchanged by this fix — build_syn_packet and parse_packet are untouched.
"""
from __future__ import annotations

import socket
import struct
from collections import deque

import pytest

from scanner import syn_scanner as ss

TARGET = "10.77.0.5"
LOCAL = "10.77.0.2"
SRC_PORT = 40001
KEY = b"\x11" * 16


def _reply(port: int, *, flags: int) -> bytes:
    """A well-formed IPv4+TCP reply from TARGET:port to LOCAL:SRC_PORT."""
    ack = (ss.syn_cookie(TARGET, port, SRC_PORT, KEY) + 1) & 0xFFFFFFFF
    ip = struct.pack("!BBHHHBBH4s4s", 0x45, 0, 40, 0, 0, 64, 6, 0,
                     socket.inet_aton(TARGET), socket.inet_aton(LOCAL))
    tcp = struct.pack("!HHIIBBHHH", port, SRC_PORT, 0, ack,
                      5 << 4, flags, 8192, 0, 0)
    return ip + tcp


class _Kernel:
    """A receive queue that silently DROPS on overflow, like SO_RCVBUF."""

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.queue: deque[bytes] = deque()
        self.dropped = 0

    def deliver(self, pkt: bytes) -> None:
        if len(self.queue) >= self.capacity:
            self.dropped += 1          # no error, no signal — this is the bug
            return
        self.queue.append(pkt)


class _RecvSock:
    def __init__(self, kernel: _Kernel):
        self.kernel = kernel
        self.recv_calls = 0

    def recv(self, _n):
        self.recv_calls += 1
        if not self.kernel.queue:
            raise BlockingIOError
        return self.kernel.queue.popleft()

    def setblocking(self, _flag): pass
    def setsockopt(self, *_a): pass
    def close(self): pass


class _SendSock:
    """Every SYN provokes an immediate reply, as a closed/open port would."""

    def __init__(self, kernel: _Kernel, open_ports: set[int]):
        self.kernel = kernel
        self.open_ports = open_ports
        self.sent: list[int] = []

    def sendto(self, pkt: bytes, _addr):
        port = struct.unpack("!H", pkt[22:24])[1 - 1]   # TCP dst_port
        self.sent.append(port)
        flags = (ss.TCP_SYN | ss.TCP_ACK) if port in self.open_ports else ss.TCP_RST
        self.kernel.deliver(_reply(port, flags=flags))

    def setsockopt(self, *_a): pass
    def close(self): pass


@pytest.fixture
def fake_net(monkeypatch):
    """Replace the kernel, not the scanner. The loop under test is real."""
    state = {}

    def install(*, capacity: int, open_ports: set[int] | None = None):
        kernel = _Kernel(capacity)
        recv = _RecvSock(kernel)
        send = _SendSock(kernel, open_ports or set())

        def _socket(_family, _type, proto):
            return send if proto == socket.IPPROTO_RAW else recv

        monkeypatch.setattr(ss.socket, "socket", _socket)
        monkeypatch.setattr(ss, "resolve",
                            lambda *a, **k: (socket.AF_INET, (TARGET, 0)))
        monkeypatch.setattr(ss, "_local_source_ip", lambda _ip: LOCAL)
        monkeypatch.setattr(ss, "choose_source_port", lambda _p: SRC_PORT)
        # Readability is just "is anything queued" — no select on a fake.
        monkeypatch.setattr(ss, "_wait_readable",
                            lambda _s, _t: bool(kernel.queue))
        state.update(kernel=kernel, send=send, recv=recv)
        return state

    return install


def _scanner(ports, **kw):
    kw.setdefault("retries", 1)
    return ss.SynScanner(
        ScopeGuardStub(), ports=ports, key=KEY, report_closed=True,
        adaptive_timeout=False, pace_sends=False,
        force_fallback=True,          # never touch a real raw socket
        rate=100_000, concurrency=10, timeout=0.05, **kw)


class ScopeGuardStub:
    def in_scope(self, _t): return True
    def assert_in_scope(self, _t): pass


def _states(results):
    return {r.port: r.status for r in results if r.port is not None}


class TestRepliesSurviveTheSendPhase:
    def test_a_wide_sweep_does_not_manufacture_filtered_ports(self, fake_net):
        """THE BUG, in one assertion. 2,000 ports against a buffer that holds
        50: without an interleaved drain, ~1,950 answered ports are lost and
        reported `filtered`."""
        ports = list(range(9000, 11000))
        net = fake_net(capacity=50, open_ports={9443})

        results = _scanner(ports)._syn_scan_blocking(TARGET)
        states = _states(results)

        assert net["kernel"].dropped == 0, (
            f"{net['kernel'].dropped} replies dropped — the socket is still "
            f"only read after the whole cohort has been sent"
        )
        assert states.get(9443) == "open"
        assert sum(1 for s in states.values() if s == "filtered") == 0

    def test_every_port_gets_a_verdict(self, fake_net):
        ports = list(range(9000, 9500))
        fake_net(capacity=20, open_ports={9100, 9200})
        states = _states(_scanner(ports)._syn_scan_blocking(TARGET))
        assert len(states) == len(ports)
        assert states[9100] == "open" and states[9200] == "open"
        assert states[9101] == "closed"

    def test_a_tiny_buffer_is_still_enough(self, fake_net):
        """Capacity 1 is the degenerate case: correctness must come from the
        drain cadence, not from buffer headroom."""
        ports = list(range(9000, 9200))
        net = fake_net(capacity=1, open_ports={9050})
        states = _states(_scanner(ports)._syn_scan_blocking(TARGET))
        assert net["kernel"].dropped == 0
        assert states.get(9050) == "open"


class TestTheDrainDoesNotStarveTheSendLoop:
    def test_sending_still_completes_under_a_reply_flood(self, fake_net):
        ports = list(range(9000, 9300))
        net = fake_net(capacity=10_000)
        _scanner(ports)._syn_scan_blocking(TARGET)
        assert set(net["send"].sent) >= set(ports), "not every port was sent"

    def test_a_resolved_port_is_not_retransmitted(self, fake_net):
        """The drain must remove answered ports from the round, or the
        retransmit loop re-sends ports that already replied."""
        ports = list(range(9000, 9100))
        net = fake_net(capacity=10_000)
        _scanner(ports, retries=2)._syn_scan_blocking(TARGET)
        assert len(net["send"].sent) == len(ports), (
            "ports were retransmitted despite having answered in round 1"
        )


class TestUnchangedContract:
    def test_a_silent_host_still_reports_filtered(self, fake_net):
        """Silence must still mean filtered — the fix removes FALSE filtered,
        not the verdict itself."""
        ports = [9000, 9001, 9002]
        net = fake_net(capacity=100)
        net["send"].sendto = lambda *_a: net["send"].sent.append(0)  # answer nothing
        states = _states(_scanner(ports)._syn_scan_blocking(TARGET))
        assert set(states.values()) == {"filtered"}

    def test_a_foreign_reply_is_ignored(self, fake_net):
        """Cross-host leakage: a reply whose cookie does not recompute must
        never resolve a port."""
        net = fake_net(capacity=100)
        bad = bytearray(_reply(9000, flags=ss.TCP_RST))
        bad[36:40] = (0).to_bytes(4, "big")           # wrong ack -> bad cookie
        net["kernel"].deliver(bytes(bad))
        states = _states(_scanner([9000, 9001])._syn_scan_blocking(TARGET))
        assert states[9000] in ("closed", "filtered")

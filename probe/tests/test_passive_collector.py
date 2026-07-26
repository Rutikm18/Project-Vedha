from __future__ import annotations

import asyncio
import errno

import pytest

from scanner import passive_collector
from scanner.passive_collector import PassiveCollector, PassiveListenerError
from scanner.scanner_base import ScopeGuard
from workflow.execution import ExecutionTrace
from workflow.workflow_engine import _run_passive


class _Writer:
    def __init__(self):
        self.results = []

    def write(self, result):
        self.results.append(result)


class _Socket:
    def __init__(self, fd: int):
        self._fd = fd
        self.closed = False

    def fileno(self):
        return self._fd

    def close(self):
        self.closed = True


def test_subset_listener_failure_reports_degraded_coverage(monkeypatch) -> None:
    sources = [
        (None, 47808, "bacnet"),
        (None, 137, "netbios"),
    ]
    active = _Socket(10)

    def open_listener(_group, port):
        if port == 137:
            raise OSError(errno.EADDRINUSE, "address already in use")
        return active

    monkeypatch.setattr(passive_collector, "PASSIVE_SOURCES", sources)
    monkeypatch.setattr(passive_collector, "_open_listener", open_listener)

    coverage = asyncio.run(PassiveCollector(
        ScopeGuard.from_list(["10.0.0.0/24"]),
        listen_seconds=0,
    ).run(_Writer()))

    assert active.closed is True
    assert coverage["active_count"] == 1
    assert coverage["failed_count"] == 1
    assert coverage["error_code"] == "listener_unavailable"

    trace = ExecutionTrace(["passive_collect"])
    trace.record(
        "passive_collect",
        target_count=1,
        results=[],
        coverage=coverage,
    )
    trace.finalize()
    assert trace.degraded is True
    assert trace.failed is False
    assert trace.as_list()[0]["status"] == "degraded"
    assert trace.as_list()[0]["coverage"]["active_count"] == 1


def test_ot_udp_backend_never_joins_or_transmits(monkeypatch) -> None:
    calls: list[tuple] = []

    class GuardSocket(_Socket):
        def setsockopt(self, level, option, *values):
            assert option != passive_collector.socket.IP_ADD_MEMBERSHIP
            calls.append(("setsockopt", level, option))

        def bind(self, address):
            calls.append(("bind", address))

        def setblocking(self, enabled):
            calls.append(("setblocking", enabled))

        def send(self, *_args, **_kwargs):
            raise AssertionError("passive backend must not call send")

        def sendto(self, *_args, **_kwargs):
            raise AssertionError("passive backend must not call sendto")

        def connect(self, *_args, **_kwargs):
            raise AssertionError("passive backend must not call connect")

    loop = asyncio.new_event_loop()
    sock = GuardSocket(12)
    monkeypatch.setattr(
        passive_collector,
        "PASSIVE_SOURCES",
        [
            ("224.0.0.251", 5353, "mdns"),
            (None, 47808, "bacnet"),
        ],
    )
    monkeypatch.setattr(passive_collector.socket, "socket", lambda *_args: sock)

    try:
        coverage = loop.run_until_complete(PassiveCollector(
            ScopeGuard.from_list(["10.0.0.0/24"]),
            listen_seconds=0,
        ).run(_Writer()))
    finally:
        loop.close()

    with pytest.raises(OSError, match="multicast joins disabled"):
        passive_collector._open_listener("224.0.0.251", 5353)
    assert sock.closed is True
    assert coverage["active_count"] == 1
    assert coverage["failed_sources"][0]["reason"] == "multicast_join_disabled"
    assert all(
        call[0] not in {"send", "sendto", "connect", "IP_ADD_MEMBERSHIP"}
        for call in calls
    )


@pytest.mark.parametrize(
    ("error", "expected_code"),
    [
        (PermissionError(errno.EACCES, "denied"), "permission_denied"),
        (OSError(errno.EADDRINUSE, "in use"), "listener_unavailable"),
    ],
)
def test_zero_listeners_returns_structured_failure(
    monkeypatch,
    error,
    expected_code,
) -> None:
    monkeypatch.setattr(
        passive_collector,
        "PASSIVE_SOURCES",
        [(None, 137, "netbios")],
    )

    def fail_listener(_group, _port):
        raise error

    monkeypatch.setattr(passive_collector, "_open_listener", fail_listener)

    results, coverage = asyncio.run(_run_passive(
        ScopeGuard.from_list(["10.0.0.0/24"]),
        0,
    ))

    assert coverage is None
    assert len(results) == 1
    assert results[0].status == "error"
    assert results[0].data["error_code"] == expected_code
    failure_coverage = results[0].data["details"]["coverage"]
    assert failure_coverage["active_count"] == 0
    assert failure_coverage["failed_count"] == 1


def test_collector_raises_when_no_listener_binds(monkeypatch) -> None:
    monkeypatch.setattr(
        passive_collector,
        "PASSIVE_SOURCES",
        [(None, 137, "netbios")],
    )
    monkeypatch.setattr(
        passive_collector,
        "_open_listener",
        lambda _group, _port: (_ for _ in ()).throw(
            PermissionError(errno.EACCES, "denied")
        ),
    )

    with pytest.raises(PassiveListenerError) as raised:
        asyncio.run(PassiveCollector(
            ScopeGuard.from_list(["10.0.0.0/24"]),
            listen_seconds=0,
        ).run(_Writer()))

    assert raised.value.error_code == "permission_denied"

"""Windows' `WinError 10054` callback tracebacks are not agent errors.

The Proactor loop logs an ERROR traceback whenever a scanned host resets a
connection asyncio is closing. The agent log showed two of them in a normal
deep scan, which reads as a crash. Only that pattern is quieted; any other
asyncio error must still surface as an ERROR.
"""
from __future__ import annotations

import logging

import pytest

from agent.agent import _QuietPeerResets

CALLBACK = ("Exception in callback _ProactorBasePipeTransport._call_connection_lost"
            "(None)")


def _record(exc, msg=CALLBACK):
    try:
        raise exc
    except BaseException as e:  # noqa: BLE001 — building exc_info for the record
        info = (type(e), e, e.__traceback__)
    return logging.LogRecord("asyncio", logging.ERROR, __file__, 1, msg, None, info)


@pytest.fixture
def root_level():
    root = logging.getLogger()
    old = root.level
    yield root
    root.setLevel(old)


def test_reset_is_dropped_at_info(root_level):
    root_level.setLevel(logging.INFO)
    rec = _record(ConnectionResetError(10054, "forcibly closed by the remote host"))
    assert _QuietPeerResets().filter(rec) is False


def test_reset_is_one_debug_line_at_debug(root_level):
    root_level.setLevel(logging.DEBUG)
    rec = _record(ConnectionAbortedError("aborted"))
    assert _QuietPeerResets().filter(rec) is True
    assert rec.levelno == logging.DEBUG and rec.exc_info is None
    assert "peer reset a closing connection" in rec.getMessage()


@pytest.mark.parametrize("exc, msg", [
    (ConnectionResetError("reset"), "Exception in callback something_else()"),
    (RuntimeError("real bug"), CALLBACK),
])
def test_other_asyncio_errors_still_surface(root_level, exc, msg):
    root_level.setLevel(logging.INFO)
    rec = _record(exc, msg)
    assert _QuietPeerResets().filter(rec) is True
    assert rec.levelno == logging.ERROR and rec.exc_info is not None


def test_configure_logging_installs_it_once(monkeypatch):
    from agent import agent
    monkeypatch.setattr(agent, "_attach_log_file", lambda level: None)
    aio = logging.getLogger("asyncio")
    before = list(aio.filters)
    try:
        agent.configure_logging()
        agent.configure_logging()
        assert sum(isinstance(f, _QuietPeerResets) for f in aio.filters) == 1
    finally:
        aio.filters[:] = before

"""
test_main_scripts_errno.py — Phase 2: shared TCP/UDP errno classification.

Verifies the single shared classifier (scanner_base) maps errno -> (state, reason)
correctly, keeps scanner-side/OS failures out of 'filtered', makes an unknown
errno self-identifying, and is the SAME function port_scanner uses.
"""
from __future__ import annotations

import errno
import socket

from main_scripts import scanner_base as sb
from main_scripts import port_scanner as ps


def _oserr(err: int) -> OSError:
    return OSError(err, "boom")


def test_definitive_states():
    assert sb.classify_os_error(_oserr(errno.ECONNREFUSED)) == (sb.CLOSED, "connection_refused")
    assert sb.classify_os_error(_oserr(errno.ETIMEDOUT)) == (sb.FILTERED, "no_response")
    assert sb.classify_os_error(_oserr(errno.EHOSTUNREACH)) == (sb.UNREACHABLE, "host_unreachable")
    assert sb.classify_os_error(_oserr(errno.ENETUNREACH)) == (sb.UNREACHABLE, "network_unreachable")


def test_scanner_side_errors_are_error_not_filtered():
    for e in (errno.EMFILE, errno.ENFILE, errno.ENOBUFS, errno.ENOMEM):
        state, reason = sb.classify_os_error(_oserr(e))
        assert state == sb.ERROR and reason == "local_resource_error"
    assert sb.classify_os_error(_oserr(errno.EADDRNOTAVAIL)) == (sb.ERROR, "address_unavailable")
    assert sb.classify_os_error(_oserr(errno.EACCES)) == (sb.ERROR, "permission_denied")


def test_unknown_errno_is_self_identifying_and_never_filtered():
    state, reason = sb.classify_os_error(_oserr(9999))
    assert state == sb.ERROR and reason == "socket_error_9999"   # not 'filtered', not bare 'os_error'


def test_errno_none_falls_back_to_os_error():
    assert sb.classify_os_error(OSError()) == (sb.ERROR, "os_error")


def test_dns_failure_is_error_not_filtered():
    assert sb.classify_os_error(socket.gaierror(socket.EAI_NONAME, "name")) == (sb.ERROR, "dns_error")


def test_describe_os_error_is_fully_debuggable():
    d = sb.describe_os_error(_oserr(errno.ECONNREFUSED))
    assert d["status"] == sb.CLOSED and d["reason"] == "connection_refused"
    # Python auto-specialises OSError(ECONNREFUSED) -> ConnectionRefusedError;
    # describe_os_error faithfully reports the concrete subclass.
    assert d["errno"] == errno.ECONNREFUSED and d["exc_type"] == "ConnectionRefusedError"
    assert "boom" in d["error"]


def test_port_scanner_uses_the_same_shared_classifier():
    # No drift: TCP classification is literally the shared function.
    assert ps.classify_os_error is sb.classify_os_error
    assert ps._CONFIDENCE is sb.STATE_CONFIDENCE

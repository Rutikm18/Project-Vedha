"""
test_tls_connect_hook.py — the injectable `connect` hook that lets tls_scanner
measure TLS tunnelled inside another protocol (gap #3: SCHANNEL behind RDP).

Pure/offline: the hook is exercised without a real TLS server by having it
record its arguments and raise, which _try_version must treat as "server refused
this version" (None), never as _UNTESTABLE (that is reserved for the scanner's own
TLS policy).
"""
from __future__ import annotations

import ssl

from scanner import tls_scanner as ts


def test_try_version_invokes_connect_hook_with_args():
    seen = {}

    def hook(host, port, timeout):
        seen["args"] = (host, port, timeout)
        raise OSError("prelude failed")

    res = ts._try_version("10.0.0.1", 3389, ssl.TLSVersion.TLSv1_2, 2.5, connect=hook)
    assert seen["args"] == ("10.0.0.1", 3389, 2.5)
    # A connect failure is the server refusing the version, not an untestable one.
    assert res is None
    assert res is not ts._UNTESTABLE


def test_scan_tls_sync_threads_hook_and_returns_none_when_unreachable():
    calls = {"n": 0}

    def hook(host, port, timeout):
        calls["n"] += 1
        raise OSError("prelude failed")

    # Every version probe fails via the hook → not a TLS service from here → None.
    assert ts._scan_tls_sync("10.0.0.1", 3389, 2.0, connect=hook) is None
    assert calls["n"] >= 1  # the hook was actually used in place of create_connection


def test_default_connect_used_when_hook_absent(monkeypatch):
    # Without a hook, _try_version must fall back to the module's default connect.
    used = {}

    def fake_default(host, port, timeout):
        used["args"] = (host, port, timeout)
        raise OSError("no server in test")

    monkeypatch.setattr(ts, "_default_connect", fake_default)
    ts._try_version("10.0.0.2", 443, ssl.TLSVersion.TLSv1_2, 1.0)
    assert used["args"] == ("10.0.0.2", 443, 1.0)

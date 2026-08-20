"""test_resolve.py — resolve() address-family selection (task A9)."""
from __future__ import annotations

import socket

import pytest

from scanner import scanner_base as sb


def _infos(*families):
    """Fake getaddrinfo results: (family, socktype, proto, canonname, sockaddr)."""
    out = []
    for fam in families:
        addr = ("::1", 0, 0, 0) if fam == socket.AF_INET6 else ("127.0.0.1", 0)
        out.append((fam, socket.SOCK_STREAM, 6, "", addr))
    return out


class TestResolveFamily:
    def test_requested_ipv4_selected_over_v6_first(self, monkeypatch):
        # AAAA sorts first (RFC 6724), but an IPv4-only raw scanner must still get v4.
        monkeypatch.setattr(socket, "getaddrinfo",
                            lambda *a, **k: _infos(socket.AF_INET6, socket.AF_INET))
        fam, sockaddr = sb.resolve("dual.example", 0, family=socket.AF_INET)
        assert fam == socket.AF_INET and sockaddr[0] == "127.0.0.1"

    def test_requested_family_absent_falls_back_to_first(self, monkeypatch):
        monkeypatch.setattr(socket, "getaddrinfo",
                            lambda *a, **k: _infos(socket.AF_INET6))
        fam, _ = sb.resolve("v6only.example", 0, family=socket.AF_INET)
        assert fam == socket.AF_INET6            # no v4 → first result (belt-and-suspenders)

    def test_default_no_family_is_backward_compatible(self, monkeypatch):
        monkeypatch.setattr(socket, "getaddrinfo",
                            lambda *a, **k: _infos(socket.AF_INET6, socket.AF_INET))
        fam, _ = sb.resolve("dual.example", 0)
        assert fam == socket.AF_INET6            # unchanged: first (RFC-6724) result

    def test_unresolvable_raises(self, monkeypatch):
        monkeypatch.setattr(socket, "getaddrinfo", lambda *a, **k: [])
        with pytest.raises(OSError):
            sb.resolve("nx.example", 0)

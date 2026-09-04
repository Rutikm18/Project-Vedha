"""
test_dualstack_fallback.py — roadmap #9 / #4.1, the CALL-SITE migration.

`resolve()` returns only getaddrinfo's first address. On a dual-stack host whose
AAAA sorts first but whose IPv6 path is black-holed (no route, filtered ICMPv6,
broken tunnel), every scanner that took that first address reported the service
as absent — a false negative indistinguishable, to an operator, from a host that
genuinely isn't running it.

These prove each migrated call site now walks the candidate list and keeps the
first address that ANSWERS. Pure/deterministic: no DNS, no network.
"""
from __future__ import annotations

import asyncio
import socket

import pytest

from scanner import os_fingerprint as osf
from scanner import rdp_scanner as rdp
from scanner import smb_scanner as smb
from scanner import tls_fingerprint as tf
from scanner.scanner_base import ScopeGuard, resolve_ip_candidates

V6, V4 = "2001:db8::1", "192.0.2.1"
_SCOPE = lambda: ScopeGuard.from_list(["192.0.2.0/24", "2001:db8::/32"])


# ── the helper itself ────────────────────────────────────────────────────────
class TestResolveIpCandidates:
    def test_returns_ips_in_order(self, monkeypatch):
        monkeypatch.setattr(socket, "getaddrinfo", lambda *a, **k: [
            (socket.AF_INET6, 1, 6, "", (V6, 445, 0, 0)),
            (socket.AF_INET, 1, 6, "", (V4, 445))])
        assert resolve_ip_candidates("h", 445) == [V6, V4]

    def test_unresolvable_returns_empty_not_raises(self, monkeypatch):
        def _boom(*a, **k):
            raise socket.gaierror("nope")
        monkeypatch.setattr(socket, "getaddrinfo", _boom)
        assert resolve_ip_candidates("nx.invalid", 445) == []


# ── SMB: sockaddr-shaped call site ───────────────────────────────────────────
class TestSmbNegotiateFallback:
    def _patch_candidates(self, monkeypatch):
        monkeypatch.setattr(smb, "resolve_candidates", lambda t, p, proto="tcp": [
            (socket.AF_INET6, (V6, p, 0, 0)), (socket.AF_INET, (V4, p))])

    def _fake_socket(self, monkeypatch, dead_family):
        """A socket whose connect() fails for `dead_family`, succeeds otherwise."""
        attempted = []

        class _Sock:
            def __init__(self, family, type_):
                self.family = family
            def settimeout(self, t): pass
            def connect(self, sa):
                attempted.append(self.family)
                if self.family == dead_family:
                    raise OSError("network unreachable")
            def sendall(self, b): pass
            def recv(self, n): return b"\x00\x00\x00\x2a\xffSMB-negotiated"
            def close(self): pass

        monkeypatch.setattr(smb.socket, "socket", _Sock)
        return attempted

    def test_falls_back_to_ipv4_when_ipv6_is_blackholed(self, monkeypatch):
        self._patch_candidates(monkeypatch)
        attempted = self._fake_socket(monkeypatch, dead_family=socket.AF_INET6)
        sc = smb.SMBScanner(_SCOPE(), timeout=0.1)
        out = sc._negotiate("host.example", b"payload")
        assert out is not None, "IPv4 answered but the scanner reported nothing"
        assert attempted == [socket.AF_INET6, socket.AF_INET]   # tried v6 first

    def test_returns_none_only_when_every_family_fails(self, monkeypatch):
        self._patch_candidates(monkeypatch)
        attempted: list = []

        def _sock(family, type_):
            class _S:
                def settimeout(self, t): pass
                def connect(self, sa):
                    attempted.append(family); raise OSError("unreachable")
                def close(self): pass
            return _S()
        monkeypatch.setattr(smb.socket, "socket", _sock)
        sc = smb.SMBScanner(_SCOPE(), timeout=0.1)
        assert sc._negotiate("host.example", b"p") is None
        assert len(attempted) == 2                     # both families attempted


# ── SMB NTLM build: ip-string-shaped call site ───────────────────────────────
class TestSmbNtlmFallback:
    def test_first_answering_address_wins(self, monkeypatch):
        monkeypatch.setattr(smb, "resolve_ip_candidates",
                            lambda t, p, proto="tcp": [V6, V4])
        tried = []

        def _ntlm(ip, port, timeout):
            tried.append(ip)
            return {"os_build": 26100} if ip == V4 else {}
        monkeypatch.setattr(smb, "ntlm_os_build", _ntlm)
        sc = smb.SMBScanner(_SCOPE(), timeout=0.1)
        assert sc._ntlm_fingerprint("host.example") == {"os_build": 26100}
        assert tried == [V6, V4]

    def test_empty_when_no_address_answers(self, monkeypatch):
        monkeypatch.setattr(smb, "resolve_ip_candidates",
                            lambda t, p, proto="tcp": [V6, V4])
        monkeypatch.setattr(smb, "ntlm_os_build", lambda ip, port, timeout: {})
        assert smb.SMBScanner(_SCOPE(), timeout=0.1)._ntlm_fingerprint("h") == {}


# ── os_fingerprint SMB build ─────────────────────────────────────────────────
class TestOsFingerprintSmbBuildFallback:
    def test_falls_back_across_families(self, monkeypatch):
        monkeypatch.setattr(osf, "resolve_ip_candidates",
                            lambda t, p, proto="tcp": [V6, V4])
        tried = []

        def _ntlm(ip, port, timeout):
            tried.append(ip)
            return {"os_build": 26100} if ip == V4 else {}
        monkeypatch.setattr(smb, "ntlm_os_build", _ntlm)
        sc = osf.OSFingerprintScanner(_SCOPE(), timeout=0.1)
        sc.smb_build = True
        assert sc._smb_build("host.example")["os_build"] == 26100
        assert tried == [V6, V4]


# ── RDP ──────────────────────────────────────────────────────────────────────
class TestRdpFallback:
    def test_probes_next_family_when_first_is_silent(self, monkeypatch):
        monkeypatch.setattr(rdp, "resolve_ip_candidates",
                            lambda t, p, proto="tcp": [V6, V4])
        tried = []

        def _probe(ip, port, timeout):
            tried.append(ip)
            return {"nla": True, "selected_protocol": 2} if ip == V4 else None
        monkeypatch.setattr(rdp, "probe_rdp_posture", _probe)
        sc = rdp.RDPScanner(_SCOPE(), timeout=0.1)
        res = asyncio.run(sc._scan_port("host.example", 3389))
        assert res is not None and res.status == "open"
        assert tried == [V6, V4]

    def test_none_when_no_family_speaks_rdp(self, monkeypatch):
        monkeypatch.setattr(rdp, "resolve_ip_candidates",
                            lambda t, p, proto="tcp": [V6, V4])
        monkeypatch.setattr(rdp, "probe_rdp_posture",
                            lambda ip, port, timeout: None)
        sc = rdp.RDPScanner(_SCOPE(), timeout=0.1)
        assert asyncio.run(sc._scan_port("host.example", 3389)) is None

    def test_unresolvable_host_is_survivable(self, monkeypatch):
        monkeypatch.setattr(rdp, "resolve_ip_candidates",
                            lambda t, p, proto="tcp": [])
        sc = rdp.RDPScanner(_SCOPE(), timeout=0.1)
        assert asyncio.run(sc._scan_port("nx.invalid", 3389)) is None


# ── TLS fingerprint ──────────────────────────────────────────────────────────
_NULL = "0" * 62


class TestTlsFingerprintFallback:
    def test_uses_the_family_that_actually_speaks_tls(self, monkeypatch):
        monkeypatch.setattr(tf, "resolve_ip_candidates",
                            lambda t, p, proto="tcp": [V6, V4])
        tried = []

        def _fp(target, ip, port, timeout):
            tried.append(ip)
            return (_NULL, []) if ip == V6 else ("a" * 62, [1])
        monkeypatch.setattr(tf, "fingerprint_host", _fp)
        monkeypatch.setattr(tf, "compute_ja4s", lambda *a, **k: None)
        sc = tf.TLSFingerprintScanner(_SCOPE(), timeout=0.1)
        res = asyncio.run(sc._scan_port("host.example", 443))
        assert res is not None
        assert tried == [V6, V4]

    def test_none_when_no_family_speaks_tls(self, monkeypatch):
        monkeypatch.setattr(tf, "resolve_ip_candidates",
                            lambda t, p, proto="tcp": [V6, V4])
        monkeypatch.setattr(tf, "fingerprint_host",
                            lambda target, ip, port, timeout: (_NULL, []))
        sc = tf.TLSFingerprintScanner(_SCOPE(), timeout=0.1)
        assert asyncio.run(sc._scan_port("host.example", 443)) is None

    def test_unresolvable_host_is_survivable(self, monkeypatch):
        monkeypatch.setattr(tf, "resolve_ip_candidates",
                            lambda t, p, proto="tcp": [])
        sc = tf.TLSFingerprintScanner(_SCOPE(), timeout=0.1)
        assert asyncio.run(sc._scan_port("nx.invalid", 443)) is None


# ── SYN scanner requests IPv4 rather than accepting AAAA-first ───────────────
class TestSynScannerRequestsIPv4:
    def test_resolve_is_asked_for_ipv4(self, monkeypatch):
        from scanner import syn_scanner as ss
        seen = {}

        def _resolve(t, p, proto="tcp", family=None):
            seen["family"] = family
            return socket.AF_INET, (V4, 0)
        monkeypatch.setattr(ss, "resolve", _resolve)
        monkeypatch.setattr(ss, "_local_source_ip", lambda dst: "192.0.2.9")

        class _S:
            def setsockopt(self, *a): pass
            def setblocking(self, *a): pass
            def sendto(self, *a): pass
            def recv(self, n): raise OSError("done")
            def fileno(self): return -1
            def close(self): pass
        monkeypatch.setattr(ss.socket, "socket", lambda *a: _S())

        sc = ss.SynScanner(_SCOPE(), ports=[80], key=b"k" * 16, timeout=0.01)
        sc._syn_scan_blocking("host.example")
        assert seen["family"] == socket.AF_INET, (
            "the v4-only raw path must REQUEST IPv4, or a dual-stack host whose "
            "AAAA sorts first is needlessly kicked to the connect fallback")

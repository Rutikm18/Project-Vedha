"""
test_rdp_schannel.py — gap #3: measure the TLS (SCHANNEL) behind RDP.

Offline/pure: real sockets and TLS are replaced by fakes. Covers
(1) the `_rdp_tls_connect` hook's negotiate-then-hand-back-socket behaviour, and
(2) RDPScanner emitting a `tls_scan`-typed fact (transport="rdp") on 3389 when RDP
negotiates a TLS-capable security protocol, so findings.py grades SCHANNEL.
"""
from __future__ import annotations

import asyncio

import pytest

from scanner import rdp_scanner as rdp
from scanner.scanner_base import ScopeGuard

_SCOPE = lambda: ScopeGuard.from_list(["192.0.2.0/24"])


class _FakeSock:
    def __init__(self, cc: bytes = b"cc"):
        self._cc = cc
        self.closed = False
        self.sent = b""

    def settimeout(self, t):
        pass

    def sendall(self, b):
        self.sent += b

    def recv(self, n):
        return self._cc

    def close(self):
        self.closed = True


def test_rdp_tls_connect_returns_live_socket_when_tls_selected(monkeypatch):
    fake = _FakeSock()
    monkeypatch.setattr(rdp.socket, "create_connection", lambda addr, timeout: fake)
    monkeypatch.setattr(rdp, "parse_connection_confirm",
                        lambda data: {"rdp_confirmed": True, "tls": True})
    sock = rdp._rdp_tls_connect("192.0.2.5", 3389, 1.0)
    assert sock is fake
    assert fake.closed is False           # handed to the TLS layer, not closed
    assert fake.sent                      # an X.224 connection request went out


def test_rdp_tls_connect_raises_and_closes_when_not_tls(monkeypatch):
    fake = _FakeSock()
    monkeypatch.setattr(rdp.socket, "create_connection", lambda addr, timeout: fake)
    monkeypatch.setattr(rdp, "parse_connection_confirm",
                        lambda data: {"rdp_confirmed": True, "tls": False,
                                      "standard_rdp_security": True})
    with pytest.raises(OSError):
        rdp._rdp_tls_connect("192.0.2.5", 3389, 1.0)
    assert fake.closed is True            # no TLS → socket released


def test_rdp_tls_connect_raises_and_closes_when_not_rdp(monkeypatch):
    fake = _FakeSock()
    monkeypatch.setattr(rdp.socket, "create_connection", lambda addr, timeout: fake)
    monkeypatch.setattr(rdp, "parse_connection_confirm", lambda data: None)
    with pytest.raises(OSError):
        rdp._rdp_tls_connect("192.0.2.5", 3389, 1.0)
    assert fake.closed is True


def _fake_schannel_info():
    return {
        "accepted_versions": ["TLSv1_0", "TLSv1_2"],
        "versions_not_tested": [],
        "cipher_by_version": {"TLSv1.0": "AES128-SHA"},
        "cipher_analysis": [],
        "posture": {"grade": "F",
                    "findings": ["deprecated protocol enabled (SSLv3/TLS1.0)"]},
        "certificate": {},
    }


def test_scan_port_emits_schannel_tls_fact(monkeypatch):
    monkeypatch.setattr(rdp, "resolve_ip_candidates",
                        lambda t, p, proto="tcp": ["192.0.2.5"])
    monkeypatch.setattr(rdp, "probe_rdp_posture",
                        lambda ip, port, timeout: {
                            "rdp_confirmed": True, "tls": True, "nla": True,
                            "selected_protocol": 2})
    monkeypatch.setattr(rdp, "_scan_tls_sync",
                        lambda host, port, timeout, connect: _fake_schannel_info())

    sc = rdp.RDPScanner(_SCOPE(), timeout=0.1)
    res = asyncio.run(sc._scan_port("host.example", 3389))

    assert len(res) == 2
    rdp_fact = next(r for r in res if r.scanner == "rdp_scan")
    tls_fact = next(r for r in res if r.scanner == "tls_scan")
    assert rdp_fact.status == "open"
    assert tls_fact.port == 3389
    assert tls_fact.data["transport"] == "rdp"
    assert tls_fact.data["posture"]["grade"] == "F"
    assert "SCHANNEL (RDP)" in tls_fact.evidence


def test_scan_port_no_tls_fact_when_standard_rdp(monkeypatch):
    # standard-RDP security (no TLS) → only the rdp_scan fact, no SCHANNEL scan.
    monkeypatch.setattr(rdp, "resolve_ip_candidates",
                        lambda t, p, proto="tcp": ["192.0.2.5"])
    monkeypatch.setattr(rdp, "probe_rdp_posture",
                        lambda ip, port, timeout: {
                            "rdp_confirmed": True, "tls": False,
                            "standard_rdp_security": True})

    def _must_not_run(*a, **k):
        raise AssertionError("_scan_tls_sync must not run when RDP has no TLS")
    monkeypatch.setattr(rdp, "_scan_tls_sync", _must_not_run)

    sc = rdp.RDPScanner(_SCOPE(), timeout=0.1)
    res = asyncio.run(sc._scan_port("host.example", 3389))
    assert len(res) == 1
    assert res[0].scanner == "rdp_scan"


# ---------------------------------------------------------------------------
# Phase 3: the SCHANNEL (RDP-transport) tls_scan fact is graded by findings.py's
# existing TLS rules — the deep-scan router never runs tls_scan on 3389, so this
# is what actually closes gap #3 in the detection output.
# ---------------------------------------------------------------------------
from scanner.findings import run_findings


def _schannel_fact(accepted, cipher_analysis=None):
    return {
        "scanner": "tls_scan", "target": "192.0.2.5", "port": 3389,
        "proto": "tcp", "status": "open",
        "data": {
            "accepted_versions": accepted,
            "cipher_analysis": cipher_analysis or [],
            "certificate": {},
            "transport": "rdp",
        },
    }


def test_findings_grade_deprecated_schannel_on_3389():
    fact = _schannel_fact(["TLSv1_0", "TLSv1_2"])
    findings = run_findings([fact])
    hit = [f for f in findings if f.rule_id == "TLS-LEGACY-PROTO" and f.port == 3389]
    assert hit, "deprecated SCHANNEL TLS on RDP 3389 should raise TLS-LEGACY-PROTO"


def test_findings_grade_weak_schannel_cipher_on_3389():
    fact = _schannel_fact(
        ["TLSv1_2"],
        cipher_analysis=[{"name": "RC4-MD5", "weak": True,
                          "weak_reasons": ["RC4 (broken stream cipher)"]}])
    findings = run_findings([fact])
    hit = [f for f in findings if f.rule_id == "TLS-WEAK-CIPHER" and f.port == 3389]
    assert hit, "weak SCHANNEL cipher on RDP 3389 should raise TLS-WEAK-CIPHER"


def test_findings_grade_underscore_form_tls_version_on_443():
    # Regression: the real tls_scanner emits stdlib underscore labels ("TLSv1_0"),
    # not the dotted form hand-built tests used — _rule_tls must grade both, or
    # TLS 1.0/1.1 goes undetected on EVERY port (the latent bug this fold fixes).
    fact = {"scanner": "tls_scan", "target": "10.0.0.9", "port": 443,
            "proto": "tcp", "status": "open",
            "data": {"accepted_versions": ["TLSv1_0", "TLSv1_2"]}}
    findings = run_findings([fact])
    assert any(f.rule_id == "TLS-LEGACY-PROTO" for f in findings)

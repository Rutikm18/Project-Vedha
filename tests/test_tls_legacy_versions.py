"""
test_tls_legacy_versions.py — the deprecated-TLS detection must measure the
SERVER, never the scanning host's own crypto policy.

Modern OpenSSL builds ship SECLEVEL=2, which refuses TLS 1.0/1.1 *client-side*:
the handshake dies with NO_PROTOCOLS_AVAILABLE before a packet leaves the probe.
tls_scanner used to swallow that in a blanket `except Exception: return None` and
record it as "the server does not accept this version", so a server happily
speaking TLS 1.0 was reported as TLS-1.2-only and graded B. That made
POSTURE-TLS-DEPRECATED-VERSION and POSTURE-TLS-WEAK-CIPHER unreachable, and — worse
— indistinguishable from a correctly hardened host.

These tests pin a loopback server to one legacy version and assert the scanner
sees it, plus assert the client-side-refusal path is reported separately rather
than being laundered into a clean result.
"""

from __future__ import annotations

import socket
import ssl
import threading
from datetime import datetime, timedelta, timezone

import pytest

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID

from scanner import tls_scanner as ts


def _self_signed(tmp_path):
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "legacy.vedha.test")])
    now = datetime.now(timezone.utc)
    cert = (x509.CertificateBuilder()
            .subject_name(name).issuer_name(name)
            .public_key(key.public_key())
            .serial_number(x509.random_serial_number())
            .not_valid_before(now - timedelta(days=1))
            .not_valid_after(now + timedelta(days=30))
            .sign(key, hashes.SHA256()))
    cert_path, key_path = tmp_path / "cert.pem", tmp_path / "key.pem"
    cert_path.write_bytes(cert.public_bytes(serialization.Encoding.PEM))
    key_path.write_bytes(key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.TraditionalOpenSSL,
        serialization.NoEncryption()))
    return str(cert_path), str(key_path)


class _LegacyTLSServer:
    """A loopback server pinned to exactly one (legacy) TLS version."""

    def __init__(self, cert, key, version):
        self._ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        self._ctx.load_cert_chain(cert, key)
        self._ctx.set_ciphers("ALL:@SECLEVEL=0")
        self._ctx.minimum_version = version
        self._ctx.maximum_version = version
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind(("127.0.0.1", 0))
        self._sock.listen(16)
        self._sock.settimeout(0.3)
        self.port = self._sock.getsockname()[1]
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._serve, daemon=True)

    def _serve(self):
        while not self._stop.is_set():
            try:
                conn, _ = self._sock.accept()
            except socket.timeout:
                continue
            except OSError:
                break
            try:
                with self._ctx.wrap_socket(conn, server_side=True) as s:
                    s.recv(16)
            except (ssl.SSLError, OSError):
                pass

    def __enter__(self):
        self._thread.start()
        return self

    def __exit__(self, *exc):
        self._stop.set()
        self._thread.join(timeout=2)
        self._sock.close()


def _server_supports(version) -> bool:
    """Skip rather than fail on a build with the legacy protocol compiled out."""
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    try:
        ctx.set_ciphers("ALL:@SECLEVEL=0")
        ctx.minimum_version = version
        ctx.maximum_version = version
        return True
    except (ValueError, ssl.SSLError, OSError):
        return False


@pytest.mark.parametrize("label,version", [
    ("TLSv1_0", ssl.TLSVersion.TLSv1),
    ("TLSv1_1", ssl.TLSVersion.TLSv1_1),
])
def test_legacy_version_is_detected_not_masked_by_client_policy(tmp_path, label, version):
    if not _server_supports(version):
        pytest.skip(f"this OpenSSL build cannot serve {label}")
    cert, key = _self_signed(tmp_path)
    with _LegacyTLSServer(cert, key, version) as srv:
        info = ts._scan_tls_sync("127.0.0.1", srv.port, timeout=3.0)
    assert info is not None, f"{label}-only server was not recognised as TLS at all"
    assert label in info["accepted_versions"], (
        f"{label} server reported as {info['accepted_versions']} — the probe's own "
        f"crypto policy is being reported as the server's")


def test_try_version_reports_client_side_refusal_separately(monkeypatch):
    """A version the probe cannot OFFER is 'not tested', not 'server refused'."""
    def _refuse(*a, **kw):
        raise ssl.SSLError(1, "[SSL: NO_PROTOCOLS_AVAILABLE] no protocols available")

    monkeypatch.setattr(ts.socket, "create_connection", _refuse)
    out = ts._try_version("127.0.0.1", 443, ssl.TLSVersion.TLSv1_2, 1.0)
    assert out is ts._UNTESTABLE
    assert out is not None, "client-side refusal must not look like a server rejection"


def test_try_version_reports_server_rejection_as_none(monkeypatch):
    def _reject(*a, **kw):
        raise ConnectionRefusedError("connection refused")

    monkeypatch.setattr(ts.socket, "create_connection", _reject)
    assert ts._try_version("127.0.0.1", 443, ssl.TLSVersion.TLSv1_2, 1.0) is None


def test_untested_versions_are_surfaced_in_the_fact(tmp_path, monkeypatch):
    """When the probe genuinely cannot test a version, the result must say so
    instead of quietly implying the server refused it."""
    cert, key = _self_signed(tmp_path)
    real = ts._try_version

    def _fake(host, port, version, timeout):
        if version == ssl.TLSVersion.TLSv1:
            return ts._UNTESTABLE
        return real(host, port, version, timeout)

    monkeypatch.setattr(ts, "_try_version", _fake)
    with _LegacyTLSServer(cert, key, ssl.TLSVersion.TLSv1_2) as srv:
        info = ts._scan_tls_sync("127.0.0.1", srv.port, timeout=3.0)
    assert info is not None
    assert "TLSv1_0" in info["versions_not_tested"]
    assert "TLSv1_0" not in info["accepted_versions"]

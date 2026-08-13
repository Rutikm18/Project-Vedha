"""
test_tls_integration.py — Tier 2.4 live check: run the real TLSScanner against a
loopback TLS server (ephemeral self-signed cert) and confirm posture is computed.
Skips cleanly if 'cryptography' is unavailable.
"""

from __future__ import annotations

import asyncio
import socket
import ssl
import threading

import pytest

crypto = pytest.importorskip("cryptography")

from datetime import datetime, timedelta, timezone

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID

from scanner.scanner_base import ScopeGuard
from scanner.tls_scanner import TLSScanner


def _self_signed(tmp_path):
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "vedha.test")])
    now = datetime.now(timezone.utc)
    cert = (x509.CertificateBuilder()
            .subject_name(name).issuer_name(name)
            .public_key(key.public_key())
            .serial_number(x509.random_serial_number())
            .not_valid_before(now - timedelta(days=1))
            .not_valid_after(now + timedelta(days=30))
            .sign(key, hashes.SHA256()))
    cert_path = tmp_path / "cert.pem"
    key_path = tmp_path / "key.pem"
    cert_path.write_bytes(cert.public_bytes(serialization.Encoding.PEM))
    key_path.write_bytes(key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.TraditionalOpenSSL,
        serialization.NoEncryption()))
    return str(cert_path), str(key_path)


class _TLSServer:
    def __init__(self, cert, key):
        self._ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        self._ctx.load_cert_chain(cert, key)
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
        self._sock.close()
        self._thread.join(timeout=2)


def test_tls_scanner_reports_posture_grade(tmp_path):
    cert, key = _self_signed(tmp_path)

    async def _run(port):
        scope = ScopeGuard.from_list(["127.0.0.0/8"])
        scanner = TLSScanner(scope, ports=[port], timeout=3.0)
        return await scanner.scan_target("127.0.0.1")

    with _TLSServer(cert, key) as server:
        results = asyncio.run(_run(server.port))

    assert results, "expected a TLS result"
    data = results[0].data
    assert "posture" in data
    assert data["posture"]["grade"] in {"A", "B", "C", "F"}
    # A modern Python default server negotiates TLS1.2/1.3, so posture is good.
    assert data["posture"]["grade"] in {"A", "B"}
    assert data["cipher_analysis"]              # at least one classified cipher
    assert any(v.startswith("TLSv1_2") or v.startswith("TLSv1_3")
               for v in data["accepted_versions"])


# ── Tier 2.3: active TLS fingerprint against the same loopback server ──────────

def test_tls_fingerprint_is_nonzero_and_stable(tmp_path):
    import scanner.tls_fingerprint as tf

    cert, key = _self_signed(tmp_path)
    with _TLSServer(cert, key) as server:
        # A single crafted ClientHello must elicit a parseable ServerHello — this
        # proves the raw-TLS byte layout is accepted by a real OpenSSL server.
        parsed = tf._one_probe("127.0.0.1", "127.0.0.1", server.port,
                               {"supported_versions": [0x0304, 0x0303]}, 1.0)
        assert parsed is not None, "server did not return a parseable ServerHello"
        assert parsed["cipher"] in tf.CIPHER_LIST

        digest1, results1 = tf.fingerprint_host("127.0.0.1", "127.0.0.1",
                                                server.port, timeout=1.0)
        digest2, _ = tf.fingerprint_host("127.0.0.1", "127.0.0.1",
                                         server.port, timeout=1.0)

    assert len(digest1) == 62
    assert digest1 != "0" * 62                    # at least one probe answered
    assert sum(1 for r in results1 if r) >= 1
    assert digest1 == digest2                     # deterministic for one server

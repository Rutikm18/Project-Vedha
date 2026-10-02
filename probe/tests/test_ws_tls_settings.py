"""The WebSocket must trust what the HTTPS client trusts.

Behind a TLS-inspecting proxy the installer's --ca-bundle sets PROBE_CA_BUNDLE.
httpx used it; websockets.connect() did not, so wss:// failed and the agent fell
back to long-polling without saying why.
"""
from __future__ import annotations

import ssl
import subprocess

import pytest

from agent.transport import Transport, _websocket_ssl_context


def _self_signed_ca(tmp_path):
    key, cert = tmp_path / "ca.key", tmp_path / "ca.pem"
    result = subprocess.run(
        ["openssl", "req", "-x509", "-newkey", "rsa:2048", "-nodes", "-keyout", str(key),
         "-out", str(cert), "-days", "1", "-subj", "/CN=corp-inspection-ca"],
        capture_output=True, check=False,
    )
    if result.returncode != 0:
        pytest.skip("openssl not available to mint a test CA")
    return cert


def test_default_https_verifies_and_http_has_no_context():
    context = _websocket_ssl_context("https://api.vedhasec.com", True, None)
    assert isinstance(context, ssl.SSLContext)
    assert context.verify_mode == ssl.CERT_REQUIRED and context.check_hostname
    assert _websocket_ssl_context("http://10.0.0.5:18080", "/x.pem", None) is None


def test_default_context_also_trusts_certifi_when_installed():
    """macOS: a bare context skips the system keychain, so a valid cert failed
    verification. certifi's bundle is loaded on top of the system store."""
    pytest.importorskip("certifi")
    import certifi
    subjects = {tuple(c["subject"]) for c in _websocket_ssl_context("https://x.example", True, None).get_ca_certs()}
    with open(certifi.where()) as handle:
        assert "BEGIN CERTIFICATE" in handle.read()
    assert subjects                                           # certifi roots were loaded


def test_ca_bundle_is_trusted_by_the_websocket(tmp_path):
    ca = _self_signed_ca(tmp_path)
    context = _websocket_ssl_context("https://api.vedhasec.com", str(ca), None)
    assert isinstance(context, ssl.SSLContext)
    assert context.verify_mode == ssl.CERT_REQUIRED and context.check_hostname
    subjects = [dict(x[0] for x in c["subject"]).get("commonName") for c in context.get_ca_certs()]
    assert "corp-inspection-ca" in subjects


def test_verify_off_is_mirrored():
    context = _websocket_ssl_context("https://api.example", False, None)
    assert context.verify_mode == ssl.CERT_NONE and not context.check_hostname


def test_transport_builds_the_context_from_its_ca_bundle(tmp_path):
    ca = _self_signed_ca(tmp_path)
    transport = Transport("https://api.vedhasec.com", ca_bundle=str(ca))
    assert isinstance(transport._ws_ssl, ssl.SSLContext)

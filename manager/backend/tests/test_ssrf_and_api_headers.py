"""
Hardening contract: SSRF guard for operator-supplied URLs and API security headers.

Integration URLs (Slack webhook, Jira/ServiceNow base URL) and the engagement
`critical_webhook_url` are fetched by the manager itself, so an operator could
aim them at the cloud metadata service or loopback services. The API also sent
no security headers of its own (only the Caddy TLS path added some).
"""
from __future__ import annotations

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.security_headers import SecurityHeadersMiddleware
from app.services import notifications
from app.services import outbound_guard as og
from app.services.outbound_guard import OutboundBlocked, check_url

_REAL_RESOLVE = og._resolve     # conftest swaps in a stub resolver for every other test


# ── SSRF guard ────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("url", [
    "http://169.254.169.254/latest/meta-data/",      # cloud metadata
    "http://127.0.0.1:8000/auth/login",              # loopback API
    "http://[::1]/",
    "http://[::ffff:169.254.169.254]/",              # IPv4-mapped metadata
    "http://0.0.0.0/",
    "file:///etc/passwd",
    "gopher://example.com/",
    "http://user:pw@example.com/",
    "http:///nohost",
    "",
])
def test_always_refused(url):
    with pytest.raises(OutboundBlocked):
        check_url(url)


@pytest.mark.parametrize("url", ["http://10.0.0.5/hook", "http://192.168.1.10/", "http://[fd00::1]/"])
def test_private_refused_unless_allowed(url):
    with pytest.raises(OutboundBlocked):
        check_url(url, public_only=True)            # a Slack webhook / critical webhook
    assert check_url(url) == url                    # self-hosted Jira on a LAN (the default policy)


def test_public_literal_allowed():
    url = "https://93.184.216.34/services/T000/B000/xxx"
    assert check_url(url, public_only=True) == url


def test_hostname_resolving_to_internal_address_refused(monkeypatch):
    import ipaddress
    monkeypatch.setattr(og, "_resolve", lambda host, port: [ipaddress.ip_address("169.254.169.254")])
    with pytest.raises(OutboundBlocked):
        check_url("https://totally-legit.example.com/hook")


def test_unresolvable_host_refused(monkeypatch):
    import socket

    def boom(*a, **k):
        raise socket.gaierror("nope")
    monkeypatch.setattr(og, "_resolve", _REAL_RESOLVE)
    monkeypatch.setattr(og.socket, "getaddrinfo", boom)
    with pytest.raises(OutboundBlocked):
        check_url("https://does-not-exist.invalid/")


def test_delivery_re_checks_at_send_time():
    """A URL saved before the guard (or whose DNS changed) must not be called."""
    assert notifications.deliver("slack", {}, "http://169.254.169.254/", "s", "b") is False


# ── Security headers ──────────────────────────────────────────────────────────

def _client() -> TestClient:
    app = FastAPI()
    app.add_middleware(SecurityHeadersMiddleware)

    @app.get("/thing")
    def thing():
        return {"ok": True}

    @app.get("/docs")
    def docs():
        return {"ok": True}

    return TestClient(app)


def test_api_responses_carry_baseline_headers():
    h = _client().get("/thing").headers
    assert h["x-content-type-options"] == "nosniff"
    assert h["x-frame-options"] == "DENY"
    assert h["referrer-policy"] == "no-referrer"
    assert "frame-ancestors 'none'" in h["content-security-policy"]
    assert h["cache-control"] == "no-store"


def test_hsts_only_over_https():
    assert "strict-transport-security" not in _client().get("/thing").headers
    https = TestClient(_client().app, base_url="https://testserver")
    assert "max-age=31536000" in https.get("/thing").headers["strict-transport-security"]


def test_docs_keep_working_without_the_strict_csp():
    h = _client().get("/docs").headers
    assert "content-security-policy" not in h
    assert h["x-content-type-options"] == "nosniff"

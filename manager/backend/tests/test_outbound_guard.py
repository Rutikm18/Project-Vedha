"""SSRF guard for tenant-supplied outbound targets, and encrypted SIEM/EDR secrets.

Tenant admins type in SIEM/EDR base URLs, Jira/ServiceNow URLs, a Slack webhook and an
SMTP host; the Manager then calls them from inside its own network. They used to be
called as given, so 127.0.0.1, the metadata service and internal hosts were reachable.
"""
from __future__ import annotations

import socket
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest
from fastapi import HTTPException

from app.detection import config_secrets
from app.detection.edr import CrowdStrikeFalcon
from app.detection.siem import SplunkSIEM
from app.routers import detection as detection_router
from app.routers import integrations as integrations_router
from app.services import notifications
from app.services import outbound_guard as og
from app.services.outbound_guard import (
    OutboundBlocked,
    check_host,
    check_smtp,
    check_url,
)

PUBLIC = "93.184.216.34"
_REAL_RESOLVE = og._resolve      # conftest swaps in a lenient resolver for every other test


@pytest.fixture
def dns(monkeypatch):
    """Fake DNS: dns.table maps name -> [addresses]; unknown names don't resolve."""
    table: dict[str, list[str]] = {}

    def getaddrinfo(host, port, *a, **kw):
        if host not in table:
            raise socket.gaierror(-2, "Name or service not known")
        return [(socket.AF_INET, socket.SOCK_STREAM, 6, "", (ip, port)) for ip in table[host]]

    monkeypatch.setattr(og, "_resolve", _REAL_RESOLVE)
    monkeypatch.setattr(og.socket, "getaddrinfo", getaddrinfo)
    return table


def policy(monkeypatch, *, private=False, allow=""):
    monkeypatch.setattr(og, "get_settings", lambda: SimpleNamespace(
        outbound_allow_private_networks=private, outbound_host_allowlist=allow))


@pytest.fixture(autouse=True)
def default_policy(monkeypatch):
    policy(monkeypatch)


# ── address classification ───────────────────────────────────────────────────

@pytest.mark.parametrize("url", [
    "https://127.0.0.1/", "https://localhost:8443/", "https://[::1]/",
    "https://169.254.169.254/latest/meta-data/", "https://[fd00:ec2::254]/",
    "https://0.0.0.0/", "https://[::ffff:127.0.0.1]/",
    "https://10.0.0.5/", "https://192.168.1.10/", "https://172.16.0.1/", "https://100.64.0.1/",
    "https://2130706433/", "https://0x7f000001/", "https://017700000001/",   # 127.0.0.1 spellings
])
def test_internal_destinations_are_refused(url, dns):
    dns["localhost"] = ["127.0.0.1"]
    with pytest.raises(OutboundBlocked):
        check_url(url)


def test_hostname_resolving_to_an_internal_address_is_refused(dns):
    dns["evil.example"] = ["10.0.0.5"]
    with pytest.raises(OutboundBlocked, match="private"):
        check_url("https://evil.example/")


def test_every_resolved_address_is_checked(dns):
    dns["mixed.example"] = [PUBLIC, "169.254.169.254"]
    with pytest.raises(OutboundBlocked):
        check_url("https://mixed.example/")


def test_public_https_target_is_allowed(dns):
    dns["splunk.example.com"] = [PUBLIC]
    assert check_url("https://splunk.example.com:8089/services") == "https://splunk.example.com:8089/services"


def test_unresolvable_host_is_refused_when_resolving_and_skipped_when_not(dns):
    with pytest.raises(OutboundBlocked, match="does not resolve"):
        check_url("https://nope.example/")
    check_url("https://nope.example/", resolve=False)


@pytest.mark.parametrize("url", [
    "http://splunk.example.com/", "ftp://splunk.example.com/", "file:///etc/passwd",
    "https://user:pw@splunk.example.com/", "https:///nohost", "", "https://[bad/",
])
def test_scheme_credentials_and_malformed_urls_are_refused(url, dns):
    dns["splunk.example.com"] = [PUBLIC]
    with pytest.raises(OutboundBlocked):
        check_url(url)


# ── operator opt-ins ─────────────────────────────────────────────────────────

def test_private_networks_can_be_enabled_for_on_prem_deployments(monkeypatch, dns):
    policy(monkeypatch, private=True)
    dns["splunk.corp.local"] = ["10.1.2.3"]
    check_url("https://splunk.corp.local:8089/")
    check_url("http://splunk.corp.local:8089/")           # http only in on-prem mode


def test_loopback_and_metadata_stay_refused_even_with_private_networks_on(monkeypatch, dns):
    policy(monkeypatch, private=True)
    for url in ("https://127.0.0.1/", "https://169.254.169.254/", "https://[::1]/"):
        with pytest.raises(OutboundBlocked):
            check_url(url)


def test_allowlisted_host_may_be_private_without_opening_everything(monkeypatch, dns):
    policy(monkeypatch, allow="jira.corp.local")
    dns["jira.corp.local"] = ["10.1.2.3"]
    dns["other.corp.local"] = ["10.1.2.4"]
    check_url("https://jira.corp.local/")
    with pytest.raises(OutboundBlocked):
        check_url("https://other.corp.local/")


def test_allowlist_cannot_override_the_always_refused_ranges(monkeypatch, dns):
    policy(monkeypatch, allow="metadata.internal")
    dns["metadata.internal"] = ["169.254.169.254"]
    with pytest.raises(OutboundBlocked):
        check_url("https://metadata.internal/")


# ── SMTP ─────────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("port", [22, 80, 443, 3306, 6379, 55553])
def test_smtp_is_limited_to_mail_ports(port, dns):
    dns["smtp.example.com"] = [PUBLIC]
    with pytest.raises(OutboundBlocked, match="port"):
        check_smtp("smtp.example.com", port)


def test_smtp_to_a_public_mail_host_is_allowed_and_internal_is_not(dns):
    dns["smtp.example.com"] = [PUBLIC]
    check_smtp("smtp.example.com", 587)
    with pytest.raises(OutboundBlocked):
        check_smtp("127.0.0.1", 25)


def test_check_host_rejects_empty():
    with pytest.raises(OutboundBlocked):
        check_host("", 443)


# ── enforcement at the call sites ────────────────────────────────────────────

def test_slack_webhook_to_metadata_is_never_sent(monkeypatch, dns):
    post = MagicMock()
    monkeypatch.setattr(notifications.httpx, "post", post)
    with pytest.raises(OutboundBlocked):
        notifications._send_slack({}, "https://169.254.169.254/latest/meta-data", "s", "b")
    post.assert_not_called()


def test_jira_and_servicenow_urls_are_checked_before_sending(monkeypatch, dns):
    post = MagicMock()
    monkeypatch.setattr(notifications.httpx, "post", post)
    with pytest.raises(OutboundBlocked):
        notifications._send_jira({"JIRA_URL": "https://127.0.0.1:8080", "JIRA_EMAIL": "a@b.c",
                                  "JIRA_PROJECT_KEY": "SEC"}, "tok", "s", "b")
    with pytest.raises(OutboundBlocked):
        notifications._send_servicenow({"SERVICENOW_URL": "https://10.0.0.9", "SERVICENOW_USERNAME": "u"},
                                       "tok", "s", "b")
    post.assert_not_called()


def test_servicenow_table_cannot_inject_path(monkeypatch, dns):
    dns["sn.example.com"] = [PUBLIC]
    post = MagicMock()
    monkeypatch.setattr(notifications.httpx, "post", post)
    with pytest.raises(ValueError, match="table"):
        notifications._send_servicenow({"SERVICENOW_URL": "https://sn.example.com", "SERVICENOW_USERNAME": "u",
                                        "SERVICENOW_TABLE": "../../admin"}, "tok", "s", "b")
    post.assert_not_called()


def test_slack_webhook_to_public_host_is_sent_without_following_redirects(monkeypatch, dns):
    dns["hooks.slack.com"] = [PUBLIC]
    post = MagicMock(return_value=MagicMock(raise_for_status=lambda: None))
    monkeypatch.setattr(notifications.httpx, "post", post)
    notifications._send_slack({}, "https://hooks.slack.com/services/T/B/x", "s", "b")
    assert post.call_args.kwargs["follow_redirects"] is False


def test_smtp_host_is_checked_before_connecting(monkeypatch, dns):
    smtp = MagicMock()
    monkeypatch.setattr(notifications.smtplib, "SMTP", smtp)
    with pytest.raises(OutboundBlocked):
        notifications._send_email({"SMTP_HOST": "127.0.0.1", "SMTP_FROM": "a@b.c", "SMTP_TO": "x@y.z"}, None, "s", "b")
    with pytest.raises(OutboundBlocked):
        notifications._send_email({"SMTP_HOST": "smtp.example.com", "SMTP_PORT": "6379",
                                   "SMTP_FROM": "a@b.c", "SMTP_TO": "x@y.z"}, None, "s", "b")
    smtp.assert_not_called()


@pytest.mark.asyncio
@pytest.mark.parametrize("engine", [SplunkSIEM({"base_url": "https://169.254.169.254"}),
                                    CrowdStrikeFalcon({"base_url": "https://127.0.0.1"})])
async def test_siem_and_edr_requests_to_internal_targets_are_not_made(engine, monkeypatch, dns):
    client = MagicMock()
    monkeypatch.setattr(httpx, "AsyncClient", client)
    assert await engine._request("GET", engine._config["base_url"] + "/x") is None
    client.assert_not_called()


# ── config-time rejection ────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_siem_config_with_internal_base_url_is_rejected(monkeypatch):
    monkeypatch.setattr(detection_router, "get_or_404", AsyncMock())
    body = detection_router.SIEMConfigIn(siem_provider="splunk",
                                         siem_config={"base_url": "https://127.0.0.1:8089", "token": "t"})
    with pytest.raises(HTTPException) as exc:
        await detection_router.configure_siem(
            engagement_id=__import__("uuid").uuid4(), body=body, db=MagicMock(),
            current_user=SimpleNamespace(tenant_id=__import__("uuid").uuid4()))
    assert exc.value.status_code == 422


@pytest.mark.asyncio
@pytest.mark.parametrize("kind,config,secret", [
    ("jira", {"JIRA_URL": "https://169.254.169.254"}, None),
    ("servicenow", {"SERVICENOW_URL": "https://127.0.0.1"}, None),
    ("slack", {}, "https://10.0.0.5/hook"),
    ("email", {"SMTP_HOST": "127.0.0.1", "SMTP_PORT": "25"}, None),
    ("email", {"SMTP_HOST": "smtp.example.com", "SMTP_PORT": "abc"}, None),
])
async def test_integration_with_internal_target_is_rejected(kind, config, secret, dns):
    dns["smtp.example.com"] = [PUBLIC]
    body = integrations_router.IntegrationIn(config=config, secret=secret)
    with pytest.raises(HTTPException) as exc:
        await integrations_router._reject_blocked_targets(kind, body)
    assert exc.value.status_code == 422


@pytest.mark.asyncio
async def test_integration_with_public_target_is_accepted(dns):
    dns["jira.example.com"] = [PUBLIC]
    await integrations_router._reject_blocked_targets(
        "jira", integrations_router.IntegrationIn(config={"JIRA_URL": "https://jira.example.com"}))


# ── SIEM/EDR secrets encrypted at rest ───────────────────────────────────────

def test_secrets_are_encrypted_and_round_trip():
    stored = config_secrets.protect({"base_url": "https://s.example.com", "token": "tok-123",
                                     "api_key": "key-456", "index": "main"})
    assert stored["token"].startswith("enc:v1:") and "tok-123" not in stored["token"]
    assert stored["api_key"].startswith("enc:v1:")
    assert stored["base_url"] == "https://s.example.com" and stored["index"] == "main"
    assert config_secrets.reveal(stored) == {"base_url": "https://s.example.com", "token": "tok-123",
                                             "api_key": "key-456", "index": "main"}


def test_protect_is_idempotent_and_handles_none():
    once = config_secrets.protect({"token": "t"})
    assert config_secrets.protect(once) == once
    assert config_secrets.protect(None) is None
    assert config_secrets.reveal(None) == {}


def test_legacy_plaintext_rows_keep_working():
    assert config_secrets.reveal({"token": "plain"}) == {"token": "plain"}


def test_undecryptable_secret_is_blanked_not_sent_as_ciphertext():
    assert config_secrets.reveal({"token": "enc:v1:not-a-real-token"}) == {"token": ""}

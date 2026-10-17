"""AD assessment launch gate, BloodHound credential handling, token error text.

* POST /ad/assess accepted any string as dc_ip, never checked the engagement scope, and
  connected (LDAP/SMB/Kerberos, BloodHound) from the Manager to wherever it pointed;
  the request could also name the Neo4j host the Manager connects to.
* bloodhound-python received the AD password as `-p <password>`, readable by any local
  user through /proc/<pid>/cmdline.
* decode_token returned the JWT library's internal reason to the client.
"""
from __future__ import annotations

import asyncio
import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import HTTPException
from pydantic import ValidationError

from app.ad import bloodhound as bh
from app.auth.jwt import create_access_token, decode_token
from app.routers import ad
from app.services import outbound_guard as og
from app.services.outbound_guard import OutboundBlocked, check_scan_target

VALID = {"dc_ip": "10.10.10.5", "domain": "corp.local", "username": "svc_scan", "password": "pw"}


# ── request validation ───────────────────────────────────────────────────────

def test_valid_request_is_accepted_and_normalised():
    req = ad.ADAssessRequest(**{**VALID, "dc_ip": " 10.10.10.5 "})
    assert req.dc_ip == "10.10.10.5"


@pytest.mark.parametrize("field,value", [
    ("dc_ip", "dc01.corp.local"), ("dc_ip", "10.10.10.5; id"), ("dc_ip", ""), ("dc_ip", "--help"),
    ("domain", "-d evil"), ("domain", "corp.local --zip"), ("domain", "a b"), ("domain", ""),
    ("username", "-u"), ("username", "a\nb"), ("username", ""),
    ("password", ""),
])
def test_malformed_fields_are_rejected(field, value):
    with pytest.raises(ValidationError):
        ad.ADAssessRequest(**{**VALID, field: value})


@pytest.mark.parametrize("username", ["svc_scan", "CORP\\svc_scan", "svc@corp.local"])
def test_normal_account_name_forms_are_accepted(username):
    ad.ADAssessRequest(**{**VALID, "username": username})


# ── launch gate ──────────────────────────────────────────────────────────────

def _engagement(scope=("10.10.10.0/24",), excluded=()):
    return SimpleNamespace(id=uuid.uuid4(), scope_cidrs=list(scope), excluded_cidrs=list(excluded))


async def _launch(monkeypatch, body, engagement):
    monkeypatch.setattr(ad, "get_or_404", AsyncMock(return_value=engagement))
    db = MagicMock()
    db.add = MagicMock()
    db.flush = AsyncMock()
    db.refresh = AsyncMock()
    tasks = MagicMock()
    user = SimpleNamespace(user_id=uuid.uuid4(), tenant_id=uuid.uuid4())
    return await ad.launch_ad_assessment(engagement.id, body, db, tasks, user), tasks


@pytest.mark.asyncio
async def test_dc_inside_scope_is_queued(monkeypatch):
    out, tasks = await _launch(monkeypatch, ad.ADAssessRequest(**VALID), _engagement())
    assert out["dc_ip"] == "10.10.10.5"
    tasks.add_task.assert_called_once()


@pytest.mark.asyncio
@pytest.mark.parametrize("dc_ip,eng", [
    ("192.168.50.1", _engagement()),                                         # outside scope
    ("10.10.10.5", _engagement(excluded=["10.10.10.0/28"])),                 # excluded
    ("10.10.10.5", _engagement(scope=())),                                   # no scope authorises nothing
])
async def test_dc_outside_scope_is_refused_and_nothing_queued(monkeypatch, dc_ip, eng):
    tasks = None
    with pytest.raises(HTTPException) as exc:
        await _launch(monkeypatch, ad.ADAssessRequest(**{**VALID, "dc_ip": dc_ip}), eng)
    assert exc.value.status_code == 403
    assert tasks is None


@pytest.mark.asyncio
@pytest.mark.parametrize("dc_ip", ["127.0.0.1", "169.254.169.254", "::1"])
async def test_loopback_and_metadata_are_refused_even_if_someone_put_them_in_scope(monkeypatch, dc_ip):
    eng = _engagement(scope=("127.0.0.0/8", "169.254.0.0/16", "::1/128"))
    with pytest.raises(HTTPException) as exc:
        await _launch(monkeypatch, ad.ADAssessRequest(**{**VALID, "dc_ip": dc_ip}), eng)
    assert exc.value.status_code == 422


def test_check_scan_target_allows_private_ips_but_not_special_ones():
    check_scan_target("10.10.10.5")
    check_scan_target("192.168.1.1")
    for bad in ("127.0.0.1", "169.254.169.254", "0.0.0.0", "224.0.0.1", "::ffff:127.0.0.1", "dc01.corp.local", ""):
        with pytest.raises(OutboundBlocked):
            check_scan_target(bad)
    assert og.SMTP_PORTS  # module import sanity


# ── Neo4j target is operator-configured ──────────────────────────────────────

def test_request_supplied_neo4j_target_is_not_honoured(monkeypatch):
    monkeypatch.setattr(ad, "get_settings", lambda: SimpleNamespace(
        neo4j_enabled=True, neo4j_uri="bolt://neo4j:7687", neo4j_user="svc", neo4j_password="op-secret"))
    req = ad.ADAssessRequest(**VALID, neo4j={"uri": "bolt://169.254.169.254:7687", "user": "x", "password": "y"})
    assert req.neo4j is not None                                   # still accepted, for compatibility
    assert ad._operator_neo4j() == {"uri": "bolt://neo4j:7687", "user": "svc", "password": "op-secret"}


def test_neo4j_import_is_skipped_when_not_enabled(monkeypatch):
    monkeypatch.setattr(ad, "get_settings", lambda: SimpleNamespace(
        neo4j_enabled=False, neo4j_uri="bolt://neo4j:7687", neo4j_user="u", neo4j_password="p"))
    assert ad._operator_neo4j() is None


# ── BloodHound: password never on the command line ───────────────────────────

class _FakeProc:
    returncode = 0

    def __init__(self):
        self.stdin_data = None

    async def communicate(self, input=None):
        self.stdin_data = input
        return b"", b""


@pytest.mark.asyncio
async def test_password_goes_over_stdin_not_argv(monkeypatch, tmp_path):
    seen = {}
    proc = _FakeProc()

    async def fake_exec(*cmd, **kwargs):
        seen["cmd"], seen["kwargs"] = cmd, kwargs
        return proc

    monkeypatch.setattr(bh.shutil, "which", lambda _b: "/usr/bin/bloodhound-python")
    monkeypatch.setattr(asyncio, "create_subprocess_exec", fake_exec)
    collector = bh.BloodHoundCollector()
    await collector.run_collection("10.10.10.5", "corp.local", {"username": "svc", "password": "S3cr3t!pw"},
                            output_dir=str(tmp_path))
    assert "S3cr3t!pw" not in " ".join(seen["cmd"])
    assert "-p" not in seen["cmd"] and not any(a.startswith("-p=") for a in seen["cmd"])
    assert proc.stdin_data == b"S3cr3t!pw\n"
    assert seen["kwargs"]["stdin"] == asyncio.subprocess.PIPE
    assert seen["kwargs"]["start_new_session"] is True            # no /dev/tty: getpass reads stdin


@pytest.mark.asyncio
async def test_option_values_are_bound_so_a_leading_dash_cannot_become_a_flag(monkeypatch, tmp_path):
    seen = {}

    async def fake_exec(*cmd, **kwargs):
        seen["cmd"] = cmd
        return _FakeProc()

    monkeypatch.setattr(bh.shutil, "which", lambda _b: "/usr/bin/bloodhound-python")
    monkeypatch.setattr(asyncio, "create_subprocess_exec", fake_exec)
    await bh.BloodHoundCollector().run_collection("10.10.10.5", "corp.local", {"username": "-x", "password": "p"},
                                           output_dir=str(tmp_path))
    assert "-u=-x" in seen["cmd"]
    assert "-x" not in seen["cmd"]


# ── token errors ─────────────────────────────────────────────────────────────

def test_invalid_token_answers_with_a_fixed_message():
    for bad in ("not-a-jwt", "a.b.c", create_access_token("u", "t", "admin") + "tampered"):
        with pytest.raises(HTTPException) as exc:
            decode_token(bad)
        assert exc.value.status_code == 401
        assert exc.value.detail == "Invalid token"


def test_expired_token_message_is_unchanged():
    token = create_access_token("u", "t", "admin", expires_minutes=-5)
    with pytest.raises(HTTPException) as exc:
        decode_token(token)
    assert exc.value.detail == "Token expired"

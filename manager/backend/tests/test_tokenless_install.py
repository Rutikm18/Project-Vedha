"""test_tokenless_install.py — installing without a `vet_` token, approved by the code the machine shows.

OFF by default. When AGENT_ALLOW_TOKENLESS_INSTALL is on, the signed package can be downloaded with
no credential (so the one-line installer needs no secret), and the thing that then protects the fleet
is the approval step: it must carry the code the machine displays, the open request queue is capped,
and a credential that IS offered but wrong is still refused.
"""
from __future__ import annotations

import asyncio
import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import HTTPException
from starlette.requests import Request

from app.config import Settings
from app.routers import agent_distribution as dist
from app.routers import probe_enrollment as pe


def _request(headers=None):
    raw = [(k.lower().encode(), v.encode()) for k, v in (headers or {}).items()]
    return Request({"type": "http", "method": "GET", "path": "/agent/package/windows", "headers": raw,
                    "client": ("203.0.113.9", 5555), "scheme": "https", "server": ("api", 443), "query_string": b""})


def _redis(count=1):
    r = MagicMock()
    r.incr = AsyncMock(return_value=count)
    r.expire = AsyncMock()
    return r


def _db(row=None):
    db = MagicMock()
    db.execute = AsyncMock(return_value=MagicMock(scalar_one_or_none=lambda: row))
    return db


def _settings(monkeypatch, **kw):
    s = Settings(**kw)
    monkeypatch.setattr(dist, "get_settings", lambda: s)
    monkeypatch.setattr(pe, "get_settings", lambda: s)
    return s


# ── the switch ───────────────────────────────────────────────────────────────

def test_it_is_off_by_default():
    assert Settings().agent_allow_tokenless_install is False
    assert Settings().probe_pending_enrollment_cap == 100


def test_with_the_switch_off_a_download_with_no_token_is_still_refused(monkeypatch):
    _settings(monkeypatch)
    with pytest.raises(HTTPException) as exc:
        asyncio.run(dist._authorize_download(_request(), _db(), _redis()))
    assert exc.value.status_code == 401


def test_with_the_switch_on_a_download_with_no_credential_at_all_is_allowed(monkeypatch):
    _settings(monkeypatch, agent_allow_tokenless_install=True)
    who = asyncio.run(dist._authorize_download(_request(), _db(), _redis()))
    assert who.id == "tokenless"


@pytest.mark.parametrize("header", [
    {"Authorization": "Bearer vet_" + "x" * 40},      # a token that does not exist
    {"Authorization": "Bearer nonsense"},              # not even a token
    {"Authorization": "Basic abc"},                    # some other credential
])
def test_a_credential_that_is_offered_but_wrong_is_never_ignored(monkeypatch, header):
    _settings(monkeypatch, agent_allow_tokenless_install=True)
    with pytest.raises(HTTPException) as exc:
        asyncio.run(dist._authorize_download(_request(header), _db(None), _redis()))
    assert exc.value.status_code == 401


def test_tokenless_downloads_have_their_own_tighter_limit(monkeypatch):
    _settings(monkeypatch, agent_allow_tokenless_install=True)
    seen = []

    class R:
        async def incr(self, key):
            seen.append(key)
            return 7 if key.startswith("agent-distribution:tokenless:") else 1

        async def expire(self, *a):
            pass

    with pytest.raises(HTTPException) as exc:
        asyncio.run(dist._authorize_download(_request(), _db(), R()))
    assert exc.value.status_code == 429
    assert any(k.startswith("agent-distribution:tokenless:203.0.113.9") for k in seen)


def test_a_rate_limiter_that_is_down_fails_closed(monkeypatch):
    _settings(monkeypatch, agent_allow_tokenless_install=True)
    r = MagicMock()
    r.incr = AsyncMock(side_effect=RuntimeError("redis down"))
    with pytest.raises(HTTPException) as exc:
        asyncio.run(dist._authorize_download(_request(), _db(), r))
    assert exc.value.status_code == 503


def test_fleet_is_told_whether_tokenless_is_on_and_gets_commands_without_a_secret(monkeypatch):
    _settings(monkeypatch)
    off = dist.tokenless_status("https://m.example.com")
    assert off == {"enabled": False, "commands": {}}
    _settings(monkeypatch, agent_allow_tokenless_install=True)
    on = dist.tokenless_status("https://m.example.com")
    assert on["enabled"] is True
    ps = on["commands"]["windows_powershell"]
    assert "-Token" not in ps and "-Manager 'https://m.example.com'" in ps and "vet_" not in ps


# ── approval needs the code the machine shows ────────────────────────────────

CODE = "ABCD2345"


def _row(**kw):
    base = dict(id=uuid.uuid4(), state="awaiting_approval", expires_at=pe.datetime.now(pe.timezone.utc) + pe.timedelta(minutes=5),
                user_code_hash=pe._keyed_hash(CODE), reported_capabilities=["discovery"], tenant_id=None)
    base.update(kw)
    return SimpleNamespace(**base)


def _approve_db(row):
    db = MagicMock()
    db.execute = AsyncMock(return_value=MagicMock(scalar_one_or_none=lambda: row))
    db.add = MagicMock()
    db.flush = AsyncMock()
    return db


USER = SimpleNamespace(user_id=uuid.uuid4(), tenant_id=uuid.uuid4())


def _approve(row, **body):
    return asyncio.run(pe.approve_request_simple(row.id, _approve_db(row), USER, pe.SimpleApproveInput(**body)))


def test_with_tokenless_on_an_approval_without_the_code_is_refused(monkeypatch):
    _settings(monkeypatch, agent_allow_tokenless_install=True)
    with pytest.raises(HTTPException) as exc:
        _approve(_row())
    assert exc.value.status_code == 422 and "code" in exc.value.detail.lower()


def test_a_wrong_code_is_refused_even_when_the_switch_is_off(monkeypatch):
    _settings(monkeypatch)
    for supplied in ("ZZZZ-ZZZZ", "abcd-2346"):
        with pytest.raises(HTTPException) as exc:
            _approve(_row(), user_code=supplied)
        assert exc.value.status_code == 403, supplied


def test_the_right_code_is_accepted_with_or_without_the_dash_and_in_any_case(monkeypatch):
    _settings(monkeypatch, agent_allow_tokenless_install=True)
    provisioned = []

    async def fake_provision(db, **kw):
        provisioned.append(kw)
        return SimpleNamespace(id=uuid.uuid4())

    monkeypatch.setattr(pe, "_provision_agent_for_site", fake_provision)
    monkeypatch.setattr(pe, "_next_probe_name", AsyncMock(return_value="vedha_agent_01"))
    for supplied in ("ABCD-2345", "abcd2345", " abcd-2345 "):
        row = _row()
        out = _approve(row, user_code=supplied)
        assert out["probe_name"] == "vedha_agent_01"
    assert len(provisioned) == 3


def test_with_the_switch_off_the_old_one_click_approval_still_works_without_a_code(monkeypatch):
    _settings(monkeypatch)
    monkeypatch.setattr(pe, "_single_tenant_mode", AsyncMock(return_value=True))   # a one-customer Manager
    monkeypatch.setattr(pe, "_provision_agent_for_site", AsyncMock(return_value=SimpleNamespace(id=uuid.uuid4())))
    monkeypatch.setattr(pe, "_next_probe_name", AsyncMock(return_value="vedha_agent_02"))
    assert _approve(_row())["probe_name"] == "vedha_agent_02"


def test_on_a_shared_manager_one_click_without_a_code_cannot_claim_an_unclaimed_device(monkeypatch):
    _settings(monkeypatch)
    monkeypatch.setattr(pe, "_single_tenant_mode", AsyncMock(return_value=False))  # several tenants
    with pytest.raises(HTTPException) as exc:
        _approve(_row())
    assert exc.value.status_code == 403 and "more than one tenant" in exc.value.detail


@pytest.mark.parametrize("tokenless", [False, True])
def test_on_a_shared_manager_the_devices_own_code_still_claims_it(monkeypatch, tokenless):
    """The code is the proof that the operator holds the device, the same proof POST /approve takes."""
    _settings(monkeypatch, agent_allow_tokenless_install=tokenless)
    monkeypatch.setattr(pe, "_single_tenant_mode", AsyncMock(return_value=False))
    monkeypatch.setattr(pe, "_provision_agent_for_site", AsyncMock(return_value=SimpleNamespace(id=uuid.uuid4())))
    monkeypatch.setattr(pe, "_next_probe_name", AsyncMock(return_value="vedha_agent_03"))
    assert _approve(_row(), user_code=CODE)["probe_name"] == "vedha_agent_03"


# ── the open request queue is capped ─────────────────────────────────────────

def test_creating_a_request_is_refused_when_too_many_are_already_waiting(monkeypatch):
    _settings(monkeypatch, probe_pending_enrollment_cap=3)
    db = MagicMock()
    db.execute = AsyncMock(return_value=MagicMock(scalar_one=lambda: 3))
    body = SimpleNamespace(signing_public_key="x")
    with pytest.raises(HTTPException) as exc:
        asyncio.run(pe.create_enrollment_request(body, _request(), db, _redis()))
    assert exc.value.status_code == 429 and "waiting for approval" in exc.value.detail

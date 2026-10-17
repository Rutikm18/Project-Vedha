"""test_agent_install_codes.py — the zero-knowledge Windows install.

An install code (``vac_...``) is the ONLY thing a client is handed: an opaque,
single-use pointer that embeds nothing and stores no secret. These tests pin the
properties that make that safe:

* the code carries >=128 bits and reveals nothing when decoded;
* the public redeem endpoint returns the SAME opaque 404 for every bad / used /
  expired / revoked code (no oracle), and mints the real vet_ only on success;
* redeem is single-use and records the redeemer IP;
* the operator's create call returns a one-liner whose only identity is the
  facade URL — no manager IP/name, no key, no token.
"""
from __future__ import annotations

import asyncio
import base64
import uuid
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

import pytest
from fastapi import HTTPException
from starlette.requests import Request

from app.models.audit_log import AuditLog
from app.models.probe_enrollment import AgentInstallCode, ProbeEnrollmentToken
from app.models.probe_site import ProbeSite
from app.routers import agent_distribution as ad
from app.routers import probe_enrollment as pe
from app.schemas.auth import CurrentUser

NOW = datetime(2026, 10, 13, 10, 0, tzinfo=timezone.utc)


# ── shared fakes ─────────────────────────────────────────────────────────────

class _Result:
    def __init__(self, value):
        self._value = value

    def scalar_one_or_none(self):
        return self._value

    def scalar_one(self):
        return self._value

    def scalars(self):
        value = self._value
        return SimpleNamespace(all=lambda: list(value or []))


class FakeDB:
    def __init__(self, *results):
        self.results = list(results)
        self.added: list = []
        self.commits = 0

    async def commit(self):
        self.commits += 1

    async def execute(self, _query):
        if not self.results:
            raise AssertionError("unexpected query")
        return _Result(self.results.pop(0))

    def add(self, obj):
        self.added.append(obj)

    async def flush(self):
        for obj in self.added:
            if not hasattr(obj, "__table__"):
                continue
            if getattr(obj, "id", None) is None:
                obj.id = uuid.uuid4()
            for column in obj.__table__.columns:
                default = getattr(column.server_default, "arg", None)
                if getattr(obj, column.key, None) is None and isinstance(default, str) and default.isdigit():
                    setattr(obj, column.key, int(default))

    def of(self, kind):
        return [obj for obj in self.added if isinstance(obj, kind)]


def _engagement(**overrides):
    base = dict(id=uuid.uuid4(), tenant_id=uuid.uuid4(), assigned_agent_id=None,
                scope_cidrs=["10.20.0.0/24"], excluded_cidrs=["10.20.0.1/32"])
    base.update(overrides)
    return SimpleNamespace(**base)


def _request():
    return Request({"type": "http", "method": "POST", "path": "/agent/redeem",
                    "headers": [], "client": ("198.51.100.7", 4000), "query_string": b""})


def _redis():
    from unittest.mock import AsyncMock, MagicMock
    redis = MagicMock()
    redis.incr = AsyncMock(return_value=1)
    redis.expire = AsyncMock()
    return redis


def _pin_manager(monkeypatch, url="https://get.vedhasec.com"):
    from app.config import Settings
    monkeypatch.setattr(ad, "get_settings", lambda: Settings(manager_public_url=url))


def _code(raw: str, **overrides) -> AgentInstallCode:
    base = dict(
        id=uuid.uuid4(), tenant_id=uuid.uuid4(), engagement_id=uuid.uuid4(), site_id=None,
        name="edge", code_hash=pe._secret_hash(raw), code_prefix=raw[:12],
        # Far future so a "live" code stays live regardless of the real wall clock
        # (the redeem endpoint uses datetime.now(), not the NOW fixture).
        expires_at=datetime(2099, 1, 1, tzinfo=timezone.utc), redeemed_at=None, redeemed_ip=None,
        minted_token_id=None, revoked_at=None,
    )
    base.update(overrides)
    return AgentInstallCode(**base)


# ── code generation + pure helpers ───────────────────────────────────────────

def test_generate_install_code_format_and_entropy():
    raw, code_hash, prefix = pe.generate_install_code()
    assert raw.startswith("vac_")
    assert ad._INSTALL_CODE_RE.fullmatch(raw)
    assert code_hash == pe._secret_hash(raw) and len(code_hash) == 64
    assert prefix == raw[:12]
    # token_urlsafe(18) → 24 url-safe chars → ~144 bits, comfortably over 128.
    body = raw[len("vac_"):]
    assert len(body) >= 22
    # two draws never collide
    assert pe.generate_install_code()[0] != raw


def test_install_code_is_usable_states():
    assert pe.install_code_is_usable(_code("vac_" + "a" * 22), NOW) is True
    assert pe.install_code_is_usable(None, NOW) is False
    assert pe.install_code_is_usable(_code("vac_" + "a" * 22, revoked_at=NOW), NOW) is False
    assert pe.install_code_is_usable(_code("vac_" + "a" * 22, redeemed_at=NOW), NOW) is False
    assert pe.install_code_is_usable(_code("vac_" + "a" * 22, expires_at=NOW), NOW) is False


def test_install_code_out_states_and_no_secret():
    raw = "vac_" + "a" * 22
    out = pe.install_code_out(_code(raw), NOW)
    assert out["state"] == "active" and out["usable"] is True
    assert "code_hash" not in out and "code" not in out
    assert out["code_prefix"] == raw[:12]
    assert pe.install_code_out(_code(raw, revoked_at=NOW), NOW)["state"] == "revoked"
    assert pe.install_code_out(_code(raw, redeemed_at=NOW, redeemed_ip="203.0.113.9"), NOW)["state"] == "redeemed"
    assert pe.install_code_out(_code(raw, expires_at=NOW), NOW)["state"] == "expired"


def test_windows_install_code_command_only_facade_and_code():
    code = "vac_" + "a" * 22
    cmd = ad.windows_install_code_command("https://get.vedhasec.com", code)
    assert cmd == (
        "& ([scriptblock]::Create((irm 'https://get.vedhasec.com/agent/install.ps1'))) "
        f"-Manager 'https://get.vedhasec.com' -Code '{code}'"
    )
    # the command reveals only the facade + the opaque code — no token, no key
    assert "vet_" not in cmd and "-Token" not in cmd
    # a plain-http lab manager or a malformed code yields no command (never a broken one)
    assert ad.windows_install_code_command("http://lab.local", code) == ""
    assert ad.windows_install_code_command("https://get.vedhasec.com", "not-a-code") == ""


def test_create_schema_requires_exactly_one_target():
    with pytest.raises(ValueError, match="exactly one"):
        pe.InstallCodeCreate(name="x")
    with pytest.raises(ValueError, match="exactly one"):
        pe.InstallCodeCreate(name="x", site_id=uuid.uuid4(), engagement_id=uuid.uuid4())
    assert pe.InstallCodeCreate(name="x", engagement_id=uuid.uuid4()).site_id is None


# ── mint-on-redeem ───────────────────────────────────────────────────────────

def test_mint_for_engagement_issues_single_use_token():
    engagement = _engagement()
    code = _code("vac_" + "a" * 22, tenant_id=engagement.tenant_id, engagement_id=engagement.id, site_id=None)
    db = FakeDB(engagement, [])  # engagement lookup, then issue_engagement_token's live-token query
    token, raw = asyncio.run(pe.mint_token_for_install_code(db, code, NOW))
    assert raw.startswith("vet_") and token.max_uses == 1
    assert token.engagement_id == engagement.id and token.token_hash == pe._secret_hash(raw)
    assert token.expires_at == NOW + timedelta(minutes=60)
    # Closing the loop: the minted token is immediately valid for the agent to enrol with.
    token.uses = 0  # server default the FakeDB would fill
    assert pe.enroll_token_is_usable(token, NOW) is True


def test_mint_for_site_issues_single_use_token():
    site = ProbeSite(id=uuid.uuid4(), tenant_id=uuid.uuid4(), name="s", status="active",
                     authorized_cidrs=["10.0.0.0/24"], approved_capabilities=["discovery"])
    code = _code("vac_" + "a" * 22, tenant_id=site.tenant_id, engagement_id=None, site_id=site.id)
    db = FakeDB(site)
    token, raw = asyncio.run(pe.mint_token_for_install_code(db, code, NOW))
    assert raw.startswith("vet_") and token.site_id == site.id and token.max_uses == 1


def test_mint_for_missing_site_raises_409():
    code = _code("vac_" + "a" * 22, engagement_id=None, site_id=uuid.uuid4())
    with pytest.raises(HTTPException) as exc:
        asyncio.run(pe.mint_token_for_install_code(FakeDB(None), code, NOW))
    assert exc.value.status_code == 409


# ── public redeem: opaque 404 on everything that is not a live code ───────────

# All >= 8 chars (RedeemInput min_length) but none a well-formed vac_ code.
@pytest.mark.parametrize("raw", ["notacode", "vet_abcdefgh", "vac_short"])
def test_redeem_bad_format_is_opaque_404(raw, monkeypatch):
    _pin_manager(monkeypatch)
    with pytest.raises(HTTPException) as exc:
        asyncio.run(ad.redeem_install_code(ad.RedeemInput(code=raw), _request(), FakeDB(), _redis()))
    assert exc.value.status_code == 404 and exc.value.detail == ad._REDEEM_OPAQUE


@pytest.mark.parametrize("overrides", [
    {},                                 # not found (FakeDB returns None)
    {"revoked_at": NOW},
    {"redeemed_at": NOW},
    {"expires_at": datetime(2020, 1, 1, tzinfo=timezone.utc)},   # unambiguously past
])
def test_redeem_unusable_code_is_opaque_404(overrides, monkeypatch):
    _pin_manager(monkeypatch)
    raw = "vac_" + "b" * 22
    looked_up = None if overrides == {} else _code(raw, **overrides)
    with pytest.raises(HTTPException) as exc:
        asyncio.run(ad.redeem_install_code(ad.RedeemInput(code=raw), _request(), FakeDB(looked_up), _redis()))
    assert exc.value.status_code == 404 and exc.value.detail == ad._REDEEM_OPAQUE


def test_redeem_happy_mints_vet_and_burns_the_code(monkeypatch):
    _pin_manager(monkeypatch)
    engagement = _engagement()
    raw = "vac_" + "c" * 22
    code = _code(raw, tenant_id=engagement.tenant_id, engagement_id=engagement.id, site_id=None)
    # redeem: code lookup → mint: engagement lookup → issue_engagement_token: live tokens []
    db = FakeDB(code, engagement, [])
    out = asyncio.run(ad.redeem_install_code(ad.RedeemInput(code=raw), _request(), db, _redis()))

    assert out["manager_url"] == "https://get.vedhasec.com"
    assert out["token"].startswith("vet_")
    # the response carries nothing but the facade + the single-use token
    assert set(out) == {"manager_url", "token", "token_expires_in_seconds"}
    # the code is now single-use-dead and the redeemer IP is recorded
    assert code.redeemed_at is not None and code.redeemed_ip == "198.51.100.7"
    assert code.minted_token_id is not None
    assert db.commits == 1
    actions = [row.action for row in db.of(AuditLog)]
    assert "agent.install_code.redeemed" in actions


def test_redeem_rate_limiter_down_fails_closed(monkeypatch):
    _pin_manager(monkeypatch)
    from unittest.mock import AsyncMock, MagicMock
    redis = MagicMock()
    redis.incr = AsyncMock(side_effect=RuntimeError("redis down"))
    with pytest.raises(HTTPException) as exc:
        asyncio.run(ad.redeem_install_code(ad.RedeemInput(code="vac_" + "d" * 22), _request(), FakeDB(), redis))
    assert exc.value.status_code == 503


# ── operator create: one call, one-liner out, no secret shown ────────────────

def _admin():
    return CurrentUser(user_id=uuid.uuid4(), tenant_id=uuid.uuid4(), role="admin")


def _op_request():
    return Request({"type": "http", "method": "POST", "path": "/probe-enrollment/install-codes",
                    "headers": [], "client": ("198.51.100.7", 4000), "query_string": b"",
                    "scheme": "https", "server": ("get.vedhasec.com", 443)})


def test_create_install_code_returns_one_liner_for_engagement(monkeypatch):
    _pin_manager(monkeypatch)
    user = _admin()
    engagement = _engagement(tenant_id=user.tenant_id)
    db = FakeDB(engagement)
    out = asyncio.run(pe.create_install_code(
        pe.InstallCodeCreate(name="Branch PC", engagement_id=engagement.id),
        _op_request(), db, user,
    ))
    assert out["code"].startswith("vac_")
    assert out["command"].startswith("& ([scriptblock]::Create((irm 'https://get.vedhasec.com/agent/install.ps1')))")
    assert out["code"] in out["command"]
    # no vet_ token, manager IP, or key is shown to the operator either
    assert "vet_" not in out["command"]
    row = db.of(AgentInstallCode)[0]
    assert row.engagement_id == engagement.id and row.tenant_id == user.tenant_id
    assert db.commits == 1
    assert any(a.action == "agent.install_code.created" for a in db.of(AuditLog))


def test_create_install_code_rejects_blocked_engagement(monkeypatch):
    _pin_manager(monkeypatch)
    user = _admin()
    engagement = _engagement(tenant_id=user.tenant_id, assigned_agent_id=uuid.uuid4())
    with pytest.raises(HTTPException) as exc:
        asyncio.run(pe.create_install_code(
            pe.InstallCodeCreate(name="x", engagement_id=engagement.id),
            _op_request(), FakeDB(engagement), user,
        ))
    assert exc.value.status_code == 409

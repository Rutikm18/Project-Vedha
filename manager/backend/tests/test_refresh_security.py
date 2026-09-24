"""
/auth/refresh security contract.

Before this suite, refresh:
  * re-minted tokens for a DISABLED user / DISABLED tenant / EXPIRED password —
    login rejects all three, refresh checked none, so an offboarded user kept a
    rolling 7-day session forever;
  * never stored or checked the refresh jti, so a stolen refresh token stayed
    valid indefinitely and the pre-rotation token kept working after rotation;
  * read the token from the query string (FastAPI's default for a bare `str`
    param), so it landed in proxy/access logs.

Contract now: refresh tokens are single-use (Redis allowlist + GETDEL); replaying
a consumed token revokes every refresh token the user holds (reuse detection);
account state is re-validated on every rotation; the token travels in the body.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import HTTPException

from app.auth import refresh_store
from app.auth.jwt import create_refresh_token, decode_token
from app.auth.router import logout, refresh
from app.models.enums import UserRole
from app.schemas.auth import RefreshRequest


class FakeRedis:
    """The handful of redis.asyncio commands the refresh store uses."""

    def __init__(self):
        self.kv: dict[str, str] = {}
        self.sets: dict[str, set[str]] = {}

    async def set(self, key, value, ex=None):
        self.kv[key] = value

    async def getdel(self, key):
        return self.kv.pop(key, None)

    async def sadd(self, key, *members):
        self.sets.setdefault(key, set()).update(members)

    async def srem(self, key, *members):
        self.sets.get(key, set()).difference_update(members)

    async def smembers(self, key):
        return set(self.sets.get(key, set()))

    async def expire(self, key, seconds):
        return True

    async def delete(self, *keys):
        for k in keys:
            self.kv.pop(k, None)
            self.sets.pop(k, None)


def _user(**over):
    base = {
        "id": uuid.uuid4(), "tenant_id": uuid.uuid4(), "role": UserRole.manager,
        "client_engagement_id": None, "is_active": True, "password_expires_at": None,
    }
    base.update(over)
    return MagicMock(**base)


def _db(user, tenant_active=True):
    tenant = MagicMock(is_active=tenant_active)
    seq = iter([user, tenant])

    async def execute(*_a, **_k):
        r = MagicMock()
        r.scalar_one_or_none.return_value = next(seq, tenant)
        return r

    db = MagicMock()
    db.execute = AsyncMock(side_effect=execute)
    return db


async def _issued(redis, user):
    token, jti = create_refresh_token(subject=str(user.id), tenant_id=str(user.tenant_id))
    await refresh_store.issue(redis, jti, str(user.id))
    return token


# ── happy path + rotation ─────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_refresh_rotates_and_new_token_is_registered():
    redis, user = FakeRedis(), _user()
    token = await _issued(redis, user)

    resp = await refresh(RefreshRequest(refresh_token=token), db=_db(user), redis=redis)

    new_jti = decode_token(resp.refresh_token)["jti"]
    assert f"rt:{new_jti}" in redis.kv


@pytest.mark.asyncio
async def test_refresh_token_is_single_use():
    redis, user = FakeRedis(), _user()
    token = await _issued(redis, user)
    await refresh(RefreshRequest(refresh_token=token), db=_db(user), redis=redis)

    with pytest.raises(HTTPException) as exc:
        await refresh(RefreshRequest(refresh_token=token), db=_db(user), redis=redis)
    assert exc.value.status_code == 401


@pytest.mark.asyncio
async def test_reuse_of_consumed_token_revokes_whole_user_session_family():
    """Replay of a rotated token = theft signal: the attacker's (or victim's)
    newer token must die too, forcing a fresh password login."""
    redis, user = FakeRedis(), _user()
    stolen = await _issued(redis, user)
    rotated = await refresh(RefreshRequest(refresh_token=stolen), db=_db(user), redis=redis)

    with pytest.raises(HTTPException):
        await refresh(RefreshRequest(refresh_token=stolen), db=_db(user), redis=redis)

    with pytest.raises(HTTPException) as exc:
        await refresh(RefreshRequest(refresh_token=rotated.refresh_token), db=_db(user), redis=redis)
    assert exc.value.status_code == 401


@pytest.mark.asyncio
async def test_unregistered_token_rejected():
    """A validly-signed token that was never issued into the store (pre-deploy
    or forged-with-leaked-secret) is not honoured."""
    redis, user = FakeRedis(), _user()
    token, _ = create_refresh_token(subject=str(user.id), tenant_id=str(user.tenant_id))

    with pytest.raises(HTTPException) as exc:
        await refresh(RefreshRequest(refresh_token=token), db=_db(user), redis=redis)
    assert exc.value.status_code == 401


# ── account state re-validated ────────────────────────────────────────────────

@pytest.mark.asyncio
@pytest.mark.parametrize("user_over,tenant_active", [
    ({"is_active": False}, True),
    ({}, False),
    ({"password_expires_at": datetime.now(timezone.utc) - timedelta(days=1)}, True),
])
async def test_refresh_rejects_unusable_account(user_over, tenant_active):
    redis, user = FakeRedis(), _user(**user_over)
    token = await _issued(redis, user)

    with pytest.raises(HTTPException) as exc:
        await refresh(RefreshRequest(refresh_token=token), db=_db(user, tenant_active), redis=redis)
    assert exc.value.status_code == 401


@pytest.mark.asyncio
async def test_refresh_rejects_deleted_user():
    redis, user = FakeRedis(), _user()
    token = await _issued(redis, user)

    with pytest.raises(HTTPException) as exc:
        await refresh(RefreshRequest(refresh_token=token), db=_db(None), redis=redis)
    assert exc.value.status_code == 401


@pytest.mark.asyncio
async def test_access_token_cannot_be_used_as_refresh():
    from app.auth.jwt import create_access_token
    redis, user = FakeRedis(), _user()
    access = create_access_token(str(user.id), str(user.tenant_id), "manager")

    with pytest.raises(HTTPException) as exc:
        await refresh(RefreshRequest(refresh_token=access), db=_db(user), redis=redis)
    assert exc.value.status_code == 401


# ── store failure fails closed ────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_refresh_fails_closed_when_store_unavailable():
    user = _user()
    token, _ = create_refresh_token(subject=str(user.id), tenant_id=str(user.tenant_id))
    broken = MagicMock()
    broken.getdel = AsyncMock(side_effect=ConnectionError("redis down"))

    with pytest.raises(HTTPException) as exc:
        await refresh(RefreshRequest(refresh_token=token), db=_db(user), redis=broken)
    assert exc.value.status_code == 503


# ── logout ────────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_logout_revokes_the_refresh_token():
    redis, user = FakeRedis(), _user()
    token = await _issued(redis, user)

    await logout(RefreshRequest(refresh_token=token), redis=redis)

    with pytest.raises(HTTPException) as exc:
        await refresh(RefreshRequest(refresh_token=token), db=_db(user), redis=redis)
    assert exc.value.status_code == 401


@pytest.mark.asyncio
async def test_logout_with_garbage_token_is_harmless_noop():
    """Logout is public (the access token may already be expired); an invalid
    token must neither error nor revoke anything."""
    resp = await logout(RefreshRequest(refresh_token="not-a-jwt"), redis=FakeRedis())
    assert resp == {"ok": True}


# ── token never in the query string ───────────────────────────────────────────

def test_refresh_route_reads_token_from_body_not_query():
    from app.auth.router import router
    route = next(r for r in router.routes if getattr(r, "path", "") == "/auth/refresh")
    query_names = [p.name for p in route.dependant.query_params]
    assert "refresh_token" not in query_names
    assert route.dependant.body_params, "refresh token must travel in the JSON body"

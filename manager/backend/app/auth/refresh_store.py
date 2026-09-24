"""
refresh_store.py — server-side allowlist for refresh tokens (rotation + reuse
detection, per OAuth 2.0 Security BCP §4.14).

A refresh JWT is honoured only while its jti is present in Redis:

  rt:{jti}        -> user_id     (TTL = refresh lifetime)
  rt:user:{uid}   -> {jti, ...}  (index so every session a user holds can be revoked)

`consume` is a single GETDEL, so a token is valid exactly once even under
concurrent refreshes. A validly-signed token whose jti is gone was already
rotated or revoked — replay of a stolen token — so the caller revokes the family.
"""
from __future__ import annotations

from app.config import get_settings

settings = get_settings()

_TTL_SECONDS = settings.refresh_token_expire_days * 24 * 3600


def _key(jti: str) -> str:
    return f"rt:{jti}"


def _user_key(user_id: str) -> str:
    return f"rt:user:{user_id}"


async def issue(redis, jti: str, user_id: str) -> None:
    await redis.set(_key(jti), user_id, ex=_TTL_SECONDS)
    await redis.sadd(_user_key(user_id), jti)
    await redis.expire(_user_key(user_id), _TTL_SECONDS)


async def consume(redis, jti: str) -> str | None:
    """Atomically remove and return the owning user_id, or None if not live."""
    owner = await redis.getdel(_key(jti))
    if owner is not None:
        await redis.srem(_user_key(owner), jti)
    return owner


async def revoke_all(redis, user_id: str) -> None:
    jtis = await redis.smembers(_user_key(user_id))
    await redis.delete(*[_key(j) for j in jtis], _user_key(user_id))

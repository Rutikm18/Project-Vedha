"""
ratelimit.py — P2: Redis-backed rate limiting (no new dependency; reuses the
existing aioredis client). Fixed-window counter — simple, multi-worker-correct
because the counter lives in Redis, not per-process memory.

Two layers guard /auth/login:
  * per client IP (`login_rate_limit`) — throttles one source hammering logins;
  * per account, failures only (`check/record/clear_login_failures`) — the
    unspoofable backstop that slows a distributed spray against one user.

The same `rate_limit()` factory can gate any hot or abusable endpoint.
"""
from __future__ import annotations

import ipaddress
from functools import lru_cache

from fastapi import Depends, HTTPException, Request, status

from app.config import get_settings
from app.dependencies import get_redis

LOGIN_FAILURES_PER_ACCOUNT = 10
LOGIN_FAILURE_WINDOW_SEC = 15 * 60


@lru_cache
def _trusted_networks() -> tuple[ipaddress._BaseNetwork, ...]:
    return tuple(
        ipaddress.ip_network(c.strip(), strict=False)
        for c in get_settings().trusted_proxy_cidrs.split(",") if c.strip()
    )


def _parse_ip(value: str) -> ipaddress._BaseAddress | None:
    try:
        return ipaddress.ip_address(value.strip())
    except ValueError:
        return None


def _is_trusted(ip: ipaddress._BaseAddress) -> bool:
    return any(ip in net for net in _trusted_networks())


def client_ip(request: Request) -> str:
    """The address to rate-limit on.

    X-Forwarded-For is believed ONLY when the socket peer is a trusted proxy;
    otherwise a direct caller could mint a fresh bucket per request. Within a
    trusted chain the client is the rightmost untrusted hop (anything left of it
    is client-supplied and forgeable). If every hop is private — normal for
    on-prem operators on a LAN — the leftmost hop is the original client: Caddy
    overwrites an untrusted client's XFF, so that value came from the edge.
    Falls back to 'unknown' so a missing peer can't bypass the limit by erroring.
    """
    if not request.client:
        return "unknown"
    peer = request.client.host
    peer_ip = _parse_ip(peer)
    if peer_ip is None or not _is_trusted(peer_ip):
        return peer

    hops = [ip for ip in (_parse_ip(h) for h in request.headers.get("x-forwarded-for", "").split(",")) if ip]
    if not hops:
        return peer
    for ip in reversed(hops):
        if not _is_trusted(ip):
            return str(ip)
    return str(hops[0])


def _too_many(ttl: int) -> HTTPException:
    retry = max(ttl, 1)
    return HTTPException(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        detail=f"Too many requests. Try again in {retry}s.",
        headers={"Retry-After": str(retry)},
    )


async def _check(redis, bucket: str, limit: int, window_sec: int) -> None:
    key = f"rl:{bucket}"
    count = await redis.incr(key)
    if count == 1:
        await redis.expire(key, window_sec)
    if count > limit:
        ttl = await redis.ttl(key)
        if ttl < 0:
            await redis.expire(key, window_sec)
            ttl = window_sec
        raise _too_many(ttl)


def rate_limit(scope: str, limit: int, window_sec: int):
    """FastAPI dependency factory. Keys the window by (scope, client-IP)."""
    async def _dep(request: Request, redis=Depends(get_redis)) -> None:
        await _check(redis, f"{scope}:{client_ip(request)}", limit, window_sec)
    return _dep


# 5 login attempts per minute per IP — stops brute force without hurting humans.
login_rate_limit = rate_limit("login", limit=5, window_sec=60)


# AI routes spend paid API credit: cap each client IP at 30 calls a minute.
ai_rate_limit = rate_limit("ai", limit=30, window_sec=60)


# ── Per-account login failures ────────────────────────────────────────────────
# Counts FAILURES only and clears on success: a legitimate user is never locked
# out by their own successful logins, and an attacker can hold an account's
# window open for at most LOGIN_FAILURE_WINDOW_SEC after their last failure.

def _account_key(email: str) -> str:
    return f"rl:login-acct:{email.strip().lower()}"


async def check_login_failures(redis, email: str) -> None:
    key = _account_key(email)
    count = await redis.get(key)
    if count is not None and int(count) >= LOGIN_FAILURES_PER_ACCOUNT:
        raise _too_many(await redis.ttl(key))


async def record_login_failure(redis, email: str) -> None:
    key = _account_key(email)
    if await redis.incr(key) == 1:
        await redis.expire(key, LOGIN_FAILURE_WINDOW_SEC)


async def clear_login_failures(redis, email: str) -> None:
    await redis.delete(_account_key(email))

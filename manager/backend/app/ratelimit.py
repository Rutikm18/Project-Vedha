"""
ratelimit.py — P2: Redis-backed rate limiting (no new dependency; reuses the
existing aioredis client). Fixed-window counter — simple, multi-worker-correct
because the counter lives in Redis, not per-process memory.

Applied to /auth/login (brute-force / credential-stuffing protection). The same
`rate_limit()` factory can gate any hot or abusable endpoint.
"""
from __future__ import annotations

from fastapi import Depends, HTTPException, Request, status

from app.dependencies import get_redis


def client_ip(request: Request) -> str:
    """Best-effort client IP. Honors X-Forwarded-For (first hop) when behind a
    proxy/LB, else the socket peer. Falls back to 'unknown' so a missing IP
    can't bypass the limit by erroring."""
    fwd = request.headers.get("x-forwarded-for")
    if fwd:
        return fwd.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


async def _check(redis, bucket: str, limit: int, window_sec: int) -> None:
    key = f"rl:{bucket}"
    count = await redis.incr(key)
    if count == 1:
        await redis.expire(key, window_sec)
    if count > limit:
        ttl = await redis.ttl(key)
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Too many requests. Try again in {max(ttl, 1)}s.",
            headers={"Retry-After": str(max(ttl, 1))},
        )


def rate_limit(scope: str, limit: int, window_sec: int):
    """FastAPI dependency factory. Keys the window by (scope, client-IP)."""
    async def _dep(request: Request, redis=Depends(get_redis)) -> None:
        await _check(redis, f"{scope}:{client_ip(request)}", limit, window_sec)
    return _dep


# 5 login attempts per minute per IP — stops brute force without hurting humans.
login_rate_limit = rate_limit("login", limit=5, window_sec=60)

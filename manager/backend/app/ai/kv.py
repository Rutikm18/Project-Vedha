"""kv.py — the small key/value surface the AI router keeps shared state in.

Cooldowns, spend counters and stored answers must be visible to every uvicorn
worker, so production uses Redis. Redis is a helper here, never a dependency: if
it is unreachable, every operation degrades to process memory (fail OPEN — the AI
still answers, each worker just keeps its own cooldowns) and the outage is logged
once.
"""
from __future__ import annotations

import math
import time
from typing import Awaitable, Callable, Protocol, TypeVar

import structlog

logger = structlog.get_logger()
T = TypeVar("T")


class KvStore(Protocol):
    async def get(self, key: str) -> str | None: ...
    async def set(self, key: str, value: str, ttl_s: float) -> None: ...
    async def set_nx(self, key: str, value: str, ttl_s: float) -> bool: ...
    async def delete(self, *keys: str) -> None: ...
    async def incr(self, key: str, ttl_s: float) -> int: ...
    async def incr_float(self, key: str, amount: float, ttl_s: float) -> float: ...
    async def ttl(self, key: str) -> float | None: ...


def _whole_seconds(ttl_s: float) -> int:
    return max(1, math.ceil(ttl_s))


class MemoryKv:
    """Process-local store with per-key expiry. The TTL of a counter is set when
    the key is created and not extended by later increments (Redis INCR semantics
    as used here)."""

    def __init__(self, clock: Callable[[], float] = time.monotonic) -> None:
        self._data: dict[str, tuple[str, float]] = {}
        self._clock = clock

    def _live(self, key: str) -> tuple[str, float] | None:
        item = self._data.get(key)
        if item is None:
            return None
        if item[1] <= self._clock():
            self._data.pop(key, None)
            return None
        return item

    async def get(self, key: str) -> str | None:
        item = self._live(key)
        return item[0] if item else None

    async def set(self, key: str, value: str, ttl_s: float) -> None:
        self._data[key] = (value, self._clock() + ttl_s)

    async def set_nx(self, key: str, value: str, ttl_s: float) -> bool:
        if self._live(key):
            return False
        await self.set(key, value, ttl_s)
        return True

    async def delete(self, *keys: str) -> None:
        for key in keys:
            self._data.pop(key, None)

    async def incr(self, key: str, ttl_s: float) -> int:
        item = self._live(key)
        count = int(item[0]) + 1 if item else 1
        self._data[key] = (str(count), item[1] if item else self._clock() + ttl_s)
        return count

    async def incr_float(self, key: str, amount: float, ttl_s: float) -> float:
        item = self._live(key)
        total = float(item[0]) + amount if item else amount
        self._data[key] = (repr(total), item[1] if item else self._clock() + ttl_s)
        return total

    async def ttl(self, key: str) -> float | None:
        item = self._live(key)
        return item[1] - self._clock() if item else None


class RedisKv:
    """Redis-backed store shared by every worker; any Redis error falls back to a
    process-local MemoryKv for that operation."""

    def __init__(self, fallback: MemoryKv | None = None) -> None:
        self._fallback = fallback or MemoryKv()
        self._warned = False

    async def _run(self, op: Callable[[object], Awaitable[T]],
                   fallback: Callable[[], Awaitable[T]]) -> T:
        from app import dependencies  # late: keeps this module import-light
        try:
            return await op(await dependencies.get_redis())
        except Exception as exc:  # noqa: BLE001 — fail open, never fail the AI call
            if not self._warned:
                logger.warning("ai.kv.redis_unavailable", error=type(exc).__name__)
                self._warned = True
            return await fallback()

    async def get(self, key: str) -> str | None:
        return await self._run(lambda r: r.get(key), lambda: self._fallback.get(key))

    async def set(self, key: str, value: str, ttl_s: float) -> None:
        await self._run(lambda r: r.set(key, value, ex=_whole_seconds(ttl_s)),
                        lambda: self._fallback.set(key, value, ttl_s))

    async def set_nx(self, key: str, value: str, ttl_s: float) -> bool:
        async def op(r):
            return bool(await r.set(key, value, ex=_whole_seconds(ttl_s), nx=True))
        return await self._run(op, lambda: self._fallback.set_nx(key, value, ttl_s))

    async def delete(self, *keys: str) -> None:
        if keys:
            await self._run(lambda r: r.delete(*keys), lambda: self._fallback.delete(*keys))

    async def incr(self, key: str, ttl_s: float) -> int:
        async def op(r):
            count = int(await r.incr(key))
            if count == 1:
                await r.expire(key, _whole_seconds(ttl_s))
            return count
        return await self._run(op, lambda: self._fallback.incr(key, ttl_s))

    async def incr_float(self, key: str, amount: float, ttl_s: float) -> float:
        async def op(r):
            total = float(await r.incrbyfloat(key, amount))
            if await r.ttl(key) < 0:
                await r.expire(key, _whole_seconds(ttl_s))
            return total
        return await self._run(op, lambda: self._fallback.incr_float(key, amount, ttl_s))

    async def ttl(self, key: str) -> float | None:
        async def op(r):
            seconds = await r.ttl(key)
            return float(seconds) if seconds and seconds > 0 else None
        return await self._run(op, lambda: self._fallback.ttl(key))


_default: KvStore | None = None


def default_kv() -> KvStore:
    global _default
    if _default is None:
        _default = RedisKv()
    return _default


def set_default_kv(store: KvStore | None) -> None:
    """Swap the process-wide store (tests use a fresh MemoryKv per test)."""
    global _default
    _default = store

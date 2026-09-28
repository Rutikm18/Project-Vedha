from __future__ import annotations

import pytest

from app.ai.kv import MemoryKv, RedisKv


class _Clock:
    def __init__(self) -> None:
        self.now = 1000.0

    def __call__(self) -> float:
        return self.now


@pytest.mark.asyncio
async def test_memory_kv_expires_values():
    clock = _Clock()
    kv = MemoryKv(clock=clock)
    await kv.set("k", "v", 10)
    assert await kv.get("k") == "v"
    assert await kv.ttl("k") == 10
    clock.now += 10
    assert await kv.get("k") is None
    assert await kv.ttl("k") is None


@pytest.mark.asyncio
async def test_memory_kv_set_nx_only_once():
    kv = MemoryKv()
    assert await kv.set_nx("lock", "1", 30) is True
    assert await kv.set_nx("lock", "1", 30) is False
    await kv.delete("lock")
    assert await kv.set_nx("lock", "1", 30) is True


@pytest.mark.asyncio
async def test_memory_kv_incr_keeps_first_ttl_and_floats_accumulate():
    clock = _Clock()
    kv = MemoryKv(clock=clock)
    assert await kv.incr("n", 60) == 1
    clock.now += 50
    assert await kv.incr("n", 60) == 2
    clock.now += 10          # the ORIGINAL 60 s window has closed
    assert await kv.get("n") is None
    assert await kv.incr_float("usd", 0.25, 60) == 0.25
    assert await kv.incr_float("usd", 0.5, 60) == 0.75


@pytest.mark.asyncio
async def test_redis_kv_fails_open_to_memory(monkeypatch):
    async def _no_redis():
        raise ConnectionError("redis down")

    monkeypatch.setattr("app.dependencies.get_redis", _no_redis)
    kv = RedisKv()
    await kv.set("k", "v", 10)
    assert await kv.get("k") == "v"
    assert await kv.set_nx("k", "x", 10) is False
    assert await kv.incr("n", 10) == 1

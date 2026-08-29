"""Perf/N+1: _resolve_asset memoizes per-run so a host with many findings is
resolved ONCE, not once per finding."""
from __future__ import annotations

import uuid
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.discovery.finding_translator import _resolve_asset
from app.models.asset import Asset


@pytest.mark.asyncio
async def test_cache_resolves_each_host_once():
    eng = uuid.uuid4()
    existing = Asset(engagement_id=eng, ip_address="10.0.0.5")
    db = MagicMock()
    db.execute = AsyncMock(return_value=MagicMock(scalar_one_or_none=lambda: existing))
    cache: dict = {}

    # 20 findings on the same host — one DB query, then cache hits.
    for _ in range(20):
        got = await _resolve_asset(db, eng, "10.0.0.5", cache=cache)
        assert got is existing
    assert db.execute.await_count == 1                 # N+1 eliminated
    assert cache["10.0.0.5"] is existing


@pytest.mark.asyncio
async def test_no_cache_keeps_old_behavior():
    eng = uuid.uuid4()
    existing = Asset(engagement_id=eng, ip_address="10.0.0.5")
    db = MagicMock()
    db.execute = AsyncMock(return_value=MagicMock(scalar_one_or_none=lambda: existing))
    for _ in range(3):
        await _resolve_asset(db, eng, "10.0.0.5")       # no cache → queries each time
    assert db.execute.await_count == 3


@pytest.mark.asyncio
async def test_host_port_target_normalized():
    eng = uuid.uuid4()
    existing = Asset(engagement_id=eng, ip_address="10.0.0.5")
    db = MagicMock()
    db.execute = AsyncMock(return_value=MagicMock(scalar_one_or_none=lambda: existing))
    cache: dict = {}
    await _resolve_asset(db, eng, "10.0.0.5:443", cache=cache)   # host:port form
    await _resolve_asset(db, eng, "10.0.0.5", cache=cache)       # same host
    assert db.execute.await_count == 1                          # both hit one host key

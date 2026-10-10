"""R8 — reading the route list must not recompute and write for an engagement that
already has a stored analysis, even when that analysis found zero routes."""
from __future__ import annotations

import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.routers import attack_paths as R


class _Result:
    def scalars(self):
        return self

    def all(self):
        return []

    def first(self):
        return None


class _DB:
    def __init__(self, analysis):
        self.analysis = analysis

    async def get(self, model, key):
        return self.analysis

    async def execute(self, stmt, params=None):
        return _Result()


async def _list(db, **kw):
    user = SimpleNamespace(tenant_id=uuid.uuid4())
    args = dict(refresh=False, target_asset_id=None, page=1, page_size=20)
    args.update(kw)
    with patch.object(R, "get_or_404", new=AsyncMock()), \
         patch.object(R, "_recompute_and_store", new=AsyncMock(return_value=[])) as rc, \
         patch.object(R, "_build_analyzer", new=AsyncMock(
             return_value=(MagicMock(diagnose=MagicMock(return_value=[])), None))), \
         patch.object(R, "_target_ids", new=AsyncMock(return_value=[])):
        body = await R.list_attack_paths(uuid.uuid4(), db, user, **args)
    return body, rc


@pytest.mark.asyncio
async def test_a_computed_engagement_with_zero_routes_is_not_recomputed_on_read():
    body, rc = await _list(_DB(analysis=object()))
    rc.assert_not_awaited()
    assert body["total"] == 0 and "why_empty" in body


@pytest.mark.asyncio
async def test_a_never_computed_engagement_is_computed_once_on_first_read():
    _, rc = await _list(_DB(analysis=None))
    rc.assert_awaited_once()


@pytest.mark.asyncio
async def test_refresh_still_recomputes_a_computed_engagement():
    _, rc = await _list(_DB(analysis=object()), refresh=True)
    rc.assert_awaited_once()

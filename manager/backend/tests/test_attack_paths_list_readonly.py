"""R8 / NF3 — reading the route list must not recompute-and-write, and must not
even rebuild the analyzer, for an engagement that already has a stored analysis,
even when that analysis found zero routes. The stored diagnostics are served
instead (O(1) read); the analyzer is rebuilt only when nothing was stored."""
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

    def scalar_one(self):
        return 0


class _DB:
    def __init__(self, analysis):
        self.analysis = analysis

    async def get(self, model, key):
        return self.analysis

    async def execute(self, stmt, params=None):
        return _Result()


def _computed(diagnostics):
    """A stored AttackPathAnalysis row (only the fields the read path touches)."""
    return SimpleNamespace(analysis={"diagnostics": diagnostics})


async def _list(db, **kw):
    user = SimpleNamespace(tenant_id=uuid.uuid4())
    args = dict(refresh=False, target_asset_id=None, page=1, page_size=20)
    args.update(kw)
    with patch.object(R, "get_or_404", new=AsyncMock()), \
         patch.object(R, "load_assessment_principal", new=AsyncMock(return_value=user)), \
         patch.object(R, "_recompute_and_store", new=AsyncMock(return_value=[])) as rc, \
         patch.object(R, "_build_analyzer", new=AsyncMock(
             return_value=(MagicMock(diagnose=MagicMock(return_value=["rebuilt"])), None))) as ba, \
         patch.object(R, "_target_ids", new=AsyncMock(return_value=[])):
        body = await R.list_attack_paths(uuid.uuid4(), db, user, **args)
    return body, rc, ba


@pytest.mark.asyncio
async def test_zero_route_read_serves_stored_diagnostics_without_recompute_or_rebuild():
    # NF3: a computed engagement with zero routes neither recomputes nor rebuilds
    # the analyzer; it returns the diagnostics the last recompute stored.
    body, rc, ba = await _list(_DB(_computed(["stored reason"])))
    rc.assert_not_awaited()
    ba.assert_not_awaited()
    assert body["total"] == 0
    assert body["why_empty"] == ["stored reason"]


@pytest.mark.asyncio
async def test_zero_route_read_falls_back_to_rebuild_when_no_diagnostics_stored():
    # Defensive: a pre-NF3 analysis row with no stored diagnostics still explains
    # itself, by rebuilding the analyzer once (never recomputing/writing).
    body, rc, ba = await _list(_DB(_computed(None)))
    rc.assert_not_awaited()
    ba.assert_awaited_once()
    assert body["why_empty"] == ["rebuilt"]


@pytest.mark.asyncio
async def test_a_never_computed_engagement_is_not_written_on_first_read():
    _, rc, ba = await _list(_DB(analysis=None))
    rc.assert_not_awaited()
    ba.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_refresh_requires_the_explicit_write_endpoint():
    from fastapi import HTTPException

    with pytest.raises(HTTPException) as raised:
        await _list(_DB(_computed(["stored reason"])), refresh=True)
    assert raised.value.status_code == 405

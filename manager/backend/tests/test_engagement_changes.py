"""H5 — the changes-since-last-scan endpoint behind 'Re-scan & Change Detection'.

The honest-boundary branches are unit-tested here; the full two-run diff (new hosts,
services, findings) is exercised live against PostgreSQL in the H6 check, which is more
trustworthy than a scripted fake database."""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest

from app.routers import changes as C

_NOW = datetime(2026, 3, 1, 12, 0, tzinfo=timezone.utc)


def _run(started=_NOW):
    return SimpleNamespace(id=uuid.uuid4(), started_at=started, status="completed")


async def _call(latest, prev):
    with patch.object(C, "get_or_404", new=AsyncMock()), \
         patch.object(C, "_two_latest_completed", new=AsyncMock(return_value=(latest, prev))):
        return await C.engagement_changes(uuid.uuid4(), db=object(), current_user=SimpleNamespace(tenant_id=uuid.uuid4()))


@pytest.mark.asyncio
async def test_no_completed_runs_reports_has_runs_false():
    body = await _call(None, None)
    assert body == {"has_runs": False}


@pytest.mark.asyncio
async def test_one_completed_run_is_a_baseline_not_a_comparison():
    body = await _call(_run(), None)
    assert body["has_runs"] is True and body["compared"] is False
    assert "nothing to compare" in body["detail"].lower()


def test_resolved_statuses_are_the_closed_ones_only():
    # a guard so a future enum change does not silently classify 'open' as resolved
    from app.models.enums import FindingStatus
    assert set(C._RESOLVED) == {FindingStatus.remediated, FindingStatus.accepted, FindingStatus.fp}
    assert set(C._OPEN) == {FindingStatus.open, FindingStatus.confirmed}

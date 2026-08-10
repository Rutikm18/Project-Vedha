from __future__ import annotations

import uuid
from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.detection.resolution import evaluate_resolutions
from app.models.enums import FindingSeverity, FindingStatus

_NOW = datetime(2026, 8, 11, tzinfo=timezone.utc)


def _finding(**kw):
    base = dict(
        severity=FindingSeverity.medium, status=FindingStatus.open,
        resolution_miss_count=0, detected_db_version="v1",
        resolved_at=None, resolution_method=None, resolution_run_id=None,
    )
    base.update(kw)
    return SimpleNamespace(**base)


def _db_returning(rows):
    db = MagicMock()
    db.execute = AsyncMock(return_value=MagicMock(all=lambda: rows))
    db.flush = AsyncMock()
    return db


@pytest.mark.asyncio
async def test_covered_clean_medium_finding_is_auto_resolved():
    run = SimpleNamespace(id=uuid.uuid4(), vuln_db_version="v1")
    f = _finding()
    db = _db_returning([(f, "10.0.0.5")])

    resolved = await evaluate_resolutions(db, uuid.uuid4(), run, {"assets": ["10.0.0.5"]}, _NOW)

    assert resolved == 1
    assert f.status == FindingStatus.remediated
    assert f.resolution_method == "auto"
    assert f.resolution_run_id == run.id
    assert f.resolved_at == _NOW
    assert f.resolution_miss_count == 1


@pytest.mark.asyncio
async def test_uncovered_finding_is_left_open():
    run = SimpleNamespace(id=uuid.uuid4(), vuln_db_version="v1")
    f = _finding()
    db = _db_returning([(f, "10.0.0.99")])  # host not in coverage

    resolved = await evaluate_resolutions(db, uuid.uuid4(), run, {"assets": ["10.0.0.5"]}, _NOW)

    assert resolved == 0
    assert f.status == FindingStatus.open
    assert f.resolution_miss_count == 0


@pytest.mark.asyncio
async def test_db_version_change_blocks_resolution():
    run = SimpleNamespace(id=uuid.uuid4(), vuln_db_version="v2")  # DB moved
    f = _finding(detected_db_version="v1")
    db = _db_returning([(f, "10.0.0.5")])

    resolved = await evaluate_resolutions(db, uuid.uuid4(), run, {"assets": ["10.0.0.5"]}, _NOW)

    assert resolved == 0
    assert f.status == FindingStatus.open

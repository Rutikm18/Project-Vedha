from __future__ import annotations

import uuid
from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.detection.resolution import evaluate_resolutions
from app.models.enums import FindingSeverity, FindingStatus

_NOW = datetime(2026, 8, 11, tzinfo=timezone.utc)
_RULE = "POSTURE-TLS-DEPRECATED-PROTOCOL"
# This run re-evaluated the finding's own rule on its own port on 10.0.0.5: the
# per-finding evidence auto-resolution requires on top of host coverage.
_CHECKS = {(_RULE, "10.0.0.5", 443)}


def _finding(**kw):
    base = dict(
        id=uuid.uuid4(),
        severity=FindingSeverity.medium, status=FindingStatus.open,
        resolution_miss_count=0, detected_db_version="v1",
        resolved_at=None, resolution_method=None, resolution_run_id=None,
        evidence={"rule_id": _RULE, "asset_ip": "10.0.0.5", "port": 443},
        cve_ids=None,
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

    resolved = await evaluate_resolutions(db, uuid.uuid4(), run, {"assets": ["10.0.0.5"]}, _NOW,
                                          evaluated_checks=_CHECKS)

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

    # The rule WAS evaluated on this host's port, so only the host gate holds it open.
    resolved = await evaluate_resolutions(db, uuid.uuid4(), run, {"assets": ["10.0.0.5"]}, _NOW,
                                          evaluated_checks={(_RULE, "10.0.0.99", 443)})

    assert resolved == 0
    assert f.status == FindingStatus.open
    assert f.resolution_miss_count == 0


@pytest.mark.asyncio
async def test_db_version_change_blocks_resolution():
    run = SimpleNamespace(id=uuid.uuid4(), vuln_db_version="v2")  # DB moved
    f = _finding(detected_db_version="v1")
    db = _db_returning([(f, "10.0.0.5")])

    resolved = await evaluate_resolutions(db, uuid.uuid4(), run, {"assets": ["10.0.0.5"]}, _NOW,
                                          evaluated_checks=_CHECKS)

    assert resolved == 0
    assert f.status == FindingStatus.open

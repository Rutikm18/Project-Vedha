from __future__ import annotations

import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import HTTPException

from app.models.enums import FindingStatus
from app.routers.findings import reopen_finding
from app.schemas.finding import FindingReopen


def _db_with(finding):
    db = MagicMock()
    db.execute = AsyncMock(return_value=MagicMock(scalar_one_or_none=lambda: finding))
    db.flush = AsyncMock()
    db.refresh = AsyncMock()
    return db


@pytest.mark.asyncio
async def test_reopen_remediated_finding_sets_open_and_audits():
    finding = SimpleNamespace(id=uuid.uuid4(), status=FindingStatus.remediated,
                              reopened_count=0, resolution_miss_count=1,
                              resolved_at="t", resolution_method="auto",
                              resolution_run_id="r", evidence={})
    user = SimpleNamespace(tenant_id=uuid.uuid4(), user_id=uuid.uuid4())
    db = _db_with(finding)

    result = await reopen_finding(
        finding.id,
        db,
        user,
        FindingReopen(reason="Exposure returned in the verification scan"),
    )

    assert result.status == FindingStatus.open
    assert finding.reopened_count == 1
    assert finding.resolution_miss_count == 0
    assert finding.evidence["reopened_by"] == str(user.user_id)
    event = db.add.call_args.args[0]
    assert event.detail["reason"] == "Exposure returned in the verification scan"


@pytest.mark.asyncio
async def test_reopen_non_remediated_is_conflict():
    finding = SimpleNamespace(id=uuid.uuid4(), status=FindingStatus.open)
    user = SimpleNamespace(tenant_id=uuid.uuid4(), user_id=uuid.uuid4())
    db = _db_with(finding)

    with pytest.raises(HTTPException) as exc:
        await reopen_finding(finding.id, db, user)
    assert exc.value.status_code == 409

from __future__ import annotations

import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.models.enums import ScanJobStatus
from app.services.job_result_service import process_job_result


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "terminal_status",
    [ScanJobStatus.completed, ScanJobStatus.failed],
)
async def test_terminal_result_retry_is_idempotent(terminal_status) -> None:
    row = SimpleNamespace(status=terminal_status)
    db = MagicMock()
    db.execute = AsyncMock(
        return_value=MagicMock(scalar_one_or_none=lambda: row)
    )
    db.flush = AsyncMock()

    result = await process_job_result(
        db,
        uuid.uuid4(),
        uuid.uuid4(),
        terminal_status == ScanJobStatus.completed,
        {"facts": [{"type": "test"}]},
        "scanner failed" if terminal_status == ScanJobStatus.failed else None,
    )

    assert result == {
        "ok": True,
        "duplicate": True,
        "assets_promoted": 0,
        "findings_created": 0,
    }
    db.add.assert_not_called()
    db.flush.assert_not_awaited()

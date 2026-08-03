from __future__ import annotations

import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.models.enums import ScanJobStatus
from app.services.job_result_service import process_job_result, validate_result_scope


def test_result_scope_accepts_authorized_targets_and_control_records() -> None:
    result = {
        "hosts": [{"ip": "10.20.0.8"}],
        "facts": [
            {"target": "10.20.0.8", "status": "open"},
            {"target": "<nmap-run>", "status": "error"},
        ],
        "findings": [{"target": "10.20.0.8:443"}],
    }

    assert validate_result_scope(result, ["10.20.0.0/24"], []) == []


@pytest.mark.parametrize(
    ("scope", "excluded", "target"),
    [
        ([], [], "10.20.0.8"),
        (["not-a-cidr"], [], "10.20.0.8"),
        (["10.20.0.0/24"], [], "10.21.0.8"),
        (["10.20.0.0/24"], ["10.20.0.8/32"], "10.20.0.8"),
        (["10.20.0.0/24"], [], "host.internal"),
    ],
)
def test_result_scope_fails_closed(scope, excluded, target) -> None:
    rejected = validate_result_scope(
        {"facts": [{"target": target}]},
        scope,
        excluded,
    )

    assert rejected == [{"path": "facts[0].target", "value": target}]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "terminal_status",
    [ScanJobStatus.completed, ScanJobStatus.failed],
)
async def test_terminal_result_retry_is_idempotent(terminal_status) -> None:
    attempt_id = uuid.uuid4()
    payload_result = {"facts": [{"type": "test"}]}
    payload_error = "scanner failed" if terminal_status == ScanJobStatus.failed else None
    from app.services.job_result_service import result_checksum
    attempt = SimpleNamespace(
        status="succeeded" if terminal_status == ScanJobStatus.completed else "failed",
        result_checksum=result_checksum(
            terminal_status == ScanJobStatus.completed,
            payload_result,
            payload_error,
        ),
    )
    row = SimpleNamespace(
        status=terminal_status,
        current_attempt_id=attempt_id,
        current_fence=3,
    )
    db = MagicMock()
    db.execute = AsyncMock(side_effect=[
        MagicMock(scalar_one_or_none=lambda: row),
        MagicMock(scalar_one_or_none=lambda: attempt),
    ])
    db.flush = AsyncMock()

    result = await process_job_result(
        db,
        uuid.uuid4(),
        uuid.uuid4(),
        terminal_status == ScanJobStatus.completed,
        payload_result,
        payload_error,
        attempt_id,
        3,
    )

    assert result == {
        "ok": True,
        "duplicate": True,
        "assets_promoted": 0,
        "findings_created": 0,
    }
    db.add.assert_not_called()
    db.flush.assert_not_awaited()


@pytest.mark.asyncio
async def test_out_of_scope_result_is_rejected_before_database_mutation() -> None:
    row = SimpleNamespace(
        status=ScanJobStatus.running,
        current_attempt_id=(attempt_id := uuid.uuid4()),
        current_fence=5,
        result={
            "_scope_cidrs": ["10.20.0.0/24"],
            "_excluded_cidrs": ["10.20.0.9/32"],
        },
    )
    db = MagicMock()
    attempt = SimpleNamespace(status="running", result_checksum=None)
    db.execute = AsyncMock(side_effect=[
        MagicMock(scalar_one_or_none=lambda: row),
        MagicMock(scalar_one_or_none=lambda: attempt),
    ])
    db.flush = AsyncMock()

    summary = await process_job_result(
        db,
        uuid.uuid4(),
        uuid.uuid4(),
        True,
        {"facts": [{"target": "10.20.0.9", "status": "open"}]},
        None,
        attempt_id,
        5,
    )

    assert summary["ok"] is False
    assert summary["status_code"] == 422
    assert summary["permanent_rejection"] is True
    assert row.status == ScanJobStatus.running
    db.add.assert_not_called()
    db.flush.assert_not_awaited()


@pytest.mark.asyncio
async def test_stale_attempt_gets_terminal_receipt_without_mutation() -> None:
    row = SimpleNamespace(
        status=ScanJobStatus.running,
        current_attempt_id=uuid.uuid4(),
        current_fence=9,
    )
    db = MagicMock()
    db.execute = AsyncMock(return_value=MagicMock(scalar_one_or_none=lambda: row))
    db.flush = AsyncMock()

    summary = await process_job_result(
        db,
        uuid.uuid4(),
        uuid.uuid4(),
        True,
        {"facts": [{"target": "10.20.0.8"}]},
        None,
        uuid.uuid4(),
        8,
    )

    assert summary["ok"] is True
    assert summary["accepted"] is False
    assert summary["stale"] is True
    assert row.status == ScanJobStatus.running
    db.flush.assert_not_awaited()

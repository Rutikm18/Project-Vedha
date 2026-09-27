from __future__ import annotations

import uuid
from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.detection import engine_bridge
from app.detection.engine_bridge import (
    _apply_regression_reopen,
    _persist_attack_paths,
    _record_regression_reopen,
)
from app.models.enums import FindingSeverity, FindingStatus


def test_reopen_flips_remediated_to_open_and_flags_regression():
    now = object()
    run_id = uuid.uuid4()
    f = SimpleNamespace(
        status=FindingStatus.remediated, reopened_count=0,
        resolution_miss_count=3, resolved_at="old", resolution_method="auto",
        resolution_run_id=uuid.uuid4(),
        evidence={"cve_id": "CVE-1"}, last_seen=None, detection_run_id=None,
    )
    _apply_regression_reopen(f, run_id, now)

    assert f.status == FindingStatus.open
    assert f.reopened_count == 1
    assert f.resolution_miss_count == 0
    assert f.resolved_at is None
    assert f.resolution_method is None
    assert f.resolution_run_id is None
    assert f.evidence["regression"] is True
    assert f.last_seen is now
    assert f.detection_run_id == run_id


@pytest.mark.asyncio
async def test_regression_reopen_persists_engine_attributed_repeat_event(monkeypatch):
    now = datetime(2026, 9, 27, 5, 30, tzinfo=timezone.utc)
    run_id = uuid.uuid4()
    prior_run_id = uuid.uuid4()
    resolved_at = datetime(2026, 9, 26, 5, 30, tzinfo=timezone.utc)
    finding = SimpleNamespace(
        status=FindingStatus.remediated,
        reopened_count=0,
        resolution_miss_count=2,
        resolved_at=resolved_at,
        resolution_method="auto",
        resolution_run_id=prior_run_id,
        evidence={},
        last_seen=None,
        detection_run_id=None,
    )
    recorder = AsyncMock()
    monkeypatch.setattr(engine_bridge, "record_event", recorder)

    await _record_regression_reopen(object(), finding, run_id, now)

    recorder.assert_awaited_once()
    call = recorder.await_args
    assert call.args[2] == "reopened"
    assert call.kwargs["actor"] == "detection-engine"
    assert call.kwargs["actor_type"] == "system"
    assert call.kwargs["from_status"] == FindingStatus.remediated
    assert call.kwargs["to_status"] == FindingStatus.open
    assert call.kwargs["detail"] == {
        "origin": "detection_engine_regression",
        "reason": "finding re-observed in a later detection run",
        "run_id": str(run_id),
        "observed_at": now.isoformat(),
        "prior_resolution_method": "auto",
        "prior_resolution_run_id": str(prior_run_id),
        "prior_resolved_at": resolved_at.isoformat(),
    }


@pytest.mark.asyncio
async def test_attack_path_regression_reopens_existing_finding(monkeypatch):
    now = datetime(2026, 9, 27, 5, 30, tzinfo=timezone.utc)
    engagement_id = uuid.uuid4()
    run = SimpleNamespace(id=uuid.uuid4())
    asset = SimpleNamespace(id=uuid.uuid4())
    regressed = SimpleNamespace(evidence={"prior": "proof"})
    reopen = AsyncMock()
    db = MagicMock()
    db.add = MagicMock()
    db.flush = AsyncMock()

    monkeypatch.setattr(engine_bridge, "_engagement_device_roles", AsyncMock(return_value={}))
    monkeypatch.setattr(
        engine_bridge,
        "attack_path_findings",
        lambda *_: [
            {
                "title": "NTLM relay path",
                "rule_id": "CORR-NTLM-RELAY-PATH",
                "target": "192.0.2.10",
                "severity": FindingSeverity.critical,
                "evidence": {"source": "correlation"},
            }
        ],
    )
    monkeypatch.setattr(engine_bridge, "_resolve_asset", AsyncMock(return_value=asset))
    monkeypatch.setattr(
        engine_bridge, "_find_open_duplicate", AsyncMock(return_value=None)
    )
    monkeypatch.setattr(
        engine_bridge, "_find_remediated_match", AsyncMock(return_value=regressed)
    )
    monkeypatch.setattr(engine_bridge, "_record_regression_reopen", reopen)

    created = await _persist_attack_paths(
        db, engagement_id, run, [{"accepted": True}], now
    )

    assert created == 0
    reopen.assert_awaited_once_with(db, regressed, run.id, now)
    assert regressed.severity == FindingSeverity.critical
    assert regressed.evidence["regression"] is True
    db.add.assert_not_called()

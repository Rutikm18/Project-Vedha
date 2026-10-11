"""
Job-status routes must scope the engagement to the caller's tenant.

  * vuln_scans.scan_status looked a job up by (job_id, engagement_id) alone, so a
    user in tenant A could read tenant B's scan job (result included) by supplying
    B's ids — a cross-tenant IDOR. Every sibling status route already gates on
    get_or_404(db, Engagement, engagement_id, tenant_id) first.
  * ad.py passed `db` twice to get_or_404, shifting every argument one slot right
    (id=db, tenant_id=engagement_id, tenant_field=<UUID>), so both AD routes
    raised before reaching the handler body — HTTP 500 on every call.
"""
from __future__ import annotations

import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import BackgroundTasks, HTTPException

from app.models.engagement import Engagement
from app.models.enums import ScanJobStatus, ScanJobType
from app.routers import ad as ad_router
from app.routers import vuln_scans
from app.schemas.auth import CurrentUser


def _user() -> CurrentUser:
    return CurrentUser(user_id=uuid.uuid4(), tenant_id=uuid.uuid4(), role="admin")


def _result(value):
    r = MagicMock()
    r.scalar_one_or_none.return_value = value
    return r


def _job(job_type=ScanJobType.vuln_scan):
    return SimpleNamespace(
        id=uuid.uuid4(), status=ScanJobStatus.completed, job_type=job_type,
        started_at=None, completed_at=None, result={"secret": "other-tenant-data"},
    )


def _not_in_tenant(*_a, **_k):
    raise HTTPException(404, "Engagement not found")


# ── vuln_scans.scan_status ────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_scan_status_rejects_engagement_outside_caller_tenant(monkeypatch):
    db = MagicMock()
    db.execute = AsyncMock(return_value=_result(_job()))  # job exists (other tenant)
    monkeypatch.setattr(vuln_scans, "get_or_404", AsyncMock(side_effect=_not_in_tenant))

    with pytest.raises(HTTPException) as exc:
        await vuln_scans.scan_status(uuid.uuid4(), uuid.uuid4(), db, _user())

    assert exc.value.status_code == 404


@pytest.mark.asyncio
async def test_scan_status_scopes_engagement_to_tenant(monkeypatch):
    user, eng_id = _user(), uuid.uuid4()
    db = MagicMock()
    db.execute = AsyncMock(return_value=_result(_job()))
    spy = AsyncMock(return_value=SimpleNamespace(id=eng_id))
    monkeypatch.setattr(vuln_scans, "get_or_404", spy)

    out = await vuln_scans.scan_status(eng_id, uuid.uuid4(), db, user)

    spy.assert_awaited_once_with(db, Engagement, eng_id, user.tenant_id)
    assert out["status"] == "completed"


# ── ad.py ─────────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_ad_status_passes_correct_args_to_get_or_404(monkeypatch):
    user, eng_id = _user(), uuid.uuid4()
    db = MagicMock()
    db.execute = AsyncMock(return_value=_result(_job(ScanJobType.ad_enum)))
    spy = AsyncMock(return_value=SimpleNamespace(id=eng_id))
    monkeypatch.setattr(ad_router, "get_or_404", spy)

    out = await ad_router.ad_assessment_status(eng_id, uuid.uuid4(), db, user)

    spy.assert_awaited_once_with(db, Engagement, eng_id, user.tenant_id)
    assert out["status"] == "completed"


@pytest.mark.asyncio
async def test_ad_status_real_get_or_404_does_not_crash():
    """Unpatched: the real helper must receive a valid call (was a TypeError → 500)."""
    user, eng_id = _user(), uuid.uuid4()
    db = MagicMock()
    db.execute = AsyncMock(side_effect=[
        _result(SimpleNamespace(id=eng_id)),          # engagement (tenant-scoped)
        _result(_job(ScanJobType.ad_enum)),          # the AD job
    ])

    out = await ad_router.ad_assessment_status(eng_id, uuid.uuid4(), db, user)

    assert out["status"] == "completed"


@pytest.mark.asyncio
async def test_ad_launch_passes_correct_args_to_get_or_404(monkeypatch):
    user, eng_id = _user(), uuid.uuid4()
    db = MagicMock()
    db.flush = AsyncMock()
    db.refresh = AsyncMock()
    spy = AsyncMock(return_value=SimpleNamespace(id=eng_id, scope_cidrs=["10.0.0.0/24"], excluded_cidrs=[]))
    monkeypatch.setattr(ad_router, "get_or_404", spy)
    body = ad_router.ADAssessRequest.model_validate(
        {"dc_ip": "10.0.0.10", "domain": "corp.local", "username": "u", "password": "p"}
    )

    await ad_router.launch_ad_assessment(eng_id, body, db, BackgroundTasks(), user)

    spy.assert_awaited_once_with(db, Engagement, eng_id, user.tenant_id)


# ── detection.py (same shifted-args bug on all five routes) ───────────────────

@pytest.mark.asyncio
async def test_detection_results_real_get_or_404_does_not_crash():
    """Was TypeError → 500 on every detection-validation route."""
    user, eng_id = _user(), uuid.uuid4()
    rows = MagicMock()
    rows.scalars.return_value.all.return_value = []
    count = MagicMock()
    count.scalar_one.return_value = 0
    db = MagicMock()
    db.execute = AsyncMock(side_effect=[_result(SimpleNamespace(id=eng_id)), count, rows, rows])

    from app.routers import detection
    try:
        await detection.get_results(eng_id, db, user, None, 1, 50)
    except TypeError as exc:  # the regression signature
        pytest.fail(f"get_or_404 called with shifted args: {exc}")
    except (AttributeError, ValueError, StopAsyncIteration):
        pass  # downstream mock shape is not what this test pins


def test_no_router_passes_db_twice_to_get_or_404():
    import pathlib
    import re
    offenders = [
        f"{p.name}:{i}" for p in pathlib.Path("app").rglob("*.py")
        for i, line in enumerate(p.read_text().splitlines(), 1)
        if re.search(r"get_or_404\(db,\s*\w+,\s*db\b", line)
    ]
    assert offenders == []

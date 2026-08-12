"""Mocked-session unit tests for the P3 active-validation endpoints (Task 4).

No DB: the AsyncSession is mocked (execute/flush/refresh/add), following the
tests/test_job_result_service.py style. Asserts the approval-gated state machine
and that approve enqueues a single-target, safe ``mode=validate`` job.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import HTTPException

from app.models.enums import ScanJobType
from app.models.validation_request import CHECK_TLS, VR_APPROVED, VR_PENDING, VR_REJECTED
from app.routers.validation import (
    RejectBody,
    ValidateRequest,
    approve_validation,
    create_validation_request,
    reject_validation,
)


def _exec(scalar):
    r = MagicMock()
    r.scalar_one_or_none.return_value = scalar
    return r


def _mock_db(execute_returns):
    db = MagicMock()
    db.execute = AsyncMock(side_effect=[_exec(x) for x in execute_returns])
    db.add = MagicMock()
    db.flush = AsyncMock()

    async def _refresh(obj):
        if getattr(obj, "id", None) is None:
            obj.id = uuid.uuid4()
        if hasattr(type(obj), "requested_at") and getattr(obj, "requested_at", None) is None:
            obj.requested_at = datetime.now(timezone.utc)

    db.refresh = AsyncMock(side_effect=_refresh)
    return db


def _user():
    return SimpleNamespace(tenant_id=uuid.uuid4(), user_id=uuid.uuid4())


@pytest.mark.asyncio
async def test_create_request_is_pending_and_derives_tls_check():
    eng_id, finding_id = uuid.uuid4(), uuid.uuid4()
    engagement = SimpleNamespace(id=eng_id, tenant_id=uuid.uuid4(), rules_of_engagement=None)
    finding = SimpleNamespace(id=finding_id, engagement_id=eng_id,
                              title="TLS 1.0 enabled", evidence={})
    db = _mock_db([engagement, finding])

    out = await create_validation_request(
        eng_id, finding_id, ValidateRequest(target_ip="10.0.0.5", target_port=443),
        db, _user(),
    )

    assert out.status == VR_PENDING
    assert out.check_kind == CHECK_TLS      # derived from the finding's title
    assert out.target_ip == "10.0.0.5"
    assert db.add.call_count == 1


@pytest.mark.asyncio
async def test_create_rejected_when_roe_forbids():
    eng_id, finding_id = uuid.uuid4(), uuid.uuid4()
    engagement = SimpleNamespace(id=eng_id, tenant_id=uuid.uuid4(),
                                 rules_of_engagement={"active_validation_allowed": False})
    finding = SimpleNamespace(id=finding_id, engagement_id=eng_id, title="x", evidence={})
    db = _mock_db([engagement, finding])

    with pytest.raises(HTTPException) as exc:
        await create_validation_request(
            eng_id, finding_id, ValidateRequest(target_ip="10.0.0.5"), db, _user()
        )
    assert exc.value.status_code == 403


@pytest.mark.asyncio
async def test_approve_enqueues_safe_validate_job():
    req_id, eng_id, finding_id = uuid.uuid4(), uuid.uuid4(), uuid.uuid4()
    vr = SimpleNamespace(
        id=req_id, engagement_id=eng_id, finding_id=finding_id, target_ip="10.0.0.5",
        target_port=443, check_kind=CHECK_TLS, status=VR_PENDING, outcome=None,
        job_id=None, requested_by="u", requested_at=datetime.now(timezone.utc),
        reviewed_by=None, reviewed_at=None,
    )
    engagement = SimpleNamespace(id=eng_id, rules_of_engagement=None)
    db = _mock_db([vr, engagement])

    resp = await approve_validation(req_id, db, _user())

    assert resp["approved"] is True
    assert vr.status == VR_APPROVED
    assert vr.job_id is not None
    # exactly one ScanJob was enqueued, safe + single-target + validate mode
    job = db.add.call_args_list[0].args[0]
    assert job.job_type == ScanJobType.vuln_scan
    assert job.result["mode"] == "validate"
    assert job.result["check_kind"] == CHECK_TLS
    assert job.result["target"] == "10.0.0.5"
    assert job.result["allowlist"] == "safe"
    assert job.result["scope_cidrs"] == ["10.0.0.5/32"]


@pytest.mark.asyncio
async def test_approve_conflict_when_not_pending():
    req_id = uuid.uuid4()
    vr = SimpleNamespace(id=req_id, engagement_id=uuid.uuid4(), status=VR_APPROVED)
    db = _mock_db([vr])
    with pytest.raises(HTTPException) as exc:
        await approve_validation(req_id, db, _user())
    assert exc.value.status_code == 409


@pytest.mark.asyncio
async def test_reject_marks_rejected():
    req_id = uuid.uuid4()
    vr = SimpleNamespace(id=req_id, engagement_id=uuid.uuid4(), status=VR_PENDING,
                         reviewed_by=None, reviewed_at=None)
    db = _mock_db([vr])
    resp = await reject_validation(req_id, RejectBody(reason="not needed"), db, _user())
    assert resp["rejected"] is True
    assert vr.status == VR_REJECTED

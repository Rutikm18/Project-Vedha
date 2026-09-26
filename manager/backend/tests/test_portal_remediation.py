"""
test_portal_remediation.py — Section 6: the customer-facing remediation route.

The gate mirrors the approved-report gate: the deterministic KB recipe is served
ALWAYS, but a stored AI plan reaches the customer only once an operator has marked
it reviewed. Handlers are called directly with a mocked async db (repo convention).
"""
from __future__ import annotations

import asyncio
import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import HTTPException

from app.routers import portal
from app.schemas.auth import CurrentUser


def _client(engagement: uuid.UUID | None = None) -> CurrentUser:
    return CurrentUser(user_id=uuid.uuid4(), tenant_id=uuid.uuid4(), role="client",
                       client_engagement_id=engagement or uuid.uuid4())


def _finding(title="SSLv3 supported (POODLE)"):
    from datetime import datetime, timezone

    from app.models.enums import FindingSeverity, FindingStatus
    now = datetime.now(timezone.utc)
    return SimpleNamespace(id=uuid.uuid4(), engagement_id=uuid.uuid4(), title=title,
                           description="", remediation="", cve_ids=[],
                           severity=FindingSeverity.high, status=FindingStatus.open,
                           first_seen=now, created_at=now, due_at=None)


def _db_scalar(*vals):
    """Each db.execute(...) → result whose .scalar_one_or_none() is the next val."""
    db = MagicMock()
    results = []
    for v in vals:
        r = MagicMock()
        r.scalar_one_or_none = MagicMock(return_value=v)
        results.append(r)
    db.execute = AsyncMock(side_effect=results)
    return db


class TestPortalRemediation:
    def test_serves_kb_when_no_stored_plan(self):
        db = _db_scalar(_finding(), None, None, None)   # finding, no plan row, no engagement/tenant SLA
        res = asyncio.run(portal.portal_finding_remediation(
            uuid.uuid4(), _client(), db, os="linux"))
        assert res["source"] == "deterministic_kb"
        assert res["os"] == "linux"
        assert res["plan"]["steps"]

    def test_serves_reviewed_ai_plan_stripping_operator_metadata(self):
        ai_plan = {"source": "ai", "summary": "patch it", "model": "claude-x",
                   "steps": [{"step": 1}]}
        row = SimpleNamespace(reviewed=True, source="ai", plan=ai_plan)
        db = _db_scalar(_finding(), row, None, None)
        res = asyncio.run(portal.portal_finding_remediation(
            uuid.uuid4(), _client(), db, os="linux"))
        assert res["source"] == "ai"
        assert res["plan"]["due"]["source"] == "default"
        assert res["plan"]["summary"] == "patch it"
        assert "model" not in res["plan"]      # operator-only metadata not leaked to customer

    def test_unreviewed_ai_plan_does_not_leak(self):
        # An AI plan that an operator has NOT reviewed must never reach the customer;
        # the KB recipe is served instead.
        ai_plan = {"source": "ai", "summary": "secret", "steps": [{"step": 1}]}
        row = SimpleNamespace(reviewed=False, source="ai", plan=ai_plan)
        db = _db_scalar(_finding(), row, None, None)
        res = asyncio.run(portal.portal_finding_remediation(
            uuid.uuid4(), _client(), db, os="linux"))
        assert res["source"] == "deterministic_kb"
        assert res["plan"]["steps"]

    def test_missing_or_out_of_scope_finding_is_404(self):
        db = _db_scalar(None)                       # scoped finding query returns None
        with pytest.raises(HTTPException) as e:
            asyncio.run(portal.portal_finding_remediation(
                uuid.uuid4(), _client(), db, os="linux"))
        assert e.value.status_code == 404

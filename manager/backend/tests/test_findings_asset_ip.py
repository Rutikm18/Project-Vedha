"""Findings carry the affected asset's IP, and the queue filters by it.

Regression: list responses left asset_context null (to avoid an N+1), so the UI's
"affected host" fell back to the asset UUID. The list now resolves identity for
the whole page in ONE query, and `asset_ip` filters by exact IP or prefix.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import HTTPException
from sqlalchemy import select

from app.models.enums import DetectionStatus, FindingSeverity, FindingStatus
from app.models.finding import Finding
from app.routers import findings as findings_router
from app.schemas.auth import CurrentUser


def _sql(clause) -> str:
    return str(select(Finding.id).where(clause).compile(compile_kwargs={"literal_binds": True}))


def test_exact_ip_is_equality():
    sql = _sql(findings_router.asset_ip_clause("192.168.1.78"))
    assert "assets.ip_address = '192.168.1.78'" in sql


def test_ipv6_exact():
    sql = _sql(findings_router.asset_ip_clause("fe80::1"))
    assert "assets.ip_address = 'fe80::1'" in sql


def test_partial_ip_is_prefix():
    sql = _sql(findings_router.asset_ip_clause("192.168.1."))
    assert "assets.ip_address LIKE '192.168.1.' || '%'" in sql


@pytest.mark.parametrize("bad", ["192.168.1.1' OR 1=1", "10.0.0.%", "host_name", "a" * 50])
def test_non_ip_input_is_rejected(bad):
    with pytest.raises(HTTPException) as e:
        findings_router.asset_ip_clause(bad)
    assert e.value.status_code == 422


def _orm_finding(asset_id):
    now = datetime.now(timezone.utc)
    return Finding(
        id=uuid.uuid4(), engagement_id=uuid.uuid4(), asset_id=asset_id, cve_ids=None,
        title="t", description=None, cvss_score=None, cvss_vector=None, epss_score=None,
        risk_score=None, severity=FindingSeverity.high, status=FindingStatus.open,
        exploitable=False, exploit_validated=False, mitre_techniques=None,
        detection_status=DetectionStatus.detected, evidence={}, remediation=None,
        needs_review=False, reopened_count=0, created_at=now, updated_at=now,
    )


@pytest.mark.asyncio
async def test_page_asset_identity_is_one_query():
    a1, a2 = uuid.uuid4(), uuid.uuid4()
    rows = [_orm_finding(a1), _orm_finding(a2), _orm_finding(a1), _orm_finding(None)]
    result = MagicMock()
    result.all.return_value = [(a1, "192.168.1.78", "nas"), (a2, "192.168.1.1", None)]
    db = MagicMock()
    db.execute = AsyncMock(return_value=result)

    out = await findings_router._with_asset_identity(db, rows)

    assert db.execute.await_count == 1
    assert [o.asset_ip for o in out] == ["192.168.1.78", "192.168.1.1", "192.168.1.78", None]
    assert out[0].asset_hostname == "nas"


@pytest.mark.asyncio
async def test_page_without_assets_skips_the_query():
    db = MagicMock()
    db.execute = AsyncMock()
    out = await findings_router._with_asset_identity(db, [_orm_finding(None)])
    assert db.execute.await_count == 0
    assert out[0].asset_ip is None


@pytest.mark.asyncio
async def test_list_findings_applies_asset_ip_filter():
    captured = {}

    async def fake_paginate(db, q, page, page_size):
        captured["sql"] = str(q.compile(compile_kwargs={"literal_binds": True}))
        return [], 0

    user = CurrentUser(user_id=uuid.uuid4(), tenant_id=uuid.uuid4(), role="manager")
    with patch.object(findings_router, "paginate_query", fake_paginate):
        await findings_router.list_findings(
            db=MagicMock(), current_user=user, severity=None, status_filter=None,
            active_only=False, asset_id=None, asset_ip="192.168.1.78",
            mitre_technique=None, engagement_id=None, agent_id=None, search=None,
            detection_status=None, exploit_validated=None, verification_state=None,
            needs_review=None, sla_breached=False, sort="risk", page=1, page_size=20)

    assert "JOIN assets ON assets.id = findings.asset_id" in captured["sql"]
    assert "assets.ip_address = '192.168.1.78'" in captured["sql"]

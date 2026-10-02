"""Portal lock guard against a real PostgreSQL — the parts compilation can't prove:
the Enum severity comparison, query caching across requests with DIFFERENT
locks, and the real operator handler the portal delegates to.

OPT-IN: skipped unless PORTAL_LOCKS_TEST_DB_URL points at a migrated database
(alembic upgrade head). Every test runs in a transaction that is rolled back.
"""
from __future__ import annotations

import os
import uuid
from types import SimpleNamespace

import pytest
import pytest_asyncio
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from app.models.engagement import Engagement
from app.models.enums import DetectionStatus, EngagementStatus, FindingSeverity, FindingStatus
from app.models.finding import Finding
from app.models.tenant import Tenant
from app.services import portal_locks

URL = os.environ.get("PORTAL_LOCKS_TEST_DB_URL")
pytestmark = pytest.mark.skipif(not URL, reason="set PORTAL_LOCKS_TEST_DB_URL to a migrated test DB")

SEVERITIES = ("critical", "high", "medium", "low")


@pytest_asyncio.fixture
async def seeded():
    engine = create_async_engine(URL)
    conn = await engine.connect()
    trans = await conn.begin()
    db = AsyncSession(bind=conn, expire_on_commit=False)
    tenant = Tenant(name=f"locks-{uuid.uuid4().hex[:6]}")
    db.add(tenant)
    await db.flush()
    eng = Engagement(tenant_id=tenant.id, name="Locks test", status=EngagementStatus.active)
    db.add(eng)
    await db.flush()
    for sev in SEVERITIES:
        db.add(Finding(engagement_id=eng.id, title=f"{sev} finding", severity=FindingSeverity(sev),
                       status=FindingStatus.open, detection_status=DetectionStatus.detected))
    await db.flush()
    try:
        yield db, tenant, eng
    finally:
        # pytest-asyncio finalizes in another context; clear rather than reset.
        portal_locks._LOCKED.set(None)
        await db.close()
        await trans.rollback()
        await conn.close()
        await engine.dispose()


async def _titles(db, eng) -> list[str]:
    rows = (await db.execute(select(Finding.title).where(Finding.engagement_id == eng.id))).scalars().all()
    return sorted(rows)


@pytest.mark.asyncio
async def test_locked_severities_are_invisible_and_operators_see_all(seeded):
    db, _, eng = seeded
    assert len(await _titles(db, eng)) == 4                         # operator: no guard
    portal_locks.activate(["critical", "high"])
    assert await _titles(db, eng) == ["low finding", "medium finding"]
    count = (await db.execute(select(func.count()).select_from(Finding)
                              .where(Finding.engagement_id == eng.id))).scalar_one()
    assert count == 2
    rows = (await db.execute(select(Finding).where(Finding.engagement_id == eng.id))).scalars().all()
    assert {r.severity.value for r in rows} == {"medium", "low"}


@pytest.mark.asyncio
async def test_cached_queries_follow_each_requests_own_locks(seeded):
    db, _, eng = seeded
    portal_locks.activate(["critical", "high"])
    assert await _titles(db, eng) == ["low finding", "medium finding"]
    portal_locks.activate(["low"])                                  # same SQL shape, new locks
    assert await _titles(db, eng) == ["critical finding", "high finding", "medium finding"]
    portal_locks.activate([])
    assert len(await _titles(db, eng)) == 4


@pytest.mark.asyncio
async def test_lifted_counts_locked_findings_for_the_teaser(seeded):
    db, _, eng = seeded
    portal_locks.activate(["critical", "high"])
    with portal_locks.lifted():
        rows = (await db.execute(
            select(Finding.severity, func.count()).where(Finding.engagement_id == eng.id)
            .group_by(Finding.severity))).all()
    assert {s.value: n for s, n in rows} == {"critical": 1, "high": 1, "medium": 1, "low": 1}
    assert await _titles(db, eng) == ["low finding", "medium finding"]  # guard back on


@pytest.mark.asyncio
async def test_the_delegated_operator_finding_list_is_filtered(seeded):
    db, tenant, eng = seeded
    from app.routers.findings import list_findings
    user = SimpleNamespace(tenant_id=tenant.id, user_id=uuid.uuid4(), role="client",
                           client_engagement_id=eng.id)
    portal_locks.activate(["critical", "high"])
    page = await list_findings(
        db=db, current_user=user, severity=None, status_filter=None, active_only=False,
        asset_id=None, asset_ip=None, mitre_technique=None, engagement_id=eng.id, agent_id=None,
        scan=None, search=None, detection_status=None, exploit_validated=None,
        verification_state=None, needs_review=None, sla_breached=False, sort="risk",
        page=1, page_size=50)
    items = page.items if hasattr(page, "items") else page["items"]
    assert sorted(i.severity.value if hasattr(i.severity, "value") else i.severity for i in items) == ["low", "medium"]

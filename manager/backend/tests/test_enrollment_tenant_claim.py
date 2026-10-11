"""Probe enrollment: an unclaimed device request cannot be adopted across tenants.

A new device files an enrollment request without logging in, so until someone
approves it the request belongs to no tenant. It used to be listed to every
tenant's admins and claimable by id (no user code), so on a multi-tenant Manager
tenant A could adopt a probe installed in tenant B's network.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import HTTPException

from app.routers import probe_enrollment as pe

TENANT_A = uuid.uuid4()
TENANT_B = uuid.uuid4()


def _user(tenant=TENANT_A):
    return SimpleNamespace(user_id=uuid.uuid4(), tenant_id=tenant, role="admin")


def _row(tenant_id=None, state="awaiting_approval"):
    return SimpleNamespace(
        id=uuid.uuid4(), tenant_id=tenant_id, state=state,
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=10),
        reported_capabilities=["tcp_scan"],
    )


class _Db:
    """Answers the tenant count first, then the row the query asks for."""

    def __init__(self, active_tenants, row=None, rows=()):
        self.statements = []
        self._count = active_tenants
        self._row = row
        self._rows = list(rows)

    async def execute(self, stmt):
        self.statements.append(stmt)
        result = MagicMock()
        text = str(stmt)
        if "count(" in text.lower():
            result.scalar_one = MagicMock(return_value=self._count)
        else:
            result.scalar_one_or_none = MagicMock(return_value=self._row)
            result.scalars = MagicMock(return_value=SimpleNamespace(all=lambda: self._rows))
        return result


@pytest.mark.asyncio
async def test_single_tenant_mode_counts_active_tenants():
    assert await pe._single_tenant_mode(_Db(1)) is True
    assert await pe._single_tenant_mode(_Db(2)) is False
    assert await pe._single_tenant_mode(_Db(0)) is False


@pytest.mark.asyncio
async def test_list_hides_unclaimed_requests_on_a_multi_tenant_manager():
    db = _Db(active_tenants=3)
    await pe.list_enrollment_requests(db=db, current_user=_user())
    where = str(db.statements[-1].compile(compile_kwargs={"literal_binds": False}))
    assert "tenant_id IS NULL" not in where


@pytest.mark.asyncio
async def test_list_shows_unclaimed_requests_to_the_only_tenant():
    db = _Db(active_tenants=1)
    await pe.list_enrollment_requests(db=db, current_user=_user())
    where = str(db.statements[-1].compile(compile_kwargs={"literal_binds": False}))
    assert "tenant_id IS NULL" in where


@pytest.mark.asyncio
async def test_one_click_claim_refused_for_unclaimed_request_on_multi_tenant_manager():
    row = _row(tenant_id=None)
    db = _Db(active_tenants=2, row=row)
    with pytest.raises(HTTPException) as exc:
        await pe.approve_request_simple(row.id, db, _user())
    assert exc.value.status_code == 403
    assert row.state == "awaiting_approval"


@pytest.mark.asyncio
async def test_one_click_claim_refused_for_another_tenants_request():
    row = _row(tenant_id=TENANT_B)
    db = _Db(active_tenants=1, row=row)
    with pytest.raises(HTTPException) as exc:
        await pe.approve_request_simple(row.id, db, _user(TENANT_A))
    assert exc.value.status_code == 404


@pytest.mark.asyncio
async def test_one_click_claim_still_works_for_the_only_tenant(monkeypatch):
    row = _row(tenant_id=None)
    db = _Db(active_tenants=1, row=row)
    db.add = MagicMock()
    db.flush = AsyncMock()
    agent = SimpleNamespace(id=uuid.uuid4())
    monkeypatch.setattr(pe, "_provision_agent_for_site", AsyncMock(return_value=agent))
    monkeypatch.setattr(pe, "_next_probe_name", AsyncMock(return_value="vedha_agent_01"))
    out = await pe.approve_request_simple(row.id, db, _user())
    assert out["agent_id"] == str(agent.id)


@pytest.mark.asyncio
async def test_code_approval_refused_for_another_tenants_request():
    row = _row(tenant_id=TENANT_B)
    db = _Db(active_tenants=2, row=row)
    body = SimpleNamespace(user_code="ABCD-2345")
    with pytest.raises(HTTPException) as exc:
        await pe.approve_enrollment(body, db, _user(TENANT_A))
    assert exc.value.status_code == 404

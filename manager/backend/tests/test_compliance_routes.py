"""Engagement profile + compliance endpoints."""
from __future__ import annotations

import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import HTTPException

from app.compliance.profile import EngagementProfile
from app.models.audit_log import AuditLog
from app.routers import compliance as routes


def _user():
    return SimpleNamespace(tenant_id=uuid.uuid4(), user_id=uuid.uuid4(), role="admin")


def _eng(roe=None):
    return SimpleNamespace(id=uuid.uuid4(), rules_of_engagement=roe)


def _one(obj):
    return MagicMock(scalar_one_or_none=lambda: obj)


def _scalars(items):
    return MagicMock(scalars=lambda: MagicMock(all=lambda: items))


def _db(*results):
    db = MagicMock()
    db.execute = AsyncMock(side_effect=list(results))
    db.flush = AsyncMock()
    db.added = []
    db.add = lambda o: db.added.append(o)
    return db


@pytest.mark.asyncio
async def test_set_profile_merges_into_roe_and_audits():
    eng = _eng({"client": "Acme Bank"})
    db = _db(_one(eng))
    await routes.set_profile(eng.id, EngagementProfile(sector="banking", jurisdictions=["IN"]), db, _user())
    assert eng.rules_of_engagement == {"client": "Acme Bank",
                                       "profile": {"sector": "banking", "jurisdictions": ["IN"]}}
    assert [a.action for a in db.added if isinstance(a, AuditLog)] == ["engagement.profile.update"]


@pytest.mark.asyncio
async def test_get_profile_defaults_and_lists_options():
    db = _db(_one(_eng()))
    out = await routes.get_profile(uuid.uuid4(), db, _user())
    assert out["profile"] == {"sector": "generic", "jurisdictions": []}
    assert "banking" in out["options"]["sectors"] and "IN" in out["options"]["jurisdictions"]


@pytest.mark.asyncio
async def test_engagement_compliance_uses_asset_tags_for_swift():
    eng = _eng({"profile": {"sector": "banking", "jurisdictions": ["IN"]}})
    tags = {"v": 1, "auto": [{"key": "compliance_scope", "value": "swift_cscf_scope"}], "manual": []}
    db = _db(_one(eng), _scalars([tags]))
    out = await routes.engagement_compliance(eng.id, db, _user())
    ids = {f["id"] for f in out["frameworks"]}
    assert {"rbi_csf", "certin_2022", "swift_cscf"} <= ids
    assert out["reporting"][0]["deadline_hours"] <= 6


@pytest.mark.asyncio
async def test_finding_obligations_route():
    eng = _eng({"profile": {"sector": "banking", "jurisdictions": ["IN"]}})
    finding = SimpleNamespace(id=uuid.uuid4(), asset_id=uuid.uuid4(), title="SMB signing not required",
                              description="", remediation="", cve_ids=[])
    db = _db(_one(eng), _one(finding), _one({"auto": [{"key": "role", "value": "file_share"}]}))
    out = await routes.finding_obligations_route(eng.id, finding.id, db, _user())
    assert out["category"] == "smb_signing"
    assert out["asset_tags"] == ["role:file_share"]
    assert any(f["framework_id"] == "rbi_csf" for f in out["frameworks"])


@pytest.mark.asyncio
async def test_finding_obligations_404():
    db = _db(_one(_eng()), _one(None))
    with pytest.raises(HTTPException) as exc:
        await routes.finding_obligations_route(uuid.uuid4(), uuid.uuid4(), db, _user())
    assert exc.value.status_code == 404


@pytest.mark.asyncio
async def test_portal_compliance_is_pinned_to_the_clients_engagement():
    from app.routers import portal
    from app.schemas.auth import CurrentUser
    eid = uuid.uuid4()
    user = CurrentUser(user_id=uuid.uuid4(), tenant_id=uuid.uuid4(), role="client", client_engagement_id=eid)
    eng = _eng({"profile": {"sector": "insurance", "jurisdictions": ["IN"]}})
    db = _db(_one(eng), _scalars([]))
    out = await portal.portal_workspace_compliance(user, db)
    assert {f["id"] for f in out["frameworks"]} >= {"irdai_isg", "certin_2022"}
    stmt = db.execute.await_args_list[0].args[0]
    assert eid.hex in str(stmt.compile(compile_kwargs={"literal_binds": True}))

"""Asset tag API: list filter, manual tags (validated + audited), engagement retag."""
from __future__ import annotations

import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import HTTPException
from pydantic import ValidationError

from app.models.asset import Asset
from app.models.audit_log import AuditLog
from app.models.service import Service
from app.routers import asset_tags as routes
from app.routers import engagements as eng
from app.schemas.asset import ManualTagsIn


def _user():
    return SimpleNamespace(tenant_id=uuid.uuid4(), user_id=uuid.uuid4(), role="admin")


def _found():
    return MagicMock(scalar_one_or_none=lambda: SimpleNamespace(id=uuid.uuid4()))


def _scalars(items):
    return MagicMock(scalars=lambda: MagicMock(all=lambda: items),
                     scalar_one_or_none=lambda: items[0] if items else None)


def _asset(ip, tags=None):
    a = Asset(engagement_id=uuid.uuid4(), ip_address=ip, tags=tags)
    a.id = uuid.uuid4()
    return a


def _db(*results):
    db = MagicMock()
    db.execute = AsyncMock(side_effect=list(results))
    db.flush = AsyncMock()
    db.added = []
    db.add = lambda obj: db.added.append(obj)
    return db


@pytest.mark.asyncio
async def test_list_assets_returns_tags_and_filters_by_tag():
    web = _asset("10.0.0.1", {"v": 1, "auto": [{"key": "role", "value": "web"}], "manual": []})
    db_ = _asset("10.0.0.2", {"v": 1, "auto": [{"key": "role", "value": "database"}],
                              "manual": [{"key": "owner_team", "value": "cards"}]})
    db = _db(_found(), _scalars([web, db_]), _scalars([]))

    out = await eng.list_engagement_assets(uuid.uuid4(), db, _user(), tag=["role:database"])

    assert [a["ip_address"] for a in out] == ["10.0.0.2"]
    assert set(out[0]["tag_strings"]) == {"role:database", "owner_team:cards"}
    assert out[0]["tags"]["manual"] == [{"key": "owner_team", "value": "cards"}]


@pytest.mark.asyncio
async def test_list_assets_multiple_tags_are_anded():
    a = _asset("10.0.0.1", {"auto": [{"key": "role", "value": "web"},
                                     {"key": "exposure", "value": "internet_facing"}]})
    b = _asset("10.0.0.2", {"auto": [{"key": "role", "value": "web"}]})
    db = _db(_found(), _scalars([a, b]), _scalars([]))
    out = await eng.list_engagement_assets(uuid.uuid4(), db, _user(),
                                           tag=["role:web", "exposure:internet_facing"])
    assert [x["ip_address"] for x in out] == ["10.0.0.1"]


def test_manual_tag_validation():
    ManualTagsIn(tags=[{"key": "owner_team", "value": "Cards & Payments"}])
    for bad in ({"key": "Bad Key", "value": "x"}, {"key": "k", "value": ""},
                {"key": "k", "value": "x" * 81}):
        with pytest.raises(ValidationError):
            ManualTagsIn(tags=[bad])
    with pytest.raises(ValidationError):
        ManualTagsIn(tags=[{"key": f"k{i}", "value": "v"} for i in range(51)])


@pytest.mark.asyncio
async def test_set_manual_tags_keeps_auto_and_audits():
    asset = _asset("10.0.0.1", {"v": 1, "auto": [{"key": "role", "value": "web"}], "manual": []})
    db = _db(_found(), _scalars([asset]))
    body = ManualTagsIn(tags=[{"key": "owner_team", "value": "cards"},
                              {"key": "owner_team", "value": "cards"}])

    out = await routes.set_manual_tags(uuid.uuid4(), asset.id, body, db, _user())

    assert asset.tags["auto"] == [{"key": "role", "value": "web"}]
    assert asset.tags["manual"] == [{"key": "owner_team", "value": "cards", "source": "manual"}]
    assert "owner_team:cards" in out["tag_strings"]
    audit = [o for o in db.added if isinstance(o, AuditLog)]
    assert audit and audit[0].action == "asset.tags.update"


@pytest.mark.asyncio
async def test_set_manual_tags_404_for_asset_outside_engagement():
    db = _db(_found(), _scalars([]))
    with pytest.raises(HTTPException) as exc:
        await routes.set_manual_tags(uuid.uuid4(), uuid.uuid4(),
                                     ManualTagsIn(tags=[]), db, _user())
    assert exc.value.status_code == 404


@pytest.mark.asyncio
async def test_retag_engagement_recomputes_every_asset_in_two_queries():
    a = _asset("10.0.0.1", {"manual": [{"key": "owner_team", "value": "cards"}]})
    b = _asset("10.0.0.2")
    svc = Service(asset_id=b.id, port=3306, protocol="tcp", service_name="mysql")
    db = _db(_found(), _scalars([a, b]), _scalars([svc]))

    out = await routes.retag_engagement_assets(uuid.uuid4(), db, _user())

    assert out == {"retagged": 2}
    assert a.tags["manual"] == [{"key": "owner_team", "value": "cards"}]
    assert any(t["value"] == "database" for t in b.tags["auto"])
    assert db.execute.await_count == 3  # engagement check + assets + services

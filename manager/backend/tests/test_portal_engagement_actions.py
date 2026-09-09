from __future__ import annotations

import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.models.audit_log import AuditLog
from app.routers import engagements
from app.routers.engagements import EngagementUpdate
from app.routers.portal import (
    patch_portal_workspace_engagement,
    portal_workspace_engagement_assets,
)
from app.schemas.auth import CurrentUser


def _client(engagement_id: uuid.UUID) -> CurrentUser:
    return CurrentUser(
        user_id=uuid.uuid4(),
        tenant_id=uuid.uuid4(),
        role="client",
        client_engagement_id=engagement_id,
    )


@pytest.mark.asyncio
async def test_customer_update_is_pinned_to_live_engagement_and_audited(monkeypatch):
    engagement_id = uuid.uuid4()
    user = _client(engagement_id)
    db = MagicMock()
    db.add = MagicMock()
    db.flush = AsyncMock()
    captured = {}

    async def fake_update_engagement(**kwargs):
        captured["update"] = kwargs
        return SimpleNamespace(id=engagement_id)

    async def fake_get_engagement(**kwargs):
        captured["detail"] = kwargs
        return SimpleNamespace(id=engagement_id, name="Bound engagement")

    monkeypatch.setattr(engagements, "update_engagement", fake_update_engagement)
    monkeypatch.setattr(engagements, "get_engagement", fake_get_engagement)

    result = await patch_portal_workspace_engagement(
        EngagementUpdate(name="Customer-updated name"),
        user,
        db,
    )

    assert result.id == engagement_id
    assert captured["update"]["engagement_id"] == engagement_id
    assert captured["detail"]["engagement_id"] == engagement_id
    assert captured["update"]["current_user"] == user
    audit = next(
        call.args[0] for call in db.add.call_args_list
        if isinstance(call.args[0], AuditLog)
    )
    assert audit.action == "engagement.updated"
    assert audit.engagement_id == engagement_id
    assert audit.detail == {
        "origin": "portal",
        "actor_type": "customer",
        "fields": ["name"],
    }


@pytest.mark.asyncio
async def test_customer_assets_cannot_select_another_engagement(monkeypatch):
    engagement_id = uuid.uuid4()
    user = _client(engagement_id)
    captured = {}

    async def fake_list_engagement_assets(**kwargs):
        captured.update(kwargs)
        return []

    monkeypatch.setattr(
        engagements,
        "list_engagement_assets",
        fake_list_engagement_assets,
    )

    assert await portal_workspace_engagement_assets(user, MagicMock()) == []
    assert captured["engagement_id"] == engagement_id
    assert captured["current_user"] == user

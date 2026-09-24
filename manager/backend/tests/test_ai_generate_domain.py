"""/ai/generate with an engagement: tenant-scoped domain brief."""
from __future__ import annotations

import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import HTTPException

from app.routers import ai as ai_router
from app.schemas.ai import AiGenerateRequest, AiMessage


class _Runtime:
    provider, model, privacy = "anthropic", "claude-sonnet-4-6", "cloud"


def _service(captured):
    async def _gen(request, domain_brief=None):
        captured["brief"] = domain_brief
        return "ok", _Runtime(), False
    svc = MagicMock()
    svc.generate_with_fallback = AsyncMock(side_effect=_gen)
    return svc


def _req(eid=None):
    return AiGenerateRequest(task="advisor", messages=[AiMessage(role="user", content="prioritise")],
                             engagement_id=eid)


def _user():
    return SimpleNamespace(tenant_id=uuid.uuid4(), user_id=uuid.uuid4(), role="admin")


@pytest.mark.asyncio
async def test_without_engagement_no_brief_and_no_db():
    captured: dict = {}
    db = MagicMock(execute=AsyncMock())
    with patch.object(ai_router, "ManagerLlmService", return_value=_service(captured)):
        out = await ai_router.ai_generate(_req(), _user(), db)
    assert captured["brief"] is None and out.skill is None
    db.execute.assert_not_awaited()


@pytest.mark.asyncio
async def test_with_engagement_builds_sector_brief():
    eng = SimpleNamespace(id=uuid.uuid4(), rules_of_engagement={"profile": {"sector": "insurance", "jurisdictions": ["IN"]}})
    db = MagicMock()
    db.execute = AsyncMock(side_effect=[
        MagicMock(scalar_one_or_none=lambda: eng),
        MagicMock(scalars=lambda: MagicMock(all=lambda: [])),
    ])
    captured: dict = {}
    with patch.object(ai_router, "ManagerLlmService", return_value=_service(captured)):
        out = await ai_router.ai_generate(_req(eng.id), _user(), db)
    assert out.skill == "insurance" and out.jurisdictions == ["IN"]
    assert "IRDAI" in captured["brief"]


@pytest.mark.asyncio
async def test_foreign_engagement_is_404():
    db = MagicMock(execute=AsyncMock(return_value=MagicMock(scalar_one_or_none=lambda: None)))
    with patch.object(ai_router, "ManagerLlmService", return_value=_service({})):
        with pytest.raises(HTTPException) as exc:
            await ai_router.ai_generate(_req(uuid.uuid4()), _user(), db)
    assert exc.value.status_code == 404

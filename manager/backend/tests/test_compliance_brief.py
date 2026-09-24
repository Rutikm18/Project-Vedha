"""Finding-level compliance view + LLM compliance brief (operator and portal)."""
from __future__ import annotations

import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.services import compliance_brief as cb
from app.services.llm import AiRuntimeError, _TASK_RULES


class _Runtime:
    provider, model, privacy = "anthropic", "claude-sonnet-4-6", "cloud"


def _finding():
    return SimpleNamespace(id=uuid.uuid4(), engagement_id=uuid.uuid4(), asset_id=uuid.uuid4(),
                           title="SMB signing not required", description="", remediation="Require signing",
                           cve_ids=[], severity=SimpleNamespace(value="medium"), cvss_score=None, risk_score=40,
                           evidence={"banner": "secret-host.corp.local"})


def _eng():
    return SimpleNamespace(id=uuid.uuid4(), rules_of_engagement={"profile": {"sector": "banking", "jurisdictions": ["IN"]}})


def _db(asset_tags=None):
    db = MagicMock()
    db.execute = AsyncMock(side_effect=[
        MagicMock(scalar_one_or_none=lambda: asset_tags),                   # asset tags
        MagicMock(scalars=lambda: MagicMock(all=lambda: [])),               # engagement tag set (brief)
        MagicMock(), MagicMock(scalar_one_or_none=lambda: None),            # audit chain lock + head
    ])
    db.add = MagicMock()
    return db


def test_task_contract_exists_and_forbids_invention():
    rules = _TASK_RULES["compliance_brief"]
    assert "Obligations implicated" in rules and "never invent" in rules.lower()


@pytest.mark.asyncio
async def test_view_is_deterministic():
    out = await cb.finding_compliance_view(_db({"auto": [{"key": "role", "value": "file_share"}]}), _finding(), _eng())
    assert out["category"] == "smb_signing"
    assert {f["framework_id"] for f in out["frameworks"]} >= {"rbi_csf", "certin_2022"}
    assert out["asset_tags"] == ["role:file_share"]


@pytest.mark.asyncio
async def test_brief_grounds_the_model_in_the_obligations_only():
    captured = {}

    async def _gen(request, domain_brief=None):
        captured["request"], captured["brief"] = request, domain_brief
        return "## Why this matters to your regulator\\nRBI Annex 1 §5 and made-up Art. 404.", _Runtime(), False
    svc = MagicMock(audit_records=[])
    svc.generate_with_fallback = AsyncMock(side_effect=_gen)
    with patch.object(cb, "ManagerLlmService", return_value=svc):
        out = await cb.generate_compliance_brief(_db(), _finding(), _eng(), actor_id=uuid.uuid4())
    ctx = captured["request"].context
    assert captured["request"].task == "compliance_brief"
    assert ctx["finding"]["title"] == "SMB signing not required"
    assert "evidence" not in ctx["finding"]                     # raw scan evidence never reaches the model
    assert ctx["obligations"]["frameworks"][0]["controls"]
    assert '<domain_expertise skill="banking">' in captured["brief"]
    assert out["content"].startswith("## Why")
    assert out["unverified_citations"] == ["art. 404"]
    assert out["skill"] == "banking" and out["obligations"]["category"] == "smb_signing"


@pytest.mark.asyncio
async def test_model_failure_still_returns_deterministic_obligations():
    svc = MagicMock(audit_records=[])
    svc.generate_with_fallback = AsyncMock(side_effect=AiRuntimeError("no AI provider is configured", 503))
    with patch.object(cb, "ManagerLlmService", return_value=svc):
        out = await cb.generate_compliance_brief(_db(), _finding(), _eng(), actor_id=uuid.uuid4())
    assert out["content"] is None and "no AI provider" in out["error"]
    assert out["obligations"]["frameworks"]


@pytest.mark.asyncio
async def test_operator_route_is_tenant_scoped():
    from fastapi import HTTPException
    from app.routers import compliance as routes
    db = MagicMock(execute=AsyncMock(return_value=MagicMock(one_or_none=lambda: None)))
    with pytest.raises(HTTPException) as exc:
        await routes.finding_obligations_by_id(uuid.uuid4(), db, SimpleNamespace(tenant_id=uuid.uuid4(), user_id=uuid.uuid4()))
    assert exc.value.status_code == 404

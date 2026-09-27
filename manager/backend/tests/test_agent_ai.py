from __future__ import annotations

import json
import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest
from fastapi import HTTPException

from app.ai.agent import (
    _CONTEXT_CHAR_LIMIT,
    AgentDecisionEngine,
    AgentUnavailableError,
    _build_bounded_context,
    _parse_submission,
)
from app.config import Settings
from app.models.agent_recommendation import STATUS_PENDING
from app.routers import agent_advisor
from app.services.llm import ManagerLlmService


def _settings(provider: str) -> Settings:
    base = dict(
        llm_provider=provider,
        openai_api_key="",
        anthropic_api_key="",
        openrouter_api_key="",
        openai_base_url="https://openai.test/v1",
        openrouter_base_url="https://openrouter.test/api/v1",
        ollama_base_url="https://ollama.test",
    )
    if provider == "openai":
        base.update(openai_api_key="openai-secret", openai_model="gpt-agent")
    elif provider == "openrouter":
        base.update(
            openrouter_api_key="openrouter-secret",
            openrouter_model="vendor/agent:free",
        )
    else:
        base.update(ollama_model="qwen-agent:latest")
    return Settings(**base)


def _mock_db():
    db = MagicMock()
    db.add = MagicMock()
    db.flush = AsyncMock()
    return db


def _ground_engine(engine: AgentDecisionEngine, finding_id: uuid.UUID) -> None:
    engine._overview = AsyncMock(return_value={
        "findings_by_severity": {"high": 1},
        "total_findings": 1,
        "asset_count": 0,
        "service_count": 0,
        "attack_path_count": 0,
    })
    engine._list_findings = AsyncMock(return_value={
        "count": 1,
        "findings": [{
            "id": str(finding_id),
            "title": "Outdated TLS",
            "severity": "high",
            "cvss": 8.1,
            "status": "open",
            "cve_ids": [],
            "exploitable": False,
        }],
    })
    engine._list_attack_paths = AsyncMock(return_value={"count": 0, "attack_paths": []})
    engine._list_assets = AsyncMock(return_value={"count": 0, "assets": []})


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("provider", "expected_model"),
    [
        ("openai", "gpt-agent"),
        ("openrouter", "vendor/agent:free"),
        ("ollama", "qwen-agent:latest"),
    ],
)
async def test_default_advisor_uses_manager_provider_and_persists_pending(
    provider, expected_model,
):
    finding_id = uuid.uuid4()
    output = json.dumps({
        "recommendations": [{
            "category": "next_action",
            "title": "Recheck the finding",
            "rationale": "The high-severity finding remains open.",
            "target_type": "finding",
            "target_id": str(finding_id),
            "action": "recheck_finding",
            "confidence": 88,
            "priority": "high",
        }],
    })
    calls: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request.url.path)
        if request.url.path == "/api/tags":
            return httpx.Response(200, json={"models": [{"name": expected_model}]})
        body = json.loads(request.content)
        assert "recommend-only security advisor" in body["messages"][0]["content"]
        assert str(finding_id) in body["messages"][0]["content"]
        if provider == "ollama":
            assert body["format"] == "json"
            return httpx.Response(200, json={"message": {"content": output}})
        assert body["response_format"] == {"type": "json_object"}
        return httpx.Response(
            200,
            json={"choices": [{"message": {"content": output}}]},
        )

    settings = _settings(provider)
    service = ManagerLlmService(settings, transport=httpx.MockTransport(handler))
    db = _mock_db()
    engine = AgentDecisionEngine(db, llm_service=service)
    _ground_engine(engine, finding_id)

    result = await engine.run(uuid.uuid4())

    assert engine.available is True
    assert result["recommendations_stored"] == 1
    row = db.add.call_args.args[0]
    assert row.status == STATUS_PENDING
    assert row.model == expected_model
    assert row.target_id == finding_id
    assert row.action == "recheck_finding"
    db.flush.assert_awaited_once()
    if provider == "ollama":
        assert calls == ["/api/tags", "/api/chat"]
    else:
        assert len(calls) == 1


@pytest.mark.asyncio
async def test_advisor_drops_target_not_present_in_grounding_context():
    grounded_id = uuid.uuid4()
    invented_id = uuid.uuid4()
    output = json.dumps({
        "recommendations": [{
            "category": "triage",
            "title": "Review a finding",
            "rationale": "Requires analyst review.",
            "target_type": "finding",
            "target_id": str(invented_id),
            "action": None,
            "confidence": 50,
            "priority": "medium",
        }],
    })

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={"choices": [{"message": {"content": output}}]},
        )

    settings = _settings("openai")
    service = ManagerLlmService(settings, transport=httpx.MockTransport(handler))
    db = _mock_db()
    engine = AgentDecisionEngine(db, llm_service=service)
    _ground_engine(engine, grounded_id)

    result = await engine.run(uuid.uuid4())

    assert result["recommendations_stored"] == 0
    db.add.assert_not_called()
    db.flush.assert_not_awaited()


def test_advisor_schema_rejects_non_allowlisted_action():
    text = json.dumps({
        "recommendations": [{
            "category": "next_action",
            "title": "Unsafe proposal",
            "rationale": "Not allowlisted.",
            "action": "run_arbitrary_shell",
        }],
    })

    with pytest.raises(AgentUnavailableError, match="no valid recommendations"):
        _parse_submission(text)


def test_advisor_context_is_bounded_and_reports_omissions():
    engagement_id = uuid.uuid4()
    findings = [{
        "id": str(uuid.uuid4()),
        "title": "x" * 2_000,
        "severity": "high",
        "status": "open",
        "cve_ids": [f"CVE-2099-{index:04d}" for index in range(50)],
    } for _ in range(200)]
    assets = [{
        "id": str(uuid.uuid4()),
        "hostname": "h" * 1_000,
        "services": [{
            "port": port,
            "proto": "tcp",
            "product": "p" * 1_000,
            "version": "v" * 1_000,
        } for port in range(30)],
    } for _ in range(100)]

    context = _build_bounded_context(
        engagement_id,
        overview={
            "total_findings": 200,
            "asset_count": 100,
            "attack_path_count": 0,
            "service_count": 3_000,
            "findings_by_severity": {"high": 200},
        },
        findings={"count": 200, "findings": findings},
        attack_paths={"count": 0, "attack_paths": []},
        assets={"count": 100, "assets": assets},
    )

    encoded = json.dumps(context, separators=(",", ":"))
    assert len(encoded) <= _CONTEXT_CHAR_LIMIT
    assert context["coverage"]["omitted"]["findings"] > 0
    assert context["coverage"]["omitted"]["assets"] > 0


@pytest.mark.asyncio
async def test_injected_anthropic_client_keeps_tool_loop_compatibility():
    read_tool = SimpleNamespace(
        type="tool_use",
        id="tool-1",
        name="get_engagement_overview",
        input={},
    )
    submit_tool = SimpleNamespace(
        type="tool_use",
        id="tool-2",
        name="submit_recommendations",
        input={"recommendations": []},
    )
    client = MagicMock()
    client.messages = MagicMock()
    client.messages.create = AsyncMock(side_effect=[
        SimpleNamespace(stop_reason="tool_use", content=[read_tool]),
        SimpleNamespace(stop_reason="tool_use", content=[submit_tool]),
    ])
    engine = AgentDecisionEngine(_mock_db(), client=client)
    engine._exec_read_tool = AsyncMock(return_value={"total_findings": 0})
    engine._persist = AsyncMock(return_value=0)

    result = await engine.run(uuid.uuid4())

    assert result["recommendations_stored"] == 0
    assert client.messages.create.await_count == 2
    engine._exec_read_tool.assert_awaited_once()
    engine._persist.assert_awaited_once()


@pytest.mark.asyncio
async def test_advisor_route_uses_provider_agnostic_unavailable_copy(monkeypatch):
    class UnavailableEngine:
        available = False

        def __init__(self, db):
            pass

    monkeypatch.setattr(agent_advisor, "AgentDecisionEngine", UnavailableEngine)
    monkeypatch.setattr(agent_advisor, "get_or_404", AsyncMock())

    with pytest.raises(HTTPException) as exc_info:
        await agent_advisor.run_advisor(
            uuid.uuid4(),
            MagicMock(),
            SimpleNamespace(tenant_id=uuid.uuid4()),
        )

    assert exc_info.value.status_code == 503
    assert "Manager AI provider" in exc_info.value.detail
    assert "ANTHROPIC" not in exc_info.value.detail

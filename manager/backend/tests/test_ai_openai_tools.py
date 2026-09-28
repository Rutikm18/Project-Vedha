"""OpenAI tool-calling client with the Anthropic SDK's shape, and agent failover."""
from __future__ import annotations

import json
from types import SimpleNamespace
from unittest.mock import MagicMock

import anthropic
import httpx
import pytest

from app.ai.agent import AgentDecisionEngine, AgentUnavailableError
from app.ai.health import ProviderHealth
from app.ai.openai_tools import (
    OpenAiToolClient,
    from_openai_response,
    to_openai_messages,
    to_openai_tool,
)
from app.services.llm_http_client import AsyncLlmHttpClient
from tests.test_ai_chain import settings

TOOL = {"name": "list_findings", "description": "List findings",
        "input_schema": {"type": "object", "properties": {"limit": {"type": "integer"}}}}

# An agent history exactly as AgentDecisionEngine builds it: SDK block objects for
# the assistant turn, plain dicts for tool results.
HISTORY = [
    {"role": "user", "content": "Review this engagement."},
    {"role": "assistant", "content": [
        SimpleNamespace(type="text", text="Let me look."),
        SimpleNamespace(type="tool_use", id="call_1", name="list_findings", input={"limit": 5}),
    ]},
    {"role": "user", "content": [
        {"type": "tool_result", "tool_use_id": "call_1", "content": '{"count": 2}'},
    ]},
]


def test_tool_definition_translation():
    assert to_openai_tool(TOOL) == {"type": "function", "function": {
        "name": "list_findings", "description": "List findings",
        "parameters": TOOL["input_schema"]}}


def test_history_translation_keeps_tool_call_pairing():
    system = [{"type": "text", "text": "You are the advisor.", "cache_control": {"type": "ephemeral"}}]
    out = to_openai_messages(system, HISTORY)
    assert out[0] == {"role": "system", "content": "You are the advisor."}
    assert out[1] == {"role": "user", "content": "Review this engagement."}
    assert out[2]["role"] == "assistant" and out[2]["content"] == "Let me look."
    call = out[2]["tool_calls"][0]
    assert (call["id"], call["function"]["name"]) == ("call_1", "list_findings")
    assert json.loads(call["function"]["arguments"]) == {"limit": 5}
    assert out[3] == {"role": "tool", "tool_call_id": "call_1", "content": '{"count": 2}'}


def test_response_translation():
    data = {"choices": [{"finish_reason": "tool_calls", "message": {
        "content": None,
        "tool_calls": [{"id": "c9", "type": "function",
                        "function": {"name": "submit_recommendations", "arguments": '{"recommendations": []}'}}],
    }}]}
    resp = from_openai_response(data)
    assert resp.stop_reason == "tool_use"
    block = resp.content[0]
    assert (block.type, block.id, block.name, block.input) == ("tool_use", "c9", "submit_recommendations",
                                                               {"recommendations": []})
    final = from_openai_response({"choices": [{"finish_reason": "stop", "message": {"content": "done"}}]})
    assert (final.stop_reason, final.content[0].text) == ("end_turn", "done")


@pytest.mark.asyncio
async def test_client_posts_translated_body():
    seen: dict = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["url"] = str(request.url)
        seen["body"] = json.loads(request.content)
        return httpx.Response(200, json={"choices": [{"finish_reason": "stop", "message": {"content": "ok"}}]})

    client = OpenAiToolClient(settings(openai_api_key="o", openai_model="gpt-x"),
                              http=AsyncLlmHttpClient(timeout_seconds=5, transport=httpx.MockTransport(handler)))
    resp = await client.messages.create(model="gpt-x", max_tokens=100, system="sys",
                                        tools=[TOOL], messages=HISTORY, output_config={"effort": "low"})
    assert resp.content[0].text == "ok"
    assert seen["url"] == "https://api.openai.com/v1/chat/completions"
    assert seen["body"]["model"] == "gpt-x"
    assert seen["body"]["tools"][0]["function"]["name"] == "list_findings"
    assert "output_config" not in seen["body"]


class _Failing:
    def __init__(self):
        request = httpx.Request("POST", "https://api.anthropic.com/v1/messages")
        self.error = anthropic.RateLimitError(
            "rate limited", response=httpx.Response(429, request=request), body=None)
        self.messages = SimpleNamespace(create=self._create)

    async def _create(self, **kwargs):
        raise self.error


class _Answering:
    def __init__(self, text: str):
        self.kwargs: dict = {}
        self.messages = SimpleNamespace(create=self._create)
        self._text = text

    async def _create(self, **kwargs):
        self.kwargs = kwargs
        return SimpleNamespace(stop_reason="end_turn", content=[SimpleNamespace(type="text", text=self._text)])


@pytest.mark.asyncio
async def test_agent_fails_over_from_anthropic_to_openai():
    openai = _Answering("from openai")
    engine = AgentDecisionEngine(MagicMock(), clients=[
        ("anthropic", _Failing(), "claude-sonnet-4-6"), ("openai", openai, "gpt-x")])
    resp = await engine._create([{"role": "user", "content": "go"}])
    assert resp.content[0].text == "from openai"
    assert openai.kwargs["model"] == "gpt-x"
    assert "output_config" not in openai.kwargs       # Anthropic-only parameter
    assert engine._model == "gpt-x"
    state = await ProviderHealth().state("anthropic")
    assert (state.state, state.reason) == ("cooling", "rate_limit")


@pytest.mark.asyncio
async def test_agent_raises_when_no_provider_can_serve():
    engine = AgentDecisionEngine(MagicMock(), clients=[("anthropic", _Failing(), "claude-sonnet-4-6")])
    with pytest.raises(AgentUnavailableError):
        await engine._create([{"role": "user", "content": "go"}])


def test_agent_builds_openai_fallback_from_settings(monkeypatch):
    cfg = settings(anthropic_api_key="a", openai_api_key="o")
    monkeypatch.setattr("app.ai.agent.get_settings", lambda: cfg)
    engine = AgentDecisionEngine(MagicMock())
    assert [name for name, _, _ in engine._clients] == ["anthropic", "openai"]
    only_openai = settings(openai_api_key="o")
    monkeypatch.setattr("app.ai.agent.get_settings", lambda: only_openai)
    assert AgentDecisionEngine(MagicMock()).available is True

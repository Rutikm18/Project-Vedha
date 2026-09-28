"""The automatic provider chain: provider adapters, tiers, masking, walker."""
from __future__ import annotations

import json

import httpx
import pytest

from app.config import Settings
from app.schemas.ai import AiGenerateRequest
from app.services.llm import AiRuntimeError, ManagerLlmService

_NO_KEYS = dict(llm_provider="", llm_chain="", openai_api_key="", anthropic_api_key="",
                gemini_api_key="", groq_api_key="", openrouter_api_key="")


def settings(**overrides) -> Settings:
    base = dict(_NO_KEYS)
    base.update(overrides)
    return Settings(**base)


def ask(task: str = "advisor", content: str = "Prioritise remediation", **kw) -> AiGenerateRequest:
    return AiGenerateRequest(task=task, messages=[{"role": "user", "content": content}], **kw)


def openai_reply(text: str) -> httpx.Response:
    return httpx.Response(200, json={"choices": [{"message": {"content": text}}]})


# ── Groq ─────────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_groq_generation_is_server_side():
    seen: dict = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["url"] = str(request.url)
        seen["auth"] = request.headers["authorization"]
        seen["body"] = json.loads(request.content)
        return openai_reply("Groq answer")

    svc = ManagerLlmService(settings(groq_api_key="gsk-test", groq_model="openai/gpt-oss-120b"),
                            transport=httpx.MockTransport(handler))
    content, runtime = await svc.generate(ask(provider="groq"))

    assert content == "Groq answer"
    assert seen["url"] == "https://api.groq.com/openai/v1/chat/completions"
    assert seen["auth"] == "Bearer gsk-test"
    assert seen["body"]["model"] == "openai/gpt-oss-120b"
    assert (runtime.provider, runtime.privacy) == ("groq", "cloud")


@pytest.mark.asyncio
async def test_groq_unconfigured_is_503():
    with pytest.raises(AiRuntimeError, match="not configured") as exc:
        await ManagerLlmService(settings()).generate(ask(provider="groq"))
    assert exc.value.status_code == 503


@pytest.mark.asyncio
async def test_status_lists_groq():
    status = await ManagerLlmService(settings(groq_api_key="g")).status()
    groq = next(p for p in status.providers if p.id == "groq")
    assert groq.configured is True


# ── Free tiers are always pseudonymized ─────────────────────────────────────

def _gemini_capture(seen: dict):
    def handler(request: httpx.Request) -> httpx.Response:
        seen["body"] = request.content.decode()
        return httpx.Response(200, json={"candidates": [{"content": {"parts": [{"text": "Isolate [IP-1] now"}]}}]})
    return handler


@pytest.mark.asyncio
async def test_free_gemini_is_pseudonymized_even_under_cloud_profile():
    seen: dict = {}
    svc = ManagerLlmService(settings(gemini_api_key="g", deployment_profile="cloud"),
                            transport=httpx.MockTransport(_gemini_capture(seen)))
    content, runtime = await svc.generate(ask(provider="gemini", content="Is 10.9.8.7 exposed?"))
    assert "10.9.8.7" not in seen["body"]
    assert "[IP-1]" in seen["body"]
    assert content == "Isolate 10.9.8.7 now"          # rehydrated for the reader
    assert runtime.tier == "free"


@pytest.mark.asyncio
async def test_paid_gemini_is_sent_raw_under_cloud_profile():
    seen: dict = {}
    svc = ManagerLlmService(settings(gemini_api_key="g", gemini_paid=True),
                            transport=httpx.MockTransport(_gemini_capture(seen)))
    _, runtime = await svc.generate(ask(provider="gemini", content="Is 10.9.8.7 exposed?"))
    assert "10.9.8.7" in seen["body"]
    assert runtime.tier == "budget"


@pytest.mark.asyncio
async def test_premium_is_sent_raw_under_cloud_profile():
    seen: dict = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["body"] = request.content.decode()
        return httpx.Response(200, json={"content": [{"type": "text", "text": "ok"}]})

    svc = ManagerLlmService(settings(anthropic_api_key="a"), transport=httpx.MockTransport(handler))
    _, runtime = await svc.generate(ask(provider="anthropic", content="Is 10.9.8.7 exposed?"))
    assert "10.9.8.7" in seen["body"]
    assert runtime.tier == "premium"

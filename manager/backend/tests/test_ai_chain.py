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

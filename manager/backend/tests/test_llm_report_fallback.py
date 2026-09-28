"""The report generator's Anthropic-SDK path falls back through the chain."""
from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import MagicMock

import anthropic
import httpx
import pytest

from app.ai.failures import classify_http
from app.ai.health import ProviderHealth
from app.ai.llm_report import LLMReportGenerator, LLMUnavailableError
from app.services.llm import AiRuntimeError, ManagerLlmService
from tests.test_ai_chain import PREMIUM_AND_FREE, Router, settings


def _rate_limit_error() -> anthropic.RateLimitError:
    request = httpx.Request("POST", "https://api.anthropic.com/v1/messages")
    response = httpx.Response(429, request=request, headers={"retry-after": "20"})
    return anthropic.RateLimitError("rate limited", response=response, body=None)


class _SdkClient:
    def __init__(self, *, error: Exception | None = None, text: str = "sdk text"):
        self.calls = 0
        self._error, self._text = error, text
        self.messages = SimpleNamespace(create=self._create)

    async def _create(self, **kwargs):
        self.calls += 1
        if self._error is not None:
            raise self._error
        return SimpleNamespace(stop_reason="end_turn",
                               content=[SimpleNamespace(type="text", text=self._text)])


@pytest.fixture
def chain_settings(monkeypatch):
    cfg = settings(**PREMIUM_AND_FREE)
    monkeypatch.setattr("app.ai.llm_report.get_settings", lambda: cfg)
    monkeypatch.setattr("app.services.llm.get_settings", lambda: cfg)
    return cfg


@pytest.fixture
def fake_chain(monkeypatch):
    seen: dict = {}

    async def complete_raw(self, **kwargs):
        seen.update(kwargs)
        return "chain text", SimpleNamespace(provider="openai", model="gpt"), True

    monkeypatch.setattr(ManagerLlmService, "complete_raw", complete_raw)
    return seen


@pytest.mark.asyncio
async def test_complete_raw_excludes_anthropic_and_serves_next_tier():
    router = Router()
    svc = ManagerLlmService(settings(**PREMIUM_AND_FREE), transport=router.transport())
    text, runtime, fallback = await svc.complete_raw(
        task="report", system="You write reports.", messages=[{"role": "user", "content": "go"}],
        max_tokens=500, exclude={"anthropic"})
    assert (text, runtime.provider, fallback) == ("openai answer", "openai", False)
    assert router.calls == ["openai"]        # report floor: gemini (free) is never used
    assert svc.audit_records and svc.audit_records[0]["task"] == "report"


@pytest.mark.asyncio
async def test_rate_limited_sdk_falls_back_and_cools_anthropic(chain_settings, fake_chain):
    client = _SdkClient(error=_rate_limit_error())
    gen = LLMReportGenerator(MagicMock(), client=client)
    assert await gen._complete("write the summary") == "chain text"
    assert client.calls == 1                          # 429 is not retried locally
    assert fake_chain["exclude"] == {"anthropic"} and fake_chain["task"] == "report"
    state = await ProviderHealth().state("anthropic")
    assert (state.state, state.reason) == ("cooling", "rate_limit")


@pytest.mark.asyncio
async def test_cooling_anthropic_is_not_called(chain_settings, fake_chain):
    await ProviderHealth().record_failure("anthropic", classify_http(429, "rate_limit"))
    client = _SdkClient()
    gen = LLMReportGenerator(MagicMock(), client=client)
    assert await gen._complete("write") == "chain text"
    assert client.calls == 0


@pytest.mark.asyncio
async def test_healthy_sdk_path_is_unchanged(chain_settings, fake_chain):
    gen = LLMReportGenerator(MagicMock(), client=_SdkClient(text="from claude"))
    assert await gen._complete("write") == "from claude"
    assert fake_chain == {}


@pytest.mark.asyncio
async def test_chain_failure_reports_both_causes(chain_settings, monkeypatch):
    async def complete_raw(self, **kwargs):
        raise AiRuntimeError("openai is temporarily unavailable (billing)", 503)

    monkeypatch.setattr(ManagerLlmService, "complete_raw", complete_raw)
    gen = LLMReportGenerator(MagicMock(), client=_SdkClient(error=_rate_limit_error()))
    with pytest.raises(LLMUnavailableError) as exc:
        await gen._complete("write")
    assert "rate" in str(exc.value).lower() and "billing" in str(exc.value)


def test_available_without_anthropic_when_chain_has_a_premium_provider(monkeypatch):
    cfg = settings(openai_api_key="o")
    monkeypatch.setattr("app.ai.llm_report.get_settings", lambda: cfg)
    assert LLMReportGenerator(MagicMock()).available is True
    empty = settings()
    monkeypatch.setattr("app.ai.llm_report.get_settings", lambda: empty)
    assert LLMReportGenerator(MagicMock()).available is False

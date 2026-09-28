from __future__ import annotations

import httpx
import pytest

from app.ai.kv import MemoryKv
from app.ai.spend import SpendMeter, parse_caps, parse_prices, usage_tokens
from app.services.llm import ManagerLlmService
from tests.test_ai_chain import PREMIUM_AND_FREE, Router, ask, settings


def test_usage_tokens_per_provider_shape():
    anthropic = {"usage": {"input_tokens": 1000, "output_tokens": 200,
                           "cache_creation_input_tokens": 400, "cache_read_input_tokens": 1000}}
    assert usage_tokens("anthropic", anthropic) == (1000 + 400 * 1.25 + 1000 * 0.1, 200)
    assert usage_tokens("openai", {"usage": {"prompt_tokens": 10, "completion_tokens": 5}}) == (10, 5)
    assert usage_tokens("groq", {"usage": {"prompt_tokens": 1, "completion_tokens": 2}}) == (1, 2)
    gemini = {"usageMetadata": {"promptTokenCount": 7, "candidatesTokenCount": 3}}
    assert usage_tokens("gemini", gemini) == (7, 3)
    assert usage_tokens("ollama", {"prompt_eval_count": 4, "eval_count": 6}) == (4, 6)
    assert usage_tokens("openai", {"choices": []}) is None
    assert usage_tokens("openai", None) is None


def test_parse_prices_and_caps():
    assert parse_prices("gpt-4.1=2:8, bad, x=1") == {"gpt-4.1": (2.0, 8.0)}
    assert parse_caps("anthropic=20, openai=7.5, junk=x") == {"anthropic": 20.0, "openai": 7.5}


@pytest.mark.asyncio
async def test_sonnet_cost_and_daily_cap():
    meter = SpendMeter(MemoryKv(), settings(ai_daily_cap_usd="anthropic=20"))
    one_million_each = {"usage": {"input_tokens": 1_000_000, "output_tokens": 1_000_000}}
    assert await meter.record("anthropic", "claude-sonnet-4-6", one_million_each) == 18.0
    assert await meter.today("anthropic") == 18.0
    assert await meter.over_cap("anthropic") is False
    await meter.record("anthropic", "claude-sonnet-4-6", one_million_each)
    assert await meter.over_cap("anthropic") is True
    assert await meter.over_cap("openai") is False            # no cap configured


@pytest.mark.asyncio
async def test_unknown_price_records_nothing():
    meter = SpendMeter(MemoryKv(), settings())
    body = {"usage": {"prompt_tokens": 10, "completion_tokens": 5}}
    assert await meter.record("openai", "some-new-model", body) == 0.0
    assert await meter.today("openai") == 0.0


@pytest.mark.asyncio
async def test_walker_skips_a_provider_over_its_daily_cap():
    kv = MemoryKv()
    capped = settings(**PREMIUM_AND_FREE, ai_daily_cap_usd="anthropic=1")
    await SpendMeter(kv, capped).record(
        "anthropic", "claude-sonnet-4-6", {"usage": {"input_tokens": 1_000_000, "output_tokens": 0}})
    router = Router()
    svc = ManagerLlmService(capped, transport=router.transport(), kv=kv)
    _, runtime, fallback = await svc.generate_with_fallback(ask())
    assert (runtime.provider, fallback) == ("openai", True)
    assert router.calls == ["openai"]


@pytest.mark.asyncio
async def test_walker_records_spend_after_success():
    kv = MemoryKv()
    router = Router(anthropic=lambda r: httpx.Response(200, json={
        "content": [{"type": "text", "text": "ok"}],
        "usage": {"input_tokens": 1_000_000, "output_tokens": 0}}))
    svc = ManagerLlmService(settings(**PREMIUM_AND_FREE), transport=router.transport(), kv=kv)
    await svc.generate_with_fallback(ask())
    assert await svc.spend.today("anthropic") == 3.0

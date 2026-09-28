from __future__ import annotations

import pytest

from app.ai.answer_store import AnswerStore, StoredAnswer
from app.ai.failures import classify_http
from app.ai.health import ProviderHealth
from app.ai.kv import MemoryKv
from app.services.llm import ManagerLlmService
from tests.test_ai_chain import PREMIUM_AND_FREE, Router, ask, settings

CTX = {"finding": {"title": "SMB signing not required", "host": "10.1.1.5"}}


def _svc(router, kv, **extra):
    return ManagerLlmService(settings(**PREMIUM_AND_FREE, **extra), transport=router.transport(), kv=kv)


@pytest.mark.asyncio
async def test_identical_brief_is_served_without_egress():
    kv, router = MemoryKv(), Router()
    first = await _svc(router, kv).generate_with_fallback(ask("security_brief", context=CTX))
    second = await _svc(router, kv).generate_with_fallback(ask("security_brief", context=CTX))
    assert router.calls == ["anthropic"]
    assert second[0] == first[0] == "anthropic answer"
    assert second[1].provider == "anthropic" and second[2] is False


@pytest.mark.asyncio
async def test_different_context_is_a_miss():
    kv, router = MemoryKv(), Router()
    await _svc(router, kv).generate_with_fallback(ask("security_brief", context=CTX))
    other = {"finding": {"title": "SMB signing not required", "host": "10.1.1.6"}}
    await _svc(router, kv).generate_with_fallback(ask("security_brief", context=other))
    assert router.calls == ["anthropic", "anthropic"]


@pytest.mark.asyncio
async def test_chat_tasks_are_never_stored():
    kv, router = MemoryKv(), Router()
    await _svc(router, kv).generate_with_fallback(ask("advisor", context=CTX))
    await _svc(router, kv).generate_with_fallback(ask("advisor", context=CTX))
    assert router.calls == ["anthropic", "anthropic"]


@pytest.mark.asyncio
async def test_fallback_answer_is_upgraded_once_premium_is_healthy_again():
    kv = MemoryKv()
    health = ProviderHealth(kv)
    rate_limited = classify_http(429, "rate_limit", retry_after=60)
    await health.record_failure("anthropic", rate_limited)
    await health.record_failure("openai", rate_limited)
    router = Router()
    served = await _svc(router, kv, gemini_paid=True).generate_with_fallback(
        ask("security_brief", context=CTX))
    assert served[1].provider == "gemini"

    # While premium is still cooling the stored budget answer is reused ...
    await _svc(router, kv, gemini_paid=True).generate_with_fallback(ask("security_brief", context=CTX))
    assert router.calls == ["gemini"]

    # ... and once premium heals, the next read regenerates with premium.
    await kv.delete("ai:cool:anthropic", "ai:strikes:anthropic")
    upgraded = await _svc(router, kv, gemini_paid=True).generate_with_fallback(
        ask("security_brief", context=CTX))
    assert upgraded[1].provider == "anthropic"


@pytest.mark.asyncio
async def test_zero_ttl_disables_the_store():
    kv, router = MemoryKv(), Router()
    await _svc(router, kv, ai_answer_cache_ttl_seconds=0).generate_with_fallback(ask("security_brief", context=CTX))
    await _svc(router, kv, ai_answer_cache_ttl_seconds=0).generate_with_fallback(ask("security_brief", context=CTX))
    assert router.calls == ["anthropic", "anthropic"]


@pytest.mark.asyncio
async def test_store_round_trip_and_key_stability():
    store = AnswerStore(MemoryKv(), ttl_s=60)
    key = AnswerStore.key("security_brief", "sys", [{"role": "user", "content": "q"}], "budget")
    assert key == AnswerStore.key("security_brief", "sys", [{"role": "user", "content": "q"}], "budget")
    assert key != AnswerStore.key("security_brief", "sys2", [{"role": "user", "content": "q"}], "budget")
    answer = StoredAnswer("t", "anthropic", "claude-sonnet-4-6", "cloud", "premium")
    await store.put(key, answer)
    assert await store.get(key) == answer

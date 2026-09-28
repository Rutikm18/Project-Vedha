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


# ── The walker ──────────────────────────────────────────────────────────────

import asyncio  # noqa: E402

from app.ai.health import ProviderHealth  # noqa: E402
from app.ai.kv import MemoryKv  # noqa: E402
from app.ai.routing import FREE, TaskPolicy  # noqa: E402

_HOSTS = {"api.anthropic.com": "anthropic", "api.openai.com": "openai",
          "generativelanguage.googleapis.com": "gemini", "api.groq.com": "groq"}
_OK = {
    "anthropic": lambda text: httpx.Response(200, json={"content": [{"type": "text", "text": text}]}),
    "openai": openai_reply,
    "groq": openai_reply,
    "gemini": lambda text: httpx.Response(200, json={"candidates": [{"content": {"parts": [{"text": text}]}}]}),
}


class Router:
    """MockTransport that answers per provider and counts calls."""

    def __init__(self, **responses):
        self.responses = responses       # provider -> Response | callable(request) | async callable
        self.calls: list[str] = []

    async def __call__(self, request: httpx.Request) -> httpx.Response:
        provider = _HOSTS[request.url.host]
        self.calls.append(provider)
        answer = self.responses.get(provider, f"{provider} answer")
        if isinstance(answer, str):
            return _OK[provider](answer)
        if callable(answer):
            result = answer(request)
            return await result if asyncio.iscoroutine(result) else result
        return answer

    def transport(self) -> httpx.MockTransport:
        return httpx.MockTransport(self)


PREMIUM_AND_FREE = dict(anthropic_api_key="a", openai_api_key="o", gemini_api_key="g")


def _err(status: int, message: str, **headers) -> httpx.Response:
    return httpx.Response(status, headers=headers, json={"error": {"message": message}})


@pytest.mark.asyncio
async def test_premium_first_serves_from_anthropic():
    router = Router()
    svc = ManagerLlmService(settings(**PREMIUM_AND_FREE), transport=router.transport())
    text, runtime, fallback = await svc.generate_with_fallback(ask())
    assert (text, runtime.provider, fallback) == ("anthropic answer", "anthropic", False)
    assert router.calls == ["anthropic"]


@pytest.mark.asyncio
async def test_rate_limit_falls_to_openai_and_cools_anthropic():
    kv = MemoryKv()
    router = Router(anthropic=_err(429, "rate_limit_error", **{"retry-after": "30"}))
    svc = ManagerLlmService(settings(**PREMIUM_AND_FREE), transport=router.transport(), kv=kv)
    text, runtime, fallback = await svc.generate_with_fallback(ask())
    assert (runtime.provider, fallback) == ("openai", True)
    state = await ProviderHealth(kv).state("anthropic")
    assert (state.state, state.reason, round(state.retry_in_s)) == ("cooling", "rate_limit", 30)

    # A second service instance (another request / worker) never calls anthropic.
    router.calls.clear()
    other = ManagerLlmService(settings(**PREMIUM_AND_FREE), transport=router.transport(), kv=kv)
    _, runtime, fallback = await other.generate_with_fallback(ask())
    assert router.calls == ["openai"]
    assert (runtime.provider, fallback) == ("openai", True)


@pytest.mark.asyncio
async def test_spend_cap_blocks_anthropic():
    kv = MemoryKv()
    router = Router(anthropic=_err(429, "You have reached your specified API usage limits."))
    svc = ManagerLlmService(settings(**PREMIUM_AND_FREE), transport=router.transport(), kv=kv)
    await svc.generate_with_fallback(ask())
    state = await ProviderHealth(kv).state("anthropic")
    assert (state.state, state.reason) == ("blocked", "spend_cap")


@pytest.mark.asyncio
async def test_floor_relaxes_when_only_free_models_are_configured():
    router = Router()
    svc = ManagerLlmService(settings(gemini_api_key="g"), transport=router.transport())
    _, runtime, _ = await svc.generate_with_fallback(ask("compliance_brief"))
    assert runtime.provider == "gemini"


@pytest.mark.asyncio
async def test_unusable_json_moves_to_next_tier_without_cooling_the_provider():
    kv = MemoryKv()
    router = Router(anthropic="Sure! Here is some prose, not JSON.", openai='{"whatIs": "x"}')
    svc = ManagerLlmService(settings(**PREMIUM_AND_FREE), transport=router.transport(), kv=kv)
    text, runtime, _ = await svc.generate_with_fallback(ask("advisor_flow"))
    assert runtime.provider == "openai" and text == '{"whatIs": "x"}'
    assert (await ProviderHealth(kv).state("anthropic")).state == "healthy"


@pytest.mark.asyncio
async def test_hung_provider_leaves_time_for_the_next_tier(monkeypatch):
    monkeypatch.setattr("app.services.llm.task_policy", lambda task: TaskPolicy(FREE, 1.0))
    monkeypatch.setattr("app.ai.routing.MIN_ATTEMPT_S", 0.2)

    async def hang(request):
        await asyncio.sleep(5)
        return _OK["anthropic"]("too late")

    kv = MemoryKv()
    router = Router(anthropic=hang)
    svc = ManagerLlmService(settings(**PREMIUM_AND_FREE), transport=router.transport(), kv=kv)
    _, runtime, _ = await svc.generate_with_fallback(ask())
    assert runtime.provider == "openai"
    state = await ProviderHealth(kv).state("anthropic")
    assert (state.state, state.reason) == ("cooling", "timeout")


@pytest.mark.asyncio
async def test_exhausted_headroom_cools_provider_after_a_success():
    kv = MemoryKv()
    router = Router(anthropic=lambda r: httpx.Response(
        200, headers={"anthropic-ratelimit-requests-remaining": "0",
                      "anthropic-ratelimit-requests-reset": "2099-01-01T00:00:00Z"},
        json={"content": [{"type": "text", "text": "last one"}]}))
    svc = ManagerLlmService(settings(**PREMIUM_AND_FREE), transport=router.transport(), kv=kv)
    text, _, _ = await svc.generate_with_fallback(ask())
    assert text == "last one"
    state = await ProviderHealth(kv).state("anthropic")
    assert (state.state, state.reason) == ("cooling", "headroom")


def test_default_runtime_is_anthropic_first():
    svc = ManagerLlmService(settings(**PREMIUM_AND_FREE))
    assert svc._default_runtime().provider == "anthropic"
    assert ManagerLlmService(settings(openai_api_key="o", gemini_api_key="g"))._default_runtime().provider == "openai"


# ── Status exposes the chain ────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_status_reports_chain_order_health_and_spend():
    from app.ai.failures import classify_http

    kv = MemoryKv()
    svc = ManagerLlmService(settings(**PREMIUM_AND_FREE, ai_daily_cap_usd="anthropic=20"), kv=kv)
    await svc.health.record_failure("anthropic", classify_http(429, "rate_limit", retry_after=40))
    await svc.spend.record("anthropic", "claude-sonnet-4-6",
                           {"usage": {"input_tokens": 1_000_000, "output_tokens": 0}})

    status = await svc.status()
    assert [e.provider for e in status.chain] == ["anthropic", "openai", "gemini"]
    first = status.chain[0]
    assert (first.tier, first.state, first.reason) == ("premium", "cooling", "rate_limit")
    assert 0 < first.retry_in_s <= 40
    assert (first.spend_today_usd, first.daily_cap_usd) == (3.0, 20.0)
    assert (status.chain[1].state, status.chain[2].tier) == ("healthy", "free")
    assert status.provider == "anthropic" and status.configured is True


# ── Production incident 2026-09-28: pinned Ollama unreachable, premium empty ──

class _NoOllama:
    """Transport where ollama.test refuses connections and cloud hosts answer."""

    def __init__(self, router: Router):
        self.router = router
        self.ollama_calls = 0

    async def __call__(self, request: httpx.Request) -> httpx.Response:
        if request.url.host == "ollama.test":
            self.ollama_calls += 1
            raise httpx.ConnectError("connection refused", request=request)
        return await self.router(request)


@pytest.mark.asyncio
async def test_unreachable_pinned_ollama_is_cooled_and_skipped():
    kv = MemoryKv()
    transport = _NoOllama(Router())
    cfg = settings(llm_provider="ollama", ollama_base_url="http://ollama.test", **PREMIUM_AND_FREE)
    svc = ManagerLlmService(cfg, transport=httpx.MockTransport(transport), kv=kv)
    _, runtime, fallback = await svc.generate_with_fallback(ask())
    assert (runtime.provider, fallback) == ("anthropic", True)
    state = await ProviderHealth(kv).state("ollama")
    assert (state.state, state.reason) == ("cooling", "network")

    again = ManagerLlmService(cfg, transport=httpx.MockTransport(transport), kv=kv)
    await again.generate_with_fallback(ask())
    assert transport.ollama_calls == 1               # not retried while cooling


_EMPTY_PREMIUM = dict(
    anthropic=_err(400, "Your credit balance is too low to access the Anthropic API."),
    openai=_err(429, "You have no credits remaining."),
)


@pytest.mark.asyncio
async def test_premium_task_falls_to_free_tier_only_after_premium_fails():
    # The user's requirement: when premium limits are exhausted the call must
    # still be served — by the free tier, last, and flagged as a fallback.
    router = Router(**_EMPTY_PREMIUM)
    svc = ManagerLlmService(settings(**PREMIUM_AND_FREE), transport=router.transport())
    _, runtime, fallback = await svc.generate_with_fallback(ask("compliance_brief"))
    assert (runtime.provider, runtime.tier, fallback) == ("gemini", "free", True)
    assert router.calls == ["anthropic", "openai", "gemini"]


@pytest.mark.asyncio
async def test_strict_quality_floor_keeps_free_models_off_premium_tasks():
    router = Router(**_EMPTY_PREMIUM)
    svc = ManagerLlmService(settings(**PREMIUM_AND_FREE, ai_strict_quality_floor=True),
                            transport=router.transport())
    with pytest.raises(AiRuntimeError):
        await svc.generate_with_fallback(ask("compliance_brief"))
    assert "gemini" not in router.calls


@pytest.mark.asyncio
async def test_tiers_meeting_the_floor_are_tried_before_lower_ones():
    router = Router()
    svc = ManagerLlmService(settings(**PREMIUM_AND_FREE, llm_chain="gemini,anthropic,openai"),
                            transport=router.transport())
    _, runtime, _ = await svc.generate_with_fallback(ask("compliance_brief"))
    assert runtime.provider == "anthropic"
    assert router.calls == ["anthropic"]


@pytest.mark.asyncio
async def test_total_failure_names_every_providers_reason():
    # The AWS error said only "Ollama is not reachable" while Anthropic was out of
    # credit and the OpenAI key was rejected — the operator could not see why.
    router = Router(anthropic=_err(400, "Your credit balance is too low to access the Anthropic API."),
                    openai=_err(401, "Incorrect API key provided."))
    transport = _NoOllama(router)
    cfg = settings(llm_provider="ollama", ollama_base_url="http://ollama.test",
                   anthropic_api_key="a", openai_api_key="o")
    svc = ManagerLlmService(cfg, transport=httpx.MockTransport(transport))
    with pytest.raises(AiRuntimeError) as exc:
        await svc.generate_with_fallback(ask("engagement_report"))
    message = str(exc.value)
    assert "ollama: unreachable" in message
    assert "anthropic: out of credit" in message
    assert "openai: API key rejected" in message
    assert exc.value.status_code == 503


@pytest.mark.asyncio
async def test_skipped_providers_are_named_too():
    kv = MemoryKv()
    from app.ai.failures import classify_http
    await ProviderHealth(kv).record_failure("anthropic", classify_http(400, "credit balance is too low"))
    router = Router(openai=_err(429, "You have no credits remaining."))
    svc = ManagerLlmService(settings(anthropic_api_key="a", openai_api_key="o"),
                            transport=router.transport(), kv=kv)
    with pytest.raises(AiRuntimeError) as exc:
        await svc.generate_with_fallback(ask())
    assert "anthropic: out of credit" in str(exc.value)
    assert "openai: out of credit" in str(exc.value)

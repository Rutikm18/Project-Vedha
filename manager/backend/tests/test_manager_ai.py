from __future__ import annotations

import httpx
import pytest
from pydantic import ValidationError

from app.config import Settings
from app.schemas.ai import AiGenerateRequest
from app.services.llm import AiRuntimeError, ManagerLlmService


@pytest.mark.asyncio
async def test_manager_ollama_generation_owns_security_prompt_and_context():
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if request.url.path == "/api/tags":
            return httpx.Response(200, json={"models": [{"name": "llama3:latest"}]})
        body = __import__("json").loads(request.content)
        system = body["messages"][0]["content"]
        assert "Public CVE metadata" in system
        assert "## Remediation plan" in system
        assert '"source":"cve"' in system
        assert body["options"]["num_predict"] == 900
        return httpx.Response(200, json={"message": {"content": "## What is the vulnerability?\nGrounded."}})

    service = ManagerLlmService(
        Settings(
            llm_provider="ollama",
            ollama_base_url="http://ollama.test",
            ollama_model="llama3:latest",
        ),
        transport=httpx.MockTransport(handler),
    )
    request = AiGenerateRequest(
        task="security_brief",
        messages=[{"role": "user", "content": "Explain it"}],
        context={"securityBrief": {"source": "cve", "cveIds": ["CVE-2025-32463"]}},
    )

    content, runtime = await service.generate(request)

    assert content.endswith("Grounded.")
    assert runtime.provider == "ollama"
    assert runtime.privacy == "local"
    assert [item.url.path for item in requests] == ["/api/tags", "/api/chat"]


@pytest.mark.asyncio
async def test_manager_openrouter_free_selection_is_server_side():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/v1/chat/completions"
        assert request.headers["authorization"] == "Bearer manager-secret"
        body = __import__("json").loads(request.content)
        assert body["model"] == "openrouter/free"
        return httpx.Response(200, json={"choices": [{"message": {"content": "Defensive answer"}}]})

    service = ManagerLlmService(
        Settings(
            llm_provider="ollama",
            openrouter_api_key="manager-secret",
            openrouter_model="openrouter/free",
        ),
        transport=httpx.MockTransport(handler),
    )
    request = AiGenerateRequest(
        task="advisor",
        provider="openrouter",
        model="openrouter/free",
        messages=[{"role": "user", "content": "Prioritize remediation"}],
    )

    content, runtime = await service.generate(request)

    assert content == "Defensive answer"
    assert runtime.provider == "openrouter"
    assert runtime.privacy == "cloud"


@pytest.mark.asyncio
async def test_manager_openai_generation_is_server_side():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/v1/chat/completions"
        assert request.headers["authorization"] == "Bearer openai-secret"
        body = __import__("json").loads(request.content)
        assert body["model"] == "gpt-4o-mini"
        assert body["messages"][0]["role"] == "system"
        return httpx.Response(200, json={"choices": [{"message": {"content": "Defensive answer"}}]})

    service = ManagerLlmService(
        Settings(
            llm_provider="openai",
            openai_api_key="openai-secret",
            openai_model="gpt-4o-mini",
        ),
        transport=httpx.MockTransport(handler),
    )
    request = AiGenerateRequest(
        task="advisor",
        provider="openai",
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Prioritize remediation"}],
    )

    content, runtime = await service.generate(request)

    assert content == "Defensive answer"
    assert runtime.provider == "openai"
    assert runtime.privacy == "cloud"


@pytest.mark.asyncio
async def test_manager_openai_rejects_unconfigured_and_unenabled_model():
    unconfigured = ManagerLlmService(Settings(openai_api_key=""))
    with pytest.raises(AiRuntimeError, match="not configured") as exc:
        await unconfigured.generate(AiGenerateRequest(
            task="advisor", provider="openai",
            messages=[{"role": "user", "content": "Hello"}],
        ))
    assert exc.value.status_code == 503

    configured = ManagerLlmService(
        Settings(openai_api_key="configured", openai_model="gpt-4o-mini"),
    )
    with pytest.raises(AiRuntimeError, match="not enabled") as exc:
        await configured.generate(AiGenerateRequest(
            task="advisor", provider="openai", model="gpt-4o",
            messages=[{"role": "user", "content": "Hello"}],
        ))
    assert exc.value.status_code == 403


@pytest.mark.asyncio
async def test_manager_rejects_unconfigured_cloud_provider():
    service = ManagerLlmService(Settings(openrouter_api_key=""))
    request = AiGenerateRequest(
        task="advisor",
        provider="openrouter",
        messages=[{"role": "user", "content": "Hello"}],
    )

    with pytest.raises(AiRuntimeError, match="not configured") as exc_info:
        await service.generate(request)

    assert exc_info.value.status_code == 503


@pytest.mark.asyncio
async def test_manager_rejects_cloud_model_not_enabled_by_deployment():
    service = ManagerLlmService(
        Settings(openrouter_api_key="configured", openrouter_model="openrouter/free"),
    )
    request = AiGenerateRequest(
        task="advisor",
        provider="openrouter",
        model="paid/vendor-model",
        messages=[{"role": "user", "content": "Hello"}],
    )

    with pytest.raises(AiRuntimeError, match="not enabled") as exc_info:
        await service.generate(request)

    assert exc_info.value.status_code == 403


@pytest.mark.asyncio
async def test_manager_status_returns_only_server_configured_choices():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={"models": [
                {"name": "llama3:latest"},
                {"name": "qwen3:8b"},
                {"name": "minimax-m2.5:cloud"},
            ]},
        )

    service = ManagerLlmService(
        Settings(
            llm_provider="ollama",
            ollama_model="llama3:latest",
            openrouter_api_key="configured",
        ),
        transport=httpx.MockTransport(handler),
    )

    result = await service.status()

    assert result.configured is True
    assert result.provider == "ollama"
    assert result.providers[0].models == ["llama3:latest", "qwen3:8b"]
    assert result.providers[1].configured is True
    assert result.providers[1].models[0] == "openrouter/free"
    assert result.providers[2].configured is False


@pytest.mark.asyncio
async def test_manager_rejects_ollama_cloud_proxy_as_local():
    service = ManagerLlmService(Settings(ollama_model="llama3:latest"))
    request = AiGenerateRequest(
        task="advisor",
        provider="ollama",
        model="minimax-m2.5:cloud",
        messages=[{"role": "user", "content": "Hello"}],
    )

    with pytest.raises(AiRuntimeError, match="cloud-proxy") as exc_info:
        await service.generate(request)

    assert exc_info.value.status_code == 403


def test_ai_request_rejects_unsafe_model_and_oversized_context():
    with pytest.raises(ValidationError, match="unsupported characters"):
        AiGenerateRequest(
            task="advisor",
            model="../model?token=secret",
            messages=[{"role": "user", "content": "Hello"}],
        )

    with pytest.raises(ValidationError, match="context exceeds"):
        AiGenerateRequest(
            task="advisor",
            messages=[{"role": "user", "content": "Hello"}],
            context={"evidence": "x" * 33_000},
        )


# ── Cloud-only provider selection (auto-detect from key; no local fallback) ─────

def _cloud(**keys) -> Settings:
    """Settings with provider unset and all cloud keys pinned, so .env cannot
    leak a real key into these deterministic cloud-only tests."""
    base = dict(llm_provider="", openai_api_key="", anthropic_api_key="", openrouter_api_key="")
    base.update(keys)
    return Settings(**base)


def test_default_auto_detects_the_configured_cloud_provider():
    # Only Anthropic configured → it becomes the default. Never Ollama.
    rt = ManagerLlmService(_cloud(anthropic_api_key="ak"))._default_runtime()
    assert rt.provider == "anthropic"
    assert rt.privacy == "cloud"


def test_default_auto_detect_prefers_openai_then_anthropic_then_openrouter():
    svc = ManagerLlmService(_cloud(openai_api_key="o", anthropic_api_key="a", openrouter_api_key="r"))
    assert svc._default_runtime().provider == "openai"
    svc2 = ManagerLlmService(_cloud(anthropic_api_key="a", openrouter_api_key="r"))
    assert svc2._default_runtime().provider == "anthropic"


def test_default_runtime_fails_closed_without_any_cloud_key():
    svc = ManagerLlmService(_cloud())  # no keys at all
    with pytest.raises(AiRuntimeError, match="No cloud AI provider") as exc:
        svc._default_runtime()
    assert exc.value.status_code == 503


@pytest.mark.asyncio
async def test_generate_fails_closed_when_no_cloud_provider_configured():
    svc = ManagerLlmService(_cloud())
    with pytest.raises(AiRuntimeError, match="provider is configured") as exc:
        await svc.generate_with_fallback(
            AiGenerateRequest(task="advisor", messages=[{"role": "user", "content": "Hi"}])
        )
    assert exc.value.status_code == 503


def test_fallback_never_includes_local_ollama():
    # Cloud primary configured; the fallback chain must stay cloud-only.
    svc = ManagerLlmService(_cloud(openai_api_key="o", openrouter_api_key="r"))
    candidates = svc._fallback_candidates(
        AiGenerateRequest(task="advisor", messages=[{"role": "user", "content": "Hi"}])
    )
    assert candidates, "expected the cloud primary as a candidate"
    assert all(c.provider != "ollama" for c in candidates)
    assert all(c.privacy == "cloud" for c in candidates)


@pytest.mark.asyncio
async def test_status_fails_safe_without_cloud_key():
    st = await ManagerLlmService(_cloud()).status()
    assert st.configured is False
    assert st.provider is None
    assert "No cloud AI provider" in (st.reason or "")

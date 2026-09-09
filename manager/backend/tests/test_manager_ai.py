from __future__ import annotations

import httpx
import pytest
from pydantic import ValidationError

from app.config import Settings
from app.schemas.ai import AiGenerateRequest
from app.services.llm import AiRuntimeError, ManagerLlmService
from app.services.llm_http_client import AsyncLlmHttpClient


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


def test_advisor_flow_prompt_grounds_lifecycle_facts():
    """The advisor_flow rules instruct the model to use lifecycle facts, and the
    real lifecycle values are serialized into the untrusted <security_context>."""
    service = ManagerLlmService(Settings(llm_provider="openai", openai_api_key="sk-test"))
    request = AiGenerateRequest(
        task="advisor_flow",
        messages=[{"role": "user", "content": "brief"}],
        context={"securityBrief": {"lifecycle": {
            "ageDays": 34, "regressed": True, "reopenedCount": 2,
        }}},
    )

    system = service._build_system(request)

    # The task rules must teach the model to reason over lifecycle/regression.
    assert "lifecycle" in system.lower()
    assert "regress" in system.lower()
    # The real recorded facts flow through as grounded (untrusted) context.
    assert '"ageDays":34' in system
    assert '"regressed":true' in system


def test_advisor_prompt_enforces_the_vulnerability_brief_contract():
    service = ManagerLlmService(Settings(llm_provider="openai", openai_api_key="sk-test"))
    request = AiGenerateRequest(
        task="advisor",
        messages=[{"role": "user", "content": "Explain CVE-2025-32463"}],
    )

    system = service._build_system(request)

    assert "250 words" in system
    assert "## Key facts" in system
    assert "impact bullets" in system.lower()
    assert "## Severity and score" in system
    assert "1. Verify" in system
    assert "2. Remediation actions" in system
    assert "3. Further hardening" in system
    assert "Linux" in system
    assert "Windows" in system
    assert "macOS" in system
    assert "do not calculate" in system.lower()


@pytest.mark.asyncio
async def test_async_llm_http_client_uses_injected_transport_and_default_timeout():
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json={"ok": True})

    transport = AsyncLlmHttpClient(
        timeout_seconds=17.0,
        transport=httpx.MockTransport(handler),
    )

    async with transport.open() as client:
        response = await client.get("https://llm.test/health")

    assert response.json() == {"ok": True}
    assert seen[0].url == httpx.URL("https://llm.test/health")
    assert response.request.extensions["timeout"]["read"] == 17.0


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


@pytest.mark.asyncio
async def test_manager_gemini_generation_is_server_side():
    def handler(request: httpx.Request) -> httpx.Response:
        # generateContent endpoint, key in a header (never the query string).
        assert request.url.path == "/v1beta/models/gemini-2.0-flash:generateContent"
        assert request.headers["x-goog-api-key"] == "gemini-secret"
        body = __import__("json").loads(request.content)
        # Gemini shape: separate system_instruction + contents/parts, role "user".
        assert "Public CVE metadata" in body["system_instruction"]["parts"][0]["text"]
        assert body["contents"][0]["role"] == "user"
        assert body["contents"][0]["parts"][0]["text"] == "Prioritize remediation"
        assert body["generationConfig"]["maxOutputTokens"] == 900
        return httpx.Response(200, json={
            "candidates": [{"content": {"parts": [{"text": "Defensive Gemini answer"}]}}]
        })

    service = ManagerLlmService(
        Settings(
            llm_provider="gemini",
            gemini_api_key="gemini-secret",
            gemini_model="gemini-2.0-flash",
        ),
        transport=httpx.MockTransport(handler),
    )
    request = AiGenerateRequest(
        task="advisor",
        provider="gemini",
        model="gemini-2.0-flash",
        messages=[{"role": "user", "content": "Prioritize remediation"}],
    )

    content, runtime = await service.generate(request)

    assert content == "Defensive Gemini answer"
    assert runtime.provider == "gemini"
    assert runtime.privacy == "cloud"


@pytest.mark.asyncio
async def test_manager_gemini_rejects_unconfigured_and_unenabled_model():
    unconfigured = ManagerLlmService(Settings(gemini_api_key=""))
    with pytest.raises(AiRuntimeError, match="not configured") as exc:
        await unconfigured.generate(AiGenerateRequest(
            task="advisor", provider="gemini",
            messages=[{"role": "user", "content": "Hello"}],
        ))
    assert exc.value.status_code == 503

    configured = ManagerLlmService(
        Settings(gemini_api_key="configured", gemini_model="gemini-2.0-flash"),
    )
    with pytest.raises(AiRuntimeError, match="not enabled") as exc:
        await configured.generate(AiGenerateRequest(
            task="advisor", provider="gemini", model="gemini-1.5-pro",
            messages=[{"role": "user", "content": "Hello"}],
        ))
    assert exc.value.status_code == 403


def test_anthropic_system_blocks_split_stable_prefix_from_context():
    from app.services.llm import _anthropic_system_blocks

    system = "BASE RULES + task contract\n\n<security_context>\n{\"finding\":\"x\"}\n</security_context>"
    blocks = _anthropic_system_blocks(system)
    assert len(blocks) == 2
    # Stable rules prefix is cached and does NOT contain the per-request context.
    assert blocks[0]["text"] == "BASE RULES + task contract"
    assert blocks[0]["cache_control"] == {"type": "ephemeral"}
    assert "<security_context>" not in blocks[0]["text"]
    # Context is its own (also-cached) block, reconstructed exactly.
    assert blocks[1]["text"] == "<security_context>\n{\"finding\":\"x\"}\n</security_context>"
    assert blocks[1]["cache_control"] == {"type": "ephemeral"}


def test_anthropic_system_blocks_single_block_when_no_context():
    from app.services.llm import _anthropic_system_blocks

    blocks = _anthropic_system_blocks("just the stable rules")
    assert len(blocks) == 1
    assert blocks[0]["text"] == "just the stable rules"
    assert blocks[0]["cache_control"] == {"type": "ephemeral"}


@pytest.mark.asyncio
async def test_anthropic_generate_sends_prompt_cache_blocks():
    captured: dict = {}

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/v1/messages"
        captured["body"] = __import__("json").loads(request.content)
        return httpx.Response(200, json={"content": [{"type": "text", "text": "Grounded answer"}]})

    service = ManagerLlmService(
        Settings(llm_provider="anthropic", anthropic_api_key="ak", llm_model="claude-sonnet-4-6"),
        transport=httpx.MockTransport(handler),
    )
    content, runtime = await service.generate(AiGenerateRequest(
        task="advisor", provider="anthropic", model="claude-sonnet-4-6",
        messages=[{"role": "user", "content": "Prioritise"}],
        context={"finding": "SMB signing not required"},
    ))

    assert content == "Grounded answer"
    system = captured["body"]["system"]
    # System is now a list of cache-control blocks, not a bare string.
    assert isinstance(system, list)
    assert system[0]["cache_control"] == {"type": "ephemeral"}
    # The stable rules block carries the base policy (which itself references the
    # <security_context> tag by name — that's fine); the per-request finding DATA
    # must live in a later, separate block, not the cached stable prefix.
    assert "senior defensive security advisor" in system[0]["text"]
    assert "SMB signing not required" not in system[0]["text"]
    assert any("SMB signing not required" in b["text"] for b in system[1:])


@pytest.mark.asyncio
async def test_non_ascii_key_is_treated_as_unconfigured_not_a_crash():
    # Regression: a '₹' (non-ASCII) OpenRouter key used to poison the fallback and
    # surface as an opaque "openrouter response was unavailable" 502. It must now
    # read as simply NOT configured everywhere.
    svc = ManagerLlmService(Settings(openrouter_api_key="₹", anthropic_api_key=""))
    st = await svc.status()
    router = next(p for p in st.providers if p.id == "openrouter")
    assert router.configured is False
    assert "invalid" in (router.reason or "").lower()
    # Selecting it explicitly gives a clean 503, not a downstream crash.
    with pytest.raises(AiRuntimeError, match="not configured") as exc:
        await svc.generate(AiGenerateRequest(
            task="advisor", provider="openrouter",
            messages=[{"role": "user", "content": "Hello"}],
        ))
    assert exc.value.status_code == 503


@pytest.mark.asyncio
async def test_fallback_skips_provider_with_invalid_key():
    # With only a broken OpenRouter key, the fallback chain must be empty and the
    # caller gets an honest "no provider configured" instead of a poisoned attempt.
    svc = ManagerLlmService(Settings(openrouter_api_key="  ", llm_provider=""))
    with pytest.raises(AiRuntimeError) as exc:
        await svc.generate_with_fallback(AiGenerateRequest(
            task="advisor", messages=[{"role": "user", "content": "Hello"}],
        ))
    assert exc.value.status_code == 503


@pytest.mark.asyncio
async def test_gemini_is_auto_detected_and_reported_in_status():
    # Only a Gemini key configured (no openai/anthropic) → it becomes the default,
    # and it appears configured in the provider status list.
    service = ManagerLlmService(Settings(gemini_api_key="gemini-secret"))
    st = await service.status()
    assert st.provider == "gemini"
    assert st.configured is True
    gemini = next(p for p in st.providers if p.id == "gemini")
    assert gemini.configured is True
    assert gemini.privacy == "cloud"

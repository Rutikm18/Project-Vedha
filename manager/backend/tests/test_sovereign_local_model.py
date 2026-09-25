"""Sovereign profile: in-bank OpenAI-compatible model (vLLM/TGI), no cloud path at all."""
from __future__ import annotations

import json

import httpx
import pytest

from app.config import get_settings
from app.schemas.ai import AiGenerateRequest, AiMessage
from app.services.llm import AiRuntimeError, ManagerLlmService, is_internal_endpoint


def _svc(handler=None, **overrides):
    base = {"deployment_profile": "sovereign", "llm_provider": "local_openai",
            "local_llm_base_url": "http://10.50.0.7:8000/v1", "local_llm_model": "qwen2.5-32b-instruct",
            "local_llm_api_key": "", "anthropic_api_key": "sk-ant-test-key-0000000000",
            "openrouter_api_key": "sk-or-v1-test-0000000000000000"}
    settings = get_settings().model_copy(update={**base, **overrides})
    transport = httpx.MockTransport(handler or (lambda r: httpx.Response(500)))
    return ManagerLlmService(settings, transport=transport)


def _req(text="What about 10.20.0.20?"):
    return AiGenerateRequest(task="advisor", messages=[AiMessage(role="user", content=text)],
                             context={"hostname": "hsm-pay-01"})


@pytest.mark.parametrize("url,ok", [
    ("http://10.50.0.7:8000/v1", True), ("http://192.168.1.5/v1", True),
    ("http://localhost:8000/v1", True), ("http://127.0.0.1:8000/v1", True),
    ("http://vllm.internal:8000/v1", True), ("http://llm.bank.local/v1", True),
    ("http://vllm:8000/v1", True),                      # compose/k8s service name
    ("https://api.openai.com/v1", False), ("https://34.120.10.5/v1", False),
    ("ftp://10.0.0.1/v1", False), ("not a url", False),
])
def test_internal_endpoint_guard(url, ok):
    assert is_internal_endpoint(url) is ok


@pytest.mark.asyncio
async def test_sovereign_uses_the_in_bank_model_with_raw_context():
    sent = {}

    def handler(request):
        sent["url"] = str(request.url)
        sent["body"] = json.loads(request.content)
        return httpx.Response(200, json={"choices": [{"message": {"content": "Isolate hsm-pay-01."}}]})

    svc = _svc(handler)
    text, runtime, fallback = await svc.generate_with_fallback(_req())
    assert sent["url"] == "http://10.50.0.7:8000/v1/chat/completions"
    assert sent["body"]["model"] == "qwen2.5-32b-instruct"
    assert "10.20.0.20" in json.dumps(sent["body"])          # local → raw, nothing leaves the bank
    assert (runtime.provider, runtime.privacy, fallback) == ("local_openai", "local", False)
    assert svc.audit_records[-1]["decision"] == "raw"


@pytest.mark.asyncio
async def test_public_url_labelled_local_is_refused():
    svc = _svc(local_llm_base_url="https://api.openai.com/v1")
    with pytest.raises(AiRuntimeError) as exc:
        await svc.generate_with_fallback(_req())
    assert exc.value.status_code == 503 and "internal" in str(exc.value)


def test_sovereign_default_must_be_local():
    svc = _svc(llm_provider="")                         # cloud keys present, but sovereign
    with pytest.raises(AiRuntimeError) as exc:
        svc._default_runtime()
    assert exc.value.status_code == 503 and "sovereign" in str(exc.value)


def test_sovereign_never_offers_a_cloud_fallback():
    svc = _svc()
    candidates = svc._fallback_candidates(_req())
    assert [c.provider for c in candidates] == ["local_openai"]


def test_sovereign_rejects_an_explicit_cloud_provider_request():
    svc = _svc()
    req = AiGenerateRequest(task="advisor", provider="anthropic", messages=[AiMessage(role="user", content="x")])
    assert all(c.privacy == "local" for c in svc._fallback_candidates(req))


@pytest.mark.asyncio
async def test_status_marks_cloud_disabled_under_sovereign():
    status = await _svc().status()
    by_id = {p.id: p for p in status.providers}
    assert status.provider == "local_openai" and status.privacy == "local"
    assert by_id["local_openai"].configured is True
    for cloud in ("anthropic", "openrouter", "openai", "gemini"):
        assert by_id[cloud].configured is False and "sovereign" in (by_id[cloud].reason or "")


def test_cloud_profile_can_still_use_local_openai():
    svc = _svc(deployment_profile="cloud")
    rt = svc._default_runtime()
    assert (rt.provider, rt.privacy) == ("local_openai", "local")

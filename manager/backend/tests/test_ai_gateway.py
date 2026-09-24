"""AI Gateway: pseudonymize-before-egress, rehydrate-on-return, deployment-profile policy."""
from __future__ import annotations

import json

import httpx
import pytest

from app.ai.gateway import GatewayDenied, Pseudonymizer, egress_decision

SECRET_BITS = ("10.20.30.40", "2001:db8::7", "dc01.corp.bank.local", "alice@bank.example",
               "CORP\\svc_backup", "00:1a:2b:3c:4d:5e", "cbs-db-01")


def _context_text() -> str:
    ctx = {"open_findings": [{"title": "SMB signing disabled on 10.20.30.40",
                              "hostname": "cbs-db-01", "fqdn": "dc01.corp.bank.local"}],
           "owner": "alice@bank.example", "evidence": "login as CORP\\svc_backup from 00:1a:2b:3c:4d:5e",
           "v6": "2001:db8::7", "authorised_scope": ["10.20.30.0/24"]}
    return "rules...\n\n<security_context>\n" + json.dumps(ctx) + "\n</security_context>"


def test_every_identifier_is_replaced():
    p = Pseudonymizer()
    out = p.pseudonymize(_context_text())
    for bit in SECRET_BITS:
        assert bit not in out, bit
    assert "[IP-1]" in out and "[HOST-" in out and "[EMAIL-1]" in out


def test_mapping_is_stable_within_a_request_and_round_trips():
    p = Pseudonymizer()
    a = p.pseudonymize("host 10.0.0.5 talks to 10.0.0.6 then 10.0.0.5 again")
    assert a == "host [IP-1] talks to [IP-2] then [IP-1] again"
    assert p.rehydrate("Patch [IP-1] first, then IP-2.") == "Patch 10.0.0.5 first, then 10.0.0.6."


def test_same_input_pseudonymizes_identically_so_prompt_cache_still_hits():
    assert Pseudonymizer().pseudonymize(_context_text()) == Pseudonymizer().pseudonymize(_context_text())


def test_non_identifiers_survive():
    p = Pseudonymizer()
    text = ("CVE-2024-3094 in OpenSSH 8.9p1; CVSS 9.8; RBI Annex 1 §7; Art. 32(1)(a); "
            "SMBv1; TLS 1.0; port 445/tcp; §500.17; see example.com docs")
    assert p.pseudonymize(text) == text


def test_hostnames_from_structured_keys_are_replaced_everywhere():
    p = Pseudonymizer()
    out = p.pseudonymize('{"hostname":"cbs-db-01"} ... cbs-db-01 is the core banking DB')
    assert "cbs-db-01" not in out and out.count("[HOST-1]") == 2


def test_rehydrate_leaves_unknown_tokens_alone():
    assert Pseudonymizer().rehydrate("[IP-9] is unknown") == "[IP-9] is unknown"


# ── policy ───────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("profile,privacy,expected", [
    ("cloud", "cloud", "raw"), ("cloud", "local", "raw"),
    ("hybrid", "cloud", "pseudonymize"), ("hybrid", "local", "raw"),
    ("sovereign", "local", "raw"),
])
def test_egress_decision(profile, privacy, expected):
    assert egress_decision(profile, privacy, force_pseudonymize=False) == expected


def test_sovereign_denies_cloud():
    with pytest.raises(GatewayDenied):
        egress_decision("sovereign", "cloud", force_pseudonymize=False)


def test_cloud_can_opt_in_to_pseudonymization():
    assert egress_decision("cloud", "cloud", force_pseudonymize=True) == "pseudonymize"


# ── end to end through ManagerLlmService: nothing raw reaches the wire ───────

@pytest.mark.asyncio
async def test_hybrid_never_sends_raw_identifiers_and_answer_is_rehydrated(monkeypatch):
    from app.config import get_settings
    from app.schemas.ai import AiGenerateRequest, AiMessage
    from app.services.llm import ManagerLlmService

    sent: dict = {}

    def handler(request: httpx.Request) -> httpx.Response:
        sent["body"] = request.content.decode()
        # The model answers in pseudonyms, as it only ever saw pseudonyms.
        return httpx.Response(200, json={"content": [{"type": "text", "text": "Isolate [IP-1] ([HOST-1]) now."}],
                                         "stop_reason": "end_turn"})

    settings = get_settings().model_copy(update={
        "deployment_profile": "hybrid", "anthropic_api_key": "sk-ant-test-key-0000000000",
        "llm_provider": "anthropic", "openrouter_api_key": ""})
    svc = ManagerLlmService(settings, transport=httpx.MockTransport(handler))
    req = AiGenerateRequest(task="advisor", messages=[AiMessage(role="user", content="What about 10.20.30.40?")],
                            context={"hostname": "cbs-db-01", "ip": "10.20.30.40"})
    text, runtime, _ = await svc.generate_with_fallback(req)

    assert "10.20.30.40" not in sent["body"] and "cbs-db-01" not in sent["body"]
    assert text == "Isolate 10.20.30.40 (cbs-db-01) now."


@pytest.mark.asyncio
async def test_sovereign_refuses_cloud_provider_with_503():
    from app.config import get_settings
    from app.schemas.ai import AiGenerateRequest, AiMessage
    from app.services.llm import AiRuntimeError, ManagerLlmService

    def handler(request):  # pragma: no cover - must never be called
        raise AssertionError("cloud provider was contacted under sovereign profile")

    settings = get_settings().model_copy(update={
        "deployment_profile": "sovereign", "anthropic_api_key": "sk-ant-test-key-0000000000",
        "llm_provider": "anthropic", "openrouter_api_key": ""})
    svc = ManagerLlmService(settings, transport=httpx.MockTransport(handler))
    req = AiGenerateRequest(task="advisor", messages=[AiMessage(role="user", content="hi")])
    with pytest.raises(AiRuntimeError) as exc:
        await svc.generate_with_fallback(req)
    assert exc.value.status_code == 503


# ── direct Anthropic-SDK paths (report generator, advisor agent) ─────────────

def _settings(profile):
    from app.config import get_settings
    return get_settings().model_copy(update={"deployment_profile": profile})


@pytest.mark.asyncio
async def test_report_generator_pseudonymizes_under_hybrid_and_is_refused_under_sovereign():
    from types import SimpleNamespace
    from unittest.mock import AsyncMock, MagicMock

    from app.ai.llm_report import LLMReportGenerator, LLMUnavailableError

    seen = {}

    async def create(**kw):
        seen["prompt"] = kw["messages"][0]["content"]
        return SimpleNamespace(stop_reason="end_turn",
                               content=[SimpleNamespace(type="text", text="Harden [IP-1].")])

    client = MagicMock()
    client.messages.create = AsyncMock(side_effect=create)
    gen = LLMReportGenerator(MagicMock(), client=client)
    gen._settings = _settings("hybrid")
    out = await gen._complete("Summarise exposure of 10.9.8.7")
    assert "10.9.8.7" not in seen["prompt"] and out == "Harden 10.9.8.7."

    gen._settings = _settings("sovereign")
    with pytest.raises(LLMUnavailableError):
        await gen._complete("anything")


@pytest.mark.asyncio
async def test_agent_pseudonymizes_tool_results_and_rehydrates_submission():
    import uuid
    from types import SimpleNamespace
    from unittest.mock import AsyncMock, MagicMock

    from app.ai.agent import AgentDecisionEngine

    sent_results: list[str] = []
    calls = {"n": 0}

    async def create(**kw):
        calls["n"] += 1
        for m in kw["messages"]:
            if m["role"] == "user" and isinstance(m["content"], list):
                sent_results.extend(r["content"] for r in m["content"])
        if calls["n"] == 1:
            return SimpleNamespace(stop_reason="tool_use", content=[
                SimpleNamespace(type="tool_use", id="t1", name="list_assets", input={"limit": 5})])
        return SimpleNamespace(stop_reason="tool_use", content=[
            SimpleNamespace(type="tool_use", id="t2", name="submit_recommendations",
                            input={"recommendations": [{"title": "Isolate [IP-1] ([HOST-1])"}]})])

    client = MagicMock()
    client.messages.create = AsyncMock(side_effect=create)
    engine = AgentDecisionEngine(MagicMock(), client=client)
    engine._settings = _settings("hybrid")
    engine._exec_read_tool = AsyncMock(return_value={"assets": [{"ip": "10.1.2.3", "hostname": "swift-sag-01"}]})
    persisted = {}

    async def persist(eid, run_id, submit_input):
        persisted.update(submit_input)
        return 1
    engine._persist = persist

    await engine.run(uuid.uuid4())

    assert sent_results and all("10.1.2.3" not in r and "swift-sag-01" not in r for r in sent_results)
    assert persisted["recommendations"][0]["title"] == "Isolate 10.1.2.3 (swift-sag-01)"

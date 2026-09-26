"""test_remediation_ai_refine.py — AI refinement layered on the KB plan.

The end-to-end test inspects the REAL bytes the gateway puts on the wire under
the hybrid profile (lesson from the 2026-09-26 real-LLM run: mocks of the
service masked a pseudonymisation leak that only the wire showed).
"""
from __future__ import annotations

import json
from types import SimpleNamespace

import httpx
import pytest

from app.ai.hallucination import HallucinationGuard
from app.remediation import ai_refine as R
from app.remediation.context import build_context
from app.remediation.plan import build_plan


def _finding():
    return SimpleNamespace(id="f1", title="OpenSSH regreSSHion", description="", remediation="",
                           evidence={"product": "openssh", "matched_version": "8.9p1", "fixed_version": "9.8p1",
                                     "port": 22},
                           cve_ids=["CVE-2024-6387"], severity=SimpleNamespace(value="high"),
                           epss_score=None, exploit_validated=False)


def _asset():
    return SimpleNamespace(ip_address="10.20.30.40", hostname="cbs-db-01", fqdn=None, os="Linux",
                           os_version="Ubuntu 22.04", asset_type=SimpleNamespace(value="server"),
                           criticality=SimpleNamespace(value="critical"), environment=None, tags=None)


def _ctx():
    return build_context(_finding(), _asset(), None)


def _kb():
    return build_plan(_finding(), _ctx(), os="linux")


def _overlay(ai):
    cves, versions = R.allowed_tokens([_ctx()])
    return R.overlay(_kb(), ai, allowed_cves=cves, allowed_versions=versions, guard=HallucinationGuard())


class TestOverlay:
    def test_omitted_fields_keep_kb_values(self):
        kb = _kb()
        plan, changes = _overlay({"summary": "Upgrade OpenSSH on the core banking DB first."})
        assert plan["summary"].startswith("Upgrade OpenSSH")
        assert plan["steps"] == kb["steps"]
        assert changes == [{"field": "summary", "step": None, "before": kb["summary"],
                            "after": plan["summary"]}]

    def test_step_edit_is_tracked(self):
        plan, changes = _overlay({"steps": [{"step": 1, "commands": ["sudo apt-get install --only-upgrade openssh-server"],
                                             "rollback": "apt-get install openssh-server=1:8.9p1-3"}]})
        s1 = plan["steps"][0]
        assert s1["ai_changed"] is True
        assert s1["commands_for_os"] == ["sudo apt-get install --only-upgrade openssh-server"]
        assert {c["field"] for c in changes} == {"commands", "rollback"}

    def test_unknown_step_number_ignored(self):
        plan, changes = _overlay({"steps": [{"step": 99, "description": "x" * 50}]})
        assert changes == []

    def test_destructive_command_dropped_and_flagged(self):
        plan, _ = _overlay({"steps": [{"step": 1, "commands": ["sudo rm -rf /etc/ssh", "sudo systemctl status ssh"]}]})
        s1 = plan["steps"][0]
        assert s1["commands_for_os"] == ["sudo systemctl status ssh"]
        assert s1["unsafe_commands_removed"] is True

    def test_unknown_cve_stripped(self):
        plan, _ = _overlay({"summary": "Fixes CVE-2024-6387 and CVE-2099-0001."})
        assert "CVE-2024-6387" in plan["summary"]
        assert "CVE-2099-0001" not in plan["summary"] and "[unverified CVE removed]" in plan["summary"]

    def test_unconfirmed_version_labelled(self):
        plan, _ = _overlay({"target_state": "OpenSSH ≥ 9.9p2"})
        assert plan["target_state"].endswith(R.UNVERIFIED_VERSION_LABEL)

    def test_confirmed_version_not_labelled(self):
        plan, _ = _overlay({"target_state": "OpenSSH ≥ 9.8p1 from the Ubuntu security pocket"})
        assert not plan["target_state"].endswith(R.UNVERIFIED_VERSION_LABEL)

    def test_additional_steps_capped(self):
        extra = [{"tier": "hardening", "title": f"Extra {i}", "description": "Do the thing properly."}
                 for i in range(6)]
        kb_len = len(_kb()["steps"])
        plan, _ = _overlay({"additional_steps": extra})
        assert len(plan["steps"]) == kb_len + R.MAX_EXTRA_STEPS
        assert plan["steps"][-1]["ai_added"] is True


class TestFingerprint:
    def test_stable_and_order_independent(self):
        a = build_context(_finding(), _asset(), None)
        b = build_context(_finding(), SimpleNamespace(**{**vars(_asset()), "ip_address": "10.0.0.9"}), None)
        assert R.facts_fingerprint([a, b]) == R.facts_fingerprint([b, a])

    def test_changes_when_version_changes(self):
        f2 = _finding()
        f2.evidence = {**f2.evidence, "matched_version": "9.8p1"}
        assert R.facts_fingerprint([_ctx()]) != R.facts_fingerprint([build_context(f2, _asset(), None)])


@pytest.mark.asyncio
async def test_hybrid_refine_never_sends_raw_identifiers_and_persists_audit(monkeypatch):
    from app.config import get_settings
    from app.services import domain_context
    from app.services.llm import ManagerLlmService

    sent: dict = {}
    answer = {"summary": "Upgrade OpenSSH on [HOST-1] ([IP-1]) during the next window.",
              "steps": [{"step": 1, "commands": ["sudo apt-get install --only-upgrade openssh-server"]}]}

    def handler(request: httpx.Request) -> httpx.Response:
        sent["body"] = request.content.decode()
        return httpx.Response(200, json={"content": [{"type": "text", "text": json.dumps(answer)}],
                                         "stop_reason": "end_turn"})

    settings = get_settings().model_copy(update={
        "deployment_profile": "hybrid", "anthropic_api_key": "sk-ant-test-key-0000000000",
        "llm_provider": "anthropic", "openrouter_api_key": ""})
    svc = ManagerLlmService(settings, transport=httpx.MockTransport(handler))

    async def no_brief(db, engagement, findings=()):
        return None
    persisted = {}

    async def capture(db, records, *, actor_id, engagement_id):
        persisted["records"] = records
    monkeypatch.setattr(domain_context, "domain_brief_for", no_brief)
    monkeypatch.setattr("app.ai.audit_chain.persist_ai_calls", capture)

    plan = await R.refine(None, engagement=SimpleNamespace(id="e1"), kb_plan=_kb(), contexts=[_ctx()],
                          findings=[_finding()], actor_id="u1", svc=svc)

    assert "10.20.30.40" not in sent["body"] and "cbs-db-01" not in sent["body"]
    assert "[IP-" in sent["body"] and "[HOST-" in sent["body"]      # pseudonyms, not raw values
    assert plan["source"] == "ai" and plan["summary"] == (
        "Upgrade OpenSSH on cbs-db-01 (10.20.30.40) during the next window.")
    assert plan["steps"][0]["commands_for_os"] == ["sudo apt-get install --only-upgrade openssh-server"]
    assert persisted["records"] and persisted["records"][0]["task"] == "remediation_refine"


@pytest.mark.asyncio
async def test_unparseable_answer_raises(monkeypatch):
    from app.config import get_settings
    from app.services import domain_context
    from app.services.llm import AiRuntimeError, ManagerLlmService

    def handler(request):
        return httpx.Response(200, json={"content": [{"type": "text", "text": "I cannot help"}],
                                         "stop_reason": "end_turn"})

    settings = get_settings().model_copy(update={
        "deployment_profile": "cloud", "anthropic_api_key": "sk-ant-test-key-0000000000",
        "llm_provider": "anthropic", "openrouter_api_key": ""})

    async def no_brief(db, engagement, findings=()):
        return None

    async def capture(db, records, *, actor_id, engagement_id):
        return None
    monkeypatch.setattr(domain_context, "domain_brief_for", no_brief)
    monkeypatch.setattr("app.ai.audit_chain.persist_ai_calls", capture)
    with pytest.raises(AiRuntimeError):
        await R.refine(None, engagement=SimpleNamespace(id="e1"), kb_plan=_kb(), contexts=[_ctx()],
                       findings=[_finding()], actor_id="u1",
                       svc=ManagerLlmService(settings, transport=httpx.MockTransport(handler)))

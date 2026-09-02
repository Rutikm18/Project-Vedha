"""
test_portal_assistant.py — the customer-facing AI assistant.

Free-form chat was an explicit product decision, taken against the portal's usual
rule that AI output reaches a customer only after operator review (reports are
gated to `approved`, remediation plans to `reviewed`). Because that gate does NOT
apply here, the two boundaries that DO apply carry the whole weight:

  DATA scope    — grounding context is built server-side from the caller's own
                  engagement. The request body carries no context, so a crafted
                  client cannot ask about another tenant or inject its own
                  "facts" as if they were recorded evidence.
  SUBJECT scope — the model runs the `client_assistant` task, whose rules confine
                  it to information security.

These tests pin both, plus the input bounds that stop the portal being used as an
unmetered pipe to the model. Handlers are called directly with a mocked async db
(repo convention).
"""
from __future__ import annotations

import asyncio
import uuid
from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import HTTPException
from pydantic import ValidationError

from app.models.enums import EngagementStatus, FindingSeverity, FindingStatus
from app.routers import portal
from app.schemas.auth import CurrentUser
from app.schemas.portal import ClientAssistantAsk, ClientAssistantMessage
from app.services.llm import AiRuntimeError


def _client(engagement: uuid.UUID | None = None) -> CurrentUser:
    return CurrentUser(user_id=uuid.uuid4(), tenant_id=uuid.uuid4(), role="client",
                       client_engagement_id=engagement or uuid.uuid4())


def _finding(**kw):
    base = dict(
        id=uuid.uuid4(), title="SMBv1 enabled", severity=FindingSeverity.critical,
        status=FindingStatus.open, cvss_score=None, risk_score=90,
        cve_ids=["CVE-2017-0144"], first_seen=datetime(2026, 9, 1, 10, 30, tzinfo=timezone.utc),
        remediation="Disable SMBv1",
    )
    base.update(kw)
    return SimpleNamespace(**base)


def _engagement(name="Acme", scope=("192.168.1.0/24",)):
    return SimpleNamespace(id=uuid.uuid4(), name=name,
                           status=EngagementStatus.active, scope_cidrs=list(scope))


def _db(engagement, findings, focus="__unset__"):
    """execute() → engagement, then findings, then (optionally) the focus finding."""
    eng_res = MagicMock(scalar_one_or_none=MagicMock(return_value=engagement))
    find_res = MagicMock()
    find_res.scalars = MagicMock(return_value=MagicMock(all=MagicMock(return_value=findings)))
    results = [eng_res, find_res]
    if focus != "__unset__":
        results.append(MagicMock(scalar_one_or_none=MagicMock(return_value=focus)))
    db = MagicMock()
    db.execute = AsyncMock(side_effect=results)
    db.add = MagicMock()
    db.flush = AsyncMock()
    db.commit = AsyncMock()
    return db


def _ask(text="Which finding should I fix first?", **kw):
    return ClientAssistantAsk(messages=[ClientAssistantMessage(role="user", content=text)], **kw)


class _Runtime:
    provider = "anthropic"
    model = "claude-sonnet-4-6"
    privacy = "cloud"


def _llm(captured: dict, reply="Fix SMBv1 first."):
    async def _gen(request):
        captured["request"] = request
        return reply, _Runtime(), False
    service = MagicMock()
    service.generate_with_fallback = AsyncMock(side_effect=_gen)
    return service


# ── DATA scope ───────────────────────────────────────────────────────────────

def test_context_is_built_server_side_from_the_callers_own_engagement():
    eng = _engagement()
    captured: dict = {}
    with patch.object(portal, "ManagerLlmService", return_value=_llm(captured)), \
         patch.object(portal, "record_audit", MagicMock()):
        reply = asyncio.run(portal.portal_assistant_chat(
            _ask(), _client(eng.id), _db(eng, [_finding()])))

    ctx = captured["request"].context
    assert ctx["engagement"]["name"] == "Acme"
    assert ctx["engagement"]["authorised_scope"] == ["192.168.1.0/24"]
    assert ctx["open_finding_count"] == 1
    assert ctx["open_findings"][0]["title"] == "SMBv1 enabled"
    assert reply.grounded is True


def test_request_body_cannot_carry_context():
    """The schema has no context field, so a client cannot inject its own
    'evidence' and have the model treat it as recorded fact."""
    assert "context" not in ClientAssistantAsk.model_fields


def test_only_the_whitelisted_finding_fields_reach_the_model():
    """Internal triage/evidence fields must never leave the operator side."""
    eng = _engagement()
    captured: dict = {}
    noisy = _finding(internal_notes="operator only", evidence_blob={"raw": "x"},
                     exploit_available=True)
    with patch.object(portal, "ManagerLlmService", return_value=_llm(captured)), \
         patch.object(portal, "record_audit", MagicMock()):
        asyncio.run(portal.portal_assistant_chat(_ask(), _client(eng.id), _db(eng, [noisy])))

    sent = captured["request"].context["open_findings"][0]
    assert set(sent) == {"id", "title", "severity", "status", "cvss_score",
                         "risk_score", "cve_ids", "first_seen", "remediation"}
    assert "internal_notes" not in sent and "evidence_blob" not in sent


def test_focus_finding_outside_the_engagement_is_404_not_403():
    """403 would confirm the id exists somewhere — a cross-tenant oracle."""
    eng = _engagement()
    db = _db(eng, [], focus=None)
    with patch.object(portal, "ManagerLlmService", return_value=_llm({})), \
         patch.object(portal, "record_audit", MagicMock()):
        with pytest.raises(HTTPException) as exc:
            asyncio.run(portal.portal_assistant_chat(
                _ask(finding_id=uuid.uuid4()), _client(eng.id), db))
    assert exc.value.status_code == 404


def test_focus_finding_in_scope_is_added_to_context():
    eng = _engagement()
    focus = _finding(title="RDP without NLA")
    captured: dict = {}
    with patch.object(portal, "ManagerLlmService", return_value=_llm(captured)), \
         patch.object(portal, "record_audit", MagicMock()):
        asyncio.run(portal.portal_assistant_chat(
            _ask(finding_id=focus.id), _client(eng.id), _db(eng, [], focus=focus)))
    assert captured["request"].context["question_is_about"]["title"] == "RDP without NLA"


def test_a_non_client_user_is_refused():
    operator = CurrentUser(user_id=uuid.uuid4(), tenant_id=uuid.uuid4(), role="manager")
    with pytest.raises(HTTPException) as exc:
        asyncio.run(portal.portal_assistant_chat(_ask(), operator, MagicMock()))
    assert exc.value.status_code in (403, 404)


# ── SUBJECT scope ────────────────────────────────────────────────────────────

def test_uses_the_security_restricted_task():
    eng = _engagement()
    captured: dict = {}
    with patch.object(portal, "ManagerLlmService", return_value=_llm(captured)), \
         patch.object(portal, "record_audit", MagicMock()):
        asyncio.run(portal.portal_assistant_chat(_ask(), _client(eng.id), _db(eng, [])))
    assert captured["request"].task == "client_assistant"


def test_the_task_rules_confine_the_model_to_security():
    from app.services.llm import _TASK_RULES
    rules = _TASK_RULES["client_assistant"].lower()
    assert "information security only" in rules or "security only" in rules
    assert "decline" in rules
    # and must not hand out attack tooling for their own estate
    assert "never provide exploit code" in rules


# ── input bounds ─────────────────────────────────────────────────────────────

class TestBounds:
    def test_rejects_an_empty_conversation(self):
        with pytest.raises(ValidationError):
            ClientAssistantAsk(messages=[])

    def test_rejects_an_oversized_turn(self):
        with pytest.raises(ValidationError):
            ClientAssistantAsk(messages=[ClientAssistantMessage(role="user", content="x" * 4_001)])

    def test_rejects_an_oversized_conversation(self):
        turns = [ClientAssistantMessage(role="user", content="x" * 3_999) for _ in range(5)]
        with pytest.raises(ValidationError):
            ClientAssistantAsk(messages=turns)

    def test_rejects_too_many_turns(self):
        turns = [ClientAssistantMessage(role="user", content="hi") for _ in range(17)]
        with pytest.raises(ValidationError):
            ClientAssistantAsk(messages=turns)

    def test_last_message_must_be_the_user(self):
        with pytest.raises(ValidationError):
            ClientAssistantAsk(messages=[ClientAssistantMessage(role="assistant", content="hi")])

    def test_accepts_a_normal_exchange(self):
        ask = ClientAssistantAsk(messages=[
            ClientAssistantMessage(role="user", content="what is SMB signing?"),
            ClientAssistantMessage(role="assistant", content="It authenticates SMB messages."),
            ClientAssistantMessage(role="user", content="why does it matter here?"),
        ])
        assert len(ask.messages) == 3


# ── failure handling ─────────────────────────────────────────────────────────

def test_model_failure_surfaces_its_status_not_a_500():
    eng = _engagement()
    service = MagicMock()
    service.generate_with_fallback = AsyncMock(side_effect=AiRuntimeError("timed out", 504))
    with patch.object(portal, "ManagerLlmService", return_value=service), \
         patch.object(portal, "record_audit", MagicMock()):
        with pytest.raises(HTTPException) as exc:
            asyncio.run(portal.portal_assistant_chat(_ask(), _client(eng.id), _db(eng, [])))
    assert exc.value.status_code == 504


def test_reply_is_timestamped_and_attributed():
    eng = _engagement()
    with patch.object(portal, "ManagerLlmService", return_value=_llm({})), \
         patch.object(portal, "record_audit", MagicMock()):
        reply = asyncio.run(portal.portal_assistant_chat(_ask(), _client(eng.id), _db(eng, [])))
    assert reply.model == "claude-sonnet-4-6"
    assert reply.generated_at.tzinfo is not None      # exact, timezone-aware


def test_the_exchange_is_audited():
    eng = _engagement()
    audit = MagicMock()
    with patch.object(portal, "ManagerLlmService", return_value=_llm({})), \
         patch.object(portal, "record_audit", audit):
        asyncio.run(portal.portal_assistant_chat(_ask(), _client(eng.id), _db(eng, [])))
    assert audit.call_count == 1
    assert audit.call_args.kwargs["action"] == "portal.assistant.chat"
    assert audit.call_args.kwargs["actor_id"] is not None

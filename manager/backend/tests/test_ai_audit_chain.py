"""Hash-chained AI call audit: records hash payloads (never store them) and detect tampering."""
from __future__ import annotations

import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest

from app.ai.audit_chain import GENESIS, ai_call_record, chain_hash, persist_ai_calls, verify_chain
from app.models.audit_log import AuditLog


def _rec(n=1):
    return ai_call_record(task="advisor", provider="anthropic", model="m", profile="hybrid",
                          decision="pseudonymize", system=f"sys {n}", messages=[{"role": "user", "content": "10.0.0.5?"}],
                          response="ok", replaced={"IP": 1})


def test_record_hashes_payloads_and_never_stores_them():
    rec = _rec()
    flat = str(rec)
    assert "10.0.0.5" not in flat and "sys 1" not in flat
    assert len(rec["request_sha256"]) == 64 and len(rec["response_sha256"]) == 64
    assert rec["redactions"] == {"IP": 1} and rec["decision"] == "pseudonymize"


def _rows(n):
    rows, prev = [], GENESIS
    for i in range(n):
        detail = {**_rec(i), "prev_hash": prev}
        detail["hash"] = chain_hash(prev, detail)
        prev = detail["hash"]
        rows.append(SimpleNamespace(id=i, detail=detail))
    return rows


def test_verify_intact_chain():
    assert verify_chain(_rows(4)) == {"ok": True, "records": 4, "broken_at": None}


def test_verify_detects_edited_record():
    rows = _rows(4)
    rows[2].detail["model"] = "something-else"
    out = verify_chain(rows)
    assert out["ok"] is False and out["broken_at"] == 2


def test_verify_detects_deleted_record():
    rows = _rows(4)
    del rows[1]
    assert verify_chain(rows)["broken_at"] == 1


@pytest.mark.asyncio
async def test_persist_links_to_previous_hash_and_takes_the_lock():
    db = MagicMock()
    db.execute = AsyncMock(side_effect=[MagicMock(),  # advisory lock
                                        MagicMock(scalar_one_or_none=lambda: {"hash": "a" * 64})])
    db.add = MagicMock()
    await persist_ai_calls(db, [_rec(1), _rec(2)], actor_id=uuid.uuid4(), engagement_id=None)
    rows = [c.args[0] for c in db.add.call_args_list]
    assert all(isinstance(r, AuditLog) and r.action == "ai.call" for r in rows)
    assert rows[0].detail["prev_hash"] == "a" * 64
    assert rows[1].detail["prev_hash"] == rows[0].detail["hash"]
    assert "pg_advisory_xact_lock" in str(db.execute.await_args_list[0].args[0])


@pytest.mark.asyncio
async def test_persist_nothing_is_a_noop():
    db = MagicMock(execute=AsyncMock())
    await persist_ai_calls(db, [], actor_id=uuid.uuid4(), engagement_id=None)
    db.execute.assert_not_awaited()


@pytest.mark.asyncio
async def test_service_collects_one_record_per_egress():
    from app.config import get_settings
    from app.schemas.ai import AiGenerateRequest, AiMessage
    from app.services.llm import ManagerLlmService

    def handler(request):
        return httpx.Response(200, json={"content": [{"type": "text", "text": "fine"}]})

    settings = get_settings().model_copy(update={
        "deployment_profile": "hybrid", "anthropic_api_key": "sk-ant-test-key-0000000000",
        "llm_provider": "anthropic", "openrouter_api_key": ""})
    svc = ManagerLlmService(settings, transport=httpx.MockTransport(handler))
    await svc.generate_with_fallback(AiGenerateRequest(task="advisor", messages=[AiMessage(role="user", content="10.1.1.1")]))
    assert len(svc.audit_records) == 1
    rec = svc.audit_records[0]
    assert rec["decision"] == "pseudonymize" and rec["redactions"] == {"IP": 1}
    assert rec["profile"] == "hybrid" and rec["provider"] == "anthropic"

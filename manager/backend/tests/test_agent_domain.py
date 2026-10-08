"""The advisor agent speaks as the engagement's sector expert (fail-soft)."""
from __future__ import annotations

import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.ai import agent as agent_mod
from app.ai.agent import SYSTEM_PROMPT, AgentDecisionEngine


def _engine(db):
    return AgentDecisionEngine(db, client=object())


def _db_returning(engagement):
    result = MagicMock()
    result.scalar_one_or_none.return_value = engagement
    db = MagicMock()
    db.execute = AsyncMock(return_value=result)
    return db


@pytest.mark.asyncio
async def test_default_system_is_plain_prompt():
    assert _engine(MagicMock())._system == SYSTEM_PROMPT


@pytest.mark.asyncio
async def test_sector_brief_is_appended(monkeypatch):
    eng = SimpleNamespace(id=uuid.uuid4(), rules_of_engagement={"profile": {"sector": "banking", "jurisdictions": ["IN"]}})
    from app.services import domain_context
    monkeypatch.setattr(domain_context, "engagement_tag_set", AsyncMock(return_value=set()))
    system = await _engine(_db_returning(eng))._system_with_domain(eng.id)
    assert system.startswith(SYSTEM_PROMPT)
    assert 'skill="banking"' in system and "CERT-In" in system


@pytest.mark.asyncio
async def test_lookup_failure_falls_back_to_plain_prompt():
    db = MagicMock()
    db.execute = AsyncMock(side_effect=RuntimeError("db down"))
    assert await _engine(db)._system_with_domain(uuid.uuid4()) == SYSTEM_PROMPT


@pytest.mark.asyncio
async def test_missing_engagement_falls_back():
    assert await _engine(_db_returning(None))._system_with_domain(uuid.uuid4()) == SYSTEM_PROMPT

"""Lean image (no `anthropic` SDK): an Anthropic-only key must still draft reports."""
from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from app.ai import llm_report
from app.ai.llm_report import LLMReportGenerator
from app.services.llm import ManagerLlmService
from tests.test_ai_chain import settings


@pytest.fixture
def lean(monkeypatch):
    cfg = settings(anthropic_api_key="a")
    monkeypatch.setattr("app.ai.llm_report.get_settings", lambda: cfg)
    monkeypatch.setattr("app.services.llm.get_settings", lambda: cfg)
    monkeypatch.setattr(llm_report, "_HAS_ANTHROPIC", False)
    return cfg


def test_anthropic_only_is_available_without_the_sdk(lean):
    gen = LLMReportGenerator(MagicMock())
    assert gen._client is None and gen.available is True


@pytest.mark.asyncio
async def test_chain_may_use_anthropic_when_there_is_no_sdk(lean, monkeypatch):
    seen: dict = {}

    async def complete_raw(self, **kwargs):
        seen.update(kwargs)
        return "claude over https", SimpleNamespace(provider="anthropic", model="m"), False

    monkeypatch.setattr(ManagerLlmService, "complete_raw", complete_raw)
    assert await LLMReportGenerator(MagicMock())._complete("write") == "claude over https"
    assert not seen["exclude"]   # anthropic stays eligible

"""
test_remediation_generator.py — Section 3: the AI remediation-plan helpers.

Pure/unit coverage for the fault-tolerant JSON extraction, the normalizer that
coerces model output into the KB schema while dropping guard-flagged commands, and
the generate_remediation_plan ValueError path when the model returns no usable plan.
"""
from __future__ import annotations

import asyncio
import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.ai.hallucination import HallucinationGuard
from app.ai.llm_report import (
    LLMReportGenerator,
    _normalize_ai_plan,
    _parse_json_response,
    _safe_commands,
)


def _finding():
    return SimpleNamespace(title="Weak TLS ciphers", description="TLS 1.0 enabled",
                           remediation="", cve_ids=[], severity=None, cvss_score=None,
                           epss_score=None, exploitable=False, exploit_validated=False)


class TestParseJsonResponse:
    def test_plain_object(self):
        assert _parse_json_response('{"a": 1}') == {"a": 1}

    def test_strips_json_fence(self):
        assert _parse_json_response('```json\n{"a": 1}\n```') == {"a": 1}

    def test_strips_bare_fence(self):
        assert _parse_json_response('```\n{"a": 1}\n```') == {"a": 1}

    def test_recovers_from_preamble(self):
        assert _parse_json_response('Sure! Here you go: {"a": 1} — done') == {"a": 1}

    def test_junk_returns_empty(self):
        assert _parse_json_response("no json anywhere here") == {}

    def test_non_object_json_returns_empty(self):
        assert _parse_json_response("[1, 2, 3]") == {}

    def test_empty_returns_empty(self):
        assert _parse_json_response("") == {}


class TestSafeCommands:
    def test_drops_destructive_keeps_safe(self):
        guard = HallucinationGuard()
        safe, had_unsafe = _safe_commands({"command": "rm -rf /var/data"}, guard)
        assert safe == [] and had_unsafe is True
        safe, had_unsafe = _safe_commands({"command": "sudo systemctl reload nginx"}, guard)
        assert safe == ["sudo systemctl reload nginx"] and had_unsafe is False

    def test_null_command_yields_nothing(self):
        safe, had_unsafe = _safe_commands({"command": None}, HallucinationGuard())
        assert safe == [] and had_unsafe is False


class TestNormalizeAiPlan:
    def _raw(self):
        return {
            "summary": "Disable weak TLS.", "effort": "low", "remediation_risk": "low",
            "steps": [
                {"title": "Wipe", "description": "d", "command": "rm -rf /etc",
                 "verification": "v", "risk": "high"},
                {"title": "Reload", "description": "d", "command": "sudo systemctl reload nginx",
                 "verification": "v", "risk": "low"},
            ],
            "verification": ["Re-scan the port"],
            "long_term_recommendations": ["Automate cert renewal"],
            "compensating_controls": "Terminate TLS at a proxy",
        }

    def test_emits_kb_schema_with_source_ai(self):
        plan = _normalize_ai_plan(self._raw(), "linux", HallucinationGuard())
        assert plan["source"] == "ai"
        assert plan["os"] == "linux"
        assert plan["category"] == "ai"
        assert plan["summary"] == "Disable weak TLS."
        assert plan["verification"] == ["Re-scan the port"]
        assert plan["long_term_recommendations"] == ["Automate cert renewal"]
        assert plan["compensating_controls"] == "Terminate TLS at a proxy"

    def test_drops_unsafe_command_and_flags_step(self):
        plan = _normalize_ai_plan(self._raw(), "linux", HallucinationGuard())
        wipe = plan["steps"][0]
        assert wipe["commands_for_os"] == []
        assert wipe["unsafe_commands_removed"] is True

    def test_keeps_safe_command_without_flag(self):
        plan = _normalize_ai_plan(self._raw(), "linux", HallucinationGuard())
        reload_step = plan["steps"][1]
        assert reload_step["commands_for_os"] == ["sudo systemctl reload nginx"]
        assert "unsafe_commands_removed" not in reload_step

    def test_missing_steps_yields_empty(self):
        plan = _normalize_ai_plan({}, "linux", HallucinationGuard())
        assert plan["steps"] == []

    def test_non_dict_step_is_skipped_and_missing_title_defaults(self):
        raw = {"steps": ["garbage", {"description": "no title"}]}
        plan = _normalize_ai_plan(raw, "linux", HallucinationGuard())
        assert len(plan["steps"]) == 1                       # the non-dict is dropped
        assert plan["steps"][0]["title"].startswith("Step")  # missing title → safe default


class TestGenerateRemediationPlan:
    def _gen(self, complete_return):
        gen = LLMReportGenerator(MagicMock(), client=object())  # available (client set)
        gen._complete = AsyncMock(return_value=complete_return)
        return gen

    def test_unparseable_output_raises_value_error(self):
        gen = self._gen("the model refused and wrote prose")
        with pytest.raises(ValueError):
            asyncio.run(gen.generate_remediation_plan(_finding(), "linux"))

    def test_valid_output_returns_ai_plan_with_model(self):
        gen = self._gen('{"summary": "x", "steps": [{"title": "Patch", '
                        '"command": "sudo apt-get upgrade", "risk": "low"}]}')
        plan = asyncio.run(gen.generate_remediation_plan(_finding(), "linux"))
        assert plan["source"] == "ai"
        assert plan["model"] == gen._model
        assert plan["steps"][0]["commands_for_os"] == ["sudo apt-get upgrade"]

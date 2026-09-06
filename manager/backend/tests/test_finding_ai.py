"""finding_ai — the OPTIONAL, fail-closed AI enrichment seam.

Contract under test: given a finding and an async completion callable, produce a
content_overrides dict (business_impact / technical_details) — but on ANY failure
(no key, transport error, malformed or empty output) return None so the caller
keeps the deterministic KB. AI is an enhancement, never a dependency.
"""
from __future__ import annotations

import asyncio
from types import SimpleNamespace

from app.services.finding_ai import MAX_FIELD_LEN, generate_content_overrides


def _f(**kw):
    base = dict(title="RDP exposed on 3389", description="", remediation="",
                cve_ids=[], evidence={"port": 3389}, severity="high")
    base.update(kw)
    return SimpleNamespace(**base)


def _run(finding, llm):
    return asyncio.run(generate_content_overrides(finding, llm))


def _llm_returning(text):
    async def _call(_prompt: str) -> str:
        return text
    return _call


def test_valid_json_becomes_overrides():
    llm = _llm_returning('{"business_impact": "Concrete board-level impact statement here.", '
                         '"technical_details": "Concrete technical explanation of the weakness."}')
    out = _run(_f(), llm)
    assert out["business_impact"].startswith("Concrete board-level")
    assert out["technical_details"].startswith("Concrete technical")


def test_json_wrapped_in_code_fences_is_parsed():
    llm = _llm_returning('```json\n{"business_impact": "Impact prose that is clearly long enough."}\n```')
    out = _run(_f(), llm)
    assert out == {"business_impact": "Impact prose that is clearly long enough."}


def test_llm_error_fails_closed_to_none():
    async def _boom(_prompt: str) -> str:
        raise RuntimeError("no API key configured")
    assert _run(_f(), _boom) is None


def test_non_json_output_fails_closed():
    assert _run(_f(), _llm_returning("I cannot help with that.")) is None


def test_missing_both_keys_fails_closed():
    assert _run(_f(), _llm_returning('{"something_else": "nope"}')) is None


def test_empty_or_whitespace_values_are_rejected():
    assert _run(_f(), _llm_returning('{"business_impact": "   ", "technical_details": ""}')) is None


def test_too_short_values_are_rejected():
    assert _run(_f(), _llm_returning('{"business_impact": "too short"}')) is None


def test_partial_output_returns_only_the_valid_field():
    llm = _llm_returning('{"technical_details": "A sufficiently long technical explanation string."}')
    out = _run(_f(), llm)
    assert set(out.keys()) == {"technical_details"}


def test_overlong_values_are_truncated():
    long_text = "A" * (MAX_FIELD_LEN + 500)
    out = _run(_f(), _llm_returning('{"business_impact": "' + long_text + '"}'))
    assert len(out["business_impact"]) <= MAX_FIELD_LEN


def test_none_llm_is_a_no_op():
    assert _run(_f(), None) is None

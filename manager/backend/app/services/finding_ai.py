"""finding_ai.py — the OPTIONAL, fail-closed AI enrichment seam for findings.

The deterministic KB (``finding_content``) is always the floor. This module is the
*ceiling raiser*: when — and only when — an LLM is configured, it asks the model to
sharpen a finding's business impact and technical explanation into prose tailored to
the specific asset and evidence, and returns a ``content_overrides`` dict. The read
path (``finding_content``) already prefers overrides field-by-field, so persisting
this dict onto ``findings.content_overrides`` is all that is needed to surface it.

Three hard rules keep AI from ever becoming a liability (mirrors ai_normalizer.py):

1. **Fail closed.** ANY problem — no key, transport error, malformed JSON, empty or
   implausibly short output — yields ``None``, and the caller silently keeps the KB.
2. **Never a hard dependency.** The completion callable is injected; this module
   imports no provider SDK and works in tests with a plain async function.
3. **Bounded and validated.** Output must be JSON with the expected keys, each a
   non-empty string of sane length (truncated to a ceiling). Nothing is trusted raw.

It deliberately does NOT invent CVEs/scores/exploit status — the prompt forbids it
and the KB (not the model) remains the source of those structured facts.
"""
from __future__ import annotations

import json
import re
from typing import Any, Awaitable, Callable

import structlog

from app.services.evidence_summary import summarize_evidence
from app.services.remediation_kb import classify_finding

logger = structlog.get_logger()

# Accepted override fields (must match the keys finding_content honours).
_FIELDS = ("business_impact", "technical_details")
# A field shorter than this is almost certainly a refusal/echo, not real prose.
MIN_FIELD_LEN = 40
# Upper bound so a runaway generation cannot bloat a stored record / the UI.
MAX_FIELD_LEN = 1200

LlmComplete = Callable[[str], Awaitable[str]]

_SYSTEM = (
    "You are Vedha's senior defensive security advisor writing for a client report. "
    "Rewrite the BUSINESS IMPACT and TECHNICAL EXPLANATION for ONE finding in clear, "
    "specific prose. Do NOT invent CVEs, CVSS/EPSS scores, exploit status, credentials, "
    "or affected assets beyond what is supplied. Return ONLY compact JSON of the form "
    '{"business_impact": "...", "technical_details": "..."}. No preamble, no code fence.'
)


def _build_prompt(finding: Any, asset_criticality: str | None) -> str:
    facts = summarize_evidence(getattr(finding, "evidence", None))
    fact_lines = "\n".join(f"- {f['label']}: {f['value']}" for f in facts) or "- (no structured evidence)"
    cves = ", ".join(str(c) for c in (getattr(finding, "cve_ids", None) or [])) or "none recorded"
    severity = getattr(finding, "severity", "unknown")
    severity = getattr(severity, "value", severity)
    return (
        f"{_SYSTEM}\n\n<security_context>\n"
        f"Title: {getattr(finding, 'title', '') or 'untitled'}\n"
        f"Category: {classify_finding(finding)}\n"
        f"Severity: {severity}\n"
        f"CVEs: {cves}\n"
        f"Asset criticality: {asset_criticality or 'unknown'}\n"
        f"Evidence:\n{fact_lines}\n"
        "</security_context>"
    )


def _extract_json(raw: str) -> dict | None:
    """Pull the first JSON object out of a completion, tolerating code fences and
    surrounding chatter. Returns None if nothing parses."""
    text = raw.strip()
    # Strip ```json … ``` or ``` … ``` fences if present.
    fence = re.search(r"```(?:json)?\s*(.+?)```", text, re.DOTALL)
    if fence:
        text = fence.group(1).strip()
    if not text.startswith("{"):
        brace = text.find("{")
        if brace == -1:
            return None
        text = text[brace:]
    if not text.endswith("}"):
        last = text.rfind("}")
        if last == -1:
            return None
        text = text[: last + 1]
    try:
        parsed = json.loads(text)
    except (json.JSONDecodeError, ValueError):
        return None
    return parsed if isinstance(parsed, dict) else None


def _validate(parsed: dict) -> dict | None:
    """Keep only well-formed override fields; None if nothing usable survives."""
    out: dict[str, str] = {}
    for key in _FIELDS:
        value = parsed.get(key)
        if not isinstance(value, str):
            continue
        cleaned = value.strip()
        if len(cleaned) < MIN_FIELD_LEN:
            continue
        out[key] = cleaned[:MAX_FIELD_LEN]
    return out or None


async def generate_content_overrides(
    finding: Any, llm_complete: LlmComplete | None, *, asset_criticality: str | None = None
) -> dict | None:
    """Return an AI-authored ``content_overrides`` dict for a finding, or None.

    ``llm_complete`` is an async ``(prompt) -> text`` callable — e.g. bridged to
    ``LLMReportGenerator._complete``. Passing ``None`` (no LLM configured) is a
    no-op. Every failure path returns None so the caller falls back to the KB.
    """
    if llm_complete is None:
        return None
    try:
        prompt = _build_prompt(finding, asset_criticality)
        raw = await llm_complete(prompt)
        parsed = _extract_json(raw or "")
        if parsed is None:
            return None
        return _validate(parsed)
    except Exception as exc:  # noqa: BLE001 — AI must never break the caller; fail closed.
        logger.info("finding_ai.enrich_failed", error=str(exc))
        return None

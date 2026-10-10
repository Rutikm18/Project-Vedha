"""report_enrichment.py — deterministic fallbacks for what a report finding did not record.

Pure and offline (no DB, no network, no AI). The report builder records what the platform
stored; where the narrative, the fix plan or the "why was this flagged" line was never
recorded, these helpers supply it from the knowledge base — and every use is labelled, so a
reader (or auditor) can tell recorded text from standard text:

    precedence    analyst/AI overrides  >  recorded evidence  >  knowledge base
    provenance    ``narrative_sources[field]`` is "recorded" or "knowledge_base"

Nothing here invents a fact about the asset: the KB text describes the weakness class, the
exploitation line says "Not validated" unless something validated it, and the fix plan is the
rule-keyed recipe rendered with the facts the platform actually holds.
"""
from __future__ import annotations

import re
from typing import Any

import structlog

from app.services.finding_content import content_category, finding_content

logger = structlog.get_logger(__name__)

SOURCE_RECORDED = "recorded"
SOURCE_KB = "knowledge_base"

_BASIS_LABEL = {
    "protocol_observed": "a protocol-level observation",
    "banner_inference": "a banner or service-name inference",
    "port_inference": "an open port only (no protocol confirmation)",
    "measured_factor": "a measured amplification factor",
}
# Text the posture bridge used to store as the description: rule metadata, not an
# explanation of the weakness.
_METADATA_LEAD = re.compile(r"^(CWE-\d+|ATT&CK\b|observed by\b)")


def _enum(value: Any) -> Any:
    return getattr(value, "value", value)


def _evidence(finding: Any) -> dict[str, Any]:
    ev = getattr(finding, "evidence", None)
    return ev if isinstance(ev, dict) else {}


def service_port(finding: Any) -> int | None:
    """The service port a finding is about, as recorded in its evidence (None if none)."""
    port = _evidence(finding).get("port")
    return port if isinstance(port, int) and not isinstance(port, bool) and 0 < port < 65536 else None


def kb_narrative(finding: Any, asset: Any | None = None) -> dict[str, Any]:
    """The KB's technical details / impact / business impact / exploitation context.

    The reproduction field is the recipe's own re-check ("how to confirm it for yourself"),
    which is what a retest needs; it is not an exploit procedure."""
    criticality = _enum(getattr(asset, "criticality", None)) if asset is not None else None
    content = finding_content(finding, asset_criticality=criticality)
    return {
        "category": content.category,
        "technical_details": content.technical_details,
        "impact": content.impact,
        "business_impact": content.business_impact,
        # Readable text (summary + the honest "not validated" note), not the raw view.
        "exploitation": " ".join(
            t.strip() for t in (content.exploitation.summary, content.exploitation.note) if t
        ),
    }


def first_sentence(text: str | None, limit: int = 240) -> str | None:
    if not text:
        return None
    head = re.split(r"(?<=[.!?])\s", text.strip(), maxsplit=1)[0]
    return head if len(head) <= limit else head[: limit - 1].rstrip() + "…"


def description_is_rule_metadata(finding: Any) -> bool:
    desc = str(getattr(finding, "description", "") or "").strip()
    if not desc:
        return False
    ev = _evidence(finding)
    if not str(ev.get("rule_id") or "").startswith("POSTURE-"):
        return False
    fp = str(ev.get("fp_notes") or "").strip()
    return bool(_METADATA_LEAD.match(desc) or (fp and fp in desc))


def detection_rationale(finding: Any) -> str | None:
    """Why the platform flagged this: the rule, what evidence it rested on, and the rule's
    own false-positive caveat. This is the text that used to occupy the Description."""
    ev = _evidence(finding)
    rule_id = ev.get("rule_id")
    parts: list[str] = []
    if rule_id:
        parts.append(f"Rule {rule_id}")
    basis = ev.get("evidence_basis") or (
        ev.get("evidence", {}).get("evidence_basis") if isinstance(ev.get("evidence"), dict) else None)
    if basis:
        parts.append("based on " + _BASIS_LABEL.get(str(basis), str(basis).replace("_", " ")))
    if ev.get("scanner"):
        parts.append(f"observed by {ev['scanner']}")
    head = ", ".join(parts)
    note = str(ev.get("fp_notes") or "").strip()
    if head and note:
        return f"{head}. {note}"
    return head or note or None


def fix_plan(finding: Any, asset: Any | None = None) -> dict[str, Any] | None:
    """The rule-keyed remediation recipe rendered for this finding: ordered steps with
    per-OS commands, verification, effort, risk and rollback. Best-effort — a rendering
    failure must never break the report."""
    try:
        from app.remediation.context import build_context
        from app.remediation.plan import build_plan
        ctx = build_context(finding, asset)
        plan = build_plan(finding, ctx)
    except Exception as exc:  # noqa: BLE001
        logger.warning("report.fix_plan_failed", finding_id=str(getattr(finding, "id", "")),
                       error=str(exc))
        return None
    return plan


def plan_text(plan: dict[str, Any] | None) -> str:
    """The plan as plain ordered text, for exports that cannot carry structure."""
    if not plan:
        return ""
    lines = [str(plan.get("title") or plan.get("summary") or "").strip()]
    for step in plan.get("steps") or []:
        n, title = step.get("step"), step.get("title")
        tier = step.get("tier")
        lines.append(f"{n}. [{tier}] {title}" if tier else f"{n}. {title}")
    check = plan.get("verification_check") or {}
    if check.get("check"):
        lines.append(f"Verify: {check['check']} — expected: {check.get('expected', '')}".rstrip())
    return "\n".join(l for l in lines if l)


__all__ = ["service_port", "SOURCE_RECORDED", "SOURCE_KB", "kb_narrative", "first_sentence",
           "description_is_rule_metadata", "detection_rationale", "fix_plan", "plan_text",
           "content_category"]

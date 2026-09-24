"""
compliance_brief.py — what a finding means for the customer's regulators.

Two layers, deliberately separate:
  * ``finding_compliance_view`` — DETERMINISTIC: the regional obligations the
    packs map to this finding (+ reporting clocks), no model involved.
  * ``generate_compliance_brief`` — the sector domain expert narrates those
    obligations for a compliance/risk audience. The model receives only a
    whitelisted finding view plus the deterministic obligations, is told to
    cite nothing else, and its citations are checked afterwards. If the model
    is unavailable the deterministic obligations are still returned.
"""
from __future__ import annotations

from typing import Any

from sqlalchemy import select

from app.ai.audit_chain import persist_ai_calls
from app.compliance.citations import check_citations
from app.compliance.profile import profile_from_roe
from app.compliance.registry import finding_obligations
from app.intel.tagging import tag_strings
from app.models.asset import Asset
from app.schemas.ai import AiGenerateRequest, AiMessage
from app.services.domain_context import domain_brief_for
from app.services.llm import AiRuntimeError, ManagerLlmService


async def finding_compliance_view(db, finding, engagement) -> dict[str, Any]:
    tags: set[str] = set()
    if getattr(finding, "asset_id", None) is not None:
        asset_tags = (await db.execute(
            select(Asset.tags).where(Asset.id == finding.asset_id)
        )).scalar_one_or_none()
        tags = set(tag_strings(asset_tags))
    out = finding_obligations(finding, profile_from_roe(engagement.rules_of_engagement), tags)
    out["asset_tags"] = sorted(tags)
    return out


def _finding_view(finding) -> dict[str, Any]:
    """Whitelist only — raw evidence (banners, hostnames) never reaches the model."""
    severity = getattr(finding, "severity", None)
    return {
        "title": finding.title,
        "severity": getattr(severity, "value", severity),
        "cvss_score": float(finding.cvss_score) if getattr(finding, "cvss_score", None) is not None else None,
        "risk_score": getattr(finding, "risk_score", None),
        "cve_ids": list(getattr(finding, "cve_ids", None) or []),
        "remediation": getattr(finding, "remediation", None),
    }


def _compact_obligations(view: dict[str, Any]) -> dict[str, Any]:
    return {
        "category": view["category"],
        "frameworks": [{"framework": f["framework"], "authority": f["authority"],
                        "controls": f["controls"], "rationale": f["rationale"]}
                       for f in view["frameworks"]],
        "reporting": [{"authority": r["authority"], "deadline_hours": r["deadline_hours"],
                       "trigger": r["trigger"]} for r in view["reporting"]],
    }


async def generate_compliance_brief(db, finding, engagement, *, actor_id) -> dict[str, Any]:
    view = await finding_compliance_view(db, finding, engagement)
    brief = await domain_brief_for(db, engagement, [finding])
    request = AiGenerateRequest(
        task="compliance_brief",
        messages=[AiMessage(role="user", content="Write the compliance impact brief for this finding.")],
        context={"finding": _finding_view(finding), "obligations": _compact_obligations(view)},
        max_tokens=900,
    )
    svc = ManagerLlmService()
    result: dict[str, Any] = {
        "obligations": view, "content": None, "error": None,
        "skill": brief.skill_id if brief else None,
        "skill_label": brief.skill_label if brief else None,
        "jurisdictions": brief.jurisdictions if brief else [],
        "unverified_citations": [], "provider": None, "model": None,
    }
    try:
        content, runtime, _fallback = await svc.generate_with_fallback(
            request, domain_brief=brief.text if brief else None)
    except AiRuntimeError as exc:
        result["error"] = str(exc)
        return result
    await persist_ai_calls(db, list(getattr(svc, "audit_records", None) or []),
                           actor_id=actor_id, engagement_id=engagement.id)
    result.update(content=content, provider=runtime.provider, model=runtime.model,
                  unverified_citations=check_citations(content)["unverified"])
    return result

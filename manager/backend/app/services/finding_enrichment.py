"""finding_enrichment.py — assemble the per-finding detail content for the API.

Thin orchestration over the three pure services — ``finding_content`` (explanation,
business impact, exploitation), ``finding_compliance`` (five-framework mapping) and
``evidence_summary`` (evidence-as-facts) — into the exact field dict the detail
endpoint merges onto ``FindingOut``. Kept separate from the router so it is pure and
unit-testable with a plain object, and separate from the individual services so each
of those keeps a single responsibility.
"""
from __future__ import annotations

from typing import Any

from app.services.evidence_summary import summarize_evidence
from app.services.finding_compliance import compliance_for
from app.services.finding_content import finding_content


def detail_enrichment(finding: Any, asset_criticality: str | None = None) -> dict[str, Any]:
    """Return the heavy detail-only enrichment fields for one finding.

    Honours ``finding.content_overrides`` (persisted AI/analyst prose) via the
    content KB, scales business impact by ``asset_criticality``, and always returns
    a fully-populated dict — every finding gets content, evidence facts, and all
    five compliance frameworks.
    """
    raw_overrides = getattr(finding, "content_overrides", None)
    overrides = raw_overrides if isinstance(raw_overrides, dict) else None

    content = finding_content(
        finding, asset_criticality=asset_criticality, overrides=overrides
    ).to_dict()

    return {
        "technical_details": content["technical_details"],
        "impact": content["impact"],
        "business_impact": content["business_impact"],
        "exploitation": content["exploitation"],
        "exploit_maturity": content["exploit_maturity"],
        "actively_exploited": content["actively_exploited"],
        "evidence_summary": summarize_evidence(getattr(finding, "evidence", None)),
        "compliance": compliance_for(finding),
    }

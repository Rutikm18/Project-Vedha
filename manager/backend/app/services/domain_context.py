"""
domain_context.py — the DB-facing half of the domain-expert AI: load an
engagement's profile + estate tags and build its domain brief.

Fail-soft by design: the brief improves answers but is never required for one,
so any lookup problem degrades to the plain assistant rather than an error.
"""
from __future__ import annotations

import uuid
from typing import Iterable

import structlog
from sqlalchemy import select

from app.ai.domain_brief import DomainBrief, build_domain_brief
from app.compliance.profile import profile_from_roe
from app.intel.tagging import tag_strings
from app.models.asset import Asset

logger = structlog.get_logger()


async def engagement_tag_set(db, engagement_id: uuid.UUID) -> set[str]:
    """Union of every asset's tags in the engagement (one query)."""
    rows = (await db.execute(
        select(Asset.tags).where(Asset.engagement_id == engagement_id, Asset.tags.isnot(None))
    )).scalars().all()
    out: set[str] = set()
    for tags in rows:
        out.update(tag_strings(tags))
    return out


async def domain_brief_for(db, engagement, findings: Iterable = ()) -> DomainBrief | None:
    """The brief for this engagement, shaped to the findings under discussion.
    None when anything goes wrong — callers then run without a brief."""
    from app.services.remediation_kb import classify_finding
    try:
        tags = await engagement_tag_set(db, engagement.id)
        categories = {classify_finding(f) for f in findings if f is not None}
        return build_domain_brief(
            profile_from_roe(getattr(engagement, "rules_of_engagement", None)), tags, categories)
    except Exception as exc:  # noqa: BLE001 — the brief is advisory
        logger.warning("ai.domain_brief_failed", engagement=str(getattr(engagement, "id", None)),
                       error=str(exc))
        return None

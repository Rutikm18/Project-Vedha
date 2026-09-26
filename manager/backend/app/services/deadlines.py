"""
deadlines.py — the single remediation due-date resolver.

Resolution order (first match wins):
  1. an APPROVED extension     → findings.due_at            (source "extension")
  2. the engagement's policy   → rules_of_engagement["sla_policy"] ("engagement")
  3. the tenant's policy       → sla_policies row           ("tenant")
  4. the environment defaults  → settings.sla_hours_*       ("default")

Plans, bundles, the report, the tracker and the SLA dashboard all read from here
(``services/sla.py`` honours ``due_at`` too), so a finding never shows two
different due dates on two screens.
"""
from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.sla_policy import SlaPolicy
from app.services import sla

SEVERITIES = ("critical", "high", "medium", "low", "info")
MAX_HOURS = 8760


def _valid_hours(v: Any) -> bool:
    return isinstance(v, int) and not isinstance(v, bool) and 0 <= v <= MAX_HOURS


def engagement_windows(engagement: Any) -> dict[str, int] | None:
    """The engagement's own SLA windows, or None when unset/invalid. An invalid
    stored policy is ignored (falls through to the tenant) rather than raising."""
    roe = getattr(engagement, "rules_of_engagement", None)
    if not isinstance(roe, dict):
        return None
    policy = roe.get("sla_policy")
    if not isinstance(policy, dict):
        return None
    out: dict[str, int] = {}
    for sev in SEVERITIES:
        v = policy.get(f"{sev}_hours")
        if not _valid_hours(v):
            return None
        out[sev] = v
    return out


def _row_windows(row: SlaPolicy) -> dict[str, int]:
    return {"critical": row.critical_hours, "high": row.high_hours, "medium": row.medium_hours,
            "low": row.low_hours, "info": row.info_hours}


async def tenant_windows(db: AsyncSession, tenant_id: uuid.UUID) -> dict[str, int] | None:
    row = (await db.execute(
        select(SlaPolicy).where(SlaPolicy.tenant_id == tenant_id)
    )).scalar_one_or_none()
    return _row_windows(row) if row is not None else None


async def windows_for(db: AsyncSession, tenant_id: uuid.UUID,
                      engagement: Any | None) -> tuple[dict[str, int], str]:
    """(windows, source) for one engagement: engagement → tenant → default."""
    if engagement is not None:
        own = engagement_windows(engagement)
        if own is not None:
            return own, "engagement"
    tenant = await tenant_windows(db, tenant_id)
    if tenant is not None:
        return tenant, "tenant"
    return sla.default_windows(), "default"


def due_for(finding: Any, windows: dict[str, int], source: str) -> dict[str, Any]:
    """``{"at": datetime | None, "source": str | None}`` for one finding. Closed or
    untracked findings (window 0, no start time) have no due date."""
    result = sla.compute(finding, windows=windows)
    if result.deadline is None:
        return {"at": None, "source": None}
    if getattr(finding, "due_at", None) is not None:
        return {"at": result.deadline, "source": "extension"}
    return {"at": result.deadline, "source": source}


def iso(value: datetime | None) -> str | None:
    return value.isoformat() if isinstance(value, datetime) else None

"""
fragile_guard.py — the DB-facing half of the fragile-asset guard (policy lives in
app/intel/fragile.py). One query per job: the engagement's tagged asset rows.
"""
from __future__ import annotations

import uuid

from sqlalchemy import select

from app.intel.fragile import FragileHost, FragilePlan, fragile_exclusions, fragile_hosts, is_gentle
from app.models.asset import Asset

OVERRIDE_ROLES = ("admin", "manager")
MIN_REASON_CHARS = 10


async def load_fragile_hosts(db, engagement_id: uuid.UUID) -> list[FragileHost]:
    rows = (await db.execute(
        select(Asset.ip_address, Asset.tags).where(
            Asset.engagement_id == engagement_id, Asset.tags.isnot(None))
    )).all()
    return fragile_hosts((row[0], row[1]) for row in rows)


async def plan_for_job(db, engagement_id: uuid.UUID, *, scan_type: str | None,
                       intensity: str | None, job_scope: list[str]) -> FragilePlan | None:
    """The exclusions a job needs, or None when it is gentle / touches no fragile host."""
    if is_gentle(scan_type, intensity):
        return None
    hosts = await load_fragile_hosts(db, engagement_id)
    if not hosts:
        return None
    plan = fragile_exclusions(hosts, job_scope)
    return plan if plan.cidrs else None


def merge_excluded(existing: list[str] | None, extra: list[str]) -> list[str]:
    return list(dict.fromkeys([*(existing or []), *extra]))


def filter_targets(targets: list[str], hosts: list[FragileHost]) -> tuple[list[str], list[dict]]:
    """For manager-side scanners that take a concrete IP list (Nuclei, Nessus)."""
    fragile = {h.ip: h.reasons for h in hosts}
    kept = [t for t in targets if t not in fragile]
    skipped = [{"ip": t, "reasons": fragile[t]} for t in targets if t in fragile]
    return kept, skipped

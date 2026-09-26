"""
service.py — engagement-level remediation: bundles with live due dates.

Shared by the operator routes, the customer portal, the report and the tracker
export so every surface shows the same bundles, refs and due dates. Query cost
is fixed: findings, assets, services (3) + the tenant SLA policy (≤ 1).
"""
from __future__ import annotations

import uuid
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.remediation.bundles import build_bundles, by_host
from app.remediation.loader import load_engagement_items
from app.services.deadlines import due_for, windows_for
from app.services.project_time import project_now


async def engagement_bundles(db: AsyncSession, engagement: Any, tenant_id: uuid.UUID) -> dict:
    """``{"bundles": [...], "sla_source": str, "items": [(finding, ctx, due)]}``."""
    items = await load_engagement_items(db, engagement.id)
    windows, source = await windows_for(db, tenant_id, engagement)
    triples = [(f, ctx, due_for(f, windows, source)) for f, ctx in items]
    bundles = build_bundles(triples, now=project_now())
    return {"bundles": bundles, "sla_source": source, "items": triples}


def summarize(bundles: list[dict]) -> dict:
    open_b = [b for b in bundles if b["status"] == "open"]
    return {
        "bundles": len(bundles),
        "open_bundles": len(open_b),
        "done_bundles": len(bundles) - len(open_b),
        "open_findings": sum(b["open_count"] for b in bundles),
        "closed_findings": sum(b["closed_count"] for b in bundles),
        "hosts": len({h["ip"] for b in bundles for h in b["hosts"]}),
        "act": sum(1 for b in open_b if b["urgency"] == "act"),
    }


def view_payload(bundles: list[dict], view: str, sla_source: str) -> dict:
    payload: dict[str, Any] = {"view": view, "sla_source": sla_source, "summary": summarize(bundles),
                               "generated_at": project_now().isoformat()}
    if view == "host":
        payload["hosts"] = by_host(bundles)
    else:
        payload["bundles"] = bundles
    return payload


def find_bundle(bundles: list[dict], fix_key: str) -> dict | None:
    return next((b for b in bundles if b["fix_key"] == fix_key), None)

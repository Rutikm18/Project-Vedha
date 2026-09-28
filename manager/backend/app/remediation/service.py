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


async def engagement_bundles(db: AsyncSession, engagement: Any, tenant_id: uuid.UUID,
                             finding_ids: set[uuid.UUID] | None = None) -> dict:
    """``{"bundles": [...], "sla_source": str, "items": [(finding, ctx, due)]}``.

    ``finding_ids`` restricts everything — bundles, host rows, counts — to those
    findings (a filtered report export). None means the whole engagement."""
    items = await load_engagement_items(db, engagement.id)
    if finding_ids is not None:
        items = [(f, ctx) for f, ctx in items if f.id in finding_ids]
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


async def export_tracker(db: AsyncSession, engagement: Any, tenant_id: uuid.UUID, fmt: str,
                         sheet: str | None = None,
                         finding_ids: set[uuid.UUID] | None = None) -> tuple[bytes, str, str]:
    """(content, media_type, filename) for the XLSX/CSV remediation tracker.

    ``sheet`` (a key of export.SHEET_KEYS) with fmt="csv" returns that one sheet
    as a plain .csv instead of the three-sheet zip — the Reports page's
    "CSV" download is the findings register, not an archive."""
    import re as _re

    from sqlalchemy import select

    from app.models.deadline_extension import DeadlineExtensionRequest
    from app.remediation.export import SHEET_KEYS, build_rows, to_csv, to_csv_zip, to_xlsx
    from app.services.project_time import project_file_stamp

    data = await engagement_bundles(db, engagement, tenant_id, finding_ids)
    extensions = list((await db.execute(
        select(DeadlineExtensionRequest).where(DeadlineExtensionRequest.engagement_id == engagement.id)
    )).scalars().all())
    sheets = build_rows(data["bundles"], data["items"], extensions)
    slug = _re.sub(r"[^A-Za-z0-9]+", "-", str(getattr(engagement, "name", "engagement"))).strip("-")[:40] or "engagement"
    stem = f"vedha-remediation-{slug}-{project_file_stamp()}"
    if fmt == "csv" and sheet in SHEET_KEYS:
        kind = "findings" if sheet == "findings" else f"remediation-{sheet.replace('_', '-')}"
        return (to_csv(sheets, SHEET_KEYS[sheet]), "text/csv; charset=utf-8",
                f"vedha-{kind}-{slug}-{project_file_stamp()}.csv")
    if fmt == "csv":
        return to_csv_zip(sheets), "application/zip", f"{stem}.zip"
    return (to_xlsx(sheets, title=f"Remediation tracker — {getattr(engagement, 'name', '')}"),
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", f"{stem}.xlsx")

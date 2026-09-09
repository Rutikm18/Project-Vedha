"""Shared finding commands for operator and customer engagement workspaces."""
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.detection.resolution import apply_manual_reopen
from app.models.asset import Asset
from app.models.engagement import Engagement
from app.models.enums import FindingStatus
from app.models.finding import Finding
from app.schemas.finding import FindingPatch
from app.services import finding_events
from app.services.audit import record_audit


def _event_detail(origin: str, detail: dict[str, object]) -> dict[str, object]:
    """Keep the established manager timeline contract; identify portal actions."""
    if origin == "manager":
        return detail
    return {"origin": origin, **detail}


async def get_finding_for_action(
    db: AsyncSession,
    finding_id: uuid.UUID,
    *,
    tenant_id: uuid.UUID,
    engagement_id: uuid.UUID | None = None,
) -> Finding:
    query = (
        select(Finding)
        .join(Engagement, Finding.engagement_id == Engagement.id)
        .where(Finding.id == finding_id, Engagement.tenant_id == tenant_id)
    )
    if engagement_id is not None:
        query = query.where(Finding.engagement_id == engagement_id)
    finding = (await db.execute(query.with_for_update())).scalar_one_or_none()
    if finding is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Finding not found")
    return finding


async def patch_finding(
    db: AsyncSession,
    finding: Finding,
    body: FindingPatch,
    *,
    actor_id: uuid.UUID,
    actor_type: str,
    origin: str,
) -> Finding:
    patch = body.model_dump(exclude_unset=True)
    changed_fields = [field for field in patch if field != "action_reason"]
    action_reason = patch.pop("action_reason", None)
    actor = str(actor_id)
    previous_status = finding.status
    previous_cvss = finding.cvss_score
    previous_risk = finding.risk_score
    target_status = patch.get("status")

    if target_status is None:
        patch.pop("status", None)
    elif target_status == FindingStatus.remediated and previous_status != FindingStatus.remediated:
        finding.resolved_at = datetime.now(timezone.utc)
        finding.resolution_method = "manual"
        finding.resolution_run_id = None
    elif target_status == FindingStatus.open and previous_status == FindingStatus.remediated:
        apply_manual_reopen(finding, by=actor, now=datetime.now(timezone.utc))

    if "notes" in patch:
        note = patch.pop("notes")
        if note:
            await finding_events.record_event(
                db, finding, "note", actor=actor, actor_type=actor_type,
                detail=_event_detail(origin, {"note": note}),
            )

    if "owner" in patch:
        owner = patch.pop("owner")
        if finding.asset_id is not None:
            asset = (await db.execute(
                select(Asset).where(
                    Asset.id == finding.asset_id,
                    Asset.engagement_id == finding.engagement_id,
                ).with_for_update()
            )).scalar_one_or_none()
            if asset is not None:
                asset.owner = owner

    for field, value in patch.items():
        setattr(finding, field, value)

    if "status" in patch and patch["status"] != previous_status:
        detail: dict[str, object] = {}
        if action_reason:
            detail["reason"] = action_reason
        if finding.status == FindingStatus.remediated:
            detail["resolution_method"] = "manual"
        if finding.status == FindingStatus.open and previous_status == FindingStatus.remediated:
            detail["reopened_count"] = finding.reopened_count
        await finding_events.record_event(
            db, finding, finding_events.event_type_for_status(finding.status),
            actor=actor, actor_type=actor_type,
            from_status=previous_status, to_status=finding.status,
            detail=_event_detail(origin, detail),
        )

    if ("cvss_score" in patch and finding.cvss_score != previous_cvss) or (
        "risk_score" in patch and finding.risk_score != previous_risk
    ):
        await finding_events.record_event(
            db, finding, "risk_changed", actor=actor, actor_type=actor_type,
            detail=_event_detail(origin, {
                "cvss_from": float(previous_cvss) if previous_cvss is not None else None,
                "cvss_to": float(finding.cvss_score) if finding.cvss_score is not None else None,
                "risk_from": float(previous_risk) if previous_risk is not None else None,
                "risk_to": float(finding.risk_score) if finding.risk_score is not None else None,
            }),
        )

    record_audit(
        db,
        actor_id=actor_id,
        action="finding.updated",
        engagement_id=getattr(finding, "engagement_id", None),
        resource_type="finding",
        resource_id=finding.id,
        detail={
            "origin": origin,
            "actor_type": actor_type,
            "changed_fields": changed_fields,
            "status_from": getattr(previous_status, "value", previous_status),
            "status_to": getattr(finding.status, "value", finding.status),
            "reason": action_reason,
        },
    )
    await db.flush()
    await db.refresh(finding)
    return finding


async def reopen_finding(
    db: AsyncSession,
    finding: Finding,
    *,
    actor_id: uuid.UUID,
    actor_type: str,
    origin: str,
    reason: str | None = None,
) -> Finding:
    if finding.status != FindingStatus.remediated:
        raise HTTPException(status.HTTP_409_CONFLICT, "Only a remediated finding can be reopened")

    apply_manual_reopen(finding, by=str(actor_id), now=datetime.now(timezone.utc))
    detail: dict[str, object] = {"reopened_count": finding.reopened_count}
    if reason:
        detail["reason"] = reason
    await finding_events.record_event(
        db, finding, "reopened", actor=str(actor_id), actor_type=actor_type,
        from_status=FindingStatus.remediated, to_status=FindingStatus.open,
        detail=_event_detail(origin, detail),
    )
    record_audit(
        db,
        actor_id=actor_id,
        action="finding.reopened",
        engagement_id=getattr(finding, "engagement_id", None),
        resource_type="finding",
        resource_id=finding.id,
        detail={"origin": origin, "actor_type": actor_type, "reason": reason},
    )
    await db.flush()
    await db.refresh(finding)
    return finding

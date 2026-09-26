"""
extensions.py — customer deadline-extension requests with operator approval.

Rules (spec §4.5):
  * the subject (a finding or a fix bundle) must be inside the requester's
    engagement and have OPEN findings; members are snapshotted at request time
  * the requested date must be later than the current due date
  * a compensating control is mandatory when any member is critical/high or on
    the CISA KEV list
  * one pending request per subject
  * an operator decides with a note; approval may grant a different date
  * only pending requests can be decided or withdrawn
Every transition writes an event on each member finding's timeline plus an
audit_logs row. Approval sets ``findings.due_at`` (source "extension"), which
services/deadlines.py and services/sla.py already honour everywhere.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.deadline_extension import DeadlineExtensionRequest
from app.models.enums import FindingStatus
from app.remediation import service as remediation_service
from app.remediation.bundles import fix_ref
from app.services import finding_events
from app.services.audit import record_audit
from app.services.deadlines import due_for, windows_for

_OPEN = (FindingStatus.open, FindingStatus.confirmed)
_SERIOUS = {"critical", "high"}


def _enum(v: Any) -> Any:
    return getattr(v, "value", v)


def _kev(finding: Any) -> bool:
    ev = getattr(finding, "evidence", None)
    ev = ev if isinstance(ev, dict) else {}
    return bool(ev.get("kev") or ev.get("kev_listed") or ev.get("actively_exploited"))


def _aware(dt: datetime | None) -> datetime | None:
    if dt is not None and dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt


async def _members(db: AsyncSession, engagement: Any, tenant_id: uuid.UUID, *, subject_type: str,
                   finding_id: uuid.UUID | None, fix_key: str | None) -> tuple[list[Any], datetime | None]:
    """(open member findings, current due date = the earliest among them)."""
    if subject_type == "finding":
        from app.models.finding import Finding
        finding = (await db.execute(
            select(Finding).where(Finding.id == finding_id, Finding.engagement_id == engagement.id)
        )).scalar_one_or_none()
        if finding is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Finding not found")
        if finding.status not in _OPEN:
            raise HTTPException(status.HTTP_409_CONFLICT, "Only an open finding can be extended")
        windows, source = await windows_for(db, tenant_id, engagement)
        return [finding], _aware(due_for(finding, windows, source)["at"])

    data = await remediation_service.engagement_bundles(db, engagement, tenant_id)
    bundle = remediation_service.find_bundle(data["bundles"], fix_key or "")
    if bundle is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Bundle not found")
    wanted = set(bundle["open_finding_ids"])
    if not wanted:
        raise HTTPException(status.HTTP_409_CONFLICT, "This bundle has no open findings")
    members = [f for f, _ctx, _due in data["items"] if str(f.id) in wanted]
    return members, _aware(bundle["due_at"])


async def _pending_exists(db: AsyncSession, engagement_id: uuid.UUID, subject_type: str,
                          finding_id: uuid.UUID | None, fix_key: str | None) -> bool:
    q = select(DeadlineExtensionRequest.id).where(
        DeadlineExtensionRequest.engagement_id == engagement_id,
        DeadlineExtensionRequest.status == "pending",
        DeadlineExtensionRequest.subject_type == subject_type,
    )
    q = q.where(DeadlineExtensionRequest.finding_id == finding_id) if subject_type == "finding" \
        else q.where(DeadlineExtensionRequest.fix_key == fix_key)
    return (await db.execute(q)).scalar_one_or_none() is not None


async def create_request(db: AsyncSession, *, engagement: Any, user: Any, subject_type: str,
                         finding_id: uuid.UUID | None, fix_key: str | None, requested_due_at: datetime,
                         reason: str, compensating_control: str | None) -> DeadlineExtensionRequest:
    members, current_due = await _members(db, engagement, user.tenant_id, subject_type=subject_type,
                                          finding_id=finding_id, fix_key=fix_key)
    if current_due is not None and requested_due_at <= current_due:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY,
                            "The requested date must be later than the current due date "
                            f"({current_due.isoformat()})")
    if requested_due_at <= datetime.now(timezone.utc):
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "The requested date must be in the future")
    serious = any(str(_enum(f.severity)).lower() in _SERIOUS or _kev(f) for f in members)
    if serious and not (compensating_control or "").strip():
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY,
                            "A compensating control is required for critical, high or "
                            "known-exploited findings")
    if await _pending_exists(db, engagement.id, subject_type, finding_id, fix_key):
        raise HTTPException(status.HTTP_409_CONFLICT, "A request for this item is already pending")

    req = DeadlineExtensionRequest(
        id=uuid.uuid4(), tenant_id=user.tenant_id, engagement_id=engagement.id,
        subject_type=subject_type, finding_id=finding_id if subject_type == "finding" else None,
        fix_key=fix_key if subject_type == "bundle" else None,
        member_finding_ids=[f.id for f in members], current_due_at=current_due,
        requested_due_at=requested_due_at, reason=reason.strip(),
        compensating_control=(compensating_control or "").strip() or None,
        status="pending", requested_by=user.user_id, requested_at=datetime.now(timezone.utc),
    )
    db.add(req)
    detail = {"request_id": str(req.id), "subject_type": subject_type,
              "fix_ref": fix_ref(fix_key) if fix_key else None,
              "current_due_at": current_due.isoformat() if current_due else None,
              "requested_due_at": requested_due_at.isoformat(), "reason": req.reason,
              "compensating_control": req.compensating_control, "origin": "portal"}
    for f in members:
        await finding_events.record_event(db, f, "extension_requested", actor=str(user.user_id),
                                          actor_type="customer", detail=detail)
    record_audit(db, actor_id=user.user_id, action="remediation.extension_requested",
                 engagement_id=engagement.id, resource_type="deadline_extension", resource_id=req.id,
                 detail={k: v for k, v in detail.items() if k != "origin"})
    await db.flush()
    return req


async def _findings(db: AsyncSession, ids: list[uuid.UUID], engagement_id: uuid.UUID) -> list[Any]:
    from app.models.finding import Finding
    if not ids:
        return []
    return list((await db.execute(
        select(Finding).where(Finding.id.in_(ids), Finding.engagement_id == engagement_id)
    )).scalars().all())


async def decide(db: AsyncSession, *, request: DeadlineExtensionRequest, operator: Any, approve: bool,
                 note: str, due_at: datetime | None = None) -> DeadlineExtensionRequest:
    if request.status != "pending":
        raise HTTPException(status.HTTP_409_CONFLICT, f"This request is already {request.status}")
    granted = due_at or request.requested_due_at
    if approve and granted <= datetime.now(timezone.utc):
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "The granted date must be in the future")

    request.status = "approved" if approve else "rejected"
    request.decided_by = operator.user_id
    request.decided_at = datetime.now(timezone.utc)
    request.decision_note = note.strip()
    request.decided_due_at = granted if approve else None

    members = await _findings(db, list(request.member_finding_ids), request.engagement_id)
    event = "extension_approved" if approve else "extension_rejected"
    applied = 0
    for f in members:
        detail = {"request_id": str(request.id), "note": request.decision_note,
                  "requested_due_at": request.requested_due_at.isoformat()}
        if approve and f.status in _OPEN:
            detail["from_due_at"] = _aware(f.due_at).isoformat() if f.due_at else (
                request.current_due_at.isoformat() if request.current_due_at else None)
            detail["to_due_at"] = granted.isoformat()
            f.due_at = granted
            f.due_at_source = "extension"
            applied += 1
        await finding_events.record_event(db, f, event, actor=str(operator.user_id), actor_type="user",
                                          detail=detail)
    record_audit(db, actor_id=operator.user_id, action=f"remediation.{event}",
                 engagement_id=request.engagement_id, resource_type="deadline_extension",
                 resource_id=request.id,
                 detail={"note": request.decision_note, "granted_due_at": granted.isoformat() if approve else None,
                         "applied_to": applied})
    await db.flush()
    return request


async def withdraw(db: AsyncSession, *, request: DeadlineExtensionRequest, user: Any) -> DeadlineExtensionRequest:
    if request.status != "pending":
        raise HTTPException(status.HTTP_409_CONFLICT, f"This request is already {request.status}")
    request.status = "withdrawn"
    request.decided_at = datetime.now(timezone.utc)
    for f in await _findings(db, list(request.member_finding_ids), request.engagement_id):
        await finding_events.record_event(db, f, "extension_withdrawn", actor=str(user.user_id),
                                          actor_type="customer", detail={"request_id": str(request.id)})
    record_audit(db, actor_id=user.user_id, action="remediation.extension_withdrawn",
                 engagement_id=request.engagement_id, resource_type="deadline_extension",
                 resource_id=request.id, detail=None)
    await db.flush()
    return request


def to_out(req: DeadlineExtensionRequest) -> dict:
    from app.schemas.extension import ExtensionOut
    out = ExtensionOut.model_validate(req).model_dump()
    out["fix_ref"] = fix_ref(req.fix_key) if req.fix_key else None
    return out

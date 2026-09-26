"""
extensions.py — operator review of customer deadline-extension requests.

Customers raise requests in the portal (routers/portal.py); operators list them
per engagement and approve (optionally with a different date) or reject, always
with a note. The workflow rules live in services/extensions.py.
"""
from __future__ import annotations

import uuid
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.rbac import require_role
from app.dependencies import DB, AuthUser
from app.models.deadline_extension import DeadlineExtensionRequest
from app.models.engagement import Engagement
from app.schemas.extension import ExtensionDecision
from app.services import extensions as ext

router = APIRouter(tags=["remediation"])
_READER = require_role(["admin", "manager", "tester", "analyst", "auditor"])
_DECIDER = require_role(["admin", "manager"])


async def _request(db: AsyncSession, request_id: uuid.UUID, tenant_id: uuid.UUID) -> DeadlineExtensionRequest:
    req = (await db.execute(
        select(DeadlineExtensionRequest).where(DeadlineExtensionRequest.id == request_id,
                                               DeadlineExtensionRequest.tenant_id == tenant_id)
    )).scalar_one_or_none()
    if req is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Extension request not found")
    return req


@router.get("/engagements/{engagement_id}/extensions", summary="Deadline-extension requests")
async def list_extensions(engagement_id: uuid.UUID, db: DB,
                          current_user: Annotated[AuthUser, _READER],
                          status_filter: str | None = Query(default=None, alias="status",
                                                            pattern="^(pending|approved|rejected|withdrawn)$")):
    eng = (await db.execute(
        select(Engagement.id).where(Engagement.id == engagement_id,
                                    Engagement.tenant_id == current_user.tenant_id)
    )).scalar_one_or_none()
    if eng is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Engagement not found")
    q = select(DeadlineExtensionRequest).where(DeadlineExtensionRequest.engagement_id == engagement_id)
    if status_filter:
        q = q.where(DeadlineExtensionRequest.status == status_filter)
    rows = (await db.execute(q.order_by(DeadlineExtensionRequest.requested_at.desc()))).scalars().all()
    return {"items": [ext.to_out(r) for r in rows]}


@router.post("/extensions/{request_id}/approve", summary="Approve an extension (optionally another date)")
async def approve_extension(request_id: uuid.UUID, body: ExtensionDecision, db: DB,
                            current_user: Annotated[AuthUser, _DECIDER]):
    req = await _request(db, request_id, current_user.tenant_id)
    req = await ext.decide(db, request=req, operator=current_user, approve=True,
                           note=body.note, due_at=body.due_at)
    return ext.to_out(req)


@router.post("/extensions/{request_id}/reject", summary="Reject an extension request")
async def reject_extension(request_id: uuid.UUID, body: ExtensionDecision, db: DB,
                           current_user: Annotated[AuthUser, _DECIDER]):
    req = await _request(db, request_id, current_user.tenant_id)
    req = await ext.decide(db, request=req, operator=current_user, approve=False, note=body.note)
    return ext.to_out(req)

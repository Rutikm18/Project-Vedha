"""
notification_rules.py — operator management of which events notify, and where.

GET returns every event in the catalogue with the tenant's choice (or the default)
and whether the product emits that event yet. PUT stores the choices. Channels
are the tenant's configured integrations (see /integrations); a rule only routes,
it does not configure delivery.
"""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from app.auth.rbac import require_role
from app.dependencies import DB, AuthUser
from app.services.audit import record_audit
from app.services.notification_rules import RuleError, effective_rules, save_rules

router = APIRouter(prefix="/notification-rules", tags=["notification-rules"])
_READ = require_role(["admin", "manager", "tester", "analyst", "auditor"])
_WRITE = require_role(["admin", "manager"])


class RuleIn(BaseModel):
    event: str = Field(..., max_length=48)
    enabled: bool
    channels: list[str] = Field(default_factory=list, max_length=8)


class RulesIn(BaseModel):
    rules: list[RuleIn] = Field(..., max_length=50)


class RuleOut(BaseModel):
    event: str
    label: str
    cadence: str
    enabled: bool
    channels: list[str]
    connected: bool      # False: nothing in the product emits this event yet
    is_custom: bool      # False: the default, never changed by this tenant


@router.get("", response_model=list[RuleOut], summary="Notification rules for the tenant")
async def list_rules(db: DB, current_user: Annotated[AuthUser, _READ]):
    return await effective_rules(db, current_user.tenant_id)


@router.put("", response_model=list[RuleOut], summary="Save notification rules")
async def put_rules(body: RulesIn, db: DB, current_user: Annotated[AuthUser, _WRITE]):
    try:
        out = await save_rules(db, current_user.tenant_id, [r.model_dump() for r in body.rules])
    except RuleError as exc:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, str(exc)) from exc
    record_audit(db, actor_id=current_user.user_id, action="notification_rules.updated",
                 engagement_id=None, resource_type="notification_rules",
                 detail={r.event: {"enabled": r.enabled, "channels": r.channels} for r in body.rules})
    await db.flush()
    return out

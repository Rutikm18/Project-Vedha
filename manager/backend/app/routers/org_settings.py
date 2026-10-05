"""
org_settings.py — read and edit an organisation's policy settings.

  GET/PUT /org-settings/auth               sign-in networks, session length   (admin)
  GET/PUT /org-settings/scan               blackouts, exclusions, override    (admin write; admin/manager read)
  GET/PUT /org-settings/customer-defaults  what a new POC customer starts with (admin write; admin/manager read)

Every change is validated strictly (see services/org_settings) and audited with the
before and after values. Enforcement lives where the rule applies: sign-in and
refresh (auth router), scan enqueue (agents and customer_access routers), and
customer provisioning.
"""
from __future__ import annotations

from typing import Annotated, Any

from fastapi import APIRouter, Body, HTTPException, status
from pydantic import ValidationError

from app.auth.rbac import require_role
from app.dependencies import DB, AuthUser
from app.services import org_settings
from app.services.audit import record_audit

router = APIRouter(prefix="/org-settings", tags=["org-settings"])

_ADMIN = require_role(["admin"])
_READ = require_role(["admin", "manager"])

_WRITERS = {"auth": "admin", "scan": "admin", "customer-defaults": "admin"}


def _section(name: str) -> str:
    if name not in org_settings.SECTIONS:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Unknown settings section '{name}'")
    return name


@router.get("/{section}", summary="An organisation policy section (defaults until edited)")
async def get_settings_section(section: str, db: DB, current_user: Annotated[AuthUser, _READ]):
    name = _section(section)
    if name == "auth" and current_user.role != "admin":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Only an admin can view the authentication policy")
    value = await org_settings.get_section(db, current_user.tenant_id, name)
    return value.model_dump(mode="json")


@router.put("/{section}", summary="Replace an organisation policy section")
async def put_settings_section(
    section: str,
    db: DB,
    current_user: Annotated[AuthUser, _ADMIN],
    body: Annotated[dict[str, Any], Body()],
):
    name = _section(section)
    model = org_settings._MODELS[name]
    try:
        value = model.model_validate(body)
    except ValidationError as exc:
        # Field-level messages the page can show next to the field.
        errors = [{"field": ".".join(str(p) for p in e["loc"]), "message": e["msg"]} for e in exc.errors()]
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, detail=errors) from exc

    before = await org_settings.get_section(db, current_user.tenant_id, name)
    await org_settings.put_section(db, current_user.tenant_id, name, value, actor=str(current_user.user_id))
    record_audit(
        db, actor_id=current_user.user_id, action=f"org_settings.{name}.updated",
        engagement_id=None, resource_type="org_settings",
        detail={"section": name, "before": before.model_dump(mode="json"), "after": value.model_dump(mode="json")},
    )
    await db.flush()
    return value.model_dump(mode="json")

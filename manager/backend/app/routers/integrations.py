"""
integrations.py — operator management of notification integrations (email/Slack/Jira).

Per-tenant, one config per kind. Non-secret fields are stored/returned in `config`;
the secret (SMTP password / Slack webhook / Jira token) is encrypted at rest and
NEVER returned — the API only reports `has_secret`. Operator-only + audited. Actual
delivery (via the outbox) consumes these rows; that wiring is a separate step.
"""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.rbac import require_role
from app.dependencies import DB, AuthUser
from app.models.integration import Integration
from app.services.audit import record_audit
from app.services.credential_crypto import decrypt_credential, encrypt_credential

router = APIRouter(prefix="/integrations", tags=["integrations"])
_OPERATOR = require_role(["admin", "manager"])
_KINDS = {"email", "slack", "jira"}


class IntegrationIn(BaseModel):
    config: dict[str, str] = Field(default_factory=dict)   # non-secret fields
    secret: str | None = None                              # None → keep existing secret
    enabled: bool = True


class IntegrationOut(BaseModel):
    kind: str
    config: dict[str, str]
    has_secret: bool          # the secret value itself is never returned
    enabled: bool


def _out(row: Integration) -> IntegrationOut:
    return IntegrationOut(kind=row.kind, config=dict(row.config or {}),
                          has_secret=bool(row.secret_enc), enabled=row.enabled)


async def _row(db: AsyncSession, tenant_id, kind: str) -> Integration | None:
    return (await db.execute(
        select(Integration).where(Integration.tenant_id == tenant_id, Integration.kind == kind)
    )).scalar_one_or_none()


@router.get("", response_model=list[IntegrationOut],
            summary="List the tenant's configured integrations (secrets masked)")
async def list_integrations(db: DB, current_user: Annotated[AuthUser, _OPERATOR]):
    rows = (await db.execute(
        select(Integration).where(Integration.tenant_id == current_user.tenant_id)
    )).scalars().all()
    return [_out(r) for r in rows]


@router.put("/{kind}", response_model=IntegrationOut,
            summary="Add or update an integration (email|slack|jira)")
async def put_integration(kind: str, body: IntegrationIn, db: DB,
                          current_user: Annotated[AuthUser, _OPERATOR]):
    if kind not in _KINDS:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY,
                            f"Unknown integration kind '{kind}'")
    row = await _row(db, current_user.tenant_id, kind)
    if row is None:
        row = Integration(
            tenant_id=current_user.tenant_id, kind=kind, config=body.config,
            enabled=body.enabled,
            secret_enc=encrypt_credential(body.secret) if body.secret else None,
        )
        db.add(row)
    else:
        row.config = body.config
        row.enabled = body.enabled
        if body.secret:                       # only replace the secret when a new one is given
            row.secret_enc = encrypt_credential(body.secret)
    await db.flush()
    record_audit(db, actor_id=current_user.user_id, action="integration.updated",
                 engagement_id=None, resource_type="integration", resource_id=row.id,
                 detail={"kind": kind, "enabled": body.enabled})
    await db.flush()
    return _out(row)


@router.delete("/{kind}", status_code=status.HTTP_204_NO_CONTENT,
               summary="Remove an integration")
async def delete_integration(kind: str, db: DB,
                             current_user: Annotated[AuthUser, _OPERATOR]):
    row = await _row(db, current_user.tenant_id, kind)
    if row is not None:
        await db.delete(row)
        record_audit(db, actor_id=current_user.user_id, action="integration.deleted",
                     engagement_id=None, resource_type="integration", resource_id=row.id,
                     detail={"kind": kind})
        await db.flush()


def integration_secret(row: Integration) -> str | None:
    """Decrypt an integration's secret for the delivery worker (never the API)."""
    return decrypt_credential(row.secret_enc)

"""Tenant user management — list and deactivate operator accounts.

Exposed endpoints:
  GET  /users          — list all non-client users in the tenant
  GET  /users/{id}     — single user detail
  POST /users/{id}/deactivate  — soft-disable (admin only)
  POST /users/{id}/activate    — re-enable  (admin only)
"""
from __future__ import annotations

import uuid
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select

from app.auth.rbac import require_role
from app.dependencies import DB, AuthUser
from app.models.enums import UserRole
from app.models.user import User

router = APIRouter(prefix="/users", tags=["users"])

_OPERATORS = require_role(["admin", "manager", "analyst", "tester"])
_ADMINS    = require_role(["admin"])


class UserOut(BaseModel):
    id: uuid.UUID
    email: str
    role: str
    is_active: bool
    mfa_enabled: bool
    created_at: datetime
    password_expires_at: datetime | None = None

    model_config = {"from_attributes": True}


def _out(u: User) -> UserOut:
    return UserOut(
        id=u.id,
        email=u.email,
        role=u.role.value if hasattr(u.role, "value") else str(u.role),
        is_active=u.is_active,
        mfa_enabled=u.mfa_enabled,
        created_at=u.created_at,
        password_expires_at=u.password_expires_at,
    )


@router.get("", response_model=list[UserOut], summary="List operator users in this tenant")
async def list_users(
    db: DB,
    current_user: Annotated[AuthUser, _OPERATORS],
) -> list[UserOut]:
    rows = (
        await db.execute(
            select(User)
            .where(
                User.tenant_id == current_user.tenant_id,
                User.role != UserRole.client,
            )
            .order_by(User.created_at)
        )
    ).scalars().all()
    return [_out(r) for r in rows]


@router.get("/{user_id}", response_model=UserOut, summary="Get a single operator user")
async def get_user(
    user_id: uuid.UUID,
    db: DB,
    current_user: Annotated[AuthUser, _OPERATORS],
) -> UserOut:
    row = (
        await db.execute(
            select(User).where(
                User.id == user_id,
                User.tenant_id == current_user.tenant_id,
            )
        )
    ).scalar_one_or_none()
    if not row:
        raise HTTPException(status_code=404, detail="User not found")
    return _out(row)


@router.post("/{user_id}/deactivate", summary="Soft-disable a user (admin only)")
async def deactivate_user(
    user_id: uuid.UUID,
    db: DB,
    current_user: Annotated[AuthUser, _ADMINS],
):
    if user_id == current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot deactivate your own account.",
        )
    row = (
        await db.execute(
            select(User).where(
                User.id == user_id,
                User.tenant_id == current_user.tenant_id,
            )
        )
    ).scalar_one_or_none()
    if not row:
        raise HTTPException(status_code=404, detail="User not found")
    row.is_active = False
    await db.flush()
    return {"ok": True, "user_id": str(user_id), "is_active": False}


@router.post("/{user_id}/activate", summary="Re-enable a deactivated user (admin only)")
async def activate_user(
    user_id: uuid.UUID,
    db: DB,
    current_user: Annotated[AuthUser, _ADMINS],
):
    row = (
        await db.execute(
            select(User).where(
                User.id == user_id,
                User.tenant_id == current_user.tenant_id,
            )
        )
    ).scalar_one_or_none()
    if not row:
        raise HTTPException(status_code=404, detail="User not found")
    row.is_active = True
    await db.flush()
    return {"ok": True, "user_id": str(user_id), "is_active": True}

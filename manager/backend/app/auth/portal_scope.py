"""
portal_scope.py — the customer-portal authorization boundary.

Every customer-portal request is scoped to the ONE engagement bound to the client
login (User.client_engagement_id, carried in the JWT). This module centralizes
that enforcement so it can never be forgotten on a new route:

  * assert_client(user)            — role gate + must be bound to an engagement
  * resolve_scope(user, wanted)    — the bound engagement id, rejecting any
                                     caller-supplied engagement_id that isn't theirs
                                     (the IDOR-defense primitive for any future
                                     route that accepts ?engagement_id)
  * client_scoped(stmt, user, col) — apply the engagement filter to a SELECT

The pure functions are unit-tested directly; the FastAPI dependencies wrap them.
"""
from __future__ import annotations

import uuid
from typing import Annotated

from fastapi import Depends, HTTPException, Query, status
from sqlalchemy import ColumnElement, Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.engagement import Engagement
from app.models.enums import UserRole
from app.models.user import User
from app.schemas.auth import CurrentUser

CLIENT_ROLE = "client"


def assert_client(user: CurrentUser) -> uuid.UUID:
    """Return the client's bound engagement id, or 403.

    403 (never 404) is deliberate: whether a given engagement exists is not
    something a customer is entitled to learn. Two failure modes both 403:
      * the caller is not a client role
      * a client whose login is not bound to an engagement (misconfiguration)
    """
    if user.role != CLIENT_ROLE:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Customer portal is client-only")
    if user.client_engagement_id is None:
        raise HTTPException(status.HTTP_403_FORBIDDEN,
                            "Client login is not bound to an engagement")
    return user.client_engagement_id


def resolve_scope(user: CurrentUser,
                  requested_engagement_id: uuid.UUID | None = None) -> uuid.UUID:
    """The safe engagement id to filter by.

    A caller-supplied engagement_id is honoured ONLY if it equals the bound one;
    otherwise 403. This is the IDOR defense — portal endpoints never trust a
    client's engagement_id parameter, they reconcile it against the token.
    """
    bound = assert_client(user)
    if requested_engagement_id is not None and requested_engagement_id != bound:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Engagement is out of scope")
    return bound


def client_scoped(stmt: Select, user: CurrentUser,
                  engagement_column: ColumnElement) -> Select:
    """The single choke point every portal SELECT must pass through: restricts the
    query to the client's bound engagement. Centralized so a new route physically
    cannot return cross-engagement rows if it uses this helper."""
    bound = assert_client(user)
    return stmt.where(engagement_column == bound)


# ── FastAPI dependencies ──────────────────────────────────────────────────────

async def require_client(
    user: Annotated[CurrentUser, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> CurrentUser:
    """Resolve the customer binding from live database state on every request.

    JWT claims identify the session, but account disablement and engagement
    rebinding must take effect immediately rather than waiting for token expiry.
    """
    token_engagement_id = assert_client(user)
    live_user = (await db.execute(
        select(User)
        .join(Engagement, User.client_engagement_id == Engagement.id)
        .where(
            User.id == user.user_id,
            User.tenant_id == user.tenant_id,
            User.role == UserRole.client,
            User.is_active.is_(True),
            Engagement.tenant_id == user.tenant_id,
        )
    )).scalar_one_or_none()
    if live_user is None or live_user.client_engagement_id is None:
        raise HTTPException(status.HTTP_403_FORBIDDEN,
                            "Customer access is disabled or no longer assigned")
    if live_user.client_engagement_id != token_engagement_id:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                            "Customer engagement changed; sign in again")
    return user


def scoped_engagement(
    user: Annotated[CurrentUser, Depends(get_current_user)],
    engagement_id: Annotated[uuid.UUID | None, Query()] = None,
) -> uuid.UUID:
    """Route dependency yielding the client's engagement id, rejecting any
    mismatched ?engagement_id. Use on every /portal endpoint that reads data."""
    return resolve_scope(user, engagement_id)


ClientUser = Annotated[CurrentUser, Depends(require_client)]
ScopedEngagement = Annotated[uuid.UUID, Depends(scoped_engagement)]

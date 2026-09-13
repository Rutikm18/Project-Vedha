"""
test_portal_scope.py — Phase 0 of the customer portal: the engagement-scoping
authorization boundary. Pure-logic (no DB): the security core that keeps a client
inside its one engagement and rejects any attempt to reach another.
"""
from __future__ import annotations

import uuid
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import HTTPException
from sqlalchemy import select

from app.auth.jwt import (
    MANAGER_AUDIENCE,
    PORTAL_AUDIENCE,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.auth.middleware import portal_jwt_path_allows
from app.auth.portal_scope import assert_client, client_scoped, require_client, resolve_scope
from app.auth.router import refresh
from app.models.enums import UserRole
from app.models.finding import Finding
from app.schemas.auth import CurrentUser


def _client(engagement: uuid.UUID | None = None) -> CurrentUser:
    return CurrentUser(
        user_id=uuid.uuid4(), tenant_id=uuid.uuid4(), role="client",
        client_engagement_id=engagement if engagement is not None else uuid.uuid4(),
    )


def _operator() -> CurrentUser:
    return CurrentUser(user_id=uuid.uuid4(), tenant_id=uuid.uuid4(), role="manager")


class TestAssertClient:
    def test_bound_client_returns_engagement(self):
        eng = uuid.uuid4()
        assert assert_client(_client(eng)) == eng

    def test_operator_is_forbidden(self):
        with pytest.raises(HTTPException) as e:
            assert_client(_operator())
        assert e.value.status_code == 403

    def test_client_without_engagement_is_forbidden(self):
        unbound = CurrentUser(user_id=uuid.uuid4(), tenant_id=uuid.uuid4(),
                              role="client", client_engagement_id=None)
        with pytest.raises(HTTPException) as e:
            assert_client(unbound)
        assert e.value.status_code == 403


class TestResolveScope:
    def test_no_request_returns_bound(self):
        eng = uuid.uuid4()
        assert resolve_scope(_client(eng)) == eng

    def test_matching_request_ok(self):
        eng = uuid.uuid4()
        assert resolve_scope(_client(eng), eng) == eng

    def test_mismatched_request_is_403_idor_defense(self):
        with pytest.raises(HTTPException) as e:
            resolve_scope(_client(uuid.uuid4()), uuid.uuid4())  # someone else's id
        assert e.value.status_code == 403


class TestClientScoped:
    def test_applies_engagement_filter_for_bound_id(self):
        eng = uuid.uuid4()
        stmt = client_scoped(select(Finding), _client(eng), Finding.engagement_id)
        sql = str(stmt.compile(compile_kwargs={"literal_binds": True}))
        assert "WHERE findings.engagement_id =" in sql
        # SQLAlchemy renders the UUID dashless in literal binds.
        assert eng.hex in sql.replace("-", "")

    def test_operator_cannot_scope(self):
        with pytest.raises(HTTPException):
            client_scoped(select(Finding), _operator(), Finding.engagement_id)


class TestLiveClientBinding:
    @staticmethod
    def _db_returning(value):
        result = MagicMock()
        result.scalar_one_or_none.return_value = value
        db = MagicMock()
        db.execute = AsyncMock(return_value=result)
        return db

    @pytest.mark.asyncio
    async def test_accepts_an_active_unchanged_binding(self):
        principal = _client()
        live_user = MagicMock(
            id=principal.user_id,
            role=UserRole.client,
            is_active=True,
            client_engagement_id=principal.client_engagement_id,
        )

        resolved = await require_client(principal, self._db_returning(live_user))

        assert resolved == principal

    @pytest.mark.asyncio
    async def test_disabled_or_deleted_binding_is_rejected_immediately(self):
        with pytest.raises(HTTPException) as exc:
            await require_client(_client(), self._db_returning(None))
        assert exc.value.status_code == 403

    @pytest.mark.asyncio
    async def test_stale_token_is_rejected_after_rebinding(self):
        principal = _client()
        live_user = MagicMock(client_engagement_id=uuid.uuid4())
        with pytest.raises(HTTPException) as exc:
            await require_client(principal, self._db_returning(live_user))
        assert exc.value.status_code == 401


class TestPortalTokenClaims:
    def test_client_token_carries_portal_aud_and_engagement(self):
        eng = uuid.uuid4()
        tok = create_access_token(
            subject=str(uuid.uuid4()), tenant_id=str(uuid.uuid4()), role="client",
            extra_claims={"aud": PORTAL_AUDIENCE, "client_engagement_id": str(eng)},
        )
        claims = decode_token(tok)
        assert claims["aud"] == PORTAL_AUDIENCE
        assert claims["client_engagement_id"] == str(eng)
        assert claims["role"] == "client"

    def test_operator_and_portal_audiences_differ(self):
        assert MANAGER_AUDIENCE != PORTAL_AUDIENCE

    def test_client_role_enum_exists(self):
        assert UserRole.client.value == "client"


class TestPortalTokenIsConfinedToPortalRoutes:
    """`jwt.py` states the portal audience exists "so it can be rejected on
    operator APIs even if a role check is ever missed" — but nothing enforced it:
    the audience was minted and never read, leaving per-route `require_role` as
    the only barrier. That is the layer the audience was meant to back up, so a
    single forgotten role gate exposed an operator route to a customer login."""

    def test_portal_routes_are_allowed(self):
        assert portal_jwt_path_allows("/portal")
        assert portal_jwt_path_allows("/portal/findings")
        assert portal_jwt_path_allows("/portal/scans")

    def test_auth_routes_are_allowed(self):
        # The portal UI must still be able to identify, refresh and log out.
        assert portal_jwt_path_allows("/auth/me")
        assert portal_jwt_path_allows("/auth/refresh")
        assert portal_jwt_path_allows("/auth/logout")

    def test_operator_routes_are_rejected(self):
        # The exact route that surfaced this: launching a scan job.
        assert not portal_jwt_path_allows("/agents/jobs")
        assert not portal_jwt_path_allows("/agents")
        assert not portal_jwt_path_allows("/engagements")
        assert not portal_jwt_path_allows("/findings")
        assert not portal_jwt_path_allows("/users")

    def test_prefix_lookalikes_do_not_slip_through(self):
        """`/portal` must not authorize `/portalsomething` or a crafted path."""
        assert not portal_jwt_path_allows("/portalx")
        assert not portal_jwt_path_allows("/portal-admin/jobs")
        assert not portal_jwt_path_allows("/authz/escalate")


class TestRefreshPreservesAudienceAndScope:
    """`/auth/refresh` must re-mint the SAME credential class the login issued.

    Login refuses to mint a client token without `client_engagement_id` ("the
    portal's entire scoping boundary"), but refresh rebuilt the access token with
    no extra claims at all — dropping both `aud` and `client_engagement_id`. The
    customer was then locked out of their own portal on the next rotation
    (assert_client fails closed with "not bound to an engagement"), and the
    audience separation silently disappeared from every refreshed token.
    """

    @staticmethod
    def _db_returning(user):
        result = MagicMock()
        result.scalar_one_or_none.return_value = user
        db = MagicMock()
        db.execute = AsyncMock(return_value=result)
        return db

    @pytest.mark.asyncio
    async def test_client_refresh_keeps_portal_aud_and_engagement(self):
        eng, uid, tid = uuid.uuid4(), uuid.uuid4(), uuid.uuid4()
        user = MagicMock(id=uid, tenant_id=tid, role=UserRole.client,
                         client_engagement_id=eng)
        token, _ = create_refresh_token(subject=str(uid), tenant_id=str(tid))

        resp = await refresh(token, db=self._db_returning(user))

        claims = decode_token(resp.access_token)
        assert claims["aud"] == PORTAL_AUDIENCE
        assert claims["client_engagement_id"] == str(eng)

    @pytest.mark.asyncio
    async def test_operator_refresh_keeps_manager_aud(self):
        uid, tid = uuid.uuid4(), uuid.uuid4()
        user = MagicMock(id=uid, tenant_id=tid, role=UserRole.manager,
                         client_engagement_id=None)
        token, _ = create_refresh_token(subject=str(uid), tenant_id=str(tid))

        resp = await refresh(token, db=self._db_returning(user))

        claims = decode_token(resp.access_token)
        assert claims["aud"] == MANAGER_AUDIENCE
        assert "client_engagement_id" not in claims

    @pytest.mark.asyncio
    async def test_unbound_client_cannot_refresh_into_an_unscoped_token(self):
        """Same rule as login: never mint an unscoped client token."""
        uid, tid = uuid.uuid4(), uuid.uuid4()
        user = MagicMock(id=uid, tenant_id=tid, role=UserRole.client,
                         client_engagement_id=None)
        token, _ = create_refresh_token(subject=str(uid), tenant_id=str(tid))

        with pytest.raises(HTTPException) as exc:
            await refresh(token, db=self._db_returning(user))
        assert exc.value.status_code == 403

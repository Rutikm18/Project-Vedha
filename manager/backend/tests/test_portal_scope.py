"""
test_portal_scope.py — Phase 0 of the customer portal: the engagement-scoping
authorization boundary. Pure-logic (no DB): the security core that keeps a client
inside its one engagement and rejects any attempt to reach another.
"""
from __future__ import annotations

import uuid

import pytest
from fastapi import HTTPException
from sqlalchemy import select

from app.auth.jwt import (
    MANAGER_AUDIENCE,
    PORTAL_AUDIENCE,
    create_access_token,
    decode_token,
)
from app.auth.portal_scope import assert_client, client_scoped, resolve_scope
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

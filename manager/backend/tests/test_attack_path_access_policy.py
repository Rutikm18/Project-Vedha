from uuid import UUID

import pytest

from app.graph.access_policy import may_access_assessment
from app.schemas.auth import CurrentUser

TENANT = UUID("00000000-0000-4000-8000-000000000001")
OTHER = UUID("00000000-0000-4000-8000-000000000002")


def principal(role="analyst", **fields):
    return CurrentUser(user_id=OTHER, tenant_id=TENANT, role=role, **fields)


@pytest.mark.parametrize("role", ["admin", "manager", "analyst", "tester"])
@pytest.mark.parametrize("operation", ["read", "compute", "compare"])
def test_authorized_operator_roles(role, operation):
    assert may_access_assessment(principal(role), TENANT, operation)


def test_auditor_is_read_only():
    user = principal("auditor")
    assert may_access_assessment(user, TENANT, "read")
    assert not may_access_assessment(user, TENANT, "compute")
    assert not may_access_assessment(user, TENANT, "compare")


@pytest.mark.parametrize("role", ["client", "viewer", "unknown"])
def test_no_projection_for_unapproved_roles(role):
    assert not may_access_assessment(principal(role), TENANT, "read")


def test_foreign_tenant_even_for_admin():
    assert not may_access_assessment(principal("admin"), OTHER, "read")


def test_pat_and_engagement_limited_principals_are_excluded():
    assert not may_access_assessment(principal(auth_type="pat"), TENANT, "read")
    assert not may_access_assessment(
        principal(client_engagement_id=OTHER), TENANT, "read"
    )


def test_access_downgrade_is_rechecked_not_cached():
    assert may_access_assessment(principal("analyst"), TENANT, "read")
    assert not may_access_assessment(principal("client"), TENANT, "read")

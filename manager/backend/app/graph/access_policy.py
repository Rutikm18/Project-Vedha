"""Operator-only initial release; no redacted conclusions or portal projection."""

from typing import Literal
from uuid import UUID

from app.schemas.auth import CurrentUser

Operation = Literal["read", "compute", "compare"]
_READ_ROLES = frozenset({"admin", "manager", "analyst", "tester", "auditor"})
_WRITE_ROLES = _READ_ROLES - {"auditor"}


def may_access_assessment(
    user: CurrentUser, tenant_id: UUID, operation: Operation
) -> bool:
    """Use fresh authenticated claims and independently tenant-scoped engagement.

    PAT and portal principals are excluded until their disclosure/scopes are
    designed. Do not call inference on a redacted set and claim it is complete.
    """
    if operation not in ("read", "compute", "compare"):
        return False
    if (
        user.tenant_id != tenant_id
        or user.auth_type != "jwt"
        or user.client_engagement_id is not None
    ):
        return False
    roles = _READ_ROLES if operation == "read" else _WRITE_ROLES
    return user.role in roles

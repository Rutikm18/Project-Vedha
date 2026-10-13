"""Live operator authorization shared by finding and legacy graph transport."""

from fastapi import HTTPException
from sqlalchemy import select

from app.graph.access_policy import may_access_assessment
from app.models.user import User
from app.models.tenant import Tenant


async def load_assessment_principal(db, user, operation="read"):
    def denied():
        return HTTPException(
            403,
            "Attack assessment access is not permitted",
            headers={"Cache-Control": "no-store"},
        )

    if not may_access_assessment(user, user.tenant_id, operation):
        raise denied()
    live = (
        await db.execute(
            select(
                User.role,
                User.is_active,
                User.client_engagement_id,
                Tenant.is_active.label("tenant_active"),
            )
            .join(Tenant, User.tenant_id == Tenant.id)
            .where(User.id == user.user_id, User.tenant_id == user.tenant_id)
        )
    ).one_or_none()
    if live is None or not live.is_active or not live.tenant_active:
        raise denied()
    role = "auditor" if "auditor" in (user.role, live.role.value) else live.role.value
    effective = user.model_copy(
        update={"role": role, "client_engagement_id": live.client_engagement_id}
    )
    if not may_access_assessment(effective, effective.tenant_id, operation):
        raise denied()
    return effective

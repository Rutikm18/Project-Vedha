from typing import Annotated

from fastapi import Depends, HTTPException, status

from app.dependencies import get_current_user
from app.schemas.auth import CurrentUser
from app import audit_context
from app.services import audit as audit_service


def require_role(allowed_roles: list[str]):
    """
    FastAPI dependency that enforces role-based access.

    Usage:
        @router.post("/")
        async def create(..., _: Annotated[CurrentUser, require_role(["admin","manager"])]):
    """
    async def _check(
        current_user: Annotated[CurrentUser, Depends(get_current_user)],
    ) -> CurrentUser:
        if current_user.role not in allowed_roles:
            # The refusal raises, so the request's transaction rolls back: the entry is
            # written in its own transaction. Method and path only, never the query string.
            ctx = audit_context.current()
            await audit_service.record_audit_independent(
                actor_id=getattr(current_user, "user_id", "unknown"), action="access.denied",
                outcome="denied", tenant_id=getattr(current_user, "tenant_id", None), resource_type="endpoint",
                detail={"method": ctx.get("method"), "path": ctx.get("path"),
                        "role": current_user.role, "required_roles": list(allowed_roles)},
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{current_user.role}' is not permitted. Required: {allowed_roles}",
            )
        return current_user

    return Depends(_check)

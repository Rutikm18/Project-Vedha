"""Binds the request's identity (source address, user agent, request id, tenant, actor)
into app.audit_context for the audit trail. Sits INSIDE TenantIsolationMiddleware, so
request.state already carries the authenticated claims by the time it runs."""
from __future__ import annotations

import re
import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app import audit_context
from app.ratelimit import client_ip

# A caller-supplied request id is kept only when it is plain, so a hostile header cannot
# smuggle control characters or an enormous string into the audit trail.
_SAFE_REQUEST_ID = re.compile(r"^[A-Za-z0-9._-]{1,64}$")


def _actor_type(request: Request) -> str | None:
    state = request.state
    if getattr(state, "user_id", None) is None:
        return None
    if getattr(state, "role", None) == "agent":
        return "agent"
    if getattr(state, "client_engagement_id", None):
        return "client"
    return "user"


class AuditContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        supplied = request.headers.get("x-request-id", "")
        audit_context.clear()
        audit_context.bind(
            ip=client_ip(request),
            user_agent=request.headers.get("user-agent", "")[:255] or None,
            request_id=supplied if _SAFE_REQUEST_ID.match(supplied) else str(uuid.uuid4()),
            tenant_id=getattr(request.state, "tenant_id", None),
            actor_id=getattr(request.state, "user_id", None),
            actor_type=_actor_type(request),
            method=request.method,
            path=request.url.path,
        )
        return await call_next(request)

from datetime import datetime, timezone
import re
import uuid

import structlog
from fastapi import Request, Response
from sqlalchemy import select
from starlette.middleware.base import BaseHTTPMiddleware

from app.auth.jwt import decode_token
from app.auth.pat import TOKEN_PREFIX, hash_pat_token, pat_scope_allows
from app.database import AsyncSessionLocal
from app.models.personal_access_token import PersonalAccessToken
from app.models.agent import Agent

logger = structlog.get_logger()

_PUBLIC_PATHS = {"/", "/health", "/metrics", "/auth/login", "/auth/refresh", "/docs", "/openapi.json", "/redoc"}
_PUBLIC_PREFIXES = ("/docs", "/redoc")

_AGENT_REFRESH_PATH = re.compile(r"^/agents/[^/]+/refresh$")
_AGENT_JOBS_PATH = re.compile(r"^/agents/[^/]+/jobs$")
_AGENT_RESULT_PATH = re.compile(r"^/agents/[^/]+/jobs/[^/]+/result$")
_AGENT_SCOPE_PATH = re.compile(r"^/engagements/[^/]+/scope$")
_PUBLIC_ENROLLMENT_PATHS = (
    re.compile(r"^/probe-enrollment/requests$"),
    re.compile(r"^/probe-enrollment/requests/[0-9a-fA-F-]+/poll$"),
    re.compile(r"^/probe-enrollment/requests/[0-9a-fA-F-]+/activate$"),
    re.compile(r"^/probe-enrollment/token$"),
)


def _is_public_enrollment_request(path: str, method: str) -> bool:
    return method.upper() == "POST" and any(pattern.fullmatch(path) for pattern in _PUBLIC_ENROLLMENT_PATHS)


def agent_jwt_path_allows(path: str, method: str) -> bool:
    """Least-privilege route allowlist for legacy probe access JWTs.

    This is the immediate containment boundary while device-audience credentials
    migrate to a dedicated API namespace. Resource ownership is still checked by
    the route handlers.
    """
    method = method.upper()
    if path == "/agents/heartbeat":
        return method == "POST"
    if _AGENT_REFRESH_PATH.fullmatch(path):
        return method == "POST"
    if _AGENT_JOBS_PATH.fullmatch(path):
        return method == "GET"
    if _AGENT_RESULT_PATH.fullmatch(path):
        return method == "POST"
    if _AGENT_SCOPE_PATH.fullmatch(path):
        return method == "GET"
    return False


class TenantIsolationMiddleware(BaseHTTPMiddleware):
    """
    Extracts JWT from Authorization header and injects tenant_id + user
    claims into request.state.  All DB queries downstream use
    request.state.tenant_id to scope results.
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        path = request.url.path
        if (
            path in _PUBLIC_PATHS
            or path.startswith(_PUBLIC_PREFIXES)
            or _is_public_enrollment_request(path, request.method)
        ):
            return await call_next(request)

        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return Response(
                content='{"detail":"Missing or invalid Authorization header"}',
                status_code=401,
                media_type="application/json",
            )

        token = auth.removeprefix("Bearer ").strip()
        if token.startswith(TOKEN_PREFIX):
            pat_payload = await self._authenticate_pat(token, path, request.method)
            if pat_payload is None:
                return Response(
                    content='{"detail":"Invalid, expired, revoked, or out-of-scope personal access token"}',
                    status_code=401,
                    media_type="application/json",
                )
            request.state.user_id = pat_payload["user_id"]
            request.state.tenant_id = pat_payload["tenant_id"]
            request.state.role = pat_payload["role"]
            request.state.auth_type = "pat"
            request.state.pat_id = pat_payload["pat_id"]
            request.state.scopes = pat_payload["scopes"]

            structlog.contextvars.bind_contextvars(
                tenant_id=pat_payload["tenant_id"],
                user_id=pat_payload["user_id"],
                auth_type="pat",
                pat_id=pat_payload["pat_id"],
            )

            response = await call_next(request)
            structlog.contextvars.clear_contextvars()
            return response

        try:
            payload = decode_token(token)
            if payload.get("type") != "access":
                raise ValueError("not an access token")
        except Exception as exc:
            logger.warning("auth.middleware.rejected", path=path, reason=str(exc))
            return Response(
                content='{"detail":"Invalid or expired token"}',
                status_code=401,
                media_type="application/json",
            )

        if payload.get("role") == "agent" and not agent_jwt_path_allows(
            path, request.method,
        ):
            logger.warning(
                "auth.agent_route_rejected",
                path=path,
                method=request.method,
                agent_id=payload.get("sub"),
            )
            return Response(
                content='{"detail":"Agent credential is not permitted on this endpoint"}',
                status_code=403,
                media_type="application/json",
            )

        if payload.get("role") == "agent" and payload.get("typ") == "device_access":
            if payload.get("aud") != "vedha-probe-api":
                return Response(
                    content='{"detail":"Wrong device token audience"}',
                    status_code=401,
                    media_type="application/json",
                )
            try:
                async with AsyncSessionLocal() as db:
                    agent = (await db.execute(
                        select(Agent).where(
                            Agent.id == uuid.UUID(str(payload.get("sub"))),
                            Agent.tenant_id == uuid.UUID(str(payload.get("tenant_id"))),
                        )
                    )).scalar_one_or_none()
            except Exception as exc:
                logger.error("auth.device_lookup_failed", error=str(exc))
                return Response(content='{"detail":"Device authentication unavailable"}', status_code=503, media_type="application/json")
            if (
                agent is None
                or agent.lifecycle_status != "active"
                or agent.credential_generation != payload.get("credential_generation")
            ):
                return Response(
                    content='{"detail":"Device credential revoked, disabled, or stale"}',
                    status_code=401,
                    media_type="application/json",
                )

        request.state.user_id = payload["sub"]
        request.state.tenant_id = payload["tenant_id"]
        request.state.role = payload["role"]
        request.state.auth_type = "jwt"
        request.state.scopes = ()

        structlog.contextvars.bind_contextvars(
            tenant_id=payload["tenant_id"],
            user_id=payload["sub"],
        )

        response = await call_next(request)
        structlog.contextvars.clear_contextvars()
        return response

    async def _authenticate_pat(self, token: str, path: str, method: str) -> dict | None:
        token_hash = hash_pat_token(token)
        now = datetime.now(timezone.utc)
        try:
            async with AsyncSessionLocal() as db:
                pat = (
                    await db.execute(
                        select(PersonalAccessToken)
                        .where(
                            PersonalAccessToken.token_hash == token_hash,
                            PersonalAccessToken.revoked_at.is_(None),
                        )
                    )
                ).scalar_one_or_none()
                if pat is None:
                    return None
                if pat.expires_at and pat.expires_at <= now:
                    return None

                scopes = list(pat.scopes or [])
                if not pat_scope_allows(path, method, scopes):
                    logger.warning(
                        "auth.pat.scope_rejected",
                        pat_id=str(pat.id),
                        path=path,
                        method=method,
                        scopes=scopes,
                    )
                    return None

                pat.last_used_at = now
                await db.commit()
                return {
                    "user_id": str(pat.user_id),
                    "tenant_id": str(pat.tenant_id),
                    "role": pat.role,
                    "pat_id": str(pat.id),
                    "scopes": tuple(scopes),
                }
        except Exception as exc:
            logger.warning("auth.pat.rejected", path=path, reason=str(exc))
            return None

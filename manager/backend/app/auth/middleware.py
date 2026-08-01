from datetime import datetime, timezone

import structlog
from fastapi import Request, Response
from sqlalchemy import select
from starlette.middleware.base import BaseHTTPMiddleware

from app.auth.jwt import decode_token
from app.auth.pat import TOKEN_PREFIX, hash_pat_token, pat_scope_allows
from app.database import AsyncSessionLocal
from app.models.personal_access_token import PersonalAccessToken

logger = structlog.get_logger()

_PUBLIC_PATHS = {"/", "/health", "/metrics", "/auth/login", "/auth/refresh", "/docs", "/openapi.json", "/redoc"}
_PUBLIC_PREFIXES = ("/docs", "/redoc")


class TenantIsolationMiddleware(BaseHTTPMiddleware):
    """
    Extracts JWT from Authorization header and injects tenant_id + user
    claims into request.state.  All DB queries downstream use
    request.state.tenant_id to scope results.
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        path = request.url.path
        if path in _PUBLIC_PATHS or path.startswith(_PUBLIC_PREFIXES):
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

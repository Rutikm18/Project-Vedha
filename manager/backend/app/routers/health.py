"""
Health endpoints.

GET /health          — liveness: DB + Redis reachability (fast, used by load-balancers)
GET /health/auth     — auth subsystem: JWT config, bcrypt, admin account
GET /health/startup  — full startup diagnostics from the last run

None of these endpoints expose secrets, internal paths, or implementation details.
Status codes follow the convention: 200 = ready, 503 = degraded/unavailable.
"""

from __future__ import annotations

import time

import structlog
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from sqlalchemy import text

from app.auth.startup import get_last_report, run_startup_diagnostics
from app.database import AsyncSessionLocal
from app.dependencies import get_redis

router = APIRouter(tags=["system"])
logger = structlog.get_logger()


# ── /health — liveness (DB + Redis) ──────────────────────────────────────────

@router.get(
    "/health",
    summary="Liveness check — DB + Redis",
    responses={
        200: {"description": "All dependencies reachable"},
        503: {"description": "One or more dependencies degraded"},
    },
)
async def health():
    t0 = time.monotonic()
    checks: dict[str, str] = {}

    async with AsyncSessionLocal() as db:
        try:
            await db.execute(text("SELECT 1"))
            checks["postgres"] = "ok"
        except Exception as exc:
            checks["postgres"] = f"error: {type(exc).__name__}"

    try:
        redis = await get_redis()
        await redis.ping()
        checks["redis"] = "ok"
    except Exception as exc:
        checks["redis"] = f"error: {type(exc).__name__}"

    ok = all(v == "ok" for v in checks.values())
    body = {
        "status": "healthy" if ok else "degraded",
        "checks": checks,
        "latency_ms": round((time.monotonic() - t0) * 1000, 2),
    }
    return JSONResponse(
        status_code=status.HTTP_200_OK if ok else status.HTTP_503_SERVICE_UNAVAILABLE,
        content=body,
    )


# ── /health/auth — auth subsystem readiness ───────────────────────────────────

@router.get(
    "/health/auth",
    summary="Auth subsystem health — JWT config, bcrypt, admin existence",
    responses={
        200: {"description": "Auth subsystem ready"},
        503: {"description": "Auth subsystem degraded"},
    },
)
async def health_auth():
    """
    Validates the authentication subsystem without touching login state.
    Returns only pass/fail per check — never leaks secret values.
    """
    import os
    import uuid

    from passlib.context import CryptContext

    from app.config import get_settings
    from app.models.user import User
    from sqlalchemy import select

    settings = get_settings()
    t0 = time.monotonic()
    checks: dict[str, str] = {}

    # JWT secret presence + strength
    secret = settings.jwt_secret
    weak = {"change-me-at-least-32-chars-long!!", "your-secret-key", "secret"}
    if not secret or secret in weak or len(secret) < 32:
        checks["jwt_secret"] = "misconfigured"
    else:
        checks["jwt_secret"] = "ok"

    # bcrypt round-trip
    try:
        pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
        probe = f"health-probe-{uuid.uuid4()}"
        assert pwd.verify(probe, pwd.hash(probe))
        checks["bcrypt"] = "ok"
    except Exception as exc:
        checks["bcrypt"] = f"error: {type(exc).__name__}"

    # Admin account existence (non-blocking — skip if DB is down)
    admin_email = os.getenv("SEED_ADMIN_EMAIL", "").strip()
    if admin_email:
        try:
            async with AsyncSessionLocal() as db:
                user = (
                    await db.execute(select(User).where(User.email == admin_email))
                ).scalar_one_or_none()
            if user is None:
                checks["admin_account"] = "not_found"
            elif not user.is_active:
                checks["admin_account"] = "disabled"
            else:
                checks["admin_account"] = "ok"
        except Exception as exc:
            checks["admin_account"] = f"db_error: {type(exc).__name__}"
    else:
        checks["admin_account"] = "skipped_no_email_configured"

    # Cookie config
    auth_cookie_secure = os.getenv("AUTH_COOKIE_SECURE", "false").lower()
    if settings.is_production and auth_cookie_secure != "true":
        checks["cookie_config"] = "insecure_in_production"
    else:
        checks["cookie_config"] = "ok"

    ok = all(v == "ok" or v.startswith("skipped") for v in checks.values())
    body = {
        "status": "ready" if ok else "degraded",
        "checks": checks,
        "latency_ms": round((time.monotonic() - t0) * 1000, 2),
    }
    return JSONResponse(
        status_code=status.HTTP_200_OK if ok else status.HTTP_503_SERVICE_UNAVAILABLE,
        content=body,
    )


# ── /health/startup — last startup diagnostics report ────────────────────────

@router.get(
    "/health/startup",
    summary="Full startup diagnostics from the last boot",
    responses={
        200: {"description": "All startup checks passed"},
        503: {"description": "One or more startup checks failed"},
    },
)
async def health_startup():
    """
    Returns the cached report from the last startup diagnostics run.
    If the report is stale or missing (cold start), runs diagnostics on-demand
    but does NOT abort — returns results without raising StartupAbortError.
    """
    report = get_last_report()

    if report is None:
        # On-demand run (e.g. first call before lifespan completed)
        try:
            report = await run_startup_diagnostics(fail_on_fatal=False)
        except Exception as exc:
            logger.error("health.startup.on_demand_failed", error=str(exc))
            return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content={"status": "error", "detail": "diagnostics failed to run"},
            )

    body = report.as_dict()
    return JSONResponse(
        status_code=status.HTTP_200_OK if report.all_ok else status.HTTP_503_SERVICE_UNAVAILABLE,
        content=body,
    )

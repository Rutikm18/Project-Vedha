"""
Startup diagnostics for Vedha Manager API.

Runs during FastAPI lifespan (before first request). Checks every dependency
and configuration invariant that must hold for the application to function
correctly. Fatal failures abort startup; warnings are logged and tolerated.

Design:
  - Each check is a method returning a CheckResult — never raises.
  - run_all() collects all results, logs a summary, and raises
    StartupAbortError if any fatal check failed.
  - Checks run concurrently (asyncio.gather) to minimise startup latency.
"""

from __future__ import annotations

import asyncio
import os
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Literal

import structlog
from passlib.context import CryptContext
from sqlalchemy import select, text

from app.auth.exceptions import DatabaseUnavailableError
from app.config import get_settings
from app.database import AsyncSessionLocal

logger = structlog.get_logger()
settings = get_settings()

_pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

Severity = Literal["fatal", "warning", "ok"]

_KNOWN_WEAK_JWT: frozenset[str] = frozenset({
    "change-me-at-least-32-chars-long!!",
    "change-me-please-to-a-long-random-secret-value!!",
    "your-secret-key",
    "secret",
})


# ── Result model ──────────────────────────────────────────────────────────────

@dataclass
class CheckResult:
    name: str
    severity: Severity
    message: str
    detail: dict = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        return self.severity == "ok"

    @property
    def fatal(self) -> bool:
        return self.severity == "fatal"


@dataclass
class DiagnosticsReport:
    results: list[CheckResult] = field(default_factory=list)
    run_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    elapsed_ms: float = 0.0

    @property
    def has_fatal(self) -> bool:
        return any(r.fatal for r in self.results)

    @property
    def all_ok(self) -> bool:
        return all(r.ok for r in self.results)

    def as_dict(self) -> dict:
        return {
            "run_at": self.run_at.isoformat(),
            "elapsed_ms": round(self.elapsed_ms, 1),
            "all_ok": self.all_ok,
            "checks": [
                {"name": r.name, "severity": r.severity, "message": r.message}
                for r in self.results
            ],
        }


class StartupAbortError(RuntimeError):
    """Raised when one or more fatal checks fail — aborts app startup."""


# ── Individual checks ─────────────────────────────────────────────────────────

async def _check_database() -> CheckResult:
    last_exc: Exception | None = None
    msg = ""
    for attempt in range(1, 4):
        try:
            async with AsyncSessionLocal() as db:
                await asyncio.wait_for(db.execute(text("SELECT 1")), timeout=5)
            return CheckResult("database", "ok", "reachable")
        except asyncio.TimeoutError:
            last_exc = None
            msg = "connection timed out after 5s"
        except Exception as exc:
            last_exc = exc
            msg = f"connection failed: {exc}"
        if attempt < 3:
            await asyncio.sleep(2)
    return CheckResult("database", "fatal", f"unreachable after 3 attempts: {msg}")


async def _check_redis() -> CheckResult:
    try:
        import redis.asyncio as aioredis
        client = aioredis.from_url(settings.redis_url, socket_timeout=5)
        await asyncio.wait_for(client.ping(), timeout=5)
        await client.aclose()
        return CheckResult("redis", "ok", "PING → PONG")
    except asyncio.TimeoutError:
        return CheckResult("redis", "fatal", "PING timed out after 5s")
    except Exception as exc:
        return CheckResult("redis", "fatal", f"connection failed: {exc}")


async def _check_jwt_secret() -> CheckResult:
    secret = settings.jwt_secret
    if not secret:
        return CheckResult("jwt_secret", "fatal", "JWT_SECRET is empty")
    if secret in _KNOWN_WEAK_JWT:
        return CheckResult(
            "jwt_secret", "fatal",
            "JWT_SECRET is a known-weak default — replace immediately",
        )
    if len(secret) < 32:
        return CheckResult(
            "jwt_secret", "fatal",
            f"JWT_SECRET too short ({len(secret)} chars, need ≥32)",
        )
    return CheckResult("jwt_secret", "ok", f"length={len(secret)}")


async def _check_bcrypt() -> CheckResult:
    """Verify the bcrypt library can round-trip a hash — catches misconfigured passlib."""
    try:
        test_pw = f"startup-probe-{uuid.uuid4()}"
        hashed = _pwd.hash(test_pw)
        if not _pwd.verify(test_pw, hashed):
            return CheckResult("bcrypt", "fatal", "verify() returned False for a freshly-hashed password")
        return CheckResult("bcrypt", "ok", "hash/verify round-trip passed")
    except Exception as exc:
        return CheckResult("bcrypt", "fatal", f"bcrypt raised: {exc}")


async def _check_admin_account() -> CheckResult:
    """Verify the seeded admin account exists and is active."""
    admin_email = os.getenv("SEED_ADMIN_EMAIL", "").strip()
    if not admin_email:
        return CheckResult(
            "admin_account", "warning",
            "SEED_ADMIN_EMAIL not set — cannot verify admin account exists",
        )
    try:
        from app.models.user import User
        async with AsyncSessionLocal() as db:
            user = (
                await asyncio.wait_for(
                    db.execute(select(User).where(User.email == admin_email)),
                    timeout=5,
                )
            ).scalar_one_or_none()

        if user is None:
            return CheckResult(
                "admin_account", "fatal",
                f"Admin user '{admin_email}' not found — run the migrate service",
            )
        if not user.is_active:
            return CheckResult(
                "admin_account", "fatal",
                f"Admin user '{admin_email}' exists but is_active=False",
            )
        return CheckResult(
            "admin_account", "ok",
            f"user_id={user.id} is_active=True role={user.role.value}",
        )
    except asyncio.TimeoutError:
        return CheckResult("admin_account", "warning", "DB timeout — skipping admin check")
    except Exception as exc:
        return CheckResult("admin_account", "warning", f"check failed: {exc}")


async def _check_tenant() -> CheckResult:
    """Verify the default tenant is active."""
    tenant_name = os.getenv("SEED_TENANT_NAME", "Default Tenant")
    try:
        from app.models.tenant import Tenant
        async with AsyncSessionLocal() as db:
            tenant = (
                await asyncio.wait_for(
                    db.execute(select(Tenant).where(Tenant.name == tenant_name)),
                    timeout=5,
                )
            ).scalar_one_or_none()

        if tenant is None:
            return CheckResult(
                "tenant", "fatal",
                f"Tenant '{tenant_name}' not found — migration + seed must run first",
            )
        if not tenant.is_active:
            return CheckResult(
                "tenant", "fatal",
                f"Tenant '{tenant_name}' is_active=False — all logins will fail",
            )
        return CheckResult(
            "tenant", "ok",
            f"tenant_id={tenant.id} is_active=True",
        )
    except asyncio.TimeoutError:
        return CheckResult("tenant", "warning", "DB timeout — skipping tenant check")
    except Exception as exc:
        return CheckResult("tenant", "warning", f"check failed: {exc}")


async def _check_cookie_config() -> CheckResult:
    auth_cookie_secure = os.getenv("AUTH_COOKIE_SECURE", "false").lower()
    app_env = settings.app_env

    if app_env == "production" and auth_cookie_secure != "true":
        return CheckResult(
            "cookie_config", "fatal",
            "AUTH_COOKIE_SECURE=false in production — session cookies are insecure",
        )
    return CheckResult(
        "cookie_config", "ok",
        f"AUTH_COOKIE_SECURE={auth_cookie_secure} APP_ENV={app_env}",
    )


async def _check_cors() -> CheckResult:
    cors = settings.cors_origins
    if not cors:
        return CheckResult("cors", "fatal", "CORS_ORIGINS is empty — all cross-origin requests will fail")
    if settings.is_production:
        localhost_origins = [o for o in cors if "localhost" in o or "127.0.0.1" in o]
        if localhost_origins:
            return CheckResult(
                "cors", "warning",
                f"CORS_ORIGINS includes localhost in production: {localhost_origins}",
            )
    return CheckResult("cors", "ok", f"origins={cors}")


async def _check_required_env_vars() -> CheckResult:
    required = [
        "DATABASE_URL",
        "REDIS_URL",
        "JWT_SECRET",
        "APP_ENV",
        "CORS_ORIGINS",
    ]
    missing = [v for v in required if not os.getenv(v)]
    if missing:
        return CheckResult(
            "required_env_vars", "fatal",
            f"missing required env vars: {missing}",
        )
    return CheckResult("required_env_vars", "ok", f"all {len(required)} vars present")


# ── Orchestrator ──────────────────────────────────────────────────────────────

# Module-level cache so health endpoints can serve the last report
_last_report: DiagnosticsReport | None = None


async def run_startup_diagnostics(*, fail_on_fatal: bool = True) -> DiagnosticsReport:
    """
    Run all startup checks concurrently.
    Called from FastAPI lifespan before the app accepts traffic.
    """
    global _last_report

    t0 = time.monotonic()

    # Run config checks before connectivity (fast, no network)
    config_checks = await asyncio.gather(
        _check_required_env_vars(),
        _check_jwt_secret(),
        _check_bcrypt(),
        _check_cookie_config(),
        _check_cors(),
        return_exceptions=False,
    )

    # Run connectivity checks concurrently
    conn_checks = await asyncio.gather(
        _check_database(),
        _check_redis(),
        return_exceptions=False,
    )

    # Admin/tenant checks depend on DB being up
    db_result = next(r for r in conn_checks if r.name == "database")
    if db_result.ok:
        app_checks = await asyncio.gather(
            _check_admin_account(),
            _check_tenant(),
            return_exceptions=False,
        )
    else:
        app_checks = [
            CheckResult("admin_account", "warning", "skipped — DB not reachable"),
            CheckResult("tenant", "warning", "skipped — DB not reachable"),
        ]

    report = DiagnosticsReport(
        results=[*config_checks, *conn_checks, *app_checks],
        elapsed_ms=(time.monotonic() - t0) * 1000,
    )
    _last_report = report

    # Structured summary log
    log_data = {
        "elapsed_ms": round(report.elapsed_ms, 1),
        "checks": {r.name: r.severity for r in report.results},
    }
    if report.has_fatal:
        logger.error("startup.diagnostics.failed", **log_data)
    else:
        logger.info("startup.diagnostics.passed", **log_data)

    if fail_on_fatal and report.has_fatal:
        fatals = [r for r in report.results if r.fatal]
        msgs = "; ".join(f"{r.name}: {r.message}" for r in fatals)
        raise StartupAbortError(
            f"Startup aborted — {len(fatals)} fatal check(s) failed: {msgs}"
        )

    return report


def get_last_report() -> DiagnosticsReport | None:
    return _last_report

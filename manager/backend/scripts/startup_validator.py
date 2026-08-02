"""
Vedha Startup Validator
=======================
Runs at application boot — before accepting traffic — to catch misconfiguration
that would cause silent failures in production.

Integrated into FastAPI lifespan or run as a pre-start check:
    python scripts/startup_validator.py

Each validator raises StartupValidationError on failure. All validators run
even if earlier ones fail, so you see all problems at once.
"""

from __future__ import annotations

import asyncio
import os
import re
import sys
import time
from dataclasses import dataclass, field
from typing import Callable, Awaitable


# ── Custom exception ──────────────────────────────────────────────────────────

class StartupValidationError(RuntimeError):
    """Raised when a required configuration invariant is violated at boot."""


# ── Result model ──────────────────────────────────────────────────────────────

@dataclass
class CheckResult:
    name: str
    passed: bool
    message: str
    severity: str = "error"   # error | warning


@dataclass
class ValidationReport:
    results: list[CheckResult] = field(default_factory=list)

    def add(self, result: CheckResult) -> None:
        self.results.append(result)

    @property
    def errors(self) -> list[CheckResult]:
        return [r for r in self.results if not r.passed and r.severity == "error"]

    @property
    def warnings(self) -> list[CheckResult]:
        return [r for r in self.results if not r.passed and r.severity == "warning"]

    def print_summary(self) -> None:
        for r in self.results:
            icon = "✓" if r.passed else ("✗" if r.severity == "error" else "⚠")
            color = "\033[32m" if r.passed else ("\033[31m" if r.severity == "error" else "\033[33m")
            print(f"  {color}{icon}\033[0m  {r.name}: {r.message}")

    def raise_if_errors(self) -> None:
        if self.errors:
            msgs = "\n".join(f"  • {e.name}: {e.message}" for e in self.errors)
            raise StartupValidationError(
                f"Startup validation failed ({len(self.errors)} error(s)):\n{msgs}"
            )


# ── Individual validators ─────────────────────────────────────────────────────

class ConfigValidator:
    """Validates required env vars are present and non-default."""

    REQUIRED: list[str] = [
        "DATABASE_URL",
        "REDIS_URL",
        "JWT_SECRET",
        "APP_ENV",
        "CORS_ORIGINS",
    ]

    WEAK_VALUES = {
        "JWT_SECRET": {
            "change-me-at-least-32-chars-long!!",
            "change-me-please-to-a-long-random-secret-value!!",
            "your-secret-key",
        },
        "POSTGRES_PASSWORD": {"secret", "password", "postgres"},
        "SEED_ADMIN_PASSWORD": {"ChangeMe123!", "admin", "password"},
    }

    def validate(self, report: ValidationReport) -> None:
        for var in self.REQUIRED:
            val = os.getenv(var, "")
            if not val:
                report.add(CheckResult(
                    name=f"env.{var}",
                    passed=False,
                    message=f"required environment variable {var!r} is not set",
                ))
            else:
                report.add(CheckResult(
                    name=f"env.{var}",
                    passed=True,
                    message="set",
                ))

        # Weak value detection
        for var, bad_values in self.WEAK_VALUES.items():
            val = os.getenv(var, "")
            if val in bad_values:
                report.add(CheckResult(
                    name=f"env.{var}.strength",
                    passed=False,
                    message=f"{var} is using a known-weak default value — regenerate before going live",
                ))


class SecretsValidator:
    """Validates secrets meet minimum strength requirements."""

    MIN_JWT_LENGTH = 32

    def validate(self, report: ValidationReport) -> None:
        jwt = os.getenv("JWT_SECRET", "")
        if len(jwt) < self.MIN_JWT_LENGTH:
            report.add(CheckResult(
                name="secret.JWT_SECRET.length",
                passed=False,
                message=f"JWT_SECRET is {len(jwt)} chars — minimum {self.MIN_JWT_LENGTH}. "
                        "Generate: openssl rand -base64 48",
            ))
        else:
            report.add(CheckResult(
                name="secret.JWT_SECRET.length",
                passed=True,
                message=f"length {len(jwt)} ≥ {self.MIN_JWT_LENGTH} ✓",
            ))

        # Entropy check: a secret that's all lowercase or all digits is weak
        jwt_charset = set(jwt)
        if len(jwt_charset) < 20:
            report.add(CheckResult(
                name="secret.JWT_SECRET.entropy",
                passed=False,
                message="JWT_SECRET has low character diversity — use openssl rand -base64 48",
            ))


class AppEnvironmentValidator:
    """Validates APP_ENV and related production flags."""

    def validate(self, report: ValidationReport) -> None:
        app_env = os.getenv("APP_ENV", "development")
        report.add(CheckResult(
            name="config.APP_ENV",
            passed=app_env == "production",
            message=f"APP_ENV={app_env!r}" + ("" if app_env == "production" else " (should be 'production' in prod)"),
            severity="warning" if app_env != "production" else "error",
        ))

        # Warn if debug logging is on in production
        log_level = os.getenv("LOG_LEVEL", "INFO")
        if app_env == "production" and log_level.upper() == "DEBUG":
            report.add(CheckResult(
                name="config.LOG_LEVEL",
                passed=False,
                message="LOG_LEVEL=DEBUG in production leaks sensitive data — set LOG_LEVEL=INFO",
                severity="warning",
            ))


class CorsValidator:
    """Validates CORS_ORIGINS is production-safe."""

    LOCALHOST_PATTERN = re.compile(r'https?://(localhost|127\.0\.0\.1)', re.IGNORECASE)

    def validate(self, report: ValidationReport) -> None:
        origins = os.getenv("CORS_ORIGINS", "")
        if not origins:
            report.add(CheckResult(
                name="config.CORS_ORIGINS",
                passed=False,
                message="CORS_ORIGINS not set — API will reject all cross-origin requests",
            ))
            return

        app_env = os.getenv("APP_ENV", "development")
        if app_env == "production" and self.LOCALHOST_PATTERN.search(origins):
            report.add(CheckResult(
                name="config.CORS_ORIGINS.localhost",
                passed=False,
                message=f"CORS_ORIGINS includes localhost in production: {origins!r}. "
                        "Set to your HTTPS domain only.",
                severity="warning",
            ))
        else:
            report.add(CheckResult(
                name="config.CORS_ORIGINS",
                passed=True,
                message=origins,
            ))

        # Wildcard is a critical misconfiguration
        if "*" in origins:
            report.add(CheckResult(
                name="config.CORS_ORIGINS.wildcard",
                passed=False,
                message="CORS_ORIGINS='*' allows any origin — this bypasses all CORS protection",
            ))


class CookieValidator:
    """Validates secure cookie configuration."""

    def validate(self, report: ValidationReport) -> None:
        secure = os.getenv("AUTH_COOKIE_SECURE", "false").lower()
        app_env = os.getenv("APP_ENV", "development")

        if app_env == "production" and secure != "true":
            report.add(CheckResult(
                name="config.AUTH_COOKIE_SECURE",
                passed=False,
                message="AUTH_COOKIE_SECURE=false in production — session cookies not Secure-flagged. "
                        "Set AUTH_COOKIE_SECURE=true and serve over HTTPS.",
            ))
        else:
            report.add(CheckResult(
                name="config.AUTH_COOKIE_SECURE",
                passed=True,
                message=f"AUTH_COOKIE_SECURE={secure}",
            ))

        samesite = os.getenv("AUTH_COOKIE_SAMESITE", "lax").lower()
        if samesite not in {"strict", "lax", "none"}:
            report.add(CheckResult(
                name="config.AUTH_COOKIE_SAMESITE",
                passed=False,
                message=f"AUTH_COOKIE_SAMESITE={samesite!r} is invalid — use 'strict', 'lax', or 'none'",
            ))


class DatabaseURLValidator:
    """Validates DATABASE_URL format and safety."""

    ASYNC_DRIVERS = {"postgresql+asyncpg", "postgres+asyncpg"}

    def validate(self, report: ValidationReport) -> None:
        db_url = os.getenv("DATABASE_URL", "")
        if not db_url:
            return  # caught by ConfigValidator

        # Must use async driver for FastAPI / asyncpg
        scheme = db_url.split("://")[0] if "://" in db_url else ""
        if scheme not in self.ASYNC_DRIVERS:
            report.add(CheckResult(
                name="config.DATABASE_URL.driver",
                passed=False,
                message=f"DATABASE_URL uses driver {scheme!r} — FastAPI requires postgresql+asyncpg",
            ))
        else:
            report.add(CheckResult(
                name="config.DATABASE_URL.driver",
                passed=True,
                message=f"async driver: {scheme} ✓",
            ))

        # Warn if connecting to localhost (expected: postgres hostname = docker service)
        if "localhost" in db_url or "127.0.0.1" in db_url:
            report.add(CheckResult(
                name="config.DATABASE_URL.host",
                passed=False,
                message="DATABASE_URL points to localhost — in Docker use the service name 'postgres'",
                severity="warning",
            ))


class DetectionEngineValidator:
    """Validates the baked-in detection engine is present."""

    def validate(self, report: ValidationReport) -> None:
        de_path = os.getenv("DETECTION_ENGINE_PATH", "/opt/detection_engine")
        if os.path.isdir(de_path):
            # Check for at least one expected file (adjust to your actual structure)
            contents = os.listdir(de_path) if os.path.isdir(de_path) else []
            if contents:
                report.add(CheckResult(
                    name="detection_engine.path",
                    passed=True,
                    message=f"{de_path} present ({len(contents)} items)",
                ))
            else:
                report.add(CheckResult(
                    name="detection_engine.path",
                    passed=False,
                    message=f"{de_path} exists but is EMPTY — detection_engine was not baked into the image",
                ))
        else:
            report.add(CheckResult(
                name="detection_engine.path",
                passed=False,
                message=f"DETECTION_ENGINE_PATH={de_path!r} does not exist — rebuild image with: "
                        "docker compose build api",
            ))


# ── Async connectivity validators ─────────────────────────────────────────────

class DatabaseConnectivityValidator:
    """Verifies actual database connectivity at startup."""

    async def validate(self, report: ValidationReport) -> None:
        try:
            import asyncpg  # type: ignore
        except ImportError:
            report.add(CheckResult(
                name="db.connectivity",
                passed=False,
                message="asyncpg not installed — cannot verify DB connection",
                severity="warning",
            ))
            return

        db_url = os.getenv("DATABASE_URL", "")
        # asyncpg uses postgres:// not postgresql+asyncpg://
        connect_url = db_url.replace("postgresql+asyncpg://", "postgresql://").replace("postgres+asyncpg://", "postgresql://")
        try:
            conn = await asyncio.wait_for(
                asyncpg.connect(connect_url),
                timeout=10,
            )
            version = await conn.fetchval("SELECT version()")
            await conn.close()
            report.add(CheckResult(
                name="db.connectivity",
                passed=True,
                message=f"connected: {version.split(',')[0]}",
            ))
        except asyncio.TimeoutError:
            report.add(CheckResult(
                name="db.connectivity",
                passed=False,
                message="database connection timed out (10s) — is postgres running?",
            ))
        except Exception as e:
            report.add(CheckResult(
                name="db.connectivity",
                passed=False,
                message=f"database connection failed: {e}",
            ))


class RedisConnectivityValidator:
    """Verifies Redis connectivity at startup."""

    async def validate(self, report: ValidationReport) -> None:
        try:
            import redis.asyncio as aioredis  # type: ignore
        except ImportError:
            report.add(CheckResult(
                name="redis.connectivity",
                passed=False,
                message="redis-py not installed — cannot verify Redis connection",
                severity="warning",
            ))
            return

        redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")
        try:
            client = aioredis.from_url(redis_url, socket_timeout=5)
            pong = await asyncio.wait_for(client.ping(), timeout=5)
            await client.aclose()
            if pong:
                report.add(CheckResult(
                    name="redis.connectivity",
                    passed=True,
                    message="PING → PONG ✓",
                ))
        except asyncio.TimeoutError:
            report.add(CheckResult(
                name="redis.connectivity",
                passed=False,
                message="Redis connection timed out (5s) — is redis running?",
            ))
        except Exception as e:
            report.add(CheckResult(
                name="redis.connectivity",
                passed=False,
                message=f"Redis connection failed: {e}",
            ))


# ── Orchestrator ──────────────────────────────────────────────────────────────

async def run_all_validators(*, raise_on_error: bool = True) -> ValidationReport:
    """
    Run all validators. Use in FastAPI lifespan:

        from scripts.startup_validator import run_all_validators
        async def lifespan(app):
            await run_all_validators()
            yield
    """
    report = ValidationReport()
    t0 = time.monotonic()

    # Sync validators
    for validator_cls in [
        ConfigValidator,
        SecretsValidator,
        AppEnvironmentValidator,
        CorsValidator,
        CookieValidator,
        DatabaseURLValidator,
        DetectionEngineValidator,
    ]:
        try:
            validator_cls().validate(report)
        except Exception as e:
            report.add(CheckResult(
                name=validator_cls.__name__,
                passed=False,
                message=f"validator raised unexpected exception: {e}",
            ))

    # Async validators (connectivity — run concurrently)
    async_validators: list[Callable[[], Awaitable[None]]] = [
        DatabaseConnectivityValidator().validate,
        RedisConnectivityValidator().validate,
    ]
    await asyncio.gather(
        *[v(report) for v in async_validators],
        return_exceptions=True,
    )

    elapsed = time.monotonic() - t0
    print(f"\n\033[1;37m── Startup Validation ({elapsed:.1f}s) ──────────────────────\033[0m")
    report.print_summary()

    if report.warnings:
        print(f"\n  {len(report.warnings)} warning(s) — review before going live")
    if report.errors:
        print(f"\n  \033[31m{len(report.errors)} error(s) — startup blocked\033[0m")

    if raise_on_error:
        report.raise_if_errors()

    return report


# ── CLI entrypoint ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    try:
        report = asyncio.run(run_all_validators(raise_on_error=False))
        sys.exit(0 if not report.errors else 1)
    except KeyboardInterrupt:
        sys.exit(1)

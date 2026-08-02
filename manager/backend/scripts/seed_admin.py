"""
Idempotent admin seeder — production-grade rewrite.

Behavior:
  First run : creates a tenant (if missing) + admin user, verifies the hash.
  Re-run    : no-op (user already exists). Logs a clear message.
  Rotation  : SEED_ADMIN_FORCE_RESET=true rotates the existing admin's password,
              verifies the new hash, and commits in a single transaction.

Exit codes:
  0  — success (seeded, or idempotent no-op, or rotation complete)
  2  — configuration error (bad env, weak password in production)
  3  — database unavailable (transient or permanent)
  4  — unexpected error / hash verification failure

Configuration drift detection:
  If > 1 admin user exists in the tenant, or the seeded email doesn't match the
  current SEED_ADMIN_EMAIL, a WARNING is emitted — human review is needed.

Usage:
  python scripts/seed_admin.py
  SEED_ADMIN_FORCE_RESET=true python scripts/seed_admin.py
"""

from __future__ import annotations

import asyncio
import json
import os
import sys
import time
from datetime import datetime, timezone

# Make the repo root importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from passlib.context import CryptContext
from sqlalchemy import func, select
from sqlalchemy.exc import OperationalError, SQLAlchemyError

from app.auth.exceptions import (
    DatabaseUnavailableError,
    PasswordRotationError,
    SeedConfigurationError,
)
from app.database import AsyncSessionLocal
from app.models.enums import UserRole
from app.models.tenant import Tenant
from app.models.user import User

_pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Passwords that must never be used in production
_KNOWN_WEAK_PASSWORDS: frozenset[str] = frozenset({
    "ChangeMe123!",
    "admin",
    "password",
    "Password123!",
    "Admin123!",
    "changeme",
    "secret",
    "vedha",
})

_MAX_RETRIES = 5
_RETRY_BASE_DELAY = 1.0   # seconds, doubles each attempt


# ── Structured logger (no third-party dep — writes JSON to stdout) ────────────

def _log(level: str, event: str, **fields: object) -> None:
    record = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "level": level,
        "event": event,
        **fields,
    }
    print(json.dumps(record), flush=True)


def log_info(event: str, **fields: object) -> None:
    _log("INFO", event, **fields)


def log_warn(event: str, **fields: object) -> None:
    _log("WARNING", event, **fields)


def log_error(event: str, **fields: object) -> None:
    _log("ERROR", event, **fields)


# ── Environment validation ────────────────────────────────────────────────────

def _validate_env() -> tuple[str, str, str, bool]:
    """
    Returns (email, password, tenant_name, force_reset).
    Raises SeedConfigurationError on any violation.
    """
    email = os.getenv("SEED_ADMIN_EMAIL", "").strip()
    if not email:
        raise SeedConfigurationError(
            "SEED_ADMIN_EMAIL is not set — seeder cannot run without it.",
        )

    password = os.getenv("SEED_ADMIN_PASSWORD", "ChangeMe123!")
    tenant_name = os.getenv("SEED_TENANT_NAME", "Default Tenant")
    force_reset = os.getenv("SEED_ADMIN_FORCE_RESET", "").strip().lower() in {
        "1", "true", "yes", "on"
    }
    app_env = os.getenv("APP_ENV", "development").lower()

    # In production, block known-weak passwords entirely.
    if app_env == "production" and password in _KNOWN_WEAK_PASSWORDS:
        raise SeedConfigurationError(
            f"SEED_ADMIN_PASSWORD is a known-weak value. "
            f"Refusing to seed in production (APP_ENV=production). "
            f"Set a strong password in SSM or .env.",
        )

    if len(password) < 12:
        if app_env == "production":
            raise SeedConfigurationError(
                "SEED_ADMIN_PASSWORD is too short (< 12 chars) for production.",
            )
        else:
            log_warn("seed.weak_password", length=len(password),
                     hint="Increase to ≥12 chars before going to production.")

    return email, password, tenant_name, force_reset


# ── Hash helpers ──────────────────────────────────────────────────────────────

def _hash(password: str) -> str:
    return _pwd.hash(password)


def _verify_hash(password: str, hashed: str) -> bool:
    try:
        return _pwd.verify(password, hashed)
    except Exception as exc:
        raise PasswordRotationError(
            f"bcrypt verification raised an exception after write: {exc}"
        ) from exc


# ── Drift detection ───────────────────────────────────────────────────────────

async def _detect_drift(db, tenant: Tenant, seeded_email: str) -> None:
    """Warn if the tenant has multiple admins or a stale admin email."""
    admin_count = (
        await db.execute(
            select(func.count(User.id)).where(
                User.tenant_id == tenant.id,
                User.role == UserRole.admin,
            )
        )
    ).scalar_one()

    if admin_count > 1:
        log_warn(
            "seed.drift.multiple_admins",
            tenant_id=str(tenant.id),
            admin_count=admin_count,
            action="review_and_disable_stale_accounts",
        )

    # If the current SEED_ADMIN_EMAIL differs from any existing admin, we may
    # have an orphaned account from a previous deploy.
    all_admin_emails = (
        await db.execute(
            select(User.email).where(
                User.tenant_id == tenant.id,
                User.role == UserRole.admin,
            )
        )
    ).scalars().all()

    stale = [e for e in all_admin_emails if e != seeded_email]
    if stale:
        log_warn(
            "seed.drift.stale_admin_emails",
            seeded_email=seeded_email,
            stale_emails=stale,
            action="disable_or_delete_stale_admins",
        )


# ── Core seeder ───────────────────────────────────────────────────────────────

async def _seed_once(email: str, password: str, tenant_name: str, force_reset: bool) -> None:
    """
    All DB work in a single transaction. Rolls back on any failure.
    Verifies the bcrypt hash after every write.
    """
    async with AsyncSessionLocal() as db:
        async with db.begin():
            # ── Check existing user ────────────────────────────────────────
            existing_user = (
                await db.execute(select(User).where(User.email == email))
            ).scalar_one_or_none()

            if existing_user:
                # ── Drift detection (non-blocking) ─────────────────────────
                tenant = (
                    await db.execute(
                        select(Tenant).where(Tenant.id == existing_user.tenant_id)
                    )
                ).scalar_one_or_none()
                if tenant:
                    await _detect_drift(db, tenant, email)

                if not force_reset:
                    log_info(
                        "seed.noop",
                        email=email,
                        user_id=str(existing_user.id),
                        is_active=existing_user.is_active,
                        hint="Set SEED_ADMIN_FORCE_RESET=true to rotate the password.",
                    )
                    return

                # ── Password rotation ──────────────────────────────────────
                new_hash = _hash(password)
                existing_user.hashed_password = new_hash

                # Force flush so the hash is written to DB before we verify
                await db.flush()
                await db.refresh(existing_user)

                # Verify: read the stored hash back and check it matches
                if not _verify_hash(password, existing_user.hashed_password):
                    raise PasswordRotationError(
                        f"Hash verification failed after rotation for {email}. "
                        "Transaction will be rolled back."
                    )

                log_info(
                    "seed.password_rotated",
                    email=email,
                    user_id=str(existing_user.id),
                    hash_verified=True,
                )
                return

            # ── First run: create tenant + admin ──────────────────────────
            tenant = (
                await db.execute(select(Tenant).where(Tenant.name == tenant_name))
            ).scalar_one_or_none()

            if tenant is None:
                tenant = Tenant(name=tenant_name, is_active=True)
                db.add(tenant)
                await db.flush()
                log_info("seed.tenant_created", name=tenant_name, tenant_id=str(tenant.id))

            elif not tenant.is_active:
                raise SeedConfigurationError(
                    f"Tenant '{tenant_name}' exists but is_active=False. "
                    "Refusing to seed an admin into a disabled tenant."
                )

            new_hash = _hash(password)
            new_user = User(
                tenant_id=tenant.id,
                email=email,
                hashed_password=new_hash,
                role=UserRole.admin,
                is_active=True,
            )
            db.add(new_user)
            await db.flush()
            await db.refresh(new_user)

            # Verify the stored hash matches the password we just hashed
            if not _verify_hash(password, new_user.hashed_password):
                raise PasswordRotationError(
                    f"Hash verification failed after creating {email}. "
                    "Transaction will be rolled back."
                )

            log_info(
                "seed.admin_created",
                email=email,
                user_id=str(new_user.id),
                tenant_id=str(tenant.id),
                tenant_name=tenant_name,
                hash_verified=True,
                is_active=True,
            )


async def _seed_with_retry(email: str, password: str, tenant_name: str, force_reset: bool) -> None:
    """Exponential-backoff retry for transient DB connectivity issues."""
    last_exc: Exception | None = None
    for attempt in range(1, _MAX_RETRIES + 1):
        try:
            await _seed_once(email, password, tenant_name, force_reset)
            return
        except (OperationalError, OSError) as exc:
            # Transient: DB not ready, connection reset, etc.
            last_exc = exc
            if attempt < _MAX_RETRIES:
                delay = _RETRY_BASE_DELAY * (2 ** (attempt - 1))
                log_warn(
                    "seed.db_transient_error",
                    attempt=attempt,
                    max_retries=_MAX_RETRIES,
                    retry_in_s=delay,
                    error=str(exc),
                )
                await asyncio.sleep(delay)
            else:
                log_error(
                    "seed.db_unavailable",
                    attempts=_MAX_RETRIES,
                    error=str(exc),
                )
                raise DatabaseUnavailableError(
                    f"Database unreachable after {_MAX_RETRIES} attempts: {exc}"
                ) from exc
        except SQLAlchemyError as exc:
            # Non-transient DB error (constraint violation, bad query, etc.)
            log_error("seed.db_error", error=str(exc), exc_type=type(exc).__name__)
            raise


# ── Entry point ───────────────────────────────────────────────────────────────

async def main() -> None:
    t0 = time.monotonic()
    log_info("seed.start", pid=os.getpid())

    try:
        email, password, tenant_name, force_reset = _validate_env()
    except SeedConfigurationError as exc:
        log_error("seed.config_error", error=str(exc))
        sys.exit(2)

    log_info(
        "seed.config",
        email=email,
        tenant_name=tenant_name,
        force_reset=force_reset,
        app_env=os.getenv("APP_ENV", "development"),
    )

    try:
        await _seed_with_retry(email, password, tenant_name, force_reset)
    except DatabaseUnavailableError as exc:
        log_error("seed.fatal", error=str(exc))
        sys.exit(3)
    except (SeedConfigurationError, PasswordRotationError) as exc:
        log_error("seed.fatal", error=str(exc))
        sys.exit(2)
    except Exception as exc:
        log_error("seed.unexpected_error", error=str(exc), exc_type=type(exc).__name__)
        sys.exit(4)

    elapsed = round((time.monotonic() - t0) * 1000, 1)
    log_info("seed.complete", elapsed_ms=elapsed)


if __name__ == "__main__":
    asyncio.run(main())

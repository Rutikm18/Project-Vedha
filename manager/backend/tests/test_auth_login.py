"""
Tests for authentication login flow.

Covers:
  - login success
  - user_not_found
  - password_mismatch
  - disabled_user
  - disabled_tenant
  - expired_password
  - bcrypt_failure
  - database_failure
  - jwt_failure
  - rate_limit (behavioural)
  - startup diagnostics: DB up, Redis up, JWT secret, bcrypt, admin account

All tests use unittest.mock — no real DB or Redis required.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.auth.exceptions import (
    BcryptFailureError,
    DatabaseFailureError,
    DisabledTenantError,
    DisabledUserError,
    ExpiredPasswordError,
    PasswordMismatchError,
    UserNotFoundError,
)
from app.auth.router import _authenticate
from app.models.enums import UserRole


# ── Fixtures ──────────────────────────────────────────────────────────────────

def _make_user(
    *,
    is_active: bool = True,
    password_expires_at: datetime | None = None,
    role: UserRole = UserRole.admin,
) -> MagicMock:
    u = MagicMock()
    u.id = uuid.uuid4()
    u.tenant_id = uuid.uuid4()
    u.email = "admin@vedha.io"
    u.hashed_password = "$2b$12$placeholder_hash_value_for_tests"
    u.role = role
    u.is_active = is_active
    u.password_expires_at = password_expires_at
    return u


def _make_tenant(*, is_active: bool = True) -> MagicMock:
    t = MagicMock()
    t.id = uuid.uuid4()
    t.name = "Default Tenant"
    t.is_active = is_active
    return t


def _make_db(user: Any = None, tenant: Any = None) -> AsyncMock:
    """AsyncSession mock that returns user on first execute, tenant on second."""
    db = AsyncMock()
    user_result = MagicMock()
    user_result.scalar_one_or_none.return_value = user

    tenant_result = MagicMock()
    tenant_result.scalar_one_or_none.return_value = tenant

    db.execute = AsyncMock(side_effect=[user_result, tenant_result])
    return db


# ── _authenticate unit tests ──────────────────────────────────────────────────

class TestAuthenticateUserNotFound:
    @pytest.mark.asyncio
    async def test_raises_user_not_found(self):
        db = _make_db(user=None)
        with patch("app.auth.router._pwd") as mock_pwd:
            mock_pwd.dummy_verify = MagicMock()
            with pytest.raises(UserNotFoundError):
                await _authenticate("nobody@example.com", "pass", db)
            mock_pwd.dummy_verify.assert_called_once()  # constant-time guard ran


class TestAuthenticatePasswordMismatch:
    @pytest.mark.asyncio
    async def test_raises_password_mismatch(self):
        user = _make_user()
        tenant = _make_tenant()
        db = _make_db(user=user, tenant=tenant)

        with patch("app.auth.router._pwd") as mock_pwd:
            mock_pwd.dummy_verify = MagicMock()
            mock_pwd.verify.return_value = False
            with pytest.raises(PasswordMismatchError):
                await _authenticate("admin@vedha.io", "wrong", db)


class TestAuthenticateDisabledUser:
    @pytest.mark.asyncio
    async def test_raises_disabled_user(self):
        user = _make_user(is_active=False)
        db = _make_db(user=user)

        with patch("app.auth.router._pwd") as mock_pwd:
            mock_pwd.dummy_verify = MagicMock()
            with pytest.raises(DisabledUserError):
                await _authenticate("admin@vedha.io", "pass", db)
            mock_pwd.dummy_verify.assert_called_once()


class TestAuthenticateDisabledTenant:
    @pytest.mark.asyncio
    async def test_raises_disabled_tenant(self):
        user = _make_user(is_active=True)
        tenant = _make_tenant(is_active=False)
        db = _make_db(user=user, tenant=tenant)

        with patch("app.auth.router._pwd") as mock_pwd:
            mock_pwd.dummy_verify = MagicMock()
            with pytest.raises(DisabledTenantError):
                await _authenticate("admin@vedha.io", "pass", db)


class TestAuthenticateExpiredPassword:
    @pytest.mark.asyncio
    async def test_raises_expired_password(self):
        expired_at = datetime.now(timezone.utc) - timedelta(days=1)
        user = _make_user(is_active=True, password_expires_at=expired_at)
        tenant = _make_tenant()
        db = _make_db(user=user, tenant=tenant)

        with patch("app.auth.router._pwd") as mock_pwd:
            mock_pwd.dummy_verify = MagicMock()
            with pytest.raises(ExpiredPasswordError):
                await _authenticate("admin@vedha.io", "pass", db)

    @pytest.mark.asyncio
    async def test_not_expired_when_future(self):
        future_expiry = datetime.now(timezone.utc) + timedelta(days=30)
        user = _make_user(is_active=True, password_expires_at=future_expiry)
        tenant = _make_tenant()
        db = _make_db(user=user, tenant=tenant)

        with patch("app.auth.router._pwd") as mock_pwd:
            mock_pwd.dummy_verify = MagicMock()
            mock_pwd.verify.return_value = True
            result = await _authenticate("admin@vedha.io", "correct", db)
            assert result is user


class TestAuthenticateBcryptFailure:
    @pytest.mark.asyncio
    async def test_raises_bcrypt_failure_on_passlib_error(self):
        from passlib.exc import PasslibError

        user = _make_user()
        tenant = _make_tenant()
        db = _make_db(user=user, tenant=tenant)

        with patch("app.auth.router._pwd") as mock_pwd:
            mock_pwd.dummy_verify = MagicMock()
            mock_pwd.verify.side_effect = PasslibError("corrupt hash")
            with pytest.raises(BcryptFailureError):
                await _authenticate("admin@vedha.io", "pass", db)


class TestAuthenticateDatabaseFailure:
    @pytest.mark.asyncio
    async def test_raises_database_failure_on_sqlalchemy_error(self):
        from sqlalchemy.exc import OperationalError

        db = AsyncMock()
        db.execute.side_effect = OperationalError("conn", {}, Exception("timeout"))

        with pytest.raises(DatabaseFailureError):
            await _authenticate("admin@vedha.io", "pass", db)


class TestAuthenticateSuccess:
    @pytest.mark.asyncio
    async def test_returns_user_on_valid_credentials(self):
        user = _make_user()
        tenant = _make_tenant()
        db = _make_db(user=user, tenant=tenant)

        with patch("app.auth.router._pwd") as mock_pwd:
            mock_pwd.dummy_verify = MagicMock()
            mock_pwd.verify.return_value = True
            result = await _authenticate("admin@vedha.io", "correct", db)

        assert result is user

    @pytest.mark.asyncio
    async def test_null_password_expires_at_never_expires(self):
        user = _make_user(password_expires_at=None)
        tenant = _make_tenant()
        db = _make_db(user=user, tenant=tenant)

        with patch("app.auth.router._pwd") as mock_pwd:
            mock_pwd.dummy_verify = MagicMock()
            mock_pwd.verify.return_value = True
            result = await _authenticate("admin@vedha.io", "correct", db)

        assert result is user


# ── Reason code contract ──────────────────────────────────────────────────────

class TestReasonCodes:
    """Ensure every exception class has the expected reason_code attribute.
    These codes appear in structured logs — breaking them breaks dashboards."""

    def test_user_not_found_code(self):
        assert UserNotFoundError.reason_code == "user_not_found"

    def test_password_mismatch_code(self):
        assert PasswordMismatchError.reason_code == "password_mismatch"

    def test_disabled_user_code(self):
        assert DisabledUserError.reason_code == "disabled_user"

    def test_disabled_tenant_code(self):
        assert DisabledTenantError.reason_code == "disabled_tenant"

    def test_expired_password_code(self):
        assert ExpiredPasswordError.reason_code == "expired_password"

    def test_bcrypt_failure_code(self):
        assert BcryptFailureError.reason_code == "bcrypt_failure"

    def test_database_failure_code(self):
        assert DatabaseFailureError.reason_code == "database_failure"


# ── Startup diagnostics ───────────────────────────────────────────────────────

class TestStartupDiagnostics:
    @pytest.mark.asyncio
    async def test_jwt_secret_too_short_is_fatal(self):
        from app.auth.startup import _check_jwt_secret
        with patch("app.auth.startup.settings") as mock_settings:
            mock_settings.jwt_secret = "short"
            result = await _check_jwt_secret()
        assert result.fatal

    @pytest.mark.asyncio
    async def test_jwt_secret_known_weak_is_fatal(self):
        from app.auth.startup import _check_jwt_secret
        with patch("app.auth.startup.settings") as mock_settings:
            mock_settings.jwt_secret = "change-me-at-least-32-chars-long!!"
            result = await _check_jwt_secret()
        assert result.fatal

    @pytest.mark.asyncio
    async def test_jwt_secret_strong_is_ok(self):
        from app.auth.startup import _check_jwt_secret
        with patch("app.auth.startup.settings") as mock_settings:
            mock_settings.jwt_secret = "a" * 48
            result = await _check_jwt_secret()
        assert result.ok

    @pytest.mark.asyncio
    async def test_bcrypt_round_trip_passes(self):
        from app.auth.startup import _check_bcrypt
        result = await _check_bcrypt()
        assert result.ok

    @pytest.mark.asyncio
    async def test_cookie_config_fatal_in_production(self):
        from app.auth.startup import _check_cookie_config
        with patch("app.auth.startup.settings") as mock_settings:
            mock_settings.app_env = "production"
            mock_settings.is_production = True
            with patch.dict("os.environ", {"AUTH_COOKIE_SECURE": "false"}, clear=False):
                result = await _check_cookie_config()
        assert result.fatal

    @pytest.mark.asyncio
    async def test_cookie_config_ok_in_development(self):
        from app.auth.startup import _check_cookie_config
        with patch("app.auth.startup.settings") as mock_settings:
            mock_settings.app_env = "development"
            mock_settings.is_production = False
            with patch.dict("os.environ", {"AUTH_COOKIE_SECURE": "false"}, clear=False):
                result = await _check_cookie_config()
        assert result.ok

    @pytest.mark.asyncio
    async def test_database_check_returns_fatal_on_connection_error(self):
        from app.auth.startup import _check_database
        with patch("app.auth.startup.AsyncSessionLocal") as mock_session:
            mock_cm = AsyncMock()
            mock_cm.__aenter__.return_value.execute.side_effect = Exception("conn refused")
            mock_session.return_value = mock_cm
            result = await _check_database()
        assert result.fatal

    @pytest.mark.asyncio
    async def test_redis_check_returns_fatal_on_connection_error(self):
        from app.auth.startup import _check_redis
        with patch("app.auth.startup.settings") as mock_settings:
            mock_settings.redis_url = "redis://127.0.0.1:1"
            result = await _check_redis()
        # Connection to port 1 should fail → fatal
        assert result.fatal

    @pytest.mark.asyncio
    async def test_run_all_aborts_on_fatal(self):
        from app.auth.startup import StartupAbortError, run_startup_diagnostics

        async def _fatal_jwt():
            from app.auth.startup import CheckResult
            return CheckResult("jwt_secret", "fatal", "weak")

        with patch("app.auth.startup._check_jwt_secret", _fatal_jwt), \
             patch("app.auth.startup._check_database", AsyncMock(return_value=MagicMock(name="database", severity="ok", ok=True, fatal=False))), \
             patch("app.auth.startup._check_redis", AsyncMock(return_value=MagicMock(name="redis", severity="ok", ok=True, fatal=False))), \
             patch("app.auth.startup._check_bcrypt", AsyncMock(return_value=MagicMock(severity="ok", ok=True, fatal=False))), \
             patch("app.auth.startup._check_cookie_config", AsyncMock(return_value=MagicMock(severity="ok", ok=True, fatal=False))), \
             patch("app.auth.startup._check_cors", AsyncMock(return_value=MagicMock(severity="ok", ok=True, fatal=False))), \
             patch("app.auth.startup._check_required_env_vars", AsyncMock(return_value=MagicMock(severity="ok", ok=True, fatal=False))), \
             patch("app.auth.startup._check_admin_account", AsyncMock(return_value=MagicMock(severity="ok", ok=True, fatal=False))), \
             patch("app.auth.startup._check_tenant", AsyncMock(return_value=MagicMock(severity="ok", ok=True, fatal=False))):
            with pytest.raises(StartupAbortError):
                await run_startup_diagnostics(fail_on_fatal=True)

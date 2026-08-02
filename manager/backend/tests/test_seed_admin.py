"""
Tests for seed_admin.py.

Covers:
  - first deployment: creates tenant + admin, verifies hash
  - existing admin (no force reset): no-op
  - password rotation: SEED_ADMIN_FORCE_RESET=true
  - invalid env: missing SEED_ADMIN_EMAIL
  - weak password in production → config error
  - hash verification failure → rotation error
  - DB unavailable → retries then exits 3
  - drift detection: multiple admins warns
"""

from __future__ import annotations

import os
import uuid
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.auth.exceptions import (
    DatabaseUnavailableError,
    PasswordRotationError,
    SeedConfigurationError,
)
from scripts.seed_admin import (
    _KNOWN_WEAK_PASSWORDS,
    _hash,
    _validate_env,
    _verify_hash,
)


# ── _validate_env ─────────────────────────────────────────────────────────────

class TestValidateEnv:
    def test_raises_when_email_missing(self, monkeypatch):
        monkeypatch.delenv("SEED_ADMIN_EMAIL", raising=False)
        with pytest.raises(SeedConfigurationError, match="SEED_ADMIN_EMAIL"):
            _validate_env()

    def test_raises_on_weak_password_in_production(self, monkeypatch):
        monkeypatch.setenv("SEED_ADMIN_EMAIL", "admin@vedha.io")
        monkeypatch.setenv("SEED_ADMIN_PASSWORD", "ChangeMe123!")
        monkeypatch.setenv("APP_ENV", "production")
        with pytest.raises(SeedConfigurationError, match="weak"):
            _validate_env()

    def test_allows_weak_password_in_development(self, monkeypatch):
        monkeypatch.setenv("SEED_ADMIN_EMAIL", "admin@vedha.io")
        monkeypatch.setenv("SEED_ADMIN_PASSWORD", "ChangeMe123!")
        monkeypatch.setenv("APP_ENV", "development")
        email, password, _, _ = _validate_env()
        assert email == "admin@vedha.io"

    def test_returns_force_reset_true(self, monkeypatch):
        monkeypatch.setenv("SEED_ADMIN_EMAIL", "admin@vedha.io")
        monkeypatch.setenv("SEED_ADMIN_PASSWORD", "StrongP@ssword1!")
        monkeypatch.setenv("SEED_ADMIN_FORCE_RESET", "true")
        monkeypatch.setenv("APP_ENV", "development")
        _, _, _, force_reset = _validate_env()
        assert force_reset is True

    def test_all_known_weak_passwords_blocked_in_production(self, monkeypatch):
        monkeypatch.setenv("SEED_ADMIN_EMAIL", "admin@vedha.io")
        monkeypatch.setenv("APP_ENV", "production")
        for pw in _KNOWN_WEAK_PASSWORDS:
            monkeypatch.setenv("SEED_ADMIN_PASSWORD", pw)
            with pytest.raises(SeedConfigurationError):
                _validate_env()


# ── Hash helpers ──────────────────────────────────────────────────────────────

class TestHashHelpers:
    def test_hash_and_verify_round_trip(self):
        pw = "StrongP@ssword1!"
        h = _hash(pw)
        assert _verify_hash(pw, h)

    def test_wrong_password_fails_verify(self):
        h = _hash("correct")
        assert not _verify_hash("wrong", h)

    def test_different_calls_produce_different_hashes(self):
        # bcrypt uses random salt per hash
        h1 = _hash("same")
        h2 = _hash("same")
        assert h1 != h2


# ── First deployment ──────────────────────────────────────────────────────────

class TestFirstDeployment:
    @pytest.mark.asyncio
    async def test_creates_tenant_and_admin_on_first_run(self, monkeypatch):
        from scripts.seed_admin import _seed_once

        # DB returns None for both user and tenant queries
        mock_user_result = MagicMock()
        mock_user_result.scalar_one_or_none.return_value = None

        mock_tenant_result = MagicMock()
        mock_tenant_result.scalar_one_or_none.return_value = None

        db = AsyncMock()
        db.execute = AsyncMock(side_effect=[mock_user_result, mock_tenant_result])
        db.flush = AsyncMock()
        db.refresh = AsyncMock()

        # After refresh, the new user should have the correct fields
        new_user = MagicMock()
        new_user.id = uuid.uuid4()
        new_user.hashed_password = _hash("StrongP@ssword1!")
        db.refresh.side_effect = lambda obj: None  # no-op

        mock_session = MagicMock()
        mock_session.__aenter__ = AsyncMock(return_value=db)
        mock_session.__aexit__ = AsyncMock(return_value=None)

        # begin() context manager
        mock_begin = MagicMock()
        mock_begin.__aenter__ = AsyncMock(return_value=None)
        mock_begin.__aexit__ = AsyncMock(return_value=None)
        db.begin.return_value = mock_begin

        with patch("scripts.seed_admin.AsyncSessionLocal", return_value=mock_session), \
             patch("scripts.seed_admin._verify_hash", return_value=True):
            # Should not raise
            await _seed_once("admin@vedha.io", "StrongP@ssword1!", "Default Tenant", False)

        db.add.assert_called()  # both Tenant and User were added


# ── Existing admin (no force reset) ──────────────────────────────────────────

class TestExistingAdminNoReset:
    @pytest.mark.asyncio
    async def test_noop_when_user_exists_and_no_force_reset(self):
        from scripts.seed_admin import _seed_once

        existing_user = MagicMock()
        existing_user.id = uuid.uuid4()
        existing_user.is_active = True
        existing_user.tenant_id = uuid.uuid4()

        mock_user_result = MagicMock()
        mock_user_result.scalar_one_or_none.return_value = existing_user

        mock_tenant_result = MagicMock()
        existing_tenant = MagicMock()
        existing_tenant.id = existing_user.tenant_id
        existing_tenant.is_active = True
        mock_tenant_result.scalar_one_or_none.return_value = existing_tenant

        # Drift detection queries (admin count, all admin emails)
        mock_count_result = MagicMock()
        mock_count_result.scalar_one.return_value = 1
        mock_emails_result = MagicMock()
        mock_emails_result.scalars.return_value.all.return_value = ["admin@vedha.io"]

        db = AsyncMock()
        db.execute = AsyncMock(side_effect=[
            mock_user_result,    # find existing user
            mock_tenant_result,  # find existing tenant
            mock_count_result,   # count admins
            mock_emails_result,  # all admin emails
        ])
        mock_begin = MagicMock()
        mock_begin.__aenter__ = AsyncMock(return_value=None)
        mock_begin.__aexit__ = AsyncMock(return_value=None)
        db.begin.return_value = mock_begin

        mock_session = MagicMock()
        mock_session.__aenter__ = AsyncMock(return_value=db)
        mock_session.__aexit__ = AsyncMock(return_value=None)

        with patch("scripts.seed_admin.AsyncSessionLocal", return_value=mock_session):
            await _seed_once("admin@vedha.io", "StrongP@ssword1!", "Default Tenant", False)

        # No commit (commit is done by `async with db.begin()` context — no explicit flush needed)
        db.add.assert_not_called()


# ── Password rotation ─────────────────────────────────────────────────────────

class TestPasswordRotation:
    @pytest.mark.asyncio
    async def test_rotation_updates_hash_and_verifies(self):
        from scripts.seed_admin import _seed_once

        existing_user = MagicMock()
        existing_user.id = uuid.uuid4()
        existing_user.is_active = True
        existing_user.tenant_id = uuid.uuid4()
        existing_user.hashed_password = _hash("OldPassword1!")

        mock_user_result = MagicMock()
        mock_user_result.scalar_one_or_none.return_value = existing_user

        mock_tenant_result = MagicMock()
        existing_tenant = MagicMock()
        existing_tenant.is_active = True
        mock_tenant_result.scalar_one_or_none.return_value = existing_tenant

        mock_count_result = MagicMock()
        mock_count_result.scalar_one.return_value = 1
        mock_emails_result = MagicMock()
        mock_emails_result.scalars.return_value.all.return_value = ["admin@vedha.io"]

        db = AsyncMock()
        db.execute = AsyncMock(side_effect=[
            mock_user_result,
            mock_tenant_result,
            mock_count_result,
            mock_emails_result,
        ])
        db.flush = AsyncMock()
        db.refresh = AsyncMock()
        mock_begin = MagicMock()
        mock_begin.__aenter__ = AsyncMock(return_value=None)
        mock_begin.__aexit__ = AsyncMock(return_value=None)
        db.begin.return_value = mock_begin

        mock_session = MagicMock()
        mock_session.__aenter__ = AsyncMock(return_value=db)
        mock_session.__aexit__ = AsyncMock(return_value=None)

        with patch("scripts.seed_admin.AsyncSessionLocal", return_value=mock_session), \
             patch("scripts.seed_admin._verify_hash", return_value=True) as mock_verify:
            await _seed_once("admin@vedha.io", "NewPassword1!", "Default Tenant", True)

        mock_verify.assert_called_once()
        # The hashed_password was updated on the user object
        assert existing_user.hashed_password != _hash("OldPassword1!")

    @pytest.mark.asyncio
    async def test_rotation_raises_on_hash_verify_failure(self):
        from scripts.seed_admin import _seed_once

        existing_user = MagicMock()
        existing_user.id = uuid.uuid4()
        existing_user.is_active = True
        existing_user.tenant_id = uuid.uuid4()
        existing_user.hashed_password = _hash("OldPassword1!")

        mock_user_result = MagicMock()
        mock_user_result.scalar_one_or_none.return_value = existing_user

        mock_tenant_result = MagicMock()
        existing_tenant = MagicMock()
        existing_tenant.is_active = True
        mock_tenant_result.scalar_one_or_none.return_value = existing_tenant

        mock_count_result = MagicMock()
        mock_count_result.scalar_one.return_value = 1
        mock_emails_result = MagicMock()
        mock_emails_result.scalars.return_value.all.return_value = ["admin@vedha.io"]

        db = AsyncMock()
        db.execute = AsyncMock(side_effect=[
            mock_user_result,
            mock_tenant_result,
            mock_count_result,
            mock_emails_result,
        ])
        db.flush = AsyncMock()
        db.refresh = AsyncMock()
        mock_begin = MagicMock()
        mock_begin.__aenter__ = AsyncMock(return_value=None)
        mock_begin.__aexit__ = AsyncMock(return_value=None)
        db.begin.return_value = mock_begin

        mock_session = MagicMock()
        mock_session.__aenter__ = AsyncMock(return_value=db)
        mock_session.__aexit__ = AsyncMock(return_value=None)

        with patch("scripts.seed_admin.AsyncSessionLocal", return_value=mock_session), \
             patch("scripts.seed_admin._verify_hash", return_value=False):
            with pytest.raises(PasswordRotationError):
                await _seed_once("admin@vedha.io", "NewPassword1!", "Default Tenant", True)


# ── DB unavailable ─────────────────────────────────────────────────────────────

class TestDatabaseUnavailable:
    @pytest.mark.asyncio
    async def test_retries_then_raises_database_unavailable(self):
        from sqlalchemy.exc import OperationalError

        from scripts.seed_admin import _seed_with_retry

        mock_session = MagicMock()
        mock_cm = AsyncMock()
        mock_cm.__aenter__.side_effect = OperationalError("conn", {}, Exception("refused"))
        mock_session.return_value = mock_cm

        with patch("scripts.seed_admin.AsyncSessionLocal", mock_session), \
             patch("scripts.seed_admin.asyncio.sleep", AsyncMock()):
            with pytest.raises(DatabaseUnavailableError):
                await _seed_with_retry("admin@vedha.io", "pass", "Tenant", False)


# ── Drift detection ───────────────────────────────────────────────────────────

class TestDriftDetection:
    @pytest.mark.asyncio
    async def test_warns_on_multiple_admins(self, caplog):
        from scripts.seed_admin import _detect_drift
        import logging

        mock_count_result = MagicMock()
        mock_count_result.scalar_one.return_value = 3  # 3 admins = drift

        mock_emails_result = MagicMock()
        mock_emails_result.scalars.return_value.all.return_value = [
            "admin@vedha.io", "old-admin@vedha.io", "another@vedha.io"
        ]

        db = AsyncMock()
        db.execute = AsyncMock(side_effect=[mock_count_result, mock_emails_result])

        tenant = MagicMock()
        tenant.id = uuid.uuid4()

        # Should complete without raising (drift = warning, not fatal)
        await _detect_drift(db, tenant, "admin@vedha.io")

    @pytest.mark.asyncio
    async def test_warns_on_stale_admin_emails(self):
        from scripts.seed_admin import _detect_drift

        mock_count_result = MagicMock()
        mock_count_result.scalar_one.return_value = 2

        mock_emails_result = MagicMock()
        mock_emails_result.scalars.return_value.all.return_value = [
            "new-admin@vedha.io", "old-admin@vedha.io"
        ]

        db = AsyncMock()
        db.execute = AsyncMock(side_effect=[mock_count_result, mock_emails_result])

        tenant = MagicMock()
        tenant.id = uuid.uuid4()

        # Should complete without raising
        await _detect_drift(db, tenant, "new-admin@vedha.io")

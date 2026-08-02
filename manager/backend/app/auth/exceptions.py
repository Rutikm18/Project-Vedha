"""
Typed exception hierarchy for Vedha authentication.

Design principle:
  - Every distinct failure mode has its own exception class.
  - All share a `reason_code` attribute — this goes into structured logs only,
    NEVER into API responses. The route handler maps everything to a generic
    401 so clients learn nothing useful for enumeration.
  - reason_code values mirror the internal telemetry keys in Datadog/CloudWatch.
"""

from __future__ import annotations


class VedhaAuthError(Exception):
    """Base for all Vedha auth exceptions."""

    reason_code: str = "unknown"

    def __init__(self, message: str = "", *, reason_code: str | None = None) -> None:
        super().__init__(message)
        if reason_code is not None:
            self.reason_code = reason_code


# ── Authentication failures (all map to HTTP 401, reason hidden from client) ──

class AuthenticationError(VedhaAuthError):
    """A login attempt failed for any reason."""
    reason_code = "authentication_failed"


class UserNotFoundError(AuthenticationError):
    """No user record for the supplied email."""
    reason_code = "user_not_found"


class PasswordMismatchError(AuthenticationError):
    """User exists but supplied password does not match the stored hash."""
    reason_code = "password_mismatch"


class DisabledUserError(AuthenticationError):
    """User account exists but is_active=False."""
    reason_code = "disabled_user"


class DisabledTenantError(AuthenticationError):
    """Tenant account is disabled — all users in it are locked out."""
    reason_code = "disabled_tenant"


class ExpiredPasswordError(AuthenticationError):
    """User's password_expires_at is in the past — must rotate before logging in."""
    reason_code = "expired_password"


class BcryptFailureError(AuthenticationError):
    """bcrypt raised an exception during verification — indicates a corrupt hash or library bug."""
    reason_code = "bcrypt_failure"


class DatabaseFailureError(AuthenticationError):
    """Could not reach the database during authentication — infrastructure failure."""
    reason_code = "database_failure"


class JWTFailureError(AuthenticationError):
    """JWT token could not be created — JWT_SECRET missing or library failure."""
    reason_code = "jwt_failure"


class RateLimitError(AuthenticationError):
    """Caller exceeded the login rate limit — already handled by the rate-limit middleware
    but included here for completeness when raised programmatically."""
    reason_code = "rate_limit"


# ── Seeder / admin bootstrap failures ─────────────────────────────────────────

class SeedConfigurationError(VedhaAuthError):
    """Required env var missing, value invalid, or weak password in production."""
    reason_code = "seed_configuration_error"


class PasswordRotationError(VedhaAuthError):
    """Password rotation was requested but could not complete (hash verify failed, etc.)."""
    reason_code = "password_rotation_error"


class DatabaseUnavailableError(VedhaAuthError):
    """Database is not reachable at all — raised by startup diagnostics and seeder."""
    reason_code = "database_unavailable"

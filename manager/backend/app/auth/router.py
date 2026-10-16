import asyncio
import time
import uuid
from datetime import datetime, timezone
from typing import Annotated

import structlog
from fastapi import APIRouter, Depends, HTTPException, Request, status
from redis.exceptions import RedisError
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.exceptions import (
    AuthenticationError,
    BcryptFailureError,
    DatabaseFailureError,
    DisabledTenantError,
    DisabledUserError,
    ExpiredPasswordError,
    JWTFailureError,
    PasswordMismatchError,
    UserNotFoundError,
)
from app.auth.jwt import (
    create_access_token,
    create_refresh_token,
    decode_token,
    MANAGER_AUDIENCE,
    PORTAL_AUDIENCE,
)
from app.auth import refresh_store
from app.auth.password import pwd_context as _pwd
from app.auth.pat import build_personal_access_token
from app.auth.rbac import require_role
from app.database import get_db
from app.dependencies import AuthUser, get_redis
from app.models.enums import UserRole
from app.models.personal_access_token import PersonalAccessToken
from app.models.tenant import Tenant
from app.models.user import User
from app.ratelimit import (
    check_login_failures,
    clear_login_failures,
    client_ip,
    login_rate_limit,
    mfa_rate_limit,
    refresh_rate_limit,
    record_login_failure,
)
from app.auth import mfa as mfa_lib
from app.auth import totp
from app.services.audit import record_audit
from app.services import audit as audit_service
from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    MfaCodeRequest,
    MfaDisableRequest,
    MfaEnableRequest,
    MfaEnabledResponse,
    MfaSetupResponse,
    MfaStatusResponse,
    MfaTokenRequest,
    PersonalAccessTokenCreate,
    PersonalAccessTokenCreated,
    PersonalAccessTokenOut,
    RefreshRequest,
    TokenResponse,
)

router = APIRouter(prefix="/auth", tags=["auth"])
logger = structlog.get_logger()

# Generic client message — never changes regardless of internal reason.
_GENERIC_401 = "Invalid credentials"

# Session-store (Redis) outages; builtin ConnectionError/TimeoutError are OSError.
_STORE_ERRORS = (RedisError, OSError)


def access_claims_for(user: User) -> dict:
    """The audience + scoping claims an access token MUST carry for this user.

    Shared by login and refresh on purpose. These claims are the credential's
    CLASS, not a login-time decoration: `aud` keeps a portal token off operator
    APIs even if a role check is ever missed, and `client_engagement_id` is the
    portal's entire scoping boundary. Refresh used to rebuild the token without
    them, so a rotation silently downgraded a scoped portal token into an
    unscoped, audience-less one — which locked the customer out of their own
    portal (assert_client fails closed) and erased the audience separation.
    Build them in one place so the two paths cannot drift again.
    """
    is_client = user.role == UserRole.client
    claims: dict = {"aud": PORTAL_AUDIENCE if is_client else MANAGER_AUDIENCE}
    if is_client:
        # A client login MUST be bound to exactly one engagement. Refuse to mint
        # an unscoped token — on refresh exactly as on login.
        if user.client_engagement_id is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Client login is not bound to an engagement",
            )
        claims["client_engagement_id"] = str(user.client_engagement_id)
    return claims


# ── Audit of sign-in events ──────────────────────────────────────────────────
#
# A failed sign-in RAISES, so the request's transaction rolls back; these are written in
# their own transaction so the failure is kept. The reason is recorded for the
# administrator and never reaches the caller (the response stays a generic 401).

def _tag_user(exc: AuthenticationError, user: User) -> AuthenticationError:
    exc.audit_user = user
    return exc


async def _audit_sign_in_failure(email: str, reason: str, user: User | None = None) -> None:
    await audit_service.record_audit_independent(
        actor_id=user.id if user else "anonymous",
        actor_type=("client" if user is not None and user.client_engagement_id else "user") if user else "anonymous",
        actor_label=email,
        tenant_id=user.tenant_id if user else None,
        action="auth.login.failure", outcome="failure",
        resource_type="user" if user else None, resource_id=user.id if user else None,
        detail={"reason": reason},
    )


async def _audit_sign_in_success(user: User, *, method: str) -> None:
    await audit_service.record_audit_independent(
        actor_id=user.id, actor_type="client" if user.client_engagement_id else "user",
        actor_label=user.email, tenant_id=user.tenant_id, action="auth.login.success",
        resource_type="user", resource_id=user.id,
        detail={"method": method, "role": user.role.value},
    )


# ── Private authentication service ───────────────────────────────────────────

async def _assert_account_usable(user: User, db: AsyncSession) -> None:
    """Account-state rules every credential issuance must pass — login AND
    refresh. Refresh used to skip these, so a disabled user (or a user in a
    disabled tenant, or with an expired password) kept a rolling session."""
    if not user.is_active:
        raise DisabledUserError(f"user {user.id} is_active=False")

    try:
        tenant = (
            await db.execute(select(Tenant).where(Tenant.id == user.tenant_id))
        ).scalar_one_or_none()
    except SQLAlchemyError as exc:
        raise DatabaseFailureError(f"DB error during tenant lookup: {exc}") from exc

    if tenant and not tenant.is_active:
        raise DisabledTenantError(
            f"tenant {user.tenant_id} is_active=False (user={user.id})"
        )

    if user.password_expires_at is not None:
        if user.password_expires_at < datetime.now(timezone.utc):
            raise ExpiredPasswordError(
                f"password expired at {user.password_expires_at.isoformat()} for user {user.id}"
            )


async def _authenticate(email: str, password: str, db: AsyncSession) -> User:
    """
    Validates credentials and returns the User on success.
    Raises a typed AuthenticationError subclass on any failure.
    The caller maps ALL of them to 401 — reason never leaves the server.
    """
    # ── Fetch user ─────────────────────────────────────────────────────────
    try:
        user = (
            await db.execute(select(User).where(User.email == email))
        ).scalar_one_or_none()
    except SQLAlchemyError as exc:
        raise DatabaseFailureError(f"DB error during user lookup: {exc}") from exc

    if user is None:
        # Constant-time dummy verify to prevent timing-based user enumeration.
        await asyncio.to_thread(_pwd.dummy_verify)
        raise UserNotFoundError(f"no user with email={email!r}")

    try:
        await _assert_account_usable(user, db)
    except (DisabledUserError, DisabledTenantError, ExpiredPasswordError) as exc:
        await asyncio.to_thread(_pwd.dummy_verify)   # maintain constant-time behaviour
        _tag_user(exc, user)
        raise

    # ── bcrypt verify ─────────────────────────────────────────────────────
    try:
        match = await asyncio.to_thread(_pwd.verify, password, user.hashed_password)
    except (ValueError, TypeError, RuntimeError) as exc:
        # passlib 1.7.4 has no single base error: verify() raises ValueError
        # (malformed/unknown hash, oversized password), TypeError (bad password
        # type), or RuntimeError (Internal/MissingBackendError). Catch all three.
        raise _tag_user(BcryptFailureError(f"bcrypt raised for user {user.id}: {exc}"), user) from exc

    if not match:
        raise _tag_user(PasswordMismatchError(f"password mismatch for user {user.id}"), user)

    return user


# ── Login route ───────────────────────────────────────────────────────────────

@router.post(
    "/login",
    response_model=LoginResponse,
    response_model_exclude_none=True,
    summary="Obtain JWT access + refresh tokens",
    dependencies=[Depends(login_rate_limit)],
)
async def login(
    body: LoginRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
    redis=Depends(get_redis),
):
    request_id = str(uuid.uuid4())
    t0 = time.monotonic()

    # Build a bound logger once — all log calls in this request carry these fields.
    bound = logger.bind(
        request_id=request_id,
        email=body.email,
        ip=client_ip(request),
        user_agent=request.headers.get("user-agent", "")[:200],
    )

    # Per-account backstop: an IP limit alone cannot slow a spray spread across
    # many sources against one user. Checked before any password work.
    try:
        await check_login_failures(redis, body.email)
    except HTTPException as exc:
        if exc.status_code == status.HTTP_429_TOO_MANY_REQUESTS:
            await audit_service.record_audit_independent(
                actor_id="anonymous", actor_type="anonymous", actor_label=body.email,
                action="auth.login.locked", outcome="denied",
                detail={"reason": "too_many_failures"})
        raise

    try:
        user = await _authenticate(body.email, body.password, db)
    except AuthenticationError as exc:
        await record_login_failure(redis, body.email)
        await _audit_sign_in_failure(body.email, exc.reason_code, getattr(exc, "audit_user", None))
        latency = round((time.monotonic() - t0) * 1000, 1)
        bound.warning(
            "auth.login.failed",
            reason_code=exc.reason_code,
            latency_ms=latency,
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=_GENERIC_401,
        ) from None
    except Exception as exc:
        # Unexpected error (bug, infra) — log as error but still return 401
        latency = round((time.monotonic() - t0) * 1000, 1)
        bound.error(
            "auth.login.unexpected_error",
            error=str(exc),
            exc_type=type(exc).__name__,
            latency_ms=latency,
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=_GENERIC_401,
        ) from None

    # Organisation sign-in network policy. Refused with the SAME generic 401 as a bad
    # password: a distinct answer would tell someone outside the allowed networks that
    # their (stolen) password is right. The reason is logged for the administrator.
    from app.services import org_settings
    auth_policy = await org_settings.get_section(db, user.tenant_id, "auth")
    if not org_settings.sign_in_allowed(auth_policy, role=user.role.value, address=client_ip(request)):
        await record_login_failure(redis, body.email)
        await _audit_sign_in_failure(body.email, "network_not_allowed", user)
        bound.warning("auth.login.network_blocked", user_id=str(user.id), role=user.role.value)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=_GENERIC_401)

    # Portal scoping + audience separation. Computed BEFORE the token try below so
    # a misconfigured client login surfaces as 403 rather than being masked as 401.
    access_claims_for(user)

    # Two-step sign-in. The password was right, but no session is issued until a
    # code is: the client gets a short-lived challenge for /auth/mfa/*.
    # A legacy row flagged on without a stored secret could never pass the code
    # step, so it is treated as not enrolled rather than locked out.
    if _has_mfa(user):
        token, _ = mfa_lib.create_challenge(str(user.id), str(user.tenant_id), mfa_lib.PURPOSE_VERIFY)
        bound.info("auth.login.mfa_challenge", user_id=str(user.id))
        return LoginResponse(mfa_required=True, mfa_token=token)
    if org_settings.mfa_required(auth_policy, role=user.role.value):
        token, _ = mfa_lib.create_challenge(str(user.id), str(user.tenant_id), mfa_lib.PURPOSE_ENROLL)
        bound.info("auth.login.mfa_enrollment_required", user_id=str(user.id))
        return LoginResponse(mfa_enrollment_required=True, mfa_token=token)

    tokens = await _issue_session(user, redis, bound)
    await _audit_sign_in_success(user, method="password")
    latency = round((time.monotonic() - t0) * 1000, 1)
    bound.info(
        "auth.login.success",
        user_id=str(user.id),
        tenant_id=str(user.tenant_id),
        role=user.role.value,
        latency_ms=latency,
    )
    return tokens


async def _issue_session(user: User, redis, bound) -> LoginResponse:
    """Mint and register a session for a user who has passed every check."""
    extra_claims = access_claims_for(user)
    try:
        access = create_access_token(
            subject=str(user.id),
            tenant_id=str(user.tenant_id),
            role=user.role.value,
            extra_claims=extra_claims,
        )
        refresh, refresh_jti = create_refresh_token(
            subject=str(user.id),
            tenant_id=str(user.tenant_id),
        )
    except Exception as exc:
        bound.error("auth.login.failed", reason_code=JWTFailureError.reason_code, error=str(exc))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=_GENERIC_401,
        ) from None

    # A refresh token is honoured only while registered, so an unregistered one
    # would silently fail at the first rotation — refuse the login instead.
    try:
        await refresh_store.issue(redis, refresh_jti, str(user.id))
    except _STORE_ERRORS as exc:
        bound.error("auth.login.session_store_failed", error=str(exc))
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Session store unavailable",
        ) from None

    await clear_login_failures(redis, user.email)
    return LoginResponse(access_token=access, refresh_token=refresh)


@router.get("/me", summary="Current user from the access token (for the dashboard)")
async def me(current_user: AuthUser, db: AsyncSession = Depends(get_db)):
    user = (await db.execute(select(User).where(User.id == current_user.user_id))).scalar_one_or_none()
    return {
        "user_id": str(current_user.user_id),
        "tenant_id": str(current_user.tenant_id),
        "role": current_user.role,
        "email": user.email if user else None,
        "auth_type": current_user.auth_type,
        "pat_id": str(current_user.pat_id) if current_user.pat_id else None,
        "scopes": list(current_user.scopes),
    }


_SESSION_EXPIRED = "Session expired — sign in again"


def _session_store_unavailable(exc: Exception) -> HTTPException:
    logger.error("auth.session_store_unavailable", error=str(exc))
    return HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail="Session store unavailable",
    )


@router.post("/refresh", response_model=TokenResponse, summary="Rotate access token using refresh token",
             dependencies=[Depends(refresh_rate_limit)])
async def refresh(
    body: RefreshRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
    redis=Depends(get_redis),
):
    payload = decode_token(body.refresh_token)
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not a refresh token")
    user_id, jti = payload["sub"], payload.get("jti", "")

    # Single use: consume before anything else, so a failure below still burns it.
    try:
        owner = await refresh_store.consume(redis, jti)
    except _STORE_ERRORS as exc:
        raise _session_store_unavailable(exc) from None

    if owner != user_id:
        # Validly signed but not live: already rotated, revoked, or never issued.
        # Replay of a rotated token is the stolen-token signal, so end every
        # session the user holds — the thief's and the victim's alike.
        logger.warning("auth.refresh.reuse_detected", user_id=user_id, jti=jti)
        try:
            await refresh_store.revoke_all(redis, user_id)
        except _STORE_ERRORS as exc:
            raise _session_store_unavailable(exc) from None
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=_SESSION_EXPIRED)

    user = (
        await db.execute(select(User).where(User.id == uuid.UUID(user_id)))
    ).scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=_SESSION_EXPIRED)
    try:
        await _assert_account_usable(user, db)
    except AuthenticationError as exc:
        logger.warning("auth.refresh.rejected", user_id=user_id, reason_code=exc.reason_code)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=_SESSION_EXPIRED) from None

    # Organisation policy at every rotation: the sign-in network rule, and the
    # absolute session limit measured from the ORIGINAL sign-in (auth_time rides
    # through each rotation). A token issued before the claim existed starts its
    # clock now, so switching a limit on never signs everyone out at once.
    from app.services import org_settings
    auth_policy = await org_settings.get_section(db, user.tenant_id, "auth")
    if not org_settings.sign_in_allowed(auth_policy, role=user.role.value, address=client_ip(request)):
        logger.warning("auth.refresh.network_blocked", user_id=user_id, role=user.role.value)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=_SESSION_EXPIRED)
    raw_auth_time = payload.get("auth_time")
    auth_time = (datetime.fromtimestamp(int(raw_auth_time), timezone.utc)
                 if isinstance(raw_auth_time, (int, float)) else None)
    if org_settings.session_expired(auth_policy, role=user.role.value, auth_time=auth_time):
        logger.info("auth.refresh.session_limit", user_id=user_id, role=user.role.value)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=_SESSION_EXPIRED)

    access = create_access_token(
        subject=str(user.id),
        tenant_id=str(user.tenant_id),
        role=user.role.value,
        extra_claims=access_claims_for(user),
    )
    new_refresh, new_jti = create_refresh_token(
        subject=str(user.id),
        tenant_id=str(user.tenant_id),
        auth_time=int(raw_auth_time) if isinstance(raw_auth_time, (int, float)) else None,
    )
    try:
        await refresh_store.issue(redis, new_jti, str(user.id))
    except _STORE_ERRORS as exc:
        raise _session_store_unavailable(exc) from None
    return TokenResponse(access_token=access, refresh_token=new_refresh)


@router.post("/logout", summary="Revoke a refresh token (server-side sign-out)")
async def logout(body: RefreshRequest, redis=Depends(get_redis)):
    """Public on purpose: the access token may already be expired at sign-out.
    Presenting a refresh token only ever revokes THAT token, so no auth is
    needed; an invalid token is a silent no-op (never an oracle)."""
    try:
        payload = decode_token(body.refresh_token)
    except HTTPException:
        return {"ok": True}
    if payload.get("type") == "refresh" and payload.get("jti"):
        try:
            await refresh_store.consume(redis, payload["jti"])
        except _STORE_ERRORS as exc:
            raise _session_store_unavailable(exc) from None
        await audit_service.record_audit_independent(
            actor_id=payload.get("sub", "unknown"), tenant_id=payload.get("tenant_id"),
            action="auth.logout", resource_type="user")
    return {"ok": True}


@router.post(
    "/personal-access-tokens",
    response_model=PersonalAccessTokenCreated,
    status_code=status.HTTP_201_CREATED,
    summary="Create a personal access token for CLI/API use",
)
async def create_personal_access_token(
    body: PersonalAccessTokenCreate,
    current_user: Annotated[AuthUser, require_role(["admin", "manager", "tester", "analyst", "auditor"])],
    db: AsyncSession = Depends(get_db),
):
    if current_user.auth_type == "pat":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Personal access tokens cannot create more personal access tokens",
        )
    try:
        token, row = build_personal_access_token(
            tenant_id=current_user.tenant_id,
            user_id=current_user.user_id,
            name=body.name,
            role=current_user.role,
            scopes=body.scopes,
            expires_in_days=body.expires_in_days,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    db.add(row)
    await db.flush()
    await db.refresh(row)
    record_audit(db, actor_id=current_user.user_id, action="auth.api_key.created",
                 resource_type="api_key", resource_id=row.id,
                 detail={"name": row.name, "role": row.role, "scopes": list(row.scopes or []),
                         "expires_at": row.expires_at.isoformat() if row.expires_at else None})
    logger.info("auth.pat.created", user_id=str(current_user.user_id), pat_id=str(row.id), name=row.name)
    return PersonalAccessTokenCreated(
        id=row.id,
        name=row.name,
        token=token,
        token_prefix=row.token_prefix,
        role=row.role,
        scopes=list(row.scopes or []),
        expires_at=row.expires_at,
        created_at=row.created_at,
    )


@router.get(
    "/personal-access-tokens",
    response_model=list[PersonalAccessTokenOut],
    summary="List current user's personal access tokens",
)
async def list_personal_access_tokens(
    current_user: Annotated[AuthUser, require_role(["admin", "manager", "tester", "analyst", "auditor"])],
    db: AsyncSession = Depends(get_db),
):
    rows = (
        await db.execute(
            select(PersonalAccessToken)
            .where(
                PersonalAccessToken.tenant_id == current_user.tenant_id,
                PersonalAccessToken.user_id == current_user.user_id,
            )
            .order_by(PersonalAccessToken.created_at.desc())
        )
    ).scalars().all()
    return [
        PersonalAccessTokenOut(
            id=row.id,
            name=row.name,
            token_prefix=row.token_prefix,
            role=row.role,
            scopes=list(row.scopes or []),
            expires_at=row.expires_at,
            last_used_at=row.last_used_at,
            revoked_at=row.revoked_at,
            created_at=row.created_at,
        )
        for row in rows
    ]


@router.delete(
    "/personal-access-tokens/{token_id}",
    summary="Revoke a personal access token",
)
async def revoke_personal_access_token(
    token_id: uuid.UUID,
    current_user: Annotated[AuthUser, require_role(["admin", "manager", "tester", "analyst", "auditor"])],
    db: AsyncSession = Depends(get_db),
):
    row = (
        await db.execute(
            select(PersonalAccessToken).where(
                PersonalAccessToken.id == token_id,
                PersonalAccessToken.tenant_id == current_user.tenant_id,
                PersonalAccessToken.user_id == current_user.user_id,
            )
        )
    ).scalar_one_or_none()
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Token not found")
    if row.revoked_at is None:
        row.revoked_at = datetime.now(timezone.utc)
        record_audit(db, actor_id=current_user.user_id, action="auth.api_key.revoked",
                     resource_type="api_key", resource_id=row.id, detail={"name": row.name})
        await db.flush()
    logger.info("auth.pat.revoked", user_id=str(current_user.user_id), pat_id=str(row.id))
    return {"ok": True, "id": str(row.id), "revoked_at": row.revoked_at.isoformat()}


# ── Two-step sign-in (TOTP) ───────────────────────────────────────────────────
#
# Sign-in with MFA:      POST /auth/login → {mfa_required, mfa_token}
#                        POST /auth/mfa/verify {mfa_token, code} → session
# Required, not set up:  POST /auth/login → {mfa_enrollment_required, mfa_token}
#                        POST /auth/mfa/enroll/setup {mfa_token} → secret + QR URI
#                        POST /auth/mfa/enroll/enable {mfa_token, code} → recovery codes + session
# Signed in:             GET /auth/mfa/status, POST /auth/mfa/setup, /enable, /disable,
#                        /recovery-codes; admins: POST /auth/mfa/reset/{user_id}

_BAD_CODE = "Invalid or expired code"


def _has_mfa(user: User) -> bool:
    return bool(user.mfa_enabled and user.mfa_secret_enc)


def _bad_code() -> HTTPException:
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=_BAD_CODE)


async def _user_by_id(db: AsyncSession, user_id) -> User | None:
    return (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()


async def _challenge_user(body_token: str, purpose: str, request: Request, db: AsyncSession, redis) -> tuple[User, dict]:
    """The user behind a usable challenge token, re-checked like a fresh sign-in."""
    claims = mfa_lib.decode_challenge(body_token)
    if claims is None or claims["purpose"] != purpose or not await mfa_lib.challenge_usable(redis, claims["jti"]):
        raise _bad_code()
    user = await _user_by_id(db, uuid.UUID(claims["sub"]))
    if user is None or str(user.tenant_id) != claims.get("tenant_id"):
        raise _bad_code()
    try:
        await _assert_account_usable(user, db)
    except AuthenticationError:
        raise _bad_code() from None
    from app.services import org_settings
    policy = await org_settings.get_section(db, user.tenant_id, "auth")
    if not org_settings.sign_in_allowed(policy, role=user.role.value, address=client_ip(request)):
        raise _bad_code()
    return user, claims


def _check_code(user: User, code: str) -> tuple[str, int | None, list[str] | None]:
    """("totp", step, None) or ("recovery", None, remaining) for a correct code,
    ("bad", None, None) otherwise."""
    if mfa_lib.looks_like_recovery_code(code):
        remaining = mfa_lib.consume_recovery_code(list(user.mfa_recovery_hashes or []), code)
        return ("recovery", None, remaining) if remaining is not None else ("bad", None, None)
    secret = mfa_lib.decrypt_secret(user.mfa_secret_enc)
    if not secret:
        return ("bad", None, None)
    step = totp.verify(secret, code, last_step=user.mfa_last_step)
    return ("totp", step, None) if step is not None else ("bad", None, None)


@router.post(
    "/mfa/verify",
    response_model=LoginResponse,
    response_model_exclude_none=True,
    summary="Finish a two-step sign-in with an app code or a recovery code",
    dependencies=[Depends(mfa_rate_limit)],
)
async def mfa_verify(body: MfaCodeRequest, request: Request, db: AsyncSession = Depends(get_db), redis=Depends(get_redis)):
    user, claims = await _challenge_user(body.mfa_token, mfa_lib.PURPOSE_VERIFY, request, db, redis)
    bound = logger.bind(user_id=str(user.id), ip=client_ip(request))
    await check_login_failures(redis, user.email)
    if not _has_mfa(user):
        raise _bad_code()
    kind, step, remaining = _check_code(user, body.code)
    if kind == "bad":
        await mfa_lib.record_challenge_failure(redis, claims["jti"])
        await record_login_failure(redis, user.email)
        bound.warning("auth.mfa.verify_failed")
        await audit_service.record_audit_independent(
            actor_id=user.id, actor_type="client" if user.client_engagement_id else "user",
            actor_label=user.email, tenant_id=user.tenant_id, action="auth.mfa.challenge_failed",
            outcome="failure", resource_type="user", resource_id=user.id)
        raise _bad_code()

    await mfa_lib.spend_challenge(redis, claims["jti"])
    if kind == "totp":
        user.mfa_last_step = step
    else:
        user.mfa_recovery_hashes = remaining
        record_audit(db, actor_id=user.id, action="auth.mfa.recovery_code_used", resource_type="user",
                     resource_id=str(user.id), detail={"remaining": len(remaining or [])}, ip=client_ip(request))
    await db.flush()
    tokens = await _issue_session(user, redis, bound)
    await _audit_sign_in_success(user, method=f"password+{'recovery_code' if kind == 'recovery' else 'authenticator'}")
    bound.info("auth.login.success", method=f"password+{kind}")
    return tokens


async def _start_setup(user: User, redis) -> MfaSetupResponse:
    secret = totp.generate_secret()
    await redis.set(mfa_lib.pending_secret_key(str(user.id)), mfa_lib.encrypt_secret(secret), ex=mfa_lib.PENDING_SECRET_SECONDS)
    return MfaSetupResponse(secret=secret, otpauth_uri=totp.provisioning_uri(secret, user.email), account=user.email)


async def _finish_setup(user: User, code: str, redis, db: AsyncSession, request: Request) -> list[str]:
    """Turn MFA on once the user proves their app has the pending secret."""
    pending = mfa_lib.decrypt_secret(await redis.get(mfa_lib.pending_secret_key(str(user.id))))
    if not pending:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Setup expired — start again to get a new code")
    step = totp.verify(pending, code)
    if step is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="That code does not match. Check the time on your phone and try again.")
    codes, hashes = mfa_lib.new_recovery_codes()
    user.mfa_secret_enc = mfa_lib.encrypt_secret(pending)
    user.mfa_last_step = step
    user.mfa_recovery_hashes = hashes
    user.mfa_enabled = True
    user.mfa_enabled_at = datetime.now(timezone.utc)
    await redis.delete(mfa_lib.pending_secret_key(str(user.id)))
    record_audit(db, actor_id=user.id, action="auth.mfa.enabled", resource_type="user",
                 resource_id=str(user.id), ip=client_ip(request))
    await db.flush()
    return codes


@router.post("/mfa/enroll/setup", response_model=MfaSetupResponse,
             summary="Start the enrolment an organisation requires at sign-in",
             dependencies=[Depends(mfa_rate_limit)])
async def mfa_enroll_setup(body: MfaTokenRequest, request: Request, db: AsyncSession = Depends(get_db), redis=Depends(get_redis)):
    user, _ = await _challenge_user(body.mfa_token, mfa_lib.PURPOSE_ENROLL, request, db, redis)
    # Set up meanwhile (another tab): never replace an existing authenticator here.
    if _has_mfa(user):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Two-step sign-in is already on — sign in again")
    return await _start_setup(user, redis)


@router.post("/mfa/enroll/enable", response_model=MfaEnabledResponse, response_model_exclude_none=True,
             summary="Finish required enrolment: turns MFA on and signs in",
             dependencies=[Depends(mfa_rate_limit)])
async def mfa_enroll_enable(body: MfaCodeRequest, request: Request, db: AsyncSession = Depends(get_db), redis=Depends(get_redis)):
    user, claims = await _challenge_user(body.mfa_token, mfa_lib.PURPOSE_ENROLL, request, db, redis)
    if _has_mfa(user):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Two-step sign-in is already on — sign in again")
    try:
        codes = await _finish_setup(user, body.code, redis, db, request)
    except HTTPException:
        await mfa_lib.record_challenge_failure(redis, claims["jti"])
        raise
    await mfa_lib.spend_challenge(redis, claims["jti"])
    tokens = await _issue_session(user, redis, logger.bind(user_id=str(user.id)))
    return MfaEnabledResponse(**tokens.model_dump(), recovery_codes=codes)


async def _signed_in_user(current_user, db: AsyncSession) -> User:
    if current_user.auth_type != "jwt":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Manage two-step sign-in from a signed-in session, not an API token")
    user = await _user_by_id(db, current_user.user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.get("/mfa/status", response_model=MfaStatusResponse, summary="Two-step sign-in status for the signed-in user")
async def mfa_status(current_user: AuthUser, db: AsyncSession = Depends(get_db)):
    user = await _signed_in_user(current_user, db)
    from app.services import org_settings
    policy = await org_settings.get_section(db, user.tenant_id, "auth")
    return MfaStatusResponse(
        enabled=_has_mfa(user),
        enabled_at=user.mfa_enabled_at if _has_mfa(user) else None,
        recovery_codes_left=len(user.mfa_recovery_hashes or []) if _has_mfa(user) else 0,
        required_by_policy=org_settings.mfa_required(policy, role=user.role.value),
    )


@router.post("/mfa/setup", response_model=MfaSetupResponse, summary="Start setting up an authenticator app")
async def mfa_setup(current_user: AuthUser, db: AsyncSession = Depends(get_db), redis=Depends(get_redis)):
    user = await _signed_in_user(current_user, db)
    if _has_mfa(user):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Two-step sign-in is already on")
    return await _start_setup(user, redis)


@router.post("/mfa/enable", response_model=MfaEnabledResponse, response_model_exclude_none=True,
             summary="Confirm the app code and turn two-step sign-in on")
async def mfa_enable(body: MfaEnableRequest, request: Request, current_user: AuthUser,
                     db: AsyncSession = Depends(get_db), redis=Depends(get_redis)):
    user = await _signed_in_user(current_user, db)
    if _has_mfa(user):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Two-step sign-in is already on")
    codes = await _finish_setup(user, body.code, redis, db, request)
    return MfaEnabledResponse(recovery_codes=codes)


@router.post("/mfa/disable", summary="Turn two-step sign-in off (password and a code required)")
async def mfa_disable(body: MfaDisableRequest, request: Request, current_user: AuthUser,
                      db: AsyncSession = Depends(get_db), redis=Depends(get_redis)):
    user = await _signed_in_user(current_user, db)
    from app.services import org_settings
    policy = await org_settings.get_section(db, user.tenant_id, "auth")
    if org_settings.mfa_required(policy, role=user.role.value):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Your organisation requires two-step sign-in")
    if not _has_mfa(user):
        return {"enabled": False}
    await check_login_failures(redis, user.email)
    password_ok = await asyncio.to_thread(_pwd.verify, body.password, user.hashed_password)
    kind, _, _ = _check_code(user, body.code)
    if not password_ok or kind == "bad":
        await record_login_failure(redis, user.email)
        # 400, not 401: the session is fine, and clients read 401 as "signed out".
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password or code is incorrect")
    user.mfa_enabled = False
    user.mfa_secret_enc = None
    user.mfa_last_step = None
    user.mfa_recovery_hashes = []
    user.mfa_enabled_at = None
    record_audit(db, actor_id=user.id, action="auth.mfa.disabled", resource_type="user",
                 resource_id=str(user.id), ip=client_ip(request))
    await db.flush()
    return {"enabled": False}


@router.post("/mfa/recovery-codes", response_model=MfaEnabledResponse, response_model_exclude_none=True,
             summary="Replace all recovery codes (an app code is required)")
async def mfa_new_recovery_codes(body: MfaEnableRequest, request: Request, current_user: AuthUser,
                                 db: AsyncSession = Depends(get_db), redis=Depends(get_redis)):
    user = await _signed_in_user(current_user, db)
    if not _has_mfa(user):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Two-step sign-in is off")
    secret = mfa_lib.decrypt_secret(user.mfa_secret_enc)
    step = totp.verify(secret, body.code, last_step=user.mfa_last_step) if secret else None
    if step is None:
        await record_login_failure(redis, user.email)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="That code does not match")
    codes, hashes = mfa_lib.new_recovery_codes()
    user.mfa_last_step = step
    user.mfa_recovery_hashes = hashes
    record_audit(db, actor_id=user.id, action="auth.mfa.recovery_codes_replaced", resource_type="user",
                 resource_id=str(user.id), ip=client_ip(request))
    await db.flush()
    return MfaEnabledResponse(recovery_codes=codes)


@router.post("/mfa/reset/{user_id}", summary="Admin: clear a user's two-step sign-in (lost phone)")
async def mfa_reset(user_id: uuid.UUID, request: Request,
                    current_user: Annotated[AuthUser, require_role(["admin"])],
                    db: AsyncSession = Depends(get_db)):
    user = await _user_by_id(db, user_id)
    # Hidden across tenants: never reveal whether another tenant's user exists.
    if user is None or user.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if user.id == current_user.user_id:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Turn your own two-step sign-in off from Settings")
    user.mfa_enabled = False
    user.mfa_secret_enc = None
    user.mfa_last_step = None
    user.mfa_recovery_hashes = []
    user.mfa_enabled_at = None
    record_audit(db, actor_id=current_user.user_id, action="auth.mfa.reset_by_admin", resource_type="user",
                 resource_id=str(user.id), detail={"email": user.email}, ip=client_ip(request))
    await db.flush()
    return {"user_id": str(user.id), "mfa_enabled": False}

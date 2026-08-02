import time
import uuid
from datetime import datetime, timezone
from typing import Annotated

import structlog
from fastapi import APIRouter, Depends, HTTPException, Request, status
from passlib.context import CryptContext
from passlib.exc import PasslibError
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
from app.auth.jwt import create_access_token, create_refresh_token, decode_token
from app.auth.pat import build_personal_access_token
from app.auth.rbac import require_role
from app.database import get_db
from app.dependencies import AuthUser
from app.models.personal_access_token import PersonalAccessToken
from app.models.tenant import Tenant
from app.models.user import User
from app.ratelimit import client_ip, login_rate_limit
from app.schemas.auth import (
    LoginRequest,
    PersonalAccessTokenCreate,
    PersonalAccessTokenCreated,
    PersonalAccessTokenOut,
    TokenResponse,
)

router = APIRouter(prefix="/auth", tags=["auth"])
logger = structlog.get_logger()
_pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Generic client message — never changes regardless of internal reason.
_GENERIC_401 = "Invalid credentials"


# ── Private authentication service ───────────────────────────────────────────

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
        _pwd.dummy_verify()
        raise UserNotFoundError(f"no user with email={email!r}")

    # ── Account state ─────────────────────────────────────────────────────
    if not user.is_active:
        _pwd.dummy_verify()   # maintain constant-time behaviour
        raise DisabledUserError(f"user {user.id} is_active=False")

    # ── Tenant state ──────────────────────────────────────────────────────
    try:
        tenant = (
            await db.execute(select(Tenant).where(Tenant.id == user.tenant_id))
        ).scalar_one_or_none()
    except SQLAlchemyError as exc:
        raise DatabaseFailureError(f"DB error during tenant lookup: {exc}") from exc

    if tenant and not tenant.is_active:
        _pwd.dummy_verify()
        raise DisabledTenantError(
            f"tenant {user.tenant_id} is_active=False (user={user.id})"
        )

    # ── Password expiry ───────────────────────────────────────────────────
    if user.password_expires_at is not None:
        if user.password_expires_at < datetime.now(timezone.utc):
            _pwd.dummy_verify()
            raise ExpiredPasswordError(
                f"password expired at {user.password_expires_at.isoformat()} for user {user.id}"
            )

    # ── bcrypt verify ─────────────────────────────────────────────────────
    try:
        match = _pwd.verify(password, user.hashed_password)
    except PasslibError as exc:
        raise BcryptFailureError(f"bcrypt raised for user {user.id}: {exc}") from exc

    if not match:
        raise PasswordMismatchError(f"password mismatch for user {user.id}")

    return user


# ── Login route ───────────────────────────────────────────────────────────────

@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Obtain JWT access + refresh tokens",
    dependencies=[Depends(login_rate_limit)],
)
async def login(body: LoginRequest, request: Request, db: AsyncSession = Depends(get_db)):
    request_id = str(uuid.uuid4())
    t0 = time.monotonic()

    # Build a bound logger once — all log calls in this request carry these fields.
    bound = logger.bind(
        request_id=request_id,
        email=body.email,
        ip=client_ip(request),
        user_agent=request.headers.get("user-agent", "")[:200],
    )

    try:
        user = await _authenticate(body.email, body.password, db)
    except AuthenticationError as exc:
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

    # ── Success path ──────────────────────────────────────────────────────
    try:
        access = create_access_token(
            subject=str(user.id),
            tenant_id=str(user.tenant_id),
            role=user.role.value,
        )
        refresh, _ = create_refresh_token(
            subject=str(user.id),
            tenant_id=str(user.tenant_id),
        )
    except Exception as exc:
        latency = round((time.monotonic() - t0) * 1000, 1)
        bound.error(
            "auth.login.failed",
            reason_code=JWTFailureError.reason_code,
            error=str(exc),
            latency_ms=latency,
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=_GENERIC_401,
        ) from None

    latency = round((time.monotonic() - t0) * 1000, 1)
    bound.info(
        "auth.login.success",
        user_id=str(user.id),
        tenant_id=str(user.tenant_id),
        role=user.role.value,
        latency_ms=latency,
    )
    return TokenResponse(access_token=access, refresh_token=refresh)


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


@router.post("/refresh", response_model=TokenResponse, summary="Rotate access token using refresh token")
async def refresh(refresh_token: str, db: AsyncSession = Depends(get_db)):
    payload = decode_token(refresh_token)
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not a refresh token")

    user_id = uuid.UUID(payload["sub"])
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    access = create_access_token(
        subject=str(user.id),
        tenant_id=str(user.tenant_id),
        role=user.role.value,
    )
    new_refresh, _ = create_refresh_token(
        subject=str(user.id),
        tenant_id=str(user.tenant_id),
    )
    return TokenResponse(access_token=access, refresh_token=new_refresh)


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
        await db.flush()
    logger.info("auth.pat.revoked", user_id=str(current_user.user_id), pat_id=str(row.id))
    return {"ok": True, "id": str(row.id), "revoked_at": row.revoked_at.isoformat()}

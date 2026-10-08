import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.auth.pat import DEFAULT_PROBE_CLI_SCOPES


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RefreshRequest(BaseModel):
    """Body-borne so the token never lands in a URL (and so in access logs)."""
    refresh_token: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class LoginResponse(BaseModel):
    """Either a session (access + refresh) or a second-step challenge.

    `mfa_required`: the user has two-step sign-in; send a code to /auth/mfa/verify.
    `mfa_enrollment_required`: the organisation requires it and the user has not
    set it up; enrol with /auth/mfa/enroll/* to finish signing in.
    """
    access_token: str | None = None
    refresh_token: str | None = None
    token_type: str = "bearer"
    mfa_required: bool = False
    mfa_enrollment_required: bool = False
    mfa_token: str | None = None


class MfaCodeRequest(BaseModel):
    mfa_token: str = Field(..., min_length=10, max_length=2048)
    # A 6-digit app code, or a recovery code like 7KQ4M-X9PRT.
    code: str = Field(..., min_length=6, max_length=32)


class MfaTokenRequest(BaseModel):
    mfa_token: str = Field(..., min_length=10, max_length=2048)


class MfaEnableRequest(BaseModel):
    code: str = Field(..., min_length=6, max_length=12)


class MfaDisableRequest(BaseModel):
    password: str = Field(..., min_length=1, max_length=512)
    code: str = Field(..., min_length=6, max_length=32)


class MfaSetupResponse(BaseModel):
    secret: str
    otpauth_uri: str
    account: str


class MfaEnabledResponse(LoginResponse):
    recovery_codes: list[str]


class MfaStatusResponse(BaseModel):
    enabled: bool
    enabled_at: datetime | None
    recovery_codes_left: int
    required_by_policy: bool


class CurrentUser(BaseModel):
    """Parsed from JWT claims — attached to request.state and injected as dependency."""
    model_config = ConfigDict(frozen=True)

    user_id: uuid.UUID
    tenant_id: uuid.UUID
    role: str
    # Set only for role == "client": the one engagement this login may access.
    # The scoping boundary for the customer portal — enforced server-side.
    client_engagement_id: uuid.UUID | None = None
    auth_type: str = "jwt"
    pat_id: uuid.UUID | None = None
    scopes: tuple[str, ...] = ()


class PersonalAccessTokenCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=120)
    scopes: list[str] = Field(default_factory=lambda: list(DEFAULT_PROBE_CLI_SCOPES))
    expires_in_days: int | None = Field(default=90, ge=1, le=365)


class PersonalAccessTokenCreated(BaseModel):
    id: uuid.UUID
    name: str
    token: str
    token_prefix: str
    role: str
    scopes: list[str]
    expires_at: datetime | None
    created_at: datetime


class PersonalAccessTokenOut(BaseModel):
    id: uuid.UUID
    name: str
    token_prefix: str
    role: str
    scopes: list[str]
    expires_at: datetime | None
    last_used_at: datetime | None
    revoked_at: datetime | None
    created_at: datetime

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.auth.pat import DEFAULT_PROBE_CLI_SCOPES


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class CurrentUser(BaseModel):
    """Parsed from JWT claims — attached to request.state and injected as dependency."""
    model_config = ConfigDict(frozen=True)

    user_id: uuid.UUID
    tenant_id: uuid.UUID
    role: str
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

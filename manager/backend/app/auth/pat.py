from __future__ import annotations

import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from typing import Any

from app.models.personal_access_token import PersonalAccessToken

TOKEN_PREFIX = "vpat_"

DEFAULT_PROBE_CLI_SCOPES = (
    "probe:read",
    "probe:write",
    "probe:register",
    "engagement:read",
    "engagement:write",
)

ALLOWED_PAT_SCOPES = {
    "api:*",
    "api:read",
    "api:write",
    "probe:read",
    "probe:write",
    "probe:register",
    "engagement:read",
    "engagement:write",
}


def new_pat_token() -> str:
    return TOKEN_PREFIX + secrets.token_urlsafe(32)


def hash_pat_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def pat_display_prefix(token: str) -> str:
    return token[:16]


def validate_pat_scopes(scopes: list[str]) -> list[str]:
    unique = []
    for scope in scopes:
        if scope not in ALLOWED_PAT_SCOPES:
            raise ValueError(f"unsupported PAT scope '{scope}'")
        if scope not in unique:
            unique.append(scope)
    return unique


def build_personal_access_token(
    *,
    tenant_id: Any,
    user_id: Any,
    name: str,
    role: str,
    scopes: list[str],
    expires_in_days: int | None,
) -> tuple[str, PersonalAccessToken]:
    validated_scopes = validate_pat_scopes(scopes)
    token = new_pat_token()
    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(days=expires_in_days) if expires_in_days else None
    row = PersonalAccessToken(
        tenant_id=tenant_id,
        user_id=user_id,
        name=name,
        token_hash=hash_pat_token(token),
        token_prefix=pat_display_prefix(token),
        role=role,
        scopes=validated_scopes,
        expires_at=expires_at,
    )
    return token, row


def pat_scope_allows(path: str, method: str, scopes: list[str]) -> bool:
    scope_set = set(scopes)
    method = method.upper()
    read_method = method in {"GET", "HEAD", "OPTIONS"}

    if "api:*" in scope_set:
        return True
    if read_method and ({"api:read", "api:write"} & scope_set):
        return True
    if not read_method and "api:write" in scope_set:
        return True

    if path == "/auth/me":
        return True

    if path == "/agents/use-cases":
        return read_method and "probe:read" in scope_set
    if path == "/agents":
        return read_method and "probe:read" in scope_set
    if path == "/agents/register":
        return method == "POST" and "probe:register" in scope_set
    if path == "/agents/jobs":
        return (read_method and "probe:read" in scope_set) or (
            method == "POST" and "probe:write" in scope_set
        )
    if path.startswith("/agents/jobs/"):
        return read_method and "probe:read" in scope_set

    if path == "/engagements" or path.startswith("/engagements/"):
        if read_method:
            return bool({"engagement:read", "probe:read"} & scope_set)
        return "engagement:write" in scope_set

    return False

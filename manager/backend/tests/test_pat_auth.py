from __future__ import annotations

import uuid

import pytest

from app.auth.pat import (
    build_personal_access_token,
    hash_pat_token,
    new_pat_token,
    pat_scope_allows,
    validate_pat_scopes,
)


def test_pat_scope_allows_probe_cli_paths():
    scopes = ["probe:read", "probe:write", "probe:register", "engagement:read"]
    assert pat_scope_allows("/auth/me", "GET", scopes)
    assert pat_scope_allows("/agents/use-cases", "GET", scopes)
    assert pat_scope_allows("/agents/register", "POST", scopes)
    assert pat_scope_allows("/agents/jobs", "POST", scopes)
    assert pat_scope_allows("/engagements/abc/scope", "GET", scopes)
    assert not pat_scope_allows("/engagements", "POST", scopes)
    assert not pat_scope_allows("/exploits", "POST", scopes)


def test_pat_scope_matrix_for_api_scopes():
    assert pat_scope_allows("/exploits", "GET", ["api:read"])
    assert not pat_scope_allows("/exploits", "POST", ["api:read"])
    assert pat_scope_allows("/exploits", "GET", ["api:write"])
    assert pat_scope_allows("/exploits", "POST", ["api:write"])
    assert pat_scope_allows("/any/path", "DELETE", ["api:*"])


def test_validate_pat_scopes_dedupes_and_rejects_unknown():
    assert validate_pat_scopes(["probe:read", "probe:read", "probe:write"]) == [
        "probe:read",
        "probe:write",
    ]
    with pytest.raises(ValueError, match="unsupported"):
        validate_pat_scopes(["probe:read", "admin:root"])


def test_new_pat_token_shape_and_hash_stability():
    token = new_pat_token()
    assert token.startswith("vpat_")
    assert len(token) > 40
    assert hash_pat_token(token) == hash_pat_token(token)
    assert hash_pat_token(token) != token


def test_pat_builder_returns_token_once_and_stores_hash_only():
    tenant_id = uuid.uuid4()
    user_id = uuid.uuid4()
    token, row = build_personal_access_token(
        tenant_id=tenant_id,
        user_id=user_id,
        name="client-dmz",
        role="manager",
        scopes=["probe:read", "probe:register"],
        expires_in_days=30,
    )

    assert token.startswith("vpat_")
    assert row.tenant_id == tenant_id
    assert row.user_id == user_id
    assert row.token_hash == hash_pat_token(token)
    assert row.token_hash != token
    assert row.token_prefix == token[:16]
    assert row.scopes == ["probe:read", "probe:register"]
    assert row.expires_at is not None


def test_pat_builder_supports_non_expiring_tokens_only_when_requested():
    token, row = build_personal_access_token(
        tenant_id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        name="break-glass",
        role="admin",
        scopes=["api:*"],
        expires_in_days=None,
    )

    assert token.startswith("vpat_")
    assert row.expires_at is None


def test_pat_builder_rejects_unknown_scope():
    with pytest.raises(ValueError, match="unsupported"):
        build_personal_access_token(
            tenant_id=uuid.uuid4(),
            user_id=uuid.uuid4(),
            name="bad",
            role="manager",
            scopes=["probe:read", "admin:root"],
            expires_in_days=30,
        )

"""test_customer_reveal.py — operator reveal of a customer login password (item 1)."""
from __future__ import annotations

import asyncio
import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import HTTPException

from app.routers import customer_access as ca
from app.schemas.auth import CurrentUser
from app.services import credential_crypto as cc


def _operator() -> CurrentUser:
    return CurrentUser(user_id=uuid.uuid4(), tenant_id=uuid.uuid4(), role="manager")


def _db(user):
    db = MagicMock()
    r = MagicMock()
    r.scalar_one_or_none = MagicMock(return_value=user)
    db.execute = AsyncMock(return_value=r)
    db.flush = AsyncMock()
    return db


def _user(enc):
    return SimpleNamespace(id=uuid.uuid4(), email="c@example.com",
                           client_engagement_id=uuid.uuid4(), portal_password_enc=enc)


def test_reveal_returns_decrypted_password():
    user = _user(cc.encrypt_credential("hunter2!"))
    res = asyncio.run(ca.reveal_customer_password(user.id, _db(user), _operator()))
    assert res.email == "c@example.com"
    assert res.password == "hunter2!"


def test_reveal_null_ciphertext_returns_none():
    user = _user(None)   # login provisioned before encrypted storage existed
    res = asyncio.run(ca.reveal_customer_password(user.id, _db(user), _operator()))
    assert res.password is None


def test_reveal_missing_user_is_404():
    with pytest.raises(HTTPException) as e:
        asyncio.run(ca.reveal_customer_password(uuid.uuid4(), _db(None), _operator()))
    assert e.value.status_code == 404

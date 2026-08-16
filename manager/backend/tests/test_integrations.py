"""test_integrations.py — operator notification-integration config (item 3)."""
from __future__ import annotations

import asyncio
import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import HTTPException

from app.routers import integrations as ig
from app.schemas.auth import CurrentUser
from app.services import credential_crypto as cc


def _operator() -> CurrentUser:
    return CurrentUser(user_id=uuid.uuid4(), tenant_id=uuid.uuid4(), role="manager")


def _db(row):
    db = MagicMock()
    r = MagicMock()
    r.scalar_one_or_none = MagicMock(return_value=row)
    db.execute = AsyncMock(return_value=r)
    db.flush = AsyncMock()
    db.add = MagicMock()
    return db


class TestPutIntegration:
    def test_rejects_unknown_kind(self):
        body = ig.IntegrationIn(config={}, secret="x")
        with pytest.raises(HTTPException) as e:
            asyncio.run(ig.put_integration("telegram", body, _db(None), _operator()))
        assert e.value.status_code == 422

    def test_create_encrypts_secret_and_masks_it(self):
        db = _db(None)
        body = ig.IntegrationIn(config={"SLACK_CHANNEL": "#sec"}, secret="https://hooks.slack/xyz")
        res = asyncio.run(ig.put_integration("slack", body, db, _operator()))
        assert res.kind == "slack"
        assert res.has_secret is True
        # the response object never carries the raw secret
        assert "secret" not in res.model_dump()
        # what got stored is ciphertext, and it decrypts back to the input.
        # (db.add is called twice: the Integration first, then the audit log.)
        stored = db.add.call_args_list[0][0][0]
        assert stored.secret_enc != "https://hooks.slack/xyz"
        assert cc.decrypt_credential(stored.secret_enc) == "https://hooks.slack/xyz"

    def test_update_without_secret_keeps_existing(self):
        existing = SimpleNamespace(id=uuid.uuid4(), kind="email",
                                   config={"SMTP_HOST": "old"}, secret_enc="KEEPME", enabled=True)
        db = _db(existing)
        body = ig.IntegrationIn(config={"SMTP_HOST": "new"}, secret=None, enabled=False)
        res = asyncio.run(ig.put_integration("email", body, db, _operator()))
        assert existing.secret_enc == "KEEPME"        # unchanged
        assert existing.config == {"SMTP_HOST": "new"}
        assert res.enabled is False and res.has_secret is True


class TestListIntegrations:
    def test_list_masks_secret(self):
        row = SimpleNamespace(kind="jira", config={"JIRA_URL": "https://x"},
                              secret_enc="cipher", enabled=True)
        db = MagicMock()
        r = MagicMock()
        r.scalars = MagicMock(return_value=MagicMock(all=MagicMock(return_value=[row])))
        db.execute = AsyncMock(return_value=r)
        res = asyncio.run(ig.list_integrations(db, _operator()))
        assert len(res) == 1
        assert res[0].has_secret is True
        assert "secret" not in res[0].model_dump()

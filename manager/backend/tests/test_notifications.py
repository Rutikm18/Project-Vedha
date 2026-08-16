"""test_notifications.py — integration delivery fan-out (item 3 delivery worker)."""
from __future__ import annotations

import asyncio
import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

from app.services import credential_crypto as cc
from app.services import notifications as nt


class TestDeliver:
    def test_dispatches_to_the_kind(self):
        calls = []
        senders = {"slack": lambda config, secret, subj, body: calls.append((secret, subj, body))}
        ok = nt.deliver("slack", {}, "hook", "Sub", "Body", senders=senders)
        assert ok is True
        assert calls == [("hook", "Sub", "Body")]

    def test_unknown_kind_returns_false(self):
        assert nt.deliver("telegram", {}, None, "s", "b", senders={}) is False

    def test_sender_error_is_swallowed(self):
        def boom(*_a):
            raise RuntimeError("smtp down")
        assert nt.deliver("email", {}, None, "s", "b", senders={"email": boom}) is False


class TestNotifyTenant:
    def test_fans_to_enabled_and_decrypts_secret(self):
        enc = cc.encrypt_credential("hook-url")
        rows = [
            SimpleNamespace(kind="slack", config={}, secret_enc=enc, enabled=True),
            SimpleNamespace(kind="email", config={"SMTP_HOST": "h"}, secret_enc=None, enabled=True),
        ]
        db = MagicMock()
        r = MagicMock()
        r.scalars = MagicMock(return_value=MagicMock(all=MagicMock(return_value=rows)))
        db.execute = AsyncMock(return_value=r)

        seen: dict[str, str | None] = {}
        senders = {
            "slack": lambda c, s, subj, b: seen.__setitem__("slack", s),
            "email": lambda c, s, subj, b: seen.__setitem__("email", s),
        }
        n = asyncio.run(nt.notify_tenant(db, uuid.uuid4(), "Sub", "Body", senders=senders))
        assert n == 2
        assert seen["slack"] == "hook-url"      # ciphertext decrypted before the sender sees it
        assert seen["email"] is None

    def test_counts_only_successful_channels(self):
        rows = [SimpleNamespace(kind="slack", config={}, secret_enc=None, enabled=True),
                SimpleNamespace(kind="email", config={}, secret_enc=None, enabled=True)]
        db = MagicMock()
        r = MagicMock()
        r.scalars = MagicMock(return_value=MagicMock(all=MagicMock(return_value=rows)))
        db.execute = AsyncMock(return_value=r)

        def boom(*_a):
            raise RuntimeError("fail")
        senders = {"slack": lambda *_a: None, "email": boom}
        n = asyncio.run(nt.notify_tenant(db, uuid.uuid4(), "S", "B", senders=senders))
        assert n == 1                            # slack ok, email failed

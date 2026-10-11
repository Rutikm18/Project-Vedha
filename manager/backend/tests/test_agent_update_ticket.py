"""test_agent_update_ticket.py — an enrolled agent fetching its own update.

An installed agent has no enrolment token, so it could not download an update. The manager
now decides whether an agent should update and, if so, gives it a short-lived single-use
ticket the download route accepts. These tests pin: the ticket cannot be forged, replayed,
used after expiry or by the wrong agent; the manager only issues one when an update really
is due and applicable; and the download route re-checks all of that.
"""
from __future__ import annotations

import asyncio
import re
import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import HTTPException

from app.auth.middleware import agent_jwt_path_allows
from app.routers import agent_distribution as dist
from app.routers import agents as ag
from app.services import agent_update_ticket as tk

AGENT = str(uuid.uuid4())
TENANT = str(uuid.uuid4())
NOW = 1_800_000_000.0


# ── the ticket itself ────────────────────────────────────────────────────────

class TestTicket:
    def test_round_trip(self):
        raw = tk.issue(AGENT, TENANT, "2.3.0", now=NOW)
        claims = tk.verify(raw, now=NOW + 10)
        assert claims and claims.agent_id == AGENT and claims.tenant_id == TENANT and claims.version == "2.3.0"
        assert claims.expires_at == int(NOW) + tk.TTL_SECONDS

    def test_the_windows_installer_accepts_it_as_a_token(self):
        """install.ps1 validates -Token with ^vet_[A-Za-z0-9_-]{8,}$ and sends it as the bearer."""
        raw = tk.issue(AGENT, TENANT, "2.3.0", now=NOW)
        assert re.fullmatch(r"vet_[A-Za-z0-9_-]{8,}", raw), raw
        assert raw.startswith("vet_") and tk.is_ticket(raw)
        assert len(raw) < tk.MAX_TICKET_CHARS

    def test_two_tickets_differ(self):
        assert tk.issue(AGENT, TENANT, "2.3.0", now=NOW) != tk.issue(AGENT, TENANT, "2.3.0", now=NOW)

    def test_expired(self):
        raw = tk.issue(AGENT, TENANT, "2.3.0", now=NOW)
        assert tk.verify(raw, now=NOW + tk.TTL_SECONDS) is None
        assert tk.verify(raw, now=NOW + tk.TTL_SECONDS - 1) is not None

    @pytest.mark.parametrize("mutate", [
        lambda r: r[:-1] + ("0" if r[-1] != "0" else "1"),                  # one signature digit
        lambda r: r.replace("vet_upd-", "vet_upd-A", 1),                    # payload shifted
        lambda r: r.rsplit("-", 1)[0] + "-" + "0" * 64,                     # signature replaced
        lambda r: "vet_upd-" + r.split("-", 1)[1].rsplit("-", 1)[0],        # signature dropped
        lambda r: "",
        lambda r: "vet_abc",
        lambda r: r + "x" * 700,
    ])
    def test_tampered_or_malformed_is_refused(self, mutate):
        assert tk.verify(mutate(tk.issue(AGENT, TENANT, "2.3.0", now=NOW)), now=NOW) is None

    def test_a_ticket_for_another_agent_cannot_be_edited_into_ours(self):
        import base64, json
        raw = tk.issue(str(uuid.uuid4()), TENANT, "2.3.0", now=NOW)
        body, sig = raw[len(tk.PREFIX):].rsplit("-", 1)
        claims = json.loads(base64.urlsafe_b64decode(body + "=" * (-len(body) % 4)))
        claims["a"] = AGENT
        forged = base64.urlsafe_b64encode(json.dumps(claims, separators=(",", ":")).encode()).decode().rstrip("=")
        assert tk.verify(f"{tk.PREFIX}{forged}-{sig}", now=NOW) is None

    def test_a_different_manager_secret_does_not_verify(self, monkeypatch):
        raw = tk.issue(AGENT, TENANT, "2.3.0", now=NOW)
        monkeypatch.setattr(tk, "get_settings", lambda: SimpleNamespace(jwt_secret="another-manager-secret-32-chars-long!!"))
        assert tk.verify(raw, now=NOW) is None


# ── the manager issuing one ──────────────────────────────────────────────────

def _release(agent_version="2.3.0", windows=True):
    return SimpleNamespace(version="1.0.400", agent_version=agent_version, windows_available=windows)


def _ask(version="2.2.0", platform="win32", *, release=None, token_sub=None, agent_status="active",
         boom=None, monkeypatch=None):
    row = SimpleNamespace(id=uuid.UUID(AGENT), tenant_id=uuid.UUID(TENANT), agent_version="2.0.0",
                          lifecycle_status=agent_status)
    db = MagicMock()
    db.execute = AsyncMock(return_value=MagicMock(scalar_one_or_none=lambda: row))
    db.flush = AsyncMock()
    request = SimpleNamespace(state=SimpleNamespace(user_id=token_sub or AGENT))

    def loader():
        if boom:
            raise boom
        return release

    monkeypatch.setattr(dist, "load_current_release", loader)
    body = ag.UpdateCheckRequest(agent_id=AGENT, agent_version=version, platform=platform, architecture="AMD64")
    return asyncio.run(ag.update_ticket(body, db, request)), row


class TestIssuing:
    def test_a_windows_agent_with_an_update_due_gets_a_ticket(self, monkeypatch):
        out, row = _ask(release=_release(), monkeypatch=monkeypatch)
        assert out["update_available"] and out["latest"] == "2.3.0"
        claims = tk.verify(out["ticket"])
        assert claims and claims.agent_id == AGENT and claims.tenant_id == TENANT and claims.version == "2.3.0"
        assert out["ticket_expires_in_seconds"] == tk.TTL_SECONDS
        assert row.agent_version == "2.2.0"                       # what is running is recorded

    def test_up_to_date_gets_no_ticket(self, monkeypatch):
        out, _ = _ask("2.3.0", release=_release(), monkeypatch=monkeypatch)
        assert out["update_available"] is False and out["ticket"] is None

    def test_a_downgrade_is_never_offered(self, monkeypatch):
        out, _ = _ask("3.0.0", release=_release("2.3.0"), monkeypatch=monkeypatch)
        assert out["ticket"] is None

    def test_no_release_is_a_normal_answer(self, monkeypatch):
        from app import agent_release
        out, _ = _ask(boom=agent_release.ReleaseUnavailable("none"), monkeypatch=monkeypatch)
        assert out["update_available"] is False and out["ticket"] is None

    @pytest.mark.parametrize("platform", ["linux", "darwin", ""])
    def test_only_windows_agents_can_apply_it_today(self, platform, monkeypatch):
        out, _ = _ask(platform=platform, release=_release(), monkeypatch=monkeypatch)
        assert out["ticket"] is None and out["update_available"] is False
        assert "automatically" in out["message"]

    def test_a_release_without_a_windows_package_gives_no_ticket(self, monkeypatch):
        out, _ = _ask(release=_release(windows=False), monkeypatch=monkeypatch)
        assert out["ticket"] is None

    def test_another_agents_credential_is_refused(self, monkeypatch):
        with pytest.raises(HTTPException) as exc:
            _ask(release=_release(), token_sub=str(uuid.uuid4()), monkeypatch=monkeypatch)
        assert exc.value.status_code == 403

    def test_a_revoked_agent_gets_nothing(self, monkeypatch):
        with pytest.raises(HTTPException) as exc:
            _ask(release=_release(), agent_status="revoked", monkeypatch=monkeypatch)
        assert exc.value.status_code == 403

    def test_the_route_is_reachable_with_an_agent_credential_and_only_by_post(self):
        assert agent_jwt_path_allows("/agents/update-ticket", "POST") is True
        assert agent_jwt_path_allows("/agents/update-ticket", "GET") is False


# ── the download route accepting it ──────────────────────────────────────────

class _Redis:
    def __init__(self):
        self.seen: set[str] = set()

    async def set(self, key, value, nx=False, ex=None):
        if nx and key in self.seen:
            return None
        self.seen.add(key)
        return True


def _download(raw, *, agent_version="2.2.0", tenant=TENANT, status="active", release_version="2.3.0",
              redis=None, agent_exists=True, monkeypatch=None):
    row = SimpleNamespace(id=uuid.UUID(AGENT), tenant_id=uuid.UUID(tenant), agent_version=agent_version,
                          lifecycle_status=status) if agent_exists else None
    db = MagicMock()
    db.execute = AsyncMock(return_value=MagicMock(scalar_one_or_none=lambda: row))
    monkeypatch.setattr(dist, "_release_or_503", lambda: _release(release_version))
    request = SimpleNamespace(headers={}, client=SimpleNamespace(host="1.2.3.4"), state=SimpleNamespace())
    return asyncio.run(dist._authorize_update_ticket(raw, request, db, redis or _Redis()))


class TestDownload:
    def test_a_valid_ticket_is_accepted_once(self, monkeypatch):
        raw, redis = tk.issue(AGENT, TENANT, "2.3.0"), _Redis()
        who = _download(raw, redis=redis, monkeypatch=monkeypatch)
        assert str(who.tenant_id) == TENANT and AGENT in who.id
        with pytest.raises(HTTPException) as exc:
            _download(raw, redis=redis, monkeypatch=monkeypatch)
        assert exc.value.status_code == 401 and "already used" in exc.value.detail

    def test_garbage_and_expired_tickets_are_401(self, monkeypatch):
        for raw in ("vet_upd-abc-def", tk.issue(AGENT, TENANT, "2.3.0", now=1.0)):
            with pytest.raises(HTTPException) as exc:
                _download(raw, monkeypatch=monkeypatch)
            assert exc.value.status_code == 401

    def test_a_ticket_for_a_deleted_or_revoked_agent_is_401(self, monkeypatch):
        raw = tk.issue(AGENT, TENANT, "2.3.0")
        for kwargs in ({"agent_exists": False}, {"status": "revoked"}, {"tenant": str(uuid.uuid4())}):
            with pytest.raises(HTTPException) as exc:
                _download(raw, monkeypatch=monkeypatch, **kwargs)
            assert exc.value.status_code == 401, kwargs

    def test_it_cannot_reinstall_the_same_version_or_roll_back(self, monkeypatch):
        raw = tk.issue(AGENT, TENANT, "2.3.0")
        for running in ("2.3.0", "2.4.0"):
            with pytest.raises(HTTPException) as exc:
                _download(raw, agent_version=running, redis=_Redis(), monkeypatch=monkeypatch)
            assert exc.value.status_code == 409

    def test_a_failed_check_does_not_spend_the_ticket(self, monkeypatch):
        raw, redis = tk.issue(AGENT, TENANT, "2.3.0"), _Redis()
        with pytest.raises(HTTPException):
            _download(raw, agent_version="2.3.0", redis=redis, monkeypatch=monkeypatch)
        assert _download(raw, redis=redis, monkeypatch=monkeypatch)       # still usable afterwards

    def test_redis_down_fails_closed(self, monkeypatch):
        class Down:
            async def set(self, *a, **k):
                raise ConnectionError("redis down")
        with pytest.raises(HTTPException) as exc:
            _download(tk.issue(AGENT, TENANT, "2.3.0"), redis=Down(), monkeypatch=monkeypatch)
        assert exc.value.status_code == 503

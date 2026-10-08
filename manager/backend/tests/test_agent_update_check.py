"""test_agent_update_check.py — the manager's answer to "is there a newer agent?"

Version management only: the manager says what it would serve; nothing is
downloaded. The agent has its own version (agent_version in the signed manifest),
separate from the platform release version that names the release directory.
"""
from __future__ import annotations

import asyncio
import base64
import json
import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from fastapi import HTTPException

from app import agent_release
from app.auth.middleware import agent_jwt_path_allows
from app.routers import agent_distribution as dist
from app.routers import agents as ag

from tests.test_agent_distribution import _keypair, build_release


@pytest.fixture(autouse=True)
def _fresh_cache():
    agent_release.clear_cache()
    yield
    agent_release.clear_cache()


def _release(tmp_path, key, pub, **manifest):
    build_release(tmp_path, key, manifest_overrides=manifest or None)
    return agent_release.load_release(tmp_path, pub)


# ── versions ─────────────────────────────────────────────────────────────────

class TestVersionCompare:
    @pytest.mark.parametrize("latest,current,expected", [
        ("2.2.0", "2.1.0", True), ("2.10.0", "2.9.0", True), ("3", "2.9.9", True),
        ("2.1.0", "2.1.0", False), ("2.1", "2.1.0", False), ("2.0.9", "2.1.0", False),
        ("x", "2.1.0", False), ("2.2.0", "x", False), (None, "2.1.0", False), ("2.2.0", None, False),
    ])
    def test_is_newer(self, latest, current, expected):
        assert agent_release.agent_version_is_newer(latest, current) is expected

    @pytest.mark.parametrize("text,expected", [
        ("2.1.0", (2, 1, 0)), ("v2.1", (2, 1)), ("2.1.0-rc1", (2, 1, 0)), ("", None),
        ("2.1.0.0.0", None), (7, None), ("2..1", None),
    ])
    def test_parse(self, text, expected):
        assert agent_release.parse_agent_version(text) == expected

    @pytest.mark.parametrize("text,expected", [
        ("2.1.0", "2.1.0"), (" 2.1.0 ", "2.1.0"), ("2.1.0-rc1+b5", "2.1.0-rc1+b5"),
        ("", None), (None, None), (5, None), ("a" * 65, None), ("2 1", None),
        ("2.1.0;DROP TABLE", None), ("../../x", None), ("<script>", None),
    ])
    def test_clean_agent_version_accepts_only_plain_tokens(self, text, expected):
        assert agent_release.clean_agent_version(text) == expected


# ── the manifest field ───────────────────────────────────────────────────────

class TestManifestAgentVersion:
    def test_release_with_an_agent_version_exposes_it(self, tmp_path):
        key, pub = _keypair()
        release = _release(tmp_path, key, pub, agent_version="2.1.0")
        assert release.agent_version == "2.1.0"
        assert release.version == "1.0.400"          # the platform release is a different number

    def test_a_release_without_the_field_still_loads(self, tmp_path):
        key, pub = _keypair()
        assert _release(tmp_path, key, pub).agent_version == ""

    @pytest.mark.parametrize("bad", ["not a version", "2.1.0.0.0", 7, ["2.1.0"], "../x"])
    def test_malformed_agent_version_is_refused(self, tmp_path, bad):
        key, pub = _keypair()
        build_release(tmp_path, key, manifest_overrides={"agent_version": bad})
        with pytest.raises(agent_release.ReleaseUnavailable, match="agent_version"):
            agent_release.load_release(tmp_path, pub)

    def test_the_field_is_covered_by_the_signature(self, tmp_path):
        """Editing agent_version after signing must break the release, or a
        tampered manager store could invent updates."""
        key, pub = _keypair()
        directory = build_release(tmp_path, key, manifest_overrides={"agent_version": "2.1.0"})
        manifest = json.loads((directory / "manifest.json").read_bytes())
        manifest["agent_version"] = "9.9.9"
        (directory / "manifest.json").write_bytes(json.dumps(manifest, indent=2).encode())
        with pytest.raises(agent_release.ReleaseUnavailable, match="signature"):
            agent_release.load_release(tmp_path, pub)

    def test_fleet_release_status_shows_it(self, tmp_path, monkeypatch):
        key, pub = _keypair()
        build_release(tmp_path, key, manifest_overrides={"agent_version": "2.1.0"})
        monkeypatch.setattr(dist, "get_settings", lambda: SimpleNamespace(
            agent_release_dir=str(tmp_path), agent_release_public_key=pub,
            agent_release_require_signature=True, is_production=False, manager_public_url="https://m"))
        status = dist.release_status(detailed=True)
        assert status["available"] and status["agent_version"] == "2.1.0" and status["version"] == "1.0.400"


# ── what the manager offers ──────────────────────────────────────────────────

class TestUpdateOffer:
    def _release(self, agent_version="2.2.0"):
        return SimpleNamespace(version="1.0.400", agent_version=agent_version)

    def test_newer_release_is_offered(self):
        offer = agent_release.update_offer(self._release("2.2.0"), "2.1.0")
        assert offer["update_available"] is True
        assert offer["latest"] == "2.2.0" and offer["current"] == "2.1.0"
        assert offer["manager_release"] == "1.0.400"

    def test_same_or_older_offers_nothing_but_says_what_is_current(self):
        for current in ("2.2.0", "2.3.0"):
            offer = agent_release.update_offer(self._release("2.2.0"), current)
            assert offer["update_available"] is False and offer["latest"] == "2.2.0"

    def test_no_release_is_a_normal_answer(self):
        offer = agent_release.update_offer(None, "2.1.0")
        assert offer["update_available"] is False and offer["latest"] is None
        assert offer["manager_release"] is None and "No agent release" in offer["message"]

    def test_old_release_without_an_agent_version_offers_nothing(self):
        offer = agent_release.update_offer(self._release(""), "2.1.0")
        assert offer["update_available"] is False and offer["latest"] is None

    def test_garbage_from_the_agent_never_offers_an_update(self):
        for current in ("", "junk", None, 5):
            assert agent_release.update_offer(self._release("9.9.9"), current)["update_available"] is False


# ── the route ────────────────────────────────────────────────────────────────

def _call(agent_id, body_version, *, token_sub=None, agent=True, release=None, boom=None, monkeypatch=None):
    agent_row = SimpleNamespace(id=uuid.UUID(agent_id), agent_version="2.0.0") if agent else None
    db = MagicMock()
    db.execute = AsyncMock(return_value=MagicMock(scalar_one_or_none=lambda: agent_row))
    db.flush = AsyncMock()
    request = SimpleNamespace(state=SimpleNamespace(user_id=token_sub if token_sub is not None else agent_id))

    def loader():
        if boom:
            raise boom
        return release

    monkeypatch.setattr(dist, "load_current_release", loader)
    body = ag.UpdateCheckRequest(agent_id=agent_id, agent_version=body_version,
                                 platform="win32", architecture="AMD64")
    out = asyncio.run(ag.update_check(body, db, request))
    return out, agent_row, db


class TestRoute:
    def release(self, agent_version="2.2.0"):
        return SimpleNamespace(version="1.0.400", agent_version=agent_version)

    def test_offers_a_newer_agent_and_records_the_running_version(self, monkeypatch):
        agent_id = str(uuid.uuid4())
        out, row, db = _call(agent_id, "2.1.0", release=self.release(), monkeypatch=monkeypatch)
        assert out["update_available"] is True and out["latest"] == "2.2.0"
        assert row.agent_version == "2.1.0"          # Fleet now shows what is really running
        db.flush.assert_awaited_once()

    def test_up_to_date_agent_is_told_so(self, monkeypatch):
        agent_id = str(uuid.uuid4())
        out, _, _ = _call(agent_id, "2.2.0", release=self.release(), monkeypatch=monkeypatch)
        assert out["update_available"] is False

    def test_no_published_release_is_not_an_error(self, monkeypatch):
        agent_id = str(uuid.uuid4())
        out, _, _ = _call(agent_id, "2.1.0", boom=agent_release.ReleaseUnavailable("none"),
                          monkeypatch=monkeypatch)
        assert out["update_available"] is False and out["manager_release"] is None

    def test_another_agents_token_is_refused(self, monkeypatch):
        agent_id = str(uuid.uuid4())
        with pytest.raises(HTTPException) as exc:
            _call(agent_id, "2.1.0", token_sub=str(uuid.uuid4()), release=self.release(),
                  monkeypatch=monkeypatch)
        assert exc.value.status_code == 403

    def test_unknown_agent_is_404(self, monkeypatch):
        with pytest.raises(HTTPException) as exc:
            _call(str(uuid.uuid4()), "2.1.0", agent=False, release=self.release(), monkeypatch=monkeypatch)
        assert exc.value.status_code == 404

    def test_a_junk_version_is_not_stored(self, monkeypatch):
        agent_id = str(uuid.uuid4())
        _, row, _ = _call(agent_id, "2.1.0;DROP", release=self.release(), monkeypatch=monkeypatch)
        assert row.agent_version == "2.0.0"

    def test_request_validation(self):
        with pytest.raises(Exception):
            ag.UpdateCheckRequest(agent_id="a", agent_version="")
        with pytest.raises(Exception):
            ag.UpdateCheckRequest(agent_id="a", agent_version="x" * 65)


class TestHeartbeatRecordsVersion:
    def run(self, version):
        agent_id = uuid.uuid4()
        row = SimpleNamespace(id=agent_id, status=ag.AgentStatus.online, current_job_id=None,
                              last_heartbeat=None, agent_version="2.0.0")
        db = MagicMock()
        db.execute = AsyncMock(return_value=MagicMock(scalar_one_or_none=lambda: row))
        db.flush = AsyncMock()
        request = SimpleNamespace(state=SimpleNamespace(user_id=str(agent_id)))
        asyncio.run(ag.heartbeat(
            ag.HeartbeatRequest(agent_id=str(agent_id), status="online", agent_version=version), db, request))
        return row

    def test_the_running_version_is_recorded(self):
        assert self.run("2.1.0").agent_version == "2.1.0"

    def test_an_older_agent_that_sends_nothing_changes_nothing(self):
        assert self.run(None).agent_version == "2.0.0"

    def test_junk_is_ignored(self):
        assert self.run("<script>").agent_version == "2.0.0"

    def test_field_is_optional_and_bounded(self):
        assert ag.HeartbeatRequest(agent_id="a").agent_version is None
        with pytest.raises(Exception):
            ag.HeartbeatRequest(agent_id="a", agent_version="x" * 65)


# ── authentication boundary ──────────────────────────────────────────────────

class TestAuthBoundary:
    def test_agent_tokens_may_post_update_check_and_nothing_else_there(self):
        assert agent_jwt_path_allows("/agents/update-check", "POST") is True
        for method in ("GET", "PUT", "DELETE", "PATCH"):
            assert agent_jwt_path_allows("/agents/update-check", method) is False

    def test_it_does_not_widen_neighbouring_paths(self):
        for path in ("/agents/update-check/", "/agents/update-checks", "/agents/update-check/x"):
            assert agent_jwt_path_allows(path, "POST") is False

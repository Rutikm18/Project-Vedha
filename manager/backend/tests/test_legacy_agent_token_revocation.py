"""Legacy agent JWTs are held to the same Fleet controls as device tokens.

/agents/register issues a one-year role=agent JWT with no `typ`. The middleware
used to look the agent up only for typ=device_access tokens, so a legacy probe
whose access had expired in Fleet (or whose row was gone) kept polling for jobs
until the token itself lapsed.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient

from app.auth import middleware as mw
from app.auth.jwt import create_access_token, create_device_access_token

AGENT_ID = uuid.uuid4()
TENANT_ID = uuid.uuid4()


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _agent(**overrides):
    fields = {"id": AGENT_ID, "tenant_id": TENANT_ID, "lifecycle_status": "active",
              "credential_generation": 1, "access_expires_at": None}
    fields.update(overrides)
    return SimpleNamespace(**fields)


@pytest.fixture
def agent_row(monkeypatch):
    """The agent row the middleware will find (None = no such agent)."""
    holder = {"row": _agent()}

    class _Session:
        async def __aenter__(self):
            db = MagicMock()
            result = MagicMock()
            result.scalar_one_or_none = MagicMock(side_effect=lambda: holder["row"])
            db.execute = AsyncMock(return_value=result)
            return db

        async def __aexit__(self, *exc):
            return False

    monkeypatch.setattr(mw, "AsyncSessionLocal", _Session)
    return holder


def _client() -> TestClient:
    app = FastAPI()

    @app.get("/agents/{agent_id}/jobs")
    async def jobs(agent_id: str, request: Request):
        return JSONResponse({"agent": request.state.user_id})

    @app.post("/agents/{agent_id}/jobs/{job_id}/result")
    async def result(agent_id: str, job_id: str):
        return JSONResponse({"ok": True})

    app.add_middleware(mw.TenantIsolationMiddleware)
    return TestClient(app)


def _legacy_token(sub=None) -> str:
    return create_access_token(str(sub or AGENT_ID), str(TENANT_ID), "agent",
                               expires_minutes=60 * 24 * 365)


def _poll(token):
    return _client().get(f"/agents/{AGENT_ID}/jobs", headers={"Authorization": f"Bearer {token}"})


def test_live_legacy_agent_still_polls(agent_row):
    assert _poll(_legacy_token()).status_code == 200


def test_expired_legacy_agent_cannot_poll_for_new_work(agent_row):
    agent_row["row"] = _agent(access_expires_at=_now() - timedelta(minutes=1))
    response = _poll(_legacy_token())
    assert response.status_code == 403
    assert "expired" in response.json()["detail"].lower()


def test_expired_legacy_agent_may_still_upload_in_flight_results(agent_row):
    agent_row["row"] = _agent(access_expires_at=_now() - timedelta(minutes=1))
    response = _client().post(
        f"/agents/{AGENT_ID}/jobs/{uuid.uuid4()}/result",
        headers={"Authorization": f"Bearer {_legacy_token()}"},
    )
    assert response.status_code == 200


def test_removed_legacy_agent_is_rejected(agent_row):
    agent_row["row"] = None
    assert _poll(_legacy_token()).status_code == 401


def test_disabled_legacy_agent_is_rejected(agent_row):
    agent_row["row"] = _agent(lifecycle_status="disabled")
    assert _poll(_legacy_token()).status_code == 401


def test_non_uuid_subject_is_rejected_not_a_server_error(agent_row):
    assert _poll(_legacy_token(sub="agent-1")).status_code == 401


def test_device_token_generation_check_unchanged(agent_row):
    agent_row["row"] = _agent(credential_generation=2)
    stale = create_device_access_token(str(AGENT_ID), str(TENANT_ID), credential_generation=1)
    assert _poll(stale).status_code == 401
    current = create_device_access_token(str(AGENT_ID), str(TENANT_ID), credential_generation=2)
    assert _poll(current).status_code == 200

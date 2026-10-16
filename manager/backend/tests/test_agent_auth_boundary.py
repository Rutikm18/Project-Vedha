from __future__ import annotations

import pytest
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient

from app.auth.jwt import create_access_token
from app.auth.middleware import (
    _is_public_distribution_request,
    _is_public_enrollment_request,
    agent_jwt_path_allows,
)
from app.auth.middleware import TenantIsolationMiddleware


@pytest.mark.parametrize(
    ("path", "method"),
    [
        ("/agents/heartbeat", "POST"),
        ("/agents/agent-1/refresh", "POST"),
        ("/agents/agent-1/jobs", "GET"),
        ("/agents/agent-1/jobs/job-1/result", "POST"),
        # Per-host durable commit while a job runs, and its resume list — without
        # these the whole partial-evidence path is dead for a JWT probe.
        ("/agents/agent-1/jobs/job-1/chunks", "POST"),
        ("/agents/agent-1/jobs/job-1/chunks", "GET"),
        ("/engagements/eng-1/scope", "GET"),
    ],
)
def test_legacy_agent_jwt_allows_only_workload_operations(path, method):
    assert agent_jwt_path_allows(path, method) is True


@pytest.mark.parametrize(
    ("path", "method"),
    [
        ("/agents", "GET"),
        ("/agents/jobs", "POST"),
        ("/agents/use-cases", "GET"),
        ("/engagements", "GET"),
        ("/engagements/eng-1", "GET"),
        ("/findings", "GET"),
        ("/analytics/exposure", "GET"),
        ("/ai/generate", "POST"),
        ("/agents/heartbeat", "GET"),
        ("/agents/agent-1/jobs", "POST"),
        ("/agents/agent-1/jobs/job-1/chunks", "DELETE"),
        ("/engagements/eng-1/scope", "POST"),
    ],
)
def test_legacy_agent_jwt_rejects_human_and_wrong_method_operations(path, method):
    assert agent_jwt_path_allows(path, method) is False


def _boundary_test_client() -> TestClient:
    app = FastAPI()

    @app.get("/engagements")
    async def engagements(request: Request):
        return JSONResponse({"role": request.state.role})

    app.add_middleware(TenantIsolationMiddleware)
    return TestClient(app)


def test_agent_jwt_is_blocked_before_human_route_handler():
    token = create_access_token("agent-1", "tenant-1", "agent", expires_minutes=5)
    response = _boundary_test_client().get(
        "/engagements",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Agent credential is not permitted on this endpoint"


def test_human_jwt_still_reaches_human_route_handler():
    token = create_access_token("user-1", "tenant-1", "admin", expires_minutes=5)
    response = _boundary_test_client().get(
        "/engagements",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json() == {"role": "admin"}


@pytest.mark.parametrize(
    "path",
    [
        "/probe-enrollment/requests",
        "/probe-enrollment/requests/00000000-0000-0000-0000-000000000000/poll",
        "/probe-enrollment/requests/00000000-0000-0000-0000-000000000000/activate",
        "/probe-enrollment/token",
    ],
)
def test_only_device_side_enrollment_posts_are_public(path):
    assert _is_public_enrollment_request(path, "POST") is True
    assert _is_public_enrollment_request(path, "GET") is False


def test_admin_enrollment_approval_is_not_public():
    assert _is_public_enrollment_request("/probe-enrollment/approve", "POST") is False
    assert _is_public_enrollment_request("/probe-enrollment/requests", "GET") is False


def test_install_code_redeem_post_is_public():
    # The zero-knowledge redeem is public by design: the client holds no credential.
    assert _is_public_distribution_request("/agent/redeem", "POST") is True
    # GET on it is not a public distribution path (redeem is POST-only).
    assert _is_public_distribution_request("/agent/redeem", "GET") is False


def test_existing_distribution_gets_stay_public_and_are_not_posts():
    for path in ("/agent/install.ps1", "/agent/manifest.json", "/agent/package/windows"):
        assert _is_public_distribution_request(path, "GET") is True
        # the only public POST under /agent is redeem — a script fetch POST is not public
        assert _is_public_distribution_request(path, "POST") is False


def test_install_code_management_is_operator_only():
    # Minting / listing / revoking codes requires an admin/manager JWT (not public).
    assert _is_public_distribution_request("/probe-enrollment/install-codes", "POST") is False
    assert _is_public_enrollment_request("/probe-enrollment/install-codes", "POST") is False

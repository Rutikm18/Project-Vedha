"""Tests for agent/transport.py"""
from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import httpx
import pytest

from agent.transport import Transport, TransportError


@pytest.fixture
def transport(tmp_path):
    """Create a Transport with a real state file path but no actual HTTP calls."""
    t = Transport(
        "http://localhost:8000",
        verify_tls=False,
        state_file=tmp_path / "state.json",
    )
    # Mock the underlying client so no real HTTP calls are made
    t._client = MagicMock()
    return t


class TestIdentity:
    def test_is_authenticated_false_initially(self):
        t = Transport("http://localhost:8000")
        assert t.is_authenticated() is False

    def test_is_authenticated_true_with_creds(self):
        t = Transport("http://localhost:8000", agent_id="abc", agent_token="tok123")
        assert t.is_authenticated() is True

    def test_auth_header(self):
        t = Transport("http://localhost:8000", agent_token="tok123")
        assert t.auth_header == {"Authorization": "Bearer tok123"}

    def test_save_and_clear_state(self, tmp_path):
        state_file = tmp_path / "state.json"
        t = Transport("http://localhost:8000", state_file=state_file)
        t.agent_id = "abc"
        t.agent_token = "tok123"
        t.save_state()
        data = json.loads(state_file.read_text())
        assert data["agent_id"] == "abc"
        assert data["token"] == "tok123"

        t.clear_state()
        assert t.agent_id == ""
        assert t.agent_token == ""
        assert state_file.exists() is False


class TestRegister:
    def test_successful_registration(self, transport):
        mock_resp = MagicMock(status_code=201)
        mock_resp.json.return_value = {"agent_id": "abc-123", "token": "tok456"}
        transport._client.post.return_value = mock_resp

        result = transport.register(
            "probe-01",
            location="dc-1",
            capabilities=["discovery", "tls_scan"],
            network_segments=["10.0.0.0/24"],
            operator_token="op-token",
        )

        assert result["agent_id"] == "abc-123"
        assert result["token"] == "tok456"
        assert transport.agent_id == "abc-123"
        assert transport.agent_token == "tok456"

        # Verify the POST call details
        call_args = transport._client.post.call_args
        assert call_args[0][0] == "/agents/register"
        assert call_args[1]["json"]["name"] == "probe-01"
        assert call_args[1]["headers"]["Authorization"] == "Bearer op-token"

    def test_registration_401_raises(self, transport):
        mock_resp = MagicMock(status_code=401)
        transport._client.post.return_value = mock_resp

        with pytest.raises(TransportError, match="rejected"):
            transport.register("probe-01", operator_token="bad-token")

    def test_registration_sends_public_key(self, transport):
        mock_resp = MagicMock(status_code=201)
        mock_resp.json.return_value = {"agent_id": "abc", "token": "tok"}
        transport._client.post.return_value = mock_resp

        transport.register("probe-01", public_key="base64pubkey==", operator_token="tok")
        call_json = transport._client.post.call_args[1]["json"]
        assert call_json["public_key"] == "base64pubkey=="


class TestHeartbeat:
    def test_successful_heartbeat(self, transport):
        transport.agent_id = "abc"
        transport.agent_token = "tok"
        mock_resp = MagicMock(status_code=200)
        transport._client.post.return_value = mock_resp

        result = transport.heartbeat("online")
        assert result is True

    def test_heartbeat_401_returns_false(self, transport):
        transport.agent_id = "abc"
        transport.agent_token = "expired"
        mock_resp = MagicMock(status_code=401)
        transport._client.post.return_value = mock_resp

        result = transport.heartbeat("online")
        assert result is False

    def test_heartbeat_sends_current_job(self, transport):
        transport.agent_id = "abc"
        transport.agent_token = "tok"
        mock_resp = MagicMock(status_code=200)
        transport._client.post.return_value = mock_resp

        transport.heartbeat("busy", "job-123")
        call_json = transport._client.post.call_args[1]["json"]
        assert call_json["status"] == "busy"
        assert call_json["current_job_id"] == "job-123"


class TestPollJobs:
    def test_returns_jobs(self, transport):
        transport.agent_id = "abc"
        transport.agent_token = "tok"
        mock_resp = MagicMock(status_code=200)
        mock_resp.json.return_value = [{"job_id": "j1"}, {"job_id": "j2"}]
        transport._client.get.return_value = mock_resp

        jobs = transport.poll_jobs(limit=2)
        assert len(jobs) == 2
        assert jobs[0]["job_id"] == "j1"

    def test_poll_401_raises(self, transport):
        transport.agent_id = "abc"
        transport.agent_token = "expired"
        mock_resp = MagicMock(status_code=401)
        transport._client.get.return_value = mock_resp

        with pytest.raises(TransportError, match="re-register"):
            transport.poll_jobs()

    def test_poll_uses_limit_param(self, transport):
        transport.agent_id = "abc"
        transport.agent_token = "tok"
        mock_resp = MagicMock(status_code=200)
        mock_resp.json.return_value = []
        transport._client.get.return_value = mock_resp

        transport.poll_jobs(limit=5)
        call_args = transport._client.get.call_args
        assert call_args[1]["params"]["limit"] == 5


class TestFetchScope:
    def test_returns_scope(self, transport):
        transport.agent_id = "abc"
        transport.agent_token = "tok"
        mock_resp = MagicMock(status_code=200)
        mock_resp.json.return_value = {"scope_cidrs": ["10.0.0.0/24"], "excluded_cidrs": []}
        transport._client.get.return_value = mock_resp

        result = transport.fetch_scope("eng-123")
        assert result["scope_cidrs"] == ["10.0.0.0/24"]

    def test_http_error_returns_none(self, transport):
        transport.agent_id = "abc"
        transport.agent_token = "tok"
        transport._client.get.side_effect = httpx.HTTPError("network error")

        result = transport.fetch_scope("eng-123")
        assert result is None


class TestSubmitResult:
    def test_successful_submit(self, transport):
        transport.agent_id = "abc"
        transport.agent_token = "tok"
        mock_resp = MagicMock(status_code=200)
        transport._client.post.return_value = mock_resp

        result = transport.submit_result("job-1", {"success": True, "result": {}})
        assert result is True

    def test_server_error_returns_false(self, transport):
        transport.agent_id = "abc"
        transport.agent_token = "tok"
        mock_resp = MagicMock(status_code=500)
        transport._client.post.return_value = mock_resp

        result = transport.submit_result("job-1", {"success": True})
        assert result is False

    def test_network_error_returns_false(self, transport):
        transport.agent_id = "abc"
        transport.agent_token = "tok"
        transport._client.post.side_effect = httpx.HTTPError("timeout")

        result = transport.submit_result("job-1", {"success": True})
        assert result is False

    def test_client_errors_return_false_no_data_loss(self, transport):
        # 4xx must NOT be treated as success — otherwise the caller deletes the
        # spooled result and scan data is lost (401=expired token, 413=too large,
        # 422=validation). Regression guard for the <500 == success bug.
        transport.agent_id = "abc"
        transport.agent_token = "tok"
        for code in (400, 401, 403, 404, 409, 413, 422):
            transport._client.post.return_value = MagicMock(status_code=code)
            assert transport.submit_result("job-1", {"success": True}) is False, code

    def test_2xx_variants_return_true(self, transport):
        transport.agent_id = "abc"
        transport.agent_token = "tok"
        for code in (200, 201, 202, 204):
            transport._client.post.return_value = MagicMock(status_code=code)
            assert transport.submit_result("job-1", {"success": True}) is True, code

    def test_large_payload_is_gzipped(self, transport):
        transport.agent_id = "abc"
        transport.agent_token = "tok"
        transport._compress_over = 100  # force compression for the test
        transport._client.post.return_value = MagicMock(status_code=200)
        big = {"success": True, "result": {"facts": ["x" * 1000]}}
        assert transport.submit_result("job-1", big) is True
        _, kwargs = transport._client.post.call_args
        assert kwargs["headers"].get("Content-Encoding") == "gzip"
        assert kwargs["content"][:2] == b"\x1f\x8b"  # gzip magic bytes

    def test_small_payload_not_gzipped(self, transport):
        transport.agent_id = "abc"
        transport.agent_token = "tok"
        transport._client.post.return_value = MagicMock(status_code=200)
        assert transport.submit_result("job-1", {"success": True}) is True
        _, kwargs = transport._client.post.call_args
        assert "Content-Encoding" not in kwargs["headers"]


class TestHttpGet:
    def test_successful_get(self, transport):
        transport.agent_id = "abc"
        transport.agent_token = "tok"
        mock_resp = MagicMock(status_code=200)
        mock_resp.json.return_value = {"key": "value"}
        transport._client.get.return_value = mock_resp

        result = transport.http_get("/some/path")
        assert result == {"key": "value"}

    def test_non_200_returns_none(self, transport):
        transport.agent_id = "abc"
        transport.agent_token = "tok"
        mock_resp = MagicMock(status_code=404)
        transport._client.get.return_value = mock_resp

        result = transport.http_get("/missing")
        assert result is None

    def test_exception_returns_none(self, transport):
        transport.agent_id = "abc"
        transport.agent_token = "tok"
        transport._client.get.side_effect = httpx.HTTPError("boom")

        result = transport.http_get("/error")
        assert result is None


class TestWebSocket:
    def test_is_ws_connected_false_by_default(self):
        t = Transport("http://localhost:8000")
        assert t.is_ws_connected is False

    def test_ws_url_http(self):
        t = Transport("http://localhost:8000", agent_token="tok123")
        url = t.ws_url
        assert url.startswith("ws://")
        assert "/agents/ws?token=" in url
        assert "tok123" in url

    def test_ws_url_https(self):
        t = Transport("https://manager.example.com", agent_token="tok456")
        url = t.ws_url
        assert url.startswith("wss://")
        assert "manager.example.com" in url
        assert "tok456" in url

    def test_ws_requires_token(self, transport):
        transport._agent_token = ""
        import pytest as pt
        from agent.transport import TransportError
        import asyncio
        with pt.raises(TransportError, match="no agent token"):
            asyncio.run(transport.connect_ws())

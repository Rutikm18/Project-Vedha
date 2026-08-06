from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

from agent.agent import _load_or_create_identity, _obtain_identity
from agent.engine import CAPABILITIES
from agent.transport import Transport, TransportError


def _cached_transport():
    transport = MagicMock()
    transport.is_authenticated.return_value = True
    transport.agent_id = "cached-agent"
    transport.agent_token = "cached-token"
    return transport


def test_generated_scope_identity_preserves_agent_credentials(tmp_path):
    state_file = tmp_path / "private" / "state.json"
    transport = Transport("http://localhost:8000", state_file=state_file)
    transport.update_state({
        "agent_id": "agent-1",
        "token": "token-1",
    })

    identity_sk, identity_pk, public_key_b64 = _load_or_create_identity(transport)

    saved = json.loads(state_file.read_text())
    assert len(identity_sk) == 32
    assert len(identity_pk) == 32
    assert public_key_b64
    assert saved["agent_id"] == "agent-1"
    assert saved["token"] == "token-1"
    assert saved["identity_sk"]


@patch(
    "agent.agent._load_or_create_identity",
    return_value=(b"private", b"public", "public-b64"),
)
def test_cached_identity_refreshes_current_capabilities(load_identity):
    transport = _cached_transport()
    transport.refresh_registration.return_value = True

    result = _obtain_identity(
        transport,
        email="",
        password="",
        operator_token="",
        probe_name="probe-1",
        location="dc-1",
        segments=["10.0.0.0/24"],
    )

    assert result[:3] == ("cached-agent", "cached-token", False)
    transport.refresh_registration.assert_called_once_with(
        capabilities=CAPABILITIES,
        network_segments=["10.0.0.0/24"],
        public_key="public-b64",
    )


@patch(
    "agent.agent._load_or_create_identity",
    return_value=(b"private", b"public", "public-b64"),
)
@patch("agent.agent.time.sleep")
def test_cached_identity_retries_transient_refresh_failure(sleep, load_identity):
    transport = _cached_transport()
    transport.refresh_registration.side_effect = [False, True]

    result = _obtain_identity(
        transport,
        email="",
        password="",
        operator_token="",
        probe_name="probe-1",
        location="",
        segments=[],
    )

    assert result[0] == "cached-agent"
    assert transport.refresh_registration.call_count == 2
    sleep.assert_called_once_with(10)


@patch(
    "agent.agent._load_or_create_identity",
    return_value=(b"private", b"public", "public-b64"),
)
def test_rejected_cached_token_falls_back_to_idempotent_registration(load_identity):
    transport = _cached_transport()
    transport.refresh_registration.side_effect = TransportError("expired")
    transport.register.return_value = {
        "agent_id": "refreshed-agent",
        "token": "refreshed-token",
    }

    result = _obtain_identity(
        transport,
        email="",
        password="",
        operator_token="operator-token",
        probe_name="probe-1",
        location="dc-1",
        segments=[],
    )

    transport.clear_state.assert_called_once()
    transport.register.assert_called_once()
    assert transport.register.call_args.kwargs["capabilities"] == CAPABILITIES
    assert result[:3] == ("refreshed-agent", "refreshed-token", True)

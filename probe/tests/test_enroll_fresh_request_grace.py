"""A just-created enrollment request may 404 for a moment — don't burn the token.

Found in the agent-install E2E run: the manager committed the enrollment row
AFTER answering (FastAPI runs the session teardown post-response), the
auto-approved agent polled at once, hit the other API worker, got 404, treated its
own request as "gone", re-enrolled, collided with its own key, wiped its identity
and came back with the single-use install token already spent — so it fell back
to manual pairing. The manager now commits first; the agent also gives a request
it created a short grace window before declaring it gone.
"""
from __future__ import annotations

from unittest.mock import MagicMock, patch

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from agent.agent import _enroll_device
from agent.transport import EnrollmentRequestNotFound


def _key() -> bytes:
    return Ed25519PrivateKey.generate().private_bytes_raw()


def _transport(state: dict, poll_effects: list):
    transport = MagicMock()
    transport._base_url = "http://manager.test"
    transport.load_state.return_value = state
    transport.create_enrollment_request.return_value = {
        "request_id": "req-1", "device_secret": "s" * 40, "poll_interval_seconds": 5,
        "state": "approved", "activation_challenge": "challenge", "agent_id": "agent-1",
    }
    transport.poll_enrollment.side_effect = poll_effects
    transport.activate_enrollment.return_value = {"agent_id": "agent-1", "access_token": "t"}
    return transport


def _enroll(transport):
    with patch("agent.agent.time.sleep"):
        return _enroll_device(
            transport, signing_private_key=_key(), signing_public_key="pk",
            encryption_public_key="ek", probe_name="branch-vm",
        )


def test_fresh_request_404_is_retried_not_recreated(monkeypatch):
    monkeypatch.setenv("PROBE_ENROLL_TOKEN", "vet_single_use_token")
    approved = {"state": "approved", "activation_challenge": "challenge", "agent_id": "agent-1"}
    transport = _transport({}, [EnrollmentRequestNotFound("not yet"), EnrollmentRequestNotFound("not yet"), approved])

    assert _enroll(transport)["agent_id"] == "agent-1"
    # one enrollment request, so the single-use token is presented exactly once
    assert transport.create_enrollment_request.call_count == 1
    assert transport.activate_enrollment.call_count == 1


def test_resumed_stale_request_404_still_recreates(monkeypatch):
    monkeypatch.delenv("PROBE_ENROLL_TOKEN", raising=False)
    approved = {"state": "approved", "activation_challenge": "challenge", "agent_id": "agent-1"}
    stored = {"enrollment_request_id": "old-req", "enrollment_device_secret": "x" * 40}
    # first poll is for the stored (stale) request → 404 → create a fresh one
    transport = _transport(stored, [EnrollmentRequestNotFound("gone"), approved])
    transport.load_state.side_effect = [stored, {}]

    assert _enroll(transport)["agent_id"] == "agent-1"
    assert transport.create_enrollment_request.call_count == 1

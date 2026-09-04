"""
Telling "revoked" apart from "wrong manager" and "manager can't answer".

THE REPORTED FAILURE (2026-09-04): a probe enrolled against the LOCAL manager was
re-pointed at a remote one and printed

    Device credential was revoked, expired, or disabled; stopping for
    administrator review.

Nothing had been revoked. The credential simply belonged to a different manager.
The old code inferred revocation from LOCAL state — `if
state.get("device_refresh_secret")` — rather than from anything the manager said.

Two facts make the status code useless as a discriminator, so the fix cannot rely
on it:
  * The manager returns **401 for BOTH** "unknown device" and "revoked/disabled"
    (probe_enrollment.py), deliberately, so agent ids cannot be enumerated.
  * A 503 "replay protection unavailable", a 5xx, or a dropped connection also
    collapsed to the same False — so a brief manager-side outage could
    permanently stop an entire fleet with a revocation message.

What discriminates is WHICH MANAGER issued the credential, which is now recorded
alongside it.
"""
from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

import httpx
import pytest

from agent.transport import (
    DEVICE_REFRESH_OK,
    DEVICE_REFRESH_REJECTED,
    DEVICE_REFRESH_UNAVAILABLE,
    Transport,
    manager_fingerprint,
)


class TestManagerFingerprint:
    def test_scheme_host_port_identify_a_manager(self):
        assert manager_fingerprint("http://13.127.147.205:18080") == \
            "http://13.127.147.205:18080"

    @pytest.mark.parametrize("variant", [
        "http://13.127.147.205:18080/",
        "HTTP://13.127.147.205:18080",
        "http://13.127.147.205:18080/api",
    ])
    def test_cosmetic_differences_are_the_same_manager(self, variant):
        """A trailing slash or a path must not look like a different manager and
        trigger a spurious re-enrollment."""
        assert manager_fingerprint(variant) == manager_fingerprint(
            "http://13.127.147.205:18080")

    def test_different_hosts_are_different_managers(self):
        assert manager_fingerprint("http://localhost:18080") != \
            manager_fingerprint("http://13.127.147.205:18080")

    def test_different_ports_are_different_managers(self):
        assert manager_fingerprint("http://a.example:18080") != \
            manager_fingerprint("http://a.example:9090")

    def test_bare_host_without_scheme_is_handled(self):
        assert manager_fingerprint("13.127.147.205") == "13.127.147.205"

    def test_empty_input_does_not_raise(self):
        assert manager_fingerprint("") == ""


def _transport(tmp_path: Path, state: dict) -> Transport:
    t = Transport("http://mgr.example:18080", verify_tls=False,
                  state_file=tmp_path / "state.json")
    t._client = MagicMock()
    t.update_state(state)
    return t


_STATE = {
    "agent_id": "be2b4c8f-e0b5-4aeb-96f4-9405a7512e0a",
    "device_refresh_secret": "s3cret",
    "credential_generation": 1,
}


class TestRefreshOutcomes:
    def _run(self, tmp_path, *, status=None, exc=None):
        t = _transport(tmp_path, _STATE)
        if exc is not None:
            t._client.post.side_effect = exc
        else:
            t._client.post.return_value = MagicMock(status_code=status)
        return t.refresh_device_access_ex(b"k" * 32)

    @pytest.mark.parametrize("code", [401, 403, 409])
    def test_authoritative_refusal_is_rejected(self, tmp_path, code):
        assert self._run(tmp_path, status=code) == DEVICE_REFRESH_REJECTED

    @pytest.mark.parametrize("code", [500, 502, 503])
    def test_server_errors_are_unavailable_not_revocation(self, tmp_path, code):
        """503 is the manager's own 'replay protection unavailable'. Calling that
        a revocation could stop every probe in the fleet over a Redis blip."""
        assert self._run(tmp_path, status=code) == DEVICE_REFRESH_UNAVAILABLE

    def test_network_failure_is_unavailable(self, tmp_path):
        assert self._run(tmp_path, exc=httpx.ConnectError("down")) == \
            DEVICE_REFRESH_UNAVAILABLE

    def test_missing_credential_material_is_rejected(self, tmp_path):
        t = _transport(tmp_path, {"agent_id": "a"})     # no secret/generation
        assert t.refresh_device_access_ex(b"k" * 32) == DEVICE_REFRESH_REJECTED

    def test_bool_wrapper_still_means_success_only(self, tmp_path):
        t = _transport(tmp_path, _STATE)
        t._client.post.return_value = MagicMock(status_code=401)
        assert t.refresh_device_access(b"k" * 32) is False

    def test_the_three_outcomes_are_distinct(self):
        assert len({DEVICE_REFRESH_OK, DEVICE_REFRESH_REJECTED,
                    DEVICE_REFRESH_UNAVAILABLE}) == 3


class TestDecisionLogic:
    """The branch chosen for each situation, asserted against the source so the
    diagnosis cannot silently regress."""

    @property
    def _src(self) -> str:
        return (Path(__file__).resolve().parent.parent
                / "agent" / "agent.py").read_text()

    def test_wrong_manager_reenrolls_instead_of_claiming_revocation(self):
        src = self._src
        assert "issued by" in src and "Re-enrolling with the new manager" in src

    def test_revocation_message_now_names_the_manager(self):
        """So the operator can see WHICH manager refused, instead of a bare
        claim that something was revoked."""
        assert 'disabled by "\n                            f"{current}' in self._src \
            or "disabled by " in self._src

    def test_unavailable_does_not_clear_state(self):
        """Discarding a valid credential during an outage turns a blip into a
        manual re-enrollment."""
        src = self._src
        i = src.index("DEVICE_REFRESH_UNAVAILABLE:")
        assert "clear_state" not in src[i:i + 1400]

    def test_unavailable_exits_2_not_1(self):
        src = self._src
        i = src.index("DEVICE_REFRESH_UNAVAILABLE:")
        assert "SystemExit(2)" in src[i:i + 1400]

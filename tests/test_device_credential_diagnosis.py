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


class TestLegacyStateWithoutIssuer:
    """Credentials enrolled BEFORE the issuer was recorded (i.e. every existing
    install). We cannot prove which manager owns them, so we must not assert
    revocation — but we must not silently continue either."""

    @property
    def _src(self) -> str:
        return (Path(__file__).resolve().parent.parent
                / "agent" / "agent.py").read_text()

    def test_legacy_path_does_not_assert_revocation(self):
        """Scoped to the legacy branch itself, which ends at its own
        SystemExit — the same-manager branch that follows SHOULD still say
        'revoked', and must not be caught by this assertion."""
        src = self._src
        start = src.index("does not record which manager")
        end = src.index("raise SystemExit(1)", start)
        branch = src[start:end]
        assert "was revoked, expired, or disabled by" not in branch
        assert "see an administrator" in branch      # hedged, not asserted

    def test_legacy_path_tells_the_operator_what_to_do(self):
        src = self._src
        assert "STATE_FILE=~/vedha-agent/state-<manager>.json" in src

    def test_legacy_path_keeps_the_credential(self):
        """Pointing the probe back at its real manager must still work."""
        src = self._src
        start = src.index("does not record which manager")
        end = src.index("raise SystemExit(1)", start)
        assert "clear_state" not in src[start:end]


def test_successful_refresh_backfills_the_issuer(tmp_path):
    """Existing installs self-heal: one legitimate refresh records the issuer,
    so the NEXT re-point is diagnosed correctly rather than as a revocation."""
    t = _transport(tmp_path, _STATE)
    t._client.post.return_value = MagicMock(
        status_code=200,
        json=lambda: {"access_token": "tok", "access_expires_in_seconds": 600},
    )
    assert t.refresh_device_access_ex(b"k" * 32) == DEVICE_REFRESH_OK
    assert t.load_state()["manager_fingerprint"] == "http://mgr.example:18080"


class TestIssuerIsWrittenOnEveryIdentityPath:
    """Regression: the binding was originally written ONLY on device refresh.

    A probe that re-registered against a new manager kept the OLD issuer, so its
    state claimed AWS-issued credentials came from localhost. That is worse than
    no binding: pointed back at localhost it would MATCH and report a revocation
    that never happened. Observed for real on 2026-09-04.
    """

    def test_save_state_records_the_issuer(self, tmp_path):
        t = Transport("http://aws.example:18080", verify_tls=False,
                      state_file=tmp_path / "state.json")
        t._client = MagicMock()
        t._agent_id, t._agent_token = "new-id", "new-token"
        t.save_state()
        assert t.load_state()["manager_fingerprint"] == "http://aws.example:18080"

    def test_re_registering_overwrites_a_stale_issuer(self, tmp_path):
        """The exact observed failure: identity moves managers, binding must follow."""
        t = Transport("http://aws.example:18080", verify_tls=False,
                      state_file=tmp_path / "state.json")
        t._client = MagicMock()
        t.update_state({"manager_fingerprint": "http://127.0.0.1:18080",
                        "agent_id": "old-id"})
        t._agent_id, t._agent_token = "new-id", "new-token"
        t.save_state()
        st = t.load_state()
        assert st["manager_fingerprint"] == "http://aws.example:18080"
        assert st["agent_id"] == "new-id"

    def test_clear_state_drops_the_issuer_too(self, tmp_path):
        """A stale binding left behind would misdiagnose the NEXT manager."""
        t = Transport("http://aws.example:18080", verify_tls=False,
                      state_file=tmp_path / "state.json")
        t._client = MagicMock()
        t._agent_id, t._agent_token = "id", "tok"
        t.save_state()
        t.clear_state()
        st = t.load_state()
        assert "manager_fingerprint" not in st
        assert "agent_id" not in st and "token" not in st

    def test_device_secrets_survive_clear_state(self, tmp_path):
        """clear_state drops the AGENT identity; the device keypair/secret is a
        separate, longer-lived thing and must not be collateral damage."""
        t = Transport("http://aws.example:18080", verify_tls=False,
                      state_file=tmp_path / "state.json")
        t._client = MagicMock()
        t.update_state({"device_refresh_secret": "s", "identity_sk": "k"})
        t._agent_id, t._agent_token = "id", "tok"
        t.save_state()
        t.clear_state()
        st = t.load_state()
        assert st["device_refresh_secret"] == "s" and st["identity_sk"] == "k"

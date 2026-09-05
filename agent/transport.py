"""
transport.py — all manager communication (HTTP + WebSocket) in one place.

Encapsulates the full connection lifecycle:
  - Registration       → POST /agents/register (get agent_id + JWT token)
  - Heartbeat          → POST /agents/heartbeat
  - Job polling        → GET  /agents/{id}/jobs  (HTTP fallback)
  - Scope fetch        → GET  /engagements/{id}/scope
  - Result submission  → POST /agents/{id}/jobs/{job_id}/result
  - WebSocket push     → wss:// (Phase 2 — foundation here)

Auto-reconnect with jittered exponential backoff.
Supports VERIFY_TLS=false for development environments.
"""
from __future__ import annotations

import gzip
import json
import logging
import os
import tempfile
import time
from pathlib import Path
from typing import Any, Iterable

import httpx

LOG = logging.getLogger("transport")


def _strip_nul(obj: Any) -> Any:
    """Recursively remove NUL (U+0000) characters from every string in a payload.

    Scan banners (SSH/HTTP, e.g. dropbear's KEX bytes) can carry raw NUL bytes.
    PostgreSQL ``jsonb`` cannot store ``\\u0000`` — the manager's result insert
    then fails with HTTP 500 and the job hangs forever. NUL is never meaningful
    in a text fact, so we drop it here, right before the payload is serialized,
    so the wire form the manager checksums is the same clean form it persists.
    """
    if isinstance(obj, str):
        return obj.replace("\x00", "") if "\x00" in obj else obj
    if isinstance(obj, dict):
        return {_strip_nul(k): _strip_nul(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_strip_nul(v) for v in obj]
    return obj


class TransportError(Exception):
    """Raised when a transport operation fails permanently (not retryable)."""


class DeviceAlreadyEnrolledError(TransportError):
    """The probe's device signing key is already registered as an agent on the
    manager (create_enrollment_request → HTTP 409).

    Distinct from a transient/network failure: retrying the create call will
    never succeed. The probe must instead refresh its device access token, or an
    operator must remove the stale agent before a fresh enrollment can proceed.
    Kept as its own type so the caller reports an accurate cause rather than the
    generic 'manager unreachable' path."""


class EnrollmentRequestNotFound(TransportError):
    """A poll/activate targeted an enrollment request the manager does not have
    (HTTP 404). The request was spent, expired, purged, or the manager's
    enrollment store was reset since it was created.

    This is AUTHORITATIVE, not a network blip: the caller must DISCARD the stored
    request_id/device_secret and create a fresh enrollment request. Retrying the
    same dead id — the old behaviour, which misread the 404 as a transient
    'connection error' — loops until the retry budget is exhausted and then lies
    that the manager is unreachable."""


# Heartbeat outcomes. A revoked lease is deliberately its own value: it is a
# DEFINITIVE "stop working on this job" from the manager (operator cancel, or
# reassignment after a lease expiry), whereas a plain failure may be transient.
HEARTBEAT_OK = "ok"
HEARTBEAT_FAILED = "failed"
HEARTBEAT_LEASE_REVOKED = "lease_revoked"


# Device access-refresh outcomes.
#
# The old bool return collapsed three very different situations into False, and
# the caller then treated ALL of them as "your credential was revoked" and exited
# for administrator review. Two of them are not revocation at all:
#
#   * REJECTED  - the manager authoritatively refused (401/403/409). NOTE the
#     manager returns 401 for BOTH "unknown device" and "revoked/disabled", on
#     purpose, so an attacker cannot enumerate agent ids. The status code alone
#     therefore CANNOT tell those apart — which manager we are talking to can
#     (see `manager_fingerprint`).
#   * UNAVAILABLE - a network error, a 5xx, or the manager's 503 "replay
#     protection unavailable". Transient. Treating this as revocation meant a
#     brief Redis outage on the manager could permanently stop every probe in
#     the fleet until a human intervened.
DEVICE_REFRESH_OK = "ok"
DEVICE_REFRESH_REJECTED = "rejected"
DEVICE_REFRESH_UNAVAILABLE = "unavailable"


def manager_fingerprint(platform_url: str) -> str:
    """Stable identity for the manager a credential belongs to.

    Device credentials are issued BY a manager and are meaningless to any other
    one. The probe stores this alongside them so that pointing it at a different
    manager is recognised as "these credentials are not for you" rather than
    misdiagnosed as "you have been revoked".

    Scheme+host+port only: a path or trailing slash does not change which
    manager you are talking to, and neither should this value.
    """
    from urllib.parse import urlsplit
    parts = urlsplit((platform_url or "").strip().rstrip("/"))
    if not parts.netloc:                       # bare host[:port] with no scheme
        return (platform_url or "").strip().rstrip("/").lower()
    return f"{parts.scheme}://{parts.netloc}".lower()


def _enrollment_conflict_detail(response: "httpx.Response") -> str:
    """Best-effort extraction of the manager's 409 ``detail`` message."""
    try:
        detail = response.json().get("detail")
    except (ValueError, AttributeError, TypeError):
        detail = None
    return str(detail) if detail else "This device key is already enrolled"


def _sync_directory(directory: Path) -> None:
    if os.name != "posix" or not directory.exists():
        return
    directory_fd = os.open(directory, os.O_RDONLY)
    try:
        os.fsync(directory_fd)
    finally:
        os.close(directory_fd)


def _atomic_write_private_state(path: Path, state: dict[str, Any]) -> None:
    """Durably replace one private JSON state file without exposing secrets."""
    payload = json.dumps(state)
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    if os.name == "posix":
        # Best-effort hardening: tighten the state directory to 0700. This can
        # legitimately fail when the dir is a PRE-EXISTING one we do not own
        # (a shared /tmp, a system path like /var/lib without root). That is NOT
        # fatal — every state file is written 0600 below regardless — so a
        # directory we cannot re-permission must degrade, never crash the probe.
        try:
            os.chmod(path.parent, 0o700)
        except OSError:
            pass

    fd, tmp_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=path.parent,
    )
    tmp_path = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            if os.name == "posix":
                os.fchmod(handle.fileno(), 0o600)
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_path, path)
        if os.name == "posix":
            os.chmod(path, 0o600)
        _sync_directory(path.parent)
    except BaseException:
        try:
            tmp_path.unlink(missing_ok=True)
        except OSError:
            pass
        raise


class Transport:
    """HTTP (+ future WebSocket) transport to the manager.

    Thread-safe for sequential use (the probe is single-threaded). Every
    callable method accepts an optional timeout override for fine-grained
    control.
    """

    def __init__(
        self,
        platform_url: str,
        *,
        verify_tls: bool = True,
        timeout: float = 30.0,
        agent_id: str = "",
        agent_token: str = "",
        state_file: str | Path | None = None,
        ca_bundle: str | None = None,
        client_cert: str | None = None,
        client_key: str | None = None,
        compress_over: int = 1 << 20,
    ):
        self._base_url = platform_url.rstrip("/")
        self._agent_id = agent_id
        self._agent_token = agent_token
        self._state_file = Path(state_file) if state_file else None
        if (
            self._state_file
            and not (self._agent_id and self._agent_token)
            and self._state_file.exists()
        ):
            try:
                cached = self.load_state()
                if cached.get("agent_id") and cached.get("token"):
                    self._agent_id = str(cached["agent_id"])
                    self._agent_token = str(cached["token"])
            except (OSError, ValueError, TypeError):
                pass
        # Payloads at/above this size are gzip-compressed before upload (a /24
        # sweep is MBs of JSON). 0 disables compression.
        self._compress_over = compress_over

        # TLS trust chain: a custom CA bundle (the manager's private PKI) takes
        # precedence over the bool; verify_tls=False disables verification (dev
        # only — the manager cert isn't checked, so only use on trusted links).
        verify: bool | str = ca_bundle if ca_bundle else verify_tls
        # mTLS: present a client certificate so the manager can authenticate the
        # probe at the TLS layer (cert+key files, or a single combined PEM).
        cert: str | tuple[str, str] | None = None
        if client_cert and client_key:
            cert = (client_cert, client_key)
        elif client_cert:
            cert = client_cert

        self._client = httpx.Client(
            base_url=platform_url.rstrip("/"),
            timeout=httpx.Timeout(connect=10.0, read=timeout, write=timeout, pool=30.0),
            verify=verify,
            cert=cert,
        )

        # WebSocket state (populated by Phase 2)
        self._ws = None  # Websocket connection object (when Phase 2 is wired)
        self._device_signing_private_key: bytes | None = None

    # ── Identity ──────────────────────────────────────────────────────────────

    @property
    def agent_id(self) -> str:
        return self._agent_id

    @agent_id.setter
    def agent_id(self, value: str) -> None:
        self._agent_id = value

    @property
    def agent_token(self) -> str:
        return self._agent_token

    @agent_token.setter
    def agent_token(self, value: str) -> None:
        self._agent_token = value

    @property
    def auth_header(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self._agent_token}"}

    def is_authenticated(self) -> bool:
        """True if we have both an agent_id and a token for API calls."""
        return bool(self._agent_id and self._agent_token)

    # ── State persistence (thin helper, not a full state manager) ─────────────

    def load_state(self) -> dict[str, Any]:
        if not self._state_file or not self._state_file.exists():
            return {}
        if os.name == "posix":
            os.chmod(self._state_file.parent, 0o700)
            os.chmod(self._state_file, 0o600)
        loaded = json.loads(self._state_file.read_text())
        return loaded if isinstance(loaded, dict) else {}

    def update_state(
        self,
        updates: dict[str, Any] | None = None,
        *,
        remove: Iterable[str] = (),
    ) -> None:
        """Merge and atomically persist private state while preserving fields."""
        if not self._state_file:
            return
        try:
            state = self.load_state()
        except (OSError, ValueError, TypeError):
            state = {}
        state.update(updates or {})
        for key in remove:
            state.pop(key, None)
        if state:
            _atomic_write_private_state(self._state_file, state)
            return
        self._state_file.unlink(missing_ok=True)
        _sync_directory(self._state_file.parent)

    def save_state(self) -> None:
        """Persist the agent identity AND the manager that issued it.

        The issuer belongs here, not only on the device-refresh path: an identity
        can also be established by registration or enrollment, and those go
        through this method. Recording it in one place only left state that
        claimed AWS-issued credentials came from localhost — worse than no
        binding at all, because the mismatch check would then wrongly MATCH when
        the probe was pointed back at the original manager and report a
        revocation that never happened.
        """
        self.update_state({
            "agent_id": self._agent_id,
            "token": self._agent_token,
            "manager_fingerprint": manager_fingerprint(self._base_url),
        })

    def clear_state(self) -> None:
        self._agent_id = ""
        self._agent_token = ""
        # The issuer describes the credential we are discarding, so it must go
        # with it — a stale binding would misdiagnose the NEXT manager.
        self.update_state(remove=("agent_id", "token", "manager_fingerprint"))

    def clear_manager_binding(self) -> None:
        """Forget everything a SPECIFIC manager issued, keeping the probe's own
        keypairs so it re-enrolls with the same device identity.

        Use this when re-pointing to a DIFFERENT manager. A device credential,
        site policy, and — critically — the pinned policy-signing key are all
        bound to the issuing manager and are meaningless to (and rejected by) a
        new one. Leaving the pinned ``policy_signing_public_key`` behind was a
        real bug: the new manager's policy then failed activation with
        "Site policy signing key changed outside an approved rotation", which the
        enrollment loop misread as a transient "connection error" and retried
        forever without ever enrolling.
        """
        self._agent_id = ""
        self._agent_token = ""
        self.update_state(remove=(
            "agent_id", "token",
            "device_refresh_secret", "credential_generation",
            "policy_signing_public_key", "site_policy", "site_id",
            "manager_fingerprint",
            "enrollment_request_id", "enrollment_device_secret",
        ))

    # ── Registration ──────────────────────────────────────────────────────────

    def register(
        self,
        name: str,
        *,
        location: str | None = None,
        capabilities: list[str] | None = None,
        network_segments: list[str] | None = None,
        public_key: str | None = None,
        operator_token: str,
    ) -> dict[str, Any]:
        """Register the probe with the manager.

        Args:
            name: Probe name (usually hostname).
            location: Optional physical/logical location hint.
            capabilities: Scan capability list (from engine.py CAPABILITIES).
            network_segments: CIDR segments this probe is deployed in.
            public_key: Base64-encoded X25519 public key (Phase 4).
            operator_token: JWT for the operator who will register this probe.

        Returns:
            {"agent_id": str, "token": str}

        Raises:
            TransportError: Registration was rejected (bad creds, etc.).
            httpx.HTTPError: Network-level failure.
        """
        body: dict[str, Any] = {"name": name}
        if location:
            body["location"] = location
        if capabilities:
            body["capabilities"] = capabilities
        if network_segments:
            body["network_segments"] = network_segments
        if public_key:
            body["public_key"] = public_key

        r = self._client.post(
            "/agents/register",
            headers={"Authorization": f"Bearer {operator_token}"},
            json=body,
        )

        if r.status_code in (401, 403):
            raise TransportError(
                f"Manager rejected registration (HTTP {r.status_code}): "
                f"check OPERATOR_TOKEN/PROBE_PAT or OPERATOR_EMAIL/OPERATOR_PASSWORD."
            )
        r.raise_for_status()
        data = r.json()
        self._agent_id = data["agent_id"]
        self._agent_token = data["token"]
        self.save_state()
        return data

    def bootstrap(
        self,
        name: str,
        *,
        bootstrap_key: str,
        location: str | None = None,
        capabilities: list[str] | None = None,
        network_segments: list[str] | None = None,
        public_key: str | None = None,
    ) -> dict[str, Any]:
        """Register using a manager-side shared bootstrap key (no user login needed).

        Falls back automatically when PROBE_PAT / OPERATOR_TOKEN are not set.
        The manager must have PROBE_BOOTSTRAP_KEY configured.
        """
        body: dict[str, Any] = {"name": name, "bootstrap_key": bootstrap_key}
        if location:
            body["location"] = location
        if capabilities:
            body["capabilities"] = capabilities
        if network_segments:
            body["network_segments"] = network_segments
        if public_key:
            body["public_key"] = public_key

        r = self._client.post("/agents/bootstrap", json=body)

        if r.status_code == 403:
            raise TransportError(
                "Bootstrap is disabled on this manager (PROBE_BOOTSTRAP_KEY not set). "
                "Set PROBE_BOOTSTRAP_KEY on the manager, or provide a PROBE_PAT."
            )
        if r.status_code == 401:
            raise TransportError("Bootstrap key rejected by manager. Check PROBE_BOOTSTRAP_KEY.")
        r.raise_for_status()
        data = r.json()
        self._agent_id = data["agent_id"]
        self._agent_token = data["token"]
        self.save_state()
        return data

    # ── Device-code enrollment ──────────────────────────────────────────────

    def create_enrollment_request(self, payload: dict[str, Any]) -> dict[str, Any]:
        response = self._client.post("/probe-enrollment/requests", json=payload)
        # A 409 here means the manager already has an agent bound to this device
        # signing key — a permanent condition, not a reachable-yet-flaky manager.
        # Surface it as its own type so the caller can attempt a device-token
        # refresh or give an actionable message instead of retrying blindly.
        if response.status_code == 409:
            raise DeviceAlreadyEnrolledError(_enrollment_conflict_detail(response))
        response.raise_for_status()
        return response.json()

    def poll_enrollment(self, request_id: str, device_secret: str) -> dict[str, Any]:
        response = self._client.post(
            f"/probe-enrollment/requests/{request_id}/poll",
            json={"device_secret": device_secret},
        )
        # 404 = this request is gone (spent/expired/purged, or the manager's
        # enrollment store was reset). Authoritative, NOT a network blip — the
        # caller must discard it and enroll afresh, not retry the dead id.
        if response.status_code == 404:
            raise EnrollmentRequestNotFound(
                f"enrollment request {request_id} not found on the manager (HTTP 404)"
            )
        response.raise_for_status()
        return response.json()

    def activate_enrollment(
        self,
        request_id: str,
        device_secret: str,
        signature: str,
    ) -> dict[str, Any]:
        response = self._client.post(
            f"/probe-enrollment/requests/{request_id}/activate",
            json={"device_secret": device_secret, "signature": signature},
        )
        # An approved request that vanishes before activation (e.g. the manager
        # was reset in the window between poll and activate) — same discard-and-
        # re-enroll recovery as poll, not a transient error.
        if response.status_code == 404:
            raise EnrollmentRequestNotFound(
                f"enrollment request {request_id} not found on activate (HTTP 404)"
            )
        response.raise_for_status()
        data = response.json()
        from agent.device_identity import verify_site_policy
        pinned_policy_key = self.load_state().get("policy_signing_public_key")
        policy_public_key = verify_site_policy(data["policy"], pinned_policy_key)
        self._agent_id = str(data["agent_id"])
        self._agent_token = str(data["access_token"])
        self.update_state({
            "agent_id": self._agent_id,
            "token": self._agent_token,
            "device_refresh_secret": data["refresh_secret"],
            "credential_generation": data["credential_generation"],
            "site_policy": data["policy"],
            "policy_signing_public_key": policy_public_key,
            # WHICH manager issued this credential. Without it the probe cannot
            # tell "revoked by this manager" from "unknown to a different one",
            # and defaults to the alarming reading.
            "manager_fingerprint": manager_fingerprint(self._base_url),
            "site_id": (data.get("policy") or {}).get("site_id"),
            "access_expires_at": time.time() + int(data.get("access_expires_in_seconds") or 600),
        }, remove=("enrollment_request_id", "enrollment_device_secret"))
        return data

    def refresh_device_access(self, signing_private_key: bytes) -> bool:
        """Backwards-compatible bool wrapper over `refresh_device_access_ex`."""
        return self.refresh_device_access_ex(signing_private_key) == DEVICE_REFRESH_OK

    def refresh_device_access_ex(self, signing_private_key: bytes) -> str:
        """Refresh the short-lived device access token, reporting WHY it failed.

        Returns DEVICE_REFRESH_OK / _REJECTED / _UNAVAILABLE. The caller needs
        the distinction: only an authoritative rejection FROM THE MANAGER THAT
        ISSUED THE CREDENTIAL justifies stopping for administrator review.
        """
        try:
            state = self.load_state()
            agent_id = str(state.get("agent_id") or self._agent_id)
            refresh_secret = state.get("device_refresh_secret")
            generation = int(state.get("credential_generation") or 0)
            if not agent_id or not refresh_secret or generation < 1:
                return DEVICE_REFRESH_REJECTED       # nothing to refresh with
            import secrets
            from agent.device_identity import sign_b64

            nonce = secrets.token_urlsafe(24)
            signature = sign_b64(
                signing_private_key,
                f"vedha-refresh:{agent_id}:{generation}:{nonce}",
            )
            response = self._client.post(
                "/probe-enrollment/token",
                json={
                    "agent_id": agent_id,
                    "generation": generation,
                    "refresh_secret": refresh_secret,
                    "nonce": nonce,
                    "signature": signature,
                },
            )
            if response.status_code in (401, 403, 409):
                return DEVICE_REFRESH_REJECTED       # authoritative "no"
            if response.status_code >= 500:
                # Includes the manager's 503 "replay protection unavailable".
                # Transient infrastructure trouble is NOT a revocation.
                return DEVICE_REFRESH_UNAVAILABLE
            response.raise_for_status()
            self._agent_id = agent_id
            self._agent_token = str(response.json()["access_token"])
            self.update_state({
                "agent_id": agent_id,
                "token": self._agent_token,
                # Backfill the issuer for credentials enrolled before this
                # binding existed: a SUCCESSFUL refresh proves this manager owns
                # them, so record it and legacy installs self-heal on first use.
                "manager_fingerprint": manager_fingerprint(self._base_url),
                "access_expires_at": time.time()
                + int(response.json().get("access_expires_in_seconds") or 600),
            })
            return DEVICE_REFRESH_OK
        except (OSError, ValueError, TypeError, httpx.HTTPError):
            # Network/parse failure — we never reached a verdict, so we must not
            # invent one. Transient until proven otherwise.
            return DEVICE_REFRESH_UNAVAILABLE

    def ensure_device_access(self, *, force: bool = False) -> bool:
        """Refresh a device token before expiry; legacy identities are unchanged.

        `force=True` bypasses the time-based check and re-mints the token
        unconditionally. Use it when the MANAGER rejected the token (401/403):
        the token can be valid by the local clock yet stale to the manager — a
        superseded credential generation, a revoked lease, or a manager that was
        redeployed. Without a forced path the probe reconnected forever with the
        same rejected token (the WebSocket 403 loop).
        """
        if self._device_signing_private_key is None:
            return True
        try:
            state = self.load_state()
            # Legacy PAT/bootstrap registrations also create a signing key so
            # they can migrate later. Without a refresh credential, their
            # existing token must remain on the legacy path.
            if not state.get("device_refresh_secret"):
                return True
            if force:
                return self.refresh_device_access(self._device_signing_private_key)
            # `access_expires_at` describes the token IN THE FILE, but requests
            # authenticate with the in-memory one. Another probe process sharing
            # this state.json (a lingering instance, a CLI run) may have rotated
            # the credential out from under us: the file then reads "fresh" while
            # we keep sending our own expired token, so the manager answers 403
            # "Token expired" on every reconnect — forever, because this check
            # never asks for a refresh. Adopt the stored credential first, so the
            # expiry we trust describes the token we actually send.
            stored_token = str(state.get("token") or "")
            if stored_token and stored_token != self._agent_token:
                self._agent_token = stored_token
                stored_agent_id = str(state.get("agent_id") or "")
                if stored_agent_id:
                    # id and token are written as one credential; never mix a
                    # rotated token with a stale id.
                    self._agent_id = stored_agent_id
            expires_at = float(state.get("access_expires_at") or 0)
            if self._agent_token and expires_at > time.time() + 60:
                return True
        except (OSError, ValueError, TypeError):
            pass
        return self.refresh_device_access(self._device_signing_private_key)

    def refresh_registration(
        self,
        *,
        capabilities: list[str],
        network_segments: list[str],
        public_key: str | None = None,
    ) -> bool | None:
        """Refresh routing metadata using the cached agent identity.

        Returns True when refreshed, False for a transient manager/network
        failure, and None when connected to an older manager without this API.
        """
        body: dict[str, Any] = {
            "capabilities": capabilities,
            "network_segments": network_segments,
        }
        if public_key:
            body["public_key"] = public_key

        try:
            r = self._client.post(
                f"/agents/{self._agent_id}/refresh",
                headers=self.auth_header,
                json=body,
            )
            if r.status_code == 404:
                return None
            if r.status_code in (401, 403, 410):
                raise TransportError(
                    "Cached agent identity was rejected during registration refresh."
                )
            r.raise_for_status()
            response_body = r.json()
            if isinstance(response_body, dict) and isinstance(response_body.get("policy"), dict):
                from agent.device_identity import verify_site_policy
                state = self.load_state()
                policy_public_key = verify_site_policy(
                    response_body["policy"], state.get("policy_signing_public_key"),
                )
                self.update_state({
                    "site_policy": response_body["policy"],
                    "policy_signing_public_key": policy_public_key,
                })
            return True
        except TransportError:
            raise
        except httpx.HTTPError:
            return False

    # ── Heartbeat ─────────────────────────────────────────────────────────────

    def heartbeat_ex(
        self,
        status: str = "online",
        current_job_id: str | None = None,
        attempt_id: str | None = None,
        fence: int | None = None,
    ) -> str:
        """Send a heartbeat and report WHY it failed, not just that it did.

        Returns one of:
          * HEARTBEAT_OK            — accepted (2xx).
          * HEARTBEAT_LEASE_REVOKED — 409. The manager no longer considers this
            attempt current: the operator cancelled the job, or it was reassigned
            after a lease expiry. Either way this probe must STOP working on it.
            This is a definitive answer, so the caller should abort immediately
            rather than spend a retry budget on it.
          * HEARTBEAT_FAILED        — anything else (auth, validation, network).
            Possibly transient, so the caller retries a bounded number of times.

        The old bool return collapsed all of these together, which meant a
        cancelled job was indistinguishable from a flaky network and kept running
        until the failure budget ran out.
        """
        try:
            if not self.ensure_device_access():
                return HEARTBEAT_FAILED
            r = self._client.post(
                "/agents/heartbeat",
                headers=self.auth_header,
                json={
                    "agent_id": self._agent_id,
                    "status": status,
                    "current_job_id": current_job_id,
                    "attempt_id": attempt_id,
                    "fence": fence,
                },
            )
            if r.status_code == 409:
                return HEARTBEAT_LEASE_REVOKED
            if r.status_code in (401, 403, 422):
                return HEARTBEAT_FAILED
            r.raise_for_status()
            return HEARTBEAT_OK
        except httpx.HTTPError:
            return HEARTBEAT_FAILED

    def heartbeat(
        self,
        status: str = "online",
        current_job_id: str | None = None,
        attempt_id: str | None = None,
        fence: int | None = None,
    ) -> bool:
        """Backwards-compatible bool form of `heartbeat_ex`.

        Returns True only when the heartbeat was accepted; every rejection —
        including a revoked lease — is False, matching the historical contract.
        """
        return self.heartbeat_ex(
            status, current_job_id, attempt_id, fence
        ) == HEARTBEAT_OK

    # ── Job polling (HTTP fallback) ────────────────────────────────────────────

    def poll_jobs(self, limit: int = 1) -> list[dict[str, Any]]:
        """Poll for pending jobs (HTTP fallback for WebSocket).

        Returns a list of job dicts (may be empty). Each job has:
            job_id, engagement_id, job_type, status, params
        """
        if not self.ensure_device_access():
            raise TransportError("Device credential refresh rejected during job poll.")
        r = self._client.get(
            f"/agents/{self._agent_id}/jobs",
            headers=self.auth_header,
            params={"limit": limit},
        )
        if r.status_code in (401, 403):
            # The token was time-valid (ensure_device_access above was happy) but
            # the manager REJECTED it — a stale credential generation, revoked
            # lease, or a redeployed manager. Force a fresh token and retry ONCE
            # before declaring re-registration, so a routine credential rotation
            # doesn't surface as a hard failure.
            if self.ensure_device_access(force=True):
                r = self._client.get(
                    f"/agents/{self._agent_id}/jobs",
                    headers=self.auth_header,
                    params={"limit": limit},
                )
            if r.status_code in (401, 403):
                raise TransportError("Token rejected during job poll — re-register needed.")
        r.raise_for_status()
        return r.json()

    # ── Scope fetch ────────────────────────────────────────────────────────────

    def fetch_scope(self, engagement_id: str) -> dict[str, Any] | None:
        """Fetch the engagement's authoritative scope.

        Returns the response dict if successful, None on any error (caller
        falls back to job-params scope).
        """
        try:
            r = self._client.get(
                f"/engagements/{engagement_id}/scope",
                headers=self.auth_header,
            )
            if r.status_code == 200:
                return r.json()
        except httpx.HTTPError:
            pass
        return None

    # ── Result submission ──────────────────────────────────────────────────────

    def submit_result(self, job_id: str, payload: dict[str, Any]) -> bool | str:
        """Submit a scan result to the manager.

        Returns True ONLY on a 2xx response (the manager durably accepted the
        result and the caller may drop its spooled copy). Every other outcome —
        4xx (auth/validation/too-large), 5xx, or a network error — returns False
        so the result stays spooled and is retried.

        This previously treated any status < 500 as success, which silently
        discarded results on 401 (expired token), 413 (too large), and 422
        (validation) — losing scan data the operator believed was delivered.

        Large payloads are gzip-compressed; the manager inflates them
        transparently (GzipRequestMiddleware).
        """
        try:
            if not self.ensure_device_access():
                return False
            # jsonb-safe: drop NUL bytes that scan banners can carry, else the
            # manager's result insert 500s and the job hangs (see _strip_nul).
            body = json.dumps(_strip_nul(payload)).encode("utf-8")
        except (TypeError, ValueError) as exc:
            LOG.error("submit_result: unserializable payload for job %s: %s", job_id, exc)
            return False

        headers = {**self.auth_header, "Content-Type": "application/json"}
        if self._compress_over and len(body) >= self._compress_over:
            body = gzip.compress(body)
            headers["Content-Encoding"] = "gzip"

        try:
            logical_job_id = str(payload.get("job_id") or job_id.split("--", 1)[0])
            r = self._client.post(
                f"/agents/{self._agent_id}/jobs/{logical_job_id}/result",
                headers=headers,
                content=body,
            )
            if 200 <= r.status_code < 300:
                return True
            if r.status_code in (400, 404, 409, 422):
                from agent.result_spool import PERMANENT_REJECTION
                LOG.error(
                    "submit_result permanently rejected (HTTP %d) for job %s — "
                    "result will be quarantined",
                    r.status_code,
                    logical_job_id,
                )
                return PERMANENT_REJECTION
            if r.status_code in (401, 403):
                LOG.warning(
                    "submit_result auth-rejected (HTTP %d) for job %s — result kept "
                    "for retry after re-register", r.status_code, job_id)
            elif r.status_code == 413:
                LOG.error(
                    "submit_result payload too large (HTTP 413) for job %s — result "
                    "kept spooled (raise the manager body limit)", job_id)
            else:
                LOG.warning("submit_result HTTP %d for job %s — result kept for retry",
                            r.status_code, job_id)
        except httpx.HTTPError as exc:
            LOG.warning("submit_result failed for job %s: %s", job_id, exc)
        return False

    # ── Low-level HTTP GET for callbacks ───────────────────────────────────────

    def http_get(self, path: str) -> dict[str, Any] | None:
        """Generic authenticated GET, returns parsed JSON or None on failure.

        Used by scope_validator.fetch_engagement_scope() via callback.
        """
        try:
            r = self._client.get(path, headers=self.auth_header)
            if r.status_code == 200:
                return r.json()
        except httpx.HTTPError:
            pass
        return None

    # ── WebSocket (Phase 2 — push protocol) ─────────────────────────────────

    @property
    def ws_url(self) -> str:
        """Return the WebSocket endpoint without embedding credentials.

        Authentication is sent in the Authorization header. Keeping credentials
        out of the URL prevents access logs and proxy traces from capturing them.
        """
        ws_scheme = "wss" if self._base_url.startswith("https") else "ws"
        host = self._base_url.split("://", 1)[1] if "://" in self._base_url else self._base_url
        return f"{ws_scheme}://{host}/agents/ws"

    async def connect_ws(self):
        """Establish an authenticated WebSocket connection to the manager.

        Returns a `websockets` connection object suitable for use in an
        async for loop. The caller is responsible for closing it.

        Raises TransportError if the token is missing.
        """
        import websockets

        if not self.ensure_device_access():
            raise TransportError("Cannot connect WebSocket: device credential refresh failed")
        if not self._agent_token:
            raise TransportError("Cannot connect WebSocket: no agent token")

        header_arg = (
            {"extra_headers": self.auth_header}
            if int(websockets.__version__.split(".", 1)[0]) < 14
            else {"additional_headers": self.auth_header}
        )
        ws = await websockets.connect(
            self.ws_url,
            open_timeout=15.0,
            close_timeout=5.0,
            ping_interval=30,      # built-in keep-alive
            ping_timeout=10,
            **header_arg,
        )
        self._ws = ws
        return ws

    @property
    def is_ws_connected(self) -> bool:
        """True if the WebSocket connection is active."""
        return (
            self._ws is not None
            and not getattr(self._ws, "closed", False)
        )

    # ── Cleanup ────────────────────────────────────────────────────────────────

    def close(self) -> None:
        try:
            self._client.close()
        except Exception:
            pass

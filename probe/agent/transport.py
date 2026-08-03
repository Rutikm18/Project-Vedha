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


class TransportError(Exception):
    """Raised when a transport operation fails permanently (not retryable)."""


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
        os.chmod(path.parent, 0o700)

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
        self.update_state({
            "agent_id": self._agent_id,
            "token": self._agent_token,
        })

    def clear_state(self) -> None:
        self._agent_id = ""
        self._agent_token = ""
        self.update_state(remove=("agent_id", "token"))

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
        response.raise_for_status()
        return response.json()

    def poll_enrollment(self, request_id: str, device_secret: str) -> dict[str, Any]:
        response = self._client.post(
            f"/probe-enrollment/requests/{request_id}/poll",
            json={"device_secret": device_secret},
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
            "access_expires_at": time.time() + int(data.get("access_expires_in_seconds") or 600),
        }, remove=("enrollment_request_id", "enrollment_device_secret"))
        return data

    def refresh_device_access(self, signing_private_key: bytes) -> bool:
        try:
            state = self.load_state()
            agent_id = str(state.get("agent_id") or self._agent_id)
            refresh_secret = state.get("device_refresh_secret")
            generation = int(state.get("credential_generation") or 0)
            if not agent_id or not refresh_secret or generation < 1:
                return False
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
                return False
            response.raise_for_status()
            self._agent_id = agent_id
            self._agent_token = str(response.json()["access_token"])
            self.update_state({
                "agent_id": agent_id,
                "token": self._agent_token,
                "access_expires_at": time.time()
                + int(response.json().get("access_expires_in_seconds") or 600),
            })
            return True
        except (OSError, ValueError, TypeError, httpx.HTTPError):
            return False

    def ensure_device_access(self) -> bool:
        """Refresh a device token before expiry; legacy identities are unchanged."""
        if self._device_signing_private_key is None:
            return True
        try:
            state = self.load_state()
            # Legacy PAT/bootstrap registrations also create a signing key so
            # they can migrate later. Without a refresh credential, their
            # existing token must remain on the legacy path.
            if not state.get("device_refresh_secret"):
                return True
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

    def heartbeat(
        self,
        status: str = "online",
        current_job_id: str | None = None,
        attempt_id: str | None = None,
        fence: int | None = None,
    ) -> bool:
        """Send a heartbeat to the manager.

        Returns True if the heartbeat was accepted (HTTP 2xx),
        False if rejected (401 — token expired).
        """
        try:
            if not self.ensure_device_access():
                return False
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
            if r.status_code in (401, 403, 409, 422):
                return False
            r.raise_for_status()
            return True
        except httpx.HTTPError:
            return False

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
        if r.status_code == 401:
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
            body = json.dumps(payload).encode("utf-8")
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

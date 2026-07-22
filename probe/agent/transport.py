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
import random
import socket
import time
from pathlib import Path
from typing import Any, Callable

import httpx

LOG = logging.getLogger("transport")


class TransportError(Exception):
    """Raised when a transport operation fails permanently (not retryable)."""


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

    def save_state(self) -> None:
        if self._state_file:
            self._state_file.parent.mkdir(parents=True, exist_ok=True)
            self._state_file.write_text(json.dumps({
                "agent_id": self._agent_id,
                "token": self._agent_token,
            }))

    def clear_state(self) -> None:
        self._agent_id = ""
        self._agent_token = ""
        if self._state_file and self._state_file.exists():
            self._state_file.unlink()

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

    # ── Heartbeat ─────────────────────────────────────────────────────────────

    def heartbeat(self, status: str = "online", current_job_id: str | None = None) -> bool:
        """Send a heartbeat to the manager.

        Returns True if the heartbeat was accepted (HTTP 2xx),
        False if rejected (401 — token expired).
        """
        try:
            r = self._client.post(
                "/agents/heartbeat",
                headers=self.auth_header,
                json={
                    "agent_id": self._agent_id,
                    "status": status,
                    "current_job_id": current_job_id,
                },
            )
            if r.status_code == 401:
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

    def submit_result(self, job_id: str, payload: dict[str, Any]) -> bool:
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
            body = json.dumps(payload).encode("utf-8")
        except (TypeError, ValueError) as exc:
            LOG.error("submit_result: unserializable payload for job %s: %s", job_id, exc)
            return False

        headers = {**self.auth_header, "Content-Type": "application/json"}
        if self._compress_over and len(body) >= self._compress_over:
            body = gzip.compress(body)
            headers["Content-Encoding"] = "gzip"

        try:
            r = self._client.post(
                f"/agents/{self._agent_id}/jobs/{job_id}/result",
                headers=headers,
                content=body,
            )
            if 200 <= r.status_code < 300:
                return True
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
        """Return the WebSocket connection URL with auth token.

        The token is passed as a query parameter so the manager can validate
        it before upgrading the connection. Replace http:// with ws://,
        https:// with wss://.
        """
        ws_scheme = "wss" if self._base_url.startswith("https") else "ws"
        host = self._base_url.split("://", 1)[1] if "://" in self._base_url else self._base_url
        return f"{ws_scheme}://{host}/agents/ws?token={self._agent_token}"

    async def connect_ws(self):
        """Establish an authenticated WebSocket connection to the manager.

        Returns a `websockets` connection object suitable for use in an
        async for loop. The caller is responsible for closing it.

        Raises TransportError if the token is missing.
        """
        import websockets

        if not self._agent_token:
            raise TransportError("Cannot connect WebSocket: no agent token")

        ws = await websockets.connect(
            self.ws_url,
            open_timeout=15.0,
            close_timeout=5.0,
            ping_interval=30,      # built-in keep-alive
            ping_timeout=10,
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

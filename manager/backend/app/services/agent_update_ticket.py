"""agent_update_ticket.py — a short-lived, single-use download ticket for an ENROLLED agent.

Why it exists: an agent that is already installed has no enrolment token left, and the
download routes (`/agent/package/windows`, `/agent/image/{arch}`) were authorised only by
one. So an agent could never fetch its own update. The manager now hands an agent a ticket
when — and only when — it has decided that agent should update.

What a ticket is: `vet_upd-<payload>-<signature>`.
  * Looks like an install token (`vet_…`, only letters, digits, `_` and `-`), so the existing
    Windows installer accepts it as `-Token` and sends it as the download bearer unchanged.
  * HMAC-SHA256 under a key derived from the manager secret (domain-separated), so nothing
    needs storing and no migration is needed.
  * Carries the agent, its tenant, the version it was offered, an expiry (15 minutes) and a
    random id. The download route spends the id in Redis, so a ticket works exactly once.
  * Grants only what an enrolment token grants for downloads: the package. It cannot enrol
    an agent, and the download route re-checks that the release is still newer than the
    version the agent runs.
"""
from __future__ import annotations

import base64
import hashlib
import hmac
import json
import secrets
import time
from dataclasses import dataclass

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

from app.config import get_settings

PREFIX = "vet_upd-"
TTL_SECONDS = 15 * 60
MAX_TICKET_CHARS = 600
_INFO = b"vedha:agent-update-ticket:v1"


@dataclass(frozen=True)
class UpdateTicket:
    agent_id: str
    tenant_id: str
    version: str          # the agent version the manager offered
    expires_at: int       # unix seconds
    jti: str


def _key() -> bytes:
    secret = (get_settings().jwt_secret or "").encode()
    if not secret:
        raise RuntimeError("jwt_secret is not configured")
    return HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=_INFO).derive(secret)


def _b64(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).decode().rstrip("=")


def _unb64(text: str) -> bytes:
    return base64.urlsafe_b64decode(text + "=" * (-len(text) % 4))


def is_ticket(raw: str) -> bool:
    return isinstance(raw, str) and raw.startswith(PREFIX)


def issue(agent_id: str, tenant_id: str, version: str, *, now: float | None = None,
          ttl: int = TTL_SECONDS) -> str:
    payload = json.dumps(
        {"a": str(agent_id), "t": str(tenant_id), "v": str(version),
         "e": int((now if now is not None else time.time()) + ttl), "j": secrets.token_hex(12)},
        separators=(",", ":"), sort_keys=True,
    ).encode()
    body = _b64(payload)
    signature = hmac.new(_key(), body.encode(), hashlib.sha256).hexdigest()
    return f"{PREFIX}{body}-{signature}"


def verify(raw: str, *, now: float | None = None) -> UpdateTicket | None:
    """The ticket's claims, or None when it is malformed, forged or expired. Never raises."""
    try:
        if not is_ticket(raw) or len(raw) > MAX_TICKET_CHARS:
            return None
        body, _, signature = raw[len(PREFIX):].rpartition("-")
        if not body or len(signature) != 64:
            return None
        expected = hmac.new(_key(), body.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(expected, signature):
            return None
        claims = json.loads(_unb64(body))
        ticket = UpdateTicket(
            agent_id=str(claims["a"]), tenant_id=str(claims["t"]), version=str(claims["v"]),
            expires_at=int(claims["e"]), jti=str(claims["j"]),
        )
    except Exception:  # noqa: BLE001 — a bad ticket is simply not valid
        return None
    if (now if now is not None else time.time()) >= ticket.expires_at:
        return None
    return ticket


def spend_key(ticket: UpdateTicket) -> str:
    return f"agent-update-ticket:{ticket.jti}"

"""agent_access.py — one definition of "this agent's access has expired".

Expiry is set from Fleet (agents.access_expires_at) and enforced ONLY here on the
manager, so a changed host clock or a patched binary can't bypass it. Shared by
the auth middleware (heartbeat, job poll, scope) and the public device-token
refresh endpoint, so every device path agrees.

Grace: a job running at the moment of expiry may still upload its finished hosts
(the result and chunk routes). Everything else — new heartbeats, new job polls,
minting a fresh access token — is refused, so no NEW work starts.
"""
from __future__ import annotations

import re
from datetime import datetime, timezone

# Device routes that an expired agent may still reach, so an in-flight scan's
# results aren't lost. Mirrors the result/chunk paths in auth/middleware.py.
_RESULT_UPLOAD_PATHS = (
    re.compile(r"^/agents/[^/]+/jobs/[^/]+/result$"),
    re.compile(r"^/agents/[^/]+/jobs/[^/]+/chunks$"),
)

EXPIRED_MESSAGE = "Agent access has expired. Ask your Vedha administrator to extend it in Fleet."
# WebSocket close reasons are limited to 123 bytes.
EXPIRED_REASON = "Agent access expired"


def is_expired(access_expires_at: datetime | None, now: datetime | None = None) -> bool:
    if access_expires_at is None:
        return False
    now = now or datetime.now(timezone.utc)
    if access_expires_at.tzinfo is None:
        access_expires_at = access_expires_at.replace(tzinfo=timezone.utc)
    return access_expires_at <= now


def path_allows_after_expiry(path: str) -> bool:
    """True for the in-flight result-upload routes that stay open after expiry."""
    return any(pattern.fullmatch(path) for pattern in _RESULT_UPLOAD_PATHS)

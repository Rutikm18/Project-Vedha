"""Centralized password hashing for the backend.

bcrypt is CPU-bound and deliberately slow (tens to hundreds of milliseconds per
call). Invoking it directly inside an async request handler blocks the event
loop for that whole duration, so every concurrent login/registration serializes
behind the one already in flight. The async wrappers below offload each bcrypt
call to a worker thread (``asyncio.to_thread``) so the loop stays free to serve
other requests while a hash is being computed.

A single shared ``CryptContext`` lives here, replacing the four identical
contexts that used to be constructed independently in ``auth/router.py``,
``routers/customer_access.py``, ``auth/startup.py`` and ``routers/health.py``.

Use the async wrappers (:func:`hash_password`, :func:`verify_password`,
:func:`dummy_verify`) inside request handlers. The ``*_sync`` variants exist for
non-request contexts (startup self-checks, CLI seeders) where blocking is fine.
"""
from __future__ import annotations

import asyncio

from passlib.context import CryptContext

# The one bcrypt context for the whole backend.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ── Async wrappers — use inside request handlers (never block the event loop) ────
async def hash_password(password: str) -> str:
    """Hash a plaintext password off the event loop."""
    return await asyncio.to_thread(pwd_context.hash, password)


async def verify_password(password: str, hashed: str) -> bool:
    """Verify a plaintext password against its hash off the event loop."""
    return await asyncio.to_thread(pwd_context.verify, password, hashed)


async def dummy_verify() -> None:
    """Constant-time no-op verify (anti-enumeration) off the event loop."""
    await asyncio.to_thread(pwd_context.dummy_verify)


# ── Sync primitives — for non-request contexts (startup + health self-checks) ────
def hash_password_sync(password: str) -> str:
    """Hash a plaintext password on the calling thread. Not for request paths."""
    return pwd_context.hash(password)


def verify_password_sync(password: str, hashed: str) -> bool:
    """Verify a password on the calling thread. Not for request paths."""
    return pwd_context.verify(password, hashed)

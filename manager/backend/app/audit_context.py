"""Who is calling, for the audit trail.

A tiny request-scoped context (contextvars) so every audit entry written during a
request carries the source address, user agent, request id and the authenticated
tenant/actor without each of the ~40 call sites passing them. Bound once per request by
AuditContextMiddleware; read by app.services.audit.record_audit. Outside a request (a
worker, a script) the context is empty and callers pass what they know explicitly.
"""
from __future__ import annotations

from contextvars import ContextVar
from typing import Any

_ctx: ContextVar[dict[str, Any]] = ContextVar("vedha_audit_ctx", default={})


def bind(**values: Any) -> None:
    _ctx.set({**_ctx.get(), **{k: v for k, v in values.items() if v is not None}})


def current() -> dict[str, Any]:
    return _ctx.get()


def clear() -> None:
    _ctx.set({})

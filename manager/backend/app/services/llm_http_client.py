"""Shared asynchronous HTTP transport for every Manager LLM provider.

Provider adapters own authentication and payload parsing; this module owns the
network client lifecycle, timeout policy, connection limits, and test transport.
Keeping that boundary small lets callers swap a deterministic MockTransport in
tests without exposing provider credentials or HTTP details to the browser.
"""

from __future__ import annotations

from dataclasses import dataclass

import httpx


@dataclass(slots=True)
class AsyncLlmHttpClient:
    """Create bounded ``httpx.AsyncClient`` instances for LLM requests.

    A fresh context-managed client keeps the current service contract intact.
    The connection limits protect the Manager from an unbounded burst while the
    injected transport provides a zero-network seam for provider contract tests.
    """

    timeout_seconds: float
    transport: httpx.AsyncBaseTransport | None = None
    max_connections: int = 20
    max_keepalive_connections: int = 10

    def open(self, *, timeout_seconds: float | None = None) -> httpx.AsyncClient:
        timeout = self.timeout_seconds if timeout_seconds is None else timeout_seconds
        return httpx.AsyncClient(
            timeout=httpx.Timeout(timeout),
            transport=self.transport,
            limits=httpx.Limits(
                max_connections=self.max_connections,
                max_keepalive_connections=self.max_keepalive_connections,
            ),
            follow_redirects=False,
        )

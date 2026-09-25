"""
Login rate-limit contract.

Before: the Next BFF called /auth/login server-to-server without forwarding the
browser's IP, so the backend keyed EVERY user onto the frontend container's IP —
one shared 5/min bucket for the whole deployment (one attacker = global lockout).
Meanwhile client_ip() trusted X-Forwarded-For from ANY peer, so a direct caller
could rotate fake IPs past the limit; and nothing capped failures per account,
so a distributed spray was never slowed on a single user.
"""
from __future__ import annotations

from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from app import ratelimit
from app.ratelimit import (
    check_login_failures,
    clear_login_failures,
    client_ip,
    record_login_failure,
)


def _req(peer: str | None, xff: str | None = None):
    headers = {"x-forwarded-for": xff} if xff is not None else {}
    return SimpleNamespace(
        client=SimpleNamespace(host=peer) if peer else None,
        headers=headers,
    )


# ── client_ip: whom to believe ────────────────────────────────────────────────

def test_direct_public_peer_cannot_spoof_via_xff():
    assert client_ip(_req("203.0.113.9", "1.2.3.4")) == "203.0.113.9"


def test_trusted_proxy_peer_yields_forwarded_client():
    """Caddy/BFF (private docker net) → honour the forwarded client."""
    assert client_ip(_req("172.18.0.5", "198.51.100.7")) == "198.51.100.7"


def test_rightmost_untrusted_hop_wins_over_client_supplied_prefix():
    """An attacker-prepended value sits LEFT of the real hop an honest proxy
    appended; take the rightmost untrusted address, not the first."""
    assert client_ip(_req("172.18.0.5", "1.2.3.4, 198.51.100.7")) == "198.51.100.7"


def test_all_private_chain_falls_back_to_original_client():
    """On-prem: operators on a LAN are private addresses too. Each distinct LAN
    user must still get their own bucket (not the proxy's)."""
    assert client_ip(_req("172.18.0.5", "192.168.1.50")) == "192.168.1.50"
    assert client_ip(_req("172.18.0.5", "192.168.1.51")) == "192.168.1.51"


def test_no_xff_uses_peer():
    assert client_ip(_req("172.18.0.5")) == "172.18.0.5"


def test_garbage_xff_entries_are_ignored():
    assert client_ip(_req("172.18.0.5", "not-an-ip, 198.51.100.7")) == "198.51.100.7"
    assert client_ip(_req("172.18.0.5", "garbage")) == "172.18.0.5"


def test_missing_peer_is_unknown_not_bypass():
    assert client_ip(_req(None, "1.2.3.4")) == "unknown"


# ── per-account failure limit ─────────────────────────────────────────────────

class FakeRedis:
    def __init__(self):
        self.kv: dict[str, int] = {}

    async def incr(self, k):
        self.kv[k] = self.kv.get(k, 0) + 1
        return self.kv[k]

    async def expire(self, k, s):
        return True

    async def get(self, k):
        v = self.kv.get(k)
        return None if v is None else str(v)

    async def ttl(self, k):
        return 600

    async def delete(self, *ks):
        for k in ks:
            self.kv.pop(k, None)


@pytest.mark.asyncio
async def test_account_locked_after_max_failures_regardless_of_ip():
    r = FakeRedis()
    for _ in range(ratelimit.LOGIN_FAILURES_PER_ACCOUNT):
        await check_login_failures(r, "Victim@Corp.com")
        await record_login_failure(r, "victim@corp.com")

    with pytest.raises(HTTPException) as exc:
        await check_login_failures(r, "VICTIM@corp.com ")  # normalised
    assert exc.value.status_code == 429
    assert "Retry-After" in exc.value.headers


@pytest.mark.asyncio
async def test_success_clears_account_failures():
    r = FakeRedis()
    for _ in range(ratelimit.LOGIN_FAILURES_PER_ACCOUNT - 1):
        await record_login_failure(r, "u@corp.com")
    await clear_login_failures(r, "u@corp.com")
    for _ in range(ratelimit.LOGIN_FAILURES_PER_ACCOUNT - 1):
        await record_login_failure(r, "u@corp.com")

    await check_login_failures(r, "u@corp.com")  # must not raise


@pytest.mark.asyncio
async def test_accounts_are_independent():
    r = FakeRedis()
    for _ in range(ratelimit.LOGIN_FAILURES_PER_ACCOUNT):
        await record_login_failure(r, "a@corp.com")
    await check_login_failures(r, "b@corp.com")  # must not raise


# ── wiring ────────────────────────────────────────────────────────────────────

def test_login_route_still_ip_rate_limited():
    from app.auth.router import router
    route = next(r for r in router.routes if getattr(r, "path", "") == "/auth/login")
    deps = [d.call for d in route.dependant.dependencies]
    assert any(getattr(d, "__qualname__", "").startswith("rate_limit") for d in deps)


def test_enrollment_limiter_uses_proxy_aware_client_ip():
    """Behind Caddy every probe shared Caddy's socket IP — one 10/min bucket
    for the whole fleet. It must key on the same client_ip as login."""
    import inspect

    from app.routers import probe_enrollment
    src = inspect.getsource(probe_enrollment._rate_limit)
    assert "client_ip(request)" in src

"""Hardening items from docs/STATUS.md: API docs off in production, AI routes rate limited."""
from __future__ import annotations

import pytest
from fastapi import HTTPException
from fastapi.routing import APIRoute

from app.main import api_docs_urls
from app.ratelimit import _check


def test_api_docs_hidden_in_production():
    assert api_docs_urls(True) == {"docs_url": None, "redoc_url": None, "openapi_url": None}


def test_api_docs_available_outside_production():
    assert api_docs_urls(False) == {
        "docs_url": "/docs", "redoc_url": "/redoc", "openapi_url": "/openapi.json",
    }


def _deps(route: APIRoute) -> set[str]:
    return {getattr(d.call, "__qualname__", "") for d in route.dependant.dependencies}


def test_ai_spending_routes_are_rate_limited():
    from app.routers import agent_advisor, ai, ai_report, portal, remediation

    expected = [
        (ai.router, {"/ai/generate"}),
        (ai_report.router, {"/generate"}),
        (agent_advisor.router, {"/run"}),
        (remediation.router, {"/{finding_id}/remediation/refine", "/{finding_id}/remediation/generate"}),
        (portal.router, {"/assistant/chat"}),
    ]
    for router, tails in expected:
        seen = set()
        for route in router.routes:
            if not isinstance(route, APIRoute) or "POST" not in route.methods:
                continue
            for tail in tails:
                if route.path.endswith(tail):
                    seen.add(tail)
                    assert any("rate_limit" in d for d in _deps(route)), f"POST {route.path} has no rate limit"
        # A rename must not silently skip the check.
        assert seen == tails, (router.prefix, tails - seen)


class _FakeRedis:
    def __init__(self):
        self.n = {}

    async def incr(self, k):
        self.n[k] = self.n.get(k, 0) + 1
        return self.n[k]

    async def expire(self, k, s):
        return True

    async def ttl(self, k):
        return 42


@pytest.mark.asyncio
async def test_ai_bucket_blocks_after_limit():
    r = _FakeRedis()
    for _ in range(30):
        await _check(r, "ai:1.2.3.4", 30, 60)
    with pytest.raises(HTTPException) as e:
        await _check(r, "ai:1.2.3.4", 30, 60)
    assert e.value.status_code == 429

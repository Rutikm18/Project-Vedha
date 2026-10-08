"""test_deploy_hardening.py — the deployment fixes from the 3 Oct architecture review.

* AI answers (a disposable cache) can live in their own Redis, so the main
  Redis — sessions, lockouts, sign-in codes — never has to evict.
* /metrics is served only to internal callers.
* The production compose file trusts forwarded client addresses only from the
  Docker networks, and the main Redis never evicts.
"""
from __future__ import annotations

import asyncio
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from app import dependencies
from app.ai import kv as kv_mod
from app.auth.middleware import _internal_caller

REPO = Path(__file__).resolve().parents[3]
COMPOSE = (REPO / "manager" / "docker-compose.yml").read_text(encoding="utf-8")


@pytest.fixture(autouse=True)
def _reset_answer_kv():
    kv_mod.set_answer_kv(None)
    yield
    kv_mod.set_answer_kv(None)


def test_answers_share_the_default_store_without_a_cache_url(monkeypatch):
    monkeypatch.setattr(kv_mod, "default_kv", lambda: "default-store")
    from app.config import get_settings
    monkeypatch.setattr(get_settings(), "redis_cache_url", "")
    assert kv_mod.answer_kv() == "default-store"


def test_answers_go_to_the_cache_redis_when_configured(monkeypatch):
    from app.config import get_settings
    monkeypatch.setattr(get_settings(), "redis_cache_url", "redis://cache:6379/0")
    store = kv_mod.answer_kv()
    assert isinstance(store, kv_mod.RedisKv) and store._cache is True

    seen = []

    async def cache_conn():
        conn = AsyncMock()
        conn.get = AsyncMock(return_value="cached")
        seen.append("cache")
        return conn

    async def main_conn():
        seen.append("main")
        return AsyncMock()

    monkeypatch.setattr(dependencies, "get_cache_redis", cache_conn)
    monkeypatch.setattr(dependencies, "get_redis", main_conn)
    assert asyncio.run(store.get("ai:ans:x")) == "cached"
    assert seen == ["cache"]


def test_cache_redis_falls_back_to_the_main_one(monkeypatch):
    monkeypatch.setattr(dependencies.settings, "redis_cache_url", "")
    sentinel = object()

    async def main():
        return sentinel

    monkeypatch.setattr(dependencies, "get_redis", main)
    assert asyncio.run(dependencies.get_cache_redis()) is sentinel


@pytest.mark.parametrize("host,internal", [
    ("127.0.0.1", True), ("172.18.0.5", True), ("10.2.3.4", True), ("192.168.1.9", True),
    ("::1", True), ("fd00::5", True), ("203.0.113.7", False), ("34.120.5.6", False), ("8.8.8.8", False), ("testclient", False), ("", False),
])
def test_metrics_are_for_internal_callers_only(host, internal):
    request = SimpleNamespace(client=SimpleNamespace(host=host) if host else None)
    assert _internal_caller(request) is internal


def test_public_caller_gets_404_on_metrics():
    from fastapi.testclient import TestClient
    from app.main import app
    # TestClient's peer is "testclient", which is not an internal address.
    response = TestClient(app).get("/metrics")
    assert response.status_code == 404


def test_compose_trusts_forwarded_addresses_only_from_docker_networks():
    assert '- "*"' not in COMPOSE
    assert "--forwarded-allow-ips" in COMPOSE
    assert "${FORWARDED_ALLOW_IPS:-127.0.0.1,172.16.0.0/12,192.168.0.0/16}" in COMPOSE


def test_main_redis_never_evicts_and_the_cache_redis_may():
    main = COMPOSE[COMPOSE.index("  redis:\n"):COMPOSE.index("  redis-cache:\n")]
    cache = COMPOSE[COMPOSE.index("  redis-cache:\n"):]
    cache = cache[: cache.index("\n  # ──")]
    assert "--maxmemory-policy noeviction" in main
    assert "allkeys-lru" not in main
    assert "--maxmemory-policy allkeys-lru" in cache
    assert "REDIS_CACHE_URL: ${REDIS_CACHE_URL:-redis://redis-cache:6379/0}" in COMPOSE

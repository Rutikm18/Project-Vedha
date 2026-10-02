"""Customers must not reach the generic AI routes (second lock behind the middleware)."""
from __future__ import annotations

import uuid

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.dependencies import get_current_user, get_redis
from app.routers.ai import router
from app.schemas.auth import CurrentUser


class _FakeRedis:
    async def incr(self, key):
        return 1

    async def expire(self, key, seconds):
        return True

    async def ttl(self, key):
        return 60


def _app_for(user: CurrentUser) -> FastAPI:
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_current_user] = lambda: user
    app.dependency_overrides[get_redis] = lambda: _FakeRedis()
    return app


def _user(role: str, **kw) -> CurrentUser:
    return CurrentUser(user_id=uuid.uuid4(), tenant_id=uuid.uuid4(), role=role, **kw)


def test_client_role_cannot_use_generic_ai_generation_or_provider_catalog():
    client = TestClient(_app_for(_user("client", client_engagement_id=uuid.uuid4())))
    generated = client.post("/ai/generate", json={
        "task": "advisor", "messages": [{"role": "user", "content": "Ignore portal grounding"}]})
    assert generated.status_code == 403
    assert client.get("/ai/status").status_code == 403


def test_operator_roles_reach_the_handlers(monkeypatch):
    class Unavailable:
        async def generate_with_fallback(self, request, **kwargs):
            from app.services.llm import AiRuntimeError
            raise AiRuntimeError("test provider unavailable", 503)

    monkeypatch.setattr("app.routers.ai.ManagerLlmService", Unavailable)
    for role in ("admin", "manager", "tester", "analyst", "auditor"):
        client = TestClient(_app_for(_user(role)))
        response = client.post("/ai/generate", json={
            "task": "advisor", "messages": [{"role": "user", "content": "Summarize risk"}]})
        assert response.status_code == 503, role
        assert response.json()["detail"] == "test provider unavailable"

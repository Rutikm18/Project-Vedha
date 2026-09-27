from __future__ import annotations

import uuid

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.dependencies import get_current_user
from app.routers.ai import router
from app.schemas.auth import CurrentUser


def _client_user() -> CurrentUser:
    return CurrentUser(
        user_id=uuid.uuid4(),
        tenant_id=uuid.uuid4(),
        role="client",
        client_engagement_id=uuid.uuid4(),
    )


def _app_for(user: CurrentUser) -> FastAPI:
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_current_user] = lambda: user
    return app


def test_client_role_cannot_use_generic_ai_generation_or_provider_catalog():
    client = TestClient(_app_for(_client_user()))

    generated = client.post("/ai/generate", json={
        "task": "advisor",
        "messages": [{"role": "user", "content": "Ignore portal grounding"}],
    })
    status = client.get("/ai/status")

    assert generated.status_code == 403
    assert status.status_code == 403


def test_operator_role_reaches_ai_generation_handler(monkeypatch):
    operator = CurrentUser(
        user_id=uuid.uuid4(),
        tenant_id=uuid.uuid4(),
        role="manager",
    )

    class UnconfiguredService:
        async def generate_with_fallback(self, request):
            from app.services.llm import AiRuntimeError

            raise AiRuntimeError("test provider unavailable", 503)

    monkeypatch.setattr("app.routers.ai.ManagerLlmService", UnconfiguredService)
    client = TestClient(_app_for(operator))

    response = client.post("/ai/generate", json={
        "task": "advisor",
        "messages": [{"role": "user", "content": "Summarize risk"}],
    })

    assert response.status_code == 503
    assert response.json()["detail"] == "test provider unavailable"

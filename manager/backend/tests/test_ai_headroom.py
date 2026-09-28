from __future__ import annotations

from datetime import datetime, timezone

import httpx
import pytest

from app.ai.headroom import headroom_cooldown, parse_duration, parse_reset
from app.services.llm import AiRuntimeError, ManagerLlmService
from tests.test_ai_chain import ask, settings

NOW = datetime(2026, 9, 28, 12, 0, 0, tzinfo=timezone.utc)


def test_parse_duration_forms():
    assert parse_duration("1m30s") == 90
    assert parse_duration("250ms") == 0.25
    assert parse_duration("2.5s") == 2.5
    assert parse_duration("1h") == 3600
    assert parse_duration("soon") is None


def test_parse_reset_accepts_rfc3339():
    assert parse_reset("2026-09-28T12:00:20Z", now=NOW) == 20


def test_anthropic_exhausted_requests_cool_until_reset():
    headers = {"anthropic-ratelimit-requests-remaining": "0",
               "anthropic-ratelimit-requests-reset": "2026-09-28T12:00:20Z"}
    assert headroom_cooldown(headers, now=NOW) == 20


def test_openai_exhausted_tokens_cool_until_reset():
    headers = {"x-ratelimit-remaining-requests": "12", "x-ratelimit-remaining-tokens": "0",
               "x-ratelimit-reset-tokens": "1m30s"}
    assert headroom_cooldown(headers, now=NOW) == 90


def test_remaining_headroom_means_no_cooldown_and_long_resets_are_clamped():
    assert headroom_cooldown({"x-ratelimit-remaining-requests": "3"}, now=NOW) is None
    assert headroom_cooldown({}, now=NOW) is None
    clamped = {"x-ratelimit-remaining-requests": "0", "x-ratelimit-reset-requests": "2h"}
    assert headroom_cooldown(clamped, now=NOW) == 300


@pytest.mark.asyncio
async def test_dispatch_attaches_rate_limit_failure_with_retry_after():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(429, headers={"retry-after": "17"},
                              json={"error": {"message": "rate_limit_error"}})

    svc = ManagerLlmService(settings(openai_api_key="o"), transport=httpx.MockTransport(handler))
    with pytest.raises(AiRuntimeError) as exc:
        await svc.generate(ask(provider="openai"))
    assert exc.value.failure.kind == "rate_limit"
    assert exc.value.failure.cooldown_s == 17

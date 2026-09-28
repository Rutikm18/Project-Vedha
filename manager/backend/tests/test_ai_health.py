from __future__ import annotations

import pytest

from app.ai.failures import Failure, classify_http
from app.ai.health import ProviderHealth
from app.ai.kv import MemoryKv


class _Clock:
    def __init__(self) -> None:
        self.now = 0.0

    def __call__(self) -> float:
        return self.now


@pytest.fixture
def clock():
    return _Clock()


@pytest.fixture
def health(clock):
    return ProviderHealth(MemoryKv(clock=clock))


@pytest.mark.asyncio
async def test_healthy_by_default(health):
    state = await health.state("anthropic")
    assert state.state == "healthy"
    assert ProviderHealth.allows(await health.acquire("anthropic"))


@pytest.mark.asyncio
async def test_rate_limit_cools_then_probes_once_then_heals(health, clock):
    await health.record_failure("anthropic", classify_http(429, "rate_limit", retry_after=30))
    cooling = await health.state("anthropic")
    assert (cooling.state, cooling.reason) == ("cooling", "rate_limit")
    assert cooling.retry_in_s == 30
    assert not ProviderHealth.allows(await health.acquire("anthropic"))

    clock.now += 30
    first = await health.acquire("anthropic")
    second = await health.acquire("anthropic")
    assert first.state == "probing" and ProviderHealth.allows(first)
    assert (second.state, second.reason) == ("cooling", "probe_in_flight")

    await health.record_success("anthropic")
    assert (await health.state("anthropic")).state == "healthy"


@pytest.mark.asyncio
async def test_overload_backoff_doubles_up_to_cap(health, clock):
    overloaded = classify_http(503, "overloaded")
    seen = []
    for _ in range(3):
        await health.record_failure("openai", overloaded)
        seen.append((await health.state("openai")).retry_in_s)
    assert seen == [30, 60, 120]
    for _ in range(6):
        await health.record_failure("openai", overloaded)
    assert (await health.state("openai")).retry_in_s == 600


@pytest.mark.asyncio
async def test_billing_is_blocked(health):
    await health.record_failure("anthropic", classify_http(400, "Your credit balance is too low"))
    state = await health.state("anthropic")
    assert (state.state, state.reason) == ("blocked", "billing")
    assert not ProviderHealth.allows(state)


@pytest.mark.asyncio
async def test_request_scoped_failure_changes_nothing(health):
    await health.record_failure("anthropic", Failure("request", None))
    assert (await health.state("anthropic")).state == "healthy"


@pytest.mark.asyncio
async def test_headroom_cooling_heals_without_probe(health, clock):
    await health.cool_for_headroom("openai", 5)
    assert (await health.state("openai")).reason == "headroom"
    clock.now += 5
    assert (await health.state("openai")).state == "healthy"

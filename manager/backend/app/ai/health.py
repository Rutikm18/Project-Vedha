"""health.py — per-provider circuit breaker shared by every worker.

States (see the routing design, diagram 4):
  healthy   no cooldown key and no recent strikes — requests go through
  cooling   ai:cool:{p} present with a transient reason (rate limit, overload,
            timeout, headroom) — skipped until it expires
  blocked   ai:cool:{p} present with a reason waiting will not fix (spend cap,
            billing, auth) — skipped; re-checked when the key expires
  probing   the cooldown expired but strikes remain — exactly ONE request (the
            winner of a SET NX lock) may try; success heals, failure re-cools with
            a doubled TTL

Without this memory every request re-discovers an outage and pays its latency;
kept in the shared KV so one worker's discovery protects all of them.
"""
from __future__ import annotations

import json
from dataclasses import dataclass

import structlog

from app.ai.failures import ESCALATION_CAP_S, Failure
from app.ai.kv import KvStore, default_kv

logger = structlog.get_logger()

STRIKES_TTL_S = 3600.0
PROBE_LOCK_S = 30.0


@dataclass(frozen=True)
class HealthState:
    state: str                   # healthy | cooling | blocked | probing
    reason: str | None = None
    retry_in_s: float | None = None


class ProviderHealth:
    def __init__(self, kv: KvStore | None = None) -> None:
        self._kv = kv or default_kv()

    @staticmethod
    def allows(state: HealthState) -> bool:
        return state.state in ("healthy", "probing")

    async def state(self, provider: str) -> HealthState:
        raw = await self._kv.get(f"ai:cool:{provider}")
        if raw:
            try:
                data = json.loads(raw)
            except ValueError:
                data = {}
            return HealthState(
                "blocked" if data.get("blocked") else "cooling",
                data.get("reason"),
                await self._kv.ttl(f"ai:cool:{provider}"),
            )
        if await self._kv.get(f"ai:strikes:{provider}"):
            return HealthState("probing")
        return HealthState("healthy")

    async def acquire(self, provider: str) -> HealthState:
        """State for a caller about to send a request. While probing, only the
        caller that wins the probe lock may proceed; everyone else waits."""
        current = await self.state(provider)
        if current.state != "probing":
            return current
        if await self._kv.set_nx(f"ai:probe:{provider}", "1", PROBE_LOCK_S):
            return current
        return HealthState("cooling", "probe_in_flight", PROBE_LOCK_S)

    async def record_failure(self, provider: str, failure: Failure) -> None:
        if failure.cooldown_s is None:
            return
        strikes = await self._kv.incr(f"ai:strikes:{provider}", STRIKES_TTL_S)
        cooldown = failure.cooldown_s
        if failure.escalates:
            cooldown = min(ESCALATION_CAP_S, cooldown * (2 ** (strikes - 1)))
        await self._kv.set(
            f"ai:cool:{provider}",
            json.dumps({"reason": failure.kind, "blocked": failure.blocked}),
            cooldown,
        )
        await self._kv.delete(f"ai:probe:{provider}")
        log = logger.error if failure.blocked else logger.warning
        log("ai.provider.cooldown", provider=provider, reason=failure.kind,
            blocked=failure.blocked, seconds=round(cooldown), strikes=strikes)

    async def record_success(self, provider: str) -> None:
        await self._kv.delete(f"ai:strikes:{provider}", f"ai:probe:{provider}")

    async def cool_for_headroom(self, provider: str, seconds: float) -> None:
        """The provider's own headers say its limit is exhausted: step aside
        until the reset instead of collecting a 429 first. Not a strike."""
        await self._kv.set(
            f"ai:cool:{provider}", json.dumps({"reason": "headroom", "blocked": False}), seconds)
        logger.info("ai.provider.headroom", provider=provider, seconds=round(seconds))

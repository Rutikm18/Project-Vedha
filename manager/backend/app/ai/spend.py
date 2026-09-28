"""spend.py — a daily dollar meter per provider, with optional caps.

Provider-side cutoffs are blunt: reaching an Anthropic usage tier's monthly spend
cap pauses the API until the 1st. A daily cap Vedha controls turns a spike (a
stuck agent loop, a report regenerated 50 times) into a step down the chain
instead of a lost month.

Cost = tokens from the provider's own ``usage`` block × a per-model price
(USD per 1M tokens). Models without a price are not metered — set
AI_MODEL_PRICES for them — and a provider without a cap is never skipped.
"""
from __future__ import annotations

import structlog

from app.ai.kv import KvStore
from app.services.project_time import project_now

logger = structlog.get_logger()

# USD per 1M tokens (input, output). Operators add/override via AI_MODEL_PRICES
# ("model=in:out,model=in:out").
DEFAULT_PRICES: dict[str, tuple[float, float]] = {"claude-sonnet-4-6": (3.0, 15.0)}
SPEND_KEY_TTL_S = 2 * 86400.0
_OPENAI_SHAPED = ("openai", "groq", "openrouter", "local_openai")


def _pairs(csv: str) -> list[tuple[str, str]]:
    out = []
    for item in (csv or "").split(","):
        name, sep, value = item.partition("=")
        if sep and name.strip() and value.strip():
            out.append((name.strip(), value.strip()))
    return out


def parse_prices(csv: str) -> dict[str, tuple[float, float]]:
    prices: dict[str, tuple[float, float]] = {}
    for model, value in _pairs(csv):
        rate_in, sep, rate_out = value.partition(":")
        try:
            if sep:
                prices[model] = (float(rate_in), float(rate_out))
        except ValueError:
            continue
    return prices


def parse_caps(csv: str) -> dict[str, float]:
    caps: dict[str, float] = {}
    for provider, value in _pairs(csv):
        try:
            caps[provider.lower()] = float(value)
        except ValueError:
            continue
    return caps


def usage_tokens(provider: str, body: dict | None) -> tuple[float, float] | None:
    """(billable input tokens, output tokens) from a provider response body.
    Anthropic prompt-cache writes cost 1.25× and reads 0.1× the input rate, so
    they are folded into input at those weights."""
    if not isinstance(body, dict):
        return None
    try:
        if provider == "anthropic":
            u = body["usage"]
            billable_in = (u.get("input_tokens", 0)
                           + 1.25 * u.get("cache_creation_input_tokens", 0)
                           + 0.1 * u.get("cache_read_input_tokens", 0))
            return billable_in, u.get("output_tokens", 0)
        if provider in _OPENAI_SHAPED:
            u = body["usage"]
            return u.get("prompt_tokens", 0), u.get("completion_tokens", 0)
        if provider == "gemini":
            u = body["usageMetadata"]
            return u.get("promptTokenCount", 0), u.get("candidatesTokenCount", 0)
        if provider == "ollama":
            return body["prompt_eval_count"], body["eval_count"]
    except (KeyError, TypeError, AttributeError):
        return None
    return None


class SpendMeter:
    def __init__(self, kv: KvStore, settings) -> None:
        self._kv = kv
        self._prices = {**DEFAULT_PRICES, **parse_prices(getattr(settings, "ai_model_prices", ""))}
        self._caps = parse_caps(getattr(settings, "ai_daily_cap_usd", ""))

    @staticmethod
    def _key(provider: str) -> str:
        # The day turns at midnight project time (IST), matching every other
        # timestamp an operator sees.
        return f"ai:spend:{provider}:{project_now():%Y-%m-%d}"

    def cap(self, provider: str) -> float | None:
        return self._caps.get(provider)

    async def record(self, provider: str, model: str, body: dict | None) -> float:
        tokens = usage_tokens(provider, body)
        price = self._prices.get(model)
        if tokens is None or price is None:
            return 0.0
        cost = (tokens[0] * price[0] + tokens[1] * price[1]) / 1_000_000
        if cost <= 0:
            return 0.0
        total = await self._kv.incr_float(self._key(provider), cost, SPEND_KEY_TTL_S)
        cap = self.cap(provider)
        if cap is not None and total >= cap and total - cost < cap:
            logger.warning("ai.spend.daily_cap_reached", provider=provider,
                           spent_usd=round(total, 2), cap_usd=cap)
        return cost

    async def today(self, provider: str) -> float:
        raw = await self._kv.get(self._key(provider))
        try:
            return float(raw) if raw else 0.0
        except ValueError:
            return 0.0

    async def over_cap(self, provider: str) -> bool:
        cap = self.cap(provider)
        return cap is not None and await self.today(provider) >= cap

"""routing.py — which models a request may use, and in what order. Pure.

Tiers, best first: premium (paid, not trained on) → budget (paid Gemini Flash) →
free (may be trained on; always pseudonymized) → local (never leaves the server).
Each task names the LOWEST cloud tier it accepts: a free model may answer an
operator's chat, never a board report. Local tiers are never filtered by the
floor — they are private, and under the sovereign profile the only option.
"""
from __future__ import annotations

from dataclasses import dataclass

PREMIUM, BUDGET, FREE, LOCAL = "premium", "budget", "free", "local"
TIER_RANK = {PREMIUM: 0, BUDGET: 1, FREE: 2}

CLOUD_PROVIDERS = ("anthropic", "openai", "gemini", "groq", "openrouter")
LOCAL_PROVIDERS = ("local_openai", "ollama")
# Local models only ever join a chain when named — never as an implicit fallback.
DEFAULT_CHAIN = CLOUD_PROVIDERS
KNOWN_PROVIDERS = frozenset(CLOUD_PROVIDERS + LOCAL_PROVIDERS)

# An attempt that is not the last candidate never takes less than this — a
# premium answer needs room to finish — nor more than half of what remains, so a
# hung provider always leaves time for the next tier.
MIN_ATTEMPT_S = 15.0


def provider_tier(provider: str, *, gemini_paid: bool = False) -> str:
    if provider in ("anthropic", "openai"):
        return PREMIUM
    if provider == "gemini":
        return BUDGET if gemini_paid else FREE
    if provider in LOCAL_PROVIDERS:
        return LOCAL
    return FREE


@dataclass(frozen=True)
class TaskPolicy:
    lowest_tier: str          # lowest cloud tier allowed to answer
    deadline_s: float         # total wall-clock budget across every attempt
    json_output: bool = False  # answer must parse as a JSON object
    cacheable: bool = False    # one-shot, deterministic input → answer may be reused


_POLICIES = {
    "advisor": TaskPolicy(FREE, 90.0),
    "security_followup": TaskPolicy(FREE, 90.0),
    "client_assistant": TaskPolicy(FREE, 90.0),
    "security_brief": TaskPolicy(BUDGET, 90.0, cacheable=True),
    "advisor_flow": TaskPolicy(BUDGET, 90.0, json_output=True, cacheable=True),
    "remediation_refine": TaskPolicy(BUDGET, 120.0, json_output=True, cacheable=True),
    "compliance_brief": TaskPolicy(PREMIUM, 90.0, cacheable=True),
    "engagement_report": TaskPolicy(PREMIUM, 180.0, json_output=True, cacheable=True),
    "report": TaskPolicy(PREMIUM, 240.0),
}
_DEFAULT_POLICY = TaskPolicy(FREE, 90.0)


def task_policy(task: str) -> TaskPolicy:
    return _POLICIES.get(task, _DEFAULT_POLICY)


def chain_order(chain_csv: str, pinned: str) -> list[str]:
    """LLM_CHAIN wins when set (unknown names and duplicates dropped, order kept).
    Otherwise the premium-first default, with an explicitly pinned LLM_PROVIDER
    moved to the front."""
    if chain_csv and chain_csv.strip():
        order: list[str] = []
        for part in chain_csv.split(","):
            name = part.strip().lower()
            if name in KNOWN_PROVIDERS and name not in order:
                order.append(name)
        return order
    order = list(DEFAULT_CHAIN)
    pinned = (pinned or "").strip().lower()
    if pinned in KNOWN_PROVIDERS:
        if pinned in order:
            order.remove(pinned)
        order.insert(0, pinned)
    return order


def allowed_by_floor(tier: str, lowest_tier: str, best_configured_rank: int) -> bool:
    """The floor relaxes to the best cloud tier actually configured: an operator
    who configured only free models chose free models."""
    if tier == LOCAL:
        return True
    floor = max(TIER_RANK[lowest_tier], best_configured_rank)
    return TIER_RANK[tier] <= floor


def attempt_budget(remaining_s: float, *, is_last: bool, cap_s: float) -> float:
    if is_last:
        return min(remaining_s, cap_s)
    return min(cap_s, remaining_s, max(MIN_ATTEMPT_S, remaining_s / 2))

from __future__ import annotations

from app.ai.routing import (
    BUDGET,
    FREE,
    LOCAL,
    PREMIUM,
    TIER_RANK,
    allowed_by_floor,
    attempt_budget,
    chain_order,
    provider_tier,
    task_policy,
)


def test_default_chain_is_premium_first_and_never_local():
    assert chain_order("", "") == ["anthropic", "openai", "gemini", "groq", "openrouter"]


def test_pinned_provider_moves_to_front():
    assert chain_order("", "gemini")[:2] == ["gemini", "anthropic"]
    assert chain_order("", "ollama")[0] == "ollama"
    assert "ollama" not in chain_order("", "")


def test_explicit_chain_is_authoritative_and_cleaned():
    assert chain_order("openai, Anthropic,bogus,openai,groq", "gemini") == ["openai", "anthropic", "groq"]


def test_provider_tiers():
    assert provider_tier("anthropic") == PREMIUM
    assert provider_tier("openai") == PREMIUM
    assert provider_tier("gemini") == FREE
    assert provider_tier("gemini", gemini_paid=True) == BUDGET
    assert provider_tier("groq") == FREE
    assert provider_tier("openrouter") == FREE
    assert provider_tier("ollama") == LOCAL
    assert provider_tier("local_openai") == LOCAL


def test_floor_excludes_free_when_premium_is_configured():
    compliance = task_policy("compliance_brief")
    best = TIER_RANK[PREMIUM]
    assert allowed_by_floor(PREMIUM, compliance.lowest_tier, best)
    assert not allowed_by_floor(FREE, compliance.lowest_tier, best)


def test_floor_relaxes_when_only_free_is_configured():
    compliance = task_policy("compliance_brief")
    assert allowed_by_floor(FREE, compliance.lowest_tier, TIER_RANK[FREE])


def test_local_is_never_filtered():
    assert allowed_by_floor(LOCAL, PREMIUM, TIER_RANK[PREMIUM])


def test_task_policies():
    assert task_policy("advisor_flow").json_output and task_policy("advisor_flow").cacheable
    assert not task_policy("client_assistant").cacheable
    assert task_policy("engagement_report").lowest_tier == PREMIUM
    assert task_policy("not-a-task").lowest_tier == FREE


def test_attempt_budget_leaves_room_for_the_next_tier():
    assert attempt_budget(90, is_last=False, cap_s=180) == 45
    assert attempt_budget(20, is_last=False, cap_s=180) == 15
    assert attempt_budget(10, is_last=False, cap_s=180) == 10
    assert attempt_budget(90, is_last=True, cap_s=180) == 90
    assert attempt_budget(90, is_last=True, cap_s=30) == 30

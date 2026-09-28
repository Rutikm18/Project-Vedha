from __future__ import annotations

import json
import re
import uuid
from typing import Any, Literal

from pydantic import BaseModel, Field, model_validator


ProviderId = Literal["ollama", "local_openai", "openrouter", "anthropic", "openai", "gemini", "groq"]

MODEL_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/-]{0,159}$")


class AiMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=6_000)


class AiGenerateRequest(BaseModel):
    task: Literal["advisor", "security_brief", "security_followup", "advisor_flow",
                  "client_assistant", "compliance_brief", "remediation_refine",
                  "engagement_report"]
    messages: list[AiMessage] = Field(min_length=1, max_length=24)
    context: dict[str, Any] = Field(default_factory=dict)
    provider: ProviderId | None = None
    model: str | None = Field(default=None, min_length=1, max_length=160)
    max_tokens: int = Field(default=900, ge=128, le=2_048)
    # Optional: answer as the engagement's sector domain expert. The server loads
    # the profile/tags itself (tenant-scoped); nothing from the caller reaches the
    # trusted system prompt.
    engagement_id: uuid.UUID | None = None

    @model_validator(mode="after")
    def validate_bounded_input(self):
        if sum(len(message.content) for message in self.messages) > 24_000:
            raise ValueError("conversation exceeds 24,000 characters")
        if len(json.dumps(self.context, default=str, separators=(",", ":"))) > 32_000:
            raise ValueError("context exceeds 32,000 characters")
        if self.model and not MODEL_ID.fullmatch(self.model):
            raise ValueError("model contains unsupported characters")
        return self


class AiProviderStatus(BaseModel):
    id: ProviderId
    label: str
    configured: bool
    privacy: Literal["local", "cloud"]
    default_model: str
    models: list[str]
    reason: str | None = None


class AiChainEntry(BaseModel):
    """One provider in the automatic chain, in the order it is tried."""
    provider: ProviderId
    model: str
    tier: Literal["premium", "budget", "free", "local"]
    state: Literal["healthy", "cooling", "blocked", "probing"]
    reason: str | None = None
    retry_in_s: int | None = None
    spend_today_usd: float | None = None
    daily_cap_usd: float | None = None


class AiStatusResponse(BaseModel):
    # None = no default provider is usable (no cloud key configured). The UI then
    # prompts for a key instead of preselecting a provider.
    provider: ProviderId | None
    model: str
    configured: bool
    privacy: Literal["local", "cloud"]
    reason: str | None = None
    providers: list[AiProviderStatus]
    # The automatic chain (the operator never picks a provider): order, health,
    # today's spend. Empty when nothing is configured.
    chain: list[AiChainEntry] = Field(default_factory=list)


class AiGenerateResponse(BaseModel):
    content: str
    provider: ProviderId
    model: str
    privacy: Literal["local", "cloud"]
    # True when the requested/default provider failed (e.g. out of credit) and a
    # free fallback model served the response instead.
    fallback: bool = False
    # premium | budget | free | local — the tier that actually answered.
    tier: str | None = None
    skill: str | None = None
    skill_label: str | None = None
    jurisdictions: list[str] = Field(default_factory=list)
    # Regulatory citations in the answer that are NOT in Vedha's compliance packs.
    unverified_citations: list[str] = Field(default_factory=list)

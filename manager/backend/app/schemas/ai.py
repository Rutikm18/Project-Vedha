from __future__ import annotations

import json
import re
from typing import Any, Literal

from pydantic import BaseModel, Field, model_validator


MODEL_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/-]{0,159}$")


class AiMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=6_000)


class AiGenerateRequest(BaseModel):
    task: Literal["advisor", "security_brief", "security_followup", "advisor_flow"]
    messages: list[AiMessage] = Field(min_length=1, max_length=24)
    context: dict[str, Any] = Field(default_factory=dict)
    provider: Literal["ollama", "openrouter", "anthropic", "openai"] | None = None
    model: str | None = Field(default=None, min_length=1, max_length=160)
    max_tokens: int = Field(default=900, ge=128, le=2_048)

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
    id: Literal["ollama", "openrouter", "anthropic", "openai"]
    label: str
    configured: bool
    privacy: Literal["local", "cloud"]
    default_model: str
    models: list[str]
    reason: str | None = None


class AiStatusResponse(BaseModel):
    provider: Literal["ollama", "openrouter", "anthropic", "openai"]
    model: str
    configured: bool
    privacy: Literal["local", "cloud"]
    reason: str | None = None
    providers: list[AiProviderStatus]


class AiGenerateResponse(BaseModel):
    content: str
    provider: Literal["ollama", "openrouter", "anthropic", "openai"]
    model: str
    privacy: Literal["local", "cloud"]

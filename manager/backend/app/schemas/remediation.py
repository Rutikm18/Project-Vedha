import uuid
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, field_validator


RemediationRisk = Literal["low", "medium", "high"]


class RemediationStepOut(BaseModel):
    step: int = Field(ge=1)
    title: str = "Remediation step"
    description: str = ""
    commands: dict[str, list[str]] | None = None
    commands_for_os: list[str] = Field(default_factory=list)
    verification: str = ""
    risk: RemediationRisk = "low"
    unsafe_commands_removed: bool = False

    @field_validator("risk", mode="before")
    @classmethod
    def normalize_risk(cls, value: object) -> str:
        normalized = str(value or "low").lower()
        return normalized if normalized in {"low", "medium", "high"} else "medium"


class RemediationPlanDetailOut(BaseModel):
    category: str = "generic"
    os: str = "generic"
    source: str = "deterministic_kb"
    summary: str = "Follow the ordered remediation actions and verify with a new assessment."
    effort: RemediationRisk = "medium"
    remediation_risk: RemediationRisk = "medium"
    steps: list[RemediationStepOut] = Field(default_factory=list)
    verification: list[str] = Field(default_factory=list)
    long_term_recommendations: list[str] = Field(default_factory=list)
    compensating_controls: str = ""
    model: str | None = None

    @field_validator("effort", "remediation_risk", mode="before")
    @classmethod
    def normalize_risk_levels(cls, value: object) -> str:
        normalized = str(value or "medium").lower()
        return normalized if normalized in {"low", "medium", "high"} else "medium"


class RemediationPlanOut(BaseModel):
    finding_id: uuid.UUID
    os: str
    source: str
    reviewed: bool
    cached: bool
    generated_at: datetime | None = None
    model: str | None = None
    plan: RemediationPlanDetailOut

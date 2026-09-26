import uuid
from datetime import datetime
from typing import Any, Literal

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
    # v2 contextual plan (app/remediation/plan.py) — optional so pre-v2 cached
    # AI rows still validate.
    tier: Literal["containment", "fix", "hardening"] = "fix"
    pre_checks: list[str] = Field(default_factory=list)
    reboot_required: bool | None = None
    downtime: str = ""
    rollback: str = ""
    ai_changed: bool = False

    @field_validator("tier", mode="before")
    @classmethod
    def normalize_tier(cls, value: object) -> str:
        normalized = str(value or "fix").lower()
        return normalized if normalized in {"containment", "fix", "hardening"} else "fix"

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
    # ── v2 contextual fields ─────────────────────────────────────────────────
    recipe_id: str | None = None
    recipe_version: int | None = None
    os_auto: str | None = None
    title: str | None = None
    remediation_type: str | None = None
    risk_response: str | None = None
    target_state: str | None = None
    urgency: dict[str, Any] | None = None
    due: dict[str, Any] | None = None
    context: dict[str, Any] | None = None
    exposure: str | None = None
    verification_check: dict[str, Any] | None = None
    references: list[str] = Field(default_factory=list)
    fragile_guard: dict[str, Any] | None = None
    provenance: dict[str, Any] | None = None
    ai_changes: list[dict[str, Any]] = Field(default_factory=list)
    sequencing_rationale: str = ""

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
    # True when a cached AI refinement was produced from facts that no longer
    # match the live asset/service record (version, port, exposure changed).
    stale: bool = False
    # The fix bundle this finding belongs to ({fix_key, ref, members}).
    bundle: dict[str, Any] | None = None

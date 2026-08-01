import uuid
from datetime import datetime
from ipaddress import ip_network

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.models.enums import EngagementStatus


# ── Request schemas ────────────────────────────────────────────────────────────

def validate_scope_entries(values: list[str]) -> list[str]:
    """Validate and de-duplicate exact IP/CIDR authorization boundaries."""
    normalized: list[str] = []
    seen: set[str] = set()
    for raw in values:
        value = raw.strip()
        if not value:
            raise ValueError("scope entries cannot be blank")
        try:
            ip_network(value, strict=False)
        except ValueError as exc:
            raise ValueError(f"invalid IP address or CIDR: {value}") from exc
        if value not in seen:
            normalized.append(value)
            seen.add(value)
    return normalized


def validate_engagement_dates(
    start_time: datetime | None,
    end_time: datetime | None,
) -> None:
    if start_time is None or end_time is None:
        return
    try:
        invalid = end_time < start_time
    except TypeError as exc:
        raise ValueError("start_time and end_time must use compatible timezones") from exc
    if invalid:
        raise ValueError("end_time must be on or after start_time")


class EngagementCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    scope_cidrs: list[str] = Field(..., min_length=1)
    excluded_cidrs: list[str] = Field(default_factory=list)
    start_time: datetime | None = None
    end_time: datetime | None = None
    rules_of_engagement: dict | None = None

    @field_validator("name")
    @classmethod
    def normalize_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("name cannot be blank")
        return value

    @field_validator("scope_cidrs", "excluded_cidrs")
    @classmethod
    def validate_scopes(cls, values: list[str]) -> list[str]:
        return validate_scope_entries(values)

    @model_validator(mode="after")
    def validate_dates(self):
        validate_engagement_dates(self.start_time, self.end_time)
        return self


class EngagementFilter(BaseModel):
    status: EngagementStatus | None = None
    start_after: datetime | None = None
    start_before: datetime | None = None
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)


# ── Response schemas ───────────────────────────────────────────────────────────

class FindingSummary(BaseModel):
    total: int
    critical: int
    high: int
    medium: int
    low: int
    info: int
    open: int
    remediated: int


class EngagementOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    name: str
    status: EngagementStatus
    scope_cidrs: list[str]
    excluded_cidrs: list[str] | None
    start_time: datetime | None
    end_time: datetime | None
    rules_of_engagement: dict | None
    created_at: datetime
    updated_at: datetime


class EngagementDetail(EngagementOut):
    asset_count: int = 0
    finding_summary: FindingSummary = Field(
        default_factory=lambda: FindingSummary(
            total=0, critical=0, high=0, medium=0, low=0, info=0, open=0, remediated=0
        )
    )

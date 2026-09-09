"""
schemas/portal.py — customer-safe response shapes.

CRITICAL: these are WHITELISTS. The operator `FindingOut` and the `Finding` model
expose internal red/blue-team judgment (exploit_validated, detection_status, the
verification_* triage, resolution mechanics, raw evidence). A customer must never
see those, so the portal has its own serializers that only ever carry customer-
appropriate fields. Never widen these to reuse an operator schema.
"""
from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.models.enums import FindingSeverity, FindingStatus


class ClientFindingOut(BaseModel):
    """A finding as a CUSTOMER may see it. model_validate(from_attributes=True)
    reads only these declared fields, so any extra attribute on the ORM object
    (evidence, verification_rationale, exploit_validated, …) is dropped."""
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    description: str | None = None
    severity: FindingSeverity
    status: FindingStatus
    cvss_score: Decimal | None = None
    cve_ids: list[str] | None = None
    risk_score: Decimal | None = None
    remediation: str | None = None
    first_seen: datetime | None = None


class ClientEngagementOut(BaseModel):
    id: uuid.UUID
    name: str
    status: str
    scope_cidr_count: int
    # The customer's own authorized scope, so the scan-request form can show what
    # they may target. Excluded ranges are enforced server-side (not exposed here).
    scope_cidrs: list[str] = []
    excluded_cidrs: list[str] = []
    has_assigned_agent: bool
    assigned_agent_id: uuid.UUID | None = None


class ClientPostureOut(BaseModel):
    risk_index: float
    exploitable_score: float
    posture_score: int
    grade: str
    open_findings: int


class ClientSummaryOut(BaseModel):
    """One call powering the dashboard header: posture + KPI counts + queue state."""
    posture: ClientPostureOut
    open_findings: int
    closed_findings: int
    severity_counts: dict[str, int]     # open findings by severity
    pending_requests: int
    running_jobs: int


class ClientTrendPoint(BaseModel):
    period: str                          # "YYYY-MM"
    opened: int
    closed: int


class ClientTrendsOut(BaseModel):
    by_severity: dict[str, int]          # open findings by severity (donut)
    timeline: list[ClientTrendPoint]     # opened vs closed per month (line)


class ClientReportOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    output_type: str
    model: str
    generated_at: datetime


class ClientReportContent(ClientReportOut):
    content: str


class ClientScanOut(BaseModel):
    id: uuid.UUID
    kind: str            # "job" (dispatched) | "request" (pending/approved/rejected)
    scan_type: str
    status: str
    at: datetime | None


class ScanRequestCreate(BaseModel):
    """A customer's rich scan request. The customer may ask for any active scan
    type, at a chosen intensity, over specific in-scope targets — an operator
    still approves every request before anything runs (the safety gate)."""
    # Validated against ScanJobType in the route so the vocabulary can't drift
    # from the enum; kept as a plain str here to avoid a second source of truth.
    scan_type: str = "vuln_scan"
    # Preferred: a capability use-case id from the portal catalog (GET
    # /portal/use-cases). When set, it drives scan_type + the probe's use case.
    use_case_id: str | None = None
    # Specific hosts / sub-ranges to scan. Each MUST be inside the engagement
    # scope (re-validated server-side). None/empty → the whole engagement scope.
    targets: list[str] | None = None
    intensity: Literal["light", "standard", "deep"] | None = None
    note: str | None = None


class ClientScanRequestOut(BaseModel):
    id: uuid.UUID
    scan_type: str
    use_case_id: str | None = None
    status: str
    targets: list[str] | None = None
    intensity: str | None = None
    note: str | None = None
    requested_at: datetime | None = None


class ClientAssistantMessage(BaseModel):
    """One turn of the customer's conversation. Bounded so a crafted client can't
    push an unbounded prompt through the portal into the model."""
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=4_000)


class ClientAssistantAsk(BaseModel):
    messages: list[ClientAssistantMessage] = Field(min_length=1, max_length=16)
    # Optional finding the customer is asking about — validated against their own
    # engagement server-side before any of it reaches the model.
    finding_id: uuid.UUID | None = None

    @model_validator(mode="after")
    def _bounded(self):
        if sum(len(m.content) for m in self.messages) > 16_000:
            raise ValueError("conversation exceeds 16,000 characters")
        if self.messages[-1].role != "user":
            raise ValueError("the last message must be from the user")
        return self


class ClientAssistantReply(BaseModel):
    content: str
    provider: str
    model: str
    # True when the answer was grounded in this engagement's recorded data.
    grounded: bool
    generated_at: datetime

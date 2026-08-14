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

from pydantic import BaseModel, ConfigDict

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
    has_assigned_agent: bool


class ClientPostureOut(BaseModel):
    risk_index: float
    exploitable_score: float
    posture_score: int
    grade: str
    open_findings: int


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
    # Constrained on purpose: a customer may only ask for safe, read-only scan
    # kinds. Anything intrusive stays operator-initiated.
    scan_type: Literal["discovery", "vuln_scan"] = "vuln_scan"
    note: str | None = None


class ClientScanRequestOut(BaseModel):
    id: uuid.UUID
    scan_type: str
    status: str
    note: str | None = None
    requested_at: datetime | None = None

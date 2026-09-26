"""Response models for the grouped findings view (GET /findings/groups)."""
import uuid
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class FindingGroupHost(BaseModel):
    ip: str | None = None
    hostname: str | None = None


class FindingGroupMember(BaseModel):
    id: uuid.UUID
    title: str
    severity: str
    status: str
    asset_ip: str | None = None
    asset_hostname: str | None = None
    port: int | None = None
    cve_ids: list[str] = Field(default_factory=list)
    risk: float
    cvss: float | None = None


class FindingGroupOut(BaseModel):
    key: str
    kind: Literal["rule", "product", "cve", "title"]
    label: str
    severity: str
    severity_counts: dict[str, int]
    status_counts: dict[str, int]
    finding_count: int
    open_count: int
    host_count: int
    unassigned_count: int
    hosts: list[FindingGroupHost]
    ports: list[int]
    port_count: int
    cve_count: int
    cves: list[str]
    max_risk: float
    max_cvss: float | None = None
    max_epss: float | None = None
    kev: bool
    exploit_validated: bool
    first_seen: datetime | None = None
    last_seen: datetime | None = None
    top_finding_id: uuid.UUID
    members: list[FindingGroupMember]
    members_truncated: bool


class FindingGroupPage(BaseModel):
    items: list[FindingGroupOut]
    total: int                 # number of groups
    page: int
    page_size: int
    pages: int
    finding_total: int         # findings across all groups (matches the list total)
    truncated: bool = False    # the row cap was hit; groups cover the first N findings

"""Deadline-extension request/decision contracts."""
from __future__ import annotations

import uuid
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, model_validator


class ExtensionCreate(BaseModel):
    subject_type: Literal["finding", "bundle"]
    finding_id: uuid.UUID | None = None
    fix_key: str | None = Field(default=None, min_length=12, max_length=12, pattern="^[0-9a-f]{12}$")
    requested_due_at: datetime
    reason: str = Field(min_length=10, max_length=2000)
    compensating_control: str | None = Field(default=None, max_length=2000)

    @model_validator(mode="after")
    def subject_matches(self):
        if self.subject_type == "finding" and self.finding_id is None:
            raise ValueError("finding_id is required for a finding request")
        if self.subject_type == "bundle" and not self.fix_key:
            raise ValueError("fix_key is required for a bundle request")
        if self.requested_due_at.tzinfo is None:
            raise ValueError("requested_due_at must include a timezone offset")
        if self.compensating_control is not None and not self.compensating_control.strip():
            self.compensating_control = None
        return self


class ExtensionDecision(BaseModel):
    note: str = Field(min_length=3, max_length=2000)
    # Approve only: an operator may grant a different date than requested.
    due_at: datetime | None = None

    @model_validator(mode="after")
    def aware(self):
        if self.due_at is not None and self.due_at.tzinfo is None:
            raise ValueError("due_at must include a timezone offset")
        return self


class ExtensionOut(BaseModel):
    id: uuid.UUID
    engagement_id: uuid.UUID
    subject_type: str
    finding_id: uuid.UUID | None = None
    fix_key: str | None = None
    fix_ref: str | None = None
    member_finding_ids: list[uuid.UUID]
    current_due_at: datetime | None = None
    requested_due_at: datetime
    reason: str
    compensating_control: str | None = None
    status: str
    requested_by: uuid.UUID | None = None
    requested_at: datetime | None = None
    decided_by: uuid.UUID | None = None
    decided_at: datetime | None = None
    decided_due_at: datetime | None = None
    decision_note: str | None = None

    model_config = {"from_attributes": True}

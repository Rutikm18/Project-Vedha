"""
customer_entitlement.py — what a customer's portal login is allowed to consume.

One row per engagement (the portal login is already 1:1 with its engagement).
The operator sets it from the Customers dashboard:

  * plan_type  — "poc" (a time-boxed trial) or "licensed" (full use)
  * starts_at / expires_at — the POC window or the licence term; NULL expiry = none
  * scan_quota — portal scans the customer may run; NULL = unlimited
  * scans_used — a ledger counter, changed only under a row lock
    (services/entitlements.py), so parallel launches can't overspend it

Operator-launched scans never touch the counter; the quota governs the portal.
"""
from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin

PLAN_POC = "poc"
PLAN_LICENSED = "licensed"
PLAN_TYPES = (PLAN_POC, PLAN_LICENSED)


class CustomerEntitlement(Base, TimestampMixin):
    __tablename__ = "customer_entitlements"
    __table_args__ = (
        CheckConstraint("plan_type IN ('poc', 'licensed')", name="ck_entitlement_plan_type"),
        CheckConstraint("scan_quota IS NULL OR scan_quota >= 0", name="ck_entitlement_quota"),
        CheckConstraint("scans_used >= 0", name="ck_entitlement_used"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    engagement_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("engagements.id", ondelete="CASCADE"),
        nullable=False, unique=True,
    )
    plan_type: Mapped[str] = mapped_column(String(16), nullable=False, server_default=PLAN_POC)
    starts_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    scan_quota: Mapped[int | None] = mapped_column(Integer, nullable=True)
    scans_used: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    # Issued the first time the plan becomes "licensed"; shown to the customer.
    license_key: Mapped[str | None] = mapped_column(String(32), nullable=True, unique=True)
    notes: Mapped[str | None] = mapped_column(Text(), nullable=True)
    updated_by: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)

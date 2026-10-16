"""
tenant_settings.py — an organisation's policy settings, one row per tenant.

Four JSON sections, each validated by a Pydantic model in
app.services.org_settings (a missing row or key means that section's defaults, so
existing tenants behave exactly as before until an admin changes something):

* auth_policy        sign-in network allowlist, absolute session length
* scan_policy        blackout windows, admin override, global exclusions
* customer_defaults  what a newly provisioned POC customer starts with
* audit_policy       how long audit-log entries are kept
"""
from __future__ import annotations

import uuid

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class TenantSettings(Base):
    __tablename__ = "tenant_settings"

    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), primary_key=True
    )
    auth_policy: Mapped[dict] = mapped_column(JSONB, nullable=False, server_default="{}")
    scan_policy: Mapped[dict] = mapped_column(JSONB, nullable=False, server_default="{}")
    customer_defaults: Mapped[dict] = mapped_column(JSONB, nullable=False, server_default="{}")
    audit_policy: Mapped[dict] = mapped_column(JSONB, nullable=False, server_default="{}")
    updated_by: Mapped[str | None] = mapped_column(String(64), nullable=True)
    updated_at = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(),
                               onupdate=func.now())

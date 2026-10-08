"""
notification_rule.py — a tenant's choice of which events send a notification, and
through which channels (email / Slack).

One row per (tenant, event). A tenant with no row for an event gets that event's
default from app.services.notification_rules, so a fresh install needs no seeding
and a new event type needs no migration.
"""
from __future__ import annotations

import uuid

from sqlalchemy import Boolean, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class NotificationRule(Base, TimestampMixin):
    __tablename__ = "notification_rules"
    __table_args__ = (UniqueConstraint("tenant_id", "event_key", name="uq_notification_rule_tenant_event"),)

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    event_key: Mapped[str] = mapped_column(String(48), nullable=False)
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="true")
    channels: Mapped[list] = mapped_column(JSONB, nullable=False, server_default="[]")

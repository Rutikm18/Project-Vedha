"""
sla_policy.py — a tenant's custom SLA remediation windows (hours per severity).

One row per tenant (absence = use the env defaults). `services/sla.py` resolves
this into the `windows` map it computes deadlines from, so a saved policy takes
effect everywhere SLA is shown without any per-call config. Operators edit it in
the manager dashboard; customers only see the resulting SLA states.
"""
from __future__ import annotations

import uuid

from sqlalchemy import ForeignKey, Integer, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class SlaPolicy(Base, TimestampMixin):
    __tablename__ = "sla_policies"
    __table_args__ = (UniqueConstraint("tenant_id", name="uq_sla_policy_tenant"),)

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    # Remediation window per severity, in hours. 0 = untracked (no SLA).
    critical_hours: Mapped[int] = mapped_column(Integer, nullable=False, server_default="24")
    high_hours: Mapped[int] = mapped_column(Integer, nullable=False, server_default="72")
    medium_hours: Mapped[int] = mapped_column(Integer, nullable=False, server_default="168")
    low_hours: Mapped[int] = mapped_column(Integer, nullable=False, server_default="720")
    info_hours: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")

"""
integration.py — a tenant's notification integration config (email / Slack / Jira).

One row per (tenant, kind). Non-secret fields live in `config` (JSONB); the single
secret per kind (SMTP password / Slack webhook / Jira API token) is stored in
`secret_enc`, encrypted at rest via credential_crypto (never returned to the UI —
only a `has_secret` flag). Operators manage these in the manager dashboard; the
customer portal only sees which integrations are configured.
"""
from __future__ import annotations

import uuid

from sqlalchemy import Boolean, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class Integration(Base, TimestampMixin):
    __tablename__ = "integrations"
    __table_args__ = (UniqueConstraint("tenant_id", "kind", name="uq_integration_tenant_kind"),)

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    kind: Mapped[str] = mapped_column(String(16), nullable=False)   # email | slack | jira
    config: Mapped[dict] = mapped_column(JSONB, nullable=False, server_default="{}")
    secret_enc: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="true")

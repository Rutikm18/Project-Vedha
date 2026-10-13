"""Notification rules: which events notify, and through which channels

* notification_rules — one row per (tenant, event). A tenant with no row for an
  event uses that event's default (app.services.notification_rules), so existing
  tenants behave exactly as before until an operator changes a rule.

Revision ID: 0055
Revises: 0054
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0055"
down_revision: Union[str, None] = "0054"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "notification_rules",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True,
                  server_default=sa.text("gen_random_uuid()")),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False),
        sa.Column("event_key", sa.String(48), nullable=False),
        sa.Column("enabled", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("channels", postgresql.JSONB(), nullable=False,
                  server_default=sa.text("'[]'::jsonb")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text("now()")),
        sa.UniqueConstraint("tenant_id", "event_key", name="uq_notification_rule_tenant_event"),
    )
    op.create_index("ix_notification_rules_tenant_id", "notification_rules", ["tenant_id"])


def downgrade() -> None:
    op.drop_index("ix_notification_rules_tenant_id", table_name="notification_rules")
    op.drop_table("notification_rules")

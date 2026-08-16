"""Integrations — per-tenant notification config (email / Slack / Jira).

One row per (tenant, kind). Non-secret fields in `config` (JSONB); the single
secret per kind in `secret_enc` (encrypted at rest via credential_crypto).

Revision ID: 0031
Revises: 0030
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0031"
down_revision: Union[str, None] = "0030"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "integrations",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"),
                  primary_key=True),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False),
        sa.Column("kind", sa.String(length=16), nullable=False),
        sa.Column("config", postgresql.JSONB(astext_type=sa.Text()), server_default="{}",
                  nullable=False),
        sa.Column("secret_enc", sa.String(length=2048), nullable=True),
        sa.Column("enabled", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"),
                  nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"),
                  nullable=False),
        sa.UniqueConstraint("tenant_id", "kind", name="uq_integration_tenant_kind"),
    )
    op.create_index("ix_integrations_tenant_id", "integrations", ["tenant_id"])


def downgrade() -> None:
    op.drop_index("ix_integrations_tenant_id", table_name="integrations")
    op.drop_table("integrations")

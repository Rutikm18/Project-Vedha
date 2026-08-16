"""SLA policies — per-tenant custom remediation windows (hours per severity).

One row per tenant; absence means the env defaults apply. services/sla.py resolves
this into its per-severity `windows` map.

Revision ID: 0030
Revises: 0029
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0030"
down_revision: Union[str, None] = "0029"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "sla_policies",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"),
                  primary_key=True),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False),
        sa.Column("critical_hours", sa.Integer(), server_default="24", nullable=False),
        sa.Column("high_hours", sa.Integer(), server_default="72", nullable=False),
        sa.Column("medium_hours", sa.Integer(), server_default="168", nullable=False),
        sa.Column("low_hours", sa.Integer(), server_default="720", nullable=False),
        sa.Column("info_hours", sa.Integer(), server_default="0", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"),
                  nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"),
                  nullable=False),
        sa.UniqueConstraint("tenant_id", name="uq_sla_policy_tenant"),
    )
    op.create_index("ix_sla_policies_tenant_id", "sla_policies", ["tenant_id"])


def downgrade() -> None:
    op.drop_index("ix_sla_policies_tenant_id", table_name="sla_policies")
    op.drop_table("sla_policies")

"""Remediation plans — cached, OS-specific, structured remediation for a finding.

One row per (finding_id, os). `source` is "ai" or "deterministic_kb"; `reviewed`
gates whether an AI plan may reach the customer portal. `plan` holds the
structured schema (steps/verification/effort/…).

Revision ID: 0028
Revises: 0027
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0028"
down_revision: Union[str, None] = "0027"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "remediation_plans",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"),
                  primary_key=True),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False),
        sa.Column("engagement_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("engagements.id", ondelete="CASCADE"), nullable=False),
        sa.Column("finding_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("findings.id", ondelete="CASCADE"), nullable=False),
        sa.Column("os", sa.String(length=16), nullable=False),
        sa.Column("plan", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("source", sa.String(length=16), nullable=False),
        sa.Column("model", sa.String(length=100), nullable=True),
        sa.Column("reviewed", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.Column("generated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"),
                  nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"),
                  nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"),
                  nullable=False),
        sa.UniqueConstraint("finding_id", "os", name="uq_remediation_finding_os"),
    )
    op.create_index("ix_remediation_plans_tenant_id", "remediation_plans", ["tenant_id"])
    op.create_index("ix_remediation_plans_engagement_id", "remediation_plans", ["engagement_id"])
    op.create_index("ix_remediation_plans_finding_id", "remediation_plans", ["finding_id"])


def downgrade() -> None:
    op.drop_index("ix_remediation_plans_finding_id", table_name="remediation_plans")
    op.drop_index("ix_remediation_plans_engagement_id", table_name="remediation_plans")
    op.drop_index("ix_remediation_plans_tenant_id", table_name="remediation_plans")
    op.drop_table("remediation_plans")

"""Customer portal foundation (Part 2, Phase 0): client role, engagement↔agent
assignment, user↔engagement scoping, and customer scan requests.

Revision ID: 0023
Revises: 0022
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

revision: str = "0023"
down_revision: Union[str, None] = "0022"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. New 'client' value on the userrole enum (customer-portal login). PG 12+
    #    permits ADD VALUE inside a migration transaction; the value is not used
    #    within this migration.
    op.execute("ALTER TYPE userrole ADD VALUE IF NOT EXISTS 'client'")

    # 2. One agent serves an engagement.
    op.add_column(
        "engagements",
        sa.Column("assigned_agent_id", UUID(as_uuid=True),
                  sa.ForeignKey("agents.id", ondelete="SET NULL"), nullable=True),
    )
    op.create_index("ix_engagements_assigned_agent_id", "engagements", ["assigned_agent_id"])

    # 3. Client login → exactly one engagement (portal scoping boundary).
    op.add_column(
        "users",
        sa.Column("client_engagement_id", UUID(as_uuid=True),
                  sa.ForeignKey("engagements.id", ondelete="SET NULL"), nullable=True),
    )
    op.create_index("ix_users_client_engagement_id", "users", ["client_engagement_id"])

    # 4. Customer-initiated, operator-approved scan requests.
    op.create_table(
        "scan_requests",
        sa.Column("id", UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), primary_key=True),
        sa.Column("tenant_id", UUID(as_uuid=True), sa.ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False),
        sa.Column("engagement_id", UUID(as_uuid=True), sa.ForeignKey("engagements.id", ondelete="CASCADE"), nullable=False),
        sa.Column("requested_by", UUID(as_uuid=True), nullable=True),
        sa.Column("scan_type", sa.String(length=32), server_default="vuln_scan", nullable=False),
        sa.Column("status", sa.String(length=16), server_default="pending", nullable=False),
        sa.Column("note", sa.Text(), nullable=True),
        sa.Column("scan_job_id", UUID(as_uuid=True), sa.ForeignKey("scan_jobs.id", ondelete="SET NULL"), nullable=True),
        sa.Column("requested_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("reviewed_by", UUID(as_uuid=True), nullable=True),
        sa.Column("reviewed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("review_reason", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )
    op.create_index("ix_scan_requests_tenant_id", "scan_requests", ["tenant_id"])
    op.create_index("ix_scan_requests_engagement_id", "scan_requests", ["engagement_id"])
    op.create_index("ix_scan_requests_status", "scan_requests", ["status"])


def downgrade() -> None:
    op.drop_index("ix_scan_requests_status", table_name="scan_requests")
    op.drop_index("ix_scan_requests_engagement_id", table_name="scan_requests")
    op.drop_index("ix_scan_requests_tenant_id", table_name="scan_requests")
    op.drop_table("scan_requests")

    op.drop_index("ix_users_client_engagement_id", table_name="users")
    op.drop_column("users", "client_engagement_id")

    op.drop_index("ix_engagements_assigned_agent_id", table_name="engagements")
    op.drop_column("engagements", "assigned_agent_id")
    # Note: Postgres cannot drop an enum value, so 'client' remains on userrole
    # after downgrade (harmless — no rows reference it once the column is dropped).

"""Approval-gated safe active-validation requests (P3).

Revision ID: 0022
Revises: 0021
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB, UUID

revision: str = "0022"
down_revision: Union[str, None] = "0021"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "validation_requests",
        sa.Column("id", UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), primary_key=True),
        sa.Column("engagement_id", UUID(as_uuid=True), sa.ForeignKey("engagements.id", ondelete="CASCADE"), nullable=False),
        sa.Column("finding_id", UUID(as_uuid=True), sa.ForeignKey("findings.id", ondelete="SET NULL"), nullable=True),
        sa.Column("target_ip", sa.String(length=45), nullable=False),
        sa.Column("target_port", sa.Integer(), nullable=True),
        sa.Column("check_kind", sa.String(length=32), nullable=False),
        sa.Column("status", sa.String(length=16), server_default="pending", nullable=False),
        sa.Column("outcome", sa.String(length=16), nullable=True),
        sa.Column("job_id", UUID(as_uuid=True), nullable=True),
        sa.Column("result", JSONB(), nullable=True),
        sa.Column("requested_by", sa.String(length=255), nullable=True),
        sa.Column("requested_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("reviewed_by", sa.String(length=255), nullable=True),
        sa.Column("reviewed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )
    op.create_index("ix_validation_requests_engagement_id", "validation_requests", ["engagement_id"])
    op.create_index("ix_validation_requests_finding_id", "validation_requests", ["finding_id"])
    op.create_index("ix_validation_requests_status", "validation_requests", ["status"])


def downgrade() -> None:
    op.drop_index("ix_validation_requests_status", table_name="validation_requests")
    op.drop_index("ix_validation_requests_finding_id", table_name="validation_requests")
    op.drop_index("ix_validation_requests_engagement_id", table_name="validation_requests")
    op.drop_table("validation_requests")

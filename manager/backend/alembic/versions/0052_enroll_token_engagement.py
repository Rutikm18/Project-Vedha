"""Bind enrolment tokens to an engagement (Fleet → Add agent).

A token can now name the engagement it installs an agent for instead of a
pre-built Site. The Site is created when the agent enrols, from the engagement's
scope at that moment, and the agent is assigned to the engagement — the same
result as approving a device code in the portal, without the code.

Revision ID: 0052
Revises: 0051
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0052"
down_revision: Union[str, None] = "0051"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "probe_enrollment_tokens",
        sa.Column("engagement_id", postgresql.UUID(as_uuid=True), nullable=True),
    )
    op.create_foreign_key(
        "fk_probe_enrollment_tokens_engagement_id",
        "probe_enrollment_tokens", "engagements",
        ["engagement_id"], ["id"], ondelete="CASCADE",
    )
    op.create_index(
        "ix_probe_enrollment_tokens_engagement_id", "probe_enrollment_tokens", ["engagement_id"],
    )
    op.alter_column("probe_enrollment_tokens", "site_id", existing_type=postgresql.UUID(as_uuid=True), nullable=True)
    op.create_check_constraint(
        "ck_probe_enrollment_tokens_target",
        "probe_enrollment_tokens",
        "site_id IS NOT NULL OR engagement_id IS NOT NULL",
    )


def downgrade() -> None:
    op.drop_constraint("ck_probe_enrollment_tokens_target", "probe_enrollment_tokens", type_="check")
    # Engagement-only tokens have no Site; they cannot survive the old NOT NULL.
    op.execute("DELETE FROM probe_enrollment_tokens WHERE site_id IS NULL")
    op.alter_column("probe_enrollment_tokens", "site_id", existing_type=postgresql.UUID(as_uuid=True), nullable=False)
    op.drop_index("ix_probe_enrollment_tokens_engagement_id", table_name="probe_enrollment_tokens")
    op.drop_constraint("fk_probe_enrollment_tokens_engagement_id", "probe_enrollment_tokens", type_="foreignkey")
    op.drop_column("probe_enrollment_tokens", "engagement_id")

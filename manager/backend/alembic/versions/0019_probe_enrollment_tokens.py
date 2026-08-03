"""Add pre-authorized, Site-bound probe enrollment tokens.

Lets a probe auto-enroll without an operator user_code step while inheriting a
bounded Site policy. Only the SHA-256 hash of the ``vet_...`` token is stored.

Revision ID: 0019
Revises: 0018
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0019"
down_revision: Union[str, None] = "0018"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "probe_enrollment_tokens",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("site_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(120), nullable=False),
        sa.Column("token_hash", sa.String(64), nullable=False),
        sa.Column("token_prefix", sa.String(24), nullable=False),
        sa.Column("max_uses", sa.Integer(), server_default="1", nullable=False),
        sa.Column("uses", sa.Integer(), server_default="0", nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("last_used_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_by", sa.String(255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["site_id"], ["probe_sites.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("token_hash", name="uq_probe_enroll_token_hash"),
    )
    op.create_index("ix_probe_enrollment_tokens_tenant_id", "probe_enrollment_tokens", ["tenant_id"])
    op.create_index("ix_probe_enrollment_tokens_site_id", "probe_enrollment_tokens", ["site_id"])
    op.create_index("ix_probe_enrollment_tokens_token_prefix", "probe_enrollment_tokens", ["token_prefix"])
    op.create_index("ix_probe_enrollment_tokens_expires_at", "probe_enrollment_tokens", ["expires_at"])


def downgrade() -> None:
    op.drop_index("ix_probe_enrollment_tokens_expires_at", table_name="probe_enrollment_tokens")
    op.drop_index("ix_probe_enrollment_tokens_token_prefix", table_name="probe_enrollment_tokens")
    op.drop_index("ix_probe_enrollment_tokens_site_id", table_name="probe_enrollment_tokens")
    op.drop_index("ix_probe_enrollment_tokens_tenant_id", table_name="probe_enrollment_tokens")
    op.drop_table("probe_enrollment_tokens")

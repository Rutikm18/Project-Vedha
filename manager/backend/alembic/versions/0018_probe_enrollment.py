"""Add Manager-approved device-key probe enrollment and Site policy.

Revision ID: 0018
Revises: 0017
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0018"
down_revision: Union[str, None] = "0017"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "probe_sites",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("location", sa.String(255), nullable=True),
        sa.Column("status", sa.String(16), server_default="active", nullable=False),
        sa.Column("authorized_cidrs", postgresql.ARRAY(sa.Text()), server_default="{}", nullable=False),
        sa.Column("excluded_cidrs", postgresql.ARRAY(sa.Text()), server_default="{}", nullable=False),
        sa.Column("approved_capabilities", postgresql.ARRAY(sa.Text()), server_default="{}", nullable=False),
        sa.Column("max_targets", sa.Integer(), server_default="4096", nullable=False),
        sa.Column("max_job_seconds", sa.Integer(), server_default="7200", nullable=False),
        sa.Column("max_rate_pps", sa.Integer(), server_default="1000", nullable=False),
        sa.Column("policy_version", sa.BigInteger(), server_default="1", nullable=False),
        sa.Column("update_channel", sa.String(32), server_default="stable", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("tenant_id", "name", name="uq_probe_site_tenant_name"),
    )
    op.create_index("ix_probe_sites_tenant_id", "probe_sites", ["tenant_id"])

    op.add_column("agents", sa.Column("site_id", postgresql.UUID(as_uuid=True), nullable=True))
    op.add_column("agents", sa.Column("lifecycle_status", sa.String(24), server_default="active", nullable=False))
    op.add_column("agents", sa.Column("signing_public_key", sa.String(64), nullable=True))
    op.add_column("agents", sa.Column("signing_key_fingerprint", sa.String(64), nullable=True))
    op.add_column("agents", sa.Column("credential_generation", sa.Integer(), server_default="0", nullable=False))
    op.add_column("agents", sa.Column("approved_capabilities", postgresql.ARRAY(sa.Text()), server_default="{}", nullable=False))
    op.add_column("agents", sa.Column("approved_networks", postgresql.ARRAY(sa.Text()), server_default="{}", nullable=False))
    op.add_column("agents", sa.Column("agent_version", sa.String(64), nullable=True))
    op.add_column("agents", sa.Column("installer_version", sa.String(64), nullable=True))
    op.add_column("agents", sa.Column("build_digest", sa.String(128), nullable=True))
    op.create_foreign_key("fk_agents_site_id", "agents", "probe_sites", ["site_id"], ["id"], ondelete="RESTRICT")
    op.create_index("ix_agents_site_id", "agents", ["site_id"])
    op.create_index("ix_agents_signing_key_fingerprint", "agents", ["signing_key_fingerprint"])
    op.create_index(
        "uq_agents_device_signing_fingerprint",
        "agents",
        ["signing_key_fingerprint"],
        unique=True,
        postgresql_where=sa.text("signing_key_fingerprint IS NOT NULL"),
    )

    op.create_table(
        "probe_enrollment_requests",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("state", sa.String(24), server_default="awaiting_approval", nullable=False),
        sa.Column("version", sa.Integer(), server_default="1", nullable=False),
        sa.Column("device_secret_hash", sa.String(64), nullable=False),
        sa.Column("user_code_hash", sa.String(64), nullable=False),
        sa.Column("signing_public_key", sa.String(64), nullable=False),
        sa.Column("encryption_public_key", sa.String(64), nullable=False),
        sa.Column("signing_key_fingerprint", sa.String(64), nullable=False),
        sa.Column("nonce", sa.String(64), nullable=False),
        sa.Column("activation_challenge", sa.String(128), nullable=True),
        sa.Column("hostname_hint", sa.String(255), nullable=True),
        sa.Column("platform", sa.String(64), nullable=False),
        sa.Column("architecture", sa.String(64), nullable=False),
        sa.Column("agent_version", sa.String(64), nullable=False),
        sa.Column("installer_version", sa.String(64), nullable=False),
        sa.Column("build_digest", sa.String(128), nullable=False),
        sa.Column("reported_capabilities", postgresql.ARRAY(sa.Text()), server_default="{}", nullable=False),
        sa.Column("source_ip", sa.String(45), nullable=True),
        sa.Column("poll_count", sa.Integer(), server_default="0", nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("approved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("activated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("denied_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("site_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("agent_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("assigned_name", sa.String(255), nullable=True),
        sa.Column("approved_by", sa.String(255), nullable=True),
        sa.Column("denied_reason", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["agent_id"], ["agents.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["site_id"], ["probe_sites.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_code_hash"),
    )
    for column in ("state", "user_code_hash", "signing_key_fingerprint", "expires_at", "tenant_id", "site_id", "agent_id"):
        op.create_index(f"ix_probe_enrollment_requests_{column}", "probe_enrollment_requests", [column])

    op.create_table(
        "agent_credentials",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("agent_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("generation", sa.Integer(), nullable=False),
        sa.Column("refresh_secret_hash", sa.String(64), nullable=False),
        sa.Column("signing_public_key", sa.String(64), nullable=False),
        sa.Column("signing_key_fingerprint", sa.String(64), nullable=False),
        sa.Column("issued_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_used_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_nonce", sa.String(128), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["agent_id"], ["agents.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("agent_id", "generation", name="uq_agent_credential_generation"),
    )
    op.create_index("ix_agent_credentials_agent_id", "agent_credentials", ["agent_id"])
    op.create_index("ix_agent_credentials_signing_key_fingerprint", "agent_credentials", ["signing_key_fingerprint"])
    op.create_index("ix_agent_credentials_expires_at", "agent_credentials", ["expires_at"])


def downgrade() -> None:
    op.drop_table("agent_credentials")
    op.drop_table("probe_enrollment_requests")
    op.drop_index("ix_agents_signing_key_fingerprint", table_name="agents")
    op.drop_index("uq_agents_device_signing_fingerprint", table_name="agents")
    op.drop_index("ix_agents_site_id", table_name="agents")
    op.drop_constraint("fk_agents_site_id", "agents", type_="foreignkey")
    for column in (
        "build_digest", "installer_version", "agent_version", "approved_networks",
        "approved_capabilities", "credential_generation", "signing_key_fingerprint",
        "signing_public_key", "lifecycle_status", "site_id",
    ):
        op.drop_column("agents", column)
    op.drop_table("probe_sites")

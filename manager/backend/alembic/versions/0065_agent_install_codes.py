"""Agent install codes — one-time opaque codes for the zero-knowledge Windows install

A new table `agent_install_codes`: an opaque `vac_...` code the operator hands a
client. It stores NO enrolment secret — it authorises minting exactly one `vet_`
token, once, at redeem time (see app/routers/agent_distribution.py redeem). Only
the SHA-256 of the raw code is stored; single-use redeem + the minted token's
`max_uses=1` bind the whole install to the first machine that redeems.

Additive and nullable throughout; nothing existing changes. Downgrade drops the
table. Portable across Postgres (prod) and SQLite.

Revision ID: 0065
Revises: 0064

Renumbered from 0063 on merge to main: main already defined 0063
(attack_assessment_snapshots) and 0064 (environment_assessments) while this was
developed in parallel, so it now chains after 0064 to keep a single alembic head.
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0065"
down_revision: Union[str, None] = "0064"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _uuid_type(bind):
    return postgresql.UUID(as_uuid=True) if bind.dialect.name == "postgresql" else sa.String(36)


def upgrade() -> None:
    bind = op.get_bind()
    uuid_type = _uuid_type(bind)
    uuid_default = sa.text("gen_random_uuid()") if bind.dialect.name == "postgresql" else None
    op.create_table(
        "agent_install_codes",
        sa.Column("id", uuid_type, primary_key=True, server_default=uuid_default),
        sa.Column("tenant_id", uuid_type, sa.ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False),
        sa.Column("engagement_id", uuid_type, sa.ForeignKey("engagements.id", ondelete="CASCADE"), nullable=True),
        sa.Column("site_id", uuid_type, sa.ForeignKey("probe_sites.id", ondelete="RESTRICT"), nullable=True),
        sa.Column("name", sa.String(120), nullable=False),
        sa.Column("code_hash", sa.String(64), nullable=False),
        sa.Column("code_prefix", sa.String(24), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("redeemed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("redeemed_ip", sa.String(45), nullable=True),
        sa.Column("minted_token_id", uuid_type,
                  sa.ForeignKey("probe_enrollment_tokens.id", ondelete="SET NULL"), nullable=True),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_by", sa.String(255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("code_hash", name="uq_agent_install_code_hash"),
        sa.CheckConstraint(
            "site_id IS NOT NULL OR engagement_id IS NOT NULL",
            name="ck_agent_install_codes_target",
        ),
    )
    for column in ("tenant_id", "engagement_id", "site_id", "code_prefix", "expires_at", "minted_token_id"):
        op.create_index(f"ix_agent_install_codes_{column}", "agent_install_codes", [column])


def downgrade() -> None:
    for column in ("minted_token_id", "expires_at", "code_prefix", "site_id", "engagement_id", "tenant_id"):
        op.drop_index(f"ix_agent_install_codes_{column}", table_name="agent_install_codes")
    op.drop_table("agent_install_codes")

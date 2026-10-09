"""Attack-path history (attack-path plan, dashboard phase 3)

* attack_path_snapshots — the headline numbers of every attack-path computation, so the
  dashboard can say whether crown jewels reachable is changing. `attack_path_analyses` keeps
  only the latest analysis, which cannot.

Purely additive: nothing reads it until a recompute writes it, and downgrading drops only history.

Revision ID: 0061
Revises: 0060
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0061"
down_revision: Union[str, None] = "0060"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "attack_path_snapshots",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("engagement_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("engagements.id", ondelete="CASCADE"), nullable=False),
        sa.Column("computed_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("trigger", sa.String(16), nullable=False, server_default="manual"),
        sa.Column("state", sa.String(16), nullable=False),
        sa.Column("jewels_total", sa.Integer(), nullable=True),
        sa.Column("jewels_reachable", sa.Integer(), nullable=True),
        sa.Column("jewels_exposed", sa.Integer(), nullable=True),
        sa.Column("fix_set_size", sa.Integer(), nullable=True),
        sa.Column("entry_points", sa.Integer(), nullable=True),
        sa.Column("path_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("assets_seen", sa.Integer(), nullable=True),
        sa.Column("coverage", sa.String(16), nullable=True),
    )
    op.create_index("ix_attack_path_snapshots_engagement_time", "attack_path_snapshots",
                    ["engagement_id", "computed_at"])


def downgrade() -> None:
    op.drop_index("ix_attack_path_snapshots_engagement_time", table_name="attack_path_snapshots")
    op.drop_table("attack_path_snapshots")

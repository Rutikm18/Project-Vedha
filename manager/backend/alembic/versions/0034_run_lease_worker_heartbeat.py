"""Stage 2b: DetectionRun lease + worker heartbeat (precise liveness).

Two additive changes that let the system OBSERVE its own liveness instead of
inferring it:

  * detection_runs.lease_expires_at — a per-run lease. A run still RUNNING past its
    lease was abandoned by a crashed worker; the outbox reaper fails it precisely
    (replacing the coarse started_at-age heuristic). Nullable, so historical runs
    simply fall back to the age heuristic.
  * worker_heartbeats — one row per worker process, updated every tick. A stale
    heartbeat means the detection worker is down, which campaign-progress uses to
    tell "worker is down" apart from "worker is busy on a backlog".

Both additive; no backfill required.

Revision ID: 0034
Revises: 0033
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0034"
down_revision: Union[str, None] = "0033"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "detection_runs",
        sa.Column("lease_expires_at", sa.DateTime(timezone=True), nullable=True),
    )
    # Reaper query: WHERE status='running' AND lease_expires_at < now  → index it.
    op.create_index("ix_detection_runs_lease", "detection_runs",
                    ["status", "lease_expires_at"])

    op.create_table(
        "worker_heartbeats",
        sa.Column("worker_name", sa.String(length=128), primary_key=True),
        sa.Column("last_beat_at", sa.DateTime(timezone=True),
                  server_default=sa.text("now()"), nullable=False),
        sa.Column("meta", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True),
                  server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True),
                  server_default=sa.text("now()"), nullable=False),
    )
    op.create_index("ix_worker_heartbeats_last_beat", "worker_heartbeats", ["last_beat_at"])


def downgrade() -> None:
    op.drop_index("ix_worker_heartbeats_last_beat", table_name="worker_heartbeats")
    op.drop_table("worker_heartbeats")
    op.drop_index("ix_detection_runs_lease", table_name="detection_runs")
    op.drop_column("detection_runs", "lease_expires_at")

"""Scan-request targets + intensity — the rich customer scan request.

Adds two nullable columns to scan_requests so a customer can ask for specific
in-scope targets at a chosen intensity (the operator still approves every one):

  * targets   JSONB   — list of validated IP/CIDR/range strings, each proven
                        subset of the engagement scope at request time.
  * intensity VARCHAR — 'light' | 'standard' | 'deep' (nullable = use-case default).

Both nullable with no server default, so existing rows (which targeted the whole
scope at default intensity) keep working unchanged.

Revision ID: 0027
Revises: 0026
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0027"
down_revision: Union[str, None] = "0026"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "scan_requests",
        sa.Column("targets", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    )
    op.add_column(
        "scan_requests",
        sa.Column("intensity", sa.String(length=16), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("scan_requests", "intensity")
    op.drop_column("scan_requests", "targets")

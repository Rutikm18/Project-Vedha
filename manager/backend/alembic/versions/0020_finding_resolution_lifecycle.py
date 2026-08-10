"""Finding resolution lifecycle: coverage-gated auto-resolution columns.

Revision ID: 0020
Revises: 0019
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

revision: str = "0020"
down_revision: Union[str, None] = "0019"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("findings", sa.Column("resolution_miss_count", sa.Integer(), nullable=False, server_default="0"))
    op.add_column("findings", sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("findings", sa.Column("resolution_method", sa.String(length=16), nullable=True))
    op.add_column("findings", sa.Column("resolution_run_id", UUID(as_uuid=True), nullable=True))
    op.add_column("findings", sa.Column("reopened_count", sa.Integer(), nullable=False, server_default="0"))
    op.add_column("findings", sa.Column("detected_db_version", sa.String(length=128), nullable=True))
    op.create_foreign_key(
        "fk_findings_resolution_run", "findings", "detection_runs",
        ["resolution_run_id"], ["id"], ondelete="SET NULL",
    )


def downgrade() -> None:
    op.drop_constraint("fk_findings_resolution_run", "findings", type_="foreignkey")
    for col in (
        "detected_db_version", "reopened_count", "resolution_run_id",
        "resolution_method", "resolved_at", "resolution_miss_count",
    ):
        op.drop_column("findings", col)

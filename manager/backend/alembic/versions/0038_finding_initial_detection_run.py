"""Record the detection run that first created each finding.

The existing ``detection_run_id`` advances whenever a later run reaffirms a
finding, so it cannot truthfully answer which scan originally discovered the
issue.  This nullable, immutable provenance pointer fixes new records without
guessing a value for historical rows.

Revision ID: 0038
Revises: 0037
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

revision: str = "0038"
down_revision: Union[str, None] = "0037"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "findings",
        sa.Column("initial_detection_run_id", UUID(as_uuid=True), nullable=True),
    )
    op.create_foreign_key(
        "fk_findings_initial_detection_run",
        "findings",
        "detection_runs",
        ["initial_detection_run_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_index(
        "ix_findings_initial_detection_run_id",
        "findings",
        ["initial_detection_run_id"],
    )


def downgrade() -> None:
    op.drop_index("ix_findings_initial_detection_run_id", table_name="findings")
    op.drop_constraint(
        "fk_findings_initial_detection_run", "findings", type_="foreignkey"
    )
    op.drop_column("findings", "initial_detection_run_id")

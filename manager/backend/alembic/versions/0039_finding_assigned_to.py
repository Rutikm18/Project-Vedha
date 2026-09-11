"""finding ownership: assigned_to

A finding with no owner is a problem in a list, not a problem in someone's queue.
SLA windows and remediation recipes already existed; nothing recorded WHO is
responsible for acting on a finding, so nothing could answer "what is on my
plate" or "which team is behind".

SCOPE NOTE: only this one column is new. `resolved_at`, `resolution_method` and
`resolution_run_id` already exist (written by the coverage-gated auto-resolver),
as do `first_seen`/`last_seen`. MTTR therefore needs no schema change at all —
it was a computation gap, not a data gap.

Nullable by design: unassigned is the normal state. Forcing an owner would either
invent accountability or block triage, and a NOT NULL backfill would have to
fabricate one for every historical finding.

ondelete=SET NULL rather than CASCADE: when a user leaves, their findings must
survive. Cascading would delete security history as a side effect of an HR event
— the kind of data loss nobody discovers until they need the audit trail.

Revision ID: 0039
Revises: 0038
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0039"
down_revision: Union[str, None] = "0038"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "findings",
        sa.Column("assigned_to", postgresql.UUID(as_uuid=True), nullable=True),
    )
    # "What is on my plate" is a per-owner query; without this it table-scans
    # findings, which is the largest table in the schema.
    op.create_index("ix_findings_assigned_to", "findings", ["assigned_to"])
    op.create_foreign_key(
        "fk_findings_assigned_to_users", "findings", "users",
        ["assigned_to"], ["id"], ondelete="SET NULL",
    )


def downgrade() -> None:
    op.drop_constraint("fk_findings_assigned_to_users", "findings", type_="foreignkey")
    op.drop_index("ix_findings_assigned_to", table_name="findings")
    op.drop_column("findings", "assigned_to")

"""scan_result_chunks.complete — separate "evidence I hold" from "host is done"

A chunk used to mean both things at once, because it was only ever written when
a host finished the whole pipeline. committed_hosts() leans on that: it is the
probe's resume list, and a host in it is not rescanned.

Committing evidence at STAGE boundaries breaks the conflation. Without this
column a probe killed during the port sweep would commit mid-scan evidence, and
the retry would then skip every host it had merely DISCOVERED — delivering a
liveness fact and calling the host scanned. That is strictly worse than the data
loss it was meant to prevent.

Partial chunks stay full evidence: they are merged into the final result and
promoted if the job is abandoned. They simply never suppress a rescan.

DEFAULT TRUE, and backfilled TRUE: every existing row was written by the old
complete-hosts-only path, and an older probe that omits the field on the wire
must keep behaving exactly as it does today. Only a probe that explicitly says
"this is partial" gets the new semantics.

Revision ID: 0042
Revises: 0041
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0042"
down_revision: Union[str, None] = "0041"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "scan_result_chunks",
        sa.Column("complete", sa.Boolean(), nullable=False,
                  server_default=sa.text("true")),
    )
    # Partial-index the resume lookup: committed_hosts() only ever asks for
    # complete rows, and a job's partial chunks can outnumber them.
    op.create_index(
        "ix_result_chunk_job_complete",
        "scan_result_chunks", ["job_id"],
        postgresql_where=sa.text("complete"),
    )


def downgrade() -> None:
    op.drop_index("ix_result_chunk_job_complete", table_name="scan_result_chunks")
    op.drop_column("scan_result_chunks", "complete")

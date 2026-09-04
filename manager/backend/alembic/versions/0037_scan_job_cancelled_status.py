"""scan jobs gain a terminal `cancelled` status

An operator could start work but never stop it. The only way out of a running
job was to wait for it to finish or for its lease to expire into `failed` — so a
scan aimed at the wrong target, or one saturating a fragile network, kept running
and the probe stayed busy behind it.

`cancelled` is deliberately NOT `failed`. A failure is the system's fault: it is
worth retrying, alerting on, and counting against reliability. A cancel is a
human decision and must do none of those things. Keeping them apart is what lets
the dashboard say "you stopped this" instead of "this broke", and keeps operator
housekeeping out of the failure metrics.

Postgres enum values cannot be added inside a transaction on older servers, and
cannot be REMOVED at all. The downgrade therefore rewrites any surviving
`cancelled` rows to `failed` rather than attempting to drop the label — lossy in
the sense that a cancel becomes indistinguishable from a failure, but that is the
only reversible option Postgres offers, and it keeps the column readable by the
older enum.

Revision ID: 0037
Revises: 0036
"""
from typing import Sequence, Union

from alembic import op

revision: str = "0037"
down_revision: Union[str, None] = "0036"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # IF NOT EXISTS keeps this idempotent if a re-run or a partially applied
    # deploy already added the label.
    op.execute("ALTER TYPE scanjobstatus ADD VALUE IF NOT EXISTS 'cancelled'")


def downgrade() -> None:
    # The label cannot be dropped from a Postgres enum, so collapse the rows that
    # use it back onto a value the previous schema understands.
    op.execute(
        "UPDATE scan_jobs SET status = 'failed' WHERE status = 'cancelled'"
    )

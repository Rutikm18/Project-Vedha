"""agents gain a `paused` status — refusing work is not the same as idle

A probe stops claiming jobs once its result spool hits the high-water mark:
taking on more work would only produce more results it cannot deliver. That
back-pressure was invisible. The probe kept heartbeating `online`, so the fleet
view showed a healthy idle probe, and the manager kept dispatching to it —
push_job and the enqueue eligibility query both select on `online`.

`paused` is deliberately NOT `offline`. An offline probe is unreachable and its
jobs should be reaped and requeued elsewhere. A paused one is connected,
healthy, and will resume the moment its uploads drain — reaping its work would
destroy exactly the results that are blocking it.

Adding the label is enough to fix dispatch: both paths already filter on
`online`, so neither needs to change.

Postgres enum values cannot be added inside a transaction on older servers and
cannot be REMOVED at all, so the downgrade rewrites surviving `paused` rows to
`online` rather than attempting to drop the label — the same trade 0037 made
for scan_jobs.cancelled.

Revision ID: 0043
Revises: 0042
"""
from typing import Sequence, Union

from alembic import op

revision: str = "0043"
down_revision: Union[str, None] = "0042"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # IF NOT EXISTS keeps this idempotent across a re-run or partial deploy.
    op.execute("ALTER TYPE agentstatus ADD VALUE IF NOT EXISTS 'paused'")


def downgrade() -> None:
    # The label cannot be dropped, so collapse the rows onto a value the older
    # schema understands. `online` rather than `offline`: a paused probe IS
    # reachable, and calling it offline would have the reaper requeue its jobs.
    op.execute("UPDATE agents SET status = 'online' WHERE status = 'paused'")

"""engagement lifecycle: add 'ongoing' and 'running' states

The engagement lifecycle was draft → active → paused → completed, surfaced in the
UI as Planning / Active / Paused / Completed. Operators asked for the assessment
phase to be expressible in the terms they actually use when reporting status:

    Planning → Ongoing → Running → Completed

'ongoing' means the assessment is underway (people are working on it) and
'running' means active scanning is the current phase. They are distinct
operator-set states, which is why they are stored rather than derived; the
platform ALSO shows observed live scan activity beside the status, so a stored
'running' is never mistaken for evidence that a scan is executing right now.

PG 12+ permits ALTER TYPE ... ADD VALUE inside a migration transaction, and the
new values are not written by this migration — the same pattern 0023 used to add
the 'client' user role.

DOWNGRADE IS DELIBERATELY A NO-OP. PostgreSQL cannot drop a value from an enum
type; the only way back is to rewrite the type and every column that uses it,
which would risk data on a rollback that is meant to be safe. Any engagement left
on a new state simply keeps it. This is recorded rather than silently omitted.

Revision ID: 0035
Revises: 0034
"""
from typing import Sequence, Union

from alembic import op

revision: str = "0035"
down_revision: Union[str, None] = "0034"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

_NEW_STATES = ("ongoing", "running")


def upgrade() -> None:
    for value in _NEW_STATES:
        op.execute(f"ALTER TYPE engagementstatus ADD VALUE IF NOT EXISTS '{value}'")


def downgrade() -> None:
    # No-op by design — see the module docstring. Removing an enum value requires
    # recreating the type and rewriting engagements.status, which is not a safe
    # thing to do automatically on a rollback.
    pass

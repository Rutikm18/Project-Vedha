"""Scanner findings no longer claim SOC detection (detection_status 'detected' -> 'unknown').

`findings.detection_status` is the SOC-detection verdict (did the SIEM/EDR see the
attack: detected / prevented / missed). The detection engine stamped every finding it
created as `detected`, meaning only "the scanner found it", so every engagement read
100% detection coverage and no blind spots. The correlator never writes a SOC verdict
back onto a finding, so for engine-managed rows (detection_run_id set) `detected` was
never a validation result: they become `unknown` (not tested). Rows from other paths
are untouched.

Data-only and idempotent. Downgrade is a no-op: the old value carried no information.

Revision ID: 0069
Revises: 0068
"""

from alembic import op

revision = "0069"
down_revision = "0068"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        "UPDATE findings SET detection_status = 'unknown' "
        "WHERE detection_run_id IS NOT NULL AND detection_status = 'detected'"
    )


def downgrade():
    pass

from __future__ import annotations

import uuid
from types import SimpleNamespace

from app.detection.engine_bridge import _apply_regression_reopen
from app.models.enums import FindingStatus


def test_reopen_flips_remediated_to_open_and_flags_regression():
    now = object()
    run_id = uuid.uuid4()
    f = SimpleNamespace(
        status=FindingStatus.remediated, reopened_count=0,
        resolution_miss_count=3, resolved_at="old", resolution_method="auto",
        resolution_run_id=uuid.uuid4(),
        evidence={"cve_id": "CVE-1"}, last_seen=None, detection_run_id=None,
    )
    _apply_regression_reopen(f, run_id, now)

    assert f.status == FindingStatus.open
    assert f.reopened_count == 1
    assert f.resolution_miss_count == 0
    assert f.resolved_at is None
    assert f.resolution_method is None
    assert f.resolution_run_id is None
    assert f.evidence["regression"] is True
    assert f.last_seen is now
    assert f.detection_run_id == run_id

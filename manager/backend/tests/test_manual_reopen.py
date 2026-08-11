from __future__ import annotations

from types import SimpleNamespace

from app.detection.resolution import apply_manual_reopen
from app.models.enums import FindingStatus


def test_manual_reopen_restores_open_and_audits():
    now = object()
    f = SimpleNamespace(status=FindingStatus.remediated, reopened_count=1,
                        resolution_miss_count=2, resolved_at="t", resolution_method="auto",
                        resolution_run_id="r", evidence={"cve_id": "CVE-9"})
    apply_manual_reopen(f, by="alice", now=now)

    assert f.status == FindingStatus.open
    assert f.reopened_count == 2
    assert f.resolution_miss_count == 0
    assert f.resolved_at is None
    assert f.resolution_method is None
    assert f.evidence["reopened_by"] == "alice"

from datetime import datetime, timezone
from types import SimpleNamespace

from app.models.enums import ScanJobStatus
from app.workers.reaper import expire_attempt


def _objects(*, attempts: int, max_attempts: int):
    attempt = SimpleNamespace(status="running", ended_at=None, error=None)
    job = SimpleNamespace(
        status=ScanJobStatus.running,
        attempt_count=attempts,
        max_attempts=max_attempts,
        agent_id="agent",
        lease_expires_at=datetime.now(timezone.utc),
        current_attempt_id="attempt",
        started_at=datetime.now(timezone.utc),
        completed_at=None,
        result={"scan_type": "discovery"},
    )
    return attempt, job


def test_expired_attempt_requeues_with_fence_history_preserved() -> None:
    attempt, job = _objects(attempts=1, max_attempts=3)
    now = datetime.now(timezone.utc)

    retryable = expire_attempt(attempt, job, now)

    assert retryable is True
    assert attempt.status == "expired"
    assert attempt.ended_at == now
    assert job.status == ScanJobStatus.pending
    assert job.agent_id is None
    assert job.current_attempt_id is None
    assert job.started_at is None


def test_expired_attempt_fails_job_when_retry_budget_is_exhausted() -> None:
    attempt, job = _objects(attempts=3, max_attempts=3)
    now = datetime.now(timezone.utc)

    retryable = expire_attempt(attempt, job, now)

    assert retryable is False
    assert attempt.status == "expired"
    assert job.status == ScanJobStatus.failed
    assert job.completed_at == now
    assert "maximum execution attempts" in job.result["error"]

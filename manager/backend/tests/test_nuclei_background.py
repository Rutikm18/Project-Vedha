from __future__ import annotations

import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest

from app.models.enums import ScanJobStatus
from app.routers.vuln_scans import _run_nuclei_and_save
from app.vuln.nuclei import NucleiRunReport, NucleiScanError


class _ScalarResult:
    def __init__(self, value) -> None:
        self._value = value

    def scalar_one_or_none(self):
        return self._value


class _NestedTransaction:
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, traceback) -> bool:
        return False


class _FakeSession:
    def __init__(self, factory: "_SessionFactory") -> None:
        self.factory = factory

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, traceback) -> bool:
        return False

    async def execute(self, statement) -> _ScalarResult:
        return _ScalarResult(self.factory.job)

    def begin_nested(self) -> _NestedTransaction:
        return _NestedTransaction()

    def add(self, value) -> None:
        self.factory.added.append(value)

    async def flush(self) -> None:
        return None

    async def commit(self) -> None:
        self.factory.commits += 1

    async def rollback(self) -> None:
        self.factory.rollbacks += 1


class _SessionFactory:
    def __init__(self) -> None:
        self.job = SimpleNamespace(
            status=ScanJobStatus.pending,
            started_at=None,
            completed_at=None,
            result={"scanner": "nuclei"},
        )
        self.added: list = []
        self.commits = 0
        self.rollbacks = 0

    def __call__(self) -> _FakeSession:
        return _FakeSession(self)


@pytest.mark.asyncio
async def test_fatal_nuclei_error_marks_background_job_failed() -> None:
    sessions = _SessionFactory()
    scanner = SimpleNamespace(
        run_scan=AsyncMock(
            side_effect=NucleiScanError(
                "not_installed",
                "nuclei binary is not installed or is not on PATH",
            )
        ),
        last_run_report=NucleiRunReport(
            "failed",
            findings_count=0,
            reason="not_installed",
        ),
    )
    enrichment = AsyncMock()

    with (
        patch("app.database.AsyncSessionLocal", sessions),
        patch("app.routers.vuln_scans.NucleiScanner", return_value=scanner),
        patch("app.routers.vuln_scans.run_post_scan_enrichment", enrichment),
    ):
        await _run_nuclei_and_save(
            str(uuid.uuid4()),
            str(uuid.uuid4()),
            ["10.0.0.1"],
            ["cves"],
            100,
            60,
        )

    assert sessions.job.status == ScanJobStatus.failed
    assert sessions.job.started_at is not None
    assert sessions.job.completed_at is not None
    assert sessions.job.result["outcome"] == "failed"
    assert sessions.job.result["issues"][0]["code"] == "not_installed"
    assert sessions.commits == 2
    enrichment.assert_not_awaited()


@pytest.mark.asyncio
async def test_partial_nuclei_run_preserves_findings_and_diagnostics() -> None:
    sessions = _SessionFactory()
    scanner = SimpleNamespace(
        run_scan=AsyncMock(
            return_value=[
                {
                    "title": "Partial result",
                    "severity": "high",
                    "evidence": {
                        "scan_status": "partial",
                        "scan_error": "timeout",
                    },
                }
            ]
        ),
        last_run_report=NucleiRunReport(
            "partial",
            findings_count=1,
            reason="timeout",
            returncode=-15,
        ),
    )
    enrichment = AsyncMock()
    engagement_id = str(uuid.uuid4())
    job_id = str(uuid.uuid4())

    with (
        patch("app.database.AsyncSessionLocal", sessions),
        patch("app.routers.vuln_scans.NucleiScanner", return_value=scanner),
        patch("app.routers.vuln_scans.run_post_scan_enrichment", enrichment),
    ):
        await _run_nuclei_and_save(
            engagement_id,
            job_id,
            ["10.0.0.1"],
            ["cves"],
            100,
            60,
        )

    assert sessions.job.status == ScanJobStatus.completed
    assert sessions.job.result["outcome"] == "partial"
    assert sessions.job.result["degraded"] is True
    assert sessions.job.result["findings_created"] == 1
    assert sessions.job.result["scanner_run"]["error_code"] == "timeout"
    assert len(sessions.added) == 1
    enrichment.assert_awaited_once_with(engagement_id, job_id)

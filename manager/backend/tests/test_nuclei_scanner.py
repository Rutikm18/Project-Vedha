from __future__ import annotations

import asyncio
import json
from unittest.mock import AsyncMock, patch

import pytest

from app.vuln.nuclei import NucleiScanError, NucleiScanner


def _finding_line() -> bytes:
    return (
        json.dumps(
            {
                "template-id": "CVE-2024-0001",
                "info": {
                    "name": "Example finding",
                    "severity": "high",
                    "description": "Test evidence",
                },
                "host": "https://10.0.0.1",
                "matched-at": "https://10.0.0.1/example",
            }
        ).encode()
        + b"\n"
    )


class FakeProcess:
    def __init__(
        self,
        *,
        stdout: bytes = b"",
        stderr: bytes = b"",
        returncode: int = 0,
        wait_forever: bool = False,
    ) -> None:
        self.stdout = asyncio.StreamReader()
        self.stdout.feed_data(stdout)
        self.stdout.feed_eof()
        self.stderr = asyncio.StreamReader()
        self.stderr.feed_data(stderr)
        self.stderr.feed_eof()
        self.returncode: int | None = None
        self._exit_code = returncode
        self._wait_forever = wait_forever
        self._stopped = asyncio.Event()

    async def wait(self) -> int:
        if self._wait_forever and self.returncode is None:
            await self._stopped.wait()
        if self.returncode is None:
            self.returncode = self._exit_code
        return self.returncode

    def terminate(self) -> None:
        self.returncode = -15
        self._stopped.set()

    def kill(self) -> None:
        self.returncode = -9
        self._stopped.set()


@pytest.mark.asyncio
async def test_run_scan_streams_jsonl_and_separates_timeouts() -> None:
    scanner = NucleiScanner()
    proc = FakeProcess(stdout=_finding_line())

    with (
        patch("app.vuln.nuclei.shutil.which", return_value="/usr/bin/nuclei"),
        patch(
            "app.vuln.nuclei.asyncio.create_subprocess_exec",
            new=AsyncMock(return_value=proc),
        ) as create_process,
    ):
        findings = await scanner.run_scan(
            ["https://10.0.0.1"],
            ["cves"],
            timeout_sec=30,
            request_timeout_sec=7,
        )

    command = create_process.await_args.args
    assert "-jsonl" in command
    assert "-json-export" not in command
    assert command[command.index("-timeout") + 1] == "7"
    assert len(findings) == 1
    assert scanner.last_run_report is not None
    assert scanner.last_run_report.status == "success"


@pytest.mark.asyncio
async def test_missing_binary_is_a_reported_failure() -> None:
    scanner = NucleiScanner()

    with patch("app.vuln.nuclei.shutil.which", return_value=None):
        with pytest.raises(NucleiScanError) as exc_info:
            await scanner.run_scan(["https://10.0.0.1"], [])

    assert exc_info.value.reason == "not_installed"
    assert scanner.last_run_report is not None
    assert scanner.last_run_report.status == "failed"


@pytest.mark.asyncio
async def test_nonzero_exit_without_findings_raises_with_stderr() -> None:
    scanner = NucleiScanner()
    proc = FakeProcess(stderr=b"no templates provided\n", returncode=1)

    with (
        patch("app.vuln.nuclei.shutil.which", return_value="/usr/bin/nuclei"),
        patch(
            "app.vuln.nuclei.asyncio.create_subprocess_exec",
            new=AsyncMock(return_value=proc),
        ),
    ):
        with pytest.raises(NucleiScanError) as exc_info:
            await scanner.run_scan(["https://10.0.0.1"], [])

    assert exc_info.value.reason == "nonzero_exit"
    assert exc_info.value.returncode == 1
    assert "no templates" in exc_info.value.stderr


@pytest.mark.asyncio
async def test_nonzero_exit_retains_and_marks_partial_findings() -> None:
    scanner = NucleiScanner()
    proc = FakeProcess(
        stdout=_finding_line(),
        stderr=b"rate limit interrupted scan\n",
        returncode=2,
    )

    with (
        patch("app.vuln.nuclei.shutil.which", return_value="/usr/bin/nuclei"),
        patch(
            "app.vuln.nuclei.asyncio.create_subprocess_exec",
            new=AsyncMock(return_value=proc),
        ),
    ):
        findings = await scanner.run_scan(["https://10.0.0.1"], [])

    assert len(findings) == 1
    assert findings[0]["evidence"]["scan_status"] == "partial"
    assert findings[0]["evidence"]["scan_error"] == "nonzero_exit"
    assert scanner.last_run_report is not None
    assert scanner.last_run_report.status == "partial"


@pytest.mark.asyncio
async def test_timeout_retains_findings_emitted_before_termination() -> None:
    scanner = NucleiScanner()
    proc = FakeProcess(stdout=_finding_line(), wait_forever=True)

    with (
        patch("app.vuln.nuclei.shutil.which", return_value="/usr/bin/nuclei"),
        patch(
            "app.vuln.nuclei.asyncio.create_subprocess_exec",
            new=AsyncMock(return_value=proc),
        ),
    ):
        findings = await scanner.run_scan(
            ["https://10.0.0.1"],
            [],
            timeout_sec=0.01,
        )

    assert len(findings) == 1
    assert findings[0]["evidence"]["scan_error"] == "timeout"
    assert scanner.last_run_report is not None
    assert scanner.last_run_report.status == "partial"


@pytest.mark.asyncio
async def test_template_initialization_failure_cannot_be_clean_zero() -> None:
    scanner = NucleiScanner()
    proc = FakeProcess(
        stderr=b"[FTL] Could not run nuclei: no templates provided for scan\n",
        returncode=0,
    )

    with (
        patch("app.vuln.nuclei.shutil.which", return_value="/usr/bin/nuclei"),
        patch(
            "app.vuln.nuclei.asyncio.create_subprocess_exec",
            new=AsyncMock(return_value=proc),
        ),
    ):
        with pytest.raises(NucleiScanError) as exc_info:
            await scanner.run_scan(["https://10.0.0.1"], [])

    assert exc_info.value.reason == "templates_missing"
    assert scanner.last_run_report is not None
    assert scanner.last_run_report.status == "failed"

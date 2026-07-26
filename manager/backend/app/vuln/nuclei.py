"""
NucleiScanner — async subprocess wrapper around the Nuclei CLI.

Nuclei outputs JSONL: one JSON object per finding on stdout.
Each line shape:
  {
    "template-id": "CVE-2021-44228",
    "info": {"name": "...", "severity": "critical", "tags": ["cve"]},
    "matched-at": "http://10.0.0.5:8080/path",
    "host": "http://10.0.0.5:8080",
    "type": "http",
    "timestamp": "2026-05-19T10:00:00Z",
    "matcher-name": "matcher-1",
    "extracted-results": [],
    "curl-command": "curl ..."
  }
"""
from __future__ import annotations

import asyncio
import json
import re
import shutil
from contextlib import suppress
from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Literal

import structlog

from app.models.enums import FindingSeverity, FindingStatus
from app.discovery.service_id import ServiceFingerprint

logger = structlog.get_logger()

_NUCLEI_SEV: dict[str, FindingSeverity] = {
    "critical": FindingSeverity.critical,
    "high":     FindingSeverity.high,
    "medium":   FindingSeverity.medium,
    "low":      FindingSeverity.low,
    "info":     FindingSeverity.info,
    "unknown":  FindingSeverity.info,
}

# Service type → relevant template tags
_SERVICE_TEMPLATE_MAP: dict[str, list[str]] = {
    "http":      ["cves", "misconfigs", "ssl", "default-logins", "exposures", "technologies"],
    "https":     ["cves", "misconfigs", "ssl", "default-logins", "exposures", "technologies"],
    "ssh":       ["cves", "default-logins", "misconfigs"],
    "ftp":       ["cves", "default-logins", "misconfigs"],
    "smb":       ["cves", "misconfigs", "network"],
    "rdp":       ["cves", "misconfigs", "default-logins"],
    "smtp":      ["cves", "misconfigs"],
    "mssql":     ["cves", "default-logins", "misconfigs"],
    "mysql":     ["cves", "default-logins", "misconfigs"],
    "postgres":  ["cves", "default-logins", "misconfigs"],
    "redis":     ["cves", "misconfigs", "default-logins"],
    "mongodb":   ["cves", "misconfigs", "default-logins"],
    "ldap":      ["misconfigs", "network"],
    "kerberos":  ["misconfigs", "network"],
    "snmp":      ["misconfigs", "network", "default-logins"],
    "netbios":   ["misconfigs", "network"],
    "default":   ["cves", "misconfigs"],
}

_CVE_RE = re.compile(r"CVE-\d{4}-\d+", re.I)
_STDERR_LIMIT = 16_384
_STDOUT_LINE_LIMIT = 8 * 1024 * 1024
_TEMPLATE_FAILURE_MARKERS = (
    "no templates provided for scan",
    "no templates found",
    "no templates available",
    "nuclei-templates are not installed",
    "could not find template",
)


@dataclass(frozen=True)
class NucleiRunReport:
    """Machine-readable state for the most recent scanner invocation."""

    status: Literal["success", "partial", "failed"]
    findings_count: int
    reason: str | None = None
    returncode: int | None = None
    stderr: str = ""
    malformed_lines: int = 0


class NucleiScanError(RuntimeError):
    """Fatal Nuclei failure, optionally carrying findings emitted before failure."""

    def __init__(
        self,
        reason: str,
        detail: str,
        *,
        partial_findings: list[dict[str, Any]] | None = None,
        returncode: int | None = None,
        stderr: str = "",
    ) -> None:
        super().__init__(f"Nuclei scan failed ({reason}): {detail}")
        self.reason = reason
        self.partial_findings = list(partial_findings or [])
        self.returncode = returncode
        self.stderr = stderr


class NucleiScanner:
    """Run Nuclei against targets and parse JSONL output into Finding dicts."""

    NUCLEI_BIN = "nuclei"

    def __init__(self) -> None:
        self.last_run_report: NucleiRunReport | None = None

    # ── run_scan ──────────────────────────────────────────────────────────────

    async def run_scan(
        self,
        targets: list[str],
        templates: list[str],
        rate_limit: int = 150,
        timeout_sec: int | float = 300,
        request_timeout_sec: int = 10,
    ) -> list[dict[str, Any]]:
        """
        Run Nuclei and stream JSONL findings from stdout.

        ``request_timeout_sec`` controls each Nuclei network request. The
        existing ``timeout_sec`` argument is the independent wall-clock
        deadline for the whole process.
        """
        if not targets:
            self.last_run_report = NucleiRunReport("success", findings_count=0)
            return []
        if timeout_sec <= 0:
            raise ValueError("timeout_sec must be greater than zero")
        if request_timeout_sec <= 0:
            raise ValueError("request_timeout_sec must be greater than zero")

        if not shutil.which(self.NUCLEI_BIN):
            detail = "nuclei binary is not installed or is not on PATH"
            self.last_run_report = NucleiRunReport(
                "failed", findings_count=0, reason="not_installed"
            )
            logger.error(
                "nuclei.scan.failed",
                reason="not_installed",
                hint="Install nuclei: https://github.com/projectdiscovery/nuclei",
            )
            raise NucleiScanError("not_installed", detail)

        target_args = []
        for t in targets:
            target_args += ["-target", t]

        tag_args = []
        if templates:
            tag_args = ["-tags", ",".join(sorted(set(templates)))]

        cmd = [
            self.NUCLEI_BIN,
            *target_args,
            *tag_args,
            "-rate-limit", str(rate_limit),
            "-jsonl",
            "-silent",
            "-no-color",
            "-timeout", str(request_timeout_sec),
        ]
        logger.info(
            "nuclei.scan.start",
            targets=len(targets),
            tags=templates,
            request_timeout_sec=request_timeout_sec,
            job_timeout_sec=timeout_sec,
        )

        try:
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                limit=_STDOUT_LINE_LIMIT,
            )
        except OSError as exc:
            detail = str(exc)
            self.last_run_report = NucleiRunReport(
                "failed", findings_count=0, reason="spawn_failed", stderr=detail
            )
            logger.error("nuclei.scan.failed", reason="spawn_failed", error=detail)
            raise NucleiScanError("spawn_failed", detail, stderr=detail) from exc

        if proc.stdout is None or proc.stderr is None:
            await self._stop_process(proc)
            detail = "subprocess pipes were not created"
            self.last_run_report = NucleiRunReport(
                "failed", findings_count=0, reason="spawn_failed"
            )
            raise NucleiScanError("spawn_failed", detail)

        findings: list[dict[str, Any]] = []
        stdout_task = asyncio.create_task(
            self._consume_stdout(proc.stdout, findings),
            name="nuclei-stdout",
        )
        stderr_task = asyncio.create_task(
            self._read_stderr(proc.stderr),
            name="nuclei-stderr",
        )
        timed_out = False

        try:
            await asyncio.wait_for(proc.wait(), timeout=float(timeout_sec))
        except asyncio.TimeoutError:
            timed_out = True
            await self._stop_process(proc)
        except asyncio.CancelledError:
            await self._stop_process(proc)
            await asyncio.gather(stdout_task, stderr_task, return_exceptions=True)
            self.last_run_report = NucleiRunReport(
                "failed",
                findings_count=len(findings),
                reason="cancelled",
                returncode=proc.returncode,
            )
            raise

        malformed_lines = await stdout_task
        stderr = await stderr_task
        returncode = proc.returncode

        if timed_out:
            return self._partial_or_raise(
                findings,
                reason="timeout",
                detail=f"job exceeded the {timeout_sec:g}s deadline",
                returncode=returncode,
                stderr=stderr,
                malformed_lines=malformed_lines,
            )

        if returncode != 0:
            return self._partial_or_raise(
                findings,
                reason="nonzero_exit",
                detail=f"nuclei exited with code {returncode}",
                returncode=returncode,
                stderr=stderr,
                malformed_lines=malformed_lines,
            )

        stderr_lower = stderr.lower()
        if any(marker in stderr_lower for marker in _TEMPLATE_FAILURE_MARKERS):
            return self._partial_or_raise(
                findings,
                reason="templates_missing",
                detail="nuclei could not load a usable template set",
                returncode=returncode,
                stderr=stderr,
                malformed_lines=malformed_lines,
            )

        if malformed_lines:
            return self._partial_or_raise(
                findings,
                reason="parse_error",
                detail=f"could not parse {malformed_lines} JSONL line(s)",
                returncode=returncode,
                stderr=stderr,
                malformed_lines=malformed_lines,
            )

        self.last_run_report = NucleiRunReport(
            "success",
            findings_count=len(findings),
            returncode=returncode,
            stderr=stderr,
        )
        logger.info(
            "nuclei.scan.done",
            findings=len(findings),
            returncode=returncode,
        )
        return findings

    async def _consume_stdout(
        self,
        stream: asyncio.StreamReader,
        findings: list[dict[str, Any]],
    ) -> int:
        malformed_lines = 0
        while True:
            raw_line = await stream.readline()
            if not raw_line:
                break
            line = raw_line.decode("utf-8", errors="replace").strip()
            if not line:
                continue
            try:
                raw = json.loads(line)
                if not isinstance(raw, dict):
                    raise TypeError("JSONL entry is not an object")
                findings.append(self._map_finding(raw))
            except (json.JSONDecodeError, KeyError, TypeError, AttributeError):
                malformed_lines += 1
                logger.warning(
                    "nuclei.output.malformed",
                    line=line[:300],
                )
        return malformed_lines

    async def _read_stderr(self, stream: asyncio.StreamReader) -> str:
        tail = bytearray()
        while True:
            chunk = await stream.read(4096)
            if not chunk:
                break
            tail.extend(chunk)
            if len(tail) > _STDERR_LIMIT:
                del tail[:-_STDERR_LIMIT]
        return tail.decode("utf-8", errors="replace").strip()

    async def _stop_process(self, proc: asyncio.subprocess.Process) -> None:
        if proc.returncode is not None:
            return
        with suppress(ProcessLookupError):
            proc.terminate()
        try:
            await asyncio.wait_for(proc.wait(), timeout=5)
        except asyncio.TimeoutError:
            with suppress(ProcessLookupError):
                proc.kill()
            with suppress(asyncio.TimeoutError):
                await asyncio.wait_for(proc.wait(), timeout=5)

    def _partial_or_raise(
        self,
        findings: list[dict[str, Any]],
        *,
        reason: str,
        detail: str,
        returncode: int | None,
        stderr: str,
        malformed_lines: int,
    ) -> list[dict[str, Any]]:
        status: Literal["partial", "failed"] = "partial" if findings else "failed"
        self.last_run_report = NucleiRunReport(
            status,
            findings_count=len(findings),
            reason=reason,
            returncode=returncode,
            stderr=stderr,
            malformed_lines=malformed_lines,
        )
        logger.error(
            "nuclei.scan.partial" if findings else "nuclei.scan.failed",
            reason=reason,
            error=detail,
            returncode=returncode,
            findings=len(findings),
            stderr=stderr[:500],
        )

        if not findings:
            raise NucleiScanError(
                reason,
                detail,
                returncode=returncode,
                stderr=stderr,
            )

        for finding in findings:
            evidence = finding.setdefault("evidence", {})
            evidence["scan_status"] = "partial"
            evidence["scan_error"] = reason
        return findings

    # ── parse_output ──────────────────────────────────────────────────────────

    def parse_output(self, jsonl_output: str) -> list[dict[str, Any]]:
        """Parse nuclei JSONL output → list of Finding-compatible dicts."""
        findings = []
        for line in jsonl_output.splitlines():
            line = line.strip()
            if not line or not line.startswith("{"):
                continue
            try:
                raw = json.loads(line)
                findings.append(self._map_finding(raw))
            except (json.JSONDecodeError, KeyError):
                continue
        return findings

    def _map_finding(self, raw: dict[str, Any]) -> dict[str, Any]:
        info = raw.get("info", {})
        severity_str = info.get("severity", "info").lower()
        severity = _NUCLEI_SEV.get(severity_str, FindingSeverity.info)

        # Extract CVE IDs from template-id and description
        template_id = raw.get("template-id", "")
        description = info.get("description", "")
        cve_ids = list({m.upper() for m in _CVE_RE.findall(f"{template_id} {description}")})

        # CVSS from metadata if present
        metadata = info.get("metadata", {})
        cvss_score = None
        cvss_val = metadata.get("cvss-score") or metadata.get("cvss3-score")
        if cvss_val:
            try:
                cvss_score = Decimal(str(cvss_val))
            except Exception:
                pass

        # MITRE techniques
        mitre = [t for t in metadata.get("attack-vector", []) if t.startswith("T")]

        matched_at = raw.get("matched-at", raw.get("host", ""))

        return {
            "title": info.get("name", template_id),
            "description": description,
            "severity": severity,
            "status": FindingStatus.open,
            "cve_ids": cve_ids,
            "cvss_score": cvss_score,
            "mitre_techniques": mitre or None,
            "exploitable": severity in (FindingSeverity.critical, FindingSeverity.high),
            "exploit_validated": False,
            "evidence": {
                "template_id": template_id,
                "matched_at": matched_at,
                "matcher_name": raw.get("matcher-name", ""),
                "extracted_results": raw.get("extracted-results", []),
                "curl_command": raw.get("curl-command", ""),
                "type": raw.get("type", ""),
                "timestamp": raw.get("timestamp", ""),
                "tags": info.get("tags", []),
            },
        }

    # ── template_selector ─────────────────────────────────────────────────────

    def template_selector(self, asset_services: list[str]) -> list[str]:
        """
        Given a list of service names on an asset, return the union
        of relevant Nuclei template tags.

        Args:
            asset_services: e.g. ["http", "ssh", "smb"]

        Returns:
            Deduplicated list of template tags: ["cves", "misconfigs", "ssl", ...]
        """
        tags: set[str] = set()
        for svc in asset_services:
            svc_lower = svc.lower()
            mapped = _SERVICE_TEMPLATE_MAP.get(svc_lower, _SERVICE_TEMPLATE_MAP["default"])
            tags.update(mapped)
        return sorted(tags)

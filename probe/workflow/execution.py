"""Execution telemetry and failure normalization for the probe workflow."""
from __future__ import annotations

import asyncio
import errno
import re
import shutil
import socket
import ssl
from dataclasses import dataclass
from typing import Iterable

from scanner.scanner_base import ScanResult

from .gates import PROFILE_DEEP_BRANCHES
from .modes import (
    STAGE_DEEP_SCAN,
    STAGE_PORT_SCAN,
    STAGE_SERVICE_BANNER,
    includes_stage,
    resolve_stage_ceiling,
)


MANIFEST_SCHEMA_VERSION = "1.0"

# Ordered by the normal workflow. These are collector components inside the
# scanner_module orchestrator, not independent vulnerability verdict engines.
COMPONENT_CATALOG: tuple[dict[str, str], ...] = (
    {"id": "host_discovery", "label": "Host Discovery", "role": "Establish host liveness before deeper active probes."},
    {"id": "port_scan", "label": "TCP Port Scan", "role": "Identify open TCP services with bounded connect probes."},
    {"id": "service_banner", "label": "Service Banner", "role": "Collect service and version evidence from confirmed open ports."},
    {"id": "tls_scan", "label": "TLS Inspector", "role": "Collect supported protocol, cipher, and certificate facts."},
    {"id": "web_scan", "label": "Web Fingerprint", "role": "Collect passive HTTP response, header, and technology facts."},
    {"id": "smb_scan", "label": "SMB Negotiation", "role": "Collect SMB dialect support through negotiation only."},
    {"id": "db_scan", "label": "Database Fingerprint", "role": "Identify database listeners through minimal protocol handshakes."},
    {"id": "mcp_ai_scan", "label": "AI / MCP Discovery", "role": "Identify exposed AI and MCP discovery endpoints without invoking tools."},
    {"id": "snmp_scan", "label": "SNMP Read Probe", "role": "Collect read-only SNMP service facts."},
    {"id": "udp_scan", "label": "UDP Service Probe", "role": "Probe selected UDP services with protocol-specific read requests."},
    {"id": "passive_collect", "label": "Passive Discovery", "role": "Observe receive-only broadcast announcements and report unavailable multicast coverage."},
    {"id": "ssh_inventory", "label": "SSH Inventory", "role": "Collect authorized Linux inventory with supplied credentials."},
    {"id": "windows_inventory", "label": "Windows Inventory", "role": "Collect authorized Windows inventory with supplied credentials."},
)

_COMPONENT_META = {item["id"]: item for item in COMPONENT_CATALOG}
_BRANCH_COMPONENT = {
    "tls": "tls_scan",
    "web": "web_scan",
    "smb": "smb_scan",
    "db": "db_scan",
    "mcp_ai": "mcp_ai_scan",
    "snmp": "snmp_scan",
    "udp": "udp_scan",
}
_TCP_BRANCHES = {"tls", "web", "smb", "db", "mcp_ai"}


def engine_manifest(*, build_version: str, build_sha: str | None = None) -> dict:
    """Return the runtime engine inventory without claiming optional tools ran."""
    orchestrator = {
        "id": "scanner_module",
        "label": "Vedha Probe Collector",
        "version": build_version,
        "role": "Scope-gated workflow orchestrator that emits raw facts.",
    }
    if build_sha:
        orchestrator["build_sha"] = build_sha

    external = (
        {
            "id": "nmap",
            "label": "Nmap",
            "available": shutil.which("nmap") is not None,
            "execution": "standalone_validation",
            "role": "Independent discovery, service, OS, and safe-NSE cross-validation.",
        },
        {
            "id": "masscan",
            "label": "Masscan",
            "available": shutil.which("masscan") is not None,
            "execution": "standalone_validation",
            "role": "Optional raw-packet discovery for very large scopes; native connect fallback is available.",
        },
    )
    return {
        "schema_version": MANIFEST_SCHEMA_VERSION,
        "orchestrator": orchestrator,
        "components": [
            {**item, "kind": "native", "available": True}
            for item in COMPONENT_CATALOG
        ],
        "external_engines": list(external),
    }


def planned_components(
    profile: str,
    *,
    service_filter: set[str] | None,
    stop_after_banner: bool,
    ssh_enabled: bool,
    windows_enabled: bool,
    stage_ceiling: str | None = None,
) -> list[str]:
    """Resolve the exact collector plan for one workflow invocation."""
    if profile == "ot":
        return ["passive_collect"]

    ceiling = resolve_stage_ceiling(
        stage_ceiling,
        stop_after_banner=stop_after_banner,
    )
    branches = PROFILE_DEEP_BRANCHES.get(profile, set())
    if service_filter is not None:
        branches = branches & service_filter
    tcp_stage_required = service_filter is None or bool(branches & _TCP_BRANCHES)
    direct_datagram = (
        service_filter is not None
        and ("udp" in service_filter or "snmp" in branches)
    )

    planned = []
    if tcp_stage_required or not direct_datagram:
        planned.append("host_discovery")
    if includes_stage(ceiling, STAGE_PORT_SCAN) and tcp_stage_required:
        planned.append("port_scan")
    if includes_stage(ceiling, STAGE_SERVICE_BANNER) and tcp_stage_required:
        planned.append("service_banner")
    if not includes_stage(ceiling, STAGE_DEEP_SCAN):
        return planned

    for item in COMPONENT_CATALOG:
        component_id = item["id"]
        if component_id in {_BRANCH_COMPONENT[b] for b in branches if b in _BRANCH_COMPONENT}:
            planned.append(component_id)

    if service_filter is None or "udp" in service_filter:
        planned.append("udp_scan")
    if ssh_enabled:
        planned.append("ssh_inventory")
    if windows_enabled:
        planned.append("windows_inventory")
    return list(dict.fromkeys(planned))


@dataclass(frozen=True)
class ErrorDetail:
    code: str
    retryable: bool
    remediation: str


def classify_scanner_error(exc: BaseException) -> ErrorDetail:
    """Map low-level failures into stable, operator-actionable categories."""
    structured_code = getattr(exc, "error_code", None)
    if structured_code in {"listener_unavailable", "permission_denied"}:
        return ErrorDetail(
            structured_code,
            bool(getattr(exc, "retryable", False)),
            str(getattr(
                exc,
                "remediation",
                "Inspect the probe listener configuration and retry.",
            )),
        )
    if isinstance(exc, FileNotFoundError):
        return ErrorDetail(
            "dependency_missing", False,
            "Install the required scanner dependency on the probe or use a native collector.",
        )
    if isinstance(exc, PermissionError):
        return ErrorDetail(
            "permission_denied", False,
            "Grant only the required socket/file capability and verify the probe service account.",
        )
    if isinstance(exc, (asyncio.TimeoutError, TimeoutError)):
        return ErrorDetail(
            "scanner_timeout", True,
            "Retry at a lower concurrency or raise the bounded per-operation timeout.",
        )
    if isinstance(exc, socket.gaierror):
        return ErrorDetail(
            "dns_resolution_failed", True,
            "Verify probe DNS configuration or scan an authorized IP address directly.",
        )
    if isinstance(exc, ssl.SSLError):
        return ErrorDetail(
            "tls_handshake_failed", True,
            "Confirm the port speaks TLS and retry with the TLS collector timeout adjusted.",
        )
    if isinstance(exc, ConnectionError):
        return ErrorDetail(
            "connection_failed", True,
            "Verify routing, firewall policy, and target availability from the probe network.",
        )
    if isinstance(exc, OSError) and exc.errno in {
        errno.EMFILE, errno.ENFILE, errno.ENOBUFS, errno.ENOMEM,
    }:
        return ErrorDetail(
            "resource_exhausted", True,
            "Lower scan concurrency and verify file-descriptor and memory limits on the probe.",
        )
    return ErrorDetail(
        "scanner_internal_error", False,
        "Inspect the component error and probe logs; retry only after correcting the underlying fault.",
    )


def scanner_failure_result(scanner: str, target: str, exc: BaseException) -> ScanResult:
    """Represent an unexpected component exception without aborting other hosts."""
    detail = classify_scanner_error(exc)
    message = re.sub(r"[\x00-\x1f\x7f]+", " ", str(exc)).strip()[:300]
    error = f"{type(exc).__name__}: {message or detail.code}"
    data = {
        "error_code": detail.code,
        "retryable": detail.retryable,
        "remediation": detail.remediation,
    }
    details = getattr(exc, "details", None)
    if isinstance(details, dict):
        data["details"] = details
    return ScanResult(
        scanner=scanner,
        target=target,
        status="error",
        data=data,
        error=error,
    )


class ExecutionTrace:
    """Mutable per-run component accounting, serialized only after completion."""

    def __init__(self, planned: Iterable[str]):
        self._runs: dict[str, dict] = {}
        for component_id in planned:
            self._ensure(component_id)

    def _ensure(self, component_id: str) -> dict:
        if component_id not in self._runs:
            meta = _COMPONENT_META.get(
                component_id,
                {"id": component_id, "label": component_id, "role": "Collector component."},
            )
            self._runs[component_id] = {
                **meta,
                "attempted_targets": 0,
                "invocations": 0,
                "result_count": 0,
                "fact_count": 0,
                "error_count": 0,
                "reused_fact_count": 0,
                "skip_reason": None,
                "coverage": None,
                "issues": [],
            }
        return self._runs[component_id]

    def record(
        self,
        component_id: str,
        *,
        target_count: int,
        results: Iterable[ScanResult],
        reused_count: int = 0,
        coverage: dict | None = None,
    ) -> None:
        run = self._ensure(component_id)
        result_list = list(results)
        run["attempted_targets"] += max(0, target_count)
        if target_count:
            run["invocations"] += 1
        run["result_count"] += len(result_list)
        run["reused_fact_count"] += max(0, reused_count)
        run["skip_reason"] = None
        if coverage is not None:
            run["coverage"] = dict(coverage)
            if coverage.get("degraded"):
                run["error_count"] += 1
                run["issues"].append({
                    "code": coverage.get("error_code", "listener_unavailable"),
                    "scanner": component_id,
                    "target": "<passive-listener>",
                    "message": (
                        f"{coverage.get('failed_count', 0)} of "
                        f"{coverage.get('requested_count', 0)} passive listeners "
                        f"were unavailable; {coverage.get('active_count', 0)} remain active."
                    ),
                    "retryable": bool(coverage.get("retryable", False)),
                    "remediation": coverage.get("remediation"),
                    "details": {"coverage": dict(coverage)},
                })
        for result in result_list:
            data = result.data or {}
            result_details = data.get("details")
            result_coverage = (
                result_details.get("coverage")
                if isinstance(result_details, dict)
                else None
            )
            if isinstance(result_coverage, dict):
                run["coverage"] = dict(result_coverage)
            if result.status != "error" and not result.error:
                run["fact_count"] += 1
                continue
            run["error_count"] += 1
            issue = {
                "code": data.get("error_code", "scanner_error"),
                "scanner": component_id,
                "target": result.target,
                "message": result.error or "scanner returned an error result",
                "retryable": bool(data.get("retryable", False)),
                "remediation": data.get("remediation"),
            }
            if isinstance(result_details, dict):
                issue["details"] = result_details
            run["issues"].append(issue)

    def reused(self, component_id: str, results: Iterable[ScanResult]) -> None:
        result_list = list(results)
        self.record(
            component_id,
            target_count=0,
            results=result_list,
            reused_count=len(result_list),
        )

    def skip(self, component_id: str, reason: str) -> None:
        run = self._ensure(component_id)
        if run["invocations"] == 0 and run["reused_fact_count"] == 0:
            run["skip_reason"] = reason

    def finalize(self, reason: str = "No eligible target or service was observed.") -> None:
        for component_id in self._runs:
            self.skip(component_id, reason)

    @property
    def issues(self) -> list[dict]:
        return [
            issue
            for run in self._runs.values()
            for issue in run["issues"]
        ]

    @property
    def degraded(self) -> bool:
        return any(run["error_count"] for run in self._runs.values())

    @property
    def failed(self) -> bool:
        """True when execution produced errors and no usable or cached facts."""
        return self.degraded and not any(
            run["fact_count"]
            or run["reused_fact_count"]
            or self._has_active_coverage(run)
            for run in self._runs.values()
        )

    @staticmethod
    def _has_active_coverage(run: dict) -> bool:
        coverage = run.get("coverage")
        return isinstance(coverage, dict) and coverage.get("active_count", 0) > 0

    def as_list(self) -> list[dict]:
        serialized = []
        for run in self._runs.values():
            if run["invocations"] == 0 and run["reused_fact_count"]:
                status = "cached"
            elif run["invocations"] == 0:
                status = "skipped"
            elif (
                run["error_count"]
                and run["fact_count"] == 0
                and not self._has_active_coverage(run)
            ):
                status = "failed"
            elif run["error_count"]:
                status = "degraded"
            else:
                status = "completed"
            serialized.append({
                key: value
                for key, value in {**run, "status": status}.items()
                if key != "issues" and value is not None
            })
        return serialized

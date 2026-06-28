"""
engine.py — adapt a manager scan job to scanner_module's workflow engine and
return RAW FACTS (a list of ScanResult dicts). Never raises; a scanner bug
becomes {"ok": False, "error": ...}, never a crashed agent loop.

result schema (v1.1) — matches techprompt.md Part A §A4:
  result_schema_version, probe_id, engagement_uuid, use_case_id, scan_type,
  profile, started_at, finished_at, facts (raw), run_stats, errors, ok
"""
from __future__ import annotations

import asyncio
import os
import socket
from dataclasses import asdict
from datetime import datetime, timezone

from scanner.scanner_base import ScopeGuard

from workflow.cache import WorkflowCache
from workflow.modes import assessment, service_specific, triage
from workflow.workflow_engine import run_engagement

RESULT_SCHEMA_VERSION = "1.1"
PROBE_ID = os.environ.get("PROBE_NAME") or socket.gethostname()

# scan_type -> (default_profile, mode-factory, service_filter)
_SCAN_MAP = {
    "discovery":            ("it",  triage,      None),
    "host_discovery":       ("it",  triage,      None),
    "port_scan":            ("it",  triage,      None),
    "service_fingerprint":  ("it",  triage,      None),
    "assessment":           ("it",  assessment,  None),
    "vuln_scan":            ("it",  assessment,  None),
    "tls_scan":             ("it",  None,        {"tls"}),
    "web_scan":             ("it",  None,        {"web"}),
    "db_fingerprint":       ("it",  None,        {"db"}),
    "smb_enum":             ("it",  None,        {"smb"}),
    "udp_scan":             ("it",  None,        {"udp"}),
    "mcp_discovery":        ("it",  None,        {"mcp_ai"}),
    "ai_service_discovery": ("it",  None,        {"mcp_ai"}),
    "passive_discovery":    ("ot",  triage,      None),
}

CAPABILITIES = sorted(_SCAN_MAP)


def resolve_scan_type(job_type: str | None, params: dict) -> str:
    return params.get("scan_type") or job_type or "discovery"


def _targets(params: dict) -> list[str]:
    t = params.get("targets") or params.get("target") or params.get("scope_cidrs") or []
    return [t] if isinstance(t, str) else list(t)


def run_scan(scan_type: str, params: dict,
             use_case_id: str | None = None,
             engagement_uuid: str | None = None,
             validated_scope: list[str] | None = None) -> dict:
    """Execute a scan and return the enriched result bundle.

    Args:
        scan_type: one of CAPABILITIES
        params: job parameters from manager
        use_case_id: optional use-case that originated this job (for result provenance)
        engagement_uuid: engagement ID from manager (for result provenance)
        validated_scope: scope CIDRs already re-validated by the agent against
            the manager's engagement scope (overrides params["scope_cidrs"]).
            When present this is the authoritative allowlist — guarantees the probe
            never scans outside the engagement boundary even if params were altered.
    """
    started_at = datetime.now(timezone.utc).isoformat()
    errors: list[str] = []

    cfg = _SCAN_MAP.get(scan_type)
    if cfg is None:
        return {
            "result_schema_version": RESULT_SCHEMA_VERSION,
            "probe_id": PROBE_ID,
            "engagement_uuid": engagement_uuid,
            "use_case_id": use_case_id,
            "scan_type": scan_type,
            "started_at": started_at,
            "finished_at": datetime.now(timezone.utc).isoformat(),
            "ok": False,
            "error": f"unsupported scan_type '{scan_type}'",
            "supported": CAPABILITIES,
            "facts": [], "run_stats": {}, "errors": [],
        }

    default_profile, mode_factory, svc_filter = cfg
    profile = params.get("profile", default_profile)

    targets = _targets(params)
    if not targets:
        return {
            "result_schema_version": RESULT_SCHEMA_VERSION,
            "probe_id": PROBE_ID,
            "engagement_uuid": engagement_uuid,
            "use_case_id": use_case_id,
            "scan_type": scan_type,
            "profile": profile,
            "started_at": started_at,
            "finished_at": datetime.now(timezone.utc).isoformat(),
            "ok": False, "error": "no targets/scope provided",
            "facts": [], "run_stats": {}, "errors": [],
        }

    # ScopeGuard: prefer the independently-validated scope (re-validated by agent
    # before this function is called); fall back to manager-provided scope_cidrs;
    # last resort: treat the targets themselves as the allowlist.
    scope_src = validated_scope or params.get("scope_cidrs") or targets
    scope = ScopeGuard.from_list([s for s in scope_src if s])

    mode = mode_factory() if mode_factory else service_specific(svc_filter or set())
    cache = WorkflowCache()

    try:
        asyncio.run(run_engagement(
            targets, scope, profile=profile,
            service_filter=mode.service_filter,
            stop_after_banner=mode.stop_after_banner, cache=cache))
    except Exception as exc:
        errors.append(f"{type(exc).__name__}: {exc}")
        return {
            "result_schema_version": RESULT_SCHEMA_VERSION,
            "probe_id": PROBE_ID,
            "engagement_uuid": engagement_uuid,
            "use_case_id": use_case_id,
            "scan_type": scan_type,
            "profile": profile,
            "started_at": started_at,
            "finished_at": datetime.now(timezone.utc).isoformat(),
            "ok": False,
            "error": errors[0],
            "facts": [], "run_stats": {}, "errors": errors,
        }

    facts = [asdict(e.result) for e in cache._store.values()]
    hosts = {f["target"] for f in facts}
    open_ports = sum(1 for f in facts if f.get("status") == "open")

    return {
        "result_schema_version": RESULT_SCHEMA_VERSION,
        "probe_id": PROBE_ID,
        "engagement_uuid": engagement_uuid,
        "use_case_id": use_case_id,
        "scan_type": scan_type,
        "profile": profile,
        "started_at": started_at,
        "finished_at": datetime.now(timezone.utc).isoformat(),
        "ok": True,
        "engine": "scanner_module",
        "facts": facts,
        "run_stats": {
            "host_count": len(hosts),
            "open_ports": open_ports,
            "fact_count": len(facts),
            "scanners_run": sorted({f.get("scanner", "") for f in facts if f.get("scanner")}),
        },
        "errors": errors,
        # legacy flat fields kept for backwards compat with manager ingest
        "host_count": len(hosts),
        "service_count": open_ports,
        "open_ports": open_ports,
        "finding_count": 0,   # probe never produces findings — manager does
    }

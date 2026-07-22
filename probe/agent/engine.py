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
from datetime import datetime, timedelta, timezone

from scanner.scanner_base import ScopeGuard

from workflow.cache import WorkflowCache
from workflow.modes import assessment, service_specific, triage
from workflow.workflow_engine import run_engagement

RESULT_SCHEMA_VERSION = "1.1"
PROBE_ID = os.environ.get("PROBE_NAME") or socket.gethostname()


def _error_result(scan_type: str, error: str, **overrides) -> dict:
    """Single factory for error result dicts — no copy-paste."""
    return {
        "result_schema_version": RESULT_SCHEMA_VERSION,
        "probe_id": PROBE_ID,
        "scan_type": scan_type,
        "started_at": datetime.now(timezone.utc).isoformat(),
        "finished_at": datetime.now(timezone.utc).isoformat(),
        "ok": False,
        "error": error,
        "facts": [],
        "run_stats": {},
        "errors": [error],
        **overrides,
    }

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
    "snmp_scan":            ("it",  None,        {"snmp"}),
    "snmp_enum":            ("it",  None,        {"snmp"}),
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


def _clamp(val, lo, hi, default):
    """Coerce val to float and clamp to [lo, hi]; fall back to default on junk.
    Defense in depth: the operator's UI sends presets, but a buggy or tampered
    job must never be able to set rate=1e9 and flood a production segment."""
    try:
        return max(lo, min(hi, float(val)))
    except (TypeError, ValueError):
        return default


def _tuning_from_params(params: dict) -> dict:
    """Translate operator-supplied job params into run_engagement() kwargs.

    This is the seam that makes the Scanner page's controls actually reach the
    scan engine. Every value is clamped to a safe envelope here — the probe is
    the last line of defense before packets leave the host, so it does not
    trust the caller's numbers blindly.

    Recognised params (all optional):
      rate, concurrency, timeout, disc_timeout  — scan intensity (nmap-style)
      passive_listen_seconds                    — OT passive capture duration
      recheck_hours                             — re-scan delta window
      ssh_creds {user,password,key_path,port}   — Gate-6 SSH collection
      win_creds {user,password,domain}          — Gate-6 Windows collection
    """
    tuning: dict = {
        "rate":         _clamp(params.get("rate"),         1,   2000, 200.0),
        "concurrency":  int(_clamp(params.get("concurrency"), 1, 500, 100)),
        "timeout":      _clamp(params.get("timeout"),      0.5, 30.0, 3.0),
        "disc_timeout": _clamp(params.get("disc_timeout"), 0.5, 15.0, 1.5),
    }

    # OT passive listen window — the OT use-case promises "duration set by operator".
    if params.get("passive_listen_seconds") is not None:
        tuning["passive_listen_seconds"] = _clamp(
            params.get("passive_listen_seconds"), 5, 3600, 60.0)

    # Re-scan delta: only re-probe facts older than this window.
    if params.get("recheck_hours") is not None:
        hours = _clamp(params.get("recheck_hours"), 0, 24 * 365, 0)
        tuning["force_recheck_after"] = timedelta(hours=hours)

    # Gate-6 credentialed collection. Only assembled when a username is present
    # so an empty form never triggers an authenticated branch.
    ssh_in = params.get("ssh_creds") or {}
    if isinstance(ssh_in, dict) and ssh_in.get("user"):
        ssh_creds = {
            "user":     str(ssh_in["user"]),
            "password": (ssh_in.get("password") or None),
            "key_path": (ssh_in.get("key_path") or None),
        }
        if ssh_in.get("port"):
            ssh_creds["port"] = int(_clamp(ssh_in.get("port"), 1, 65535, 22))
        tuning["ssh_creds"] = ssh_creds

    win_in = params.get("win_creds") or {}
    if isinstance(win_in, dict) and win_in.get("user"):
        win_creds = {
            "user":     str(win_in["user"]),
            "password": str(win_in.get("password") or ""),
        }
        if win_in.get("domain"):
            win_creds["domain"] = str(win_in["domain"])
        tuning["win_creds"] = win_creds

    return tuning


def _count_open_port_facts(facts: list[dict]) -> int:
    """Count concrete open services, not generic host-liveness observations."""
    return sum(
        1 for f in facts
        if f.get("status") == "open" and f.get("port") is not None
    )


def run_scan(scan_type: str, params: dict,
             use_case_id: str | None = None,
             engagement_uuid: str | None = None,
             validated_scope: list[str] | None = None,
             validated_excludes: list[str] | None = None) -> dict:
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
        validated_excludes: excluded CIDRs the agent fetched from the engagement's
            authoritative /scope (merged with any per-job excluded_cidrs). These are
            carved OUT of the allowlist by ScopeGuard — packets never reach them.
    """
    started_at = datetime.now(timezone.utc).isoformat()
    errors: list[str] = []

    cfg = _SCAN_MAP.get(scan_type)
    if cfg is None:
        return _error_result(scan_type, f"unsupported scan_type '{scan_type}'",
                            engagement_uuid=engagement_uuid,
                            use_case_id=use_case_id,
                            supported=CAPABILITIES)

    default_profile, mode_factory, svc_filter = cfg
    profile = params.get("profile", default_profile)

    targets = _targets(params)
    if not targets:
        return _error_result(scan_type, "no targets/scope provided",
                            engagement_uuid=engagement_uuid,
                            use_case_id=use_case_id, profile=profile)

    # ScopeGuard: prefer the independently-validated scope (re-validated by agent
    # before this function is called); fall back to manager-provided scope_cidrs;
    # last resort: treat the targets themselves as the allowlist.
    scope_src = validated_scope or params.get("scope_cidrs") or targets
    # Exclusions: authoritative engagement excludes (from agent) merged with any
    # per-job excluded_cidrs the operator set in the UI. ScopeGuard subtracts them.
    # Deduped, order-preserving — the agent may pass the same list via both routes.
    exclude_src = list(dict.fromkeys(
        e for e in (*(validated_excludes or []), *(params.get("excluded_cidrs") or [])) if e
    ))
    scope = ScopeGuard.from_list([s for s in scope_src if s], excludes=exclude_src)

    mode = mode_factory() if mode_factory else service_specific(svc_filter or set())
    cache = WorkflowCache()

    # Translate the operator's job params (scan intensity, OT listen window,
    # re-scan delta, credentials) into engine kwargs. This is what makes the
    # Scanner page's controls drive the actual scan instead of being ignored.
    tuning = _tuning_from_params(params)

    try:
        asyncio.run(run_engagement(
            targets, scope, profile=profile,
            service_filter=mode.service_filter,
            stop_after_banner=mode.stop_after_banner, cache=cache,
            **tuning))
    except Exception as exc:
        error_msg = f"{type(exc).__name__}: {exc}"
        errors.append(error_msg)
        return _error_result(scan_type, error_msg,
                            engagement_uuid=engagement_uuid,
                            use_case_id=use_case_id, profile=profile,
                            errors=errors)

    facts = [asdict(e.result) for e in cache._store.values()]
    unique_hosts = {f["target"] for f in facts}
    open_ports = _count_open_port_facts(facts)

    # Build `hosts` list from facts for manager-side asset promotion.
    # The manager's _promote_assets expects: [{"ip":..., "hostname":..., "ports":[{"port":..., "protocol":..., "service":...}]}]
    _host_map: dict[str, dict] = {}
    for f in facts:
        t = f["target"]
        if t not in _host_map:
            _host_map[t] = {"ip": t, "hostname": f.get("data", {}).get("hostname") or None, "ports": []}
        if f.get("port") is not None:
            _host_map[t]["ports"].append({
                "port": f["port"],
                "protocol": f.get("proto", "tcp"),
                "service": f.get("data", {}).get("service") or f.get("data", {}).get("first_line"),
            })
    hosts_list = list(_host_map.values())

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
        "hosts": hosts_list,
        "run_stats": {
            "host_count": len(unique_hosts),
            "open_ports": open_ports,
            "fact_count": len(facts),
            "scanners_run": sorted({f.get("scanner", "") for f in facts if f.get("scanner")}),
            # Provenance: the effective tuning that produced these facts. Credential
            # VALUES are never echoed — only whether an authenticated branch ran.
            "applied_tuning": {
                "rate": tuning.get("rate"),
                "concurrency": tuning.get("concurrency"),
                "timeout": tuning.get("timeout"),
                "disc_timeout": tuning.get("disc_timeout"),
                "passive_listen_seconds": tuning.get("passive_listen_seconds"),
                "recheck_hours": (tuning["force_recheck_after"].total_seconds() / 3600
                                  if tuning.get("force_recheck_after") else None),
                "ssh_auth": bool(tuning.get("ssh_creds")),
                "win_auth": bool(tuning.get("win_creds")),
            },
            # Scope provenance: exactly what the probe was authorized to touch.
            "scope_enforced": {
                "allow": [s for s in scope_src if s],
                "exclude": [e for e in exclude_src if e],
                "targets_requested": targets,
            },
        },
        "errors": errors,
        # legacy flat fields kept for backwards compat with manager ingest
        "host_count": len(unique_hosts),
        "service_count": open_ports,
        "open_ports": open_ports,
        "finding_count": 0,   # probe never produces findings — manager does
    }

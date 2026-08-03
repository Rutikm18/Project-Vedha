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

from scanner.scanner_base import ScopeGuard, expand_targets

from workflow.cache import WorkflowCache
from workflow.execution import (
    ExecutionTrace,
    engine_manifest,
    planned_components,
)
from workflow.modes import (
    assessment,
    discovery as discovery_mode,
    host_discovery as host_discovery_mode,
    port_scan as port_scan_mode,
    service_fingerprint as service_fingerprint_mode,
    service_specific,
    triage,
)
from workflow.workflow_engine import run_engagement

RESULT_SCHEMA_VERSION = "1.1"
PROBE_ID = os.environ.get("PROBE_NAME") or socket.gethostname()
ENGINE_ID = "scanner_module"
ENGINE_VERSION = os.environ.get("PROBE_BUILD_VERSION", "2.0.0")
ENGINE_BUILD_SHA = os.environ.get("PROBE_BUILD_SHA")
VALID_PROFILES = {"it", "iot", "ot"}


def _env_number(name: str, default: float, minimum: float, maximum: float) -> float:
    """Read a bounded numeric safety setting without trusting the environment."""
    try:
        return max(minimum, min(maximum, float(os.environ.get(name, default))))
    except (TypeError, ValueError):
        return default


# Hard appliance ceilings. A job may ask for less, never more. The target cap
# is intentionally much smaller than scanner_base's generic 200k guard because
# this path expands every host and runs a multi-stage assessment workflow.
MAX_TARGETS = int(_env_number("PROBE_MAX_TARGETS", 4096, 1, 200_000))
MAX_JOB_SECONDS = _env_number("PROBE_MAX_JOB_SECONDS", 7200, 1, 86_400)


def _runtime_manifest() -> dict:
    return engine_manifest(
        build_version=ENGINE_VERSION,
        build_sha=ENGINE_BUILD_SHA,
    )


def _error_result(
    scan_type: str,
    error: str,
    *,
    error_code: str = "job_invalid",
    remediation: str | None = None,
    **overrides,
) -> dict:
    """Single factory for error result dicts — no copy-paste."""
    issue = {
        "code": error_code,
        "scanner": ENGINE_ID,
        "message": error,
        "retryable": False,
    }
    if remediation:
        issue["remediation"] = remediation
    result = {
        "result_schema_version": RESULT_SCHEMA_VERSION,
        "probe_id": PROBE_ID,
        "scan_type": scan_type,
        "started_at": datetime.now(timezone.utc).isoformat(),
        "finished_at": datetime.now(timezone.utc).isoformat(),
        "ok": False,
        "outcome": "failed",
        "engine": ENGINE_ID,
        "engine_manifest": _runtime_manifest(),
        "error": error,
        "error_code": error_code,
        "facts": [],
        "run_stats": {},
        "errors": [error],
        "issues": [issue],
    }
    result.update(overrides)
    return result

# scan_type -> (default_profile, mode-factory, service_filter)
_SCAN_MAP = {
    "discovery":            ("it",  discovery_mode,            None),
    "host_discovery":       ("it",  host_discovery_mode,       None),
    "port_scan":            ("it",  port_scan_mode,            None),
    "service_fingerprint":  ("it",  service_fingerprint_mode,  None),
    "assessment":           ("it",  assessment,  None),
    "vuln_scan":            ("it",  assessment,  None),
    "tls_scan":             ("it",  None,        {"tls"}),
    "web_scan":             ("it",  None,        {"web"}),
    "web_tls_scan":         ("it",  None,        {"tls", "web"}),
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


def _string_list(value, field: str) -> list[str]:
    if value is None:
        return []
    values = [value] if isinstance(value, str) else value
    if not isinstance(values, (list, tuple)):
        raise ValueError(f"{field} must be a string or list of strings")
    normalized = []
    for item in values:
        if not isinstance(item, str):
            raise ValueError(f"{field} must contain only strings")
        item = item.strip()
        if item:
            normalized.append(item)
    return list(dict.fromkeys(normalized))


def _targets(params: dict) -> list[str]:
    value = params.get("targets")
    if value is None:
        value = params.get("target")
    if value is None:
        value = params.get("scope_cidrs")
    return _string_list(value, "targets")


def _clamp(val, lo, hi, default):
    """Coerce val to float and clamp to [lo, hi]; fall back to default on junk.
    Defense in depth: the operator's UI sends presets, but a buggy or tampered
    job must never be able to set rate=1e9 and flood a production segment."""
    try:
        return max(lo, min(hi, float(val)))
    except (TypeError, ValueError):
        return default


def _job_runtime_seconds(params: dict) -> float:
    """Return the effective whole-job deadline; callers can only reduce it."""
    return _clamp(
        params.get("max_runtime_seconds"),
        min(1.0, MAX_JOB_SECONDS),
        MAX_JOB_SECONDS,
        MAX_JOB_SECONDS,
    )


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
    """Count unique open network endpoints, not every confirming scanner fact."""
    return len({
        (
            f.get("target"),
            (f.get("proto") or "tcp").lower(),
            int(f["port"]),
        )
        for f in facts
        if (
            f.get("target")
            and f.get("status") == "open"
            and f.get("port") is not None
        )
    })


def _facts_from_cache(cache: WorkflowCache) -> list[dict]:
    return [asdict(entry.result) for entry in cache._store.values()]


def _hosts_from_facts(facts: list[dict]) -> list[dict]:
    """Build promotion-ready hosts without duplicating scanner facts per port."""
    host_map: dict[str, dict] = {}
    port_map: dict[str, dict[tuple[int, str], dict]] = {}
    for fact in facts:
        # Only affirmative network evidence may create an inventory asset.
        # Negative/ambiguous observations such as host-discovery "filtered",
        # closed TCP ports, and unanswered UDP probes are useful run telemetry,
        # but they do not prove that a host exists.
        if fact.get("status") not in {"open", "observed"} or fact.get("error"):
            continue
        target = fact.get("target")
        if not target:
            continue
        data = fact.get("data") or {}
        host = host_map.setdefault(
            target,
            {
                "ip": target,
                "hostname": data.get("hostname") or None,
                "ports": [],
            },
        )
        if not host["hostname"] and data.get("hostname"):
            host["hostname"] = data["hostname"]
        port = fact.get("port")
        if port is None or fact.get("status") not in {"open", "observed"}:
            continue
        proto = fact.get("proto") or "tcp"
        service = data.get("service") or data.get("first_line")
        key = (int(port), proto)
        existing = port_map.setdefault(target, {}).get(key)
        candidate = {
            "port": int(port),
            "protocol": proto,
            "service": service,
        }
        if existing is None or (not existing.get("service") and service):
            port_map[target][key] = candidate

    for target, host in host_map.items():
        host["ports"] = sorted(
            port_map.get(target, {}).values(),
            key=lambda item: (item["port"], item["protocol"]),
        )
    return list(host_map.values())


def _applied_tuning(tuning: dict, job_runtime_seconds: float) -> dict:
    """Serialize effective limits without ever echoing credential values."""
    return {
        "rate": tuning.get("rate"),
        "concurrency": tuning.get("concurrency"),
        "timeout": tuning.get("timeout"),
        "disc_timeout": tuning.get("disc_timeout"),
        "passive_listen_seconds": tuning.get("passive_listen_seconds"),
        "recheck_hours": (
            tuning["force_recheck_after"].total_seconds() / 3600
            if tuning.get("force_recheck_after")
            else None
        ),
        "max_targets": MAX_TARGETS,
        "max_runtime_seconds": job_runtime_seconds,
        "ssh_auth": bool(tuning.get("ssh_creds")),
        "win_auth": bool(tuning.get("win_creds")),
    }


def _build_run_stats(
    facts: list[dict],
    issues: list[dict],
    tuning: dict,
    job_runtime_seconds: float,
    *,
    scope_src: list[str],
    exclude_src: list[str],
    local_scope_src: list[str] | None,
    requested_targets: list[str],
    authorized_targets: list[str],
) -> tuple[dict, list[dict]]:
    """Build one consistent result summary for complete and interrupted runs."""
    successful_facts = [
        fact
        for fact in facts
        if fact.get("status") != "error" and not fact.get("error")
    ]
    hosts = _hosts_from_facts(facts)
    stats = {
        "host_count": len(hosts),
        "open_ports": _count_open_port_facts(facts),
        "fact_count": len(successful_facts),
        "error_count": len(issues),
        "result_count": len(facts),
        "scanners_run": sorted({
            fact.get("scanner", "")
            for fact in facts
            if fact.get("scanner")
        }),
        "applied_tuning": _applied_tuning(tuning, job_runtime_seconds),
        "scope_enforced": {
            "allow": scope_src,
            "exclude": exclude_src,
            "local_allow": local_scope_src,
            "targets_requested": requested_targets,
            "targets_authorized": authorized_targets,
        },
    }
    return stats, hosts


class LeaseLostError(RuntimeError):
    """Raised when Manager fencing revokes the running attempt."""


async def _run_with_cancellation(coro, cancellation_event):
    task = asyncio.create_task(coro)
    try:
        while True:
            done, _ = await asyncio.wait({task}, timeout=0.1)
            if task in done:
                return await task
            if cancellation_event is not None and cancellation_event.is_set():
                task.cancel()
                await asyncio.gather(task, return_exceptions=True)
                raise LeaseLostError("job attempt lease was lost during execution")
    finally:
        if not task.done():
            task.cancel()


def run_scan(scan_type: str, params: dict,
             use_case_id: str | None = None,
             engagement_uuid: str | None = None,
             validated_scope: list[str] | None = None,
             validated_excludes: list[str] | None = None,
             local_allowed_scope: list[str] | None = None,
             cancellation_event=None) -> dict:
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
        local_allowed_scope: optional deployment-local CIDR ceiling. When supplied,
            targets must pass this guard in addition to the engagement allowlist.
    """
    started_at = datetime.now(timezone.utc).isoformat()
    errors: list[str] = []

    if not isinstance(params, dict):
        return _error_result(
            str(scan_type),
            "job params must be an object",
            error_code="invalid_job_params",
            engagement_uuid=engagement_uuid,
            use_case_id=use_case_id,
        )
    if not isinstance(scan_type, str):
        return _error_result(
            str(scan_type),
            "scan_type must be a string",
            error_code="invalid_scan_type",
            engagement_uuid=engagement_uuid,
            use_case_id=use_case_id,
        )

    cfg = _SCAN_MAP.get(scan_type)
    if cfg is None:
        return _error_result(
            scan_type,
            f"unsupported scan_type '{scan_type}'",
            error_code="unsupported_scan_type",
            remediation="Select a scan type advertised by the assigned probe.",
            engagement_uuid=engagement_uuid,
            use_case_id=use_case_id,
            supported=CAPABILITIES,
        )

    default_profile, mode_factory, svc_filter = cfg
    profile = params.get("profile", default_profile)
    if not isinstance(profile, str) or profile not in VALID_PROFILES:
        return _error_result(
            scan_type,
            f"unsupported profile {profile!r}",
            error_code="unsupported_profile",
            remediation=f"Use one of: {', '.join(sorted(VALID_PROFILES))}.",
            engagement_uuid=engagement_uuid,
            use_case_id=use_case_id,
            profile=profile,
        )

    try:
        targets = _targets(params)
    except ValueError as exc:
        return _error_result(
            scan_type,
            str(exc),
            error_code="invalid_targets",
            remediation="Provide IP addresses, CIDRs, hostnames, or IP ranges as strings.",
            engagement_uuid=engagement_uuid,
            use_case_id=use_case_id,
            profile=profile,
        )
    if not targets:
        return _error_result(
            scan_type,
            "no targets/scope provided",
            error_code="targets_missing",
            remediation="Add at least one target inside the engagement scope.",
            engagement_uuid=engagement_uuid,
            use_case_id=use_case_id,
            profile=profile,
        )

    # Expand CIDR/range specs into concrete hosts before scanning. Host discovery
    # connects to each target directly and cannot resolve a CIDR string like
    # "172.18.0.7/32" or "10.0.0.0/24" — every CLI path expands via
    # expand_targets(), but this agent/engine path (manager-issued jobs) did not,
    # so a CIDR-form engagement scope discovered ZERO hosts. ScopeGuard (built
    # from the raw scope_src below) still enforces the authoritative boundary.
    requested_targets = list(targets)
    try:
        expanded = expand_targets(targets, max_hosts=MAX_TARGETS)
        if expanded:
            targets = expanded
    except ValueError as exc:
        return _error_result(
            scan_type,
            str(exc),
            error_code="target_expansion_limit",
            remediation=(
                "Split the authorized scope into smaller jobs. For a genuine large "
                "scope, use the separately governed Masscan validation path."
            ),
            engagement_uuid=engagement_uuid,
            use_case_id=use_case_id,
            profile=profile,
            requested_targets=requested_targets,
        )

    # ScopeGuard: prefer the independently-validated scope (re-validated by agent
    # before this function is called); fall back to manager-provided scope_cidrs;
    # last resort: treat the targets themselves as the allowlist.
    raw_scope = (
        validated_scope
        if validated_scope is not None
        else params.get("scope_cidrs")
    )
    if raw_scope is None:
        raw_scope = targets
    try:
        scope_src = _string_list(raw_scope, "scope_cidrs")
        manager_excludes = _string_list(
            params.get("excluded_cidrs"),
            "excluded_cidrs",
        )
        authoritative_excludes = _string_list(
            validated_excludes,
            "validated_excludes",
        )
    except ValueError as exc:
        return _error_result(
            scan_type,
            str(exc),
            error_code="invalid_scope",
            remediation="Use only string IP, CIDR, hostname, or range entries.",
            engagement_uuid=engagement_uuid,
            use_case_id=use_case_id,
            profile=profile,
        )
    if not scope_src:
        return _error_result(
            scan_type,
            "authoritative engagement scope is empty",
            error_code="scope_empty",
            remediation="Authorize scope on the engagement before assigning a probe.",
            engagement_uuid=engagement_uuid,
            use_case_id=use_case_id,
            profile=profile,
        )
    # Exclusions: authoritative engagement excludes (from agent) merged with any
    # per-job excluded_cidrs the operator set in the UI. ScopeGuard subtracts them.
    # Deduped, order-preserving — the agent may pass the same list via both routes.
    exclude_src = list(dict.fromkeys(
        [*authoritative_excludes, *manager_excludes]
    ))
    scope = ScopeGuard.from_list(scope_src, excludes=exclude_src)
    targets = list(scope.filter(targets))
    if not targets:
        return _error_result(
            scan_type,
            "no requested targets remain inside the authorized scope",
            error_code="no_authorized_targets",
            remediation="Correct the job targets or the engagement allow/exclude rules.",
            engagement_uuid=engagement_uuid,
            use_case_id=use_case_id,
            profile=profile,
            requested_targets=requested_targets,
        )

    local_scope_src: list[str] | None = None
    if local_allowed_scope is not None:
        try:
            local_scope_src = _string_list(local_allowed_scope, "local_allowed_scope")
        except ValueError as exc:
            return _error_result(
                scan_type,
                str(exc),
                error_code="invalid_local_scope",
                remediation="Set PROBE_NETWORK_SEGMENTS to valid IP/CIDR strings.",
                engagement_uuid=engagement_uuid,
                use_case_id=use_case_id,
                profile=profile,
            )
        if not local_scope_src:
            return _error_result(
                scan_type,
                "probe local network ceiling is empty",
                error_code="local_scope_empty",
                remediation="Set PROBE_NETWORK_SEGMENTS before assigning scan jobs.",
                engagement_uuid=engagement_uuid,
                use_case_id=use_case_id,
                profile=profile,
            )
        local_scope = ScopeGuard.from_list(local_scope_src)
        targets = list(local_scope.filter(targets))
        if not targets:
            return _error_result(
                scan_type,
                "no requested targets remain inside the probe's local network ceiling",
                error_code="outside_local_scope",
                remediation="Assign a probe whose PROBE_NETWORK_SEGMENTS covers the target.",
                engagement_uuid=engagement_uuid,
                use_case_id=use_case_id,
                profile=profile,
                requested_targets=requested_targets,
            )

    mode = mode_factory() if mode_factory else service_specific(svc_filter or set())
    cache = WorkflowCache()

    # Translate the operator's job params (scan intensity, OT listen window,
    # re-scan delta, credentials) into engine kwargs. This is what makes the
    # Scanner page's controls drive the actual scan instead of being ignored.
    tuning = _tuning_from_params(params)
    job_runtime_seconds = _job_runtime_seconds(params)
    trace = ExecutionTrace(planned_components(
        profile,
        service_filter=mode.service_filter,
        stop_after_banner=mode.stop_after_banner,
        ssh_enabled=bool(tuning.get("ssh_creds")),
        windows_enabled=bool(tuning.get("win_creds")),
        stage_ceiling=mode.stage_ceiling,
    ))

    try:
        asyncio.run(asyncio.wait_for(
            _run_with_cancellation(
                run_engagement(
                    targets, scope, profile=profile,
                    service_filter=mode.service_filter,
                    stop_after_banner=mode.stop_after_banner,
                    stage_ceiling=mode.stage_ceiling,
                    cache=cache,
                    trace=trace,
                    **tuning,
                ),
                cancellation_event,
            ),
            timeout=job_runtime_seconds,
        ))
    except LeaseLostError as exc:
        error_msg = str(exc)
        trace.finalize("Stopped because the Manager rejected the attempt fence.")
        return _error_result(
            scan_type,
            error_msg,
            error_code="attempt_lease_lost",
            remediation="Wait for the Manager to issue a new fenced attempt.",
            engagement_uuid=engagement_uuid,
            use_case_id=use_case_id,
            profile=profile,
            facts=_facts_from_cache(cache),
            errors=[error_msg],
        )
    except asyncio.TimeoutError:
        error_msg = (
            f"job exceeded the {job_runtime_seconds:g}-second runtime ceiling"
        )
        trace.finalize("Not run because the job runtime ceiling was reached.")
        facts = _facts_from_cache(cache)
        deadline_issue = {
            "code": "job_deadline_exceeded",
            "scanner": ENGINE_ID,
            "message": error_msg,
            "retryable": True,
            "remediation": (
                "Narrow the target set or lower scan intensity; raise "
                "PROBE_MAX_JOB_SECONDS only after capacity review."
            ),
        }
        issues = [*trace.issues, deadline_issue]
        run_stats, hosts = _build_run_stats(
            facts,
            issues,
            tuning,
            job_runtime_seconds,
            scope_src=scope_src,
            exclude_src=exclude_src,
            local_scope_src=local_scope_src,
            requested_targets=requested_targets,
            authorized_targets=targets,
        )
        has_evidence = bool(run_stats["fact_count"])
        return _error_result(
            scan_type,
            error_msg,
            error_code="job_deadline_exceeded",
            remediation=deadline_issue["remediation"],
            engagement_uuid=engagement_uuid,
            use_case_id=use_case_id,
            profile=profile,
            started_at=started_at,
            ok=has_evidence,
            outcome="partial" if has_evidence else "failed",
            degraded=True,
            facts=facts,
            hosts=hosts,
            scanner_runs=trace.as_list(),
            issues=issues,
            run_stats=run_stats,
            errors=[error_msg],
            host_count=run_stats["host_count"],
            service_count=run_stats["open_ports"],
            open_ports=run_stats["open_ports"],
            finding_count=0,
        )
    except Exception as exc:
        error_msg = f"{type(exc).__name__}: {exc}"
        errors.append(error_msg)
        trace.finalize("Not run because the workflow terminated unexpectedly.")
        facts = _facts_from_cache(cache)
        workflow_issue = {
            "code": "workflow_internal_error",
            "scanner": ENGINE_ID,
            "message": error_msg,
            "retryable": False,
            "remediation": "Inspect probe logs and component run states before retrying.",
        }
        issues = [*trace.issues, workflow_issue]
        run_stats, hosts = _build_run_stats(
            facts,
            issues,
            tuning,
            job_runtime_seconds,
            scope_src=scope_src,
            exclude_src=exclude_src,
            local_scope_src=local_scope_src,
            requested_targets=requested_targets,
            authorized_targets=targets,
        )
        has_evidence = bool(run_stats["fact_count"])
        return _error_result(
            scan_type,
            error_msg,
            error_code="workflow_internal_error",
            remediation="Inspect probe logs and component run states before retrying.",
            engagement_uuid=engagement_uuid,
            use_case_id=use_case_id,
            profile=profile,
            started_at=started_at,
            ok=has_evidence,
            outcome="partial" if has_evidence else "failed",
            degraded=True,
            facts=facts,
            hosts=hosts,
            scanner_runs=trace.as_list(),
            issues=issues,
            run_stats=run_stats,
            errors=errors,
            host_count=run_stats["host_count"],
            service_count=run_stats["open_ports"],
            open_ports=run_stats["open_ports"],
            finding_count=0,
        )

    facts = _facts_from_cache(cache)
    issues = trace.issues
    errors.extend(issue["message"] for issue in issues)
    run_stats, hosts_list = _build_run_stats(
        facts,
        issues,
        tuning,
        job_runtime_seconds,
        scope_src=scope_src,
        exclude_src=exclude_src,
        local_scope_src=local_scope_src,
        requested_targets=requested_targets,
        authorized_targets=targets,
    )
    open_ports = run_stats["open_ports"]
    host_count = run_stats["host_count"]
    outcome = (
        "failed"
        if trace.failed
        else "partial"
        if trace.degraded
        else "completed"
    )
    result_error = errors[0] if trace.failed and errors else None

    return {
        "result_schema_version": RESULT_SCHEMA_VERSION,
        "probe_id": PROBE_ID,
        "engagement_uuid": engagement_uuid,
        "use_case_id": use_case_id,
        "scan_type": scan_type,
        "profile": profile,
        "started_at": started_at,
        "finished_at": datetime.now(timezone.utc).isoformat(),
        "ok": not trace.failed,
        "outcome": outcome,
        "degraded": trace.degraded,
        "error": result_error,
        "engine": ENGINE_ID,
        "engine_manifest": _runtime_manifest(),
        "scanner_runs": trace.as_list(),
        "issues": issues,
        "facts": facts,
        "hosts": hosts_list,
        "run_stats": run_stats,
        "errors": errors,
        # legacy flat fields kept for backwards compat with manager ingest
        "host_count": host_count,
        "service_count": open_ports,
        "open_ports": open_ports,
        "finding_count": 0,   # probe never produces findings — manager does
    }

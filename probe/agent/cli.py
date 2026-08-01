#!/usr/bin/env python3
"""
Probe CLI.

The CLI is the operator-facing control plane for deployed probes:
  - authenticate with a manager-issued personal access token,
  - list available scope/use-cases,
  - create engagements when the PAT role permits it,
  - enqueue scans and poll job status,
  - launch the long-running probe daemon using the stored PAT.
"""
from __future__ import annotations

import argparse
import getpass
import json
import os
import stat
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import httpx


class CliError(Exception):
    pass


def _env(name: str, default: str = "") -> str:
    value = os.environ.get(name)
    return value if value is not None else default


def default_config_path() -> Path:
    override = _env("PROBE_CLI_CONFIG")
    if override:
        return Path(override).expanduser()
    base = Path(_env("XDG_CONFIG_HOME") or Path.home() / ".config")
    return base / "vedha" / "probe-cli.json"


def normalize_manager_url(value: str) -> str:
    url = value.strip().rstrip("/")
    if not url:
        raise CliError("manager URL is required")
    if not (url.startswith("http://") or url.startswith("https://")):
        raise CliError("manager URL must start with http:// or https://")
    return url


class ConfigStore:
    def __init__(self, path: Path):
        self.path = path

    def load(self) -> dict[str, Any]:
        try:
            data = json.loads(self.path.read_text())
            if isinstance(data, dict):
                profiles = data.setdefault("profiles", {})
                if not isinstance(profiles, dict):
                    raise CliError(f"invalid CLI config at {self.path}: profiles must be an object")
                return data
        except FileNotFoundError:
            pass
        except json.JSONDecodeError as exc:
            raise CliError(f"invalid CLI config at {self.path}: {exc}")
        return {"profiles": {}}

    def save(self, data: dict[str, Any]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        try:
            os.chmod(self.path.parent, 0o700)
        except OSError:
            pass
        tmp = self.path.with_suffix(self.path.suffix + ".tmp")
        tmp.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
        os.chmod(tmp, stat.S_IRUSR | stat.S_IWUSR)
        tmp.replace(self.path)
        os.chmod(self.path, stat.S_IRUSR | stat.S_IWUSR)

    def get_profile(self, name: str) -> dict[str, Any]:
        return dict(self.load().get("profiles", {}).get(name, {}))

    def set_profile(self, name: str, profile: dict[str, Any]) -> None:
        data = self.load()
        profiles = data.setdefault("profiles", {})
        profiles[name] = profile
        self.save(data)

    def remove_profile(self, name: str) -> bool:
        data = self.load()
        profiles = data.setdefault("profiles", {})
        existed = name in profiles
        profiles.pop(name, None)
        self.save(data)
        return existed


class ManagerClient:
    def __init__(
        self,
        manager_url: str,
        token: str,
        *,
        verify_tls: bool = True,
        ca_bundle: str | None = None,
        timeout: float = 30.0,
    ):
        verify: bool | str = ca_bundle if ca_bundle else verify_tls
        self._client = httpx.Client(
            base_url=normalize_manager_url(manager_url),
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/json",
                "User-Agent": "vedha-probe-cli/1",
            },
            timeout=httpx.Timeout(connect=10.0, read=timeout, write=timeout, pool=30.0),
            verify=verify,
        )

    def request(
        self,
        method: str,
        path: str,
        *,
        json_body: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> Any:
        try:
            response = self._client.request(method, path, json=json_body, params=params)
        except httpx.HTTPError as exc:
            raise CliError(f"manager request failed: {exc}") from exc
        if response.status_code >= 400:
            detail = response.text
            try:
                parsed = response.json()
                detail = parsed.get("detail", parsed)
            except Exception:
                pass
            raise CliError(f"manager returned HTTP {response.status_code}: {detail}")
        if not response.content:
            return {}
        try:
            return response.json()
        except json.JSONDecodeError:
            return response.text


def split_values(values: list[str] | None) -> list[str]:
    out: list[str] = []
    for value in values or []:
        for part in value.split(","):
            item = part.strip()
            if item:
                out.append(item)
    return out


def parse_param_pairs(values: list[str] | None) -> dict[str, Any]:
    params: dict[str, Any] = {}
    for raw in values or []:
        key, sep, value = raw.partition("=")
        if not sep or not key.strip():
            raise CliError(f"invalid --param '{raw}', expected key=value")
        text = value.strip()
        try:
            params[key.strip()] = json.loads(text)
        except json.JSONDecodeError:
            params[key.strip()] = text
    return params


def output(data: Any, *, as_json: bool = False, columns: list[tuple[str, str]] | None = None) -> None:
    if as_json or columns is None:
        print(json.dumps(data, indent=2, sort_keys=True, default=str))
        return
    rows = data if isinstance(data, list) else [data]
    if not rows:
        print("No rows.")
        return
    widths: dict[str, int] = {}
    for key, label in columns:
        widths[key] = len(label)
        for row in rows:
            widths[key] = max(widths[key], len(str(row.get(key, ""))))
    print("  ".join(label.ljust(widths[key]) for key, label in columns))
    print("  ".join("-" * widths[key] for key, _ in columns))
    for row in rows:
        print("  ".join(str(row.get(key, "")).ljust(widths[key]) for key, _ in columns))


def resolve_profile(args: argparse.Namespace) -> dict[str, Any]:
    store = ConfigStore(Path(args.config).expanduser())
    profile = store.get_profile(args.profile)

    manager_url = (
        args.manager
        or _env("PROBE_MANAGER_URL")
        or _env("PLATFORM_URL")
        or profile.get("manager_url")
        or ""
    )
    token = args.pat or _env("PROBE_PAT") or _env("VEDHA_PAT") or profile.get("token") or ""
    verify_tls = profile.get("verify_tls", True)
    if args.insecure:
        verify_tls = False
    ca_bundle = args.ca_bundle or profile.get("ca_bundle")

    if not manager_url:
        raise CliError("not authenticated: run 'probe auth login --manager https://manager.example'")
    if not token:
        raise CliError("not authenticated: run 'probe auth login --pat <token>'")

    return {
        "manager_url": normalize_manager_url(manager_url),
        "token": token,
        "verify_tls": bool(verify_tls),
        "ca_bundle": ca_bundle,
    }


def client_from_args(args: argparse.Namespace) -> ManagerClient:
    profile = resolve_profile(args)
    return ManagerClient(
        profile["manager_url"],
        profile["token"],
        verify_tls=profile["verify_tls"],
        ca_bundle=profile["ca_bundle"],
        timeout=args.timeout,
    )


def cmd_auth_login(args: argparse.Namespace) -> int:
    manager_url = normalize_manager_url(
        args.manager or _env("PROBE_MANAGER_URL") or _env("PLATFORM_URL")
    )
    token = args.pat or _env("PROBE_PAT") or _env("VEDHA_PAT")
    if not token:
        token = getpass.getpass("Personal access token: ").strip()
    if not token:
        raise CliError("personal access token is required")

    client = ManagerClient(
        manager_url,
        token,
        verify_tls=not args.insecure,
        ca_bundle=args.ca_bundle,
        timeout=args.timeout,
    )
    me = client.request("GET", "/auth/me")
    store = ConfigStore(Path(args.config).expanduser())
    store.set_profile(
        args.profile,
        {
            "manager_url": manager_url,
            "token": token,
            "verify_tls": not args.insecure,
            "ca_bundle": args.ca_bundle,
        },
    )
    if args.json:
        output({"authenticated": True, "profile": args.profile, "user": me}, as_json=True)
    else:
        print(f"Authenticated profile '{args.profile}' as {me.get('email') or me.get('user_id')}.")
        print(f"Role: {me.get('role')}  Auth: {me.get('auth_type')}  Scopes: {', '.join(me.get('scopes') or [])}")
        print(f"Config: {Path(args.config).expanduser()}")
    return 0


def cmd_auth_status(args: argparse.Namespace) -> int:
    client = client_from_args(args)
    me = client.request("GET", "/auth/me")
    if args.json:
        output(me, as_json=True)
    else:
        print(f"Authenticated as {me.get('email') or me.get('user_id')}")
        print(f"Tenant: {me.get('tenant_id')}")
        print(f"Role: {me.get('role')}")
        print(f"Auth: {me.get('auth_type')}")
        scopes = me.get("scopes") or []
        if scopes:
            print(f"Scopes: {', '.join(scopes)}")
    return 0


def cmd_auth_logout(args: argparse.Namespace) -> int:
    removed = ConfigStore(Path(args.config).expanduser()).remove_profile(args.profile)
    print(f"Removed profile '{args.profile}'." if removed else f"Profile '{args.profile}' was not configured.")
    return 0


def cmd_whoami(args: argparse.Namespace) -> int:
    return cmd_auth_status(args)


def _doctor_check(checks: list[dict[str, Any]], name: str, fn, *, required: bool = True) -> Any:
    try:
        data = fn()
    except Exception as exc:
        status_text = "fail" if required else "warn"
        checks.append({"name": name, "status": status_text, "detail": str(exc)})
        return None
    checks.append({"name": name, "status": "ok", "detail": data})
    return data


def cmd_doctor(args: argparse.Namespace) -> int:
    profile = resolve_profile(args)
    client = ManagerClient(
        profile["manager_url"],
        profile["token"],
        verify_tls=profile["verify_tls"],
        ca_bundle=profile["ca_bundle"],
        timeout=args.timeout,
    )

    warnings: list[str] = []
    if profile["manager_url"].startswith("http://") and "127.0.0.1" not in profile["manager_url"] \
            and "localhost" not in profile["manager_url"]:
        warnings.append("manager URL uses plain HTTP; production must use HTTPS")
    if not profile["verify_tls"]:
        warnings.append("TLS verification is disabled")
    if not profile["token"].startswith("vpat_"):
        warnings.append("credential is not a vpat_ personal access token")

    checks: list[dict[str, Any]] = []
    _doctor_check(checks, "manager_health", lambda: client.request("GET", "/health"))
    me = _doctor_check(checks, "auth", lambda: client.request("GET", "/auth/me"))
    use_cases = _doctor_check(checks, "use_cases", lambda: client.request("GET", "/agents/use-cases"))
    agents = _doctor_check(checks, "agents", lambda: client.request("GET", "/agents"))

    if args.engagement_id:
        _doctor_check(
            checks,
            "engagement_scope",
            lambda: client.request("GET", f"/engagements/{args.engagement_id}/scope"),
        )

    online_agents = []
    if isinstance(agents, list):
        online_agents = [agent for agent in agents if agent.get("online")]
        if not online_agents and not args.allow_no_agent:
            checks.append({
                "name": "online_agent",
                "status": "fail",
                "detail": "no online probe is available to pick up jobs",
            })
        else:
            checks.append({
                "name": "online_agent",
                "status": "ok" if online_agents else "warn",
                "detail": f"{len(online_agents)} online probe(s)",
            })

    failed = [check for check in checks if check["status"] == "fail"]
    result = {
        "ok": not failed,
        "manager_url": profile["manager_url"],
        "warnings": warnings,
        "checks": checks,
        "summary": {
            "auth_type": me.get("auth_type") if isinstance(me, dict) else None,
            "role": me.get("role") if isinstance(me, dict) else None,
            "scopes": me.get("scopes", []) if isinstance(me, dict) else [],
            "use_case_count": len(use_cases) if isinstance(use_cases, list) else 0,
            "online_agent_count": len(online_agents),
        },
    }

    if args.json:
        output(result, as_json=True)
    else:
        print("Probe Doctor")
        print(f"Manager: {result['manager_url']}")
        for warning in warnings:
            print(f"WARN  {warning}")
        for check in checks:
            print(f"{check['status'].upper():<5} {check['name']}: {check['detail']}")
        print(
            f"Summary: role={result['summary']['role']} "
            f"use_cases={result['summary']['use_case_count']} "
            f"online_agents={result['summary']['online_agent_count']}"
        )
    return 0 if result["ok"] else 1


def cmd_use_cases(args: argparse.Namespace) -> int:
    data = client_from_args(args).request("GET", "/agents/use-cases")
    output(
        data,
        as_json=args.json,
        columns=[
            ("use_case_id", "Use Case"),
            ("display_name", "Name"),
            ("scan_type", "Scan Type"),
            ("profile", "Profile"),
            ("expected_runtime_hint", "Runtime"),
        ],
    )
    return 0


def cmd_agents_list(args: argparse.Namespace) -> int:
    data = client_from_args(args).request("GET", "/agents")
    output(
        data,
        as_json=args.json,
        columns=[
            ("id", "Agent ID"),
            ("name", "Name"),
            ("status", "Status"),
            ("online", "Online"),
            ("location", "Location"),
            ("last_heartbeat", "Last Heartbeat"),
        ],
    )
    return 0


def cmd_engagements_list(args: argparse.Namespace) -> int:
    data = client_from_args(args).request(
        "GET",
        "/engagements",
        params={"page": args.page, "page_size": args.page_size},
    )
    items = data.get("items", data) if isinstance(data, dict) else data
    output(
        items,
        as_json=args.json,
        columns=[
            ("id", "Engagement ID"),
            ("name", "Name"),
            ("status", "Status"),
            ("scope_cidrs", "Scope"),
        ],
    )
    return 0


def cmd_engagements_create(args: argparse.Namespace) -> int:
    scope = split_values(args.scope)
    excluded = split_values(args.exclude)
    if not scope:
        raise CliError("--scope is required")
    body = {
        "name": args.name,
        "scope_cidrs": scope,
        "excluded_cidrs": excluded,
        "rules_of_engagement": {
            "scan_profile": args.scan_profile,
            "cli_created": True,
        },
    }
    data = client_from_args(args).request("POST", "/engagements", json_body=body)
    output(
        data,
        as_json=args.json,
        columns=[
            ("id", "Engagement ID"),
            ("name", "Name"),
            ("status", "Status"),
            ("scope_cidrs", "Scope"),
        ],
    )
    return 0


def cmd_engagements_scope(args: argparse.Namespace) -> int:
    data = client_from_args(args).request("GET", f"/engagements/{args.engagement_id}/scope")
    output(data, as_json=True if args.json else False)
    return 0


def _poll_job(client: ManagerClient, job_id: str, interval: float, timeout: float) -> dict[str, Any]:
    if interval <= 0:
        raise CliError("--poll-interval must be greater than 0")
    if timeout < 0:
        raise CliError("--wait-timeout must be 0 or greater")

    deadline = time.monotonic() + timeout if timeout > 0 else None
    while True:
        data = client.request("GET", f"/agents/jobs/{job_id}")
        status = data.get("status")
        if status in {"completed", "failed"}:
            return data
        if deadline is not None and time.monotonic() >= deadline:
            raise CliError(f"timed out waiting for job {job_id}; last status was {status}")
        time.sleep(interval)


def cmd_scan_run(args: argparse.Namespace) -> int:
    params = parse_param_pairs(args.param)
    targets = split_values(args.target)
    if targets:
        params["targets"] = targets
    if args.ports:
        params["ports"] = args.ports

    body = {
        "engagement_id": args.engagement_id,
        "job_type": args.job_type,
        "use_case_id": args.use_case,
        "params": params,
    }
    client = client_from_args(args)
    created = client.request("POST", "/agents/jobs", json_body=body)
    if args.wait:
        data = _poll_job(client, created["job_id"], args.poll_interval, args.wait_timeout)
    else:
        data = created
    output(
        data,
        as_json=args.json,
        columns=[
            ("job_id", "Job ID"),
            ("job_type", "Job Type"),
            ("use_case_id", "Use Case"),
            ("status", "Status"),
        ],
    )
    return 0


def cmd_scan_status(args: argparse.Namespace) -> int:
    data = client_from_args(args).request("GET", f"/agents/jobs/{args.job_id}")
    output(data, as_json=args.json)
    return 0


def _write_private_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        os.chmod(path.parent, 0o700)
    except OSError:
        pass
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2, sort_keys=True, default=str) + "\n")
    os.chmod(tmp, 0o600)
    tmp.replace(path)
    os.chmod(path, 0o600)


def _fetch_all_findings(client: ManagerClient, engagement_id: str) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    page = 1
    while True:
        data = client.request(
            "GET",
            "/findings",
            params={
                "engagement_id": engagement_id,
                "page": page,
                "page_size": 100,
            },
        )
        batch = data.get("items", []) if isinstance(data, dict) else []
        items.extend(batch)
        total = int(data.get("total", len(items))) if isinstance(data, dict) else len(items)
        if not batch or len(items) >= total:
            return items
        page += 1


def _manager_is_local(url: str) -> bool:
    hostname = (urlparse(url).hostname or "").lower()
    return hostname in {"localhost", "127.0.0.1", "::1"}


def cmd_validate(args: argparse.Namespace) -> int:
    """Run a bounded capability suite and optionally score known ground truth."""
    from agent.validation import (
        resolve_use_cases,
        score_inventory,
        target_address_count,
        validate_ground_truth,
        validate_targets,
    )

    profile = resolve_profile(args)
    if profile["manager_url"].startswith("http://") and not _manager_is_local(
        profile["manager_url"]
    ):
        raise CliError("Probe validation requires HTTPS for a non-local manager")
    if not profile["verify_tls"] and not _manager_is_local(profile["manager_url"]):
        raise CliError("TLS verification cannot be disabled for remote validation")
    if not 1 <= args.repeat <= 10:
        raise CliError("--repeat must be between 1 and 10")
    if args.poll_interval <= 0:
        raise CliError("--poll-interval must be greater than 0")
    if args.wait_timeout <= 0:
        raise CliError("--wait-timeout must be greater than 0")
    if args.settle_seconds < 0:
        raise CliError("--settle-seconds must be 0 or greater")
    if args.strict_ground_truth and not args.ground_truth:
        raise CliError("--strict-ground-truth requires --ground-truth")
    if args.ports:
        from scanner.scanner_base import parse_ports
        try:
            parse_ports(args.ports)
        except ValueError as exc:
            raise CliError(f"invalid --ports value: {exc}") from exc

    targets = split_values(args.target)
    scope_values = split_values(args.scope)
    excluded_values = split_values(args.exclude)
    if args.engagement_id and (scope_values or excluded_values):
        raise CliError("--scope/--exclude cannot be combined with --engagement-id")
    try:
        address_count = target_address_count(targets)
    except ValueError as exc:
        raise CliError(str(exc)) from exc
    if address_count > 4096:
        raise CliError(
            f"targets represent {address_count} addresses; the Probe hard limit is 4096"
        )
    if address_count > 256 and not args.allow_large_targets:
        raise CliError(
            f"targets represent {address_count} addresses; capability validation "
            "defaults to at most 256. Narrow the target or use --allow-large-targets"
        )
    try:
        selected_use_cases = resolve_use_cases(args.suite, args.use_case)
    except ValueError as exc:
        raise CliError(str(exc)) from exc

    client = ManagerClient(
        profile["manager_url"],
        profile["token"],
        verify_tls=profile["verify_tls"],
        ca_bundle=profile["ca_bundle"],
        timeout=args.timeout,
    )
    me = client.request("GET", "/auth/me")
    scopes = set(me.get("scopes") or [])
    required_scopes = {"probe:read", "probe:write", "engagement:read"}
    if not args.engagement_id:
        required_scopes.add("engagement:write")
        if me.get("role") not in {"admin", "manager"}:
            raise CliError(
                "creating a validation engagement requires an admin or manager PAT"
            )
    missing_scopes = sorted(required_scopes - scopes)
    if missing_scopes:
        raise CliError(
            "PAT is missing required scopes: " + ", ".join(missing_scopes)
        )

    available_rows = client.request("GET", "/agents/use-cases")
    available = {
        row.get("use_case_id"): row
        for row in available_rows
        if isinstance(row, dict) and row.get("use_case_id")
    }
    unknown = [value for value in selected_use_cases if value not in available]
    if unknown:
        raise CliError(
            "manager does not support selected use-cases: " + ", ".join(unknown)
        )

    agents = client.request("GET", "/agents")
    online_agents = [
        agent for agent in agents
        if isinstance(agent, dict) and agent.get("online")
    ]
    if not online_agents:
        raise CliError("no online Probe is available for validation")

    engagement = None
    if args.engagement_id:
        engagement = client.request("GET", f"/engagements/{args.engagement_id}")
        scope_data = client.request(
            "GET", f"/engagements/{args.engagement_id}/scope"
        )
        engagement_id = args.engagement_id
        scan_profile = (
            (engagement.get("rules_of_engagement") or {}).get("scan_profile")
            or args.scan_profile
        )
    else:
        if not scope_values:
            raise CliError("--scope is required when --engagement-id is not supplied")
        scope_data = {
            "scope_cidrs": scope_values,
            "excluded_cidrs": excluded_values,
        }
        engagement_id = None
        scan_profile = args.scan_profile

    if scan_profile == "ot" and selected_use_cases != ["uc_ot_passive"]:
        raise CliError(
            "OT engagements are passive-only; use --suite ot-passive by itself"
        )
    if scan_profile != "ot" and "uc_ot_passive" in selected_use_cases:
        raise CliError("uc_ot_passive requires an engagement with scan profile 'ot'")
    try:
        validate_targets(
            targets,
            scope_data.get("scope_cidrs") or [],
            scope_data.get("excluded_cidrs") or [],
        )
    except ValueError as exc:
        raise CliError(str(exc)) from exc

    reachable_agents = []
    for agent in online_agents:
        segments = agent.get("network_segments") or []
        if not segments:
            reachable_agents.append(agent)
            continue
        try:
            validate_targets(targets, segments, [])
        except ValueError:
            continue
        reachable_agents.append(agent)
    if not reachable_agents:
        raise CliError(
            "no online Probe declares network segments that cover every target"
        )
    if len(reachable_agents) > 1 and not args.allow_multiple_agents:
        names = ", ".join(
            str(agent.get("name") or agent.get("id"))
            for agent in reachable_agents
        )
        raise CliError(
            "multiple Probes can reach the targets and jobs cannot currently be "
            f"pinned to one Probe ({names}); stop the others or use "
            "--allow-multiple-agents"
        )
    for use_case_id in selected_use_cases:
        scan_type = available[use_case_id].get("scan_type")
        if not any(
            scan_type in set(agent.get("capabilities") or [])
            for agent in reachable_agents
        ):
            raise CliError(
                f"no reachable online Probe advertises capability {scan_type!r} "
                f"required by {use_case_id}"
            )

    ground_truth = None
    if args.ground_truth:
        try:
            ground_truth = validate_ground_truth(
                json.loads(Path(args.ground_truth).read_text())
            )
            validate_targets(
                [host["ip"] for host in ground_truth["hosts"]],
                scope_data.get("scope_cidrs") or [],
                scope_data.get("excluded_cidrs") or [],
            )
            validate_targets(
                [host["ip"] for host in ground_truth["hosts"]],
                targets,
                [],
            )
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            raise CliError(f"invalid ground truth: {exc}") from exc

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output_dir = Path(args.output_dir or f"validation-results/{timestamp}")
    plan = {
        "manager_url": profile["manager_url"],
        "engagement_id": engagement_id,
        "engagement_name": args.engagement_name,
        "scan_profile": scan_profile,
        "scope_cidrs": scope_data.get("scope_cidrs") or [],
        "excluded_cidrs": scope_data.get("excluded_cidrs") or [],
        "targets": targets,
        "use_cases": selected_use_cases,
        "repeat": args.repeat,
        "ports": args.ports,
        "online_probes": [
            {
                "id": agent.get("id"),
                "name": agent.get("name"),
                "capabilities": agent.get("capabilities") or [],
            }
            for agent in reachable_agents
        ],
        "ground_truth": str(Path(args.ground_truth)) if args.ground_truth else None,
        "output_dir": str(output_dir),
    }
    if args.dry_run:
        output({"dry_run": True, "plan": plan}, as_json=args.json)
        return 0
    if output_dir.exists():
        raise CliError(
            f"output directory already exists: {output_dir}; choose a new --output-dir"
        )
    if not args.confirm_authorized:
        raise CliError(
            "refusing to send scan traffic without --confirm-authorized; "
            "use --dry-run to review the plan first"
        )

    if engagement_id is None:
        created = client.request(
            "POST",
            "/engagements",
            json_body={
                "name": args.engagement_name,
                "scope_cidrs": scope_data["scope_cidrs"],
                "excluded_cidrs": scope_data["excluded_cidrs"],
                "rules_of_engagement": {
                    "scan_profile": scan_profile,
                    "cli_created": True,
                    "probe_validation": True,
                },
            },
        )
        engagement_id = str(created["id"])
        plan["engagement_id"] = engagement_id

    output_dir.mkdir(parents=True, exist_ok=False)
    os.chmod(output_dir, 0o700)
    _write_private_json(output_dir / "plan.json", plan)

    jobs: list[dict[str, Any]] = []
    failed_jobs = 0
    for run_number in range(1, args.repeat + 1):
        for use_case_id in selected_use_cases:
            params: dict[str, Any] = {"targets": targets}
            if args.ports:
                params["ports"] = args.ports
            created = client.request(
                "POST",
                "/agents/jobs",
                json_body={
                    "engagement_id": engagement_id,
                    "job_type": "discovery",
                    "use_case_id": use_case_id,
                    "params": params,
                },
            )
            job = _poll_job(
                client,
                str(created["job_id"]),
                args.poll_interval,
                args.wait_timeout,
            )
            record = {
                "run": run_number,
                "use_case_id": use_case_id,
                **job,
            }
            jobs.append(record)
            _write_private_json(
                output_dir / f"{run_number:02d}-{use_case_id}.json",
                record,
            )
            if job.get("status") != "completed":
                failed_jobs += 1

    if args.settle_seconds:
        time.sleep(args.settle_seconds)
    assets = client.request("GET", f"/engagements/{engagement_id}/assets")
    findings = _fetch_all_findings(client, engagement_id)
    _write_private_json(output_dir / "assets.json", assets)
    _write_private_json(output_dir / "findings.json", findings)

    fact_counts: dict[str, list[int | None]] = {}
    for job in jobs:
        result = job.get("result") or {}
        fact_counts.setdefault(job["use_case_id"], []).append(result.get("fact_count"))
    repeatability = {
        use_case_id: {
            "fact_counts": counts,
            "stable_fact_count": len(set(counts)) == 1,
        }
        for use_case_id, counts in fact_counts.items()
    }

    accuracy = (
        score_inventory(ground_truth, assets, findings)
        if ground_truth is not None else {
            "scored": False,
            "reason": "no --ground-truth file was supplied",
        }
    )
    summary = {
        "ok": failed_jobs == 0,
        "engagement_id": engagement_id,
        "output_dir": str(output_dir),
        "jobs_total": len(jobs),
        "jobs_failed": failed_jobs,
        "repeatability": repeatability,
        "accuracy": accuracy,
        "asset_count": len(assets),
        "finding_count": len(findings),
    }

    if args.strict_ground_truth and ground_truth is not None:
        inaccurate = [
            name for name, metric in accuracy.items()
            if isinstance(metric, dict)
            and metric.get("scored")
            and (metric.get("false_positive") or metric.get("false_negative"))
        ]
        if inaccurate:
            summary["ok"] = False
            summary["accuracy_failures"] = inaccurate
    _write_private_json(output_dir / "summary.json", summary)
    output(summary, as_json=args.json)
    return 0 if summary["ok"] else 1


def cmd_daemon_run(args: argparse.Namespace) -> int:
    profile = resolve_profile(args)
    os.environ["PLATFORM_URL"] = profile["manager_url"]
    os.environ["OPERATOR_TOKEN"] = profile["token"]
    os.environ["VERIFY_TLS"] = "true" if profile["verify_tls"] else "false"
    if profile["ca_bundle"]:
        os.environ["PROBE_CA_BUNDLE"] = str(profile["ca_bundle"])
    if args.name:
        os.environ["PROBE_NAME"] = args.name
    if args.location:
        os.environ["PROBE_LOCATION"] = args.location
    segments = split_values(args.segment)
    if segments:
        os.environ["PROBE_NETWORK_SEGMENTS"] = ",".join(segments)

    from agent.agent import main as agent_main
    agent_main()
    return 0


def build_parser() -> argparse.ArgumentParser:
    def add_json_flag(command_parser: argparse.ArgumentParser) -> None:
        command_parser.add_argument(
            "--json",
            action="store_true",
            default=argparse.SUPPRESS,
            help="Emit JSON",
        )

    parser = argparse.ArgumentParser(prog="probe", description="Vedha Probe CLI")
    parser.add_argument("--profile", default=_env("PROBE_PROFILE", "default"), help="CLI profile name")
    parser.add_argument("--config", default=str(default_config_path()), help="CLI config path")
    parser.add_argument("--manager", help="Manager base URL, for example https://manager.example")
    parser.add_argument("--pat", help="Personal access token. Prefer PROBE_PAT for automation.")
    parser.add_argument("--insecure", action="store_true", help="Disable TLS verification for development only")
    parser.add_argument("--ca-bundle", help="CA bundle path for private manager TLS")
    parser.add_argument("--timeout", type=float, default=30.0, help="HTTP timeout in seconds")
    parser.add_argument("--json", action="store_true", help="Emit JSON")

    sub = parser.add_subparsers(dest="command", required=True)

    auth = sub.add_parser("auth", help="Authenticate and manage local CLI auth")
    auth_sub = auth.add_subparsers(dest="auth_command", required=True)
    auth_login = auth_sub.add_parser("login", help="Store a manager PAT in the local CLI profile")
    auth_login.add_argument("--manager", default=argparse.SUPPRESS, help="Manager base URL")
    auth_login.add_argument("--pat", default=argparse.SUPPRESS, help="Personal access token")
    auth_login.add_argument("--insecure", action="store_true", default=argparse.SUPPRESS,
                            help="Disable TLS verification for development only")
    auth_login.add_argument("--ca-bundle", default=argparse.SUPPRESS,
                            help="CA bundle path for private manager TLS")
    add_json_flag(auth_login)
    auth_login.set_defaults(func=cmd_auth_login)
    auth_status = auth_sub.add_parser("status", help="Show authenticated identity")
    add_json_flag(auth_status)
    auth_status.set_defaults(func=cmd_auth_status)
    auth_logout = auth_sub.add_parser("logout", help="Remove the local CLI profile")
    auth_logout.set_defaults(func=cmd_auth_logout)

    whoami = sub.add_parser("whoami", help="Show authenticated identity")
    add_json_flag(whoami)
    whoami.set_defaults(func=cmd_whoami)

    doctor = sub.add_parser("doctor", help="Run pre-scan manager/auth/probe checks")
    doctor.add_argument("--engagement-id", help="Also verify authoritative scope for this engagement")
    doctor.add_argument("--allow-no-agent", action="store_true",
                        help="Warn instead of failing when no online probe is available")
    add_json_flag(doctor)
    doctor.set_defaults(func=cmd_doctor)

    use_cases = sub.add_parser("use-cases", help="List scan use-cases available to probes")
    add_json_flag(use_cases)
    use_cases.set_defaults(func=cmd_use_cases)

    agents = sub.add_parser("agents", help="Inspect registered probes")
    agents_sub = agents.add_subparsers(dest="agents_command", required=True)
    agents_list = agents_sub.add_parser("list", help="List registered probes")
    add_json_flag(agents_list)
    agents_list.set_defaults(func=cmd_agents_list)

    engagements = sub.add_parser("engagements", help="Manage scan engagements")
    eng_sub = engagements.add_subparsers(dest="engagements_command", required=True)
    eng_list = eng_sub.add_parser("list", help="List engagements")
    eng_list.add_argument("--page", type=int, default=1)
    eng_list.add_argument("--page-size", type=int, default=20)
    add_json_flag(eng_list)
    eng_list.set_defaults(func=cmd_engagements_list)
    eng_create = eng_sub.add_parser("create", help="Create an engagement")
    eng_create.add_argument("--name", required=True)
    eng_create.add_argument("--scope", action="append", required=True, help="CIDR/IP scope. Repeat or comma-separate.")
    eng_create.add_argument("--exclude", action="append", help="CIDR/IP exclusions. Repeat or comma-separate.")
    eng_create.add_argument("--scan-profile", choices=["it", "iot", "ot"], default="it")
    add_json_flag(eng_create)
    eng_create.set_defaults(func=cmd_engagements_create)
    eng_scope = eng_sub.add_parser("scope", help="Show authoritative engagement scope")
    eng_scope.add_argument("engagement_id")
    add_json_flag(eng_scope)
    eng_scope.set_defaults(func=cmd_engagements_scope)

    scan = sub.add_parser("scan", help="Dispatch and inspect probe scan jobs")
    scan_sub = scan.add_subparsers(dest="scan_command", required=True)
    scan_run = scan_sub.add_parser("run", help="Enqueue a probe scan job")
    scan_run.add_argument("--engagement-id", required=True)
    scan_run.add_argument("--use-case", default="uc_discovery_only")
    scan_run.add_argument("--job-type", choices=["discovery", "lateral", "cloud_scan"], default="discovery")
    scan_run.add_argument("--target", action="append", help="Target override. Repeat or comma-separate.")
    scan_run.add_argument("--ports", help="Port expression understood by the probe, for example 1-1024")
    scan_run.add_argument("--param", action="append", help="Extra job param as key=value. JSON values are accepted.")
    scan_run.add_argument("--wait", action="store_true", help="Poll until the job completes or fails")
    scan_run.add_argument("--poll-interval", type=float, default=5.0)
    scan_run.add_argument("--wait-timeout", type=float, default=1800.0, help="Seconds; 0 waits forever")
    add_json_flag(scan_run)
    scan_run.set_defaults(func=cmd_scan_run)
    scan_status = scan_sub.add_parser("status", help="Show scan job status")
    scan_status.add_argument("job_id")
    add_json_flag(scan_status)
    scan_status.set_defaults(func=cmd_scan_status)

    validate = sub.add_parser(
        "validate",
        help="Run a controlled Probe capability and accuracy validation",
    )
    validate.add_argument("--engagement-id", help="Use an existing engagement")
    validate.add_argument(
        "--engagement-name",
        default="Probe Capability Validation",
        help="Name used when creating a validation engagement",
    )
    validate.add_argument(
        "--scope",
        action="append",
        help="Authorized CIDR/IP for a new engagement. Repeat or comma-separate.",
    )
    validate.add_argument(
        "--exclude",
        action="append",
        help="Excluded CIDR/IP for a new engagement. Repeat or comma-separate.",
    )
    validate.add_argument(
        "--target",
        action="append",
        required=True,
        help="Target IP/CIDR. Repeat or comma-separate.",
    )
    validate.add_argument(
        "--scan-profile",
        choices=["it", "iot", "ot"],
        default="it",
    )
    validate.add_argument(
        "--suite",
        action="append",
        choices=[
            "baseline", "web", "infrastructure", "inventory",
            "exposure", "full", "ot-passive",
        ],
        help="Capability suite. Repeat to combine. Default: baseline.",
    )
    validate.add_argument(
        "--use-case",
        action="append",
        help="Additional manager-supported use-case ID. Repeat as needed.",
    )
    validate.add_argument("--ports", help="Optional port expression, for example 22,80,443")
    validate.add_argument(
        "--repeat",
        type=int,
        default=3,
        help="Runs per use-case for repeatability (1-10; default 3)",
    )
    validate.add_argument("--ground-truth", help="Ground-truth JSON file")
    validate.add_argument(
        "--strict-ground-truth",
        action="store_true",
        help="Fail if any scored expected/observed item differs",
    )
    validate.add_argument("--output-dir", help="New private results directory")
    validate.add_argument("--poll-interval", type=float, default=5.0)
    validate.add_argument("--wait-timeout", type=float, default=3600.0)
    validate.add_argument(
        "--settle-seconds",
        type=float,
        default=5.0,
        help="Wait for asset/finding processing after jobs finish",
    )
    validate.add_argument(
        "--allow-multiple-agents",
        action="store_true",
        help="Accept that jobs may be handled by different online Probes",
    )
    validate.add_argument(
        "--allow-large-targets",
        action="store_true",
        help="Allow validation targets larger than 256 addresses (hard limit 4096)",
    )
    validate.add_argument(
        "--confirm-authorized",
        action="store_true",
        help="Confirm written authorization to send the planned scan traffic",
    )
    validate.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate and print the plan without creating or scanning",
    )
    add_json_flag(validate)
    validate.set_defaults(func=cmd_validate)

    daemon = sub.add_parser("daemon", help="Run the long-lived probe process")
    daemon_sub = daemon.add_subparsers(dest="daemon_command", required=True)
    daemon_run = daemon_sub.add_parser("run", help="Start probe daemon using the stored PAT")
    daemon_run.add_argument("--name", help="Probe display name")
    daemon_run.add_argument("--location", help="Probe location label")
    daemon_run.add_argument("--segment", action="append", help="Reachable CIDR segment. Repeat or comma-separate.")
    daemon_run.set_defaults(func=cmd_daemon_run)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except CliError as exc:
        print(f"probe: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

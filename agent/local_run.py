"""
local_run.py — run the probe's REAL pipeline (workflow.run_engagement) directly on
this host, one use case at a time, WITHOUT the manager. This ships inside the probe
and is exposed as a first-class CLI subcommand of the production entrypoint:

    python -m agent.agent local-run <target> [profile] [stage] [service_filter]

  profile        : it | iot | ot                       (default: it)
  stage          : host_discovery | port_scan | service_banner | deep_scan
                   ('-' or omitted = full deep_scan)
  service_filter : comma list to isolate deep branches, e.g. tls,web | smb | udp

Ports default to a fast [22, 80, 443] probe; override with PROBE_LOCAL_PORTS
("full" = the profile's whole catalog, or a list/range like "445,161" / "1-65535").
Scope is read from PROBE_SCOPE_FILE (default /tmp/s.txt) and MUST contain the target.

This never touches the manager — it is an on-box diagnostic / LAN-validation path
that exercises the exact engine the production probe runs. For the manager-connected
flow use the daemon (`python -m agent.agent`) or `./probe validate ...`.
"""
from __future__ import annotations

import asyncio
import json
import os
import sys

from scanner.scanner_base import ScopeGuard
from workflow.gates import PROFILE_PORTS          # canonical profile catalog (it/iot/ot)
from workflow.modes import STAGE_ORDER, VALID_SERVICES
from workflow.workflow_engine import run_engagement

VALID_PROFILES = tuple(PROFILE_PORTS)             # ("it", "iot", "ot") — single source of truth
_FULL_STAGE_SENTINELS = ("-", "")                 # explicit "no ceiling = full deep_scan"
_PROG = "python -m agent.agent local-run"


def _scope_file() -> str:
    return os.environ.get("PROBE_SCOPE_FILE", "/tmp/s.txt")


def _ports_from_env():
    """Resolve the port set from PROBE_LOCAL_PORTS.

      unset      → [22, 80, 443]   (fast default)
      full       → None            (engine scans the profile's full port catalog)
      "445,161"  → those ports
      "1-65535"  → an inclusive range (for a true full-port audit)
    Comma-separated ranges/ports may be mixed, e.g. "22,80,443,8000-8100".
    """
    raw = os.environ.get("PROBE_LOCAL_PORTS", "").strip()
    if not raw:
        return [22, 80, 443]
    if raw.lower() == "full":
        return None
    ports: list[int] = []
    for part in (p.strip() for p in raw.split(",")):
        if not part:
            continue
        if "-" in part:
            lo, hi = (int(x) for x in part.split("-", 1))
            ports.extend(range(lo, hi + 1))
        else:
            ports.append(int(part))
    return sorted(set(ports)) or [22, 80, 443]


def _clean(d):
    """Drop internal bookkeeping keys (_collected_at, _via…) for readable output."""
    if not d:
        return d
    return {k: v for k, v in d.items() if not k.startswith("_")}


def _port_label(port: int, pf) -> str:
    """Render a port fact unambiguously: '445/tcp open', '11211/udp open|filtered
    (uncertain)'. A UDP no-reply is only 'open|filtered' — surfacing proto + state
    prevents reading it as a confirmed live TCP service."""
    proto = getattr(pf, "proto", "tcp")
    status = getattr(pf, "status", "open")
    certainty = getattr(pf, "certainty", "")
    if certainty == "uncertain" and status == "open":
        status = "open|filtered"                  # UDP ambiguity — not a confirmed service
    label = f"{port}/{proto} {status}"
    if certainty and certainty != "deterministic":
        label += f" ({certainty})"
    return label


def summarize(a) -> dict:
    if a is None:
        return {"note": "target not in scope / no asset produced"}
    return {
        "alive": a.last_seen_alive is not None,
        "open_ports": [_port_label(p, pf) for p, pf in sorted(a.open_ports.items())],
        "services": {p: (v.get("service") or v.get("product")) for p, v in a.services.items()},
        "os_fact": getattr(a, "os_fact", None),        # from os_fingerprint (Gate 4b), if wired
        "enrichment": getattr(a, "enrichment", None),  # from service_enum   (Gate 5a), if wired
        # Deep-branch findings — full facts, not just a port list or a boolean.
        "tls": {p: _clean(v) for p, v in a.tls_facts.items()},
        "web": {p: _clean(v) for p, v in a.web_facts.items()},
        "smb": _clean(a.smb_state),
        "snmp": {p: _clean(v) for p, v in a.snmp_state.items()},
        "db": {p: _clean(v) for p, v in a.db_facts.items()},
        "ai": {p: _clean(v) for p, v in a.ai_facts.items()},
    }


def _usage_error(msg: str) -> int:
    """Actionable input error on stderr → exit code 2. No traceback: this is
    operator input error, not an internal crash."""
    print(f"error: {msg}\n", file=sys.stderr)
    print(f"usage: {_PROG} <target> [profile] [stage] [service_filter]", file=sys.stderr)
    print(f"  profile        : {' | '.join(VALID_PROFILES)}   (default: it)", file=sys.stderr)
    print(f"  stage          : {' | '.join(STAGE_ORDER)}   ('-' = full deep_scan)", file=sys.stderr)
    print(f"  service_filter : {', '.join(sorted(VALID_SERVICES))}   (comma-separated)", file=sys.stderr)
    return 2


def _parse_args(args: list[str]) -> tuple[str, str, str | None, set[str] | None]:
    """Validate positional args (args[0]=target, [1]=profile, [2]=stage, [3]=filter)
    at the boundary. Raises ValueError with an actionable, corrected-command message
    so a typo never reaches the engine as a raw traceback."""
    target = args[0].strip()
    if not target:
        raise ValueError("target (argument 1) is empty")

    profile = (args[1].strip() if len(args) > 1 and args[1].strip() else "it")
    if profile not in VALID_PROFILES:
        hint = (f"  — '{profile}' is a STAGE, not a profile; did you mean: "
                f"{target} it {profile}?") if profile in STAGE_ORDER else ""
        raise ValueError(f"unknown profile {profile!r}; valid: {', '.join(VALID_PROFILES)}{hint}")

    raw_stage = args[2].strip() if len(args) > 2 else None
    stage = None if raw_stage in _FULL_STAGE_SENTINELS else raw_stage
    if stage is not None and stage not in STAGE_ORDER:
        hint = ""
        if stage in VALID_PROFILES:
            svc = args[3].strip() if len(args) > 3 and args[3].strip() else "service_banner"
            hint = (f"\n  '{stage}' is a PROFILE, not a stage — you likely have an extra "
                    f"profile arg. Did you mean:\n      {target} {stage} {svc}")
        raise ValueError(
            f"unknown stage {stage!r}; valid: {', '.join(STAGE_ORDER)} (or '-' = full).{hint}"
        )

    svc = None
    if len(args) > 3 and args[3].strip():
        svc = {s.strip() for s in args[3].split(",") if s.strip()}
        unknown = svc - VALID_SERVICES
        if unknown:
            raise ValueError(
                f"unknown service filter(s): {', '.join(sorted(unknown))}; "
                f"valid: {', '.join(sorted(VALID_SERVICES))}"
            )
    return target, profile, stage, svc


async def _main(args: list[str]) -> int:
    if not args:
        print(__doc__)
        return 2

    # 1) Validate operator input at the boundary — fail fast, no engine traceback.
    try:
        target, profile, stage, svc = _parse_args(args)
    except ValueError as exc:
        return _usage_error(str(exc))

    # 2) The scope allowlist is a hard precondition; guide on a missing file.
    scope_file = _scope_file()
    if not os.path.exists(scope_file):
        return _usage_error(
            f"scope file {scope_file!r} not found — create it with the target in scope:\n"
            f"      echo \"{target}/32\" > {scope_file}\n"
            f"  (or point PROBE_SCOPE_FILE at another allowlist)"
        )
    scope = ScopeGuard.from_file(scope_file)

    port_override = _ports_from_env()
    kw = dict(profile=profile, timeout=3.0, disc_timeout=1.5)
    if port_override is not None:
        kw["port_override"] = port_override
    if stage:
        kw["stage_ceiling"] = stage
    if svc:
        kw["service_filter"] = svc

    # 3) A remaining ValueError from the engine is input rejection (e.g. bad scope),
    #    not a bug — surface it cleanly. Unexpected errors still raise a traceback.
    try:
        assets = await run_engagement([target], scope, **kw)
    except ValueError as exc:
        return _usage_error(f"engine rejected the run: {exc}")

    print(json.dumps(summarize(assets.get(target)), default=str, indent=2))
    return 0


def run(args: list[str]) -> int:
    """Synchronous entrypoint for the `local-run` CLI subcommand."""
    return asyncio.run(_main(args))

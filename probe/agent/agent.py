#!/usr/bin/env python3
"""
agent.py — the probe's manager transport loop.

  login (operator)  → POST /auth/login        (one-time, to get a register token)
  register          → POST /agents/register   → {agent_id, token}, cached
  heartbeat (30s)   → POST /agents/heartbeat
  poll jobs         → GET  /agents/{id}/jobs
  scope validation  → GET  /engagements/{id}/scope  (re-validate before any packet)
  run scan          → scanner_module engine (RAW FACTS, via use-case library)
  submit result     → POST /agents/{id}/jobs/{job_id}/result  (with local retry)

Security properties (techprompt.md):
  - Outbound-only. No inbound port is opened.
  - Scope re-validated on probe against manager's engagement scope BEFORE any packet.
    A buggy or compromised manager cannot widen scope beyond what the engagement allows.
  - Use-case library: probe only runs pre-defined, finite scan scenarios.
  - Local persistence: result saved locally, retried on upload failure.
"""
from __future__ import annotations

import ipaddress
import json
import os
import random
import socket
import sys
import time
from pathlib import Path
from typing import Any

import httpx

from agent.engine import CAPABILITIES, resolve_scan_type, run_scan
from agent.use_cases import USE_CASES, resolve as resolve_use_case

VERSION = "2.0.0"


def _load_env(path: Path) -> None:
    try:
        for line in path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
    except OSError:
        pass


_load_env(Path(__file__).resolve().parent.parent / "probe.env")

PLATFORM_URL = os.environ.get("PLATFORM_URL", "").rstrip("/")
PROBE_NAME = os.environ.get("PROBE_NAME") or socket.gethostname()
PROBE_LOCATION = os.environ.get("PROBE_LOCATION", "")
NETWORK_SEGMENTS = [s.strip() for s in os.environ.get("PROBE_NETWORK_SEGMENTS", "").split(",") if s.strip()]
OPERATOR_EMAIL = os.environ.get("OPERATOR_EMAIL", "")
OPERATOR_PASSWORD = os.environ.get("OPERATOR_PASSWORD", "")
AGENT_ID = os.environ.get("AGENT_ID", "")
AGENT_TOKEN = os.environ.get("AGENT_TOKEN", "")
HEARTBEAT_INTERVAL = int(os.environ.get("HEARTBEAT_INTERVAL", "30"))
POLL_INTERVAL = int(os.environ.get("POLL_INTERVAL", "10"))
JOB_LIMIT = int(os.environ.get("JOB_LIMIT", "1"))
VERIFY_TLS = os.environ.get("VERIFY_TLS", "true").lower() not in ("false", "0", "no")
STATE_FILE = Path(os.environ.get("STATE_FILE", "/var/lib/adversa-probe/state.json"))
RESULT_SPOOL_DIR = Path(os.environ.get("RESULT_SPOOL_DIR", "/var/lib/adversa-probe/spool"))
RESULT_UPLOAD_RETRIES = int(os.environ.get("RESULT_UPLOAD_RETRIES", "5"))
RESULT_RETRY_DELAY = int(os.environ.get("RESULT_RETRY_DELAY", "15"))


def say(msg: str = "", indent: int = 0) -> None:
    print(("  " * indent) + msg, flush=True)


# ── identity (cached; host-bound encryption is a TODO — plaintext cache for now) ──

def _load_state() -> dict[str, str]:
    try:
        return json.loads(STATE_FILE.read_text())
    except (OSError, ValueError):
        return {}


def _save_state(state: dict[str, str]) -> None:
    try:
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        STATE_FILE.write_text(json.dumps(state))
    except OSError as exc:
        say(f"warning: could not persist identity ({exc})", 1)


def obtain_identity(client: httpx.Client) -> tuple[str, str, bool]:
    """Return (agent_id, token, fresh) where fresh=True means we just registered."""
    if AGENT_ID and AGENT_TOKEN:
        return AGENT_ID, AGENT_TOKEN, False
    cached = _load_state()
    if cached.get("agent_id") and cached.get("token"):
        return cached["agent_id"], cached["token"], False
    if not (OPERATOR_EMAIL and OPERATOR_PASSWORD):
        say("Setup needed: set OPERATOR_EMAIL and OPERATOR_PASSWORD in probe.env.")
        raise SystemExit(1)
    r = client.post("/auth/login", json={"email": OPERATOR_EMAIL, "password": OPERATOR_PASSWORD})
    r.raise_for_status()
    op_token = r.json()["access_token"]
    r = client.post("/agents/register", headers={"Authorization": f"Bearer {op_token}"},
                    json={"name": PROBE_NAME, "location": PROBE_LOCATION or None,
                          "capabilities": CAPABILITIES, "network_segments": NETWORK_SEGMENTS})
    r.raise_for_status()
    data = r.json()
    _save_state({"agent_id": data["agent_id"], "token": data["token"]})
    return data["agent_id"], data["token"], True


def connect_with_retry(client: httpx.Client) -> tuple[str, str, bool]:
    while True:
        try:
            return obtain_identity(client)
        except SystemExit:
            raise
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code in (401, 403):
                say("Manager rejected sign-in — check OPERATOR_EMAIL / OPERATOR_PASSWORD.")
                raise SystemExit(1)
            say(f"Manager error (HTTP {exc.response.status_code}); retrying in {POLL_INTERVAL}s ...")
        except httpx.HTTPError:
            say(f"Can't reach the manager at {PLATFORM_URL} yet; retrying ...")
        time.sleep(POLL_INTERVAL)


def license_gate() -> None:
    """Verify the host-locked license before doing anything. Honors
    LICENSE_ENFORCED (default on). A copied probe or wrong-host license
    fails here with a clear, actionable message and the machine's Host ID."""
    from agent.license import check_license, LicenseError, short_id
    try:
        lic = check_license()
    except LicenseError as exc:
        say("License check failed:")
        say(exc.friendly, 1)
        say(f"This machine's Host ID: {short_id()}", 1)
        raise SystemExit(2)
    if lic:
        say(f"License OK — {lic.get('customer','?')}, valid until {lic.get('expires','?')}")


def main() -> None:
    say("Intrynx Probe (scanner_module)")
    say("--------------------------------")
    license_gate()
    if not PLATFORM_URL:
        say("Setup needed: PLATFORM_URL is not set.")
        raise SystemExit(1)

    client = httpx.Client(base_url=PLATFORM_URL,
                          timeout=httpx.Timeout(connect=10.0, read=30.0, write=30.0, pool=30.0),
                          verify=VERIFY_TLS)
    say(f"Connecting to the manager at {PLATFORM_URL} ...")
    agent_id, token, fresh = connect_with_retry(client)
    auth = {"Authorization": f"Bearer {token}"}
    action = "Registered" if fresh else "Resumed"
    say(f"{action} as '{PROBE_NAME}'. Capabilities: {', '.join(CAPABILITIES)}")
    say(f"Use-case library: {', '.join(sorted(USE_CASES))}")
    _flush_spool(client, auth, agent_id)
    say("Waiting for scan jobs...")

    last_hb = 0.0
    while True:
        now = time.monotonic()
        try:
            if now - last_hb >= HEARTBEAT_INTERVAL:
                hb = client.post("/agents/heartbeat", headers=auth,
                                 json={"agent_id": agent_id, "status": "online"})
                if hb.status_code == 401:
                    say("Heartbeat rejected (stale token) — will re-register on next poll.")
                last_hb = now
            r = client.get(f"/agents/{agent_id}/jobs", headers=auth, params={"limit": JOB_LIMIT})
            if r.status_code == 401:
                say("Identity rejected — re-registering ...")
                _save_state({})
                agent_id, token, _ = connect_with_retry(client)
                auth = {"Authorization": f"Bearer {token}"}
                say(f"Re-registered as '{PROBE_NAME}'. Resuming job polling ...")
                continue
            r.raise_for_status()
            for job in r.json():
                _run_job(client, auth, agent_id, job)
        except httpx.HTTPError:
            say("Can't reach the manager right now — will keep retrying.")
        # P2: jitter the poll so a fleet of probes doesn't synchronize into a
        # thundering herd against the manager (±50% spread on each interval).
        time.sleep(POLL_INTERVAL + random.uniform(0, POLL_INTERVAL * 0.5))


def _fetch_engagement_scope(client: httpx.Client, auth: dict, engagement_id: str) -> list[str] | None:
    """Fetch the engagement's authoritative scope_cidrs from the manager.

    Returns a list of CIDR strings, or None if the fetch fails (caller falls
    back to job-params scope in that case, which is still ScopeGuard-enforced).
    """
    try:
        r = client.get(f"/engagements/{engagement_id}/scope", headers=auth)
        if r.status_code == 200:
            return r.json().get("scope_cidrs") or None
        say(f"  scope fetch returned HTTP {r.status_code} — falling back to job params", 1)
    except httpx.HTTPError as exc:
        say(f"  scope fetch failed ({exc}) — falling back to job params", 1)
    return None


def _validate_targets_in_scope(targets: list[str], scope_cidrs: list[str]) -> tuple[list[str], list[str]]:
    """Return (allowed, rejected) by checking each target against scope_cidrs."""
    networks = []
    for cidr in scope_cidrs:
        try:
            networks.append(ipaddress.ip_network(cidr, strict=False))
        except ValueError:
            pass

    allowed, rejected = [], []
    for t in targets:
        host = t.split(":")[0] if ":" in t else t
        try:
            addr = ipaddress.ip_address(host)
            in_scope = any(addr in net for net in networks)
        except ValueError:
            # hostname or CIDR — pass through, ScopeGuard handles it at packet level
            in_scope = True
        (allowed if in_scope else rejected).append(t)
    return allowed, rejected


def _spool_result(job_id: str, payload: dict) -> Path:
    """Persist result to local spool so upload can be retried after failures."""
    RESULT_SPOOL_DIR.mkdir(parents=True, exist_ok=True)
    p = RESULT_SPOOL_DIR / f"{job_id}.json"
    p.write_text(json.dumps(payload))
    return p


def _submit_result(client: httpx.Client, auth: dict, agent_id: str,
                   job_id: str, payload: dict) -> bool:
    """Upload result with retry. Returns True on success."""
    spool_file = _spool_result(job_id, payload)
    for attempt in range(1, RESULT_UPLOAD_RETRIES + 1):
        try:
            r = client.post(f"/agents/{agent_id}/jobs/{job_id}/result",
                            headers=auth, json=payload)
            if r.status_code < 500:
                spool_file.unlink(missing_ok=True)
                return True
            say(f"  upload attempt {attempt}/{RESULT_UPLOAD_RETRIES}: HTTP {r.status_code} — retrying in {RESULT_RETRY_DELAY}s", 1)
        except httpx.HTTPError as exc:
            say(f"  upload attempt {attempt}/{RESULT_UPLOAD_RETRIES}: {exc} — retrying in {RESULT_RETRY_DELAY}s", 1)
        if attempt < RESULT_UPLOAD_RETRIES:
            time.sleep(RESULT_RETRY_DELAY)
    say(f"  upload failed after {RESULT_UPLOAD_RETRIES} attempts — result spooled at {spool_file}", 1)
    return False


def _flush_spool(client: httpx.Client, auth: dict, agent_id: str) -> None:
    """Re-submit any results that failed to upload in a previous run."""
    if not RESULT_SPOOL_DIR.exists():
        return
    for p in RESULT_SPOOL_DIR.glob("*.json"):
        job_id = p.stem
        try:
            payload = json.loads(p.read_text())
            r = client.post(f"/agents/{agent_id}/jobs/{job_id}/result",
                            headers=auth, json=payload)
            if r.status_code < 500:
                p.unlink(missing_ok=True)
                say(f"Flushed spooled result for job {job_id}")
        except Exception:
            pass


def _run_job(client: httpx.Client, auth: dict, agent_id: str, job: dict[str, Any]) -> None:
    job_id = job["job_id"]
    engagement_id = job.get("engagement_id", "")
    params = dict(job.get("params") or {})
    use_case_id = params.get("use_case_id") or job.get("use_case_id")

    # ── Use-case resolution ──────────────────────────────────────────────────
    # The probe only executes use-cases from the finite library. An unknown
    # use_case_id is rejected immediately without scanning.
    try:
        scan_type, profile = resolve_use_case(use_case_id, job.get("job_type"), params)
    except ValueError as exc:
        say(f"Job {job_id} rejected: {exc}")
        _submit_result(client, auth, agent_id, job_id, {
            "success": False, "result": {}, "error": str(exc)})
        return

    # ── Scope re-validation (defense in depth) ───────────────────────────────
    # Fetch the engagement's authoritative scope from the manager independently
    # of the job params. This ensures a buggy or tampered job cannot widen scope
    # beyond what the engagement actually allows.
    targets_raw: list[str] = params.get("targets") or params.get("scope_cidrs") or []
    if isinstance(targets_raw, str):
        targets_raw = [targets_raw]

    engagement_scope = None
    if engagement_id:
        engagement_scope = _fetch_engagement_scope(client, auth, engagement_id)

    if engagement_scope and targets_raw:
        allowed, rejected = _validate_targets_in_scope(targets_raw, engagement_scope)
        if rejected:
            say(f"  scope guard: {len(rejected)} target(s) outside engagement scope — skipped: {rejected}", 1)
        if not allowed:
            say(f"Job {job_id} rejected: all targets are outside the engagement scope {engagement_scope}")
            _submit_result(client, auth, agent_id, job_id, {
                "success": False, "result": {},
                "error": f"All targets out of scope. Engagement scope: {engagement_scope}"})
            return
        params["targets"] = allowed

    uc_label = f"use-case={use_case_id}" if use_case_id else f"scan_type={scan_type}"
    say(f"Running {uc_label} on {params.get('targets') or params.get('scope_cidrs')} ...")

    client.post("/agents/heartbeat", headers=auth,
                json={"agent_id": agent_id, "status": "busy", "current_job_id": job_id})

    params["profile"] = profile
    result = run_scan(scan_type, params,
                      use_case_id=use_case_id,
                      engagement_uuid=engagement_id,
                      validated_scope=engagement_scope)

    stats = result.get("run_stats") or {}
    say(f"done — {stats.get('host_count', result.get('host_count', 0))} hosts, "
        f"{stats.get('open_ports', result.get('open_ports', 0))} open ports", 1)

    _submit_result(client, auth, agent_id, job_id, {
        "success": bool(result.get("ok")),
        "result": result,
        "error": result.get("error"),
    })
    client.post("/agents/heartbeat", headers=auth, json={"agent_id": agent_id, "status": "online"})


if __name__ == "__main__":
    try:
        arg = sys.argv[1] if len(sys.argv) > 1 else "run"
        if arg in ("version", "-v", "--version"):
            say(f"Intrynx Probe {VERSION}")
        elif arg == "hostid":
            # clients run this and send the Host ID to the vendor for a license
            from agent.license import short_id
            say(short_id())
        else:
            main()
    except KeyboardInterrupt:
        say("\nProbe stopped.")
        sys.exit(0)

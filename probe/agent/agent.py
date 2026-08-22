#!/usr/bin/env python3
"""
agent.py — thin main loop for the Vedha Probe.

Startup gauntlet (HW bind → license → register → flush spool → main loop).
Delegates all actual work to focused submodules:

    transport.py       — HTTP + WebSocket (Phase 2) manager communication
    task_runner.py     — job lifecycle orchestration
    scope_validator.py — defense-in-depth scope re-validation
    result_spool.py    — local spooling with upload retry
    scope_crypt.py     — X25519 + AES-GCM scope decryption (Phase 4)
    hw_bind.py         — hardware fingerprinting for binary host-locking
    engine.py          — scan execution
    use_cases.py       — finite use-case library

Security properties (outbound-only, no inbound ports):
  - Hardware-bound binary: binary only runs on specific machine
  - License gate: host-locked Ed25519-signed license
  - Scope re-validated independently of job params before any packet
  - Use-case library: finite, pre-defined scan scenarios only
  - Local spool: results never lost, retried on upload failure
"""
from __future__ import annotations

import asyncio
import concurrent.futures
import ipaddress
import json
import logging
import os
import random
import secrets
import socket
import sys
import threading
import time
from pathlib import Path
from urllib.parse import urlparse

from agent.transport import DeviceAlreadyEnrolledError, Transport, TransportError

VERSION = "2.0.0"
LOG = logging.getLogger("agent")


def _bounded_env_int(name: str, default: int, minimum: int, maximum: int) -> int:
    """Return an integer environment setting constrained to a safe range."""
    try:
        value = int(os.environ.get(name, str(default)))
    except (TypeError, ValueError):
        return default
    return max(minimum, min(maximum, value))


def _is_local_manager_url(value: str) -> bool:
    """Recognize only explicit single-host development/Compose manager names."""
    platform_host = (urlparse(value).hostname or "").lower()
    return platform_host in {
        "localhost", "127.0.0.1", "::1", "api", "host.docker.internal",
    }


def _load_env(path: Path) -> None:
    """Load key=value lines from probe.env for dev convenience."""
    try:
        for line in path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
    except OSError:
        pass


def say(msg: str = "", indent: int = 0) -> None:
    print(("  " * indent) + msg, flush=True)


# ── DEBUG (temporary) — set PROBE_DEBUG=1 to trace the connection handshake ────
# Prints the URL, HTTP status, and short response body of every Manager call plus
# the enrollment/refresh state transitions, so a stuck "can't connect" is
# diagnosable without a packet capture. Safe to leave in (no-op unless enabled).
_DEBUG = os.environ.get("PROBE_DEBUG", "").lower() in ("1", "true", "yes", "on")


def _dbg(msg: str) -> None:
    if _DEBUG:
        print(f"[debug] {msg}", flush=True)


def _job_intent(job: dict) -> str:
    """Human label for what a job will actually run — the use-case (real intent),
    not the coarse `job_type` enum (which the manager hardcodes to 'discovery').
    A numeric `uc` code is shown too. This is what makes probe output transparent:
    the operator sees exactly which use-case/scanner was dispatched."""
    uc = job.get("use_case_id") or (job.get("params") or {}).get("use_case_id")
    code = (job.get("params") or {}).get("uc")
    if uc:
        return f"{uc}" + (f" (uc={code})" if code is not None else "")
    if code is not None:
        return f"uc={code}"
    return f"job_type={job.get('job_type', '?')}"


def _result_summary(result) -> str:
    """One-line, transparent summary of what a scan actually found so the operator
    can tell at a glance whether the result matches expectations (0 hosts usually
    means a scope/target problem, not a scanner bug)."""
    data = getattr(result, "result", None) or {}
    stats = data.get("run_stats") or {}
    facts = data.get("facts")
    parts = [result.scan_type]
    if stats.get("host_count") is not None:
        parts.append(f"{stats.get('host_count', 0)} hosts")
    if stats.get("open_ports") is not None:
        parts.append(f"{stats.get('open_ports', 0)} open ports")
    if isinstance(facts, list):
        parts.append(f"{len(facts)} facts")
    outcome = data.get("outcome")
    if outcome and outcome not in ("ok", "completed"):
        parts.append(f"outcome={outcome}")
    return " — ".join([parts[0], ", ".join(parts[1:])]) if len(parts) > 1 else parts[0]


# ── Connection preflight + auto-troubleshoot ─────────────────────────────────
# The probe should never spin forever on a bad connection: it diagnoses WHY the
# Manager is unreachable, gives a specific fix, retries a bounded number of times,
# and then either proceeds (reachable) or exits with a clear, actionable error.
def _classify_connection_error(exc: Exception, url: str) -> tuple[str, str]:
    """Map a low-level connection exception to (reason, how-to-fix)."""
    host = url.split("://", 1)[-1].split("/", 1)[0] if "://" in url else url
    s = str(exc).lower()
    tname = type(exc).__name__.lower()
    if "timed out" in s or "timeout" in tname:
        return ("connection timed out",
                f"A firewall/security-group is likely DROPPING traffic to {host}. "
                f"Open the Manager's port to this host, or check PLATFORM_URL.")
    if "refused" in s:
        return ("connection refused",
                f"Nothing is listening at {host}. Is the Manager UP? "
                f"Verify on the Manager host: curl {url}/health")
    if "getaddrinfo" in s or "name or service not known" in s or "nodename nor servname" in s:
        return ("cannot resolve host",
                f"DNS can't resolve '{host}'. Check PLATFORM_URL and this host's resolver.")
    if "ssl" in s or "certificate" in s or "tls" in s:
        return ("TLS handshake failed",
                "The Manager cert isn't trusted. For a private CA set "
                "PROBE_CA_BUNDLE=/path/ca.pem; for testing use an http:// URL.")
    if "connection" in s or "connecterror" in tname:
        return ("cannot connect",
                f"Could not reach {host}. Check PLATFORM_URL, network, and firewall.")
    return ("connection error", f"{type(exc).__name__}: {str(exc)[:140]}")


def _manager_reachable(transport) -> tuple[bool, str]:
    """GET /health. Returns (ok, human-detail) — distinguishes down vs 5xx vs net."""
    try:
        r = transport._client.get("/health", timeout=8.0)
        if r.status_code == 200:
            return True, "healthy"
        if 500 <= r.status_code < 600:
            return False, (f"Manager returned HTTP {r.status_code} at /health — "
                           f"server-side error; check the Manager (api) logs.")
        return False, f"Manager returned HTTP {r.status_code} at /health (unexpected)."
    except Exception as exc:  # noqa: BLE001 — classify every transport failure
        reason, fix = _classify_connection_error(exc, getattr(transport, "_base_url", "?"))
        return False, f"{reason} — {fix}"


def _wait_for_manager(transport, *, attempts: int = 6, base_delay: float = 5.0) -> None:
    """Bounded reachability preflight. Proceeds the moment the Manager answers
    /health; after `attempts` failures prints a boxed diagnosis and EXITS(2) —
    never an infinite silent retry."""
    url = getattr(transport, "_base_url", "?")
    last = ""
    for i in range(1, attempts + 1):
        ok, detail = _manager_reachable(transport)
        if ok:
            say(f"✓ Manager reachable at {url}")
            return
        last = detail
        say(f"✗ Manager not reachable [{i}/{attempts}]: {detail}")
        _dbg(f"preflight /health failed: {detail}")
        if i < attempts:
            time.sleep(min(30.0, base_delay * i))
    say("")
    say("═" * 60)
    say("  CANNOT CONNECT TO THE MANAGER — stopping")
    say("═" * 60)
    say(f"  URL   : {url}")
    say(f"  Why   : {last}")
    say("  Then re-run install.sh. (set PROBE_DEBUG=1 for verbose tracing)")
    say("═" * 60)
    raise SystemExit(2)


def _poll_jobs_or_empty(transport: Transport, limit: int) -> list[dict]:
    """Poll for work. Auth failures (TransportError) and transient network
    failures both propagate to the caller's unified retry/backoff handler so
    outages are diagnosed and rate-limited rather than silently swallowed."""
    return transport.poll_jobs(limit=limit)


def main() -> None:
    # ── Load environment ──────────────────────────────────────────────────────
    _load_env(Path(__file__).resolve().parent.parent / "probe.env")

    PLATFORM_URL = os.environ.get("PLATFORM_URL", "").rstrip("/")
    PROBE_NAME = os.environ.get("PROBE_NAME") or socket.gethostname()
    PROBE_LOCATION = os.environ.get("PROBE_LOCATION", "")
    NETWORK_SEGMENTS = [s.strip() for s in
                        os.environ.get("PROBE_NETWORK_SEGMENTS", "").split(",") if s.strip()]
    try:
        NETWORK_SEGMENTS = [
            str(ipaddress.ip_network(segment, strict=False))
            for segment in NETWORK_SEGMENTS
        ]
    except ValueError as exc:
        say(f"Setup needed: PROBE_NETWORK_SEGMENTS contains an invalid CIDR: {exc}")
        raise SystemExit(1) from exc
    OPERATOR_EMAIL = os.environ.get("OPERATOR_EMAIL", "")
    OPERATOR_PASSWORD = os.environ.get("OPERATOR_PASSWORD", "")
    OPERATOR_TOKEN = (
        os.environ.get("OPERATOR_TOKEN", "")
        or os.environ.get("PROBE_PAT", "")
        or os.environ.get("VEDHA_PAT", "")
    )
    AGENT_ID_ENV = os.environ.get("AGENT_ID", "")
    AGENT_TOKEN_ENV = os.environ.get("AGENT_TOKEN", "")
    HEARTBEAT_INTERVAL = _bounded_env_int("HEARTBEAT_INTERVAL", 30, 5, 300)
    POLL_INTERVAL = _bounded_env_int("POLL_INTERVAL", 10, 1, 300)
    # This agent executes jobs sequentially. Claiming multiple jobs up front
    # would let later leases expire while the first assessment is still running.
    JOB_LIMIT = 1
    VERIFY_TLS = os.environ.get("VERIFY_TLS", "true").lower() not in ("false", "0", "no")
    STATE_FILE = Path(os.environ.get("STATE_FILE", "/var/lib/vedha-probe/state.json"))
    SPOOL_DIR = Path(os.environ.get("RESULT_SPOOL_DIR", "/var/lib/vedha-probe/spool"))
    SPOOL_MAX_BYTES = _bounded_env_int(
        "RESULT_SPOOL_MAX_BYTES", 512 << 20, 1 << 20, 16 << 30,
    )
    SPOOL_MAX_FILES = _bounded_env_int(
        "RESULT_SPOOL_MAX_FILES", 1024, 1, 100_000,
    )
    # Secure transport (optional): a private-PKI CA bundle to trust, and an mTLS
    # client cert/key so the manager can authenticate the probe at the TLS layer.
    CA_BUNDLE = os.environ.get("PROBE_CA_BUNDLE") or None
    CLIENT_CERT = os.environ.get("PROBE_CLIENT_CERT") or None
    CLIENT_KEY = os.environ.get("PROBE_CLIENT_KEY") or None
    # gzip result payloads at/above this many bytes (default 1 MiB; 0 disables).
    COMPRESS_OVER = _bounded_env_int(
        "RESULT_COMPRESS_OVER", 1 << 20, 0, 64 << 20,
    )

    # ── Banner ────────────────────────────────────────────────────────────────
    say("Vedha Probe (scanner_module)")
    say("--------------------------------")

    if not PLATFORM_URL:
        say("Setup needed: PLATFORM_URL is not set.")
        raise SystemExit(1)
    # ── Transport security posture (warn loudly, never silently downgrade) ────
    _is_local = _is_local_manager_url(PLATFORM_URL)
    if PLATFORM_URL.startswith("http://") and not _is_local:
        say("Note: manager is http:// (unencrypted) — OK for testing, use https:// in production.")
    if PLATFORM_URL.startswith("https://") and not VERIFY_TLS:
        say("WARNING: VERIFY_TLS is off — the manager certificate is NOT verified "
            "(MITM-exposed). Trusted links only; set PROBE_CA_BUNDLE for private PKI.")
    if CLIENT_CERT:
        say(f"mTLS enabled — presenting client certificate {CLIENT_CERT}.")

    # ── Step 1: Startup gauntlet ─────────────────────────────────────────────
    # One function: HW bind → license → anti-debug.  Fails fast with clear,
    # actionable messages so the operator knows exactly why the probe refused
    # to start.  The license dict is returned for logging/banner display.
    try:
        lic = _startup_gauntlet()
    except SystemExit:
        raise
    if lic:
        say(f"License OK — {lic.get('customer','?')}, valid until {lic.get('expires','?')}")

    # ── Step 2: Setup transport ──────────────────────────────────────────────
    transport = Transport(
        PLATFORM_URL,
        verify_tls=VERIFY_TLS,
        agent_id=AGENT_ID_ENV,
        agent_token=AGENT_TOKEN_ENV,
        state_file=STATE_FILE,
        ca_bundle=CA_BUNDLE,
        client_cert=CLIENT_CERT,
        client_key=CLIENT_KEY,
        compress_over=COMPRESS_OVER,
    )

    # Device-enrolled probes receive their local execution ceiling from the
    # Manager-owned Site policy. An explicit environment value remains a
    # further local restriction for legacy/air-gapped deployments.
    if not NETWORK_SEGMENTS:
        try:
            stored_policy = transport.load_state().get("site_policy") or {}
            NETWORK_SEGMENTS = list(stored_policy.get("authorized_cidrs") or [])
        except (OSError, ValueError, TypeError):
            NETWORK_SEGMENTS = []

    from agent.result_spool import ResultSpool
    spool = ResultSpool(
        spool_dir=SPOOL_DIR,
        max_bytes=SPOOL_MAX_BYTES,
        max_files=SPOOL_MAX_FILES,
    )

    # ── Preflight: is the Manager actually reachable? ────────────────────────
    # Bounded, self-diagnosing check BEFORE the identity dance so a down/blocked
    # Manager surfaces one clear error instead of an opaque retry loop later.
    _wait_for_manager(transport)

    # ── Step 3: Register / resume identity ──────────────────────────────────
    agent_id, token, fresh, identity_sk, identity_pk, _public_key_b64 = _obtain_identity(
        transport, OPERATOR_EMAIL, OPERATOR_PASSWORD, OPERATOR_TOKEN,
        PROBE_NAME, PROBE_LOCATION, NETWORK_SEGMENTS,
    )
    if not NETWORK_SEGMENTS:
        try:
            stored_policy = transport.load_state().get("site_policy") or {}
            NETWORK_SEGMENTS = list(stored_policy.get("authorized_cidrs") or [])
        except (OSError, ValueError, TypeError):
            NETWORK_SEGMENTS = []
    if not NETWORK_SEGMENTS:
        say("Setup needed: the approved Site policy contains no authorized CIDRs.")
        raise SystemExit(1)
    try:
        site_policy = transport.load_state().get("site_policy") or {}
    except (OSError, ValueError, TypeError):
        site_policy = {}
    SITE_EXCLUDED_SEGMENTS = list(site_policy.get("excluded_cidrs") or [])
    # Manager Site budgets can only tighten the appliance defaults.
    from agent import engine as scan_engine
    scan_engine.MAX_TARGETS = min(
        scan_engine.MAX_TARGETS,
        int(site_policy.get("max_targets") or scan_engine.MAX_TARGETS),
    )
    scan_engine.MAX_JOB_SECONDS = min(
        scan_engine.MAX_JOB_SECONDS,
        float(site_policy.get("max_job_seconds") or scan_engine.MAX_JOB_SECONDS),
    )
    action = "Registered" if fresh else "Resumed"
    say(f"{action} as '{PROBE_NAME}'.")

    from agent.engine import CAPABILITIES
    from agent.use_cases import USE_CASES
    say(f"Capabilities: {', '.join(CAPABILITIES)}")
    say(f"Use-case library: {', '.join(sorted(USE_CASES))}")

    # ── Step 4: Create TaskRunner (with identity for scope decryption) ────────
    from agent.task_runner import TaskRunner
    runner = TaskRunner(
        http_get=transport.http_get,
        submit_result=lambda jid, p: transport.submit_result(jid, p),
        spool_submit=spool.submit_with_retry,
        identity_sk=identity_sk,   # Phase 4: X25519 private key for scope decryption
        local_allowed_networks=NETWORK_SEGMENTS,
        local_excluded_networks=SITE_EXCLUDED_SEGMENTS,
    )

    # ── Step 5: Try WebSocket push mode first ────────────────────────────────
    # Phase 2: persistent WebSocket connection with manager push.
    # If the manager supports WS, the probe stays in push mode indefinitely.
    # If WS fails (manager down, network issue, unsupported), fall through
    # to HTTP polling below.
    ws_mode_available = os.environ.get("PROBE_WS_ENABLED", "true").lower() not in (
        "false", "0", "no",
    )

    if ws_mode_available:
        say("Attempting WebSocket push mode...")
        try:
            ws_result = asyncio.run(_run_ws_push_loop(
                transport, runner, agent_id, spool, HEARTBEAT_INTERVAL, POLL_INTERVAL,
            ))
            if ws_result:
                # WS loop exited cleanly (shutdown or unrecoverable error)
                say("WebSocket loop exited. Probe stopping.")
                return
            # ws_result is False → WS unavailable, fall through to HTTP poll
        except KeyboardInterrupt:
            say("\nProbe stopped (WebSocket mode).")
            raise SystemExit(0)
        except Exception as exc:
            say(f"WebSocket mode crashed ({exc}) — falling back to HTTP poll.")
    else:
        # Flush spool over HTTP before entering poll loop
        flushed = spool.flush_spool(
            lambda jid, p: transport.submit_result(jid, p),
        )
        if flushed:
            say(f"Flushed {flushed} spooled result(s) from previous run(s).")

    # ── Step 6: Main loop (HTTP polling — fallback) ──────────────────────────
    say("Waiting for scan jobs (HTTP polling)...")
    last_hb = 0.0
    last_spool_warning = 0.0
    # Runtime resilience: an already-onboarded probe rides out Manager restarts
    # (results are spooled), but never silently hot-loops — failures back off and
    # escalate to a diagnosed warning so the operator can act.
    poll_fail_streak = 0
    POLL_FAIL_BACKOFF_MAX = 60.0

    while True:
        now = time.monotonic()
        jobs: list[dict] = []
        try:
            if now - last_hb >= HEARTBEAT_INTERVAL:
                if not transport.heartbeat("online", None if not hasattr(runner, '_current_job') else None):
                    say("Heartbeat rejected (stale token).")
                last_hb = now

            if spool.at_capacity:
                if now - last_spool_warning >= 60:
                    say(
                        "Result spool high-water mark reached "
                        f"({spool.spool_count} files, {spool.spool_bytes} bytes); "
                        "pausing new jobs until uploads recover."
                    )
                    last_spool_warning = now
            else:
                jobs = _poll_jobs_or_empty(transport, JOB_LIMIT)

            poll_fail_streak = 0  # a clean pass clears the outage counter

        except TransportError:
            say("Token rejected — re-registering...")
            transport.clear_state()
            agent_id, token, fresh, identity_sk, identity_pk, _ = _obtain_identity(
                transport, OPERATOR_EMAIL, OPERATOR_PASSWORD, OPERATOR_TOKEN,
                PROBE_NAME, PROBE_LOCATION, NETWORK_SEGMENTS,
            )
            # Update runner's identity (may have changed if state was wiped)
            runner._identity_sk = identity_sk
            poll_fail_streak = 0
            say(f"Re-registered as '{PROBE_NAME}'. Resuming...")
            continue
        except Exception as exc:
            # Transient Manager outage: back off (never hot-loop), and after a
            # sustained streak print a diagnosed reason so it's not silent.
            poll_fail_streak += 1
            reason, fix = _classify_connection_error(exc, transport._base_url)
            if poll_fail_streak in (1, 5) or poll_fail_streak % 20 == 0:
                say(f"Manager unreachable ({reason}) — retrying "
                    f"[streak {poll_fail_streak}]. {fix}")
                _dbg(f"poll-loop failure: {exc!r}")
            backoff = min(POLL_FAIL_BACKOFF_MAX, POLL_INTERVAL * poll_fail_streak)
            time.sleep(backoff + random.uniform(0, POLL_INTERVAL * 0.5))
            continue

        for job in jobs:
            # Mark busy before running
            transport.heartbeat(
                "busy",
                job.get("job_id"),
                job.get("attempt_id"),
                job.get("fence"),
            )
            try:
                result = _run_polled_job_with_heartbeats(
                    transport,
                    runner,
                    job,
                    agent_id,
                    heartbeat_interval=HEARTBEAT_INTERVAL,
                )
                if result.error:
                    say(f"Job {result.job_id}: {result.error}", 1)
                else:
                    say(f"Job {result.job_id} done — {_result_summary(result)}", 1)
            except Exception as exc:
                LOG.exception("Job %s crashed runner", job.get("job_id"))
                transport.submit_result(job.get("job_id", "?"), {
                    "job_id": job.get("job_id", "?"),
                    "attempt_id": job.get("attempt_id"),
                    "fence": job.get("fence"),
                    "success": False, "result": {},
                    "error": f"Runner crashed: {exc}",
                })

        # Re-flush results spooled during an earlier manager outage. flush_spool
        # makes a single upload attempt per file, so a transient partition
        # recovers within the poll loop instead of waiting for a probe restart.
        if spool.spool_count:
            reflushed = spool.flush_spool(
                lambda jid, p: transport.submit_result(jid, p),
            )
            if reflushed:
                say(f"Re-flushed {reflushed} spooled result(s).", 1)

        # P2: jitter to avoid thundering herd across a probe fleet
        time.sleep(POLL_INTERVAL + random.uniform(0, POLL_INTERVAL * 0.5))


def _run_polled_job_with_heartbeats(
    transport: "Transport",
    runner,
    job: dict,
    agent_id: str,
    *,
    heartbeat_interval: float,
):
    """Run an HTTP-claimed job while renewing its manager lease."""
    job_id = job.get("job_id")
    attempt_id = job.get("attempt_id")
    fence = job.get("fence")
    cancellation_event = threading.Event()
    consecutive_failures = 0
    failure_limit = _bounded_env_int("LEASE_LOSS_GRACE_HEARTBEATS", 3, 1, 10)
    interval = max(0.05, float(heartbeat_interval))
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=1,
        thread_name_prefix="probe-job",
    ) as executor:
        future = executor.submit(
            runner.run_job,
            job,
            agent_id,
            cancellation_event=cancellation_event,
        )
        while True:
            try:
                return future.result(timeout=interval)
            except concurrent.futures.TimeoutError:
                if not transport.heartbeat("busy", job_id, attempt_id, fence):
                    consecutive_failures += 1
                    say(
                        f"Lease heartbeat failed for running job {job_id}; "
                        f"failure {consecutive_failures}/{failure_limit}.",
                        1,
                    )
                    if consecutive_failures >= failure_limit:
                        cancellation_event.set()
                else:
                    consecutive_failures = 0


# ── P2: WebSocket push loop ────────────────────────────────────────────────

WS_RECONNECT_BACKOFF_MIN = 1.0
WS_RECONNECT_BACKOFF_MAX = 60.0


async def _run_ws_push_loop(
    transport: "Transport",
    runner,
    agent_id: str,
    spool,
    heartbeat_interval: int,
    poll_interval: int,
) -> bool:
    """Persistent WebSocket push loop.

    Returns False if WebSocket is unavailable (caller should fall back to
    HTTP polling). Returns True only on clean shutdown or unrecoverable error
    (caller should exit).
    """
    import websockets

    backoff = WS_RECONNECT_BACKOFF_MIN

    while True:
        try:
            say("Connecting via WebSocket (push mode)...")
            ws = await transport.connect_ws()

            # ── Auth: send hello ─────────────────────────────────────────
            await ws.send(json.dumps({
                "type": "hello",
                "agent_id": agent_id,
                "token": transport.agent_token,
                "protocol_version": 2,
                "features": ["atomic_job_claim_v1"],
            }))

            # Wait for hello_ok (with timeout)
            try:
                hello_raw = await asyncio.wait_for(ws.recv(), timeout=10.0)
            except asyncio.TimeoutError:
                say("WebSocket hello timed out — falling back to HTTP poll.")
                await ws.close()
                return False

            hello_msg = json.loads(hello_raw)
            if hello_msg.get("type") == "error":
                say(f"WebSocket auth rejected: {hello_msg.get('message', '?')}")
                await ws.close()
                return False

            if hello_msg.get("type") != "hello_ok":
                say("WebSocket handshake unexpected — falling back to HTTP poll.")
                await ws.close()
                return False

            features = set(hello_msg.get("features") or [])
            if "atomic_job_claim_v1" not in features:
                say(
                    "Manager does not support confirmed WebSocket claims "
                    "— falling back to atomic HTTP polling."
                )
                await ws.close()
                return False

            say("WebSocket connected. Push mode active — waiting for jobs.")
            backoff = WS_RECONNECT_BACKOFF_MIN  # reset on successful connect

            # Results use one durable path in every mode: local spool followed
            # by authenticated HTTP submission. WS is control-plane only.
            await _flush_spool_over_http(transport, spool)

            # ── Start heartbeat + HTTP poll fallback tasks ────────────────
            # WebSocket pushes are process-local on the manager. With multiple
            # API workers a launch request can land on a different worker than
            # the probe's WS connection, so keep polling as a safety net.
            job_state = {"current_job_id": None, "pending_job": None}
            job_lock = asyncio.Lock()
            hb_task = asyncio.create_task(
                _ws_heartbeat_sender(ws, agent_id, heartbeat_interval, job_state),
            )
            poll_task = asyncio.create_task(
                _ws_http_poll_fallback(
                    ws, transport, runner, agent_id, spool,
                    poll_interval, job_lock, job_state,
                ),
            )

            # ── Main receive loop ────────────────────────────────────────
            async for raw in ws:
                try:
                    msg = json.loads(raw)
                except json.JSONDecodeError:
                    continue

                msg_type = msg.get("type", "")

                if msg_type == "job_push":
                    await _ws_stage_job_offer(
                        ws, msg.get("job", {}), job_state,
                    )

                elif msg_type == "job_claim":
                    pending_job = _ws_take_confirmed_job(msg, job_state)
                    if pending_job is None:
                        continue

                    async with job_lock:
                        await _ws_run_job(ws, runner, agent_id, pending_job, job_state,
                                          pushed=True, transport=transport,
                                          heartbeat_interval=heartbeat_interval)
                        await _flush_spool_over_http(transport, spool)

                elif msg_type == "error":
                    say(f"Manager: {msg.get('message', 'unknown error')}")

                elif msg_type == "result_ack":
                    # Manager acknowledged our result
                    pass

                elif msg_type == "displaced":
                    say(f"WebSocket displaced: {msg.get('message', '?')}")
                    break

            # Loop exited (ws closed by manager)
            for task in (hb_task, poll_task):
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass

        except websockets.exceptions.ConnectionClosed as exc:
            say(f"WebSocket closed (code={exc.code}) — reconnecting in {backoff:.0f}s...")
        except (OSError, asyncio.TimeoutError) as exc:
            say(f"WebSocket unavailable ({exc}) — reconnecting in {backoff:.0f}s...")
        except TransportError as exc:
            say(f"WebSocket auth error: {exc} — falling back to HTTP poll.")
            return False
        except Exception as exc:
            say(f"WebSocket error: {type(exc).__name__}: {exc} — reconnecting in {backoff:.0f}s...", 1)

        # Exponential backoff
        await asyncio.sleep(backoff)
        backoff = min(backoff * 2, WS_RECONNECT_BACKOFF_MAX)


async def _ws_stage_job_offer(ws, job: dict, job_state: dict) -> bool:
    """Acknowledge an offer without executing it before claim confirmation."""
    job_id = job.get("job_id")
    can_accept = bool(
        job_id
        and job_state.get("current_job_id") is None
        and job_state.get("pending_job") is None
    )
    if can_accept:
        job_state["pending_job"] = job
    await ws.send(json.dumps({
        "type": "job_ack",
        "job_id": job_id or "",
        "accepted": can_accept,
    }))
    return can_accept


def _ws_take_confirmed_job(message: dict, job_state: dict) -> dict | None:
    """Release a staged job only after the manager confirms its claim."""
    job_id = message.get("job_id", "")
    pending_job = job_state.get("pending_job")
    if not pending_job or pending_job.get("job_id") != job_id:
        return None

    job_state["pending_job"] = None
    if not message.get("claimed", False):
        say(
            f"Push offer {job_id} was not claimed "
            f"({message.get('reason', 'unknown')}).",
            1,
        )
        return None
    return {
        **pending_job,
        "attempt_id": message.get("attempt_id"),
        "attempt_number": message.get("attempt_number"),
        "fence": message.get("fence"),
        "lease_expires_at": message.get("lease_expires_at"),
    }


async def _ws_run_job(
    ws,
    runner,
    agent_id: str,
    job: dict,
    job_state: dict,
    *,
    pushed: bool,
    transport: "Transport" | None = None,
    heartbeat_interval: float = 30,
):
    """Run one job while keeping WS status/result frames best-effort."""
    job_id = job.get("job_id", "?")
    if pushed:
        say(f"▶ Push: job {job_id} — {_job_intent(job)}")
    else:
        say(f"▶ Poll fallback: job {job_id} — {_job_intent(job)}")

    job_state["current_job_id"] = job_id
    job_state["attempt_id"] = job.get("attempt_id")
    job_state["fence"] = job.get("fence")
    # Best-effort WS status frame (as this function's docstring promises). A flapping
    # push channel must NEVER abort the job — it still runs and submits its result
    # over HTTP via _run_polled_job_with_heartbeats below.
    try:
        await ws.send(json.dumps({
            "type": "heartbeat",
            "status": "busy",
            "current_job_id": job_id,
            "attempt_id": job.get("attempt_id"),
            "fence": job.get("fence"),
        }))
    except Exception as exc:  # noqa: BLE001 — status is optional; the job continues over HTTP
        _dbg(f"ws busy-heartbeat send dropped (job continues via HTTP): {exc!r}")

    try:
        # Run job in a thread — engine.run_scan() internally calls
        # asyncio.run(), which can't run inside an existing event loop.
        if transport is not None:
            result = await asyncio.to_thread(
                _run_polled_job_with_heartbeats,
                transport,
                runner,
                job,
                agent_id,
                heartbeat_interval=heartbeat_interval,
            )
        else:
            result = await asyncio.to_thread(runner.run_job, job, agent_id)

        if result.error:
            say(f"  ✗ {result.error}", 1)
        else:
            say(f"  ✓ {_result_summary(result)}", 1)
        return result
    finally:
        job_state["current_job_id"] = None
        job_state["attempt_id"] = None
        job_state["fence"] = None
        try:
            await ws.send(json.dumps({
                "type": "heartbeat",
                "status": "online",
                "current_job_id": None,
                "attempt_id": None,
                "fence": None,
            }))
        except Exception as exc:  # noqa: BLE001 — best-effort WS status frame
            _dbg(f"ws idle-heartbeat send dropped: {exc!r}")


async def _ws_http_poll_fallback(
    ws,
    transport: "Transport",
    runner,
    agent_id: str,
    spool,
    interval: int,
    job_lock: asyncio.Lock,
    job_state: dict,
) -> None:
    """Poll pending jobs even while WS is connected.

    This makes result delivery reliable when manager WS pushes are missed, for
    example under multi-worker API deployments with process-local WS state.
    """
    while True:
        await asyncio.sleep(max(1, interval))
        if (
            job_state.get("current_job_id")
            or job_state.get("pending_job") is not None
        ):
            continue
        try:
            jobs = await asyncio.to_thread(transport.poll_jobs, 1)
        except TransportError as exc:
            say(f"HTTP poll fallback auth error: {exc} — reconnecting.")
            await ws.close()
            return
        except Exception as exc:
            say(f"HTTP poll fallback failed ({exc})", 1)
            continue
        if not jobs:
            continue
        async with job_lock:
            for job in jobs:
                await _ws_run_job(ws, runner, agent_id, job, job_state,
                                  pushed=False, transport=transport,
                                  heartbeat_interval=max(5, interval))
                await _flush_spool_over_http(transport, spool)


async def _ws_heartbeat_sender(
    ws,
    agent_id: str,
    interval: int,
    job_state: dict | None = None,
) -> None:
    """Send periodic heartbeats over WebSocket."""
    try:
        while True:
            await asyncio.sleep(interval)
            current_job_id = (job_state or {}).get("current_job_id")
            await ws.send(json.dumps({
                "type": "heartbeat",
                "status": "busy" if current_job_id else "online",
                "current_job_id": current_job_id,
                "attempt_id": (job_state or {}).get("attempt_id"),
                "fence": (job_state or {}).get("fence"),
            }))
    except Exception:
        pass  # ws closed, task will be cancelled


async def _flush_spool_over_http(transport: "Transport", spool) -> None:
    """Retry durable result files using the acknowledged HTTP result path."""
    if spool.spool_count == 0:
        return

    count = await asyncio.to_thread(
        spool.flush_spool,
        transport.submit_result,
    )
    if count:
        say(f"  Flushed {count} spooled result(s) over HTTP.", 1)


def _startup_gauntlet() -> dict | None:
    """Run all startup security checks before any network I/O.

    Order matters: HW bind first (hardest to bypass), then license,
    then anti-debug (informational — doesn't block).

    Returns the license dict (for logging), or None if enforcement is off.
    Raises SystemExit on any hard failure.
    """
    # ── Gate 1: Hardware binding ──────────────────────────────────────────
    from agent.hw_bind import check_hw_bind, HWBindError
    try:
        check_hw_bind()
    except HWBindError as exc:
        say("╔══════════════════════════════════════════════════════════════╗")
        say("║  HARDWARE BINDING CHECK FAILED                              ║")
        say("╠══════════════════════════════════════════════════════════════╣")
        for line in str(exc).splitlines():
            say(f"║  {line:<60}║")
        say("╚══════════════════════════════════════════════════════════════╝")
        raise SystemExit(2)

    # ── Gate 2: License verification ──────────────────────────────────────
    from agent.license import check_license, LicenseError, short_id
    try:
        lic = check_license()
    except LicenseError as exc:
        say("╔══════════════════════════════════════════════════════════════╗")
        say("║  LICENSE CHECK FAILED                                       ║")
        say("╠══════════════════════════════════════════════════════════════╣")
        for line in str(exc.friendly).splitlines():
            say(f"║  {line:<60}║")
        say(f"║  This machine's Host ID: {short_id():<39}║")
        say("╠══════════════════════════════════════════════════════════════╣")
        say("║  To get a license:                                          ║")
        say("║    1. Run: ./vedha-probe hostid                           ║")
        say("║    2. Send the Host ID to your administrator                ║")
        say("║    3. Set PROBE_LICENSE=<token> in the environment          ║")
        say("╚══════════════════════════════════════════════════════════════╝")
        raise SystemExit(2)

    # ── Gate 3: Anti-debug (informational) ────────────────────────────────
    _check_anti_debug()

    return lic


def _check_anti_debug() -> None:
    """Detect common debugging/tracing tools.  Informational only — does
    NOT block startup because legitimate operators may run the binary
    under a profiler or in a monitored environment.

    In a Nuitka-compiled binary these are harder to detect; in dev mode
    (plain Python) they're just a warning.
    """
    import sys
    indicators: list[str] = []

    # ptrace / DTrace attached? (Linux/macOS)
    if sys.platform == "linux":
        try:
            with open("/proc/self/status") as f:
                for line in f:
                    if line.startswith("TracerPid:"):
                        pid = int(line.split(":")[1].strip())
                        if pid > 0:
                            indicators.append(f"ptrace attached (tracer PID {pid})")
        except (OSError, ValueError):
            pass

    if sys.platform == "darwin":
        import subprocess
        try:
            out = subprocess.check_output(
                ["launchctl", "getenv", "DYLD_INSERT_LIBRARIES"],
                stderr=subprocess.DEVNULL, text=True,
            ).strip()
            if out:
                indicators.append(f"DYLD_INSERT_LIBRARIES={out}")
        except Exception:
            pass

    # Python-level debugging
    if sys.gettrace() is not None:
        indicators.append("Python debugger attached (sys.gettrace)")

    if os.environ.get("NUITKA_DEBUG"):
        indicators.append("NUITKA_DEBUG is set")

    if indicators:
        say("─ Anti-debug notice (informational, NOT blocking) ─")
        for i in indicators:
            say(f"  • {i}", 1)


def _load_or_create_identity(transport) -> tuple[bytes, bytes, str]:
    """Load the probe's X25519 identity from persistent state, or create one.

    Returns (private_key_bytes, public_key_bytes, public_key_b64).
    The identity is stored alongside the transport state in the state file.
    Generating a new identity invalidates any previously encrypted scope
    payloads from the manager (the manager stores the old public key until
    the next re-registration).
    """
    identity_sk = None
    identity_pk = None

    # Try to load from the state file
    if transport._state_file and transport._state_file.exists():
        try:
            state = transport.load_state()
            if state.get("identity_sk"):
                from agent.scope_crypt import pubkey_to_bytes, bytes_to_pubkey_b64
                identity_sk = pubkey_to_bytes(state["identity_sk"])
                if identity_sk and len(identity_sk) == 32:
                    # Reconstruct public key from private key
                    from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey
                    sk = X25519PrivateKey.from_private_bytes(identity_sk)
                    identity_pk = sk.public_key().public_bytes_raw()
                    public_key_b64 = bytes_to_pubkey_b64(identity_pk)
                    return identity_sk, identity_pk, public_key_b64
        except Exception:
            identity_sk = None

    # Generate a fresh identity
    from agent.scope_crypt import generate_identity, bytes_to_pubkey_b64
    identity_sk, identity_pk = generate_identity()
    public_key_b64 = bytes_to_pubkey_b64(identity_pk)

    # Persist alongside transport state
    if transport._state_file:
        try:
            import base64
            transport.update_state({
                "identity_sk": base64.b64encode(identity_sk).decode(),
                "identity_pk": public_key_b64,
            })
            say(f"Generated new X25519 identity (pk: {public_key_b64[:12]}…)", 1)
        except OSError as exc:
            say(f"warning: could not persist identity ({exc})", 1)

    return identity_sk, identity_pk, public_key_b64


def _load_or_create_signing_identity(transport) -> tuple[bytes, str]:
    """Load or atomically create the probe's Ed25519 enrollment identity."""
    from agent.device_identity import (
        decode_key,
        encode_key,
        generate_signing_identity,
        signing_public_from_private,
    )

    try:
        state = transport.load_state()
        if state.get("signing_identity_sk"):
            private = decode_key(state["signing_identity_sk"])
            public = signing_public_from_private(private)
            return private, encode_key(public)
    except (OSError, ValueError, TypeError):
        pass

    private, public = generate_signing_identity()
    transport.update_state({
        "signing_identity_sk": encode_key(private),
        "signing_identity_pk": encode_key(public),
    })
    return private, encode_key(public)


def _enroll_device(
    transport: Transport,
    *,
    signing_private_key: bytes,
    signing_public_key: str,
    encryption_public_key: str,
    probe_name: str,
) -> dict:
    """Request UI approval, poll, prove key possession, and activate."""
    from agent.device_identity import sign_b64
    from agent.engine import CAPABILITIES

    state = transport.load_state()
    request_id = state.get("enrollment_request_id")
    device_secret = state.get("enrollment_device_secret")
    poll_interval = 5
    if not request_id or not device_secret:
        enroll_payload = {
            "signing_public_key": signing_public_key,
            "encryption_public_key": encryption_public_key,
            "nonce": secrets.token_urlsafe(24),
            "hostname_hint": probe_name,
            "platform": sys.platform,
            "architecture": os.uname().machine if hasattr(os, "uname") else "unknown",
            "agent_version": VERSION,
            "installer_version": os.environ.get("PROBE_INSTALLER_VERSION", VERSION),
            "build_digest": os.environ.get("PROBE_BUILD_DIGEST", "development-build"),
            "capabilities": CAPABILITIES,
        }
        enroll_token = os.environ.get("PROBE_ENROLL_TOKEN")
        if enroll_token:
            # Pre-authorized, Site-bound token: the manager auto-approves and
            # returns state="approved" with an activation challenge — no operator
            # user_code step. A bad/expired/used token degrades to the manual
            # path (manager returns "awaiting_approval" with a user_code).
            enroll_payload["enroll_token"] = enroll_token
        try:
            response = transport.create_enrollment_request(enroll_payload)
        except DeviceAlreadyEnrolledError as exc:
            # This device's signing key is already an agent on the manager, so a
            # fresh enrollment can never be created. The only autonomous recovery
            # is to re-mint a short-lived access token from the stored device
            # refresh secret. If that secret is gone (never activated, or state
            # was wiped), no amount of retrying helps — the operator must remove
            # the stale probe in Fleet, or the local identity must be cleared.
            if transport.refresh_device_access(signing_private_key):
                say("Device already enrolled — reconnected by refreshing its access token.")
                return {
                    "agent_id": transport.agent_id,
                    "access_token": transport.agent_token,
                }
            # The device key is registered on the Manager but this install has no
            # reusable credential (never activated, cleared by the refresh self-heal,
            # revoked, or the Manager DB was re-created). Rather than dead-ending in a
            # restart loop on repeated 409s, WIPE the stale local identity so the next
            # boot generates a FRESH key and enrolls clean — the container's restart
            # policy makes this automatic and the probe self-heals to online. The old,
            # orphaned agent can be pruned in Fleet.
            say("")
            say("═" * 58)
            say("  Already enrolled, no reusable credential — self-healing")
            say("═" * 58)
            say(f"  Why : {exc}")
            say("  Clearing this install's stale identity and re-enrolling as a")
            say("  fresh device on restart. (Remove the old probe in Fleet later.)")
            say("═" * 58)
            transport.update_state(remove=(
                "signing_identity_sk", "signing_identity_pk",
                "agent_id", "token", "device_refresh_secret", "credential_generation",
                "enrollment_request_id", "enrollment_device_secret",
            ))
            raise SystemExit(4) from exc
        request_id = response["request_id"]
        device_secret = response["device_secret"]
        poll_interval = int(response.get("poll_interval_seconds") or 5)
        transport.update_state({
            "enrollment_request_id": request_id,
            "enrollment_device_secret": device_secret,
        })
        _dbg(f"enrollment request created → state={response.get('state')} "
             f"request_id={request_id} auto={response.get('state') == 'approved'}")
        if response.get("state") == "approved":
            say("Probe pre-authorized via enrollment token — auto-approving, no code needed.")
        else:
            verification_path = response.get("verification_path", "/fleet/enroll")
            url = f"{transport._base_url}{verification_path}"
            code = response["user_code"]
            # Prominent, un-missable pairing block — this is the whole zero-touch
            # onboarding: the operator matches this code in the dashboard, approves,
            # and the probe below activates automatically.
            say("")
            say("═" * 58)
            say("  PROBE PAIRING REQUIRED — approve to start scanning")
            say("═" * 58)
            say(f"   1) Open this URL : {url}")
            say(f"   2) Enter code    : {code}")
            say("═" * 58)
            say("Waiting for dashboard approval… (the probe starts automatically once approved)")

    # Bounds so enrollment never hangs silently:
    #  • net_fail_streak — consecutive transport/network errors → give up with a
    #    diagnosed reason (the Manager is down/blocked, not slow to approve).
    #  • approval_deadline — an unapproved probe surfaces a clear message instead
    #    of waiting forever (auto-enroll approves instantly, so this only bites a
    #    manual pairing that nobody actioned).
    net_fail_streak = 0
    NET_FAIL_LIMIT = _bounded_env_int("PROBE_ENROLL_NET_FAIL_LIMIT", 12, 3, 100)
    approval_wait_secs = _bounded_env_int("PROBE_ENROLL_WAIT_SECS", 1800, 60, 86400)
    approval_deadline = time.monotonic() + approval_wait_secs
    last_wait_note = time.monotonic()
    while True:
        try:
            response = transport.poll_enrollment(str(request_id), str(device_secret))
            net_fail_streak = 0
            state_name = response.get("state")
            _dbg(f"enrollment poll → state={state_name}")
            if state_name in {"awaiting_approval", "requested"}:
                if time.monotonic() >= approval_deadline:
                    say("")
                    say("═" * 58)
                    say("  ENROLLMENT NOT APPROVED — stopping")
                    say("═" * 58)
                    say(f"  No approval within {approval_wait_secs // 60} min. "
                        "Approve the probe in the dashboard (Fleet → Enroll),")
                    say("  or set PROBE_AUTO_ENROLL=true on the Manager, then re-run.")
                    say("═" * 58)
                    raise SystemExit(3)
                now = time.monotonic()
                if now - last_wait_note >= 60:
                    remaining = int(approval_deadline - now)
                    say(f"Still waiting for dashboard approval… ({remaining // 60} min left)")
                    last_wait_note = now
                time.sleep(max(5, int(response.get("poll_interval_seconds") or poll_interval)))
                continue
            if state_name == "approved":
                challenge = response.get("activation_challenge")
                if not challenge:
                    raise RuntimeError("approved enrollment omitted activation challenge")
                message = f"vedha-enrollment:{request_id}:{challenge}"
                return transport.activate_enrollment(
                    str(request_id),
                    str(device_secret),
                    sign_b64(signing_private_key, message),
                )
            if state_name == "active":
                challenge = response.get("activation_challenge")
                message = f"vedha-enrollment:{request_id}:{challenge}"
                return transport.activate_enrollment(
                    str(request_id), str(device_secret), sign_b64(signing_private_key, message)
                )
            if state_name in {"denied", "expired"}:
                transport.update_state(remove=("enrollment_request_id", "enrollment_device_secret"))
                raise TransportError(f"Enrollment {state_name}: {response.get('reason', '')}".strip())
            raise RuntimeError(f"unexpected enrollment state: {state_name}")
        except TransportError:
            raise
        except SystemExit:
            raise
        except Exception as exc:
            net_fail_streak += 1
            reason, fix = _classify_connection_error(exc, transport._base_url)
            if net_fail_streak >= NET_FAIL_LIMIT:
                say("")
                say("═" * 58)
                say("  ENROLLMENT FAILED — Manager unreachable")
                say("═" * 58)
                say(f"  Why : {reason}")
                say(f"  Fix : {fix}")
                say("═" * 58)
                raise SystemExit(2) from exc
            say(f"Enrollment manager unavailable ({reason}) — retrying "
                f"[{net_fail_streak}/{NET_FAIL_LIMIT}].")
            _dbg(f"enrollment poll failure: {exc!r}")
            time.sleep(min(30, 5 * net_fail_streak))


def _obtain_identity(
    transport: Transport,
    email: str, password: str, operator_token: str,
    probe_name: str, location: str, segments: list[str],
) -> tuple[str, str, bool, bytes, bytes, str]:
    """Return (agent_id, token, fresh, identity_sk, identity_pk, public_key_b64).

    A cached identity refreshes its routing metadata before use, then falls back
    to login + registration if its agent token is rejected. Network failures
    retry with backoff up to a bounded limit, then exit with a diagnosed error
    (see PROBE_REGISTER_NET_FAIL_LIMIT / PROBE_ENROLL_NET_FAIL_LIMIT) so a probe
    never spins silently against a down or blocked Manager.
    """
    from agent.engine import CAPABILITIES

    # Phase 4: generate/load X25519 identity BEFORE registration
    # (needed even when already authenticated so the caller has the keys)
    identity_sk, identity_pk, public_key_b64 = _load_or_create_identity(transport)
    signing_sk, signing_public_key = _load_or_create_signing_identity(transport)
    # Keep the device key in process memory for proactive short-lived token
    # renewal. The raw private key is never sent to the Manager.
    transport._device_signing_private_key = signing_sk

    # Refresh cached routing metadata with the agent's own token. This keeps
    # newly added scan capabilities routable without retaining bootstrap admin
    # credentials on the probe.
    if transport.is_authenticated():
        _refresh_tries = 0
        while True:
            try:
                state = transport.load_state()
            except (OSError, ValueError, TypeError):
                state = {}
            policy = state.get("site_policy") if isinstance(state, dict) else None
            policy = policy if isinstance(policy, dict) else {}
            approved_capabilities = policy.get("approved_capabilities")
            if not isinstance(approved_capabilities, list):
                approved_capabilities = CAPABILITIES
            effective_capabilities = [
                capability for capability in CAPABILITIES
                if capability in approved_capabilities
            ]
            try:
                refreshed = transport.refresh_registration(
                    capabilities=effective_capabilities,
                    network_segments=segments,
                    public_key=public_key_b64,
                )
                _dbg(f"refresh_registration → {refreshed!r} (agent_id={transport.agent_id})")
            except TransportError as exc:
                _dbg(f"refresh_registration raised: {exc}")
                if transport.refresh_device_access(signing_sk):
                    say("Refreshed short-lived device access token.", 1)
                    continue
                if state.get("device_refresh_secret"):
                    say("Device credential was revoked, expired, or disabled; stopping for administrator review.")
                    raise SystemExit(1)
                say("Cached agent token was rejected — identity requires re-enrollment.")
                transport.clear_state()
                break

            if refreshed is True:
                return transport.agent_id, transport.agent_token, False, \
                       identity_sk, identity_pk, public_key_b64
            if refreshed is None:
                # Rolling-upgrade compatibility: older managers do not enforce
                # capability-aware scheduling and do not expose this endpoint.
                say("Manager does not support agent metadata refresh; using cached identity.", 1)
                return transport.agent_id, transport.agent_token, False, \
                       identity_sk, identity_pk, public_key_b64

            # Self-heal: a cached identity the Manager can no longer refresh
            # (agent deleted, DB re-created, policy changed) would otherwise loop
            # forever. After a few tries, drop it and fall through to
            # (re-)registration / device enrollment instead of spinning.
            _refresh_tries += 1
            if _refresh_tries >= 3:
                say("Cached identity can't be refreshed — clearing and re-enrolling.")
                transport.clear_state()
                break
            say(f"Can't refresh cached capabilities yet — retrying ({_refresh_tries}/3).")
            time.sleep(10)

    BOOTSTRAP_KEY = os.environ.get("PROBE_BOOTSTRAP_KEY", "")

    reg_fail_streak = 0
    REG_FAIL_LIMIT = _bounded_env_int("PROBE_REGISTER_NET_FAIL_LIMIT", 12, 3, 100)
    while True:
        try:
            if not operator_token:
                if not BOOTSTRAP_KEY and not (email and password):
                    data = _enroll_device(
                        transport,
                        signing_private_key=signing_sk,
                        signing_public_key=signing_public_key,
                        encryption_public_key=public_key_b64,
                        probe_name=probe_name,
                    )
                    return data["agent_id"], data["access_token"], True, \
                           identity_sk, identity_pk, public_key_b64
                # Try bootstrap key first (no admin login required)
                if BOOTSTRAP_KEY:
                    say("No PAT configured — using PROBE_BOOTSTRAP_KEY to self-register.", 1)
                    data = transport.bootstrap(
                        probe_name,
                        bootstrap_key=BOOTSTRAP_KEY,
                        location=location or None,
                        capabilities=CAPABILITIES,
                        network_segments=segments,
                        public_key=public_key_b64,
                    )
                    return data["agent_id"], data["token"], True, \
                           identity_sk, identity_pk, public_key_b64

                if not email or not password:
                    say("Setup needed: set PROBE_BOOTSTRAP_KEY, PROBE_PAT, or OPERATOR_EMAIL + OPERATOR_PASSWORD.")
                    raise SystemExit(1)

                # Login as operator for development compatibility. Production
                # deployments should pass a scoped PAT instead of a password.
                r = transport._client.post(
                    "/auth/login",
                    json={"email": email, "password": password},
                )
                r.raise_for_status()
                operator_token = r.json()["access_token"]

            # Register as agent (send X25519 public key for scope encryption)
            data = transport.register(
                probe_name,
                location=location or None,
                capabilities=CAPABILITIES,
                network_segments=segments,
                public_key=public_key_b64,
                operator_token=operator_token,
            )
            return data["agent_id"], data["token"], True, \
                   identity_sk, identity_pk, public_key_b64

        except TransportError:
            # A stale/invalid PAT — or a Manager that was re-created — must not
            # dead-end the probe. When the only credential was a token (no
            # operator login, no bootstrap key), fall back to DEVICE ENROLLMENT:
            # the probe's own keypair is its id, and the Manager issues a token
            # (auto-approved when PROBE_AUTO_ENROLL is on, else a pairing code).
            # This is what makes a bare `install.sh <manager-ip>` self-heal.
            if operator_token and not (email and password) and not BOOTSTRAP_KEY:
                say("Saved credential rejected — falling back to device enrollment…")
                data = _enroll_device(
                    transport,
                    signing_private_key=signing_sk,
                    signing_public_key=signing_public_key,
                    encryption_public_key=public_key_b64,
                    probe_name=probe_name,
                )
                return data["agent_id"], data["access_token"], True, \
                       identity_sk, identity_pk, public_key_b64
            say("Manager rejected sign-in — check credentials.")
            raise SystemExit(1)
        except SystemExit:
            raise
        except Exception as exc:
            reg_fail_streak += 1
            reason, fix = _classify_connection_error(exc, transport._base_url)
            if reg_fail_streak >= REG_FAIL_LIMIT:
                say("")
                say("═" * 58)
                say("  REGISTRATION FAILED — Manager unreachable")
                say("═" * 58)
                say(f"  Why : {reason}")
                say(f"  Fix : {fix}")
                say("═" * 58)
                raise SystemExit(2) from exc
            say(f"Can't reach manager yet ({reason}) — retrying "
                f"[{reg_fail_streak}/{REG_FAIL_LIMIT}].")
            _dbg(f"registration failure: {exc!r}")
            time.sleep(min(30, 5 * reg_fail_streak))


if __name__ == "__main__":
    try:
        arg = sys.argv[1] if len(sys.argv) > 1 else "run"
        if arg in ("version", "-v", "--version"):
            say(f"Vedha Probe {VERSION}")
        elif arg == "hostid":
            from agent.license import host_fingerprint
            say(host_fingerprint())
        elif arg == "self-test":
            say("Running self-test...")
            try:
                lic = _startup_gauntlet()
                say(f"  License: {'OK' if lic else 'SKIPPED (dev mode)'}")
            except SystemExit:
                say("  Self-test FAILED — see above for details.")
                sys.exit(1)
            say("Self-test passed.")
        elif arg == "manifest":
            # Deterministic capability surface — printed as raw JSON (no logging
            # prefix) so CI can diff the SEALED binary against the plaintext build.
            # If Nuitka drops a module or a registration, importing these fails or
            # the output diverges, and the seal-parity job goes red. No network,
            # no license, no host state — pure introspection.
            import json
            from agent.engine import CAPABILITIES
            from agent.use_cases import USE_CASES, USE_CASE_CODES, INTENSITY_CODES
            print(json.dumps({
                "version": VERSION,
                "capabilities": sorted(CAPABILITIES),
                "use_cases": sorted(USE_CASES),
                "use_case_codes": {str(k): v for k, v in sorted(USE_CASE_CODES.items())},
                "intensity_codes": {str(k): v for k, v in sorted(INTENSITY_CODES.items())},
            }, indent=2, sort_keys=True))
        elif arg == "local-run":
            # On-box diagnostic: run the REAL scan engine locally, no manager.
            # Lazily imported so the daemon path and the `manifest` contract (which
            # the seal-parity job diffs byte-for-byte) are completely unaffected.
            from agent.local_run import run as _local_run
            raise SystemExit(_local_run(sys.argv[2:]))
        else:
            main()
    except KeyboardInterrupt:
        say("\nProbe stopped.")
        sys.exit(0)

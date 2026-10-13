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
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

from agent.instance_lock import (
    InstanceLockError,
    acquire_instance_lock,
)
from agent.transport import (
    DEVICE_REFRESH_OK,
    AccessExpiredError,
    DEVICE_REFRESH_EXPIRED,
    DEVICE_REFRESH_REJECTED,
    DEVICE_REFRESH_UNAVAILABLE,
    HEARTBEAT_LEASE_REVOKED,
    HEARTBEAT_OK,
    DeviceAlreadyEnrolledError,
    EnrollmentRequestNotFound,
    Transport,
    TransportError,
    TransportUnavailableError,
    manager_fingerprint,
)

from agent.version import AGENT_VERSION as VERSION  # the agent's own number (agent/version.py)

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
        # utf-8-sig: a file written by Windows PowerShell may start with a byte-order
        # mark, which would otherwise glue itself to the first key's name.
        for line in path.read_text(encoding="utf-8-sig").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
    except OSError:
        pass


def _force_utf8_streams() -> None:
    """Make stdout/stderr encode-proof so non-ASCII output can never crash the agent.

    On Windows the default console encoding is cp1252, which can't encode common
    UI glyphs the agent prints (warnings ``⚠``, checks ``✓``, arrows ``→``). Any
    such print used to raise UnicodeEncodeError and kill the process mid-startup —
    a cosmetic line taking down the whole agent. Reconfiguring the streams to UTF-8
    with ``errors="replace"`` fixes the entire class at once: unencodable glyphs
    degrade to a placeholder instead of raising. Best-effort and idempotent; if a
    stream can't be reconfigured (redirected/wrapped), say() still guards below.
    """
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            try:
                reconfigure(encoding="utf-8", errors="replace")
            except (ValueError, OSError):
                pass


_force_utf8_streams()


# When PROBE_LOG_FILE is set (the Windows installer does), everything the agent says is
# also written to a size-capped, rotating file: a Scheduled Task has no console, so
# without this a client would have no log to read or send us.
_SAY_LOG = logging.getLogger("agent.say")
_SAY_LOG.propagate = False          # it has its own file handler; never echo to stderr twice


def say(msg: str = "", indent: int = 0) -> None:
    line = ("  " * indent) + msg
    if _SAY_LOG.handlers:
        _SAY_LOG.info(line)
    try:
        print(line, flush=True)
    except UnicodeEncodeError:
        # Belt-and-braces: a stream we couldn't reconfigure (older Python, an
        # exotic wrapper) must still never crash the agent over an output glyph.
        enc = getattr(sys.stdout, "encoding", None) or "ascii"
        try:
            print(line.encode(enc, "replace").decode(enc, "replace"), flush=True)
        except (OSError, ValueError):
            pass
    except (OSError, ValueError):
        # No usable console (a Windows Scheduled Task, a closed pipe). The line is
        # already in the log file when one is configured; narrating must never stop the agent.
        pass


# ── Runtime status (read by the installer, `status` and the support bundle) ─────
# A headless agent (Windows Scheduled Task, container) has no console, so its state
# is recorded in status.json beside the state file. Best effort: never raises.
_STATUS_PATH: Path | None = None


def _status(state: str, **fields) -> None:
    if _STATUS_PATH is None:
        return
    from agent import runtime_status
    runtime_status.write(_STATUS_PATH, state, version=VERSION,
                         manager=os.environ.get("PLATFORM_URL", ""), **fields)


def _record_crash(exc: BaseException) -> None:
    """An unexpected error must never be silent. A headless agent (a Windows Scheduled
    Task) has no console to show a traceback, so write it to the log and record why the
    agent stopped, where `status`, `doctor` and the installer will report it."""
    logging.getLogger("agent").critical("The agent stopped because of an unexpected error:", exc_info=exc)
    _status("failed", reason=f"unexpected error: {type(exc).__name__}: {exc}",
            remediation="Run `vedha-agent support-bundle` and send the file to Vedha support; "
                        "the details are in the agent log.")


def _status_connection_lost(what: str) -> None:
    """`status` must not keep saying ONLINE after a live connection is lost: record it, so
    the installer, `status`, `doctor` and the support bundle show the truth."""
    _status("retrying", reason=what[:200],
            remediation="Run `vedha-agent doctor`. If it does not recover, run "
                        "`vedha-agent support-bundle` and send the file to Vedha support.",
            detail="reconnecting to the manager")


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
    # An HTTP status error means the manager ANSWERED and rejected the request —
    # a server/API fault, never a network one. Classify it by its code so we
    # never again call an HTTP 4xx/5xx a "connection error" (which sent the probe
    # into a 12x retry against a manager that was replying all along).
    _resp = getattr(exc, "response", None)
    _code = getattr(_resp, "status_code", None)
    if _code is not None:
        return (f"manager returned HTTP {_code}",
                f"The manager at {host} answered but rejected the request "
                f"(HTTP {_code}). This is a manager-side/API fault, not the "
                f"network — check the manager logs, not the firewall.")
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


def _detect_primary_ipv4() -> str | None:
    """Best-effort primary IPv4 of this host — the address a scan sources from.
    Uses a UDP socket to a public IP to read the routing decision; no packet is
    actually sent, and it works on any interface (not just en0)."""
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("1.1.1.1", 80))
            return s.getsockname()[0]
        finally:
            s.close()
    except OSError:
        return None


def _preflight_connect_fast_fail() -> None:
    """Windows only: say whether scan sockets report a closed port at network
    speed. Without it every closed port costs ~2 s and connect scans read closed
    ports as filtered (scanner/win_fast_connect.py). One loopback connect; never
    blocks startup."""
    try:
        from scanner import win_fast_connect
        result = win_fast_connect.self_check(include_default=False)
    except Exception:  # noqa: BLE001 — a preflight must never stop the agent
        return
    if result is None:
        return
    fast = result.get("fast_fail_s")
    if result.get("effective"):
        say(f"✓ Port scans: closed ports report in {fast * 1000:.0f} ms "
            f"(Windows SYN retry off, mode {result['mode']}).", 1)
    else:
        say("⚠ Port scans: Windows still retries refused connections (~2 s per closed "
            "port); full-port sweeps from this agent will be slow. "
            "Run `doctor` for details.", 1)


def _preflight_scope_check(network_segments: list[str]) -> None:
    """Auto-troubleshoot the single silent killer of job execution: a scan
    ceiling that doesn't match the network this probe is actually on.

    The manager only dispatches a job whose targets are inside the probe's
    declared PROBE_NETWORK_SEGMENTS, and the probe re-enforces the same ceiling
    locally. If that ceiling excludes the probe's own network, the probe connects
    happily and then rejects (or is never offered) every job — the "connected but
    nothing scans" failure. Warn loudly at startup instead of failing in silence.
    Warnings only: the manager stays the authority, and an operator may
    deliberately declare a remote range they route to.
    """
    if not network_segments:
        # The normal case for an enrolled agent: its ceiling is the authorized
        # scope in the Manager's signed Site policy (the engagement scope for an
        # install token), loaded after enrolment. Startup stops with a clear
        # message if that policy turns out to authorize nothing.
        say("Scan range: from the Manager's Site policy after enrolment "
            "(set PROBE_NETWORK_SEGMENTS only to narrow it further).", 1)
        return
    ip = _detect_primary_ipv4()
    if not ip:
        return
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        return
    for seg in network_segments:
        try:
            if addr in ipaddress.ip_network(seg, strict=False):
                say(f"✓ Scan ceiling {network_segments} covers this host ({ip}).", 1)
                return
        except ValueError:
            continue
    suggested = f"{ip.rsplit('.', 1)[0]}.0/24"
    say(f"⚠ This probe is on {ip}, but PROBE_NETWORK_SEGMENTS={network_segments} "
        f"does not include it.", 1)
    say(f"  Jobs targeting this network will be rejected as out-of-ceiling. If you "
        f"mean to scan the local network, set PROBE_NETWORK_SEGMENTS={suggested} "
        f"(or the exact range you intend to scan) and restart.", 1)


def _keep_retrying() -> bool:
    """PROBE_KEEP_RETRYING=true: wait for an unreachable Manager instead of exiting.
    The Windows installer sets it - there the agent is a Scheduled Task and a reboot or a
    network blip must not leave it stopped. Container hosts leave it off: their restart
    policy supervises the process, so exiting with a diagnosis is the right behaviour."""
    return os.environ.get("PROBE_KEEP_RETRYING", "").strip().lower() in ("1", "true", "yes", "on")


KEEP_RETRYING_MAX_WAIT = 300.0      # seconds between rounds once the agent has settled into waiting


def _retry_wait(streak: int, *, cap: float = 30.0) -> float:
    return min(KEEP_RETRYING_MAX_WAIT if _keep_retrying() else cap, 5.0 * streak)


def _reason_and_fix(detail: str) -> tuple[str, str]:
    """_manager_reachable reports 'reason — fix'; status.json keeps them apart."""
    reason, sep, fix = detail.partition(" — ")
    return reason, (fix if sep else "Run `vedha-agent doctor` to see what is blocking the connection.")


def _wait_for_manager(transport, *, attempts: int = 6, base_delay: float = 5.0) -> None:
    """Reachability preflight. Proceeds the moment the Manager answers /health.
    Normally, after `attempts` failures it prints a boxed diagnosis and EXITS(2) - never an
    infinite silent retry. With PROBE_KEEP_RETRYING it records the diagnosis in the status file
    and tries again, with a growing pause, until the Manager answers."""
    url = getattr(transport, "_base_url", "?")
    keep = _keep_retrying()
    rounds = 0
    while True:
        last = ""
        for i in range(1, attempts + 1):
            ok, detail = _manager_reachable(transport)
            if ok:
                say(f"✓ Manager reachable at {url}")
                return
            last = detail
            reason, fix = _reason_and_fix(detail)
            _status("retrying", reason=reason, remediation=fix, detail=f"manager check {i}/{attempts}")
            say(f"✗ Manager not reachable [{i}/{attempts}]: {detail}")
            _dbg(f"preflight /health failed: {detail}")
            if i < attempts:
                time.sleep(min(30.0, base_delay * i))
        if not keep:
            reason, fix = _reason_and_fix(last)
            _status("failed", reason=reason, remediation=fix)
            say("")
            say("═" * 60)
            say("  CANNOT CONNECT TO THE MANAGER — stopping")
            say("═" * 60)
            say(f"  URL   : {url}")
            say(f"  Why   : {last}")
            say("  Then re-run install.sh. (set PROBE_DEBUG=1 for verbose tracing)")
            say("═" * 60)
            raise SystemExit(2)
        rounds += 1
        wait = min(KEEP_RETRYING_MAX_WAIT, 30.0 * 2 ** (rounds - 1))
        say(f"Cannot reach the manager at {url} yet. The agent keeps trying; next check in {int(wait)} s. "
            f"Run `vedha-agent doctor` to see what is blocking it.")
        time.sleep(wait)


_LOG_LEVELS = ("CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG")


def configure_logging() -> str:
    """Install a root log handler for the daemon.

    Nothing on the daemon path called basicConfig(), so the root logger had no
    handler and Python fell back to its last-resort handler — which emits
    WARNING and above ONLY. Every LOG.info() the probe writes (job claimed,
    use-case resolved, scope guard decisions, "done — N hosts, M open ports",
    "result archived -> ...") was produced and then discarded before reaching
    `docker compose logs`, which is why probe-side troubleshooting was blind.

    Level comes from LOG_LEVEL (default INFO); PROBE_DEBUG=1 forces DEBUG so the
    existing connection-tracing switch also turns up the rest of the probe.
    Idempotent: safe to call more than once, and it never overrides a handler an
    embedding process already installed.
    """
    requested = (os.environ.get("LOG_LEVEL") or "").strip().upper()
    # Re-read PROBE_DEBUG rather than trusting the import-time constant: probe.env
    # is loaded inside main(), i.e. AFTER this module was imported, so a value set
    # there would otherwise never be seen.
    debug = _DEBUG or os.environ.get("PROBE_DEBUG", "").lower() in ("1", "true", "yes", "on")
    if debug:
        level_name = "DEBUG"
    elif requested in _LOG_LEVELS:
        level_name = requested
    else:
        if requested:
            print(f"[warn] ignoring unknown LOG_LEVEL={requested!r}; "
                  f"valid: {', '.join(_LOG_LEVELS)}", file=sys.stderr, flush=True)
        level_name = "INFO"

    root = logging.getLogger()
    if not root.handlers:
        logging.basicConfig(
            level=getattr(logging, level_name),
            format="%(asctime)s %(levelname)-7s %(name)s: %(message)s",
            stream=sys.stderr,
        )
    else:
        root.setLevel(getattr(logging, level_name))
    _attach_log_file(level_name)
    # Third-party chatter would bury the probe's own narration.
    #
    # httpx logs one INFO line per request, and the probe polls the manager every
    # POLL_INTERVAL seconds (default 10) FOREVER, plus a heartbeat every 30s. At
    # the old floor of INFO that produced an endless scroll of
    #   HTTP Request: GET /agents/<id>/jobs "HTTP/1.1 200 OK"
    # which tells an operator nothing, hides the lines that do matter (job
    # claimed, scan finished, errors), and makes an idle probe look busy.
    # Routine transport chatter is DEBUG-only now; warnings and errors — the ones
    # that actually indicate a problem reaching the manager — still surface.
    transport_level = logging.DEBUG if level_name == "DEBUG" else logging.WARNING
    for noisy in ("httpx", "httpcore", "websockets", "asyncio", "urllib3"):
        logging.getLogger(noisy).setLevel(transport_level)
    aio = logging.getLogger("asyncio")
    if not any(isinstance(f, _QuietPeerResets) for f in aio.filters):
        aio.addFilter(_QuietPeerResets())
    return level_name


class _QuietPeerResets(logging.Filter):
    """A scanned host closing a connection is not an agent error.

    On Windows the Proactor loop logs a full ERROR traceback when a peer resets a
    socket while asyncio is closing it ("Exception in callback
    _ProactorBasePipeTransport._call_connection_lost ... WinError 10054"). Banner
    grabs and deep branches hit this on every host that hangs up on them, which
    reads as a crashing agent. Such a record becomes one DEBUG line (shown only
    at DEBUG); every other asyncio error is untouched.
    """

    _RESETS = (ConnectionResetError, ConnectionAbortedError)

    def filter(self, record: logging.LogRecord) -> bool:
        exc = record.exc_info[1] if record.exc_info else None
        if not (isinstance(exc, self._RESETS)
                and "_call_connection_lost" in record.getMessage()):
            return True
        if not logging.getLogger().isEnabledFor(logging.DEBUG):
            return False
        record.levelno, record.levelname = logging.DEBUG, "DEBUG"
        record.msg, record.args = f"peer reset a closing connection ({exc})", None
        record.exc_info = record.exc_text = None
        return True


LOG_FILE_MAX_BYTES = 10 * 1024 * 1024
LOG_FILE_BACKUPS = 5


def _attach_log_file(level_name: str) -> None:
    """Mirror the agent's logging and its narration into PROBE_LOG_FILE, rotating at
    10 MB and keeping 5 old files (about 60 MB at most). Best effort: a log file that
    cannot be opened must never stop the agent."""
    path = os.environ.get("PROBE_LOG_FILE", "").strip()
    if not path:
        return
    root = logging.getLogger()
    if any(getattr(h, "_vedha_file", False) for h in root.handlers):
        return
    try:
        from logging.handlers import RotatingFileHandler
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        handler = RotatingFileHandler(path, maxBytes=LOG_FILE_MAX_BYTES,
                                      backupCount=LOG_FILE_BACKUPS, encoding="utf-8")
    except OSError as exc:
        print(f"[warn] cannot write the log file {path}: {exc}", file=sys.stderr, flush=True)
        return
    handler._vedha_file = True  # type: ignore[attr-defined]
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)-7s %(name)s: %(message)s"))
    root.addHandler(handler)
    root.setLevel(min(root.level or logging.INFO, getattr(logging, level_name)))
    _SAY_LOG.addHandler(handler)
    _SAY_LOG.setLevel(logging.INFO)


def _poll_jobs_or_empty(transport: Transport, limit: int) -> list[dict]:
    """Poll for work. Auth failures (TransportError) and transient network
    failures both propagate to the caller's unified retry/backoff handler so
    outages are diagnosed and rate-limited rather than silently swallowed."""
    return transport.poll_jobs(limit=limit)


def main() -> None:
    global _STATUS_PATH
    # ── Load environment ──────────────────────────────────────────────────────
    _load_env(Path(__file__).resolve().parent.parent / "probe.env")
    # The installer's configuration file (Windows: %ProgramData%\vedha-agent\agent.env).
    # An explicit environment variable always wins over it.
    from agent import diagnostics
    _load_env_file = diagnostics.default_env_file()
    if _load_env_file is not None:
        _load_env(_load_env_file)

    # Logging BEFORE anything else, so startup failures are narrated too.
    level = configure_logging()
    logging.getLogger("agent").info("Vedha Probe %s starting (log level %s)", VERSION, level)

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
    STATE_FILE = Path(os.environ.get("STATE_FILE", "/var/lib/vedha-agent/state.json"))

    # ── One probe per state file ──────────────────────────────────────────────
    # STATE_FILE holds the probe's IDENTITY. A second process sharing it is not a
    # second probe, it is a second impersonation of the same one: both heartbeat
    # for one agent_id, both claim jobs, and — the part that actually corrupts
    # results — both scan, doubling the probe rate the target sees from a single
    # source. Hosts that rate-limit RSTs then suppress replies, and suppressed
    # replies are reported as `filtered`. Two honest probes manufacture false
    # negatives in each other's scans. Refuse early and say exactly how to fix it.
    # Held for the process lifetime; the kernel releases it if we die.
    try:
        _INSTANCE_LOCK = acquire_instance_lock(STATE_FILE)
    except InstanceLockError as exc:
        say("")
        say("=" * 62)
        say("  ANOTHER PROBE IS ALREADY RUNNING")
        say("=" * 62)
        say(f"  {exc}")
        say("")
        say("  Two probes sharing one state file share ONE identity. They")
        say("  corrupt each other's job leases and, because both scan, they")
        say("  double the load on every target — which makes hosts suppress")
        say("  replies and turns real 'closed' ports into false 'filtered'.")
        say("")
        say("  Either stop the other probe, or give this one its own identity:")
        say(f"    STATE_FILE=~/vedha-agent/state-2.json {sys.argv[0] if sys.argv else 'probe'}")
        say("=" * 62)
        raise SystemExit(1) from exc

    # Only the process that holds the lock may describe the agent's state.
    from agent import runtime_status
    _STATUS_PATH = Path(os.environ.get("PROBE_STATUS_FILE") or runtime_status.path_for(STATE_FILE))
    _status("starting", detail="loading configuration")

    SPOOL_DIR = Path(os.environ.get("RESULT_SPOOL_DIR", "/var/lib/vedha-agent/spool"))
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

    # ── Auto-troubleshoot: catch the silent job-blockers before connecting ────
    # Surfaces a scan-ceiling/network mismatch (the #1 "connected but never
    # scans" cause) at startup instead of leaving it to be discovered by a job
    # that quietly never runs. Warnings only — never blocks startup.
    _preflight_scope_check(NETWORK_SEGMENTS)
    _preflight_connect_fast_fail()

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

    # Stand up the local result archive now, so the directory exists and any
    # permission problem is reported at boot rather than after the first scan.
    # Unlike the spool above (a delivery buffer that empties itself on success),
    # this keeps every submitted payload for offline accuracy review.
    from agent.task_runner import prepare_result_dir
    prepare_result_dir()

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
    _status("online", detail=f"{action.lower()} as '{PROBE_NAME}'; starting to listen for jobs")

    from agent.engine import CAPABILITIES
    from agent.use_cases import USE_CASES
    say(f"Capabilities: {', '.join(CAPABILITIES)}")
    say(f"Use-case library: {', '.join(sorted(USE_CASES))}")

    # What this HOST can sustain, stated once at startup. Conntrack overflow and
    # neighbour-table eviction drop packets with no error returned to userspace,
    # so the scanner records them as `filtered` and cannot tell they were its own
    # limits. Printing the ceilings is the only way that failure is ever
    # diagnosable. Advisory: nothing here blocks a job.
    try:
        from agent.kernel_limits import describe_capability, probe_limits
        say(describe_capability(probe_limits()))
    except Exception as exc:  # noqa: BLE001 — diagnostics must never stop startup
        _dbg(f"kernel-limit preflight skipped: {exc!r}")

    # ── Update check (version management only) ──────────────────────────────
    # Ask the manager whether a newer agent exists. Best effort — it never raises
    # and never delays the scan loop. A person at the terminal is asked y/N; a
    # headless agent (service, container) only logs it. A background re-check
    # runs every few hours and logs once per new version. Nothing is downloaded
    # or installed here. See agent/update_check.py.
    try:
        import platform as _platform
        from agent import update_check
        _arch = _platform.machine() or "unknown"
        update_check.run_startup_check(
            transport, VERSION, platform=sys.platform, architecture=_arch, say=say,
        )
        _apply = None
        try:
            from agent import auto_update
            auto_update.cleanup_after_update()          # remove a finished update's one-shot task and files
            if auto_update.enabled():
                _apply = lambda info: auto_update.apply_update(  # noqa: E731
                    transport, info, manager_url=PLATFORM_URL, platform=sys.platform, architecture=_arch)
                say("Automatic update: on (PROBE_AUTO_UPDATE). It only runs while no scan is running.")
        except Exception as exc:  # noqa: BLE001
            _dbg(f"auto-update setup skipped: {exc!r}")
        update_check.PeriodicUpdateChecker(
            transport, VERSION, platform=sys.platform, architecture=_arch, say=say, apply=_apply,
        ).start()
    except Exception as exc:  # noqa: BLE001 — a version check must never stop startup
        _dbg(f"update check skipped: {exc!r}")

    # ── Step 4: Create TaskRunner (with identity for scope decryption) ────────
    from agent.task_runner import TaskRunner
    runner = TaskRunner(
        http_get=transport.http_get,
        submit_result=lambda jid, p: transport.submit_result(jid, p),
        spool_submit=spool.submit_with_retry,
        identity_sk=identity_sk,   # Phase 4: X25519 private key for scope decryption
        local_allowed_networks=NETWORK_SEGMENTS,
        local_excluded_networks=SITE_EXCLUDED_SEGMENTS,
        # Per-host evidence buffer: commit each finished host while the job runs,
        # and skip on retry whatever the manager already holds. Both are
        # best-effort inside Transport, so an older manager without the chunk
        # endpoints changes nothing.
        submit_chunk=transport.submit_chunk,
        committed_hosts=transport.committed_hosts,
    )

    # ── Step 5: Try WebSocket push mode first ────────────────────────────────
    # Phase 2: persistent WebSocket connection with manager push.
    # If the manager supports WS, the probe stays in push mode indefinitely.
    # If WS fails (manager down, network issue, unsupported), fall through
    # to HTTP polling below.
    ws_mode_available = os.environ.get("PROBE_WS_ENABLED", "true").lower() not in (
        "false", "0", "no",
    )

    push_retry_secs = _bounded_env_int("PROBE_PUSH_RETRY_SECS", 300, 60, 3600)
    if ws_mode_available:
        if _attempt_push_mode(transport, runner, agent_id, spool, HEARTBEAT_INTERVAL, POLL_INTERVAL):
            return
    else:
        # Flush spool over HTTP before entering poll loop
        flushed = spool.flush_spool(
            lambda jid, p: transport.submit_result(jid, p),
        )
        if flushed:
            say(f"Flushed {flushed} spooled result(s) from previous run(s).")

    # ── Step 6: Main loop (HTTP polling — fallback) ──────────────────────────
    say("Waiting for scan jobs (HTTP polling)...")
    _status("online", detail="connected to the manager (polling); waiting for jobs")
    next_push_attempt = time.monotonic() + push_retry_secs
    last_hb = 0.0
    last_spool_warning = 0.0
    # Runtime resilience: an already-onboarded probe rides out Manager restarts
    # (results are spooled), but never silently hot-loops — failures back off and
    # escalate to a diagnosed warning so the operator can act.
    poll_fail_streak = 0
    POLL_FAIL_BACKOFF_MAX = 60.0

    while True:
        now = time.monotonic()
        if _push_retry_due(enabled=ws_mode_available, unavailable_for_good=_PUSH_UNAVAILABLE_FOR_GOOD,
                           now=now, next_attempt=next_push_attempt):
            # No job is running here (jobs run inline below), so it is safe to leave polling for a while.
            say("Trying push mode again...")
            if _attempt_push_mode(transport, runner, agent_id, spool, HEARTBEAT_INTERVAL, POLL_INTERVAL):
                return
            say("Waiting for scan jobs (HTTP polling)...")
            _status("online", detail="connected to the manager (polling); waiting for jobs")
            next_push_attempt = time.monotonic() + push_retry_secs
            now = time.monotonic()
        jobs: list[dict] = []
        try:
            if now - last_hb >= HEARTBEAT_INTERVAL:
                if not transport.heartbeat(
                    _heartbeat_status(spool, None), None,
                ):
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

            if poll_fail_streak:
                _status("online", detail="connected to the manager (polling); waiting for jobs")
            poll_fail_streak = 0  # a clean pass clears the outage counter

        except AccessExpiredError:
            # Access expiry set in Fleet: wait, keep the identity (no clear_state,
            # no re-enrolment) and resume by itself once the date is extended.
            wait = _bounded_env_int("PROBE_EXPIRED_RETRY_SECS", 300, 30, 3600)
            say("This agent's access has expired (set in Fleet). Waiting — it resumes "
                f"by itself once extended. Re-checking in {wait // 60 or 1} min.", 1)
            time.sleep(wait)
            continue
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
            _status("retrying", reason=reason, remediation=fix,
                    detail=f"manager unreachable (streak {poll_fail_streak})")
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


def _attempt_push_mode(transport, runner, agent_id, spool, heartbeat_interval, poll_interval) -> bool:
    """Run WebSocket push mode until it becomes unusable. True = the probe should stop; False = carry on by
    polling over HTTP (the caller may try push mode again later)."""
    say("Attempting WebSocket push mode...")
    try:
        ws_result = asyncio.run(_run_ws_push_loop(
            transport, runner, agent_id, spool, heartbeat_interval, poll_interval,
        ))
        if ws_result:
            # WS loop exited cleanly (shutdown or unrecoverable error)
            say("WebSocket loop exited. Probe stopping.")
            return True
        # ws_result is False → WS unavailable, fall through to HTTP poll
    except KeyboardInterrupt:
        say("\nProbe stopped (WebSocket mode).")
        raise SystemExit(0)
    except Exception as exc:
        say(f"WebSocket mode crashed ({exc}) — falling back to HTTP poll.")
    return False


def _lease_deadline(job: dict) -> float | None:
    """The claim's `lease_expires_at`, as a monotonic deadline.

    Monotonic on purpose: wall-clock arithmetic would misjudge the lease if NTP
    stepped the clock mid-scan, which is exactly the kind of host event that
    also causes the heartbeat failures this is deciding about.

    Returns None when the manager sent nothing usable (an older manager), which
    tells the caller to fall back to counting failures.
    """
    raw = job.get("lease_expires_at")
    if not raw:
        return None
    try:
        parsed = datetime.fromisoformat(str(raw))
    except (TypeError, ValueError):
        return None
    if parsed.tzinfo is None:
        # The manager sends UTC. Reading a naive stamp as LOCAL time would look
        # hours expired on any host that is not on UTC.
        parsed = parsed.replace(tzinfo=timezone.utc)
    remaining = (parsed - datetime.now(timezone.utc)).total_seconds()
    return time.monotonic() + remaining


def _renewed_deadline(current: float, *, lease_duration: float | None,
                      now: float | None = None) -> float:
    """Push the local deadline out after a heartbeat the manager accepted.

    The duration is the one OBSERVED at claim time, so an operator who changes
    job_lease_seconds is followed automatically.
    """
    if not lease_duration:
        return current
    return (now if now is not None else time.monotonic()) + lease_duration


def _should_abandon_lease(*, failures: int, failure_limit: int,
                          lease_deadline: float | None) -> bool:
    """Has this probe genuinely lost its claim?

    When the lease expiry is known it is the ONLY thing that matters: counting
    failed heartbeats conflates "the manager took my job" with "the network
    hiccupped", and the count means different wall-clock times on different
    paths — three misses was 90s on the push path and 30s on the poll fallback,
    against a 300s lease either way.

    Without an expiry (an older manager) the count is all there is.
    """
    if lease_deadline is None:
        return failures >= failure_limit
    return time.monotonic() >= lease_deadline


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
    # Be exactly as patient as the manager. The claim already told us when the
    # lease runs out; abandoning earlier throws away work nobody has taken.
    lease_deadline = _lease_deadline(job)
    lease_duration = (
        max(0.0, lease_deadline - time.monotonic())
        if lease_deadline is not None else None
    )
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
                outcome = transport.heartbeat_ex("busy", job_id, attempt_id, fence)
                if outcome == HEARTBEAT_LEASE_REVOKED:
                    # 409 is DEFINITIVE: the operator cancelled this job (or it
                    # was reassigned). Unlike a network blip there is nothing to
                    # retry — the manager will reject our results anyway — so
                    # stop now and free the probe for the next queued job
                    # instead of burning the whole failure budget first.
                    say(
                        f"Job {job_id} was stopped by the operator "
                        f"(lease revoked) — abandoning it.",
                        1,
                    )
                    cancellation_event.set()
                elif outcome != HEARTBEAT_OK:
                    consecutive_failures += 1
                    if lease_deadline is not None:
                        left = max(0.0, lease_deadline - time.monotonic())
                        say(
                            f"Lease heartbeat failed for running job {job_id}; "
                            f"{left:.0f}s of lease remain — still scanning.",
                            1,
                        )
                    else:
                        say(
                            f"Lease heartbeat failed for running job {job_id}; "
                            f"failure {consecutive_failures}/{failure_limit}.",
                            1,
                        )
                    if _should_abandon_lease(
                        failures=consecutive_failures,
                        failure_limit=failure_limit,
                        lease_deadline=lease_deadline,
                    ):
                        say(f"Job {job_id}: lease lost — abandoning it.", 1)
                        cancellation_event.set()
                else:
                    consecutive_failures = 0
                    lease_deadline = _renewed_deadline(
                        lease_deadline, lease_duration=lease_duration,
                    ) if lease_deadline is not None else None


# ── P2: WebSocket push loop ────────────────────────────────────────────────

WS_RECONNECT_BACKOFF_MIN = 1.0
WS_RECONNECT_BACKOFF_MAX = 60.0
# Consecutive WS auth rejections (403/401) tolerated — each triggers a forced
# device-token refresh — before falling back to HTTP poll / re-registration.
WS_AUTH_FAIL_LIMIT = 3
# Set when push mode can NEVER work in this process (the WebSocket library is missing from the build). Every
# other reason for dropping to HTTP polling is treated as possibly temporary and retried (see _push_retry_due).
_PUSH_UNAVAILABLE_FOR_GOOD = False


def _push_retry_due(*, enabled: bool, unavailable_for_good: bool, now: float, next_attempt: float) -> bool:
    """Should the HTTP-poll loop hand control back to push mode now?

    Polling works, but a push agent is the normal state. Dropping to polling used to be permanent: after one
    blip (the manager restarting, a hello that timed out, a credential refresh that could not reach the
    manager) the agent polled until someone restarted it. So the poll loop tries push mode again at a slow,
    fixed interval, unless push can never work in this build."""
    return enabled and not unavailable_for_good and now >= next_attempt
# How long a job offer may sit staged, acked but unconfirmed, before the
# probe drops it. `pending_job` used to be cleared ONLY by a matching
# job_claim frame, so a confirmation that never arrived (multi-worker
# manager, Redis backplane miss, socket displaced between ack and claim)
# left the field set forever — and the poll fallback's own guard then
# skipped every cycle, so the probe kept heartbeating and never took
# another job. Far below the 300 s manager lease: the recovery has to be
# quicker than the failure it prevents.
WS_OFFER_TTL_SECONDS = 30.0

# Reported when the probe is refusing work because its result spool is at
# the high-water mark. Not a synonym for idle: an `online` probe is ready
# for a job, a `paused` one will decline every offer until uploads recover.
# The manager stops dispatching to it (push_job and the enqueue eligibility
# query both select on `online`), which is the correct behaviour AND makes
# the state visible instead of looking like a healthy idle probe.
PAUSED_STATUS = "paused"


def _spool_saturated(spool) -> bool:
    """Is the result spool refusing new work? Absent spool = no pressure."""
    try:
        return bool(spool is not None and spool.at_capacity)
    except Exception:  # noqa: BLE001 — back-pressure must never crash the loop
        return False


def _heartbeat_status(spool, current_job_id) -> str:
    """What this probe should tell the manager it is doing.

    A running job outranks spool pressure: `busy` is what carries
    current_job_id, and the manager renews that attempt's lease from it.
    """
    if current_job_id:
        return "busy"
    if _spool_saturated(spool):
        return PAUSED_STATUS
    return "online"


async def _run_ws_push_loop(
    transport: "Transport",
    runner,
    agent_id: str,
    spool,
    heartbeat_interval: int,
    poll_interval: int,
) -> bool:
    """Run WebSocket push mode until it becomes unusable, then return False so
    the caller falls back to HTTP polling.

    Before returning it waits for any job a poll task is still running, which
    can take as long as that scan: the HTTP poll loop must not start beside it.
    """
    pollers: set = set()
    try:
        result = await _ws_connection_loop(
            transport, runner, agent_id, spool,
            heartbeat_interval, poll_interval, pollers,
        )
    finally:
        # A poll task may still be finishing a job it claimed. Handing the
        # caller (the HTTP poll loop) a probe that looks idle mid-scan would
        # start a second job beside it. This runs even when the connection
        # loop raises, so a crash cannot leave a claimed job orphaned.
        await asyncio.gather(*pollers, return_exceptions=True)
    return result


async def _ws_connection_loop(
    transport: "Transport",
    runner,
    agent_id: str,
    spool,
    heartbeat_interval: int,
    poll_interval: int,
    pollers: set,
) -> bool:
    """Connect, serve pushed jobs with HTTP polling as a fallback, and reconnect
    with backoff. Returns False when push mode is unavailable. Registers every
    poll task it starts in `pollers` so the caller can wait for them."""
    import websockets.exceptions

    backoff = WS_RECONNECT_BACKOFF_MIN
    auth_failures = 0
    # The probe's one-job-at-a-time state belongs to the PROCESS, not to a
    # connection: a poll task outliving its socket must still see — and
    # update — the same busy flag and lock as every later connection.
    #   current_job_id — a job is RUNNING
    #   pending_job    — an offer is acked, awaiting the manager's claim
    #   pending_since  — when it was staged, so it can expire
    #   claiming       — the fallback is mid-claim and must not be raced
    job_state = {"current_job_id": None, "pending_job": None,
                 "pending_since": None, "claiming": False}
    job_lock = asyncio.Lock()

    while True:
        hb_task = None
        stop_polling = asyncio.Event()
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
            _status("online", detail="connected to the manager (live connection); waiting for jobs")
            backoff = WS_RECONNECT_BACKOFF_MIN  # reset on successful connect

            # Results use one durable path in every mode: local spool followed
            # by authenticated HTTP submission. WS is control-plane only.
            await _flush_spool_over_http(transport, spool)

            # ── Start heartbeat + HTTP poll fallback tasks ────────────────
            # WebSocket pushes are process-local on the manager. With multiple
            # API workers a launch request can land on a different worker than
            # the probe's WS connection, so keep polling as a safety net.
            #
            # An offer staged on an earlier connection can never be confirmed:
            # its claim frame would have arrived on the socket that died.
            job_state["pending_job"] = None
            job_state["pending_since"] = None
            hb_task = asyncio.create_task(
                _ws_heartbeat_sender(ws, agent_id, heartbeat_interval,
                                     job_state, spool),
            )
            poller = asyncio.create_task(
                _ws_http_poll_fallback(
                    ws, transport, runner, agent_id, spool,
                    poll_interval, job_lock, job_state, stop=stop_polling,
                ),
            )
            pollers.add(poller)
            poller.add_done_callback(pollers.discard)

            # Auth succeeded (hello_ok received above) — clear the auth-failure
            # streak so a later expiry gets its own full refresh budget.
            auth_failures = 0

            # ── Main receive loop ────────────────────────────────────────
            async for raw in ws:
                try:
                    msg = json.loads(raw)
                except json.JSONDecodeError:
                    continue

                msg_type = msg.get("type", "")

                if msg_type == "job_push":
                    await _ws_stage_job_offer(
                        ws, msg.get("job", {}), job_state, spool,
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

                elif msg_type == "access_expired":
                    # The manager closes the socket right after this; the reconnect
                    # path then waits (PROBE_EXPIRED_RETRY_SECS) instead of looping.
                    say(f"Access expired: {msg.get('message', 'extend it in Fleet')}")
                    break

        except websockets.exceptions.ConnectionClosed as exc:
            close_code = exc.rcvd.code if exc.rcvd is not None else None
            say(f"WebSocket closed (code={close_code}) — reconnecting in {backoff:.0f}s...")
            _status_connection_lost(f"live connection closed (code {close_code})")
        except (OSError, asyncio.TimeoutError) as exc:
            say(f"WebSocket unavailable ({exc}) — reconnecting in {backoff:.0f}s...")
            _status_connection_lost(f"live connection unavailable ({type(exc).__name__})")
        except TransportUnavailableError as exc:
            # The manager was unreachable (or answered 5xx) while the credential was refreshed: no verdict
            # was reached, so this is NOT a revoked credential. Retry with backoff; giving up here used to
            # drop the agent into HTTP polling for good after one blip (seen 11 Oct 2026).
            say(f"WebSocket: {exc} — reconnecting in {backoff:.0f}s...", 1)
            _status_connection_lost("manager unreachable while refreshing the credential")
        except TransportError as exc:
            say(f"WebSocket auth error: {exc} — falling back to HTTP poll.")
            return False
        except ImportError as exc:
            # The WebSocket library (or a part of it) is missing from this build. Retrying can
            # never fix that, and the agent must not sit silent: polling over HTTPS does the
            # same job (heartbeats, jobs), so say so and fall back to it.
            say(f"Push mode is not available in this build ({type(exc).__name__}: {exc}) "
                "— falling back to HTTP poll.")
            LOG.error("WebSocket support is missing from this build: %s", exc)
            global _PUSH_UNAVAILABLE_FOR_GOOD
            _PUSH_UNAVAILABLE_FOR_GOOD = True      # retrying can never help; the poll loop must not try again
            return False
        except Exception as exc:
            # A 403/401 on the WS upgrade means the manager REJECTED our token —
            # usually time-valid locally but stale to the manager (superseded
            # credential generation, revoked lease, or a redeployed manager).
            # Reconnecting with the same token loops on 403 forever; force a fresh
            # token and retry, and if forced refreshes keep failing the credential
            # is genuinely dead — fall back so the outer loop can re-register.
            code = getattr(getattr(exc, "response", None), "status_code", None)
            msg = str(exc)
            if code in (401, 403) or " 403" in msg or " 401" in msg:
                auth_failures += 1
                say(f"WebSocket rejected (auth) — refreshing device token and "
                    f"retrying [{auth_failures}/{WS_AUTH_FAIL_LIMIT}].", 1)
                refreshed = False
                try:
                    refreshed = await asyncio.to_thread(
                        transport.ensure_device_access, force=True)
                except Exception as rexc:  # noqa: BLE001
                    _dbg(f"forced device-access refresh raised: {rexc!r}")
                if transport.access_expired:
                    # Fleet-set access expiry, not a dead credential: stay in the
                    # loop, keep the identity, and retry slowly.
                    wait = _bounded_env_int("PROBE_EXPIRED_RETRY_SECS", 300, 30, 3600)
                    say("This agent's access has expired (set in Fleet). Waiting — it "
                        f"resumes by itself once extended. Re-checking in {wait // 60 or 1} min.", 1)
                    auth_failures = 0
                    await asyncio.sleep(wait)
                    continue
                if not refreshed or auth_failures >= WS_AUTH_FAIL_LIMIT:
                    say("WebSocket auth keeps failing — the device credential looks "
                        "stale; falling back to re-registration.", 1)
                    return False
                # Retry immediately with the fresh token — don't sit on the backoff.
                continue
            say(f"WebSocket error: {type(exc).__name__}: {exc} — reconnecting in {backoff:.0f}s...", 1)
            _status_connection_lost(f"live connection error ({type(exc).__name__})")
        finally:
            await _end_ws_session(hb_task, stop_polling)

        # Exponential backoff
        await asyncio.sleep(backoff)
        backoff = min(backoff * 2, WS_RECONNECT_BACKOFF_MAX)


async def _end_ws_session(hb_task, stop_polling: asyncio.Event) -> None:
    """Stop one connection's background work, on every exit path.

    The heartbeat sender only writes to this connection, so it is cancelled.
    The poll fallback is only told to stop: it may be running a job in a
    worker thread, and cancelling the coroutine that awaits that thread would
    clear current_job_id while the scan kept going. It exits once any job it
    holds has finished.
    """
    stop_polling.set()
    if hb_task is None:
        return
    hb_task.cancel()
    # wait() does not re-raise the task's own CancelledError, so a cancel aimed
    # at this coroutine still propagates.
    await asyncio.wait({hb_task})


def _ws_expire_stale_offer(job_state: dict, now: float | None = None) -> bool:
    """Drop a staged offer the manager never confirmed. True if dropped.

    Recovery, not policy: the job itself is already claimed manager-side,
    so its lease expires and the reaper requeues it. What this prevents is
    the PROBE being stranded behind a confirmation that is never coming.
    """
    staged_at = job_state.get("pending_since")
    if staged_at is None:
        return False
    if (now if now is not None else time.monotonic()) - staged_at < WS_OFFER_TTL_SECONDS:
        return False
    stranded = (job_state.get("pending_job") or {}).get("job_id", "?")
    say(f"Push offer {stranded} was never confirmed within "
        f"{WS_OFFER_TTL_SECONDS:.0f}s — dropping it and resuming polling.", 1)
    job_state["pending_job"] = None
    job_state["pending_since"] = None
    return True


def _ws_probe_is_free(job_state: dict) -> bool:
    """Can this probe take on a job right now?

    `claiming` is the reservation the HTTP poll fallback takes BEFORE it
    awaits. Without it the fallback checked its state, yielded, and a
    job_push arriving during that window was staged against state that was
    already stale — so the probe held two claims. job_lock then serialised
    execution, but the second job's lease had already started ticking and
    nothing renews a job that is not running.
    """
    return (
        job_state.get("current_job_id") is None
        and job_state.get("pending_job") is None
        and not job_state.get("claiming")
    )


async def _ws_stage_job_offer(ws, job: dict, job_state: dict,
                              spool=None) -> bool:
    """Acknowledge an offer without executing it before claim confirmation.

    Declines while the result spool is saturated. The HTTP-only poll loop
    has always applied that back-pressure; this path — the DEFAULT one —
    did not, so a probe that could not deliver its results kept taking on
    work that produced more of them.
    """
    job_id = job.get("job_id")
    _ws_expire_stale_offer(job_state)
    can_accept = bool(
        job_id
        and _ws_probe_is_free(job_state)
        and not _spool_saturated(spool)
    )
    if can_accept:
        job_state["pending_job"] = job
        job_state["pending_since"] = time.monotonic()
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
    # Clear the clock with the offer — a leftover timestamp would expire
    # the NEXT offer the moment it is staged.
    job_state["pending_since"] = None
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
    try:
        from agent import auto_update
        auto_update.mark_job_started()          # an automatic update waits until no scan is running
    except Exception:  # noqa: BLE001
        pass
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
            "agent_version": VERSION,
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
        try:
            from agent import auto_update
            auto_update.mark_job_finished()
        except Exception:  # noqa: BLE001
            pass
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
                "agent_version": VERSION,
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
    stop: asyncio.Event | None = None,
) -> None:
    """Poll pending jobs even while WS is connected.

    This makes result delivery reliable when manager WS pushes are missed, for
    example under multi-worker API deployments with process-local WS state.
    """
    stop = stop or asyncio.Event()
    while not stop.is_set():
        try:
            await asyncio.wait_for(stop.wait(), timeout=max(1, interval))
            return                  # the connection ended while this was idle
        except asyncio.TimeoutError:
            pass
        # An offer the manager never confirmed must not strand this loop.
        _ws_expire_stale_offer(job_state)
        if not _ws_probe_is_free(job_state) or _spool_saturated(spool):
            continue
        # RESERVE BEFORE YIELDING. Everything below awaits, and a job_push
        # arriving mid-await would otherwise be staged against state that says
        # this probe is idle — two claims, one probe. The reservation is held
        # across the poll AND the run, and released in exactly one place.
        job_state["claiming"] = True
        try:
            jobs = await asyncio.to_thread(transport.poll_jobs, 1)
            if not jobs:
                continue
            async with job_lock:
                for job in jobs:
                    await _ws_run_job(ws, runner, agent_id, job, job_state,
                                      pushed=False, transport=transport,
                                      heartbeat_interval=max(5, interval))
                    await _flush_spool_over_http(transport, spool)
        except TransportError as exc:
            say(f"HTTP poll fallback auth error: {exc} — reconnecting.")
            await ws.close()
            return
        except Exception as exc:
            say(f"HTTP poll fallback failed ({exc})", 1)
            continue
        finally:
            job_state["claiming"] = False


async def _ws_heartbeat_sender(
    ws,
    agent_id: str,
    interval: int,
    job_state: dict | None = None,
    spool=None,
) -> None:
    """Send periodic heartbeats over WebSocket."""
    try:
        while True:
            await asyncio.sleep(interval)
            current_job_id = (job_state or {}).get("current_job_id")
            await ws.send(json.dumps({
                "type": "heartbeat",
                "status": _heartbeat_status(spool, current_job_id),
                "current_job_id": current_job_id,
                "attempt_id": (job_state or {}).get("attempt_id"),
                "fence": (job_state or {}).get("fence"),
                "agent_version": VERSION,
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
        say("║    1. Run: ./vedha-agent hostid                           ║")
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
    _recreate_budget: int = 3,
) -> dict:
    """Request UI approval, poll, prove key possession, and activate.

    `_recreate_budget` bounds how many times a stored enrollment request that the
    manager 404s (spent/expired/purged) may be discarded and re-created before we
    give up — so a manager that keeps losing requests fails loudly instead of
    looping, while an ordinary stale request self-heals on the next attempt."""
    from agent.device_identity import sign_b64
    from agent.engine import CAPABILITIES

    state = transport.load_state()
    request_id = state.get("enrollment_request_id")
    device_secret = state.get("enrollment_device_secret")
    poll_interval = 5
    # A request created by THIS call may 404 for a moment: a manager that commits
    # after responding (or a replica behind it) can answer the first poll before
    # the row is visible. Treating that as "gone" re-enrols, and with a
    # single-use install token that burns the token. Allow a short grace window.
    fresh_until = 0.0
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
        fresh_until = time.monotonic() + 15
        transport.update_state({
            "enrollment_request_id": request_id,
            "enrollment_device_secret": device_secret,
        })
        _dbg(f"enrollment request created → state={response.get('state')} "
             f"request_id={request_id} auto={response.get('state') == 'approved'}")
        if response.get("state") == "approved":
            say("Probe pre-authorized via enrollment token — auto-approving, no code needed.")
            _status("enrolling", detail="install token accepted; registering with the manager")
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
            _status("awaiting-approval", pairing_code=str(code), pairing_url=url,
                    detail="a person must approve this agent in Fleet")

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
        except EnrollmentRequestNotFound as exc:
            if time.monotonic() < fresh_until:
                _dbg("enrollment request not visible yet — retrying within the grace window")
                time.sleep(1)
                continue
            # The request we were polling is GONE on the manager (spent, expired,
            # purged, or the manager's enrollment store was reset). This is the
            # bug that surfaced as "connection error … retrying [n/12]" then a
            # false "Manager unreachable": a 404 is authoritative, so discard the
            # dead request and create a fresh one instead of retrying the id.
            transport.update_state(remove=("enrollment_request_id", "enrollment_device_secret"))
            if _recreate_budget <= 0:
                say("")
                say("═" * 58)
                say("  ENROLLMENT FAILED — manager keeps losing the request")
                say("═" * 58)
                say("  The manager accepted enrollment requests but then reported")
                say("  them missing (HTTP 404) repeatedly. This points at the")
                say("  manager side, not the network:")
                say("   • its probe-enrollment service / Redis was reset mid-flight, or")
                say("   • requests are evicted faster than approval completes, or")
                say("   • it is load-balanced across instances with a non-shared store.")
                say("═" * 58)
                raise SystemExit(2) from exc
            say("Stored enrollment request no longer exists on the manager — "
                f"starting a fresh enrollment ({_recreate_budget} attempt(s) left).")
            return _enroll_device(
                transport,
                signing_private_key=signing_private_key,
                signing_public_key=signing_public_key,
                encryption_public_key=encryption_public_key,
                probe_name=probe_name,
                _recreate_budget=_recreate_budget - 1,
            )
        except TransportError:
            raise
        except SystemExit:
            raise
        except ValueError as exc:
            # The manager ANSWERED (poll/activate returned 200) but its response
            # failed a verification check — almost always the site-policy signing
            # key ("...changed outside an approved rotation"). This is NOT a
            # network fault, so retrying it as a "connection error" (the old bug)
            # just spun forever at [1/12]. A deliberate manager re-point clears
            # the pin up front (clear_manager_binding); reaching here means the
            # pin is still set and mismatched — security-relevant, so stop loud.
            say("")
            say("═" * 58)
            say("  ENROLLMENT REJECTED — site policy verification failed")
            say("═" * 58)
            say(f"  Why : {exc}")
            say("  If you deliberately re-pointed this probe to a DIFFERENT")
            say("  manager, clear its identity and re-enroll:")
            say("     mv ~/vedha-agent/state.json ~/vedha-agent/state.json.bak")
            say("  Otherwise the manager's policy-signing key changed")
            say("  unexpectedly — investigate before trusting it.")
            say("═" * 58)
            raise SystemExit(1) from exc
        except Exception as exc:
            net_fail_streak += 1
            reason, fix = _classify_connection_error(exc, transport._base_url)
            if net_fail_streak >= NET_FAIL_LIMIT and not _keep_retrying():
                say("")
                say("═" * 58)
                say("  ENROLLMENT FAILED — Manager unreachable")
                say("═" * 58)
                say(f"  Why : {reason}")
                say(f"  Fix : {fix}")
                say("═" * 58)
                _status("failed", reason=reason, remediation=fix)
                raise SystemExit(2) from exc
            progress = f"{net_fail_streak}" if _keep_retrying() else f"{net_fail_streak}/{NET_FAIL_LIMIT}"
            _status("retrying", reason=reason, remediation=fix, detail=f"enrolment attempt {progress}")
            say(f"Enrollment manager unavailable ({reason}) — retrying [{progress}].")
            _dbg(f"enrollment poll failure: {exc!r}")
            time.sleep(_retry_wait(net_fail_streak))


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
        # Transient-failure budget, kept separate from _refresh_tries: a manager
        # that cannot ANSWER is a different situation from one that answers "no".
        _unavail_tries = 0
        _UNAVAIL_LIMIT = _bounded_env_int("PROBE_CREDENTIAL_RETRY_LIMIT", 5, 1, 50)
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
                outcome = transport.refresh_device_access_ex(signing_sk)
                if outcome == DEVICE_REFRESH_OK:
                    say("Refreshed short-lived device access token.", 1)
                    continue

                if outcome == DEVICE_REFRESH_EXPIRED:
                    # Access expiry set in Fleet. The credential is fine; the
                    # manager will accept it again as soon as an administrator
                    # extends the date. Keep the identity, stay quiet, retry slowly
                    # — never stop (a restart loop) or re-enrol (a stray request).
                    wait = _bounded_env_int("PROBE_EXPIRED_RETRY_SECS", 300, 30, 3600)
                    say("This agent's access has expired (set in Fleet). Waiting — it "
                        f"resumes by itself once an administrator extends it. "
                        f"Re-checking in {wait // 60 or 1} min.", 1)
                    time.sleep(wait)
                    continue

                # WHOSE credential is this? Device credentials are issued BY a
                # manager and are meaningless to any other one, so before calling
                # anything a revocation we check we are even talking to the
                # issuer. Pointing a probe at a second manager used to print
                # "revoked ... stopping for administrator review" and exit — an
                # alarming, wrong diagnosis for an ordinary re-point.
                issuer = state.get("manager_fingerprint")
                current = manager_fingerprint(transport._base_url)
                if issuer and issuer != current:
                    say(f"These credentials were issued by {issuer}, but this "
                        f"probe is pointed at {current}.", 1)
                    say("Re-enrolling with the new manager (the old credential "
                        "is untouched and still valid there).", 1)
                    # FULL unbind, not just agent_id/token: the old manager's
                    # pinned site-policy key would otherwise reject the new
                    # manager's policy at activation and loop forever.
                    transport.clear_manager_binding()
                    break

                if outcome == DEVICE_REFRESH_UNAVAILABLE:
                    # We never got a VERDICT — a network failure, a 5xx, or the
                    # manager's 503 "replay protection unavailable". Treating
                    # that as revocation meant a brief manager-side outage could
                    # permanently stop the whole fleet.
                    #
                    # Retry, then give up WITHOUT clearing state: if the manager
                    # cannot answer, re-enrolling cannot work either, and
                    # discarding a valid device credential during an outage
                    # turns a five-minute blip into a manual re-enrollment.
                    # Exit 2 (not 1) so callers can tell "unreachable" from
                    # "revoked".
                    _unavail_tries += 1
                    if _unavail_tries >= _UNAVAIL_LIMIT:
                        say(f"Manager could not answer the credential refresh after "
                            f"{_unavail_tries} attempts.")
                        say("This is NOT a revocation — the credential is kept. "
                            "Check the manager, then re-run.", 1)
                        raise SystemExit(2)
                    say(f"Credential refresh unavailable (temporary) — retrying "
                        f"({_unavail_tries}/{_UNAVAIL_LIMIT}).", 1)
                    time.sleep(min(30, 5 * _unavail_tries))
                    continue

                if state.get("device_refresh_secret"):
                    if not issuer:
                        # LEGACY state, enrolled before credentials recorded their
                        # issuer. We genuinely cannot tell "revoked by this
                        # manager" from "belongs to a different one", so say that
                        # instead of asserting the alarming reading — and give the
                        # operator the exact way out. State is kept, so a probe
                        # pointed back at its real manager still works.
                        say("Cached device credential was refused by "
                            f"{current}, and it does not record which manager "
                            "issued it (enrolled before that was tracked).")
                        say("If this is a DIFFERENT manager, re-enroll against it "
                            "with a separate state file, e.g.:", 1)
                        say("STATE_FILE=~/vedha-agent/state-<manager>.json "
                            "./install.sh <manager> --enroll", 2)
                        say("If this IS the issuing manager, the credential was "
                            "revoked or disabled — see an administrator.", 1)
                        raise SystemExit(1)
                    # Same manager, authoritative rejection: genuinely revoked,
                    # disabled, or superseded by a newer credential generation.
                    say("Device credential was revoked, expired, or disabled by "
                        f"{current}; stopping for administrator review.")
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
    # A configured PAT/token (typically from probe.env) that the manager rejects
    # should not dead-end when operator email/password are ALSO available: drop
    # the dead token and retry via login. Guarded to run once so a genuinely bad
    # password cannot loop.
    pat_fallback_done = False
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
                login = r.json()
                if "access_token" not in login:
                    # Two-step sign-in cannot be completed unattended.
                    say("This operator account uses two-step sign-in. Set PROBE_PAT (or PROBE_BOOTSTRAP_KEY) instead of a password.")
                    raise SystemExit(1)
                operator_token = login["access_token"]

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
            # dead-end the probe. Prefer self-healing, in this order:
            #
            #   1. A configured PAT/OPERATOR_TOKEN was rejected but we ALSO have
            #      operator email/password: drop the dead token and retry via
            #      login. This is the common "stale probe.env PROBE_PAT" case —
            #      a token minted against a manager that was since recreated,
            #      expired, or revoked. Without this the probe stopped with a
            #      misleading "check credentials" even though the password worked.
            if operator_token and email and password and not pat_fallback_done:
                pat_fallback_done = True
                say("Configured PROBE_PAT/OPERATOR_TOKEN was rejected — "
                    "falling back to operator sign-in.")
                operator_token = ""
                continue
            #   2. A token was the ONLY credential (no login, no bootstrap key):
            #      fall back to DEVICE ENROLLMENT — the probe's own keypair is its
            #      id, and the Manager issues a token (auto-approved when
            #      PROBE_AUTO_ENROLL is on, else a pairing code). This is what
            #      makes a bare `install.sh <manager-ip>` self-heal.
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
            #   3. Nothing else to try — say WHICH credential failed so the fix is
            #      obvious (re-mint the PAT vs check the password), not a vague
            #      "check credentials".
            if operator_token:
                say("Manager rejected the configured PROBE_PAT/OPERATOR_TOKEN — it is "
                    "expired, revoked, or was minted against a different manager.")
                say("Re-mint one with `make probe-pat`, or clear PROBE_PAT to use "
                    "OPERATOR_EMAIL/OPERATOR_PASSWORD.", 1)
            else:
                say("Manager rejected sign-in — check OPERATOR_EMAIL / OPERATOR_PASSWORD.")
            raise SystemExit(1)
        except SystemExit:
            raise
        except Exception as exc:
            reg_fail_streak += 1
            reason, fix = _classify_connection_error(exc, transport._base_url)
            if reg_fail_streak >= REG_FAIL_LIMIT and not _keep_retrying():
                say("")
                say("═" * 58)
                say("  REGISTRATION FAILED — Manager unreachable")
                say("═" * 58)
                say(f"  Why : {reason}")
                say(f"  Fix : {fix}")
                say("═" * 58)
                _status("failed", reason=reason, remediation=fix)
                raise SystemExit(2) from exc
            progress = f"{reg_fail_streak}" if _keep_retrying() else f"{reg_fail_streak}/{REG_FAIL_LIMIT}"
            _status("retrying", reason=reason, remediation=fix, detail=f"registration attempt {progress}")
            say(f"Can't reach manager yet ({reason}) — retrying [{progress}].")
            _dbg(f"registration failure: {exc!r}")
            time.sleep(_retry_wait(reg_fail_streak))



def _library_entry_point_failures() -> list[str]:
    """Use the real entry points of the libraries the agent relies on.

    A library that loads parts of itself lazily, by name, is invisible to a compiler: importing
    the package succeeds and the missing part shows up only when it is used (a compiled agent once
    registered fine and then could not open its WebSocket: websockets.asyncio was absent). So this
    does not just import: it opens a connection to a closed local port and signs with the real keys.
    Anything except a missing module counts as the library having loaded and tried. Offline."""
    failures: list[str] = []

    def probe(label: str, action) -> None:
        try:
            action()
        except ImportError as exc:
            failures.append(f"{label}: {type(exc).__name__}: {exc}")
        except Exception:  # noqa: BLE001 - refused / timed out: the library loaded and tried
            pass

    def websocket_connect() -> None:
        import websockets

        async def attempt() -> None:
            await asyncio.wait_for(websockets.connect("ws://127.0.0.1:9", open_timeout=2), timeout=5)

        asyncio.run(attempt())

    def https_request() -> None:
        import httpx
        httpx.get("https://127.0.0.1:9", timeout=2)

    def identity_keys() -> None:
        from cryptography.hazmat.primitives.asymmetric import ed25519, x25519
        x25519.X25519PrivateKey.generate().public_key()
        ed25519.Ed25519PrivateKey.generate().sign(b"vedha")

    probe("websockets (live connection)", websocket_connect)
    probe("httpx (HTTPS client)", https_request)
    probe("cryptography (identity keys)", identity_keys)
    return failures


USAGE = """Vedha agent {version}

Usage: vedha-agent [command]

  run              start the agent (this is what the installed service does)
  doctor           check this computer's connection to the manager and explain any problem
                   (doctor --preinstall: only the checks that make sense before installing)
  status [--json]  show what the agent is doing right now
  support-bundle   [--out FILE] [--mask-ips]   write a redacted zip to send to Vedha support
  version          print the agent version
  hostid           print this host's identifier
  help             show this text
"""

_DIAGNOSTIC_COMMANDS = ("doctor", "status", "support-bundle")


def _diagnostic_command(arg: str, args: list[str]) -> int:
    """doctor / status / support-bundle. Read-only: they never change the client's
    settings and never touch the agent's credentials."""
    from agent import diagnostics
    env_file = diagnostics.default_env_file()
    if env_file is not None:
        _load_env(env_file)
    _force_utf8_streams()
    if arg == "doctor":
        checks = diagnostics.run_doctor(preinstall="--preinstall" in args)
        say(diagnostics.format_doctor(checks))
        return 1 if any(c.status == "fail" for c in checks) else 0
    if arg == "status":
        info = diagnostics.collect_status()
        if "--json" in args:
            import json
            print(json.dumps(info, indent=2, default=str))
        else:
            say(diagnostics.format_status(info))
        return 0 if info.get("state") == "online" else 1
    # support-bundle
    out = None
    if "--out" in args:
        index = args.index("--out")
        out = args[index + 1] if index + 1 < len(args) else None
        if out is None:
            say("--out needs a file name, for example: support-bundle --out C:\\Temp\\vedha-support.zip")
            return 2
    path = diagnostics.build_support_bundle(out, mask_ips="--mask-ips" in args)
    say(f"Support bundle written to: {path}")
    say("It contains no passwords, tokens or keys. Logs do contain host names and IP addresses"
        + (" (masked)." if "--mask-ips" in args else " (add --mask-ips to hide them)."))
    say("Please email this file to your Vedha contact.")
    return 0


if __name__ == "__main__":
    try:
        arg = sys.argv[1] if len(sys.argv) > 1 else "run"
        if arg in ("help", "-h", "--help"):
            say(USAGE.format(version=VERSION))
        elif arg in _DIAGNOSTIC_COMMANDS:
            sys.exit(_diagnostic_command(arg, sys.argv[2:]))
        elif arg in ("version", "-v", "--version"):
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
        elif arg == "runtime-check":
            # Build gate for the compiled / closure-only agent: import every
            # module of ours it may load (lazily, mid-scan) plus its third-party
            # libraries. A module the compiler or the image dropped fails HERE,
            # at build time, instead of as ModuleNotFoundError in a customer scan.
            # No network, no licence, no host state.
            import importlib
            from agent._closure import MODULES
            failed = []
            for name in MODULES:
                try:
                    importlib.import_module(name)  # agent-closure: verified-names
                except Exception as exc:  # noqa: BLE001 — report every broken module
                    failed.append(f"{name}: {type(exc).__name__}: {exc}")
            for lib in ("httpx", "websockets", "cryptography", "impacket", "ldap3", "dns.resolver"):
                try:
                    importlib.import_module(lib)  # agent-closure: verified-names
                except Exception as exc:  # noqa: BLE001
                    failed.append(f"{lib}: {type(exc).__name__}: {exc}")
            failed.extend(_library_entry_point_failures())
            if failed:
                print("runtime-check FAILED:\n  " + "\n  ".join(failed))
                sys.exit(1)
            print(f"runtime-check OK: {len(MODULES)} agent modules and 6 libraries load "
                  "(connection, HTTPS and key entry points exercised)")
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
            _load_env(Path(__file__).resolve().parent.parent / "probe.env")
            configure_logging()
            from agent.local_run import run as _local_run
            raise SystemExit(_local_run(sys.argv[2:]))
        elif arg == "run":
            try:
                main()
            except Exception as exc:  # noqa: BLE001 — recorded in the log and status, then a non-zero exit
                _record_crash(exc)
                sys.exit(1)
        else:
            # A mistyped command used to start the whole agent. Say so instead.
            say(f"Unknown command: {arg}")
            say(USAGE.format(version=VERSION))
            sys.exit(2)
    except KeyboardInterrupt:
        say("\nProbe stopped.")
        sys.exit(0)

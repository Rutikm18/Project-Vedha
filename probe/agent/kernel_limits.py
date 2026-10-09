"""kernel_limits.py — measure the OS ceilings a wide scan actually runs into.

WHY THIS EXISTS
---------------
scanner_base._ERRNO_MAP already handles the resource failures the kernel REPORTS
BACK: EMFILE, ENOBUFS and EADDRNOTAVAIL become `local_resource_error`, never
`filtered`, and any one of them sets ScanMetrics.degraded. That covers the honest
half of the problem.

The limits measured here are the other half. When conntrack fills, or the
neighbour table overflows, the kernel drops the packet with NO error returned to
userspace. The scanner sees silence, waits out its timeout, and records
`filtered` — a claim about the TARGET produced entirely by a limit on the
SCANNER. It is invisible from the inside, so the only defence is to measure the
ceilings before the scan and say what they are.

The arithmetic each check encodes:

  ephemeral ports  Every connect() holds a local port in TIME_WAIT for 60s, so
                   the sustainable connect rate is capacity/60 — ~470/sec on the
                   default 32768-60999 range. This is a HARD ceiling on connect
                   scanning that no amount of concurrency raises.
  conntrack        Docker's default bridge network is NAT, so every probe takes
                   a conntrack entry, held for nf_conntrack_tcp_timeout_syn_sent
                   (120s) when unanswered. Steady-state demand is rate x 120.
  neighbour table  gc_thresh3 defaults to 1024. Sweeping more hosts than that on
                   one L2 segment evicts live entries and drops packets.
  fds              safe_connect_concurrency() guards this on the CLI path only;
                   the agent path constructs PortScanner directly.
  raw sockets      Without CAP_NET_RAW a wide sweep silently becomes 65,535
                   connect() per host, which the ephemeral ceiling above makes
                   impossible. Better to know than to discover it in hour nine.

ADVISORY ONLY. Nothing here blocks a scan — admission control owns refusals, and
`doctor` must not start failing because a host is merely under-tuned. Every
check returns "pass" or "warn", never "fail".

A limit that cannot be read (not Linux, no netfilter, container without /proc)
yields None and is skipped; assess() notes the skipped set ONCE rather than
emitting a warning per missing file.
"""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from pathlib import Path

from agent.doctor import Check, format_report

# Linux TCP_TIMEWAIT_LEN — 2*MSL, not tunable without a kernel rebuild.
TIME_WAIT_SECONDS = 60
# nf_conntrack_tcp_timeout_syn_sent default: how long an UNANSWERED SYN (the
# common case in a port sweep) occupies a conntrack slot.
CONNTRACK_SYN_SENT_SECONDS = 120
# Keep concurrency this far below the fd soft limit — mirrors the margin
# safe_connect_concurrency() already uses so the two agree.
FD_MARGIN = 200
# Fraction of gc_thresh3 a sweep may reach before it is worth warning about.
NEIGHBOUR_HEADROOM = 0.8
# Below this many ports, running over connect() instead of SYN is unremarkable.
WIDE_SWEEP_PORTS = 1024

_PROC = Path("/proc/sys")
_CONNTRACK_MAX = _PROC / "net/netfilter/nf_conntrack_max"
_CONNTRACK_COUNT = _PROC / "net/netfilter/nf_conntrack_count"
_PORT_RANGE = _PROC / "net/ipv4/ip_local_port_range"
_GC_THRESH3 = _PROC / "net/ipv4/neigh/default/gc_thresh3"


@dataclass(frozen=True)
class KernelLimits:
    """Raw ceilings as read from the host. None = could not be read."""
    fd_soft: int | None
    fd_hard: int | None
    conntrack_max: int | None
    conntrack_count: int | None
    ephemeral_lo: int | None
    ephemeral_hi: int | None
    gc_thresh3: int | None
    syn_capable: bool


# ── pure classifiers ─────────────────────────────────────────────────────────

def max_sustained_connect_rate(
    lo: int | None, hi: int | None, *, time_wait_seconds: int = TIME_WAIT_SECONDS,
) -> float | None:
    """Connections per second the local ephemeral range can sustain.

    Each connect() burns a source port held in TIME_WAIT, so the range divided
    by that hold time is the ceiling. Concurrency cannot raise it: the ports are
    gone whether one coroutine or a thousand consumed them.
    """
    if lo is None or hi is None or hi < lo or time_wait_seconds <= 0:
        return None
    return (hi - lo + 1) / time_wait_seconds


def check_ephemeral_ports(
    lo: int | None, hi: int | None, requested_rate: float,
) -> Check | None:
    ceiling = max_sustained_connect_rate(lo, hi)
    if ceiling is None:
        return None
    detail = (f"range {lo}-{hi} sustains ~{int(ceiling)} connect/sec "
              f"(requested {requested_rate:g})")
    if requested_rate > ceiling:
        return Check(
            "ephemeral", "warn", detail,
            "connect scanning will stall on EADDRNOTAVAIL — lower the rate, "
            "widen net.ipv4.ip_local_port_range, or use a SYN scan "
            "(CAP_NET_RAW), which consumes no ephemeral ports",
        )
    return Check("ephemeral", "pass", detail)


def conntrack_demand(
    rate: float, *, syn_sent_timeout: int = CONNTRACK_SYN_SENT_SECONDS,
) -> int:
    """Steady-state conntrack entries a sustained probe rate occupies."""
    return int(rate * syn_sent_timeout)


def check_conntrack(
    max_entries: int | None, count: int | None, requested_rate: float,
) -> Check | None:
    if max_entries is None:
        return None
    in_use = count or 0
    headroom = max_entries - in_use
    demand = conntrack_demand(requested_rate)
    detail = (f"table {max_entries:,} ({in_use:,} in use, {headroom:,} free); "
              f"{requested_rate:g} pps needs ~{demand:,} entries")
    if demand > headroom:
        return Check(
            "conntrack", "warn", detail,
            "the table will overflow and the kernel drops the excess SILENTLY — "
            "those ports get reported 'filtered' when they are not. Raise "
            "nf_conntrack_max, lower the rate, or bypass NAT with "
            "network_mode: host",
        )
    return Check("conntrack", "pass", detail)


def check_neighbour_table(
    gc_thresh3: int | None, host_count: int,
) -> Check | None:
    if gc_thresh3 is None:
        return None
    detail = f"gc_thresh3 {gc_thresh3}, sweeping {host_count} host(s)"
    if host_count >= gc_thresh3 * NEIGHBOUR_HEADROOM:
        return Check(
            "neighbour", "warn", detail,
            "on a flat L2 segment the ARP/neighbour table will evict live "
            "entries and drop packets silently (reported as 'filtered') — "
            "raise net.ipv4.neigh.default.gc_thresh3 above the host count",
        )
    return Check("neighbour", "pass", detail)


def check_fd_headroom(soft: int | None, concurrency: int) -> Check | None:
    if not soft:                       # 0 or None: no rlimit info (e.g. Windows)
        return None
    detail = f"soft limit {soft:,}, concurrency {concurrency}"
    if concurrency + FD_MARGIN > soft:
        return Check(
            "fd", "warn", detail,
            "concurrency crowds the descriptor limit; connects will fail with "
            "EMFILE (recorded as local_resource_error, which marks the scan "
            "degraded) — raise ulimit -n or lower concurrency",
        )
    return Check("fd", "pass", detail)


def check_syn_capability(syn_capable: bool, port_count: int,
                         platform: str | None = None) -> Check | None:
    if syn_capable:
        return Check("raw_socket", "pass", "CAP_NET_RAW available — SYN scan usable")
    if port_count < WIDE_SWEEP_PORTS:
        return None                    # narrow sweep over connect() is normal
    platform = platform if platform is not None else sys.platform
    if platform == "win32":
        # Windows will not send TCP over raw sockets at all, so there is nothing
        # to grant. The advice that fits Linux ("grant NET_RAW") is wrong here.
        return Check(
            "raw_socket", "warn",
            f"Windows has no SYN scan — a {port_count}-port sweep uses connect()",
            "one connect() per port: with Windows' SYN retry turned off (see "
            "doctor: connect_fast_fail) a few hosts' full sweep fits the job "
            "budget; for full-port sweeps of a whole subnet use a Linux agent",
        )
    if not platform.startswith("linux"):
        return Check(
            "raw_socket", "warn",
            f"no SYN scan on {platform} — a {port_count}-port sweep uses connect()",
            "raw sockets here cannot receive TCP replies; for full-port sweeps of "
            "a whole subnet use a Linux agent",
        )
    return Check(
        "raw_socket", "warn",
        f"no CAP_NET_RAW — a {port_count}-port sweep falls back to connect scan",
        "a wide sweep over connect() is bounded by the ephemeral-port ceiling "
        "and cannot complete in a useful time; grant NET_RAW and run "
        "network_mode: host, or narrow the port profile",
    )


def assess(
    limits: KernelLimits, *,
    rate: float, concurrency: int, host_count: int, port_count: int,
) -> list[Check]:
    """Every check whose input could be read, plus one note for those that could not.

    "Unread" means the LIMIT was unavailable, not that the check stayed quiet.
    check_syn_capability() deliberately says nothing about a narrow sweep over
    connect() — that is a measured non-event, and reporting it as unmeasurable
    would be a lie about what the probe knows.
    """
    checks = [
        check for check in (
            check_ephemeral_ports(limits.ephemeral_lo, limits.ephemeral_hi, rate),
            check_conntrack(limits.conntrack_max, limits.conntrack_count, rate),
            check_neighbour_table(limits.gc_thresh3, host_count),
            check_fd_headroom(limits.fd_soft, concurrency),
            check_syn_capability(limits.syn_capable, port_count),
        ) if check is not None
    ]
    unread = [
        name for name, readable in (
            ("ephemeral", limits.ephemeral_lo is not None
                          and limits.ephemeral_hi is not None),
            ("conntrack", limits.conntrack_max is not None),
            ("neighbour", limits.gc_thresh3 is not None),
            ("fd", bool(limits.fd_soft)),
            # syn_capable is a bool: always measured, never unread.
        ) if not readable
    ]
    if unread:
        checks.append(Check(
            "limits_unread", "pass",
            f"not measurable on this host: {', '.join(unread)}",
            "",
        ))
    return checks


# Ceilings whose overflow the kernel drops SILENTLY, so the scanner records
# `filtered` for a port it never really probed. These are the only checks that
# may block a job, and the line is not severity — it is whether the failure can
# speak for itself:
#
#   ephemeral / fd  surface as EADDRNOTAVAIL / EMFILE, which _ERRNO_MAP turns
#                   into local_resource_error and marks the scan degraded. The
#                   result already reports its own injury.
#   raw_socket      the connect() fallback is slow, not wrong, and the
#                   feasibility floor already refuses what cannot finish.
#   neighbour       silent, but the arithmetic holds only on a FLAT L2 segment.
#                   The probe cannot see its targets' topology, so a wide sweep
#                   across routed subnets never touches gc_thresh3 and blocking
#                   it would be a false refusal. Warning is the honest response
#                   to a hazard we cannot confirm.
#
# conntrack is the one that is both silent and unconditional: under NAT every
# probe takes an entry, whatever the topology beyond the first hop.
BLOCKING_CHECKS = ("conntrack",)


def blocking_checks(checks: list[Check]) -> list[Check]:
    """The subset of `checks` that must refuse a job rather than warn about it."""
    return [c for c in checks
            if c.name in BLOCKING_CHECKS and c.status != "pass"]


def as_run_stats(checks: list[Check]) -> dict:
    """The ceilings this scan ran under, as JSON for the job result.

    `gate_measured` is False when a blocking ceiling could not be read (no /proc,
    no netfilter): the refusal gate then ran blind, which is a different
    statement from "the ceilings are fine".
    """
    present = {c.name for c in checks}
    return {
        "gate_measured": all(name in present for name in BLOCKING_CHECKS),
        "warnings": sum(1 for c in checks if c.status != "pass"),
        "blocking": [c.name for c in blocking_checks(checks)],
        "checks": [{"name": c.name, "status": c.status, "detail": c.detail}
                   for c in checks],
    }


def format_preflight(checks: list[Check]) -> str:
    """Same rendering as `doctor`, so an operator reads one format everywhere."""
    return format_report(checks)


def describe_capability(limits: KernelLimits) -> str:
    """One line stating what this HOST can sustain, independent of any job.

    Logged at startup beside the capability and use-case lines. A job-specific
    verdict needs the envelope (see assess()); this is the standing fact, and it
    is what turns "the scan reported everything filtered" into a five-second
    diagnosis instead of an afternoon.
    """
    fd = f"{limits.fd_soft:,}" if limits.fd_soft else "n/a"

    ceiling = max_sustained_connect_rate(limits.ephemeral_lo, limits.ephemeral_hi)
    ephemeral = (
        f"{limits.ephemeral_lo}-{limits.ephemeral_hi} (~{int(ceiling)} connect/sec)"
        if ceiling is not None else "n/a"
    )

    if limits.conntrack_max is None:
        conntrack = "n/a"
    else:
        in_use = limits.conntrack_count
        used = f", {in_use:,} in use" if in_use is not None else ""
        conntrack = f"{limits.conntrack_max:,}{used}"

    neigh = f"{limits.gc_thresh3:,}" if limits.gc_thresh3 is not None else "n/a"

    return (
        f"Host scan ceilings: fd {fd} | ephemeral {ephemeral} | "
        f"conntrack {conntrack} | neigh gc_thresh3 {neigh} | "
        f"SYN scan: {'yes' if limits.syn_capable else 'no'}"
    )


# ── IO wiring ────────────────────────────────────────────────────────────────

def read_int(path) -> int | None:
    """One integer from a sysctl file, or None when absent/unparseable."""
    try:
        return int(Path(path).read_text().strip())
    except (OSError, ValueError):
        return None


def read_port_range(path) -> tuple[int | None, int | None]:
    """ip_local_port_range is two whitespace-separated integers."""
    try:
        parts = Path(path).read_text().split()
        if len(parts) != 2:
            return (None, None)
        return (int(parts[0]), int(parts[1]))
    except (OSError, ValueError):
        return (None, None)


def probe_limits() -> KernelLimits:
    """Read every ceiling this host exposes. Never raises: unknown stays None."""
    fd_soft = fd_hard = None
    try:
        from scanner.scanner_base import get_fd_limit
        fd_soft, fd_hard = get_fd_limit()
    except Exception:                  # noqa: BLE001 — a missing limit is not an error
        pass

    syn_capable = False
    try:
        from scanner.syn_scanner import syn_scan_supported
        syn_capable = bool(syn_scan_supported())
    except Exception:                  # noqa: BLE001
        pass

    lo, hi = read_port_range(_PORT_RANGE)
    return KernelLimits(
        fd_soft=fd_soft,
        fd_hard=fd_hard,
        conntrack_max=read_int(_CONNTRACK_MAX),
        conntrack_count=read_int(_CONNTRACK_COUNT),
        ephemeral_lo=lo,
        ephemeral_hi=hi,
        gc_thresh3=read_int(_GC_THRESH3),
        syn_capable=syn_capable,
    )


def preflight_report(
    *, rate: float, concurrency: int, host_count: int, port_count: int,
) -> tuple[list[Check], KernelLimits]:
    """Read the host's ceilings and judge them against one scan envelope."""
    limits = probe_limits()
    return assess(limits, rate=rate, concurrency=concurrency,
                  host_count=host_count, port_count=port_count), limits


def env_int(name: str, default: int) -> int:
    """Small helper so callers can express an envelope from the environment."""
    try:
        return int(os.environ.get(name, "") or default)
    except ValueError:
        return default

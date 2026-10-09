"""doctor.py — real self-diagnosis: pass / warn / fail with a remediation string.

Fixes the two review defects: the `or True` false-positive, and a `doctor` that
promised reachability but never contacted the Manager. The classifiers are pure
and unit-tested; `run()` wires the real IO (DNS/TCP/TLS/cert, clock, disk,
interfaces) and calls them.
"""
from __future__ import annotations

import shutil
import socket
import ssl
import sys
from dataclasses import dataclass
from urllib.parse import urlparse

_CLOCK_WARN_S = 60
_CLOCK_FAIL_S = 300
_DISK_MIN_BYTES = 500 * 1024 * 1024


@dataclass
class Check:
    name: str
    status: str          # "pass" | "warn" | "fail"
    detail: str
    remediation: str = ""


def check_python(version_info) -> Check:
    ok = tuple(version_info[:2]) >= (3, 8)
    return Check("python", "pass" if ok else "fail",
                 f"{version_info[0]}.{version_info[1]}",
                 "" if ok else "install Python 3.8+ and re-run")


def check_clock(offset_s: float, warn: int = _CLOCK_WARN_S, fail: int = _CLOCK_FAIL_S) -> Check:
    a = abs(offset_s)
    if a > fail:
        return Check("clock", "fail", f"offset {offset_s:.0f}s vs manager",
                     "fix NTP — clock skew breaks TLS handshakes and enrollment tokens")
    if a > warn:
        return Check("clock", "warn", f"offset {offset_s:.0f}s vs manager",
                     "consider syncing NTP")
    return Check("clock", "pass", f"offset {offset_s:.0f}s vs manager")


def check_disk(free_bytes: int, min_bytes: int = _DISK_MIN_BYTES) -> Check:
    ok = free_bytes >= min_bytes
    return Check("disk", "pass" if ok else "fail",
                 f"{free_bytes // (1024 * 1024)} MiB free for the result queue",
                 "" if ok else "free disk — the result queue needs headroom")


def classify_connectivity(dns_ok: bool, tcp_ok: bool, tls_ok: bool, cert_ok: bool) -> Check:
    if not dns_ok:
        return Check("manager", "fail", "DNS resolution of the manager host failed",
                     "check DNS and the manager hostname")
    if not tcp_ok:
        return Check("manager", "fail", "TCP connect to the manager failed",
                     "check firewall / egress to the manager port")
    if not tls_ok:
        return Check("manager", "fail", "TLS handshake failed",
                     "check TLS version / proxy; a WS-incapable proxy needs long-poll")
    if not cert_ok:
        return Check("manager", "fail", "certificate chain validation failed",
                     "install the CA bundle (PROBE_CA_BUNDLE) or fix the certificate")
    return Check("manager", "pass", "dns + tcp + tls + cert ok")


def check_privilege(is_privileged: bool) -> Check:
    if is_privileged:
        return Check("privilege", "pass", "running privileged")
    return Check("privilege", "warn",
                 "unprivileged — SYN / OS-fingerprint fall back to connect-scan",
                 "run with sudo/admin only if you need raw-socket depth")


def check_connect_fast_fail(result: dict | None) -> Check | None:
    """Windows only: does a closed port report at network speed?

    Windows re-sends the SYN after an RST unless the scan socket opts out
    (scanner/win_fast_connect.py). If the opt-out did not take, every closed
    port costs ~2 s and connect scans read closed ports as filtered.
    """
    if result is None:
        return None
    fast, default = result.get("fast_fail_s"), result.get("default_s")
    seen = (f"closed port reports in {fast:.3f}s" if fast is not None
            else "closed-port timing could not be measured")
    if default is not None:
        seen += f" (Windows default {default:.1f}s)"
    if result.get("effective"):
        return Check("connect_fast_fail", "pass", seen)
    return Check("connect_fast_fail", "warn", seen,
                 "port scans from this agent will be slow and may report closed "
                 "ports as filtered; use Windows 10 1709 or later, or run full-port "
                 "sweeps from a Linux agent")


def exit_code(checks: list[Check]) -> int:
    return 1 if any(c.status == "fail" for c in checks) else 0


def format_report(checks: list[Check]) -> str:
    mark = {"pass": "ok  ", "warn": "warn", "fail": "FAIL"}
    lines = []
    for c in checks:
        line = f"[{mark.get(c.status, '?')}] {c.name:<12} {c.detail}"
        if c.remediation and c.status != "pass":
            line += f"\n              → {c.remediation}"
        lines.append(line)
    return "\n".join(lines)


# ── IO wiring (not unit-tested; exercised by the CI smoke) ───────────────────
def _measure_manager(url: str, timeout: float = 5.0) -> tuple[bool, bool, bool, bool]:
    dns_ok = tcp_ok = tls_ok = cert_ok = False
    try:
        u = urlparse(url)
        host = u.hostname or ""
        port = u.port or (443 if u.scheme == "https" else 80)
        dns_ok = bool(socket.getaddrinfo(host, port, proto=socket.IPPROTO_TCP))
        with socket.create_connection((host, port), timeout=timeout) as sock:
            tcp_ok = True
            if u.scheme == "https":
                ctx = ssl.create_default_context()
                with ctx.wrap_socket(sock, server_hostname=host) as ss:
                    tls_ok = True
                    cert_ok = bool(ss.getpeercert())
            else:
                tls_ok = cert_ok = True  # not applicable over http
    except Exception:
        pass
    return dns_ok, tcp_ok, tls_ok, cert_ok


def _offset_from_date_header(date_header: str | None, now_epoch: float) -> float | None:
    """Pure: server clock offset (seconds) from an HTTP Date header vs local now."""
    if not date_header:
        return None
    import email.utils
    try:
        server = email.utils.parsedate_to_datetime(date_header).timestamp()
    except (TypeError, ValueError, OverflowError):
        return None
    return server - now_epoch


def _server_date_offset(url: str, timeout: float = 5.0) -> float | None:
    import time as _t
    import urllib.request
    for req in (urllib.request.Request(url, method="HEAD"), url):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:  # noqa: S310
                return _offset_from_date_header(resp.headers.get("Date"), _t.time())
        except Exception:
            continue
    return None


def run(manager_url: str, is_privileged: bool, state_dir: str = ".") -> list[Check]:
    checks = [check_python(sys.version_info), check_privilege(is_privileged)]
    try:
        from scanner import win_fast_connect
        fast_fail = check_connect_fast_fail(
            win_fast_connect.self_check(include_default=True))
    except Exception:  # noqa: BLE001 — a diagnostic must never break doctor
        fast_fail = None
    if fast_fail is not None:
        checks.append(fast_fail)
    try:
        free = shutil.disk_usage(state_dir).free
        checks.append(check_disk(free))
    except OSError:
        checks.append(Check("disk", "warn", "could not stat the state dir"))
    if manager_url:
        checks.append(classify_connectivity(*_measure_manager(manager_url)))
        offset = _server_date_offset(manager_url)
        if offset is not None:
            checks.append(check_clock(offset))
        else:
            checks.append(Check("clock", "warn", "clock offset vs manager not measured",
                                "needs a reachable manager to check skew"))
    else:
        checks.append(Check("manager", "warn", "no manager URL configured",
                            "run `connect --manager <url>` or set PLATFORM_URL"))
    return checks

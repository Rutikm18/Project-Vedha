"""diagnostics.py — `vedha-agent doctor | status | support-bundle`: a client can
find out what is wrong, and tell us, without us on the phone.

Design rules:
  * explain, never change: nothing here edits the client's firewall, proxy,
    Defender or certificate settings. A check says what it saw and the exact fix;
    the client (or their IT) applies it;
  * read-only with respect to the agent's identity: these commands never open the
    state file's secrets for output and never refresh a credential (two processes
    rotating one device token would lock the real agent out);
  * the support bundle holds no secrets by construction: it contains only files
    this module builds, every text passes through `redact_text`, and the identity
    file, keys and scan results are never read into it.

Pure functions (classification, redaction, formatting) are unit-tested; the socket
work is thin and exercised against local servers in the tests.
"""
from __future__ import annotations

import json
import os
import platform
import re
import shutil
import socket
import ssl
import sys
import tempfile
import time
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping
from urllib.parse import urlparse

from agent import doctor, runtime_status
from agent.doctor import Check
from agent.version import AGENT_VERSION

HEALTH_PATH = "/health"
LOG_TAIL_LINES = 2000
LOG_TAIL_BYTES = 2_000_000
BUNDLE_MAX_LOG_FILES = 3


# ── where things live ────────────────────────────────────────────────────────

def default_env_file(environ: Mapping[str, str] | None = None, os_name: str | None = None) -> Path | None:
    """The configuration file the installer writes. VEDHA_AGENT_ENV overrides; on
    Windows it is %ProgramData%\\vedha-agent\\agent.env; elsewhere there is none."""
    environ = os.environ if environ is None else environ
    explicit = environ.get("VEDHA_AGENT_ENV", "").strip()
    if explicit:
        return Path(explicit)
    if (os_name or os.name) == "nt":
        base = environ.get("ProgramData") or environ.get("PROGRAMDATA")
        if base:
            return Path(base) / "vedha-agent" / "agent.env"
    return None


def parse_env_text(text: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in text.lstrip("﻿").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, _, value = line.partition("=")
            values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def load_env_file(path: Path | None, environ: dict[str, str] | None = None) -> bool:
    """Load KEY=VALUE lines into the environment WITHOUT overriding what is already
    set (an explicit variable always wins). Tolerates a UTF-8 byte-order mark."""
    environ = os.environ if environ is None else environ
    if path is None:
        return False
    try:
        values = parse_env_text(path.read_text(encoding="utf-8-sig"))
    except OSError:
        return False
    for key, value in values.items():
        environ.setdefault(key, value)
    return True


@dataclass
class Paths:
    state_file: Path
    status_file: Path
    log_file: Path
    env_file: Path | None


def resolve_paths(environ: Mapping[str, str] | None = None) -> Paths:
    environ = os.environ if environ is None else environ
    state_file = Path(environ.get("STATE_FILE") or "/var/lib/vedha-agent/state.json")
    status_file = Path(environ.get("PROBE_STATUS_FILE") or runtime_status.path_for(state_file))
    log_file = Path(environ.get("PROBE_LOG_FILE") or state_file.with_name("logs") / "agent.log")
    return Paths(state_file, status_file, log_file, default_env_file(environ))


# ── redaction ────────────────────────────────────────────────────────────────

_SENSITIVE_KEY = re.compile(r"token|secret|passw|passwd|pat\b|_pat|key|authorization|credential|licen[sc]e|cookie", re.I)
_REDACTIONS: tuple[tuple[re.Pattern, str], ...] = (
    (re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----.*?-----END [A-Z0-9 ]*PRIVATE KEY-----", re.S), "[private key removed]"),
    (re.compile(r"\bvet_[A-Za-z0-9_\-]{6,}"), "vet_[removed]"),
    (re.compile(r"\bvpat_[A-Za-z0-9_\-]{6,}"), "vpat_[removed]"),
    (re.compile(r"\beyJ[A-Za-z0-9_\-]{8,}\.[A-Za-z0-9_\-]{8,}\.[A-Za-z0-9_\-]{4,}"), "[jwt removed]"),
    (re.compile(r"(?i)\b(bearer|basic)\s+[A-Za-z0-9._~+/=\-]{8,}"), r"\1 [removed]"),
    (re.compile(r"(?i)(://)[^/\s:@]+:[^/\s@]+@"), r"\1[user]:[removed]@"),
    # NAME=value / "name": "value" where the name CONTAINS a sensitive word, so prefixed
    # names such as PROBE_ENROLL_TOKEN or device_secret are caught too.
    (re.compile(r"(?i)([A-Za-z0-9_\-]*(?:token|secret|passw(?:or)?d|api[_-]?key|authorization))(\"?\s*[=:]\s*\"?)[^\s\"',;&]{3,}"),
     r"\1\2[removed]"),
)
_IPV4 = re.compile(r"\b(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})\b")


def redact_text(text: str, *, mask_ips: bool = False) -> str:
    """Remove credentials from free text. Conservative: it prefers hiding too much.
    It recognises credentials by their shape (vet_…, JWTs, Bearer headers, private keys,
    user:password@ URLs) or by a label (token=…, password: …). A bare password with no
    label or recognisable shape cannot be identified, which is why the support bundle
    also never includes the files that hold secrets."""
    for pattern, replacement in _REDACTIONS:
        text = pattern.sub(replacement, text)
    if mask_ips:
        text = _IPV4.sub(lambda m: f"{m.group(1)}.{m.group(2)}.{m.group(3)}.x", text)
    return text


def redact_env(values: Mapping[str, str]) -> dict[str, str]:
    return {k: ("[removed]" if _SENSITIVE_KEY.search(k) else redact_text(v)) for k, v in values.items()}


def read_tail(path: Path, max_lines: int = LOG_TAIL_LINES, max_bytes: int = LOG_TAIL_BYTES) -> list[str]:
    try:
        size = path.stat().st_size
        with path.open("rb") as handle:
            if size > max_bytes:
                handle.seek(size - max_bytes)
            data = handle.read()
    except OSError:
        return []
    return data.decode("utf-8", "replace").splitlines()[-max_lines:]


# ── manager reachability, stage by stage ─────────────────────────────────────

@dataclass
class ManagerProbe:
    url: str
    host: str = ""
    port: int = 0
    via_proxy: str = ""
    dns_ok: bool = False
    dns_error: str = ""
    proxy_status: int = 0           # HTTP status of the proxy's answer to CONNECT (0 = not used / no answer)
    tcp_ok: bool = False
    tcp_error: str = ""
    tls_ok: bool = False
    tls_error: str = ""
    cert_issuer: str = ""           # who signed the certificate we were shown (even if untrusted)
    http_status: int = 0
    http_error: str = ""
    clock_offset_s: float | None = None
    https: bool = True


def _proxy_for(url: str, environ: Mapping[str, str]) -> str:
    scheme = urlparse(url).scheme
    names = ("HTTPS_PROXY", "https_proxy", "ALL_PROXY", "all_proxy") if scheme == "https" else \
            ("HTTP_PROXY", "http_proxy", "ALL_PROXY", "all_proxy")
    for name in names:
        if environ.get(name):
            return environ[name]
    return ""


def _no_proxy_matches(host: str, environ: Mapping[str, str]) -> bool:
    patterns = [p.strip().lower().lstrip(".") for p in (environ.get("NO_PROXY") or environ.get("no_proxy") or "").split(",") if p.strip()]
    host = host.lower()
    return any(p == "*" or host == p or host.endswith("." + p) for p in patterns)


def _issuer_of(sock_der: bytes) -> str:
    try:
        from cryptography import x509
        return x509.load_der_x509_certificate(sock_der).issuer.rfc4514_string()[:200]
    except Exception:  # noqa: BLE001 — informational only
        return ""


def _read_http_response(stream: Any, limit: int = 65536) -> tuple[int, dict[str, str]]:
    data = b""
    while b"\r\n\r\n" not in data and len(data) < limit:
        chunk = stream.recv(4096)
        if not chunk:
            break
        data += chunk
    head = data.split(b"\r\n\r\n", 1)[0].decode("latin-1", "replace").split("\r\n")
    try:
        status = int(head[0].split()[1])
    except (IndexError, ValueError):
        return 0, {}
    headers = {}
    for line in head[1:]:
        name, _, value = line.partition(":")
        headers[name.strip().lower()] = value.strip()
    return status, headers


def probe_manager(url: str, *, environ: Mapping[str, str] | None = None, timeout: float = 6.0) -> ManagerProbe:
    """Walk DNS → (proxy) → TCP → TLS → HTTP and record where it stops and why.
    Honours HTTPS_PROXY / NO_PROXY and PROBE_CA_BUNDLE exactly as the agent does,
    so a client behind a proxy is not told their working setup is broken."""
    environ = os.environ if environ is None else environ
    parsed = urlparse(url)
    result = ManagerProbe(url=url, host=parsed.hostname or "", https=parsed.scheme == "https")
    result.port = parsed.port or (443 if result.https else 80)
    if not result.host:
        result.dns_error = "the manager address has no host name"
        return result

    proxy = "" if _no_proxy_matches(result.host, environ) else _proxy_for(url, environ)
    result.via_proxy = proxy
    target_host, target_port = result.host, result.port
    if proxy:
        pp = urlparse(proxy if "://" in proxy else "http://" + proxy)
        target_host, target_port = pp.hostname or "", pp.port or 3128

    try:
        socket.getaddrinfo(target_host, target_port, proto=socket.IPPROTO_TCP)
        result.dns_ok = True
    except OSError as exc:
        result.dns_error = str(exc)[:200]
        return result

    try:
        sock = socket.create_connection((target_host, target_port), timeout=timeout)
    except OSError as exc:
        result.tcp_error = str(exc)[:200]
        return result
    try:
        if proxy and result.https:
            sock.sendall(f"CONNECT {result.host}:{result.port} HTTP/1.1\r\nHost: {result.host}:{result.port}\r\n\r\n".encode())
            result.proxy_status, _ = _read_http_response(sock)
            if result.proxy_status != 200:
                result.tcp_error = f"the proxy answered HTTP {result.proxy_status or 'nothing'} to CONNECT"
                return result
        result.tcp_ok = True

        stream: Any = sock
        if result.https:
            bundle = environ.get("PROBE_CA_BUNDLE") or environ.get("SSL_CERT_FILE") or ""
            verify = environ.get("VERIFY_TLS", "true").lower() not in ("false", "0", "no")
            try:
                ctx = ssl.create_default_context(cafile=bundle) if bundle and Path(bundle).is_file() else ssl.create_default_context()
                if not verify:
                    ctx.check_hostname = False
                    ctx.verify_mode = ssl.CERT_NONE
                stream = ctx.wrap_socket(sock, server_hostname=result.host)
                result.tls_ok = True
            except ssl.SSLCertVerificationError as exc:
                result.tls_error = str(exc)[:250]
                result.cert_issuer = _untrusted_issuer(result, target_host, target_port, proxy, timeout)
                return result
            except (ssl.SSLError, OSError) as exc:
                result.tls_error = str(exc)[:250]
                return result
        else:
            result.tls_ok = True

        request = f"GET {HEALTH_PATH} HTTP/1.1\r\nHost: {result.host}\r\nConnection: close\r\nUser-Agent: vedha-agent-doctor\r\n\r\n"
        if proxy and not result.https:
            request = f"GET {url.rstrip('/')}{HEALTH_PATH} HTTP/1.1\r\nHost: {result.host}\r\nConnection: close\r\n\r\n"
        stream.sendall(request.encode())
        result.http_status, headers = _read_http_response(stream)
        if not result.http_status:
            result.http_error = "no valid HTTP answer"
        date = headers.get("date")
        if date:
            result.clock_offset_s = doctor._offset_from_date_header(date, time.time())
    except OSError as exc:
        if not result.tcp_ok:
            result.tcp_error = str(exc)[:200]
        else:
            result.http_error = str(exc)[:200]
    finally:
        try:
            sock.close()
        except OSError:
            pass
    return result


def _untrusted_issuer(result: ManagerProbe, host: str, port: int, proxy: str, timeout: float) -> str:
    """The certificate was refused. Look at it anyway (without trusting it) so we can
    name who signed it — a corporate TLS-inspection CA names itself."""
    try:
        sock = socket.create_connection((host, port), timeout=timeout)
        try:
            if proxy:
                sock.sendall(f"CONNECT {result.host}:{result.port} HTTP/1.1\r\nHost: {result.host}:{result.port}\r\n\r\n".encode())
                status, _ = _read_http_response(sock)
                if status != 200:
                    return ""
            ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            with ctx.wrap_socket(sock, server_hostname=result.host) as tls:
                der = tls.getpeercert(binary_form=True)
            return _issuer_of(der) if der else ""
        finally:
            try:
                sock.close()
            except OSError:
                pass
    except OSError:
        return ""


def classify_probe(probe: ManagerProbe) -> list[Check]:
    """Turn what the probe saw into a plain-language finding and the exact fix."""
    where = f"{probe.host}:{probe.port}"
    proxy_note = f" (through the proxy {probe.via_proxy})" if probe.via_proxy else ""
    if not probe.dns_ok:
        what = "the proxy's address" if probe.via_proxy else probe.host
        return [Check("manager", "fail", f"cannot look up {what} in DNS ({probe.dns_error})",
                      "check this computer's DNS settings; try `nslookup " + (probe.host or "<manager>") +
                      "`. On a split-DNS or VPN network, use a DNS server that can resolve the manager name.")]
    if not probe.tcp_ok:
        if probe.proxy_status in (407,):
            return [Check("manager", "fail", "the proxy requires a login (HTTP 407)",
                          "ask IT to exempt this computer from proxy authentication, or allow it to reach " + where)]
        if probe.proxy_status == 403:
            return [Check("manager", "fail", "the proxy refused the connection (HTTP 403)",
                          f"ask IT to allow {probe.host} through the proxy")]
        error = (probe.tcp_error or "").lower()
        proxy_hint = ", or install with -Proxy http://proxy:port if a proxy is required." if not probe.via_proxy else "."
        if "refused" in error or "10061" in error:
            # Something answered and said no: a wrong address/port, or a firewall that rejects.
            fix = ("the address answered but nothing accepted the connection. Check the manager address is right (" + where +
                   "). If it is, ask IT whether a firewall rejects outbound TCP " + str(probe.port) + proxy_hint)
        elif "timed out" in error or "10060" in error:
            fix = ("no answer came back, which usually means a firewall is silently dropping outbound TCP " + str(probe.port) +
                   ". Ask IT to allow this computer to reach " + where + proxy_hint)
        else:
            fix = ("the network path to the manager is not open. Ask IT to allow this computer to reach " + where + proxy_hint)
        return [Check("manager", "fail", f"cannot connect to {where}{proxy_note}: {probe.tcp_error}", fix)]
    if probe.https and not probe.tls_ok:
        err = probe.tls_error.lower()
        if "certificate" in err or "verify" in err or probe.cert_issuer:
            issuer = f" It was signed by: {probe.cert_issuer}." if probe.cert_issuer else ""
            return [Check("manager", "fail",
                          f"the manager's TLS certificate is not trusted by this computer.{issuer}",
                          "This usually means a security gateway is inspecting HTTPS traffic. Ask IT to exempt " + probe.host +
                          " from TLS inspection (preferred), or reinstall with -CaBundle <path to your company's root certificate .pem>.")]
        return [Check("manager", "fail", f"the secure (TLS) handshake with {where} failed: {probe.tls_error}",
                      "a proxy or firewall may be interfering with HTTPS. Ask IT to allow " + probe.host + " without inspection.")]
    if probe.http_status == 0:
        return [Check("manager", "fail", f"connected to {where}, but no valid answer came back ({probe.http_error or 'empty reply'})",
                      "a proxy or filter may be answering instead of the manager. Open " + probe.url.rstrip('/') + HEALTH_PATH + " in a browser on this computer and send us what it shows.")]
    if probe.http_status >= 500:
        return [Check("manager", "warn", f"the manager answered HTTP {probe.http_status} (a problem on the manager's side)",
                      "try again in a few minutes; if it persists contact Vedha support")]
    if probe.http_status in (403, 407):
        return [Check("manager", "fail", f"something between this computer and the manager answered HTTP {probe.http_status}",
                      "a web filter or proxy is blocking " + probe.host + ". Ask IT to allow it (it may be classified as a new or uncategorised site).")]
    return [Check("manager", "pass", f"{where} reachable{proxy_note}; secure connection ok; manager answered HTTP {probe.http_status}")]


# ── status ───────────────────────────────────────────────────────────────────

def _state_flags(state_file: Path) -> dict[str, bool]:
    """What the identity file says, as booleans only. Secret values never leave this function."""
    try:
        data = json.loads(state_file.read_text(encoding="utf-8-sig"))
    except (OSError, ValueError):
        return {"state_file_present": state_file.exists(), "enrolled": False}
    return {"state_file_present": True, "enrolled": bool(isinstance(data, dict) and data.get("agent_id"))}


def collect_status(environ: Mapping[str, str] | None = None, *, now: float | None = None,
                   alive: Callable[[Any], bool] = runtime_status.process_alive) -> dict[str, Any]:
    environ = os.environ if environ is None else environ
    paths = resolve_paths(environ)
    info = runtime_status.effective(runtime_status.read(paths.status_file), now=now, alive=alive)
    info.update(_state_flags(paths.state_file))
    info.update(
        agent_version=AGENT_VERSION,
        manager=environ.get("PLATFORM_URL", "") or info.get("manager", ""),
        scope=environ.get("PROBE_NETWORK_SEGMENTS", ""),
        log_file=str(paths.log_file),
        platform=sys.platform,
    )
    info.pop("pid", None)
    return info


_STATE_TEXT = {
    "starting": "Starting up",
    "enrolling": "Registering with the manager",
    "awaiting-approval": "Waiting for a person to approve this agent in Fleet",
    "online": "ONLINE - registered with the manager and waiting for scan jobs",
    "retrying": "Cannot reach the manager yet - still trying",
    "failed": "STOPPED - the agent gave up",
    "not-running": "NOT RUNNING",
}


def format_status(info: Mapping[str, Any]) -> str:
    state = str(info.get("state", "not-running"))
    lines = [f"Vedha agent {info.get('agent_version', '')} on {info.get('platform', '')}",
             f"  Status   : {_STATE_TEXT.get(state, state)}"]
    if info.get("detail"):
        lines.append(f"  Detail   : {info['detail']}")
    if state == "awaiting-approval" and info.get("pairing_code"):
        lines.append(f"  Approve  : open {info.get('pairing_url') or 'Fleet'} and enter code {info['pairing_code']}")
    if info.get("reason"):
        lines.append(f"  Why      : {info['reason']}")
    if info.get("remediation"):
        lines.append(f"  Fix      : {info['remediation']}")
    lines.append(f"  Enrolled : {'yes' if info.get('enrolled') else 'no'}")
    if info.get("manager"):
        lines.append(f"  Manager  : {info['manager']}")
    if info.get("scope"):
        lines.append(f"  Scope    : {info['scope']}")
    elif state != "not-running":
        lines.append("  Scope    : (none set locally - the manager will not send jobs until one is configured)")
    if "age_seconds" in info and state != "not-running":
        lines.append(f"  Updated  : {info['age_seconds']} s ago")
    lines.append(f"  Log      : {info.get('log_file', '')}")
    return "\n".join(lines)


# ── doctor ───────────────────────────────────────────────────────────────────

def _writable(directory: Path) -> tuple[bool, str]:
    try:
        directory.mkdir(parents=True, exist_ok=True)
        fd, name = tempfile.mkstemp(dir=directory, prefix=".vedha-write-test")
        os.close(fd)
        os.unlink(name)
        return True, ""
    except OSError as exc:
        return False, str(exc)[:160]


def local_checks(environ: Mapping[str, str], status: Mapping[str, Any]) -> list[Check]:
    checks: list[Check] = []
    paths = resolve_paths(environ)
    ok, why = _writable(paths.state_file.parent)
    checks.append(Check("data-folder", "pass" if ok else "fail",
                        f"{paths.state_file.parent} is writable" if ok else f"cannot write to {paths.state_file.parent} ({why})",
                        "" if ok else "run this command from an elevated (Administrator) prompt, or repair the folder's permissions"))
    state = status.get("state")
    if state == "not-running":
        start = ("start it with: Start-ScheduledTask -TaskName VedhaAgent   (or re-run install.cmd -Repair)"
                 if sys.platform.startswith("win") else
                 "start it again (for a container: docker start vedha-agent)")
        checks.append(Check("agent", "fail", str(status.get("detail") or "the agent is not running"), start))
    elif state == "failed":
        checks.append(Check("agent", "fail", str(status.get("reason") or "the agent stopped"), str(status.get("remediation") or "")))
    elif state == "awaiting-approval":
        checks.append(Check("agent", "warn", "waiting for approval in Fleet",
                            f"enter code {status.get('pairing_code', '')} at {status.get('pairing_url') or 'Fleet'}"))
    elif state == "retrying":
        checks.append(Check("agent", "warn", str(status.get("reason") or "cannot reach the manager yet"), str(status.get("remediation") or "")))
    else:
        checks.append(Check("agent", "pass", f"state: {state}"))
    if environ.get("PROBE_ENROLL_TOKEN") and status.get("enrolled"):
        checks.append(Check("install-token", "warn", "an install token is still stored in the configuration file after enrolment",
                            "it is single-use and harmless once used; re-run the installer with -Repair to remove it"))
    if not environ.get("PROBE_NETWORK_SEGMENTS"):
        checks.append(Check("scope", "warn", "no local scan scope is configured, so the manager will send no jobs",
                            "re-run the installer with -Scope <network in CIDR form>, for example -Scope 192.168.1.0/24"))
    return checks


def run_doctor(environ: Mapping[str, str] | None = None, *, preinstall: bool = False) -> list[Check]:
    """All checks. `preinstall` runs only the environment and network ones, for use
    before the agent is installed (there is no agent, data folder or scope to check yet)."""
    environ = os.environ if environ is None else environ
    status = collect_status(environ)
    checks = [doctor.check_python(sys.version_info), doctor.check_privilege(_is_admin())]
    paths = resolve_paths(environ)
    try:
        checks.append(doctor.check_disk(shutil.disk_usage(paths.state_file.parent if paths.state_file.parent.exists() else Path(".")).free))
    except OSError:
        checks.append(Check("disk", "warn", "could not measure free disk space"))
    url = environ.get("PLATFORM_URL", "")
    if url:
        probe = probe_manager(url, environ=environ)
        checks.extend(classify_probe(probe))
        if probe.clock_offset_s is not None:
            checks.append(doctor.check_clock(probe.clock_offset_s))
    else:
        checks.append(Check("manager", "fail", "no manager address is configured",
                            "re-run the installer with -Manager https://<your manager>"))
    if not preinstall:
        checks.extend(local_checks(environ, status))
    return checks


def _is_admin() -> bool:
    try:
        if os.name == "nt":
            import ctypes
            return bool(ctypes.windll.shell32.IsUserAnAdmin())  # type: ignore[attr-defined]
        return os.geteuid() == 0  # type: ignore[attr-defined]
    except Exception:  # noqa: BLE001
        return False


def summarise(checks: Iterable[Check]) -> str:
    checks = list(checks)
    failed = [c for c in checks if c.status == "fail"]
    warned = [c for c in checks if c.status == "warn"]
    if failed:
        first = failed[0]
        return f"RESULT: {len(failed)} problem(s) found. Start with: {first.name} - {first.remediation or first.detail}"
    if warned:
        return f"RESULT: working, with {len(warned)} warning(s) to review."
    return "RESULT: everything checked is healthy."


def format_doctor(checks: list[Check]) -> str:
    return doctor.format_report(checks) + "\n\n" + summarise(checks)


# ── support bundle ───────────────────────────────────────────────────────────

_BUNDLE_README = """Vedha agent support bundle
==========================
Created : {when}
Agent   : {version} on {platform}

What is inside
  doctor.txt          connectivity and health checks (what is wrong, and the suggested fix)
  status.json         what the agent reports it is doing (no credentials)
  system.txt          agent version, operating system, architecture, Python runtime
  configuration.txt   the agent's settings with every secret removed
  agent.log           the most recent agent log lines, with credentials removed
  install-*.log       the most recent installer logs, with credentials removed

What is NOT inside
  the agent's identity file, private keys, install tokens, scan results.

Please review before sending: logs contain host names and IP addresses from your network{ips}.
Email this file to your Vedha contact. Nothing was sent automatically.
"""


def build_support_bundle(out_path: Path | str | None = None, *, environ: Mapping[str, str] | None = None,
                         mask_ips: bool = False, now: float | None = None) -> Path:
    environ = os.environ if environ is None else environ
    paths = resolve_paths(environ)
    stamp = time.strftime("%Y%m%d-%H%M%S", time.localtime(now if now is not None else time.time()))
    host = re.sub(r"[^A-Za-z0-9_.-]", "_", platform.node() or "host")
    target = Path(out_path) if out_path else Path.cwd() / f"vedha-support-{host}-{stamp}.zip"
    if target.is_dir():
        target = target / f"vedha-support-{host}-{stamp}.zip"

    def clean(text: str) -> str:
        return redact_text(text, mask_ips=mask_ips)

    checks = run_doctor(environ)
    status = collect_status(environ, now=now)
    env_values = {}
    if paths.env_file:
        try:
            env_values = parse_env_text(paths.env_file.read_text(encoding="utf-8-sig"))
        except OSError:
            env_values = {}
    config_lines = [f"{k}={v}" for k, v in sorted(redact_env({**env_values, **{
        k: v for k, v in environ.items() if k.startswith(("PROBE_", "PLATFORM_", "VERIFY_", "STATE_", "HTTPS_PROXY", "NO_PROXY", "LICENSE_"))
    }}).items())]

    members: dict[str, str] = {
        "README.txt": _BUNDLE_README.format(when=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now if now is not None else time.time())),
                                            version=AGENT_VERSION, platform=sys.platform,
                                            ips=" (masked in this bundle)" if mask_ips else ""),
        "doctor.txt": clean(format_doctor(checks)),
        "status.json": clean(json.dumps(status, indent=2, default=str)),
        "system.txt": clean("\n".join([
            f"agent_version={AGENT_VERSION}", f"platform={sys.platform}", f"os={platform.platform()}",
            f"machine={platform.machine()}", f"python={platform.python_version()}",
            f"admin={_is_admin()}", f"time_utc={time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(now if now is not None else time.time()))}"])),
        "configuration.txt": clean("\n".join(config_lines)),
    }
    log_text = "\n".join(read_tail(paths.log_file))
    if log_text:
        members["agent.log"] = clean(log_text)
    logs_dir = paths.log_file.parent
    try:
        installs = sorted(logs_dir.glob("install-*.log"), key=lambda p: p.stat().st_mtime, reverse=True)[:BUNDLE_MAX_LOG_FILES]
    except OSError:
        installs = []
    for item in installs:
        members[item.name] = clean("\n".join(read_tail(item)))

    target.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as bundle:
        for name, content in members.items():
            bundle.writestr(name, content)
    return target

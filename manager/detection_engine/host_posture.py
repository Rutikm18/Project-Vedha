"""
host_posture.py — credentialed host posture & attacker-behaviour (IOA) detection.

The probe's credentialed collectors (ssh_inventory, windows_inventory) read a
host's OWN authoritative state over an authenticated session: the real service
table and its binary paths, Windows Defender status, local administrators, the
running-process list, and listening sockets. The manager stored all of it and
NO rule read any of it — only correlate.py's MS17-010 hotfix check touched the
Windows inventory at all. So a host with Defender switched off, a service running
from C:\\Users\\Public, or a cryptominer in its process list reported completely
clean.

This module closes that gap. It is the host-side complement to posture_rules.py's
network-observation rules: those see a service from the outside; these read what
the host itself reports from the inside. Because the source is credentialed
(authoritative — ingest tags it so), its findings are CONFIRMED, the strongest
state the engine assigns.

Two kinds of signal:
  * MISCONFIGURATION / WEAKNESS — unquoted service path (T1574.009), a service
    binary in a user-writable directory (T1543.003), too many local admins.
  * INDICATOR OF ATTACK (IOA) — endpoint protection disabled (T1562.001), a
    known-malicious/cryptominer process (T1496), a backdoor/C2 listener (T1571).
    These are behaviours an attacker PRODUCES, not just exposure an attacker could
    use — the thing a VA that only looks at open ports can never surface.

DESIGN (same discipline as posture_rules.py):
  * Pure parsing, no I/O; deterministic — same inventory in, same findings out.
  * A detector NEVER guesses. Format-Table truncation ('…'), an absent section, a
    command that errored, or an unparseable line all yield NOTHING, never a false
    accusation — the asymmetry favours silence (a false "your AV is off" or
    "you're running a miner" destroys trust in every other finding).
  * Curated bad-process / writable-path / backdoor-port sets are small, explicit
    and cited — the match MECHANISM is the value, not a bundled blocklist.
  * Returns findings already keyed + risk-scored, plus a per-rule evaluation
    trace (MATCH / NO_MATCH / NO_EVIDENCE) so a non-finding explains itself and
    coverage can tell "checked and clean" from "never credentialed-scanned".
"""
from __future__ import annotations

import hashlib
import re
from datetime import datetime, timezone
from typing import Any, Optional

from models import Asset, Fact
from posture_rules import (
    OUTCOME_MATCH, OUTCOME_NO_EVIDENCE, OUTCOME_NO_MATCH, PostureFinding, TraceRow,
    _STATE_CONF, _state_for, compute_risk,
)

_WIN = "windows_inventory"
_SSH = "ssh_inventory"


def _hp_id(asset_ip: str, rule_id: str, subject: str) -> str:
    """Deterministic id keyed by (asset, rule, subject) so several findings of the
    same rule on one host (three bad services, two miner processes) coexist without
    colliding, and the SAME subject re-hashes identically across runs for delta."""
    raw = f"{asset_ip}|{rule_id}|{subject}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


def _inventory(fact: Fact) -> dict:
    data = fact.data if isinstance(fact.data, dict) else {}
    inv = data.get("inventory")
    return inv if isinstance(inv, dict) else {}


def _evidence_ref(f: Fact) -> str:
    if f.source_file:
        return f"{f.source_file}:{f.source_line}"
    return f"{f.scanner}:{f.target}:{f.port}"


# ── Format-List parsing ("Key : Value" per line) ──────────────────────────────
_KV_RE = re.compile(r"^\s*([A-Za-z][A-Za-z0-9 _]+?)\s*:\s*(.*?)\s*$")


def parse_kv_list(text: str) -> dict[str, str]:
    """Parse PowerShell `Format-List` output into {key: value}. Robust to blank
    lines and the __error__/__stderr__ sentinels the collector writes on failure."""
    out: dict[str, str] = {}
    if not isinstance(text, str) or text.startswith("__error__") or text.startswith("__stderr__"):
        return out
    for line in text.splitlines():
        m = _KV_RE.match(line)
        if m:
            out[m.group(1).strip().lower()] = m.group(2).strip()
    return out


def _as_bool(val: str | None) -> Optional[bool]:
    if val is None:
        return None
    v = val.strip().lower()
    if v in ("true", "1", "yes", "enabled"):
        return True
    if v in ("false", "0", "no", "disabled"):
        return False
    return None


# ── Windows: endpoint protection disabled / degraded (IOA, T1562.001) ─────────
def detect_av_disabled(fact: Fact) -> Optional[dict]:
    """Get-MpComputerStatus said the antimalware service or real-time protection
    is OFF. A defender that reports healthy, a host where the cmdlet errored (no
    Defender present — common on servers / third-party AV), or an unparseable blob
    all return None: we only ever fire on a POSITIVELY parsed False.
    """
    inv = _inventory(fact)
    kv = parse_kv_list(inv.get("defender_status", ""))
    if not kv:
        return None
    am = _as_bool(kv.get("amserviceenabled"))
    rtp = _as_bool(kv.get("realtimeprotectionenabled"))
    off = []
    if am is False:
        off.append("antimalware service disabled")
    if rtp is False:
        off.append("real-time protection disabled")
    if not off:
        return None
    return {"disabled": off,
            "amservice_enabled": am, "realtime_protection_enabled": rtp,
            "signature_last_updated": kv.get("antivirussignaturelastupdated")}


# ── Windows: service binary path analysis ─────────────────────────────────────
# A service ImagePath under one of these lives somewhere a non-admin user can
# write, so a standard user (or malware running as one) can replace the binary the
# service launches as SYSTEM. Deliberately the clearly-user-writable locations
# only — ProgramData is left out because legitimate vendor services use it, and a
# false "malware persistence" call is worse than a missed one.
_WRITABLE_DIR_RE = re.compile(
    r"\\(users|temp|tmp|appdata|public|downloads|perflogs|\$recycle\.bin"
    r"|windows\\temp)\\", re.IGNORECASE)
# The image-path token: an optionally-quoted drive path up to its first executable
# extension. Group 1 is set when the path was quoted.
_SVC_PATH_RE = re.compile(
    r'("?)([A-Za-z]:\\[^"\r\n]*?\.(?:exe|dll|bat|cmd|ps1|com|scr))', re.IGNORECASE)
_SVC_NAME_RE = re.compile(r"^\s*(\S+)")
_TRUNCATED = ("…", "...")


def _service_rows(services_text: str):
    """Yield (name, image_path, was_quoted) per service line. Skips the header,
    the separator, blank lines, and any line Format-Table truncated — a truncated
    path cannot be judged, so it is never accused."""
    if not isinstance(services_text, str) or services_text.startswith("__"):
        return
    for line in services_text.splitlines():
        s = line.strip()
        if not s or s.lower().startswith("name") or set(s) <= set("- "):
            continue
        if any(t in line for t in _TRUNCATED):
            continue
        m = _SVC_PATH_RE.search(line)
        if not m:
            continue
        name_m = _SVC_NAME_RE.match(line)
        name = name_m.group(1) if name_m else "?"
        yield name, m.group(2), bool(m.group(1))


def detect_service_writable_path(fact: Fact) -> list[dict]:
    """Services whose binary lives in a user-writable directory — a SYSTEM-level
    code-execution foothold (T1543.003). One evidence dict per offending service."""
    out: list[dict] = []
    seen: set[str] = set()
    for name, path, _quoted in _service_rows(_inventory(fact).get("services", "")):
        if _WRITABLE_DIR_RE.search(path) and path.lower() not in seen:
            seen.add(path.lower())
            out.append({"service": name, "image_path": path})
    return out


def detect_unquoted_service_path(fact: Fact) -> list[dict]:
    """Unquoted service ImagePath containing a space in a directory component
    (CWE-428 / T1574.009): Windows resolves `C:\\Program Files\\x.exe` by trying
    `C:\\Program.exe` first, so a writable `C:\\Program.exe` hijacks a SYSTEM
    service. Only fires when the path is BOTH unquoted AND has a space before the
    executable, and is not purely under System32 (which never has spaces)."""
    out: list[dict] = []
    seen: set[str] = set()
    for name, path, quoted in _service_rows(_inventory(fact).get("services", "")):
        if quoted:
            continue
        # a space anywhere in the directory portion is what makes it ambiguous
        head = path.rsplit("\\", 1)[0]
        if " " in head and path.lower() not in seen:
            seen.add(path.lower())
            out.append({"service": name, "image_path": path})
    return out


# ── Windows: excessive local administrators ───────────────────────────────────
# A small, auditable set of principals that are expected in Administrators and do
# not count toward "excessive" (the built-in account and the usual domain groups).
_EXPECTED_ADMINS = {"administrator", "domain admins", "enterprise admins"}
_MAX_LOCAL_ADMINS = 10


def detect_excessive_local_admins(fact: Fact) -> Optional[dict]:
    """The local Administrators group has an unusually large membership — a wide
    privilege surface (T1078 / CWE-269). Counts parsed member names from the
    Get-LocalGroupMember table; informational unless clearly excessive."""
    text = _inventory(fact).get("local_admins", "")
    if not isinstance(text, str) or text.startswith("__"):
        return None
    members: list[str] = []
    for line in text.splitlines():
        s = line.strip()
        if not s or s.lower().startswith("name") or set(s) <= set("- "):
            continue
        name_m = _SVC_NAME_RE.match(line)
        if name_m:
            members.append(name_m.group(1))
    extra = [m for m in members if m.split("\\")[-1].lower() not in _EXPECTED_ADMINS]
    if len(members) < _MAX_LOCAL_ADMINS:
        return None
    return {"admin_count": len(members), "threshold": _MAX_LOCAL_ADMINS,
            "non_default_sample": extra[:12]}


# ── Linux: known-malicious / cryptominer processes (IOA, T1496) ───────────────
# Curated, unambiguous bad process names: Linux cryptojacking families and the
# miners they drop. Dual-use admin/offensive tools (nc, ncat, socat, python) are
# DELIBERATELY excluded — their presence is not evidence of compromise, and
# flagging them would bury the real signal in noise. Match is exact on the
# `ps -eo comm=` basename (case-insensitive), never a substring, so `xmrig` never
# matches an unrelated `xmrigcheck-is-fine`.
_MALICIOUS_PROCS: dict[str, str] = {
    "xmrig": "XMRig Monero cryptominer",
    "minerd": "cpuminer/minerd cryptominer",
    "cpuminer": "cpuminer cryptominer",
    "cgminer": "cgminer cryptominer",
    "xmr-stak": "xmr-stak cryptominer",
    "kinsing": "Kinsing malware loader (cryptojacking botnet)",
    "kdevtmpfsi": "Kinsing miner payload (kdevtmpfsi)",
    "kthreaddi": "impostor kernel-thread miner (kthreaddi)",
    "watchdogs": "Watchdogs cryptojacking worm",
    "kworkerds": "kworkerds cryptojacking impostor",
    "sustes": "Sustes cryptojacking malware",
    "ddgs": "DDG mining botnet (ddgs)",
    "systemten": "SystemTen cryptominer",
    "xlg": "xlg cryptojacking agent",
    "bioset": "biosetjenkins cryptojacking persistence",
    "tsm": "TSM cryptojacking miner",
}


def _process_names(fact: Fact) -> list[str]:
    text = _inventory(fact).get("processes", "")
    if not isinstance(text, str) or text.startswith("__"):
        return []
    return [p.strip() for p in text.splitlines() if p.strip()]


def detect_malicious_process(fact: Fact) -> list[dict]:
    """A process whose name exactly matches a curated cryptominer/malware family."""
    out: list[dict] = []
    for name in _process_names(fact):
        base = name.rsplit("/", 1)[-1].lower()
        label = _MALICIOUS_PROCS.get(base)
        if label:
            out.append({"process": name, "match": label})
    return out


# ── Linux: backdoor/C2 listener bound on the host (IOA, T1571) ────────────────
# ss/netstat LISTEN line: capture the local address:port. A listener on a known
# backdoor/C2 default port bound to a wildcard address is a host-confirmed
# indicator, stronger than seeing the port from the network (the host itself
# reports the socket is open and listening).
_LISTEN_RE = re.compile(r"(?:^|\s)(\*|0\.0\.0\.0|\[::\]|::|\[::\]|0:0:0:0:0:0:0:0):(\d{1,5})(?:\s|$)")


def _backdoor_ports() -> dict[int, str]:
    """Reuse port_intel's curated backdoor/C2 port table so the host-side and
    network-side layers agree on what a backdoor port is (single source of truth)."""
    try:
        from port_intel import _BACKDOOR
        return dict(_BACKDOOR)
    except Exception:  # noqa: BLE001 — defensive; never sink detection
        return {}


def detect_backdoor_listener(fact: Fact) -> list[dict]:
    """A wildcard-bound listener on a known backdoor/C2 default port, read from the
    host's own ss/netstat output."""
    bd = _backdoor_ports()
    if not bd:
        return []
    out: list[dict] = []
    seen: set[int] = set()
    inv = _inventory(fact)
    for section in ("listening_tcp", "listening_udp"):
        text = inv.get(section, "")
        if not isinstance(text, str):
            continue
        for line in text.splitlines():
            for m in _LISTEN_RE.finditer(line):
                try:
                    port = int(m.group(2))
                except ValueError:
                    continue
                if port in bd and port not in seen:
                    seen.add(port)
                    out.append({"port": port, "listener": bd[port],
                                "bind": m.group(1), "proto": "udp" if section.endswith("udp") else "tcp"})
    return out


# ── rule metadata ─────────────────────────────────────────────────────────────
class _HPRule:
    __slots__ = ("rule_id", "title", "severity", "cwe", "mitre", "category",
                 "scanner", "remediation", "fp_notes")

    def __init__(self, rule_id, title, severity, cwe, mitre, category, scanner,
                 remediation, fp_notes):
        self.rule_id = rule_id
        self.title = title
        self.severity = severity
        self.cwe = cwe
        self.mitre = mitre
        self.category = category
        self.scanner = scanner
        self.remediation = remediation
        self.fp_notes = fp_notes


HOST_RULES: list[_HPRule] = [
    _HPRule("HOST-AV-DISABLED", "Endpoint protection disabled or degraded",
            "high", "CWE-693", "T1562.001", "endpoint_protection", _WIN,
            "Re-enable Microsoft Defender's antimalware service and real-time "
            "protection (or confirm a managed third-party AV is active and "
            "reporting). Disabled AV is a common post-compromise action — "
            "investigate why it is off before assuming it is intentional.",
            "Fires only on a POSITIVELY parsed AMServiceEnabled/RealTimeProtection "
            "= False. A host with no Defender (cmdlet errors — third-party AV or "
            "Server Core) emits no parseable status and never fires this."),
    _HPRule("HOST-SERVICE-WRITABLE-PATH", "Service binary in a user-writable directory",
            "high", "CWE-732", "T1543.003", "privilege_escalation", _WIN,
            "Move the service binary to a protected location (Program Files / "
            "System32) and restrict the directory ACL, or remove the service. A "
            "SYSTEM service launched from a user-writable path lets a low-privileged "
            "user replace the binary and run code as SYSTEM.",
            "Reads the real Win32_Service PathName. Truncated Format-Table lines are "
            "skipped, not guessed at. Confirm the service is legitimate — some "
            "vendor agents legitimately install under ProgramData (excluded here)."),
    _HPRule("HOST-UNQUOTED-SERVICE-PATH", "Unquoted Windows service path",
            "medium", "CWE-428", "T1574.009", "privilege_escalation", _WIN,
            "Quote the service ImagePath in the registry so the space-containing "
            "path resolves unambiguously. Unquoted, Windows tries each space-"
            "delimited prefix (C:\\Program.exe first), which a writable higher-level "
            "path can hijack to run as the service account.",
            "Only fires when the path is BOTH unquoted AND contains a space in a "
            "directory component. System32 paths (no spaces) never match."),
    _HPRule("HOST-EXCESSIVE-LOCAL-ADMINS", "Excessive local administrators",
            "low", "CWE-269", "T1078", "misconfiguration", _WIN,
            "Review and trim the local Administrators group to the minimum set of "
            "accounts; prefer just-in-time / group-managed admin over standing "
            "membership. A wide admin group broadens the credential-theft blast "
            "radius on this host.",
            "Threshold-based and informational; counts parsed member names. A large "
            "number can be legitimate on a management host — review, don't assume."),
    _HPRule("HOST-MALICIOUS-PROCESS", "Known-malicious / cryptominer process running",
            "critical", "CWE-506", "T1496", "malware_indicator", _SSH,
            "Isolate and investigate the host immediately — a process matching a "
            "known cryptojacking/malware family is running. Identify the parent, "
            "persistence and initial access; this is an active-compromise indicator, "
            "not a configuration weakness.",
            "Exact basename match against a small curated family list; dual-use "
            "admin tools are deliberately excluded. A match is high-signal but still "
            "warrants IR confirmation (a sanctioned miner is rare but possible)."),
    _HPRule("HOST-BACKDOOR-LISTENER", "Backdoor/C2 listener bound on the host",
            "high", "CWE-506", "T1571", "malware_indicator", _SSH,
            "Investigate the listening process and the account that owns it — a "
            "wildcard-bound listener on a known backdoor/C2 default port is a "
            "compromise indicator. Identify and remove the implant; preserve volatile "
            "evidence first if IR applies.",
            "Uses the same curated backdoor-port table as the network exposed-service "
            "layer. A legitimate service that happens to use one of these ports will "
            "match — confirm the owning process from the host."),
]

# Detector dispatch: each rule_id -> (detector, multi?) where multi detectors
# return a list of evidence dicts (one finding each) and single detectors return
# one evidence dict or None.
_SINGLE = {
    "HOST-AV-DISABLED": detect_av_disabled,
    "HOST-EXCESSIVE-LOCAL-ADMINS": detect_excessive_local_admins,
}
_MULTI = {
    "HOST-SERVICE-WRITABLE-PATH": detect_service_writable_path,
    "HOST-UNQUOTED-SERVICE-PATH": detect_unquoted_service_path,
    "HOST-MALICIOUS-PROCESS": detect_malicious_process,
    "HOST-BACKDOOR-LISTENER": detect_backdoor_listener,
}
_RULE_BY_ID = {r.rule_id: r for r in HOST_RULES}


def _subject_of(rule_id: str, ev: dict) -> str:
    """A stable per-finding discriminator so multiple findings of one rule coexist."""
    for key in ("image_path", "process", "port", "service"):
        if ev.get(key) is not None:
            return str(ev[key])
    return rule_id


def detect_host_posture_traced(
    asset: Asset, exposure: dict[str, dict] | None = None,
) -> tuple[list[PostureFinding], list[TraceRow]]:
    """Run the credentialed host-posture / IOA rules over one asset's inventory
    facts. Returns (findings, traces). Findings are CONFIRMED (credentialed source)
    and already risk-scored. A rule whose collector never ran on this host emits a
    NO_EVIDENCE trace, so 'not credentialed-scanned' is visible and never passes for
    'checked and clean'."""
    exposure = exposure or {}
    exp = exposure.get(asset.ip, {})
    internet_facing = exp.get("internet_facing")
    default_auth = exp.get("auth_enforced")
    now = datetime.now(timezone.utc).isoformat()

    facts_by_scanner: dict[str, list[Fact]] = {_WIN: [], _SSH: []}
    for f in asset.facts:
        if f.scanner in facts_by_scanner:
            facts_by_scanner[f.scanner].append(f)

    out: list[PostureFinding] = []
    traces: list[TraceRow] = []

    def _emit(rule: _HPRule, f: Fact, ev: dict) -> None:
        subject = _subject_of(rule.rule_id, ev)
        state = _state_for(f.scanner)            # credentialed -> confirmed
        port = ev.get("port") if isinstance(ev.get("port"), int) else None
        risk, priority = compute_risk(rule.severity, state, internet_facing, default_auth)
        pf = PostureFinding(
            finding_id=_hp_id(asset.ip, rule.rule_id, subject),
            asset_ip=asset.ip, rule_id=rule.rule_id, title=rule.title,
            category=rule.category, severity=rule.severity, state=state,
            confidence=_STATE_CONF.get(state, 90), cwe=rule.cwe, mitre=rule.mitre,
            port=port, proto=ev.get("proto"), evidence_refs=[_evidence_ref(f)],
            evidence=ev, remediation=rule.remediation, fp_notes=rule.fp_notes,
            internet_facing=internet_facing, auth_enforced=default_auth,
            risk_score=risk, priority=priority, created_at=now, scanner=f.scanner)
        out.append(pf)
        traces.append(TraceRow(rule.rule_id, f.scanner, OUTCOME_MATCH, asset.ip,
                               port=port, evidence=ev))

    for rule in HOST_RULES:
        facts = facts_by_scanner.get(rule.scanner, [])
        if not facts:
            traces.append(TraceRow(rule.rule_id, rule.scanner, OUTCOME_NO_EVIDENCE,
                                   asset.ip,
                                   reason=f"no {rule.scanner} (credentialed) evidence for this asset"))
            continue
        fired = False
        for f in facts:
            if rule.rule_id in _SINGLE:
                ev = _SINGLE[rule.rule_id](f)
                if ev:
                    _emit(rule, f, ev)
                    fired = True
            else:
                for ev in _MULTI[rule.rule_id](f):
                    _emit(rule, f, ev)
                    fired = True
        if not fired:
            # collector ran but the weakness was not present -> genuinely clean
            traces.append(TraceRow(rule.rule_id, rule.scanner, OUTCOME_NO_MATCH,
                                   asset.ip))
    return out, traces


def detect_host_posture(asset: Asset,
                        exposure: dict[str, dict] | None = None) -> list[PostureFinding]:
    """Findings-only wrapper over detect_host_posture_traced."""
    findings, _ = detect_host_posture_traced(asset, exposure)
    return findings

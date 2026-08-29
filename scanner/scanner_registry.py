"""
scanner_registry.py — the single source of truth for WHICH scanners are trusted.

Every scanner emits ScanResult.scanner (a stable name). This module is the one
place that says, for each of those names: its human display name, what it assesses,
and — the point of this module — whether it is VERIFIED (validated against ground
truth and safe to present as authoritative) or EXPERIMENTAL (runs, but its output
is not yet trusted and must be labelled as such).

WHY THIS EXISTS: the campaign shows a capability catalog and the report shows
findings; both were silent on trust, so an operator could not tell a validated
result from an unvalidated one. A VA that cannot say "how sure are we, and why"
is not a VA. This registry lets the scanner-module view flag verified scanners and
lets the finding section mark each finding verified/experimental from its source.

It mirrors the manager's detection_engine.posture_rules.VALIDATED_SCANNERS — the two
lists must be kept in agreement (probe decides what to trust; the manager confirms
findings only from those same trusted sensors). Keep VERIFIED curated and reviewed;
it is governed data, like an allowlist.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ScannerInfo:
    name: str          # the ScanResult.scanner value this describes
    display: str       # operator-facing name
    category: str      # discovery | ports | os | posture | service | tls | udp | rpc
    verified: bool     # validated against ground truth → present as authoritative
    summary: str       # one line: what it assesses


# The catalog. `verified=True` == validated against the reference target
# (DESKTOP-34M18MB / 192.168.1.77) and proven accurate; everything else RUNS but
# is presented as experimental until it earns a place here.
_SCANNERS: tuple[ScannerInfo, ...] = (
    # ── verified (trusted) ──
    ScannerInfo("host_discovery", "Host Discovery", "discovery", True,
                "Liveness across ICMP/TCP/ARP with graded confidence."),
    ScannerInfo("port_scan", "TCP Port Scan", "ports", True,
                "Canonical open-TCP set (connect scan)."),
    ScannerInfo("syn_scan", "TCP SYN Scan", "ports", True,
                "Stateless SYN scan with retransmit; harvests stack signals."),
    ScannerInfo("mass_scan", "Mass Port Scan", "ports", True,
                "High-rate open-port discovery."),
    ScannerInfo("os_fingerprint", "OS Fingerprint", "os", True,
                "OS family + exact Windows build (SMB2 NTLM) with provenance."),
    ScannerInfo("smb_scan", "SMB Posture", "posture", True,
                "SMB dialect, signing, SMBv1, and NTLM-derived build."),
    ScannerInfo("rdp_scan", "RDP Posture", "posture", True,
                "X.224 confirm + NLA/TLS and whether NLA is required."),
    ScannerInfo("tls_scan", "TLS Posture", "tls", True,
                "Accepted versions, weak ciphers, certificate validity, JA4X."),
    ScannerInfo("msrpc_scan", "MSRPC Endpoint Map", "rpc", True,
                "Anonymous EPM enumeration + dynamic-port discovery."),
    ScannerInfo("rpc_reconcile", "RPC Port Reconcile", "rpc", True,
                "Confirms EPM-advertised dynamic ports (advertised vs reachable)."),
    ScannerInfo("udp_scan", "UDP Services", "udp", True,
                "Honest UDP probing (responded / open|filtered), amplifier checks."),
    ScannerInfo("service_banner", "Service Banners", "service", True,
                "Banner grab across open ports; captures the raw banner, reports "
                "'no banner' honestly rather than guessing a version."),
    ScannerInfo("printer_scan", "Printers", "service", True,
                "Confirms a printer via a real PJL protocol handshake, not the port "
                "number."),

    # ── experimental (runs, not yet validated → labelled provisional) ──
    ScannerInfo("web_scan", "Web Assessment", "service", False,
                "HTTP headers, methods, and surface checks."),
    ScannerInfo("db_scan", "Database Services", "service", False,
                "Database service exposure checks."),
    ScannerInfo("ssh_scan", "SSH Posture", "service", False,
                "SSH algorithms / Terrapin exposure."),
    ScannerInfo("ldap_scan", "LDAP Services", "service", False,
                "LDAP/anonymous-bind checks."),
    ScannerInfo("dns_scan", "DNS Services", "service", False, "DNS service checks."),
    ScannerInfo("nfs_scan", "NFS Exports", "service", False, "NFS export exposure."),
    ScannerInfo("ftp_scan", "FTP Services", "service", False, "FTP/anonymous checks."),
    ScannerInfo("rsync_scan", "Rsync Modules", "service", False, "Rsync module exposure."),
    ScannerInfo("vnc_scan", "VNC Services", "service", False, "VNC auth checks."),
    ScannerInfo("smtp_scan", "SMTP Services", "service", False, "SMTP/STARTTLS checks."),
    ScannerInfo("snmp_scan", "SNMP Services", "udp", False,
                "SNMP community / v3 checks."),
    ScannerInfo("ipmi_scan", "IPMI/BMC", "service", False, "IPMI cipher-0 checks."),
    ScannerInfo("smb_enum_scan", "SMB Enumeration", "posture", False,
                "Null-session share/user enumeration (unauthenticated only)."),
)

REGISTRY: dict[str, ScannerInfo] = {s.name: s for s in _SCANNERS}

VERIFIED: frozenset = frozenset(s.name for s in _SCANNERS if s.verified)
EXPERIMENTAL: frozenset = frozenset(s.name for s in _SCANNERS if not s.verified)


def is_verified(scanner: str | None) -> bool:
    """True only for a scanner explicitly on the verified (trusted) list. Unknown
    scanners are treated as NOT verified — trust is opt-in, never assumed."""
    return scanner in VERIFIED


def info(scanner: str | None) -> ScannerInfo | None:
    return REGISTRY.get(scanner) if scanner else None


def verification_report() -> dict:
    """The scanner-module trust view: which scanners are verified vs experimental,
    with display metadata. This is what the campaign/report shows so the operator
    can see, at a glance, which results are authoritative."""
    def _entry(s: ScannerInfo) -> dict:
        return {"name": s.name, "display": s.display, "category": s.category,
                "summary": s.summary}
    return {
        "verified": [_entry(s) for s in _SCANNERS if s.verified],
        "experimental": [_entry(s) for s in _SCANNERS if not s.verified],
        "verified_count": len(VERIFIED),
        "experimental_count": len(EXPERIMENTAL),
    }

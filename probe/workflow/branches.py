"""
branches.py — the deep-scan branch registry: ONE declarative description of
every Gate-5 branch, replacing 20 near-identical hand-written blocks in
workflow_engine.py.

WHY THIS EXISTS. Every branch ran the same five steps — gate, split cached vs
fresh, construct the scanner, record the run, store the results — so each new
service meant pasting ten more lines into an already 740-line engine, and any
fix to the shared shape (a cache-key change, a new trace field) had to be made
twenty times or it silently applied to only some branches. That is exactly the
class of bug where "the scanner works standalone but the manager never saw the
fact": the branch was wired *slightly* differently from its neighbours. A table
cannot drift from itself.

WHAT A SPEC OWNS: only what actually differs between branches — the gate key,
the emitted scanner name, which ports it cares about, whether the router can
route extra ports to it, and any constructor arguments beyond the standard set.
The execution shape lives once, in workflow_engine._run_branch.

WHAT IT DELIBERATELY DOES NOT OWN: the scanner CLASS. Specs name the class by
its attribute name in workflow_engine's namespace and the engine resolves it at
call time, so `monkeypatch.setattr("workflow.workflow_engine.TLSScanner", ...)`
keeps working exactly as before — tests patch the engine, not this table.

Port tables stay in gates.py (they are policy copied verbatim from pipeline.py,
and gate_5_branch_eligible needs them independently); this module references
them rather than restating them, so the two can never disagree.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from .asset import Asset
from .gates import (
    AI_PORTS, DB_PORTS, DNS_PORTS, FTP_PORTS, IPMI_PORTS, LDAP_PORTS,
    MSRPC_PORTS, NFS_PORTS, PRINTER_PORTS, RDP_PORTS, RSYNC_PORTS,
    SMB_ENUM_PORTS, SMTP_PORTS, SNMP_PORTS, SSH_PORTS, TLS_PORTS, VNC_PORTS,
    WEB_PORTS,
)

# A branch's per-invocation constructor kwargs. Returning MORE than one dict
# runs the scanner more than once — the database branch needs exactly this: one
# pass over ports with a known engine, one over router-discovered ports with
# every probe enabled.
KwargsBuilder = Callable[[Asset, list[int]], list[dict]]


def _ports_kwargs(asset: Asset, to_scan: list[int]) -> list[dict]:
    """The default: hand the scanner the ports that still need probing."""
    return [{"ports": to_scan}]


def _no_kwargs(asset: Asset, to_scan: list[int]) -> list[dict]:
    """For scanners that take no `ports` argument — a host-level branch, or a
    datagram scanner that already knows the single port it probes."""
    return [{}]


def _web_kwargs(asset: Asset, to_scan: list[int]) -> list[dict]:
    """Tell the web scanner which of these ports service_banner OBSERVED
    speaking TLS, so HTTPS on a non-standard port is fetched as https first
    instead of being guessed from a static port table (and missed)."""
    tls_seen = {p for p in to_scan if (asset.services.get(p) or {}).get("tls")}
    return [{"ports": to_scan, "tls_ports": tls_seen}]


def _db_kwargs(asset: Asset, to_scan: list[int]) -> list[dict]:
    """Ports with a known database engine get that engine's probe; ports the
    router flagged from a banner signature get every probe tried, since their
    engine is by definition not the one the port number implies."""
    from scanner.db_scanner import DEFAULT_DB_PORTS

    known = {p: DEFAULT_DB_PORTS[p] for p in to_scan if p in DEFAULT_DB_PORTS}
    unknown = [p for p in to_scan if p not in DEFAULT_DB_PORTS]
    runs: list[dict] = []
    if known:
        runs.append({"port_map": known})
    if unknown:
        runs.append({"port_map": {p: "" for p in unknown}, "try_all_on_port": True})
    return runs


@dataclass(frozen=True)
class BranchSpec:
    """One deep-scan branch. `branch` is the gate key (gates.PROFILE_DEEP_BRANCHES
    decides whether a profile allows it); `component` is both the emitted
    ScanResult.scanner name and the trace component id."""

    branch: str
    component: str
    scanner: str                       # attribute name in workflow_engine's namespace
    ports: frozenset | None            # None = host-level (cached under port key None)
    label: str = ""                    # operator-facing name in the plan/manifest
    role: str = ""                     # one line: what this branch collects
    dynamic: str | None = None         # router branch key that may add ports
    datagram: bool = False             # probe the fixed table, not the open-port set
    kwargs: KwargsBuilder = _ports_kwargs

    @property
    def host_level(self) -> bool:
        """True when the fact describes the host rather than one port — it is
        cached under a null port and never intersected with the open-port set."""
        return self.ports is None


# Order is the order branches run, preserved from the hand-written blocks so
# traces and any consumer reading them are byte-for-byte unaffected.
BRANCHES: tuple[BranchSpec, ...] = (
    BranchSpec("tls", "tls_scan", "TLSScanner", frozenset(TLS_PORTS),
               "TLS Inspector",
               "Collect supported protocol, cipher, and certificate facts.",
               dynamic="tls"),
    BranchSpec("web", "web_scan", "WebScanner", frozenset(WEB_PORTS),
               "Web Fingerprint",
               "Collect passive HTTP response, header, and technology facts.",
               dynamic="web", kwargs=_web_kwargs),
    # Host-level: smb_scanner probes one fixed port but the fact it returns
    # (smbv1_enabled / signing_required) describes the host's SMB stack.
    BranchSpec("smb", "smb_scan", "SMBScanner", None,
               "SMB Negotiation",
               "Collect SMB dialect support through negotiation only.",
               kwargs=_no_kwargs),
    BranchSpec("db", "db_scan", "DBScanner", frozenset(DB_PORTS),
               "Database Fingerprint",
               "Identify database listeners through minimal protocol handshakes.",
               dynamic="db", kwargs=_db_kwargs),
    BranchSpec("mcp_ai", "mcp_ai_scan", "MCPAIScanner", frozenset(AI_PORTS),
               "AI / MCP Discovery",
               "Identify exposed AI and MCP discovery endpoints without invoking tools."),
    BranchSpec("ssh", "ssh_scan", "SSHScanner", frozenset(SSH_PORTS),
               "SSH Posture",
               "Collect SSH identification and negotiated algorithm facts.",
               dynamic="ssh"),
    BranchSpec("smb_enum", "smb_enum_scan", "SMBEnumScanner", frozenset(SMB_ENUM_PORTS),
               "SMB Enumeration",
               "Collect null-session share and account facts where anonymous access is allowed."),
    BranchSpec("ldap", "ldap_scan", "LDAPScanner", frozenset(LDAP_PORTS),
               "LDAP Directory",
               "Collect anonymous-bind and naming-context facts."),
    BranchSpec("dns", "dns_scan", "DNSScanner", frozenset(DNS_PORTS),
               "DNS Service",
               "Collect recursion and zone-transfer exposure facts."),
    BranchSpec("nfs", "nfs_scan", "NFSScanner", frozenset(NFS_PORTS),
               "NFS Exports",
               "Collect exported-filesystem and RPC program facts."),
    BranchSpec("ftp", "ftp_scan", "FTPScanner", frozenset(FTP_PORTS),
               "FTP Service",
               "Collect banner and anonymous-login facts."),
    BranchSpec("rsync", "rsync_scan", "RsyncScanner", frozenset(RSYNC_PORTS),
               "Rsync Modules",
               "Collect unauthenticated module-listing facts."),
    BranchSpec("vnc", "vnc_scan", "VNCScanner", frozenset(VNC_PORTS),
               "VNC Service",
               "Collect RFB version and authentication-requirement facts."),
    BranchSpec("smtp", "smtp_scan", "SMTPScanner", frozenset(SMTP_PORTS),
               "SMTP Service",
               "Collect banner, extension, and relay-posture facts."),
    BranchSpec("msrpc", "msrpc_scan", "MSRPCScanner", frozenset(MSRPC_PORTS),
               "MSRPC Endpoint Map",
               "Collect anonymously enumerable endpoint-map facts."),
    # RDP: the confirming X.224 + NLA-posture scanner. Without this branch the
    # agent's network_va never assessed 3389, so RDP-without-NLA never reached
    # the manager — the original reason branch coverage is now table-driven.
    BranchSpec("rdp", "rdp_scan", "RDPScanner", frozenset(RDP_PORTS),
               "RDP Posture",
               "Confirm RDP and collect NLA/TLS requirement facts."),
    BranchSpec("printer", "printer_scan", "PrinterScanner", frozenset(PRINTER_PORTS),
               "Printer Service",
               "Confirm a printer through a real PJL handshake, not the port number."),
    # Datagram branches: the probe is a UDP read sent straight at the authorized
    # target, so the port set comes from the table — an open TCP port is neither
    # required nor meaningful. SNMPScanner probes 161 itself and takes no `ports`.
    BranchSpec("snmp", "snmp_scan", "SNMPScanner", frozenset(SNMP_PORTS),
               "SNMP Read Probe",
               "Collect read-only SNMP service facts.",
               datagram=True, kwargs=_no_kwargs),
    BranchSpec("ipmi", "ipmi_scan", "IPMIScanner", frozenset(IPMI_PORTS),
               "IPMI / BMC Probe",
               "Collect RMCP presence and IPMI capability facts.",
               datagram=True),
)

BRANCH_BY_NAME = {spec.branch: spec for spec in BRANCHES}
# execution.py renders the plan from this, so a branch cannot appear in the
# engine without appearing in the plan (or vice versa).
BRANCH_COMPONENT = {spec.branch: spec.component for spec in BRANCHES}

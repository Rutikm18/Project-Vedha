"""
gates.py — precondition functions deciding whether each stage of the
workflow runs. Every function is pure (Asset + config in, bool out) so
workflow_engine.py's loop stays a thin "if precondition: run" driver with
no decision logic of its own.

Port tables below are copied VERBATIM from pipeline.py (and the relevant
scanner modules' own DEFAULT_* constants) — never re-derived or guessed —
since pipeline.py itself is left untouched (this is a new, parallel
orchestrator, not a modification of the existing one) and the two must
agree on what a profile actually means.
"""
from __future__ import annotations

from datetime import timedelta

from scanner.db_scanner import DEFAULT_DB_PORTS
# ONE authoritative TLS port set. gates.py used to keep its own copy, and the two
# had already drifted (3269 in one, 989 in the other), so a port could satisfy the
# branch spec and then be refused by the gate — a silent coverage hole.
from scanner.service_enum import TLS_PORTS

from .asset import Asset

# --- verbatim from pipeline.py ------------------------------------------
_IT_BASE_PORTS = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 389, 443, 445, 465, 587,
           623, 636, 993, 995, 1433, 1521, 2049, 2375, 3306, 3389, 5060, 5432, 5900,
           5985, 5986, 6379, 6443, 8000, 8080, 8443, 9200, 10250, 11211, 27017]

# --- risk-catalog coverage (the collection half of the exposed-service rules) --
# MIRRORS manager/detection_engine/port_intel.py. Every port the manager can raise
# an exposed-service finding on must be SCANNED here, or the rule is dead code: the
# detector reads the open-port set, so a port nobody probed can never be reported.
#
# This was a real, total blind spot. The base catalog above covers 40 ports and the
# risk catalog names 85; 55 were never swept — including EVERY backdoor/C2 port
# (4444 Meterpreter, 31337 Back Orifice, 12345 NetBus, 6667 IRC C2, 2323 Mirai,
# 5555 ADB), etcd, Kafka, Cassandra, Zookeeper, the r-services and X11. So
# POSTURE-EXPOSED-BACKDOOR — a HIGH-severity rule — could not fire on a default
# network_va no matter what was listening.
#
# tests/test_risk_port_coverage.py asserts probe coverage ⊇ manager catalog, the
# same governed-data discipline as scanner_registry ↔ VALIDATED_SCANNERS. Add a
# port there and this list must grow with it.
VA_RISK_PORTS = [
    69, 79,                                  # tftp, finger (cleartext legacy)
    512, 513, 514,                           # r-services (rexec/rlogin/rsh)
    1080,                                    # socks proxy — common C2 pivot
    1337, 4444, 4445, 4446, 5555, 6666, 6667, 6668, 6669, 7547, 9999,
    12345, 12346, 20034, 27374, 30303, 31337, 2323,   # backdoor / C2 / RAT / Mirai
    1434, 3050, 5433, 8529, 50000,           # mssql-udp-browser, firebird, pg-alt, arangodb, db2
    2181, 5601, 5984, 7000, 7001, 8086, 9042, 9092, 9300, 27018,  # datastores/APIs
    2376, 2379, 2380, 10255,                 # docker-tls, etcd client/peer, kubelet ro
    3283, 5800, 5902, 5903, 6000,            # ARD, vnc-http, vnc:2/:3, X11
    8006, 8088, 9090, 10000, 15672, 16010, 50070,     # admin UIs
]

IT_PORTS = sorted(set(_IT_BASE_PORTS) | set(VA_RISK_PORTS))
IOT_PORTS = [22, 23, 80, 443, 554, 1883, 8883, 5683, 8080, 8443, 8888, 9000, 9100,
            49152, 62078, 5000, 8081, 37777]
WEB_PORTS = {80, 443, 8080, 8443, 8000, 8888, 9000, 9200, 8081, 5000}
SMB_PORTS = {139, 445}
DB_PORTS = set(DEFAULT_DB_PORTS)
AI_PORTS = {11434, 8000, 8080, 5000, 3000, 1234, 8001, 7860, 11435}  # DEFAULT_AI_PORTS in mcp_ai_scanner.py
UDP_PORTS = {53, 123, 161, 137, 11211}                # UDP_PROBES.keys() in udp_scanner.py
SNMP_PORTS = {161}
SSH_PORTS = {22, 2222}
LDAP_PORTS = {389, 636, 3268, 3269}
SMB_ENUM_PORTS = {445}
DNS_PORTS = {53}
NFS_PORTS = {111, 2049}
FTP_PORTS = {21}
RSYNC_PORTS = {873}
VNC_PORTS = {5900, 5901}
IPMI_PORTS = {623}
SMTP_PORTS = {25, 587}
MSRPC_PORTS = {135}
RDP_PORTS = {3389}
PRINTER_PORTS = {9100, 631}

PROFILE_PORTS = {"it": IT_PORTS, "iot": IOT_PORTS, "ot": []}
PROFILE_DEEP_BRANCHES = {
    "it": {"tls", "web", "smb", "db", "mcp_ai", "snmp", "ssh", "smb_enum", "ldap", "dns", "nfs", "ftp", "rsync", "vnc", "ipmi", "smtp", "msrpc", "rdp", "printer"},
    "iot": {"tls", "web", "ssh", "ftp", "vnc", "printer"},
    "ot": set(),
}
LIVENESS_RECHECK_THRESHOLD = {"it": timedelta(hours=1), "iot": timedelta(minutes=5)}

_BRANCH_PORT_TABLE = {"tls": TLS_PORTS, "web": WEB_PORTS, "smb": SMB_PORTS,
                      "db": DB_PORTS, "mcp_ai": AI_PORTS, "snmp": SNMP_PORTS,
                      "ssh": SSH_PORTS, "smb_enum": SMB_ENUM_PORTS, "ldap": LDAP_PORTS,
                      "dns": DNS_PORTS, "nfs": NFS_PORTS, "ftp": FTP_PORTS,
                      "rsync": RSYNC_PORTS, "vnc": VNC_PORTS, "ipmi": IPMI_PORTS,
                      "smtp": SMTP_PORTS, "msrpc": MSRPC_PORTS, "rdp": RDP_PORTS,
                      "printer": PRINTER_PORTS}


def gate_0_is_passive_profile(profile: str) -> bool:
    """True means OT/ICS passive-only mode — a hard stop, never reached by
    any active-probe gate below. workflow_engine.py checks this FIRST and
    routes to PassiveCollector exclusively when True."""
    return profile == "ot"


def gate_2_host_discovery(asset: Asset, profile: str) -> bool:
    if gate_0_is_passive_profile(profile):
        return False
    threshold = LIVENESS_RECHECK_THRESHOLD.get(profile, timedelta(hours=1))
    return asset.needs_recheck_live(threshold)


def gate_3_port_scan(asset: Asset, profile: str) -> bool:
    if gate_0_is_passive_profile(profile):
        return False
    return asset.last_seen_alive is not None


def gate_4_service_banner(asset: Asset) -> bool:
    return len(asset.open_ports_for_deep_scan()) > 0


def gate_4b_os_fingerprint(asset: Asset, profile: str) -> bool:
    """OS identity for a host already proven alive. Runs on the SAME evidence the
    port stage produced — no extra reachability requirement — because the OS is an
    inventory fact about the host, not about a service: device classification
    weights it, and the manager's rules read it. Passive (OT) profiles never
    actively probe, so they are excluded."""
    if gate_0_is_passive_profile(profile):
        return False
    return asset.last_seen_alive is not None


def gate_5_branch_eligible(branch: str, asset: Asset, profile: str,
                           service_filter: set[str] | None,
                           dynamically_routed: bool = False) -> bool:
    """Does `branch` apply to this host?
      - Must be in this profile's allowed deep-scan set (ot allows none;
        iot allows tls/web only; it allows tls/web/smb/db).
      - If the caller passed an explicit --services filter, branch must be in it.
      - SNMP is a UDP read probe. Explicit SNMP jobs target the authorized scope
        directly; unfiltered assessments still require prior liveness.
      - Otherwise, either router.py already determined this branch applies from
        OBSERVED banner/handshake content (dynamically_routed=True — the
        HTTPS-on-9443 case, passed in by the caller, this function doesn't
        re-derive it), OR at least one open port falls in the branch's
        static port table (the fallback signal, weaker but still useful
        when nothing volunteered an identifying banner).
    """
    if branch not in PROFILE_DEEP_BRANCHES.get(profile, set()):
        return False
    if service_filter is not None and branch not in service_filter:
        return False
    if branch in ("snmp", "ipmi"):
        # SNMP/IPMI are UDP probes sent directly to the authorized target; they do
        # not need an open TCP port first, only prior liveness (or an explicit job).
        return asset.last_seen_alive is not None or service_filter is not None
    if dynamically_routed:
        return True
    open_ports = asset.open_ports_for_deep_scan()
    return bool(open_ports & _BRANCH_PORT_TABLE.get(branch, set()))


def gate_6_credentialed_collection(asset: Asset, has_ssh_creds: bool, has_win_creds: bool) -> bool:
    if not has_ssh_creds and not has_win_creds:
        return False
    if asset.last_seen_alive is None:
        return False
    if asset.cred_collected:
        return False
    return True

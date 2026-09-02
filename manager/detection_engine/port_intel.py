"""
port_intel.py — port-intelligence catalog for the exposed-service detector.

The dedicated scanners (SMB/RDP/TLS/MSRPC/SNMP) each have a deep posture rule. But
the long tail of RISKY open ports — backdoor/C2 listeners, unauthenticated data
stores, container/orchestration APIs, cleartext protocols, and exposed admin UIs —
has no deep scanner and no rule. Yet the port itself, plus a banner and the exposure
class, is enough to raise a defensible finding an operator must triage.

This catalog is the researched map from a well-known port to a RISK CLASS. Sources:
IANA registrations, Metasploit/Cobalt-Strike defaults, historically unauthenticated
data-store defaults (Redis/Mongo/Elasticsearch/Memcached/CouchDB/Docker/etcd/K8s),
Mirai/IRC-botnet ports, and cleartext legacy protocols. Severity is the BASE for an
internal exposure; internet-facing exposure escalates one level (the BOD-26-04
"asset exposure" variable — the manager's own reachability data).
"""
from __future__ import annotations

from dataclasses import dataclass

# Severity ladder used for internet-facing escalation.
_SEV_ORDER = ["info", "low", "medium", "high", "critical"]


def escalate(sev: str, steps: int = 1) -> str:
    try:
        i = _SEV_ORDER.index(sev)
    except ValueError:
        return sev
    return _SEV_ORDER[min(i + steps, len(_SEV_ORDER) - 1)]


@dataclass(frozen=True)
class PortRisk:
    category: str        # backdoor | container | datastore | database | cleartext
                         #  | remote_access | admin_ui
    service: str         # human name
    severity: str        # BASE severity (internal). internet-facing escalates +1.
    cwe: str
    mitre: str
    note: str            # why it matters / what to check


# ── Backdoor / C2 / RAT default ports (suspicious regardless of exposure) ──────
# Metasploit/CS handler defaults, classic RATs, IRC-botnet and Mirai ports.
_BACKDOOR = {
    4444: "Metasploit/Meterpreter default handler",
    4445: "Metasploit alt handler",
    4446: "Metasploit alt handler",
    1337: "'leet' — common backdoor/dev listener",
    31337: "Back Orifice (classic backdoor)",
    12345: "NetBus (classic backdoor)",
    12346: "NetBus (classic backdoor)",
    20034: "NetBus Pro",
    27374: "SubSeven (classic RAT)",
    30303: "Sockets de Troie",
    9999: "common RAT/interactive shell",
    6666: "IRC — botnet C2",
    6667: "IRC — botnet C2",
    6668: "IRC — botnet C2",
    6669: "IRC — botnet C2",
    5555: "Android ADB / freeciv RATs — remote shell",
    2323: "Telnet-alt — Mirai/IoT botnet",
    7547: "CWMP/TR-069 — Mirai worm vector",
    1080: "SOCKS proxy — frequently abused for pivoting",
}

# ── Container / orchestration APIs (unauth = remote code execution) ────────────
_CONTAINER = {
    2375: "Docker API (unauthenticated TCP) — remote container/host takeover",
    2376: "Docker API (TLS) — verify client-cert auth",
    2379: "etcd client API — cluster secrets store",
    2380: "etcd peer API",
    6443: "Kubernetes API server",
    8443: "Kubernetes/API-alt",
    10250: "Kubelet API — node command execution",
    10255: "Kubelet read-only API",
    5000: "Docker registry / dev app server",
}

# ── Data stores historically unauthenticated by default ───────────────────────
_DATASTORE = {
    6379: "Redis (no auth by default)",
    27017: "MongoDB",
    27018: "MongoDB shard",
    9200: "Elasticsearch HTTP (often unauth)",
    9300: "Elasticsearch transport",
    11211: "Memcached (no auth; also a UDP amplifier)",
    5984: "CouchDB",
    9042: "Cassandra CQL",
    7000: "Cassandra internode",
    7001: "Cassandra SSL internode",
    8086: "InfluxDB",
    2181: "ZooKeeper",
    9092: "Kafka broker",
    5601: "Kibana (ES front-end)",
    9000: "dev app / SonarQube / Portainer",
}

# ── Traditional databases (auth expected, exposure still a risk) ──────────────
_DATABASE = {
    3306: "MySQL/MariaDB",
    5432: "PostgreSQL",
    1433: "Microsoft SQL Server",
    1434: "MSSQL monitor (UDP)",
    1521: "Oracle TNS",
    50000: "IBM Db2 / SAP",
    3050: "Firebird",
    5433: "PostgreSQL-alt",
    8529: "ArangoDB",
}

# ── Cleartext / legacy protocols (credentials/data in the clear) ──────────────
_CLEARTEXT = {
    23: ("Telnet", "high"),
    21: ("FTP (control)", "medium"),
    512: ("rexec", "high"),
    513: ("rlogin", "high"),
    514: ("rsh/syslog", "high"),
    69: ("TFTP", "medium"),
    79: ("finger", "low"),
    110: ("POP3 (cleartext)", "medium"),
    143: ("IMAP (cleartext)", "medium"),
    25: ("SMTP (verify STARTTLS)", "low"),
    2049: ("NFS", "medium"),
    111: ("RPCbind/portmapper", "medium"),
}

# ── Remote access / management not covered by a dedicated rule ────────────────
_REMOTE = {
    5900: "VNC", 5901: "VNC", 5902: "VNC", 5903: "VNC",
    5800: "VNC over HTTP",
    5985: "WinRM (HTTP)",
    5986: "WinRM (HTTPS)",
    6000: "X11 (often unauthenticated)",
    3283: "Apple Remote Desktop",
}

# ── Exposed admin / dev / CI web UIs ──────────────────────────────────────────
_ADMIN_UI = {
    8080: "HTTP-alt / app or proxy",
    8081: "HTTP-alt / app",
    8888: "HTTP-alt / notebook (Jupyter)",
    9090: "Prometheus / Cockpit",
    3000: "Grafana / dev server",
    15672: "RabbitMQ management",
    10000: "Webmin",
    8006: "Proxmox VE",
    9100: "JetDirect / Prometheus node-exporter",
    50070: "Hadoop NameNode UI",
    8088: "Hadoop/YARN ResourceManager",
    16010: "HBase master UI",
}


def _banner_confirms_backdoor(banner: str | None) -> bool:
    if not banner:
        return False
    b = banner.lower()
    return any(s in b for s in ("meterpreter", "shell", "cmd.exe", "/bin/sh",
                                "backdoor", "cobaltstrike", "beacon"))


# service_banner's soft-matched `service` label -> the risk class it PROVES on
# any port. Stronger than the port number: the probe observed the protocol.
#   shell   — a bash/cmd prompt answered the socket: a bind shell, whatever the port
#   telnet  — IAC negotiation / bare login prompt: cleartext credentials
_SERVICE_RISK = {
    "shell":  ("backdoor",  "interactive shell answered the socket", "high"),
    "telnet": ("cleartext", "Telnet / cleartext login prompt", "high"),
}


# ── observation beats the port-number hypothesis ──────────────────────────────
# A catalog entry is a HYPOTHESIS ("something on 7000 is probably Cassandra").
# When service_banner positively identifies a DIFFERENT, well-known product that
# legitimately occupies that port, the hypothesis is disproven and the finding is a
# false positive. Real case that motivated this: macOS ships an AirPlay receiver on
# 5000 and 7000, so a clean laptop reported "Docker registry exposed" and
# "Cassandra internode exposed" — two high/medium findings, both wrong, on every
# Mac in scope.
#
# Keyed by port -> normalized product/service tokens that mean "not the risky
# service this port stands for". Deliberately NARROW: only products that are
# unambiguous and common enough to matter. It suppresses ONLY the port-number
# guess; a backdoor or cleartext verdict driven by observed protocol is never
# suppressed here (those are decided before this check).
_BENIGN_OCCUPANTS: dict[int, set[str]] = {
    5000: {"airtunes", "airplay"},      # macOS AirPlay Receiver, not a Docker registry
    7000: {"airtunes", "airplay"},      # macOS AirPlay Receiver, not Cassandra
    5001: {"airtunes", "airplay"},
    8080: {"cups"},                     # a print server, not an app admin UI
    631:  {"cups"},
}


def _normalized(*values: str | None) -> str:
    return "".join(ch for ch in "".join(v or "" for v in values).lower() if ch.isalnum())


def contradicts_port_hypothesis(port: int, product: str | None,
                                service: str | None = None) -> bool:
    """True when an identified product proves the catalog's port guess wrong."""
    expected = _BENIGN_OCCUPANTS.get(port)
    if not expected:
        return False
    seen = _normalized(product, service)
    return any(token in seen for token in expected)


def classify_port(port: int, banner: str | None = None,
                  service: str | None = None,
                  basic_auth_cleartext: bool = False,
                  product: str | None = None) -> PortRisk | None:
    """Map an open TCP port (+ optional banner, the probe's soft-matched service
    label and product, and its Basic-auth-over-plaintext flag) to its risk class,
    or None if the port isn't independently interesting.

    Evidence order: observed-protocol risk (a shell is a shell on any port) beats
    everything; then a product identification that CONTRADICTS the port's meaning
    suppresses it; only then does the port-number catalog apply."""
    svc_risk = _SERVICE_RISK.get((service or "").lower())
    if port in _BACKDOOR or _banner_confirms_backdoor(banner) or (
            svc_risk and svc_risk[0] == "backdoor"):
        name = _BACKDOOR.get(port) or (svc_risk[1] if svc_risk else None) \
            or "interactive shell suggested by banner"
        return PortRisk("backdoor", name, "high", "CWE-506", "T1571",
                        "Non-standard listener commonly used for backdoors/C2 — "
                        "identify the owning process; treat as compromise until cleared.")
    if svc_risk and svc_risk[0] == "cleartext" and port not in _CLEARTEXT:
        # Telnet moved off 23 is still telnet — the probe saw the protocol.
        return PortRisk("cleartext", svc_risk[1], svc_risk[2], "CWE-319", "T1040",
                        "Legacy/cleartext protocol — credentials and data are "
                        "sniffable; replace with an encrypted equivalent.")
    if basic_auth_cleartext and port not in _CLEARTEXT:
        return PortRisk("cleartext", "HTTP Basic authentication over plaintext", "medium",
                        "CWE-319", "T1040",
                        "The service challenges for Basic credentials on a connection "
                        "that never negotiated TLS — every login is sniffable. Serve it "
                        "over HTTPS or put it behind an authenticating proxy.")
    # Everything below is a port-number hypothesis. A positive identification of a
    # different, known-benign occupant disproves it, so report nothing rather than
    # a confidently-wrong service name.
    if contradicts_port_hypothesis(port, product, service):
        return None
    if port in _CONTAINER:
        return PortRisk("container", _CONTAINER[port], "high", "CWE-306", "T1610",
                        "Container/orchestration control plane — an unauthenticated "
                        "endpoint here is remote code execution on the host/cluster.")
    if port in _DATASTORE:
        return PortRisk("datastore", _DATASTORE[port], "medium", "CWE-306", "T1210",
                        "Data store that ships without authentication by default — "
                        "verify auth is enforced and the port is not reachable broadly.")
    if port in _DATABASE:
        return PortRisk("database", _DATABASE[port], "medium", "CWE-284", "T1210",
                        "Database reachable over the network — restrict to app tier; "
                        "confirm strong auth and that it is not internet-exposed.")
    if port in _CLEARTEXT:
        name, sev = _CLEARTEXT[port]
        return PortRisk("cleartext", name, sev, "CWE-319", "T1040",
                        "Legacy/cleartext protocol — credentials and data are "
                        "sniffable; replace with an encrypted equivalent.")
    if port in _REMOTE:
        return PortRisk("remote_access", _REMOTE[port], "medium", "CWE-284", "T1021",
                        "Remote-access/management service exposed — restrict to "
                        "VPN/jump hosts and enforce strong auth + MFA.")
    if port in _ADMIN_UI:
        return PortRisk("admin_ui", _ADMIN_UI[port], "low", "CWE-284", "T1190",
                        "Admin/dev web interface exposed — confirm authentication "
                        "and that it should be reachable from this segment.")
    return None

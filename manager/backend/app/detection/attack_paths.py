"""
attack_paths.py — manager-native composite correlation over raw probe facts.

The probe ships FACTS (no findings); the manager's CVE detection engine turns a
fact's product/version into CVE findings, but the highest-signal output — the
CHAINED attack path an operator must fix first — comes from correlating multiple
weaknesses on one host. The probe has a rich correlation layer
(probe/scanner/findings.py), but the manager is a separate deployment and cannot
import it, and that layer never ran on the production detection path. This module
brings the composite correlation onto the outbox detection path, native to the
manager and operating directly on the persisted facts.

Design:
  * Pure logic (no DB, no I/O) — the composites are unit-testable in isolation and
    the caller (engine_bridge) handles persistence/dedup.
  * Device-aware (Track B2): a role from the probe's device_classifier amplifies
    severity — SMB-signing-off on a *domain controller* is a domain-takeover
    primitive, not a medium misconfiguration.
  * Every composite CITES the signals it was built from (evidence.correlated),
    so nothing is a black box, and carries ATT&CK techniques for the matrix.
"""
from __future__ import annotations

from app.models.enums import FindingSeverity

# ── signal port tables (mirrors probe gates.py / findings.py) ────────────────
RDP_PORT = 3389
# Cleartext-credential protocols: a sniffing position harvests creds from any.
_CLEARTEXT_PORTS: dict[int, str] = {21: "FTP", 23: "Telnet", 110: "POP3", 143: "IMAP"}
# Datastore ports whose exposure + no-auth is a direct data-breach path.
_DB_PORTS: dict[int, str] = {
    1433: "MSSQL", 3306: "MySQL", 5432: "Postgres", 1521: "Oracle",
    27017: "MongoDB", 6379: "Redis", 9200: "Elasticsearch", 11211: "Memcached",
    5984: "CouchDB", 9042: "Cassandra",
}
_DEFAULT_SNMP_COMMUNITIES = {"public", "private"}

# Severity ladder, low → high, for role-based amplification.
_LADDER = [
    FindingSeverity.info, FindingSeverity.low, FindingSeverity.medium,
    FindingSeverity.high, FindingSeverity.critical,
]


def _bump(severity: FindingSeverity, steps: int = 1) -> FindingSeverity:
    try:
        idx = _LADDER.index(severity)
    except ValueError:
        return severity
    return _LADDER[min(idx + steps, len(_LADDER) - 1)]


def _is_domain_controller(role_detail: str | None, device_role: str | None) -> bool:
    return role_detail == "domain_controller"


def _is_network_device(device_role: str | None) -> bool:
    return device_role in ("network_device", "network")


# ── per-host signal extraction ───────────────────────────────────────────────
class _HostSignals:
    """The weaknesses observed on ONE host, distilled from its facts."""

    def __init__(self) -> None:
        self.open_tcp: set[int] = set()
        self.smbv1: bool = False
        self.smb_signing_required: bool | None = None
        self.smb_seen: bool = False
        self.unauth: bool = False
        self.snmp_default_community: bool = False
        self.db_ports: set[int] = set()
        self.device_role: str | None = None
        self.role_detail: str | None = None

    def observe(self, fact: dict) -> None:
        data = fact.get("data") if isinstance(fact.get("data"), dict) else {}
        scanner = fact.get("scanner")
        port = fact.get("port")
        proto = (fact.get("proto") or "tcp").lower()
        status = fact.get("status")

        if port is not None and proto == "tcp" and status == "open":
            try:
                self.open_tcp.add(int(port))
            except (TypeError, ValueError):
                pass

        if scanner in ("smb_scan", "smb_enum"):
            self.smb_seen = True
            if data.get("smbv1_enabled") is True:
                self.smbv1 = True
            if "signing_required" in data:
                self.smb_signing_required = bool(data.get("signing_required"))

        if scanner == "device_classify" or data.get("device_type"):
            self.device_role = data.get("device_type") or self.device_role
            self.role_detail = data.get("role_detail") or self.role_detail

        # Unauthenticated datastore/service access — require an EXPLICIT signal,
        # never infer it from an open port alone (that would be a false positive).
        if (
            data.get("unauthenticated") is True
            or data.get("unauth") is True
            or data.get("access") == "unauthenticated"
            or data.get("requires_auth") is False
            or data.get("auth") == "none"
        ):
            self.unauth = True

        if scanner in ("snmp_scan", "snmp_enum"):
            community = str(data.get("community") or "").lower()
            if community in _DEFAULT_SNMP_COMMUNITIES or data.get("default_community") is True:
                self.snmp_default_community = True

        if port is not None and proto == "tcp" and status == "open":
            try:
                p = int(port)
            except (TypeError, ValueError):
                p = None
            if p in _DB_PORTS:
                self.db_ports.add(p)

    def finalize(self, device_role: str | None, role_detail: str | None) -> None:
        """Fold in a persisted device role (from a prior device_inventory scan)."""
        self.device_role = self.device_role or device_role
        self.role_detail = self.role_detail or role_detail


def _group(facts: list[dict], roles: dict[str, dict]) -> dict[str, _HostSignals]:
    hosts: dict[str, _HostSignals] = {}
    for fact in facts:
        if not isinstance(fact, dict):
            continue
        target = fact.get("target")
        if not target:
            continue
        hosts.setdefault(target, _HostSignals()).observe(fact)
    for ip, sig in hosts.items():
        role = roles.get(ip) or {}
        sig.finalize(role.get("device_role"), role.get("role_detail"))
    return hosts


# ── composites ───────────────────────────────────────────────────────────────
def _ntlm_relay(ip: str, s: _HostSignals) -> dict | None:
    if s.smb_signing_required is not False:   # only when signing is NOT required
        return None
    correlated = ["SMB-SIGNING-NOT-REQUIRED"]
    severity = FindingSeverity.medium
    detail = ("SMB signing is not required — the host is a viable NTLM relay target.")
    if s.smbv1:
        correlated.append("SMB-V1-ENABLED")
        severity = FindingSeverity.high
        detail = ("SMB signing is not required AND SMBv1 is enabled — the host is both "
                  "coercible and relayable: an attacker can coerce authentication and "
                  "relay it to take over the host.")
    dc = _is_domain_controller(s.role_detail, s.device_role)
    if dc:
        severity = FindingSeverity.critical   # relaying to a DC = domain takeover
        detail += " This host is a DOMAIN CONTROLLER — relaying here is a path to full domain compromise."
    return {
        "rule_id": "CORR-NTLM-RELAY-PATH",
        "title": "NTLM relay attack path (SMB signing not required)",
        "severity": severity,
        "target": ip,
        "port": 445,
        "description": detail,
        "remediation": ("Require SMB signing on all hosts (especially DCs); disable SMBv1; "
                        "enforce LDAP channel binding + signing."),
        "mitre_techniques": ["T1557.001", "T1210"],
        "evidence": {"correlated": correlated, "smbv1": s.smbv1,
                     "domain_controller": dc, "device_role": s.device_role,
                     "role_detail": s.role_detail},
    }


def _legacy_windows(ip: str, s: _HostSignals) -> dict | None:
    if not (s.smbv1 and RDP_PORT in s.open_tcp):
        return None
    severity = FindingSeverity.high
    dc = _is_domain_controller(s.role_detail, s.device_role)
    detail = ("SMBv1 is enabled (wormable, EternalBlue class) AND RDP is exposed "
              "(brute-force / BlueKeep) on the same host — a classic ransomware entry path.")
    if dc:
        severity = FindingSeverity.critical
        detail += " On a DOMAIN CONTROLLER this is a direct route to domain-wide ransomware."
    return {
        "rule_id": "CORR-LEGACY-WINDOWS-SURFACE",
        "title": "Legacy Windows attack surface (SMBv1 + exposed RDP)",
        "severity": severity,
        "target": ip,
        "port": None,
        "description": detail,
        "remediation": "Disable SMBv1; restrict RDP to VPN/jump hosts with NLA + MFA.",
        "mitre_techniques": ["T1210", "T1021.001"],
        "evidence": {"correlated": ["SMB-V1-ENABLED", "SVC-RDP-EXPOSED"],
                     "domain_controller": dc, "device_role": s.device_role},
    }


def _cleartext_cluster(ip: str, s: _HostSignals) -> dict | None:
    present = sorted(p for p in _CLEARTEXT_PORTS if p in s.open_tcp)
    if len(present) < 2:
        return None
    names = [f"{_CLEARTEXT_PORTS[p]}({p})" for p in present]
    return {
        "rule_id": "CORR-CLEARTEXT-CLUSTER",
        "title": "Multiple cleartext services (credential-capture risk)",
        "severity": FindingSeverity.medium,
        "target": ip,
        "port": None,
        "description": (f"Multiple cleartext protocols exposed on one host ({', '.join(names)}) — "
                        "a single sniffing position captures credentials across services."),
        "remediation": "Replace cleartext services with encrypted equivalents (SSH / FTPS / IMAPS / HTTPS).",
        "mitre_techniques": ["T1040"],
        "evidence": {"correlated": [f"SVC-CLEARTEXT-{p}" for p in present], "ports": present},
    }


def _exposed_db_unauth(ip: str, s: _HostSignals) -> dict | None:
    """B3: an exposed datastore with unauthenticated access = direct data breach."""
    if not (s.db_ports and s.unauth):
        return None
    names = sorted(f"{_DB_PORTS[p]}({p})" for p in s.db_ports)
    severity = FindingSeverity.critical
    return {
        "rule_id": "CORR-DB-UNAUTH-EXPOSED",
        "title": "Exposed datastore with unauthenticated access",
        "severity": severity,
        "target": ip,
        "port": sorted(s.db_ports)[0],
        "description": (f"A datastore ({', '.join(names)}) is reachable AND accepts unauthenticated "
                        "access — any client on this path can read/modify the data directly."),
        "remediation": "Require authentication; bind the datastore to loopback/private interfaces; firewall the port.",
        "mitre_techniques": ["T1210", "T1078", "T1005"],
        "evidence": {"correlated": ["SVC-DATASTORE-EXPOSED", "UNAUTH-ACCESS"],
                     "db_ports": sorted(s.db_ports)},
    }


def _snmp_public_lateral(ip: str, s: _HostSignals) -> dict | None:
    """B3: a default SNMP community on network gear = topology/creds for lateral movement."""
    if not s.snmp_default_community:
        return None
    net = _is_network_device(s.device_role)
    severity = FindingSeverity.high if net else FindingSeverity.medium
    detail = ("A default/guessable SNMP community string is readable — it leaks device config, "
              "routes, and often credentials.")
    if net:
        detail += (" This host is NETWORK infrastructure — the leaked topology and community are a "
                   "lateral-movement and pivot primitive.")
    return {
        "rule_id": "CORR-SNMP-PUBLIC-LATERAL",
        "title": "Default SNMP community on infrastructure (lateral-movement risk)",
        "severity": severity,
        "target": ip,
        "port": 161,
        "description": detail,
        "remediation": "Set a strong SNMPv3 credential; disable SNMPv1/v2c public/private communities; ACL UDP/161.",
        "mitre_techniques": ["T1602.001", "T1078"],
        "evidence": {"correlated": ["SNMP-DEFAULT-COMMUNITY"], "network_device": net,
                     "device_role": s.device_role},
    }


_COMPOSITES = [
    _ntlm_relay, _legacy_windows, _cleartext_cluster,
    _exposed_db_unauth, _snmp_public_lateral,
]


def attack_path_findings(
    facts: list[dict], device_roles: dict[str, dict] | None = None,
) -> list[dict]:
    """Correlate composite attack paths from raw probe facts.

    `device_roles` maps ip → {device_role, role_detail} from persisted assets (a
    prior device_inventory scan), used for severity amplification. Returns a list
    of finding descriptors, most-severe first. Pure; deterministic; safe.
    """
    hosts = _group(facts or [], device_roles or {})
    out: list[dict] = []
    for ip, signals in hosts.items():
        for composite in _COMPOSITES:
            found = composite(ip, signals)
            if found is not None:
                out.append(found)
    out.sort(key=lambda d: _LADDER.index(d["severity"]), reverse=True)
    return out

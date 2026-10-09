"""
crown_jewels.py — P4b: auto-select high-value targets when no operator-tagged assets.

Context (ATTACK_PATH_PLAN.md §3.5 / §9 FM-04):
  AttackPath generation requires at least one crown-jewel target. The router uses
  Asset.criticality == critical, but nothing in the detection path sets this field —
  so every engagement that has not been manually annotated gets no paths (FM-04).

Fix (this module):
  Score every asset from port profile, service banners, device role, and hostname
  patterns using the same heuristics XM Cyber, Tenable One, and BloodHound CE use
  for implicit crown-jewel selection. Assets scoring above a threshold are treated
  as implicit high-value targets for path generation. The operator's tagged assets
  always take precedence; auto-selection is a fallback, never a replacement.

Design:
  * Pure (no DB, no I/O) — takes Asset and Service ORM objects, returns scored list.
  * Port profiles and hostname patterns are derived from empirical red-team data:
    DC (88/389/636/3268), hypervisor (443+ESXi/vSphere/Proxmox, 902, 623 IPMI),
    database (1433/3306/5432/1521/27017/6379), IAM/PAM (389+non-DC, 1812, 8200,
    CyberArk/HashiCorp banners), OT/SCADA (102/502/20000/44818/4840).
  * Scores are additive weights (not probabilities). Threshold = 30 by default.
  * Auto-selected assets are annotated with auto_crown_jewel=True and the
    signals that triggered the selection.

Integration:
  app/routers/attack_paths.py._target_ids falls back to auto_crown_jewels()
  when no operator-tagged critical assets exist.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any


# ── port-profile scoring weights ──────────────────────────────────────────────

# Domain controller: all DC-characteristic ports together.
_DC_PORTS: dict[int, int] = {
    88: 15,    # Kerberos — the most reliable DC signal
    389: 8,    # LDAP
    636: 6,    # LDAPS
    3268: 12,  # Global Catalog
    3269: 10,  # GC over SSL
    445: 3,    # SMB (domain member, not unique, lower weight)
    135: 2,    # MSRPC (same)
}

# Hypervisor / bare-metal management: vSphere, Proxmox, Hyper-V, IPMI.
_HYPERVISOR_PORTS: dict[int, int] = {
    902: 20,   # VMware vSphere SDK — very specific
    443: 5,    # HTTPS (generic, needs banner confirmation)
    623: 15,   # IPMI — BMC interface
    8006: 20,  # Proxmox VE — highly specific
    8443: 4,   # alt HTTPS management
}

# Databases / data stores — direct data breach or RCE path.
_DB_PORTS: dict[int, int] = {
    1433: 10,  # MSSQL
    3306: 10,  # MySQL
    5432: 10,  # PostgreSQL
    1521: 12,  # Oracle
    27017: 10, # MongoDB
    6379: 10,  # Redis
    9200: 8,   # Elasticsearch
    5984: 8,   # CouchDB
    7474: 8,   # Neo4j
    9042: 8,   # Cassandra
    11211: 7,  # Memcached
}

# IAM / credential store — compromise = all assets compromised.
_IAM_PORTS: dict[int, int] = {
    8200: 20,  # HashiCorp Vault — highly specific
    1812: 12,  # RADIUS authentication server
    1813: 8,   # RADIUS accounting
    636: 4,    # LDAPS (non-DC, standalone LDAP server)
    389: 3,    # LDAP (non-DC)
}

# OT / SCADA / ICS — safety-critical systems.
_OT_PORTS: dict[int, int] = {
    102: 25,   # Siemens S7comm — highest confidence
    502: 20,   # Modbus
    20000: 20, # DNP3
    44818: 20, # EtherNet/IP (Rockwell/Allen-Bradley)
    4840: 18,  # OPC-UA
    47808: 15, # BACnet
    18245: 15, # GE SRTP
    1089: 12,  # FF HSE
}

# Scoring thresholds.
_THRESHOLD_AUTO_SELECT = 30    # minimum score to be auto-selected
_THRESHOLD_TIER1 = 60          # DC / hypervisor / IAM / OT tier
_THRESHOLD_TIER2 = 30          # database tier
_MAX_AUTO_TARGETS = 10         # cap; don't overwhelm the graph with targets


# ── hostname and banner patterns ──────────────────────────────────────────────

_DC_HOSTNAME_RE = re.compile(
    r"(^dc[\d]|[-_]dc[-_]|^adds[-_]|^ad[\d]|^ldap|domaincontrol|[\.\-]dc\b)",
    re.IGNORECASE,
)
_HYPERVISOR_HOSTNAME_RE = re.compile(
    r"(^esxi|vcenter|vsphere|proxmox|hyperv|hyper-v|xen|bmchost|^idrac|^ilo[\d])",
    re.IGNORECASE,
)
_DB_HOSTNAME_RE = re.compile(
    r"(^db[\d\-]|[-_]db[\d]|^sql|^mysql|^postgres|^oracle|^mongo|^redis|datastor)",
    re.IGNORECASE,
)
_IAM_HOSTNAME_RE = re.compile(
    r"(^iam[-_]|^pam[-_]|^vault|^cyberark|^hashicorp|^okta|^radius|^ldap[-_]|^kms)",
    re.IGNORECASE,
)
_OT_HOSTNAME_RE = re.compile(
    r"(^scada|^plc[\d]|^hmi[\d]|^dcs|^rtu[\d]|^historian|^opc|^bacnet|^modbus)",
    re.IGNORECASE,
)
_PAYMENT_HOSTNAME_RE = re.compile(
    r"(^pos[\d\-]|payment|checkout|ecom|^pci|^cardholder|^acquir)",
    re.IGNORECASE,
)

# Banner substrings that confirm a role (lowercased for matching).
_DC_BANNERS = ("defaultnamingcontext", "isglobalcatalogready", "microsoft active directory",
               "ldap://domaindn")
_HYPERVISOR_BANNERS = ("vmware esxi", "vsphere", "proxmox virtual environment",
                       "hyper-v", "xen server", "idrac", "ilo")
_VAULT_BANNERS = ("hashicorp vault", "x-vault-request-id", "cyberark")


# ── scoring engine ────────────────────────────────────────────────────────────


@dataclass
class CrownJewelScore:
    asset_id: str
    hostname: str | None
    ip_address: str | None
    score: int = 0
    role: str = "unknown"          # "dc" | "hypervisor" | "database" | "iam" | "ot" | "payment"
    signals: list[str] = field(default_factory=list)
    auto_selected: bool = False


def _score_asset(
    asset: Any,
    open_ports: set[int],
    banners: dict[int, str],
) -> CrownJewelScore:
    def ga(name: str, default: Any = None) -> Any:
        if isinstance(asset, dict):
            return asset.get(name, default)
        return getattr(asset, name, default)

    asset_id = str(ga("id") or ga("entity_id") or "")
    hostname = str(ga("hostname") or "").lower()
    ip = str(ga("ip_address") or "")
    device_role = str(getattr(ga("device_role"), "value", ga("device_role")) or "").lower()
    role_detail = str(ga("role_detail") or "").lower()
    criticality = str(getattr(ga("criticality"), "value", ga("criticality")) or "").lower()

    s = CrownJewelScore(asset_id=asset_id, hostname=hostname or None, ip_address=ip or None)
    # Match hostname patterns against the short label only (first FQDN segment) so
    # "esxi01.dc.local" does not match the DC pattern via its domain suffix.
    short_hostname = hostname.split(".")[0] if hostname else ""

    # Operator-tagged assets never need auto-selection; they won't be passed here.
    if criticality == "critical":
        s.score = 200
        s.role = "operator_tagged"
        s.signals.append("criticality=critical")
        return s

    # ── device role from probe classification ──────────────────────────────────
    if role_detail == "domain_controller" or "domain_controller" in device_role:
        s.score += 55
        s.role = "dc"
        s.signals.append("device_role=domain_controller")
    elif role_detail in ("vmware_hypervisor", "hypervisor") or "hypervisor" in device_role:
        s.score += 55
        s.role = "hypervisor"
        s.signals.append(f"device_role={role_detail or device_role}")
    elif "database" in device_role or role_detail in ("database_server", "datastore"):
        s.score += 35
        s.role = "database"
        s.signals.append("device_role=database")

    # ── port profile scoring ──────────────────────────────────────────────────
    dc_port_score = sum(w for p, w in _DC_PORTS.items() if p in open_ports)
    hypervisor_port_score = sum(w for p, w in _HYPERVISOR_PORTS.items() if p in open_ports)
    db_port_score = sum(w for p, w in _DB_PORTS.items() if p in open_ports)
    iam_port_score = sum(w for p, w in _IAM_PORTS.items() if p in open_ports)
    ot_port_score = sum(w for p, w in _OT_PORTS.items() if p in open_ports)

    best_port_role = max(
        ("dc", dc_port_score),
        ("hypervisor", hypervisor_port_score),
        ("database", db_port_score),
        ("iam", iam_port_score),
        ("ot", ot_port_score),
        key=lambda x: x[1],
    )
    if best_port_role[1] > 0:
        if s.role == "unknown":
            s.role = best_port_role[0]
        s.score += best_port_role[1]
        s.signals.append(f"port_profile={best_port_role[0]}(+{best_port_role[1]})")

    def _set_role(candidate: str) -> None:
        if s.role == "unknown":
            s.role = candidate

    # ── hostname patterns ──────────────────────────────────────────────────────
    if short_hostname:
        if _DC_HOSTNAME_RE.search(short_hostname):
            s.score += 20
            _set_role("dc")
            s.signals.append("hostname_pattern=dc")
        elif _HYPERVISOR_HOSTNAME_RE.search(short_hostname):
            s.score += 20
            _set_role("hypervisor")
            s.signals.append("hostname_pattern=hypervisor")
        elif _DB_HOSTNAME_RE.search(short_hostname):
            s.score += 15
            _set_role("database")
            s.signals.append("hostname_pattern=database")
        elif _IAM_HOSTNAME_RE.search(short_hostname):
            s.score += 20
            _set_role("iam")
            s.signals.append("hostname_pattern=iam")
        elif _OT_HOSTNAME_RE.search(short_hostname):
            s.score += 25
            _set_role("ot")
            s.signals.append("hostname_pattern=ot")
        elif _PAYMENT_HOSTNAME_RE.search(short_hostname):
            s.score += 20
            _set_role("payment")
            s.signals.append("hostname_pattern=payment")

    # ── banner confirmation (strongest signal — probe-confirmed role) ─────────
    all_banners = " ".join(b.lower() for b in banners.values() if b)
    if any(tok in all_banners for tok in _DC_BANNERS):
        s.score += 30
        s.role = "dc"   # banner overrides heuristic role
        s.signals.append("banner_confirmed=dc")
    elif any(tok in all_banners for tok in _HYPERVISOR_BANNERS):
        s.score += 30
        s.role = "hypervisor"
        s.signals.append("banner_confirmed=hypervisor")
    elif any(tok in all_banners for tok in _VAULT_BANNERS):
        s.score += 35
        s.role = "iam"
        s.signals.append("banner_confirmed=vault/iam")

    # OT ports are highly specific — a single confirmed OT port is a crown jewel.
    if ot_port_score > 0:
        s.score += 20
        s.role = "ot"
        s.signals.append(f"ot_port_confirmed(+{ot_port_score})")

    return s


def score_assets(
    assets: list[Any],
    services: list[Any],
) -> list[CrownJewelScore]:
    """Score every asset and return sorted list (highest score first).

    ``assets``   — Asset ORM objects or dicts.
    ``services`` — Service ORM objects or dicts (port, service_name, banner, asset_id).
    """
    # Build port → banner index per asset.
    ports_by_asset: dict[str, set[int]] = {}
    banners_by_asset: dict[str, dict[int, str]] = {}
    for svc in services:
        def gs(name: str) -> Any:
            return svc.get(name) if isinstance(svc, dict) else getattr(svc, name, None)

        aid = str(gs("asset_id") or "")
        if not aid:
            continue
        port = gs("port")
        banner = str(gs("banner") or gs("service_name") or "")
        try:
            port = int(port)
        except (TypeError, ValueError):
            continue
        ports_by_asset.setdefault(aid, set()).add(port)
        if banner:
            banners_by_asset.setdefault(aid, {})[port] = banner

    scores: list[CrownJewelScore] = []
    for asset in assets:
        def ga(name: str, default: Any = None) -> Any:
            return asset.get(name, default) if isinstance(asset, dict) else getattr(asset, name, default)

        asset_id = str(ga("id") or ga("entity_id") or "")
        open_ports = ports_by_asset.get(asset_id, set())
        banners = banners_by_asset.get(asset_id, {})
        sc = _score_asset(asset, open_ports, banners)
        scores.append(sc)

    scores.sort(key=lambda s: (-s.score, s.asset_id))
    return scores


def auto_crown_jewels(
    assets: list[Any],
    services: list[Any],
    threshold: int = _THRESHOLD_AUTO_SELECT,
    max_targets: int = _MAX_AUTO_TARGETS,
) -> list[CrownJewelScore]:
    """Select high-value targets automatically when the operator has tagged none.

    Returns up to ``max_targets`` assets scoring above ``threshold``, with OT
    and hypervisor assets always included when present regardless of score cap
    (compromising an OT controller or hypervisor is always catastrophic).
    """
    scores = score_assets(assets, services)
    selected: list[CrownJewelScore] = []
    seen: set[str] = set()

    # Tier 1: always include DC / hypervisor / IAM / OT if found.
    for sc in scores:
        if sc.role in ("dc", "hypervisor", "iam", "ot") and sc.score >= 20:
            sc.auto_selected = True
            selected.append(sc)
            seen.add(sc.asset_id)

    # Tier 2: fill remaining slots with threshold-passing assets.
    for sc in scores:
        if sc.asset_id in seen:
            continue
        if sc.score >= threshold and len(selected) < max_targets:
            sc.auto_selected = True
            selected.append(sc)
            seen.add(sc.asset_id)

    return selected[:max_targets]


def auto_crown_jewel_ids(
    assets: list[Any],
    services: list[Any],
    threshold: int = _THRESHOLD_AUTO_SELECT,
    max_targets: int = _MAX_AUTO_TARGETS,
) -> list[str]:
    """Convenience: return just the asset_id strings for auto-selected targets."""
    return [sc.asset_id for sc in auto_crown_jewels(assets, services, threshold, max_targets)]

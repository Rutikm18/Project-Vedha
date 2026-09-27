"""
finding_groups.py — collapse near-identical findings into "one fix" groups.

Findings are deduped per (engagement, asset, title), which is right for tracking
but noisy to prioritise from: the CVE track writes one row per CVE per host and
the posture track one row per port (``"<rule> (port N)"``). A single outdated
OpenSSH on ten hosts is dozens of rows that one upgrade closes.

Every finding gets ONE deterministic group identity, first match wins:

  1. rule    — ``evidence.rule_id``: the same posture check, any port, any host.
  2. product — CVE rows with a CPE 2.3 name: same vendor:product:version. One
               upgrade fixes all of them. Versions stay separate (different CVE
               sets), accuracy over compression.
  3. title   — everything else: the title with the port suffix stripped,
               case- and whitespace-normalised.

There is deliberately no "same CVE set" tier: enrichment attaches CVE ids to
some rows of an issue and not others, so keying on them split one issue into
two groups. Engine CVE rows without a product are titled by their CVE id, so
the title already groups them.

Groups never cross an engagement: the same IP in two engagements is two
different networks (often two customers), so "one fix closes N findings" would
be false. The engagement is part of every group's identity.

Pure — no DB, no I/O — so the grouping contract is unit-testable in isolation.
Group order mirrors the list's "critical always on top": groups that still have
an active finding first, then severity tier, KEV, validated exploit, risk.
"""
from __future__ import annotations

import re
import uuid
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime

SEVERITY_RANK = {"critical": 4, "high": 3, "medium": 2, "low": 1, "info": 0}
ACTIVE_STATUSES = frozenset({"open", "confirmed"})
HOSTS_SHOWN = 8
PORTS_SHOWN = 12
CVES_SHOWN = 8

_PORT_SUFFIX = re.compile(r"\s*\(port\s+\d+\)\s*$", re.IGNORECASE)
_WS = re.compile(r"\s+")
_CPE_WILDCARDS = {"", "*", "-"}


@dataclass(frozen=True)
class GroupRow:
    """One finding, reduced to the columns grouping needs."""
    id: uuid.UUID
    engagement_id: uuid.UUID
    title: str
    severity: str
    status: str
    cvss: float | None
    risk: float
    epss: float | None
    cve_ids: tuple[str, ...]
    asset_id: uuid.UUID | None
    asset_ip: str | None
    asset_hostname: str | None
    port: int | None
    rule_id: str | None
    cpe: str | None
    kev: bool
    exploit_validated: bool
    first_seen: datetime | None
    last_seen: datetime | None


def _display_title(title: str) -> str:
    return _WS.sub(" ", _PORT_SUFFIX.sub("", title or "")).strip() or "Untitled finding"


def _cpe_parts(cpe: str | None) -> tuple[str, str, str | None] | None:
    """(vendor, product, version|None) from a CPE 2.3 name, or None."""
    if not isinstance(cpe, str):
        return None
    parts = cpe.split(":")
    if len(parts) < 5 or parts[0] != "cpe" or parts[1] != "2.3":
        return None
    vendor, product = parts[3].lower(), parts[4].lower()
    if vendor in _CPE_WILDCARDS or product in _CPE_WILDCARDS:
        return None
    version = parts[5].lower() if len(parts) > 5 else ""
    return vendor, product, (None if version in _CPE_WILDCARDS else version)


def group_identity(row: GroupRow) -> tuple[str, str, str]:
    """(key, kind, label) — the deterministic group a finding belongs to."""
    if row.rule_id:
        return f"rule:{row.rule_id.strip().lower()}", "rule", _display_title(row.title)

    parts = _cpe_parts(row.cpe) if any(c and c.strip() for c in row.cve_ids) else None
    if parts is not None:
        vendor, product, version = parts
        key = f"product:{vendor}:{product}" + (f":{version}" if version else "")
        name = product.replace("_", " ")
        label = f"{name} {version} — known vulnerabilities" if version \
            else f"{name} — known vulnerabilities"
        return key, "product", label

    label = _display_title(row.title)
    return "title:" + label.lower(), "title", label


def _member_order(row: GroupRow) -> tuple:
    return (-SEVERITY_RANK.get(row.severity, 0), -row.risk, str(row.id))


def _member(row: GroupRow) -> dict:
    return {
        "id": row.id, "title": row.title, "severity": row.severity, "status": row.status,
        "asset_ip": row.asset_ip, "asset_hostname": row.asset_hostname, "port": row.port,
        "cve_ids": list(row.cve_ids), "risk": row.risk, "cvss": row.cvss,
    }


def _max(values: Iterable[float | None]) -> float | None:
    present = [v for v in values if v is not None]
    return max(present) if present else None


def _aggregate(engagement_id: uuid.UUID, key: str, kind: str, rows: list[GroupRow],
               member_cap: int) -> dict:
    rows = sorted(rows, key=_member_order)
    top = rows[0]
    severity_counts: dict[str, int] = {}
    status_counts: dict[str, int] = {}
    hosts: dict[uuid.UUID, dict] = {}
    ports: set[int] = set()
    cves: set[str] = set()
    for r in rows:
        severity_counts[r.severity] = severity_counts.get(r.severity, 0) + 1
        status_counts[r.status] = status_counts.get(r.status, 0) + 1
        if r.asset_id is not None and r.asset_id not in hosts:
            hosts[r.asset_id] = {"ip": r.asset_ip, "hostname": r.asset_hostname}
        if r.port is not None:
            ports.add(r.port)
        cves.update(c.strip().upper() for c in r.cve_ids if c and c.strip())
    firsts = [r.first_seen for r in rows if r.first_seen is not None]
    lasts = [r.last_seen for r in rows if r.last_seen is not None]
    return {
        "engagement_id": engagement_id,
        "key": key,
        "kind": kind,
        # The label comes from the highest-priority member so casing is stable.
        "label": group_identity(top)[2],
        "severity": top.severity,
        "severity_counts": severity_counts,
        "status_counts": status_counts,
        "finding_count": len(rows),
        "open_count": sum(1 for r in rows if r.status in ACTIVE_STATUSES),
        "host_count": len(hosts),
        "unassigned_count": sum(1 for r in rows if r.asset_id is None),
        "hosts": list(hosts.values())[:HOSTS_SHOWN],
        "ports": sorted(ports)[:PORTS_SHOWN],
        "port_count": len(ports),
        "cve_count": len(cves),
        "cves": sorted(cves)[:CVES_SHOWN],
        "max_risk": max(r.risk for r in rows),
        "max_cvss": _max(r.cvss for r in rows),
        "max_epss": _max(r.epss for r in rows),
        "kev": any(r.kev for r in rows),
        "exploit_validated": any(r.exploit_validated for r in rows),
        "first_seen": min(firsts) if firsts else None,
        "last_seen": max(lasts) if lasts else None,
        "top_finding_id": top.id,
        "members": [_member(r) for r in rows[:member_cap]],
        "members_truncated": len(rows) > member_cap,
    }


def _group_order(g: dict) -> tuple:
    return (
        0 if g["open_count"] else 1,
        -SEVERITY_RANK.get(g["severity"], 0),
        0 if g["kev"] else 1,
        0 if g["exploit_validated"] else 1,
        -g["max_risk"],
        -g["open_count"],
        -g["host_count"],
        g["label"].lower(),
        g["key"],
        str(g["engagement_id"]),
    )


def build_groups(rows: Iterable[GroupRow], *, member_cap: int = 100) -> list[dict]:
    """Group findings by identity and return the groups in priority order."""
    buckets: dict[tuple[uuid.UUID, str], tuple[str, list[GroupRow]]] = {}
    for row in rows:
        key, kind, _label = group_identity(row)
        buckets.setdefault((row.engagement_id, key), (kind, []))[1].append(row)
    groups = [_aggregate(engagement_id, key, kind, members, member_cap)
              for (engagement_id, key), (kind, members) in buckets.items()]
    groups.sort(key=_group_order)
    return groups

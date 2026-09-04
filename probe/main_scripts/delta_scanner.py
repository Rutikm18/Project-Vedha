"""
delta_scanner.py — scan-state comparison and continuous attack-surface monitoring.

Implements playbook 08 (Re-scan / Delta Assessment):

  CORE MODEL
  ----------
  A scan is a JSONL file where each line is a ScanResult record (scanner, target,
  port, proto, status, data, evidence, timestamp).

  The stable identity key for each finding is:
      (host_id, proto, port)
  where host_id is derived from the richest available identifier:
      MAC address (from ARP-harvest) > hostname (from SSH/banner) > IP address

  Two JSONL snapshots are compared; the diff classifies each change into:
      new_service      — (host, proto, port) appeared in current but not baseline
      service_gone     — appeared in baseline but not current (possible outage/fix)
      version_change   — same (host, proto, port), different service/version string
      state_change     — filtered ↔ open transition
      host_appeared    — a new host_id in current not seen in baseline
      host_gone        — a host_id in baseline missing from current

  USAGE (programmatic)
  --------------------
      from scanner.delta_scanner import DeltaEngine
      engine = DeltaEngine()
      baseline  = engine.load_jsonl("baseline_2026-01-01.jsonl")
      current   = engine.load_jsonl("scan_2026-02-01.jsonl")
      deltas    = engine.diff(baseline, current)
      for d in deltas:
          print(d)

  USAGE (CLI)
  -----------
      python -m scanner.delta_scanner baseline.jsonl current.jsonl
      python -m scanner.delta_scanner baseline.jsonl current.jsonl --output delta.jsonl
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .scanner_base import project_timestamp


# ── Data types ────────────────────────────────────────────────────────────────

@dataclass
class ScanRecord:
    """Normalised representation of one ScanResult JSONL line."""
    host_id: str        # stable identity: MAC > hostname > IP
    ip: str             # raw IP as scanned
    proto: str          # "tcp" | "udp"
    port: int
    status: str         # "open" | "filtered" | "error"
    scanner: str
    service: str        # best-effort service name from data/evidence
    version: str        # best-effort version string
    evidence: str
    timestamp: str
    raw: dict           # original parsed JSON record


@dataclass
class Delta:
    """One security-relevant change between two scans."""
    kind: str           # new_service | service_gone | version_change | state_change |
                        # host_appeared | host_gone
    host_id: str
    proto: str
    port: int
    baseline_status: str | None
    current_status: str | None
    baseline_service: str | None
    current_service: str | None
    baseline_version: str | None
    current_version: str | None
    severity_hint: str  # high | medium | low | info
    note: str

    def to_dict(self) -> dict:
        return asdict(self)


# ── Identity resolution ───────────────────────────────────────────────────────

def _stable_host_id(record: dict) -> str:
    """
    Derive a stable host identity from a raw scan record in priority order:
      1. MAC address  (from host_discovery/ARP data or SSH inventory)
      2. Hostname     (from ssh_inventory hostname, banner, etc.)
      3. IP address   (fallback — may be unstable under DHCP)
    """
    data = record.get("data") or {}

    # MAC from host_discovery ARP data
    mac = data.get("mac_address") or data.get("mac")
    if mac and mac != "00:00:00:00:00:00":
        return f"mac:{mac.lower().replace('-', ':')}"

    # Hostname from SSH inventory
    inv = data.get("inventory") or {}
    hostname = inv.get("hostname") or data.get("hostname") or ""
    if hostname and hostname not in ("localhost", ""):
        return f"host:{hostname.lower()}"

    # Hostname from banner grab
    banner = (record.get("evidence") or "")
    if "SSH" in banner or "OpenSSH" in banner:
        # banner may carry no hostname — skip
        pass

    # Fallback: IP
    return f"ip:{record.get('target', 'unknown')}"


def _extract_service(record: dict) -> str:
    """Best-effort service name from data dict or scanner name."""
    data = record.get("data") or {}
    for key in ("engine", "service", "service_guess", "banner_service"):
        if key in data:
            return str(data[key])
    # Infer from scanner name
    scanner = record.get("scanner", "")
    svc_map = {
        "port_scan": "", "db_scan": "database", "tls_scan": "tls",
        "snmp_scan": "snmp", "udp_scan": data.get("service", ""),
        "smb_scan": "smb", "ssh_inventory": "ssh",
        "mcp_ai_scan": "ai/mcp", "iot_scan": "iot", "web_scan": "http",
    }
    return svc_map.get(scanner, scanner)


def _extract_version(record: dict) -> str:
    """Best-effort version string."""
    data = record.get("data") or {}
    for key in ("server_version", "version", "sysdescr", "banner"):
        if key in data and data[key]:
            return str(data[key])[:120]
    inv = data.get("inventory") or {}
    for key in ("os_pretty_name", "kernel"):
        if key in inv:
            return str(inv[key])[:120]
    return ""


# ── JSONL loading and indexing ────────────────────────────────────────────────

SnapshotIndex = dict[tuple[str, str, int], ScanRecord]
"""key = (host_id, proto, port)"""


class DeltaEngine:
    """Load JSONL scan snapshots and compute security-relevant diffs."""

    def load_jsonl(self, path: str | Path) -> SnapshotIndex:
        """
        Parse a JSONL file of ScanResult records and return a SnapshotIndex.
        Lines that are not valid JSON or lack required fields are silently skipped.
        """
        index: SnapshotIndex = {}
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(f"Snapshot not found: {path}")
        with p.open() as fh:
            for lineno, line in enumerate(fh, 1):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if rec.get("status") in ("error", None):
                    continue
                target = rec.get("target", "")
                proto = rec.get("proto", "tcp")
                port = rec.get("port")
                if not target or port is None:
                    continue
                host_id = _stable_host_id(rec)
                key = (host_id, proto, int(port))
                sr = ScanRecord(
                    host_id=host_id,
                    ip=target,
                    proto=proto,
                    port=int(port),
                    status=rec.get("status", ""),
                    scanner=rec.get("scanner", ""),
                    service=_extract_service(rec),
                    version=_extract_version(rec),
                    evidence=rec.get("evidence") or "",
                    timestamp=rec.get("timestamp") or "",
                    raw=rec,
                )
                # Later record for same (host, port, proto) wins (most recent)
                index[key] = sr
        return index

    def diff(self, baseline: SnapshotIndex,
             current: SnapshotIndex) -> list[Delta]:
        """Compute security-relevant deltas between baseline and current snapshots."""
        deltas: list[Delta] = []
        baseline_hosts = {k[0] for k in baseline}
        current_hosts  = {k[0] for k in current}

        # Host-level changes
        for hid in current_hosts - baseline_hosts:
            deltas.append(Delta(
                kind="host_appeared", host_id=hid, proto="", port=0,
                baseline_status=None, current_status="seen",
                baseline_service=None, current_service=None,
                baseline_version=None, current_version=None,
                severity_hint="medium",
                note="New host in scope — verify it belongs here"))

        for hid in baseline_hosts - current_hosts:
            deltas.append(Delta(
                kind="host_gone", host_id=hid, proto="", port=0,
                baseline_status="seen", current_status=None,
                baseline_service=None, current_service=None,
                baseline_version=None, current_version=None,
                severity_hint="info",
                note="Host no longer responding — outage or decommissioned?"))

        # Port/service-level changes
        all_keys = set(baseline) | set(current)
        for key in all_keys:
            host_id, proto, port = key
            b = baseline.get(key)
            c = current.get(key)

            if b is None and c is not None:
                # New service
                hint = _new_service_severity(c)
                deltas.append(Delta(
                    kind="new_service", host_id=host_id, proto=proto, port=port,
                    baseline_status=None, current_status=c.status,
                    baseline_service=None, current_service=c.service,
                    baseline_version=None, current_version=c.version,
                    severity_hint=hint,
                    note=f"New {proto}/{port} ({c.service}) on {c.ip}"))

            elif b is not None and c is None:
                # Service disappeared
                deltas.append(Delta(
                    kind="service_gone", host_id=host_id, proto=proto, port=port,
                    baseline_status=b.status, current_status=None,
                    baseline_service=b.service, current_service=None,
                    baseline_version=b.version, current_version=None,
                    severity_hint="info",
                    note=f"{proto}/{port} ({b.service}) no longer open on {b.ip}"))

            elif b is not None and c is not None:
                # State change: filtered → open
                if b.status != c.status:
                    hint = "high" if c.status == "open" else "low"
                    deltas.append(Delta(
                        kind="state_change", host_id=host_id, proto=proto, port=port,
                        baseline_status=b.status, current_status=c.status,
                        baseline_service=b.service, current_service=c.service,
                        baseline_version=b.version, current_version=c.version,
                        severity_hint=hint,
                        note=f"{proto}/{port} changed {b.status}→{c.status} on {c.ip}"))

                # Version / service change
                elif _significant_version_change(b.version, c.version):
                    hint = "medium"
                    deltas.append(Delta(
                        kind="version_change", host_id=host_id, proto=proto, port=port,
                        baseline_status=b.status, current_status=c.status,
                        baseline_service=b.service, current_service=c.service,
                        baseline_version=b.version, current_version=c.version,
                        severity_hint=hint,
                        note=f"{proto}/{port} version changed on {c.ip}"))

        deltas.sort(key=lambda d: (
            {"high": 0, "medium": 1, "low": 2, "info": 3}.get(d.severity_hint, 9),
            d.host_id, d.port))
        return deltas

    # ── helpers ──────────────────────────────────────────────────────────────

    def summary(self, deltas: list[Delta]) -> dict:
        counts: dict[str, int] = {}
        for d in deltas:
            counts[d.kind] = counts.get(d.kind, 0) + 1
        high = sum(1 for d in deltas if d.severity_hint == "high")
        return {"total": len(deltas), "by_kind": counts, "high_severity": high}


def _new_service_severity(rec: ScanRecord) -> str:
    """Heuristic priority for a newly-detected service."""
    HIGH_PORTS = {22, 23, 25, 80, 443, 445, 3306, 3389, 5432, 6379, 8080, 8443, 9200, 27017}
    HIGH_SVCS  = {"smb", "rdp", "mysql", "postgresql", "redis", "mongodb",
                  "mssql", "oracle", "snmp", "database", "ai/mcp"}
    if rec.port in HIGH_PORTS or rec.service.lower() in HIGH_SVCS:
        return "high"
    if rec.status == "open" and rec.port < 1024:
        return "medium"
    return "low"


def _significant_version_change(old: str, new: str) -> bool:
    """True if version changed in a security-relevant way (not just whitespace)."""
    old_n = " ".join(old.split())
    new_n = " ".join(new.split())
    return bool(old_n and new_n and old_n != new_n)


# ── CLI ───────────────────────────────────────────────────────────────────────

def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(
        description="Compare two Vedha JSONL scan snapshots and report deltas.")
    parser.add_argument("baseline", help="Baseline JSONL scan file")
    parser.add_argument("current", help="Current JSONL scan file")
    parser.add_argument("-o", "--output", default=None,
                        help="Write delta records as JSONL to this file")
    parser.add_argument("--summary-only", action="store_true",
                        help="Print only the summary counts, not each delta")
    args = parser.parse_args()

    engine = DeltaEngine()
    try:
        baseline = engine.load_jsonl(args.baseline)
        current  = engine.load_jsonl(args.current)
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)

    deltas = engine.diff(baseline, current)
    summary = engine.summary(deltas)

    print(f"Baseline : {args.baseline} ({len(baseline)} records)")
    print(f"Current  : {args.current} ({len(current)} records)")
    print(f"Deltas   : {summary['total']} total, {summary['high_severity']} high-severity")
    for kind, n in sorted(summary["by_kind"].items()):
        print(f"  {kind:<20} {n}")

    if not args.summary_only:
        print()
        for d in deltas:
            sev = f"[{d.severity_hint.upper()}]"
            print(f"{sev:<8} {d.kind:<20} {d.host_id}  {d.proto}/{d.port}  {d.note}")

    if args.output:
        out = Path(args.output)
        ts = project_timestamp()
        with out.open("w") as fh:
            for d in deltas:
                rec = d.to_dict()
                rec["generated_at"] = ts
                fh.write(json.dumps(rec) + "\n")
        print(f"\nDelta JSONL written to {args.output}")


if __name__ == "__main__":
    main()

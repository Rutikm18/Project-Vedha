"""
ingest.py — stream-read scanner_module JSONL output, validate, assemble
per-host Assets.

SCOPE: this validates against scanner_module's ScanResult schema specifically
(scanner/target/timestamp/port/proto/status/data/evidence/error — see
scanner_module/scanner/scanner_base.py). Ingesting Vedha probe's different
result envelope shape (scan_type/engine/tool/ok/hosts|findings) would be a
separate, additive parser, not assumed here.

Malformed lines are quarantined to IngestResult.quarantined rather than
raised — a single truncated/corrupt line must never take down an entire
ingestion pass over what could be hundreds of thousands of records.
"""
from __future__ import annotations

import ipaddress
import json
from dataclasses import dataclass
from pathlib import Path

from models import Asset, Fact, SourceConfidence

# Scanners that read a host's OWN authoritative state via credentials
# (installed package lists, real OS/registry reads) rather than guessing
# from network-observable banners. This single classification is what lets
# Phase 1.4's matcher treat a credentialed package-version match as
# "confirmed" and a banner-version match as merely "suspected".
_AUTHORITATIVE_SCANNERS = {"ssh_inventory", "windows_inventory"}

REQUIRED_FIELDS = {"scanner", "target", "timestamp", "status"}

# Scanners whose `target` is NOT a host: it names the interface/segment the run
# swept, or the literal "auto" when none resolved. Their evidence is real and is
# counted as ingested, but it must never mint an Asset — doing so put a phantom
# host called "auto" into the inventory on every assessment and inflated host
# counts by one. Mirrors probe/agent/engine.py's _RUN_SCOPED_SCANNERS.
_RUN_SCOPED_SCANNERS = {"ipv6_discovery"}


@dataclass
class QuarantinedLine:
    source_file: str
    source_line: int
    raw: str
    reason: str


class IngestResult:
    def __init__(self) -> None:
        self.assets: dict[str, Asset] = {}
        self.quarantined: list[QuarantinedLine] = []
        # Accepted facts that describe the run rather than a host (see
        # _RUN_SCOPED_SCANNERS). Kept, not dropped: they count toward fact_count
        # so the ingest census still balances against what the probe submitted.
        self.run_scoped: list[Fact] = []
        self.fact_count = 0

    def get_or_create_asset(self, key: str) -> Asset:
        if key not in self.assets:
            self.assets[key] = Asset(ip=key, is_ip_keyed=_is_ip(key))
        return self.assets[key]


def _classify_confidence(scanner: str) -> SourceConfidence:
    return (SourceConfidence.authoritative if scanner in _AUTHORITATIVE_SCANNERS
            else SourceConfidence.inferred)


def _validate(record: dict) -> str | None:
    """Returns an error reason string if invalid, else None."""
    if not isinstance(record, dict):
        return "not a JSON object"
    missing = REQUIRED_FIELDS - record.keys()
    if missing:
        return f"missing required field(s): {sorted(missing)}"
    if not isinstance(record.get("target"), str) or not record["target"]:
        return "target must be a non-empty string"
    port = record.get("port")
    if port is not None and not isinstance(port, int):
        return "port must be an int or null"
    # `data` carries every scanner-specific field the rules read, and they read it
    # with .get(). A non-mapping here is not a degraded fact, it is one that makes
    # the whole CVE pass raise mid-batch and take every other host's findings down
    # with it. Reject it at the same gate as the rest, so it is quarantined and
    # counted rather than fatal.
    data = record.get("data")
    if data is not None and not isinstance(data, dict):
        return f"data must be an object or null (got {type(data).__name__})"
    return None


def _is_ip(target: str) -> bool:
    try:
        ipaddress.ip_address(target)
        return True
    except ValueError:
        return False


def _extract_aliases(scanner: str, data: dict) -> list[str]:
    """Real, verified hostname-alias sources in scanner_module's output —
    deliberately narrow. Not every scanner has a clean hostname field
    (passive_collector's device_hints is descriptive text, not a hostname,
    and is intentionally NOT treated as an alias here).
    """
    aliases: list[str] = []
    if scanner == "ssh_inventory":
        raw = (data.get("inventory") or {}).get("hostname")
        if raw:
            aliases.append(raw.strip())
    if scanner == "tls_scan":
        san = (data.get("certificate") or {}).get("san") or []
        aliases.extend(s for s in san if isinstance(s, str))
    if scanner == "host_discovery":
        # The discovery tier's PTR record and NetBIOS node-status name — both
        # answered by the target (or its authoritative resolver), not guessed.
        for key in ("hostname", "netbios_name"):
            raw = data.get(key)
            if isinstance(raw, str) and raw.strip():
                aliases.append(raw.strip())
    return aliases


def ingest_file(path: str | Path, result: IngestResult | None = None) -> IngestResult:
    """Stream-read one JSONL file, validating and assembling Assets as it goes.

    Pass an existing IngestResult to accumulate across multiple files (e.g.
    one per scanner from run_scan.py's --split-output) into one merged set
    of Assets keyed by target.
    """
    result = result if result is not None else IngestResult()
    path = Path(path)
    source_file = str(path)

    with path.open("r", encoding="utf-8") as fh:
        for lineno, raw_line in enumerate(fh, start=1):
            line = raw_line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                result.quarantined.append(QuarantinedLine(
                    source_file, lineno, line[:300], f"invalid JSON: {exc}"))
                continue

            err = _validate(record)
            if err:
                result.quarantined.append(QuarantinedLine(
                    source_file, lineno, line[:300], err))
                continue

            target = record["target"]
            data = record.get("data") or {}
            fact = Fact(
                scanner=record["scanner"], target=target,
                timestamp=record.get("timestamp", ""), port=record.get("port"),
                proto=record.get("proto"), status=record["status"], data=data,
                evidence=record.get("evidence"), error=record.get("error"),
                source_confidence=_classify_confidence(record["scanner"]),
                source_file=source_file, source_line=lineno,
            )
            # A run-scoped fact is evidence about the SCAN, not about a host at
            # `target`. Count it, keep it, but never let it mint an Asset.
            if record["scanner"] in _RUN_SCOPED_SCANNERS:
                result.run_scoped.append(fact)
                result.fact_count += 1
                continue

            # IP is the join key (per spec). A hostname-only target becomes
            # an asset keyed by that hostname string itself — this module
            # does not perform DNS resolution to merge it into some other
            # IP's asset; that would require live lookups this ingester
            # deliberately doesn't do. is_ip is recorded for downstream
            # consumers that want to treat the two cases differently.
            asset = result.get_or_create_asset(target)
            asset.add_fact(fact)
            for alias in _extract_aliases(record["scanner"], data):
                asset.add_alias(alias)
            result.fact_count += 1

    return result


def ingest_files(paths: list[str | Path]) -> IngestResult:
    result = IngestResult()
    for p in paths:
        ingest_file(p, result)
    return result

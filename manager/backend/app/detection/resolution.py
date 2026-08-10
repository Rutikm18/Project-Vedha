"""
resolution.py — coverage-gated auto-resolution of findings.

Split into a PURE core (host_of / build_coverage / decide_resolution) that is
fully unit-testable without a database, and a thin async applier
(evaluate_resolutions) that walks the engagement's still-open findings and
applies the pure decision. Wired into engine_bridge.create_findings_from_facts.

Safety rule: absence of a finding is only meaningful if we PROVED we looked.
A host counts as covered this run only if a *completed* scanner produced a fact
about it; a degraded/failed/skipped scanner is not proof.
"""
from __future__ import annotations


def host_of(target: str) -> str:
    """IP/host part of a probe target: '10.0.0.5:443' -> '10.0.0.5'.
    Mirrors finding_translator._resolve_asset's host extraction."""
    if not target:
        return ""
    return target.split(":", 1)[0] if target.count(":") == 1 else target


def build_coverage(scanner_runs: list[dict] | None, facts: list[dict] | None) -> dict:
    """What this run PROVABLY re-observed. An asset is covered only if a
    completed scanner produced a fact about it. Fail-closed: no scanner_runs
    (older probe) → empty coverage → nothing auto-resolves."""
    scanner_runs = scanner_runs or []
    facts = facts or []
    completed = {sr.get("id") for sr in scanner_runs if sr.get("status") == "completed"}
    degraded = {
        sr.get("id") for sr in scanner_runs
        if sr.get("status") in ("degraded", "failed", "skipped")
    }
    assets = {
        host_of(f.get("target", "")) for f in facts
        if f.get("scanner") in completed and host_of(f.get("target", ""))
    }
    return {
        "assets": sorted(a for a in assets if a),
        "scanners_completed": sorted(c for c in completed if c),
        "scanners_degraded": sorted(d for d in degraded if d),
    }

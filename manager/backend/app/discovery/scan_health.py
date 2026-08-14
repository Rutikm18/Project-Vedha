"""
scan_health.py — turn the probe's per-host scan completeness/health metrics into
a single engagement-visible verdict.

The probe's PortScanner emits a `scan_summary` fact per host (completeness +
self-health), surfaced at the top of the result as `result["scan_metrics"]`.
Before this bridge the manager persisted those metrics but never READ them, so a
firewall-truncated or fd-exhausted scan (which manufactures false NEGATIVES —
open services reported as unseen) looked identical to a genuinely clean host.

This module computes an honest "was this scan trustworthy?" summary. Pure logic —
no DB — so it is unit-testable in isolation.
"""
from __future__ import annotations


def scan_health_summary(result: dict | None) -> dict:
    """Aggregate result['scan_metrics'] into a coverage/health verdict.

      degraded   — a host hit local resource limits (fd/buffer exhaustion), which
                   manufactures false negatives; the scan is untrustworthy there.
      incomplete — a host's requested ports were not all classified (firewall
                   truncation, timeouts) — real exposure may be under-reported.
      healthy    — metrics were collected and none were degraded or incomplete.

    A result with no port metrics (host_discovery, passive, etc.) is neither
    healthy nor degraded — there is simply nothing to attest, and `should_warn`
    is False so no coverage finding is raised.
    """
    metrics = [m for m in ((result or {}).get("scan_metrics") or []) if isinstance(m, dict)]

    hosts_degraded = sum(1 for m in metrics if m.get("health") == "degraded")
    hosts_incomplete = sum(
        1 for m in metrics if m.get("complete") is False or int(m.get("missing") or 0) > 0
    )
    missing_total = sum(int(m.get("missing") or 0) for m in metrics)
    resource_errors_total = sum(int(m.get("local_resource_errors") or 0) for m in metrics)

    degraded = hosts_degraded > 0
    incomplete = hosts_incomplete > 0

    reasons: list[str] = []
    if degraded:
        reasons.append(
            f"{hosts_degraded} host(s) hit local resource limits during scanning "
            f"({resource_errors_total} error(s)) — open services may be under-reported"
        )
    if incomplete:
        reasons.append(
            f"{hosts_incomplete} host(s) had incomplete port coverage "
            f"({missing_total} requested port(s) never verified)"
        )

    return {
        "hosts_measured": len(metrics),
        "hosts_degraded": hosts_degraded,
        "hosts_incomplete": hosts_incomplete,
        "missing_ports_total": missing_total,
        "local_resource_errors_total": resource_errors_total,
        "degraded": degraded,
        "incomplete": incomplete,
        "healthy": bool(metrics) and not degraded and not incomplete,
        "should_warn": degraded or incomplete,
        "reason": "; ".join(reasons) or "scan coverage complete and healthy",
    }

"""
scan_health.py — turn the probe's per-host scan completeness/health metrics into
a single engagement-visible verdict.

Either port scanner emits a `scan_summary` fact per host (completeness +
self-health), surfaced at the top of the result as `result["scan_metrics"]`.
Before this bridge the manager persisted those metrics but never READ them, so a
firewall-truncated or fd-exhausted scan (which manufactures false NEGATIVES —
open services reported as unseen) looked identical to a genuinely clean host.

This module computes an honest "was this scan trustworthy?" summary. Pure logic —
no DB — so it is unit-testable in isolation.

ONE HOST CAN CARRY SEVERAL SUMMARIES
-------------------------------------
A two-phase deep scan emits two scan_summary facts per host (a fast first pass,
then a port tail over the rest of the range — disjoint port sets), each stamped
with the same `target` (`agent/engine.py::_scan_metrics_from_facts`). Counting
every summary as its own host would double hosts_measured and anything derived
from it, so summaries that carry a target are grouped by it before counting.
Entries without one (older probes) fall back to counting each entry as its
own host.

A host's gap counts differently depending on WHY it exists: `missing`/
`complete is False` from a summary that also says `budget_exhausted` is the
operator's own time-budget choice ending a wide sweep early, not a coverage
failure — it lands in `hosts_budget_truncated`, not `hosts_incomplete`. The same
kind of gap in a summary that does NOT report a budget reason is real,
unexplained loss and still counts as incomplete.
"""
from __future__ import annotations


def _has_gap(metric: dict) -> bool:
    return metric.get("complete") is False or int(metric.get("missing") or 0) > 0


def _host_verdict(entries: list[dict]) -> tuple[bool, bool, bool]:
    """(degraded, incomplete, budget_truncated) for one host's summaries."""
    degraded = any(m.get("health") == "degraded" for m in entries)
    non_budget_gap = any(_has_gap(m) and not m.get("budget_exhausted") for m in entries)
    budget_gap = any(_has_gap(m) and m.get("budget_exhausted") for m in entries)
    incomplete = non_budget_gap
    budget_truncated = budget_gap and not non_budget_gap
    return degraded, incomplete, budget_truncated


def scan_health_summary(result: dict | None) -> dict:
    """Aggregate result['scan_metrics'] into a coverage/health verdict.

      degraded          — a host hit local resource limits (fd/buffer
                          exhaustion), which manufactures false negatives; the
                          scan is untrustworthy there.
      incomplete         — a host's requested ports were not all classified for
                          a reason other than its own time budget (firewall
                          truncation, timeouts) — real exposure may be
                          under-reported.
      budget_truncated   — a host's only gap is a tail that ran out of its time
                          budget: an operator-chosen tradeoff, reported
                          truthfully, but NOT coverage degradation.
      healthy            — metrics were collected and none were degraded or
                          incomplete.

    A result with no port metrics (host_discovery, passive, etc.) is neither
    healthy nor degraded — there is simply nothing to attest, and `should_warn`
    is False so no coverage finding is raised.
    """
    metrics = [m for m in ((result or {}).get("scan_metrics") or []) if isinstance(m, dict)]

    targeted = [m for m in metrics if m.get("target")]
    untargeted = [m for m in metrics if not m.get("target")]

    by_host: dict[str, list[dict]] = {}
    for m in targeted:
        by_host.setdefault(m["target"], []).append(m)

    hosts_degraded = 0
    hosts_incomplete = 0
    hosts_budget_truncated = 0

    for entries in by_host.values():
        degraded, incomplete, budget_truncated = _host_verdict(entries)
        hosts_degraded += int(degraded)
        hosts_incomplete += int(incomplete)
        hosts_budget_truncated += int(budget_truncated)

    # Legacy per-entry counting for probes that never stamped a target.
    for m in untargeted:
        if m.get("health") == "degraded":
            hosts_degraded += 1
        if _has_gap(m):
            hosts_incomplete += 1

    hosts_measured = len(by_host) + len(untargeted)
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
    if hosts_budget_truncated:
        reasons.append(
            f"{hosts_budget_truncated} host(s) reached their time budget before "
            f"the full port range; unreached ports are recorded as not scanned"
        )

    return {
        "hosts_measured": hosts_measured,
        "hosts_degraded": hosts_degraded,
        "hosts_incomplete": hosts_incomplete,
        "hosts_budget_truncated": hosts_budget_truncated,
        "missing_ports_total": missing_total,
        "local_resource_errors_total": resource_errors_total,
        "degraded": degraded,
        "incomplete": incomplete,
        "healthy": bool(metrics) and not degraded and not incomplete,
        "should_warn": degraded or incomplete,
        "reason": "; ".join(reasons) or "scan coverage complete and healthy",
    }

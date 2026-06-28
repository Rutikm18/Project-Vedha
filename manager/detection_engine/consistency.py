"""
consistency.py — Phase 5: N-run consistency & reporting.

"A single scan is an anecdote." Network scans are noisy — wifi/LAN churn and
timeout flakiness mean a host (or a finding) can appear in one run and vanish
in the next. detection_engine itself is DETERMINISTIC (the same facts always
produce the same findings, with the same deterministic finding_id — see
models.make_finding_id), so all cross-run variance lives in the SCAN INPUTS,
not in detection. That determinism is what lets us track "is this the same
finding?" across N runs at all.

This module aggregates N runs (N scans of the same scope against the same
pinned DB snapshot) and reports, per finding:
  - appearance rate  k/N  + a Wilson 95% confidence interval
  - stable vs intermittent classification
  - the failure-mode taxonomy of the runs themselves (why a run produced
    nothing for a host: scanner_error / no_data / timeout / out_of_scope —
    first-class states, DISTINCT from "confirmed not vulnerable").

Output core is deterministic. An AI prose-narrative layer is deliberately
NOT built here (it's optional and the lowest-value/lowest-urgency AI use;
the deterministic report is the product of record).
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

from models import Finding


def wilson_ci(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    """Wilson score interval for a binomial proportion k/n, as percentages.
    Chosen over the naive normal approximation because it stays inside
    [0,100] and is well-behaved at the extremes (k=0, k=N, small N) — the
    exact regime an appearance-rate over ~20-30 runs lives in.
    """
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    z2 = z * z
    denom = 1 + z2 / n
    center = (p + z2 / (2 * n)) / denom
    margin = (z * math.sqrt(p * (1 - p) / n + z2 / (4 * n * n))) / denom
    return (round(max(0.0, center - margin) * 100, 1),
            round(min(1.0, center + margin) * 100, 1))


@dataclass
class FindingConsistency:
    finding_id: str
    cve_id: str
    asset_ip: str
    appearances: int
    runs: int
    exemplar: Finding              # a representative Finding (latest seen) for its metadata

    @property
    def rate(self) -> float:
        return self.appearances / self.runs if self.runs else 0.0

    @property
    def ci(self) -> tuple[float, float]:
        return wilson_ci(self.appearances, self.runs)

    @property
    def classification(self) -> str:
        # Stable: present in (almost) every run. Intermittent: comes and goes.
        # The thresholds are deliberately conservative — a finding seen in
        # < 90% of runs is flagged intermittent so an operator treats its
        # variance as a signal (real churn or tool flakiness), not noise.
        if self.appearances == self.runs:
            return "stable"
        if self.rate >= 0.9:
            return "mostly-stable"
        return "intermittent"


# Run-level failure taxonomy — why a run yielded no data for a target. These
# are first-class outcomes, NOT "not vulnerable": a timeout tells you nothing
# about the host's security, only about that probe attempt.
FAILURE_MODES = ("scanner_error", "timeout", "no_data", "out_of_scope")


@dataclass
class ConsistencyReport:
    runs: int
    findings: list[FindingConsistency]
    run_failures: list[dict] = field(default_factory=list)  # per-run failure tallies

    @property
    def stable(self) -> list[FindingConsistency]:
        return [f for f in self.findings if f.classification == "stable"]

    @property
    def intermittent(self) -> list[FindingConsistency]:
        return [f for f in self.findings if f.classification == "intermittent"]


def aggregate(run_findings: list[list[Finding]],
              run_failures: list[dict] | None = None) -> ConsistencyReport:
    """run_findings: one list of Findings per run (N runs). Aggregated by
    the deterministic finding_id so 'the same finding' is tracked across
    runs even though each run was a fresh scan.
    """
    n = len(run_findings)
    counts: dict[str, int] = {}
    exemplar: dict[str, Finding] = {}
    for findings in run_findings:
        seen_this_run: set[str] = set()
        for f in findings:
            if f.finding_id in seen_this_run:
                continue          # dedup within a run (count presence, not multiplicity)
            seen_this_run.add(f.finding_id)
            counts[f.finding_id] = counts.get(f.finding_id, 0) + 1
            exemplar[f.finding_id] = f

    out = [
        FindingConsistency(
            finding_id=fid, cve_id=exemplar[fid].cve_id,
            asset_ip=exemplar[fid].asset_ip, appearances=k, runs=n,
            exemplar=exemplar[fid])
        for fid, k in counts.items()
    ]
    # Highest-appearance first, then by CVE for stable ordering.
    out.sort(key=lambda c: (-c.appearances, c.cve_id))
    return ConsistencyReport(runs=n, findings=out, run_failures=run_failures or [])


def format_line(fc: FindingConsistency) -> str:
    """The spec's reporting line, e.g.:
    'Host 10.0.0.5 — CVE-2021-41773 in 27/30 runs (CI [78.0,98.0]),
     confirmed, conf 95, KEV, [stable]'.
    """
    e = fc.exemplar
    lo, hi = fc.ci
    bits = [f"{e.state.value}"]
    if e.confidence is not None:
        bits.append(f"conf {e.confidence}")
    if e.kev:
        bits.append("KEV")
    if e.priority:
        bits.append(e.priority)
    return (f"Host {fc.asset_ip} — {fc.cve_id} in {fc.appearances}/{fc.runs} runs "
            f"(CI [{lo},{hi}]), {', '.join(bits)}  [{fc.classification}]")

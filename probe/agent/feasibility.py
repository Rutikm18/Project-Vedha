"""feasibility.py — will this job finish before the runtime ceiling?

WHY THIS EXISTS
---------------
A job whose port stage cannot possibly complete looks, for the entire two-hour
ceiling, exactly like one that can. Then it returns `partial` / `degraded` with
no statement of what was impossible from the first second. The operator learns
nothing except that it took two hours.

The arithmetic is not subtle, which is the point — it just was not being done:

    probes       = hosts x ports
    floor        = probes / rate

THE MODEL IS A FLOOR, DELIBERATELY
----------------------------------
It covers the PORT STAGE ONLY, at one probe per port, and ignores everything
that runs after it (banner, OS, deep branches, UDP) plus everything that can
multiply it (retries, the cleanup pass). Real runs are always slower. That
asymmetry is what makes the verdict trustworthy: if the FLOOR does not fit,
no amount of downstream tuning rescues the job.

WHY RATE IS NOT PER HOST
------------------------
scanner_base.RateLimiter lives on the scanner INSTANCE, and workflow_engine
builds ONE PortScanner for the whole port stage. Every host in the stage draws
from the same token stream, so `rate` is the aggregate for the stage, not a
per-host allowance. Doubling the host count doubles the wall clock.

ADVISORY ONLY. as_check() returns pass/warn, never fail — admission control
(refusing the job at enqueue) is a separate decision with its own policy.
"""
from __future__ import annotations

from dataclasses import dataclass

from agent.doctor import Check

# A floor past this fraction of the ceiling will not survive contact with
# reality: retries, the cleanup pass, and every stage after the port sweep all
# add on top of it. Calling that "fits" would be a promise the job cannot keep.
TIGHT_FRACTION = 0.5

# PortScanner's cleanup-pass defaults (see port_scanner.PortScanner.__init__).
# Mirrored here so the estimate reflects what the scanner will actually do.
DEFAULT_REPROBE_RETRIES = 3
DEFAULT_REPROBE_RATE = 40.0


@dataclass(frozen=True)
class Estimate:
    hosts: int
    ports: int
    probes: int
    rate: float
    ceiling_seconds: float
    #: One probe per port at `rate` — the optimistic port-stage floor.
    floor_seconds: float
    #: Every port retried to exhaustion (a wholly silent target).
    retry_seconds: float
    #: The cleanup pass if every port stays ambiguous. Not bounded by
    #: max_host_seconds today — this term is the evidence for that defect.
    reprobe_seconds: float
    #: How many of `hosts` the ceiling actually has room for.
    reachable_hosts: int
    #: The rate that would make the whole scope fit. Often above the clamp.
    required_rate: float
    verdict: str                      # "fits" | "tight" | "cannot_finish"
    #: What `ports` covers. "full_sweep": every port the job sweeps.
    #: "first_pass": only a phased sweep's first pass. Its tail runs inside
    #: whatever time budget is left, so a `fits` here promises nothing about
    #: the remaining ports, which may end up reported not_scanned.
    scope: str = "full_sweep"


def estimate(
    *,
    hosts: int,
    ports: int,
    rate: float,
    ceiling_seconds: float,
    retries: int = 1,
    reprobe_retries: int = DEFAULT_REPROBE_RETRIES,
    reprobe_rate: float = DEFAULT_REPROBE_RATE,
) -> Estimate | None:
    """Project the port stage against the runtime ceiling.

    Returns None on degenerate input rather than inventing a number: a job with
    no hosts, no ports, no rate or no ceiling has nothing to predict, and a
    fabricated estimate is worse than none.
    """
    if hosts <= 0 or ports <= 0 or rate <= 0 or ceiling_seconds <= 0:
        return None

    probes = hosts * ports
    floor = probes / rate
    retry = probes * (retries + 1) / rate
    reprobe = (probes * (reprobe_retries + 1) / reprobe_rate
               if reprobe_rate > 0 else 0.0)

    reachable = min(hosts, int(ceiling_seconds * rate / ports))
    required = probes / ceiling_seconds

    if floor > ceiling_seconds:
        verdict = "cannot_finish"
    elif floor > ceiling_seconds * TIGHT_FRACTION:
        verdict = "tight"
    else:
        verdict = "fits"

    return Estimate(
        hosts=hosts, ports=ports, probes=probes, rate=rate,
        ceiling_seconds=ceiling_seconds,
        floor_seconds=floor, retry_seconds=retry, reprobe_seconds=reprobe,
        reachable_hosts=reachable, required_rate=required, verdict=verdict,
    )


def _hms(seconds: float) -> str:
    """Compact duration — hours matter more than precision at this scale."""
    if seconds < 90:
        return f"{seconds:.0f}s"
    if seconds < 5400:
        return f"{seconds / 60:.0f}m"
    return f"{seconds / 3600:.1f}h"


def describe(est: Estimate | None) -> str:
    """One line for the job log."""
    if est is None:
        return "Runtime estimate: not applicable"
    return (
        f"Runtime estimate: {est.hosts} host(s) x {est.ports} port(s) "
        f"= {est.probes:,} probes at {est.rate:g} pps "
        f"→ floor {_hms(est.floor_seconds)} vs ceiling "
        f"{_hms(est.ceiling_seconds)} [{est.verdict}]"
    )


def as_check(est: Estimate | None) -> Check:
    """Advisory Check, so this composes with the kernel-limit preflight report."""
    if est is None:
        return Check("runtime", "pass", "no runtime estimate for this job")

    detail = (
        f"{est.probes:,} probes at {est.rate:g} pps → floor "
        f"{_hms(est.floor_seconds)} vs ceiling {_hms(est.ceiling_seconds)} "
        f"({est.verdict})"
    )

    if est.verdict == "fits":
        return Check("runtime", "pass", detail)

    # Both remaining verdicts get the same two actionable numbers: how much of
    # the scope fits as configured, and the rate that would fit all of it.
    remediation = (
        f"only ~{est.reachable_hosts} of {est.hosts} host(s) fit in the "
        f"ceiling at this envelope; finishing all of them needs "
        f"~{est.required_rate:,.0f} pps. Narrow the port profile, split the "
        f"scope, or raise PROBE_MAX_JOB_SECONDS after capacity review"
    )
    return Check("runtime", "warn", detail, remediation)


def as_run_stats(est: Estimate | None) -> dict | None:
    """The prediction, shaped for the job result.

    Recorded beside the ACTUAL elapsed time so the model is falsifiable. An
    estimate nobody can check against the outcome is decoration; one sitting
    next to the real number either earns trust or gets corrected.
    """
    if est is None:
        return None
    return {
        "hosts": est.hosts,
        "ports": est.ports,
        "probes": est.probes,
        "rate": est.rate,
        "floor_seconds": round(est.floor_seconds, 1),
        "retry_seconds": round(est.retry_seconds, 1),
        "reprobe_seconds": round(est.reprobe_seconds, 1),
        "ceiling_seconds": round(est.ceiling_seconds, 1),
        "reachable_hosts": est.reachable_hosts,
        "required_rate": round(est.required_rate, 1),
        "verdict": est.verdict,
        "scope": est.scope,
    }


def port_count_for(
    profile: str,
    service_filter: set[str] | None,
    port_override: list[int] | None,
) -> int:
    """How many TCP ports this job will actually sweep.

    Delegates to workflow_engine._port_candidates rather than re-deriving the
    catalog: an estimate computed from a DIFFERENT port set than the engine
    sweeps is not an estimate, it is a second bug. Imported lazily so this
    module stays cheap and free of a circular import.
    """
    from workflow.workflow_engine import _port_candidates
    return len(_port_candidates(profile, service_filter,
                                port_override=port_override))


def admission_port_count(
    profile: str,
    service_filter: set[str] | None,
    port_override: list[int] | None,
    first_pass_ports: list[int] | None,
    *,
    phased: bool,
) -> int:
    """Ports a job MUST sweep to finish — what admission sizes it by.

    A phased sweep (a first pass exists and stages run after the port scan)
    must finish only that first pass; the remaining ports are a tail budgeted
    per host that truncates to not_scanned by design. Computes the same split
    run_engagement makes, so admission and execution agree on the port set.
    """
    from workflow.workflow_engine import _port_candidates
    ports = set(_port_candidates(profile, service_filter, port_override=port_override))
    if not (phased and first_pass_ports):
        return len(ports)
    first = set(_port_candidates(profile, service_filter,
                                 port_override=list(first_pass_ports))) & ports
    return len(first) if first and len(first) < len(ports) else len(ports)

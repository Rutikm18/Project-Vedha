"""
host_health.py — detect a target that was proven alive and has since gone away,
stop working on it, and say so instead of reporting a half-scanned host as clean.

WHY THIS IS NOT JUST "COUNT THE FAILURES"
A deep branch that finds nothing is normal — most branches don't apply to most
hosts. Even a branch that errors on every port is normal when the service isn't
there. And from a failed connect() a powered-off host is INDISTINGUISHABLE from a
firewalled one: both are silence. So counting failures alone would abort scans of
perfectly healthy, well-defended hosts.

The only defensible evidence that a host went away is that the same liveness
probe which proved it alive at Gate 2 no longer gets an answer. That is what this
monitor does: failures raise suspicion, an ACTIVE re-check decides.

The re-check has a second job that matters as much as the first. When it says the
host IS still answering, we have learned something specific and useful — the
branches are failing because we are being filtered, throttled, or blocked by an
IPS, not because the target is down. That is recorded as `flaky`, and the scan
CONTINUES. Reporting "offline" there would be a lie that sends an operator to
check a machine that never went down.

BLAST RADIUS IS ONE HOST
A ten-host job where one machine reboots must still deliver the other nine.
Aborting the job would throw away completed work and is the wrong response to a
single flaky target, so this only ever skips the remaining stages of the host
that failed its re-check.

THE SAFETY PROPERTY
The point is not to save scan time. It is that a host we stopped scanning must
never be presented as a host with nothing wrong. Every verdict emits a fact with
`scan_complete: false` naming the stages that never ran, so downstream
"no findings" cannot be read as "clean".
"""

from __future__ import annotations

import asyncio
import logging
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone

from scanner.scanner_base import ScanResult

LOG = logging.getLogger("host_health")

# Statuses that prove the host answered us. `closed` counts: a TCP RST is the
# host's own stack replying, which is positive proof of life even though the
# port is shut. Treating it as a failure was the obvious trap here.
#
# "open|filtered" is deliberately absent even though it begins with "open": it is
# the UDP no-reply verdict — we sent and heard nothing back. Matching it as
# contact (by splitting on the pipe) made a host that had already gone away look
# like it was still answering.
_CONTACT_STATUSES = frozenset({"open", "closed", "observed"})

# Transport-level failures that are consistent with a host having gone away.
# `filtered` is included because a dropped packet and a dead host look the same
# from here — which is exactly why a strike alone never decides anything.
_SILENCE_STATUSES = frozenset({"unreachable", "filtered", "error", "open|filtered"})

_SILENCE_ERROR_CODES = frozenset({
    "connection_failed", "scanner_timeout", "host_unreachable",
    "network_unreachable", "resource_exhausted",
})

VERDICT_OFFLINE = "offline"
VERDICT_FLAKY = "flaky"

DETECTED_BY_HEARTBEAT = "heartbeat"
DETECTED_BY_STRIKES = "branch_silence"


def _env_int(name: str, default: int, minimum: int = 1) -> int:
    try:
        return max(minimum, int(os.environ.get(name, str(default))))
    except (TypeError, ValueError):
        return default


def _strike_threshold() -> int:
    """Consecutive silent components before we spend a re-check on this host."""
    return _env_int("PROBE_OFFLINE_STRIKES", 2)


def _heartbeat_interval() -> float:
    """Seconds between liveness heartbeats while a host is being scanned."""
    try:
        return max(1.0, float(os.environ.get("PROBE_HEARTBEAT_SECONDS", "10")))
    except (TypeError, ValueError):
        return 10.0


def _heartbeat_misses() -> int:
    """Consecutive missed heartbeats before a host is declared offline."""
    return _env_int("PROBE_HEARTBEAT_MISSES", 2)


@dataclass
class _HostState:
    strikes: int = 0
    verdict: str | None = None
    silent_components: list[str] = field(default_factory=list)
    completed_components: list[str] = field(default_factory=list)
    skipped_components: list[str] = field(default_factory=list)
    last_contact_component: str | None = None
    detected_at: str | None = None
    detected_by: str | None = None
    detection_reason: str | None = None


class HostHealthMonitor:
    """Tracks per-host reachability across the deep-scan stages.

    `liveness_probe` is an async callable(host) -> bool, injected so the monitor
    is testable without a network and so the engine keeps ownership of how a
    liveness check is actually configured.
    """

    def __init__(self, liveness_probe, *, strike_threshold: int | None = None):
        self._probe = liveness_probe
        self._threshold = strike_threshold if strike_threshold is not None else _strike_threshold()
        self._hosts: dict[str, _HostState] = {}
        self._facts: list[ScanResult] = []

    # ── observation ──────────────────────────────────────────────────────────

    def _state(self, host: str) -> _HostState:
        return self._hosts.setdefault(host, _HostState())

    @staticmethod
    def _is_silence(results: list[ScanResult]) -> bool:
        """True when a component ran and got nothing back that proves life.

        An empty result list is NOT silence: a branch can legitimately decline to
        run (no candidate ports), and that says nothing about the host.
        """
        if not results:
            return False
        for r in results:
            if (getattr(r, "status", "") or "") in _CONTACT_STATUSES:
                return False
        for r in results:
            if (getattr(r, "status", "") or "") in _SILENCE_STATUSES:
                return True
            code = ((getattr(r, "data", None) or {}).get("error_code"))
            if code in _SILENCE_ERROR_CODES:
                return True
        return False

    def observe(self, host: str, component: str, results: list[ScanResult]) -> None:
        """Feed one component's results in.

        Only pass components that had POSITIVE REASON TO EXPECT A REPLY — a branch
        gated on a port this scan already confirmed open. Datagram probes (SNMP,
        IPMI, the UDP sweep) must never be fed here: getting nothing back is their
        normal result on almost every host, so counting that as evidence of death
        would put every healthy target one strike from a false alarm.

        Contact resets the strike count — suspicion must be CONSECUTIVE, or a host
        with many inapplicable branches would accumulate its way to a verdict
        across an entirely healthy scan.
        """
        state = self._state(host)
        if state.verdict == VERDICT_OFFLINE:
            return
        if not results:
            return
        if self._is_silence(results):
            state.strikes += 1
            if component not in state.silent_components:
                state.silent_components.append(component)
        else:
            state.strikes = 0
            state.last_contact_component = component
            if component not in state.completed_components:
                state.completed_components.append(component)

    # ── verdict ──────────────────────────────────────────────────────────────

    def suspect(self, host: str) -> bool:
        state = self._state(host)
        return state.verdict is None and state.strikes >= self._threshold

    def is_offline(self, host: str) -> bool:
        return self._state(host).verdict == VERDICT_OFFLINE

    def note_skipped(self, host: str, component: str) -> None:
        state = self._state(host)
        if component not in state.skipped_components:
            state.skipped_components.append(component)

    async def confirm(self, host: str) -> str | None:
        """Re-probe a suspected host and record the verdict.

        Returns VERDICT_OFFLINE, VERDICT_FLAKY, or None when no check was due.
        Never raises: a failing health check must not take down the scan it is
        supposed to be protecting — an errored probe is treated as inconclusive
        and the scan continues.
        """
        state = self._state(host)
        if not self.suspect(host):
            return None
        try:
            alive = await self._probe(host)
        except Exception as exc:
            LOG.warning("liveness re-check for %s failed to run (%s: %s) — "
                        "treating as inconclusive and continuing",
                        host, type(exc).__name__, exc)
            state.strikes = 0
            return None

        now = datetime.now(timezone.utc).isoformat()
        if alive:
            # Answering, but its services are not. Being blocked is a different
            # problem from being down, and the operator needs the difference.
            state.strikes = 0
            state.verdict = VERDICT_FLAKY
            LOG.info("%s: %d silent component(s) but the host still answers — "
                     "treating as filtered/throttled, NOT offline", host, len(state.silent_components))
            self._facts.append(ScanResult(
                "host_liveness", host, status="observed",
                method="liveness_recheck",
                data={
                    "went_offline": False,
                    "verdict": VERDICT_FLAKY,
                    "recheck": "alive",
                    "silent_components": list(state.silent_components),
                    "scan_complete": True,
                },
                evidence=(f"{len(state.silent_components)} component(s) got no reply but the "
                          f"host still answers a liveness probe — likely filtered, throttled, "
                          f"or rate-limited rather than offline"),
            ))
            state.verdict = None      # allow re-suspicion later in the scan
            return VERDICT_FLAKY

        self._mark_offline(host, DETECTED_BY_STRIKES,
                           f"liveness re-check failed after "
                           f"{len(state.silent_components)} silent component(s)")
        return VERDICT_OFFLINE

    def _mark_offline(self, host: str, detected_by: str, why: str) -> None:
        state = self._state(host)
        if state.verdict == VERDICT_OFFLINE:
            return
        state.verdict = VERDICT_OFFLINE
        state.detected_at = datetime.now(timezone.utc).isoformat()
        state.detected_by = detected_by
        state.detection_reason = why
        LOG.warning("%s WENT OFFLINE mid-scan (%s) — %s; skipping its remaining stages",
                    host, detected_by, why)

    async def watch(self, host: str, *, interval: float | None = None,
                    misses: int | None = None) -> None:
        """Heartbeat a host for as long as it is being scanned.

        This, not the strike counter, is the primary detector — and the reason is
        empirical. The TCP branches finish in MILLISECONDS; the datagram ones
        (SNMP, IPMI, the UDP sweep) own tens of seconds of every host's scan. So
        inferring death from branch failures can only ever notice a host that dies
        inside a vanishingly small window, and is blind for the long tail where
        most of the scan actually happens. A killed lab container went completely
        undetected until this existed.

        Cheap enough to leave on: one liveness probe per host per interval, and
        only while that host has work in flight.

        Runs until cancelled by the scan loop. Never raises into its parent.
        """
        interval = interval if interval is not None else _heartbeat_interval()
        misses = misses if misses is not None else _heartbeat_misses()
        consecutive = 0
        try:
            while True:
                await asyncio.sleep(interval)
                if self.is_offline(host):
                    return
                try:
                    alive = await self._probe(host)
                except Exception as exc:
                    # An unusable probe is inconclusive, not proof of death.
                    LOG.debug("heartbeat for %s could not run (%s)", host, exc)
                    continue
                if alive:
                    consecutive = 0
                    continue
                consecutive += 1
                LOG.info("heartbeat missed for %s (%d/%d)", host, consecutive, misses)
                if consecutive >= misses:
                    self._mark_offline(
                        host, DETECTED_BY_HEARTBEAT,
                        f"{consecutive} consecutive liveness heartbeat(s) went unanswered")
                    return
        except asyncio.CancelledError:
            return

    # ── output ───────────────────────────────────────────────────────────────

    def finalize(self) -> list[ScanResult]:
        """Emit one fact per offline host, plus any flaky notes gathered."""
        facts = list(self._facts)
        for host, state in self._hosts.items():
            if state.verdict != VERDICT_OFFLINE:
                continue
            facts.append(ScanResult(
                "host_liveness", host, status="unreachable",
                method="liveness_recheck",
                reason="target_went_offline",
                # Setting `error` is what promotes this from a quiet fact into an
                # entry in the run's issues[] — and therefore onto the operator's
                # screen. It also marks the run degraded, which is the honest
                # outcome: this host's results are incomplete, and a run that
                # reports "completed" would be claiming otherwise.
                error=f"target_went_offline: {state.detection_reason}",
                data={
                    "went_offline": True,
                    "verdict": VERDICT_OFFLINE,
                    "recheck": "no_reply",
                    "detected_at": state.detected_at,
                    "detected_by": state.detected_by,
                    "detection_reason": state.detection_reason,
                    "silent_components": list(state.silent_components),
                    "completed_components": list(state.completed_components),
                    "skipped_components": list(state.skipped_components),
                    # The safety property: downstream must not read the absence
                    # of findings on this host as evidence that it is clean.
                    "scan_complete": False,
                    "error_code": "target_went_offline",
                    "retryable": True,
                    "remediation": (
                        "The host stopped answering during the scan and a liveness re-check "
                        "confirmed it. Verify the host is powered on and reachable from the "
                        "probe's segment, then re-run — its results are incomplete."
                    ),
                },
                evidence=(
                    f"host went offline mid-scan: {state.detection_reason}; "
                    f"{len(state.skipped_components)} stage(s) were skipped"
                ),
            ))
        return facts

    def offline_hosts(self) -> list[str]:
        return [h for h, s in self._hosts.items() if s.verdict == VERDICT_OFFLINE]

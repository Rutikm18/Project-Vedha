#!/usr/bin/env python3
"""
adaptive_timeout.py — per-host RTT-adaptive probe timeout (spec Phase 7).

A single static timeout is wrong in both directions: too short on a slow WAN host
(its OPEN ports get mislabeled filtered — a scanner-manufactured false negative)
and needlessly long on a fast LAN host (wasted wall time on silence). This tracks
a smoothed round-trip time and its variance (Jacobson/Karels, as TCP's RTO does)
and derives `SRTT + 4*RTTVAR`, clamped to a sane band.

Pure + deterministic: feed it RTTs from successful connects / ICMP / host
discovery, ask it for a timeout. No network, no state beyond the estimate.
"""
from __future__ import annotations


class AdaptiveTimeout:
    _ALPHA = 0.125   # SRTT smoothing (1/8), as RFC 6298
    _BETA = 0.25     # RTTVAR smoothing (1/4)

    def __init__(self, base: float, minimum: float, maximum: float):
        if not (minimum <= base <= maximum):
            raise ValueError("require minimum <= base <= maximum")
        self.base = base
        self.minimum = minimum
        self.maximum = maximum
        self.srtt: float | None = None
        self.rttvar: float | None = None
        self.samples = 0

    def observe(self, rtt: float | None) -> None:
        """Fold one round-trip sample (seconds) into the estimate. Ignores
        missing/negative samples so a bad reading never corrupts the timer."""
        if rtt is None or rtt < 0:
            return
        if self.srtt is None:
            self.srtt = rtt
            self.rttvar = rtt / 2
        else:
            self.rttvar = (1 - self._BETA) * self.rttvar + self._BETA * abs(self.srtt - rtt)
            self.srtt = (1 - self._ALPHA) * self.srtt + self._ALPHA * rtt
        self.samples += 1

    def timeout(self) -> float:
        """Current timeout: base until we have a sample, then SRTT + 4*RTTVAR
        clamped to [minimum, maximum]."""
        if self.srtt is None:
            return self.base
        est = self.srtt + 4 * self.rttvar
        return max(self.minimum, min(self.maximum, est))


def from_rtts(rtts, base: float = 2.0, minimum: float = 0.3,
              maximum: float = 8.0) -> AdaptiveTimeout:
    """Convenience: build an estimator and fold in a sequence of RTT samples."""
    est = AdaptiveTimeout(base, minimum, maximum)
    for r in rtts:
        est.observe(r)
    return est

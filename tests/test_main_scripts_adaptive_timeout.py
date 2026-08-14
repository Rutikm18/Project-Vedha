"""
test_main_scripts_adaptive_timeout.py — Phase 7: per-host adaptive probe timeout.

Pure SRTT/RTTVAR estimator: base until sampled, then SRTT+4*RTTVAR clamped; fast
LAN → short timeout, slow WAN → long (capped). No network.
"""
from __future__ import annotations

import pytest

from main_scripts.adaptive_timeout import AdaptiveTimeout, from_rtts


def test_no_samples_returns_base():
    assert AdaptiveTimeout(base=2.0, minimum=0.3, maximum=8.0).timeout() == 2.0


def test_first_sample_sets_srtt_and_timeout():
    est = AdaptiveTimeout(2.0, 0.3, 8.0)
    est.observe(0.05)                       # 50 ms
    # srtt=0.05, rttvar=0.025 -> 0.05 + 4*0.025 = 0.15, clamped up to minimum 0.3
    assert est.timeout() == pytest.approx(0.3)


def test_fast_lan_gets_short_timeout_slow_wan_gets_long():
    lan = from_rtts([0.002, 0.0022, 0.0019], base=2.0, minimum=0.05, maximum=8.0)
    wan = from_rtts([1.5, 1.6, 1.4], base=2.0, minimum=0.05, maximum=8.0)
    assert lan.timeout() < wan.timeout()
    assert lan.timeout() <= 0.2             # sub-LAN, tight
    assert wan.timeout() >= 1.5             # slow host is NOT treated as fast


def test_timeout_is_clamped_to_max():
    est = from_rtts([20.0, 20.0, 20.0], base=2.0, minimum=0.3, maximum=8.0)
    assert est.timeout() == 8.0


def test_observe_ignores_bad_samples():
    est = AdaptiveTimeout(2.0, 0.3, 8.0)
    est.observe(None); est.observe(-1.0)
    assert est.samples == 0 and est.timeout() == 2.0


def test_estimate_converges_on_stable_rtt():
    est = from_rtts([0.5] * 20, base=2.0, minimum=0.05, maximum=8.0)
    # variance collapses -> timeout approaches SRTT (~0.5)
    assert est.timeout() == pytest.approx(0.5, abs=0.05)


def test_invalid_band_rejected():
    with pytest.raises(ValueError):
        AdaptiveTimeout(base=0.1, minimum=0.3, maximum=8.0)

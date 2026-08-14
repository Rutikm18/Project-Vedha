"""
test_exposure.py — the probe exposure_matrix → Service verdict + severity bump.

Guards the reachability-aware risk path: an internet-reachable service escalates
one rung; internal-only / ambiguous / not-exposed never inflate risk.
"""
from __future__ import annotations

from app.discovery.exposure import escalate_for_exposure, service_exposure
from app.models.enums import FindingSeverity


def test_service_exposure_flattens_per_port_verdicts():
    result = {
        "scan_type": "exposure_matrix",
        "exposure": [
            {"ip": "203.0.113.5", "ports": {
                "tcp/443": {"exposure": "external"},
                "tcp/445": {"exposure": "internal_only"},
            }},
            {"ip": "10.0.0.7", "ports": {"udp/161": {"exposure": "not_exposed"}}},
        ],
    }
    m = service_exposure(result)
    assert m[("203.0.113.5", "tcp", 443)] == "external"
    assert m[("203.0.113.5", "tcp", 445)] == "internal_only"
    assert m[("10.0.0.7", "udp", 161)] == "not_exposed"


def test_service_exposure_ignores_malformed_and_non_exposure():
    assert service_exposure({"scan_type": "discovery"}) == {}
    assert service_exposure(None) == {}
    weird = {"exposure": ["nope", {"ip": "x"}, {"ip": "y", "ports": {"bad": {"exposure": "external"}}}]}
    assert service_exposure(weird) == {}   # "bad" has no proto/port separator


def test_external_escalates_one_rung():
    assert escalate_for_exposure(FindingSeverity.medium, "external") == FindingSeverity.high
    assert escalate_for_exposure(FindingSeverity.low, "external") == FindingSeverity.medium
    assert escalate_for_exposure(FindingSeverity.info, "external") == FindingSeverity.low


def test_critical_stays_critical():
    assert escalate_for_exposure(FindingSeverity.critical, "external") == FindingSeverity.critical


def test_non_external_never_escalates():
    for exposure in ("internal_only", "ambiguous", "not_exposed", None, "unknown"):
        assert escalate_for_exposure(FindingSeverity.medium, exposure) == FindingSeverity.medium

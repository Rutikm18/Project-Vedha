"""
test_vantage_fusion.py — fleet-level reconciliation of exposure_matrix across probes.

Guards the core promise: an OPEN port from an external vantage is `external` even
when the ingesting probe is internal; vantages are never averaged or overwritten.
"""
from __future__ import annotations

from app.detection.vantage_fusion import (
    fuse_exposure_results,
    fused_service_exposure,
)


def _probe(ip, ports):
    """Build a one-target probe exposure result. `ports` maps 'proto/port' →
    {vantage: status}."""
    return {"exposure": [{
        "ip": ip,
        "ports": {k: {"by_vantage": v} for k, v in ports.items()},
    }]}


def test_external_vantage_open_makes_port_external():
    external = _probe("203.0.113.5", {"tcp/443": {"internet-edge": "open"}})
    internal = _probe("203.0.113.5", {"tcp/443": {"lan-probe": "closed"},
                                      "tcp/445": {"lan-probe": "open"}})
    fused = fuse_exposure_results([external, internal])["203.0.113.5"]
    assert fused["ports"]["tcp/443"]["exposure"] == "external"
    assert 443 in fused["externally_exposed"]
    assert fused["ports"]["tcp/445"]["exposure"] == "internal_only"
    assert 445 in fused["internal_only"]


def test_internal_only_when_no_external_probe_sees_open():
    a = _probe("10.0.0.7", {"tcp/445": {"lan-a": "open"}})
    b = _probe("10.0.0.7", {"tcp/445": {"lan-b": "closed"}})
    fused = fuse_exposure_results([a, b])["10.0.0.7"]
    assert fused["ports"]["tcp/445"]["exposure"] == "internal_only"
    assert fused["externally_exposed"] == []


def test_internal_open_does_not_imply_external():
    # The whole point: an internal OPEN never becomes 'external'.
    internal = _probe("10.0.0.9", {"tcp/3389": {"corp-lan": "open"}})
    external = _probe("10.0.0.9", {"tcp/3389": {"internet": "filtered"}})
    fused = fuse_exposure_results([internal, external])["10.0.0.9"]
    assert fused["ports"]["tcp/3389"]["exposure"] == "internal_only"


def test_ambiguous_when_only_open_filtered():
    a = _probe("10.0.0.5", {"udp/161": {"lan": "open|filtered"}})
    fused = fuse_exposure_results([a])["10.0.0.5"]
    assert fused["ports"]["udp/161"]["exposure"] == "ambiguous"


def test_not_exposed_when_closed_everywhere():
    a = _probe("10.0.0.5", {"tcp/22": {"lan": "closed"}})
    b = _probe("10.0.0.5", {"tcp/22": {"internet": "filtered"}})
    fused = fuse_exposure_results([a, b])["10.0.0.5"]
    assert fused["ports"]["tcp/22"]["exposure"] == "not_exposed"


def test_declared_external_vantage_without_hint_name():
    # A probe named 'probe-42' is external only because config says so.
    p = _probe("203.0.113.9", {"tcp/443": {"probe-42": "open"}})
    fused = fuse_exposure_results([p], external_vantages={"probe-42"})["203.0.113.9"]
    assert fused["ports"]["tcp/443"]["exposure"] == "external"
    assert "probe-42" in fused["external_vantages"]


def test_single_probe_matches_its_own_verdict():
    p = _probe("203.0.113.1", {"tcp/443": {"edge-node": "open"}})
    fused = fuse_exposure_results([p])["203.0.113.1"]
    assert fused["ports"]["tcp/443"]["exposure"] == "external"   # 'edge' hint
    assert fused["vantages"] == ["edge-node"]


def test_fused_service_exposure_is_keyed_for_service_rows():
    external = _probe("203.0.113.5", {"tcp/443": {"internet-edge": "open"}})
    internal = _probe("203.0.113.5", {"tcp/445": {"lan": "open"}})
    m = fused_service_exposure([external, internal])
    assert m[("203.0.113.5", "tcp", 443)] == "external"
    assert m[("203.0.113.5", "tcp", 445)] == "internal_only"


def test_empty_and_malformed_are_safe():
    assert fuse_exposure_results([]) == {}
    assert fuse_exposure_results([{"exposure": ["nope", {"ip": "x"}]}]) == {}
    assert fused_service_exposure(None) == {}


def test_reconstruct_probe_results_from_persisted_facts():
    # The ingest adapter rebuilds one {"exposure": [...]} per agent from the
    # persisted exposure_matrix facts, then fuses across agents.
    from app.detection.exposure_fusion_service import _results_from_scan_rows

    ext_facts = [{"scanner": "exposure_matrix", "target": "203.0.113.5",
                  "data": {"ports": {"tcp/443": {"by_vantage": {"internet-edge": "open"}}}}}]
    int_facts = [{"scanner": "exposure_matrix", "target": "203.0.113.5",
                  "data": {"ports": {"tcp/443": {"by_vantage": {"lan": "closed"}},
                                     "tcp/445": {"by_vantage": {"lan": "open"}}}}},
                 {"scanner": "host_discovery", "target": "203.0.113.5", "data": {}}]  # ignored
    rows = [("agent-ext", ext_facts), ("agent-int", int_facts)]

    results = _results_from_scan_rows(rows)
    assert len(results) == 2   # one per agent
    fused = fused_service_exposure(results)
    assert fused[("203.0.113.5", "tcp", 443)] == "external"
    assert fused[("203.0.113.5", "tcp", 445)] == "internal_only"

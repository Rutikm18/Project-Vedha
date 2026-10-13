"""P3 — credential-reuse and NTLM-relay movement edges, with precondition checks
and honest labels (FM-08/09).

Signing-off alone is never a path (that is the FM-09 false positive); a relay edge
appears only when a distinct coercion source shares the target's subnet, and it is
always labelled `assumed`. Shared default credentials are reported as INFORMATION
(no movement edge, H2). Reflection to the same host is blocked.
"""
from __future__ import annotations

import uuid
from types import SimpleNamespace as NS

from app.detection.credentials import derive_credential_edges
from app.graph.analyzer import PathAnalyzer
from app.graph.builder import GraphBuilder


def _asset(aid, ip, crit="medium", role_detail=None, exposed=False):
    return NS(id=aid, ip_address=ip, hostname=f"h-{aid}", criticality=crit, device_role=None,
              role_detail=role_detail, role_confidence=None, os=None, environment=None,
              tags={"internet_exposed": True} if exposed else {}, site_id=None, last_seen=None)


def _svc(sid, aid, port, exposure=None):
    return NS(id=sid, asset_id=aid, service_name="svc", port=port, exposure=exposure)


def _finding(fid, aid, rule, mitre="T1557.001", state="confirmed", conf=90, sev="high", **ev):
    return NS(id=fid, asset_id=aid, title=rule, cvss_score=None, cvss_vector=None,
              epss_score=None, severity=sev, status="open", exploitable=False,
              exploit_validated=False, mitre_techniques=[mitre], verification_confidence=conf,
              verification_state=state,
              evidence={"rule_id": rule, "state": state, "confidence": conf, **ev}, last_seen=None)


# ── the derivation ──────────────────────────────────────────────────────────

def test_relay_edge_needs_a_distinct_coercion_source_on_the_same_subnet():
    assets = [_asset("a1", "10.0.0.5"), _asset("a2", "10.0.0.9")]
    services = [_svc("s1", "a1", 445), _svc("s2", "a2", 445)]
    findings = [_finding("f1", "a2", "POSTURE-SMB-SIGNING-OFF")]  # a2 is the relay target
    out = derive_credential_edges(assets, findings, services)
    edges = out["relay_edges"]
    assert len(edges) == 1
    assert edges[0]["src"] == "a1" and edges[0]["dst"] == "a2"
    assert edges[0]["basis"] == "assumed"
    assert edges[0]["preconditions"]["target_signing_off"] is True


def test_signing_off_alone_is_not_a_relay_path():
    # One lonely signing-off host with no other SMB host: no coercion source, no edge.
    assets = [_asset("a1", "10.0.0.5")]
    services = [_svc("s1", "a1", 445)]
    findings = [_finding("f1", "a1", "POSTURE-SMB-SIGNING-OFF")]
    assert derive_credential_edges(assets, findings, services)["relay_edges"] == []


def test_no_relay_reflection_to_the_same_host():
    assets = [_asset("a1", "10.0.0.5")]
    services = [_svc("s1", "a1", 445)]
    findings = [_finding("f1", "a1", "POSTURE-SMB-SIGNING-OFF")]
    edges = derive_credential_edges(assets, findings, services)["relay_edges"]
    assert all(e["src"] != e["dst"] for e in edges)


def test_relay_stays_within_a_subnet():
    assets = [_asset("a1", "10.0.0.5"), _asset("a2", "10.9.9.9")]  # different /24
    services = [_svc("s1", "a1", 445), _svc("s2", "a2", 445)]
    findings = [_finding("f1", "a2", "POSTURE-SMB-SIGNING-OFF")]
    assert derive_credential_edges(assets, findings, services)["relay_edges"] == []


def test_relay_to_a_domain_controller_scores_higher():
    assets = [_asset("a1", "10.0.0.5"), _asset("dc", "10.0.0.9", role_detail="domain_controller")]
    services = [_svc("s1", "a1", 445), _svc("s2", "dc", 445)]
    findings = [_finding("f1", "dc", "POSTURE-SMB-SIGNING-OFF")]
    edge = derive_credential_edges(assets, findings, services)["relay_edges"][0]
    assert edge["preconditions"]["target_is_dc"] is True
    assert edge["confidence"] > 0.4


def test_shared_default_snmp_community_is_reported_as_information():
    assets = [_asset("a1", "10.0.0.5"), _asset("a2", "10.0.0.6"), _asset("a3", "10.0.0.7")]
    findings = [
        _finding("f1", "a1", "POSTURE-SNMP-DEFAULT-COMMUNITY", "T1078", community="public"),
        _finding("f2", "a2", "POSTURE-SNMP-DEFAULT-COMMUNITY", "T1078", community="public"),
        _finding("f3", "a3", "POSTURE-SNMP-DEFAULT-COMMUNITY", "T1078", community="private"),
    ]
    out = derive_credential_edges(assets, findings, [])
    shared = out["shared_default_credentials"]
    assert len(shared) == 1                     # only the shared 'public', not the lone 'private'
    assert shared[0]["basis"] == "possible"
    assert sorted(shared[0]["reused_on"]) == ["a1", "a2"]
    # H2: information only — no movement edge is produced from a shared default
    assert "credentials" not in out


def test_a_credential_on_one_host_is_not_shared():
    assets = [_asset("a1", "10.0.0.5")]
    findings = [_finding("f1", "a1", "POSTURE-SNMP-DEFAULT-COMMUNITY", "T1078", community="public")]
    assert derive_credential_edges(assets, findings, [])["shared_default_credentials"] == []


# ── wired through the graph ─────────────────────────────────────────────────

def test_relay_edge_lets_a_path_reach_a_signing_off_crown_jewel():
    eid = uuid.uuid4()
    # entry: an exposed foothold; dc: a signing-off crown jewel with no exploit of its own.
    assets = [_asset("a1", "10.0.0.5", exposed=True),
              _asset("dc", "10.0.0.9", crit="critical", role_detail="domain_controller")]
    services = [_svc("s1", "a1", 445, exposure="external"), _svc("s2", "dc", 445)]
    findings = [_finding("f1", "a1", "POSTURE-DB-UNAUTHENTICATED-ACCESS", "T1213"),
                _finding("f2", "dc", "POSTURE-SMB-SIGNING-OFF")]
    b = GraphBuilder()
    b.assemble(eid, assets, services, findings, scope_cidrs=["10.0.0.0/24"])
    analyzer = PathAnalyzer(b.graph)
    paths = analyzer.find_paths_to_target("dc")
    assert paths, "a relay edge should let the path reach the signing-off DC"
    techniques = {e["technique"] for p in paths for e in p["edges"]}
    assert "RELAY" in techniques


def test_without_a_relay_a_signing_off_only_host_is_not_compromisable():
    eid = uuid.uuid4()
    # The target has ONLY signing-off (credential_access, non-control) and there is no
    # other SMB host to coerce, so nothing owns it.
    assets = [_asset("a1", "10.0.0.5", exposed=True),
              _asset("a2", "10.0.0.9", crit="critical")]
    services = [_svc("s1", "a1", 80, exposure="external")]
    findings = [_finding("f1", "a1", "POSTURE-DB-UNAUTHENTICATED-ACCESS", "T1213"),
                _finding("f2", "a2", "POSTURE-SMB-SIGNING-OFF")]
    b = GraphBuilder()
    b.assemble(eid, assets, services, findings, scope_cidrs=["10.0.0.0/24"])
    analyzer = PathAnalyzer(b.graph)
    assert analyzer.find_paths_to_target("a2") == []


def test_shared_default_credentials_create_no_graph_edge(monkeypatch=None):
    # H2 end to end: two printers on the same default SNMP community and nothing else
    # must not let a path cross between them.
    import uuid as _uuid
    eid = _uuid.uuid4()
    assets = [_asset("a1", "10.0.0.5", exposed=True), _asset("a2", "10.0.0.9", crit="critical")]
    services = []
    findings = [
        _finding("f1", "a1", "POSTURE-SNMP-DEFAULT-COMMUNITY", "T1078", community="public"),
        _finding("f2", "a2", "POSTURE-SNMP-DEFAULT-COMMUNITY", "T1078", community="public"),
    ]
    b = GraphBuilder()
    g = b.assemble(eid, assets, services, findings, scope_cidrs=["10.0.0.0/24"])
    # the cluster is recorded for the report …
    assert len(g.graph.get("shared_default_credentials") or []) == 1
    # … but there is no CREDENTIAL_REUSE edge and no route
    assert not any(d.get("type") == "CREDENTIAL_REUSE" for _, _, d in g.edges(data=True))
    assert PathAnalyzer(g).find_paths_to_target("a2") == []


def test_relay_is_a_hub_not_a_mesh_on_a_flat_windows_subnet():
    # H3: on a subnet where every host is both an SMB host and a signing-off target,
    # the graph must stay O(n), not O(n^2).
    import uuid as _uuid
    n = 40
    assets = [_asset(f"h{i}", f"10.0.0.{i + 1}") for i in range(n)]
    assets[0].tags = {"internet_exposed": True}
    assets[-1] = _asset(f"h{n - 1}", f"10.0.0.{n}", crit="critical")
    services = [_svc(f"s{i}", f"h{i}", 445) for i in range(n)]
    findings = [_finding("g0", "h0", "POSTURE-DB-UNAUTHENTICATED-ACCESS", "T1213")] + \
               [_finding(f"f{i}", f"h{i}", "POSTURE-SMB-SIGNING-OFF") for i in range(n)]
    g = GraphBuilder().assemble(_uuid.uuid4(), assets, services, findings, scope_cidrs=["10.0.0.0/24"])
    hubs = [x for x, d in g.nodes(data=True) if d.get("type") == "RelayHub"]
    relay_edges = sum(1 for _, _, d in g.edges(data=True)
                      if d.get("type") in ("RELAY_FROM", "RELAY_TO"))
    assert len(hubs) == 1
    assert relay_edges <= 2 * n + 2          # O(n), far below n*n = 1600
    # and a relay route to the signing-off crown jewel still exists
    paths = PathAnalyzer(g).find_paths_to_target(f"h{n - 1}")
    assert paths and any(e["technique"] == "RELAY" for e in paths[0]["edges"])

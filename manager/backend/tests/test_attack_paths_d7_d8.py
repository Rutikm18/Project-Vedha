"""D7 — completed/paused engagements are demoted (not hidden) in the dashboard order.
D8 — the analyzer's min_fix_set names crown jewels that are exposed outright."""
from __future__ import annotations

import uuid
from types import SimpleNamespace as NS

from app.graph.analyzer import PathAnalyzer
from app.graph.builder import GraphBuilder
from app.graph.overview import is_demoted, row_sort_key


# ── D7 ──────────────────────────────────────────────────────────────────────

def _row(name, state, status, reachable=0, top_risk=0.0):
    return {"name": name, "state": state, "status": status,
            "jewels_reachable": reachable, "top_risk": top_risk}


def test_completed_and_paused_are_demoted_but_not_hidden():
    assert is_demoted(_row("x", "reachable", "completed"))
    assert is_demoted(_row("x", "reachable", "paused"))
    assert not is_demoted(_row("x", "reachable", "active"))
    assert not is_demoted(_row("x", "reachable", "running"))


def test_an_active_engagement_outranks_a_completed_one_even_at_a_lower_state():
    active_unreachable = _row("a", "unreachable", "active")
    completed_exposed = _row("b", "exposed", "completed", reachable=1, top_risk=90)
    ordered = sorted([completed_exposed, active_unreachable], key=row_sort_key)
    assert ordered[0]["name"] == "a"       # active first, though its state is lower
    assert ordered[1]["name"] == "b"       # the completed exposed one is shown, just demoted


def test_within_active_the_usual_state_order_holds():
    exposed = _row("e", "exposed", "active", reachable=1)
    reachable = _row("r", "reachable", "active", reachable=1)
    unreachable = _row("u", "unreachable", "active")
    ordered = [r["name"] for r in sorted([unreachable, reachable, exposed], key=row_sort_key)]
    assert ordered == ["e", "r", "u"]


# ── D8 ──────────────────────────────────────────────────────────────────────

def _asset(aid, ip, crit="medium", exposed=False):
    return NS(id=aid, ip_address=ip, hostname=f"h-{aid}", criticality=crit, device_role=None,
              role_detail=None, role_confidence=None, os=None, environment=None,
              tags={"internet_exposed": True} if exposed else {}, site_id=None, last_seen=None)


def _svc(sid, aid, port, exposure=None):
    return NS(id=sid, asset_id=aid, service_name="svc", port=port, exposure=exposure)


def _finding(fid, aid, rule, mitre="T1213"):
    return NS(id=fid, asset_id=aid, title=rule, cvss_score=None, cvss_vector=None, epss_score=None,
              severity="critical", status="open", exploitable=False, exploit_validated=False,
              mitre_techniques=[mitre], verification_confidence=90, verification_state="confirmed",
              evidence={"rule_id": rule, "state": "confirmed", "confidence": 90}, last_seen=None)


def test_min_fix_set_names_an_exposed_crown_jewel():
    eid = uuid.uuid4()
    # The crown jewel is itself an exploitable internet-exposed host.
    assets = [_asset("jewel", "10.0.0.9", crit="critical", exposed=True)]
    services = [_svc("s1", "jewel", 5432, exposure="external")]
    findings = [_finding("f1", "jewel", "POSTURE-DB-UNAUTHENTICATED-ACCESS")]
    b = GraphBuilder()
    b.assemble(eid, assets, services, findings, scope_cidrs=["10.0.0.0/24"])
    analyzer = PathAnalyzer(b.graph)
    choke = analyzer.choke_analysis(["jewel"])
    assert choke["min_fix_set"]["exposed_targets"] == ["jewel"]
    # and the target itself is flagged exposed_directly, as before
    assert choke["targets"][0]["exposed_directly"] is True


def test_min_fix_set_has_no_exposed_targets_when_none_are_exposed():
    eid = uuid.uuid4()
    assets = [_asset("a1", "10.0.0.5", exposed=True), _asset("jewel", "10.0.0.9", crit="critical")]
    services = [_svc("s1", "a1", 5432, exposure="external")]
    findings = [_finding("f1", "a1", "POSTURE-DB-UNAUTHENTICATED-ACCESS"),
                _finding("f2", "jewel", "POSTURE-VNC-NO-AUTH", "T1021.005")]
    b = GraphBuilder()
    b.assemble(eid, assets, services, findings, scope_cidrs=["10.0.0.0/24"])
    analyzer = PathAnalyzer(b.graph)
    choke = analyzer.choke_analysis(["jewel"])
    assert choke["min_fix_set"]["exposed_targets"] == []

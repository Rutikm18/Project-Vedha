"""P2 — posture / misconfiguration findings become attacker steps via the
capability map, independent of the `exploitable` flag (FM-03/12/19).

Before P2 only AD-set `exploitable` findings created steps, so an ordinary
network-VA engagement produced zero paths and `no_exploitable_steps`.
"""
from __future__ import annotations

import uuid
from types import SimpleNamespace as NS

from app.detection.capability_map import (
    CONTROL_CAPABILITIES, capability_for, grants_control, step_likelihood_for_capability,
)
from app.graph.analyzer import PathAnalyzer
from app.graph.builder import GraphBuilder


def _asset(aid, ip, crit="medium", exposed=False):
    return NS(id=aid, ip_address=ip, hostname=f"h-{aid}", criticality=crit, device_role=None,
              role_detail=None, role_confidence=None, os=None, environment=None,
              tags={"internet_exposed": True} if exposed else {}, site_id=None, last_seen=None)


def _svc(sid, aid, port, exposure=None):
    return NS(id=sid, asset_id=aid, service_name="svc", port=port, exposure=exposure)


def _finding(fid, aid, rule, mitre="T1213", state="confirmed", conf=90, sev="high",
             category=None, exploitable=False):
    return NS(id=fid, asset_id=aid, title=rule, cvss_score=None, cvss_vector=None,
              epss_score=None, severity=sev, status="open", exploitable=exploitable,
              exploit_validated=False, mitre_techniques=[mitre], verification_confidence=conf,
              verification_state=state,
              evidence={"rule_id": rule, "state": state, "confidence": conf, "category": category},
              last_seen=None)


# ── the map itself ────────────────────────────────────────────────────────────

def test_rule_ids_map_to_their_intended_capability():
    assert capability_for("POSTURE-DB-UNAUTHENTICATED-ACCESS") == "foothold"
    # SMB signing off is a relay precondition (P3), not a control step by itself (FM-09)
    assert capability_for("POSTURE-SMB-SIGNING-OFF") == "credential_access"
    assert capability_for("POSTURE-RDP-EXPOSED") == "lateral"
    assert capability_for("POSTURE-SNMP-DEFAULT-COMMUNITY") == "credential_access"
    assert capability_for("POSTURE-LDAP-ANONYMOUS-BIND") == "recon"
    assert capability_for("CORR-NTLM-RELAY-PATH") == "lateral"


def test_a_dos_amplifier_is_not_an_attack_step():
    # T1498 network DoS is explicitly not a path step.
    assert capability_for("POSTURE-UDP-AMPLIFIER", "amplification", "T1498.002") is None


def test_unknown_rule_falls_back_through_category_then_mitre_then_none():
    assert capability_for("NEW-RULE", "default_credentials") == "foothold"
    assert capability_for("NEW-RULE", "weak_crypto", "T1040") == "credential_access"
    assert capability_for("NEW-RULE", "weird", "T9999") is None


def test_only_foothold_lateral_privesc_grant_control():
    assert grants_control("foothold") and grants_control("lateral") and grants_control("priv_esc")
    assert not grants_control("credential_access")
    assert not grants_control("recon")
    assert not grants_control(None)
    assert CONTROL_CAPABILITIES == frozenset({"foothold", "lateral", "priv_esc"})


def test_recon_and_credential_access_have_zero_control_likelihood():
    assert step_likelihood_for_capability({"capability": "recon", "state": "confirmed"}) == 0.0
    assert step_likelihood_for_capability({"capability": "credential_access", "state": "confirmed"}) == 0.0


def test_confirmed_step_outranks_suspected_and_kev_raises_it():
    base = {"capability": "foothold", "confidence": 100}
    confirmed = step_likelihood_for_capability({**base, "state": "confirmed"})
    suspected = step_likelihood_for_capability({**base, "state": "suspected"})
    kev = step_likelihood_for_capability({**base, "state": "confirmed", "kev": True})
    assert suspected < confirmed <= kev


def test_lower_confidence_lowers_the_step():
    hi = step_likelihood_for_capability({"capability": "foothold", "state": "confirmed", "confidence": 95})
    lo = step_likelihood_for_capability({"capability": "foothold", "state": "confirmed", "confidence": 30})
    assert lo < hi


# ── wired through the graph ─────────────────────────────────────────────────────

def _two_host_posture_graph():
    eid = uuid.uuid4()
    entry, jewel = "a1", "a2"
    assets = [_asset(entry, "10.0.0.5", exposed=True), _asset(jewel, "10.0.0.9", crit="critical")]
    services = [_svc("s1", entry, 5432, exposure="external")]
    findings = [_finding("f1", entry, "POSTURE-DB-UNAUTHENTICATED-ACCESS", "T1213"),
                _finding("f2", jewel, "POSTURE-VNC-NO-AUTH", "T1021.005")]
    b = GraphBuilder()
    b.assemble(eid, assets, services, findings, scope_cidrs=["10.0.0.0/24"])
    return PathAnalyzer(b.graph), entry, jewel


def test_posture_findings_alone_produce_a_path():
    analyzer, _entry, jewel = _two_host_posture_graph()
    paths = analyzer.find_paths_to_target(jewel)
    assert len(paths) == 1
    step = paths[0]["edges"][-1]
    assert step["capability"] == "foothold"
    assert step["exploited"] is True


def test_an_exposed_host_with_only_a_recon_finding_is_not_an_entry_point():
    eid = uuid.uuid4()
    assets = [_asset("a1", "10.0.0.5", exposed=True), _asset("a2", "10.0.0.9", crit="critical")]
    services = [_svc("s1", "a1", 389, exposure="external")]
    # anonymous LDAP is recon only: reachable, but it does not own the host
    findings = [_finding("f1", "a1", "POSTURE-LDAP-ANONYMOUS-BIND", "T1087.002"),
                _finding("f2", "a2", "POSTURE-VNC-NO-AUTH", "T1021.005")]
    b = GraphBuilder()
    b.assemble(eid, assets, services, findings, scope_cidrs=["10.0.0.0/24"])
    analyzer = PathAnalyzer(b.graph)
    assert analyzer.find_paths_to_target("a2") == []
    diag = analyzer.diagnose(["a2"])
    assert any(r["code"] == "entry_points_not_compromisable" for r in diag["reasons"])


def test_diagnose_no_longer_says_no_exploitable_steps_when_a_foothold_exists():
    analyzer, _entry, jewel = _two_host_posture_graph()
    diag = analyzer.diagnose([jewel])
    codes = {r["code"] for r in diag["reasons"]}
    assert "no_exploitable_steps" not in codes
    assert diag["compromising_findings"] == 2
    assert diag["exploitable_findings"] == 0

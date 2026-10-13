"""P2 — posture / misconfiguration findings become attacker steps via the
capability map, independent of the `exploitable` flag (FM-03/12/19).

Before P2 only AD-set `exploitable` findings created steps, so an ordinary
network-VA engagement produced zero paths and `no_exploitable_steps`.
"""
from __future__ import annotations

import uuid
from types import SimpleNamespace as NS

from app.detection.capability_map import (
    CONTROL_CAPABILITIES, capability_for, classify, grants_control, step_likelihood_for_capability,
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
    # SMB signing off (and its composite) is a relay precondition (P3), not a control step (FM-09)
    assert capability_for("POSTURE-SMB-SIGNING-OFF") == "credential_access"
    assert capability_for("CORR-NTLM-RELAY-PATH") == "credential_access"
    # reaching a login screen is not owning the host (FM-05)
    assert capability_for("POSTURE-RDP-EXPOSED") == "recon"
    assert capability_for("POSTURE-RTSP-EXPOSED") == "recon"
    # a precondition for a known exploit class, vulnerability unproven
    assert capability_for("POSTURE-SMB-V1-ENABLED") == "exploit_precondition"
    assert capability_for("POSTURE-RDP-NO-NLA") == "exploit_precondition"
    assert capability_for("POSTURE-SNMP-DEFAULT-COMMUNITY") == "credential_access"
    assert capability_for("POSTURE-LDAP-ANONYMOUS-BIND") == "recon"


def test_a_dos_amplifier_is_not_an_attack_step():
    # T1498 network DoS is explicitly not a path step.
    assert capability_for("POSTURE-UDP-AMPLIFIER", "amplification", "T1498.002") is None


def test_unknown_rule_falls_back_through_category_then_mitre_then_none():
    assert classify("NEW-RULE", "default_credentials") == ("credential_access", "category")
    assert classify("NEW-RULE", "weak_crypto", "T1040") == ("credential_access", "mitre")
    assert classify("NEW-RULE", "weird", "T9999") == (None, None)


def test_a_fallback_classification_never_grants_control():
    # F1: an imported scanner finding tagged T1190 is classified, but is not a foothold.
    cap, source = classify(None, None, ["T1190"])
    assert cap == "foothold" and source == "mitre"
    assert not grants_control(cap, source)
    assert step_likelihood_for_capability({"capability": cap, "capability_source": source,
                                           "state": "confirmed"}) == 0.0


def test_only_curated_control_capabilities_grant_control():
    for cap in ("foothold", "exploit_precondition", "lateral", "priv_esc"):
        assert grants_control(cap, "rule")
        assert not grants_control(cap, "category")
        assert not grants_control(cap, "mitre")
    assert not grants_control("credential_access")
    assert not grants_control("recon")
    assert not grants_control(None)
    assert CONTROL_CAPABILITIES == frozenset({"foothold", "exploit_precondition", "lateral", "priv_esc"})


def test_mgmt_plane_composite_is_a_foothold_only_for_ipmi_cipher_zero():
    assert classify("CORR-MGMT-PLANE-EXPOSED", evidence={"correlated": ["IPMI-CIPHER-ZERO"]})[0] == "foothold"
    assert classify("CORR-MGMT-PLANE-EXPOSED",
                    evidence={"correlated": ["SVC-WINRM-EXPOSED", "SVC-RDP-EXPOSED"]})[0] == "recon"


def test_a_precondition_ranks_well_below_a_foothold_unless_kev_backs_it():
    base = {"capability_source": "rule", "state": "confirmed", "confidence": 100}
    foothold = step_likelihood_for_capability({**base, "capability": "foothold"})
    pre = step_likelihood_for_capability({**base, "capability": "exploit_precondition"})
    pre_kev = step_likelihood_for_capability({**base, "capability": "exploit_precondition", "kev": True})
    assert pre < pre_kev < foothold
    assert pre <= 0.2


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


# ── H1 failure areas, end to end through the graph ────────────────────────────

def _graph_for(findings, exposed_port=5432):
    eid = uuid.uuid4()
    assets = [_asset("a1", "10.0.0.5", exposed=True), _asset("a2", "10.0.0.9", crit="critical")]
    services = [_svc("s1", "a1", exposed_port, exposure="external")]
    b = GraphBuilder()
    b.assemble(eid, assets, services, findings, scope_cidrs=["10.0.0.0/24"])
    return PathAnalyzer(b.graph)


def _imported(fid, aid, mitre):
    """A finding imported from another scanner: free-form ATT&CK tag, no curated rule."""
    return NS(id=fid, asset_id=aid, title="Imported finding", cvss_score=None, cvss_vector=None,
              epss_score=None, severity="info", status="open", exploitable=False,
              exploit_validated=False, mitre_techniques=[mitre], verification_confidence=None,
              verification_state=None, evidence={"source": "nuclei"}, last_seen=None)


def test_an_imported_t1190_finding_is_not_a_foothold():
    analyzer = _graph_for([_imported("f1", "a1", "T1190"),
                           _finding("f2", "a2", "POSTURE-VNC-NO-AUTH", "T1021.005")])
    assert analyzer.find_paths_to_target("a2") == []
    assert analyzer.diagnose(["a2"])["entry_points"] == 0


def test_rdp_merely_answering_does_not_make_a_host_ownable():
    analyzer = _graph_for([_finding("f1", "a1", "POSTURE-DB-UNAUTHENTICATED-ACCESS"),
                           _finding("f2", "a2", "POSTURE-RDP-EXPOSED", "T1021.001")], 5432)
    assert analyzer.find_paths_to_target("a2") == []


def test_the_relay_composite_alone_does_not_own_its_host():
    analyzer = _graph_for([_finding("f1", "a1", "POSTURE-DB-UNAUTHENTICATED-ACCESS"),
                           _finding("f2", "a2", "CORR-NTLM-RELAY-PATH", "T1557.001")])
    # no other SMB host on the subnet to coerce from, so no relay and no route
    assert analyzer.find_paths_to_target("a2") == []


def test_an_smbv1_step_is_possible_but_weak():
    analyzer = _graph_for([_finding("f1", "a1", "POSTURE-DB-UNAUTHENTICATED-ACCESS"),
                           _finding("f2", "a2", "POSTURE-SMB-V1-ENABLED", "T1210")])
    paths = analyzer.find_paths_to_target("a2")
    assert paths and paths[0]["edges"][-1]["capability"] == "exploit_precondition"
    assert paths[0]["edges"][-1]["likelihood"] <= 0.2


def test_hop_wording_never_calls_a_precondition_an_exploitation():
    from app.routers.attack_paths import _explain_hop
    base = {"source": "a", "target": "b", "technique": "SAME_SUBNET", "via": ["10.0.0.0/24"],
            "basis": "same_subnet", "exploited": True, "cvss": 0.0}
    pre = _explain_hop({**base, "capability": "exploit_precondition"}, {})
    assert "not verified" in pre and "exploits it" not in pre
    foot = _explain_hop({**base, "capability": "foothold"}, {})
    assert "needs no credential" in foot and "CVSS" not in foot
    cve = _explain_hop({**base, "capability": None, "cvss": 9.8}, {})
    assert "CVSS 9.8" in cve

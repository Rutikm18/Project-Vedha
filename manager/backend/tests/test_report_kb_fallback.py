"""M7/M8 — the report fills unrecorded narrative and the fix plan from the deterministic KB.

Precedence is overrides > recorded evidence > knowledge base, every fallback is labelled in
`narrative_sources`, and the rule's internal false-positive note moves to `detection_rationale`.
"""
from __future__ import annotations

from datetime import timedelta

from app.models.enums import FindingSeverity
from app.services import report_enrichment as enrich
from app.services.finding_content import content_category
from app.services.report_document import build_report_document
from tests.test_report_document import (
    NOW, _asset, _engagement, _finding,
)

_WINDOWS = {"critical": 24, "high": 72, "medium": 168, "low": 720, "info": 0}


def _doc(finding, asset):
    return build_report_document(
        engagement=_engagement(), finding_rows=[(finding, asset)], event_rows=[],
        remediation_plan_rows=[], resolution_runs={}, generated_at=NOW, sla_windows=_WINDOWS)


def _posture(engagement, asset, **over):
    base = dict(
        title="VNC server accepts connections without authentication (port 5900)",
        description="CWE-306; ATT&CK T1021.005; observed by vnc_scan; needs a successful RFB handshake",
        severity=FindingSeverity.critical, cve_ids=None, cvss_score=None, cvss_vector=None,
        epss_score=None, remediation="Require a VNC password.", exploitable=False,
        evidence={"rule_id": "POSTURE-VNC-NO-AUTH", "scanner": "vnc_scan", "port": 5900,
                  "fp_notes": "needs a successful RFB handshake",
                  "evidence": {"evidence_basis": "protocol_observed"}},
    )
    base.update(over)
    return _finding(engagement.id, asset.id, None, **base)


def test_unrecorded_narrative_comes_from_the_kb_and_is_labelled():
    eng, asset = _engagement(), None
    asset = _asset(eng.id)
    item = _doc(_posture(eng, asset), asset).findings[0]
    assert item.technical_details and "authentication" in item.technical_details.lower()
    assert item.impact and item.business_impact
    assert "Not validated" in item.exploitation                 # honest about exploitation
    assert item.narrative_sources["impact"] == "knowledge_base"
    assert item.narrative_sources["technical_details"] == "knowledge_base"


def test_recorded_narrative_beats_the_kb():
    eng = _engagement()
    asset = _asset(eng.id)
    item = _doc(_finding(eng.id, asset.id, None), asset).findings[0]      # evidence records all of it
    assert item.impact == "A downgrade may expose session traffic."
    assert item.narrative_sources["impact"] == "recorded"
    assert item.narrative_sources["description"] == "recorded"


def test_rule_metadata_description_moves_to_detection_rationale():
    eng = _engagement()
    asset = _asset(eng.id)
    item = _doc(_posture(eng, asset), asset).findings[0]
    assert "CWE-306" not in (item.description or "")           # no longer the rule's metadata line
    assert item.narrative_sources["description"] == "knowledge_base"
    assert "POSTURE-VNC-NO-AUTH" in item.detection_rationale
    assert "protocol-level observation" in item.detection_rationale
    assert "needs a successful RFB handshake" in item.detection_rationale


def test_fix_plan_is_attached_with_ordered_steps_and_verification():
    eng = _engagement()
    asset = _asset(eng.id)
    item = _doc(_posture(eng, asset), asset).findings[0]
    plan = item.remediation.fix_plan
    assert plan and plan["source"] == "deterministic_kb"
    assert [s["step"] for s in plan["steps"]] == list(range(1, len(plan["steps"]) + 1))
    assert plan["verification_check"]["check"]
    kinds = {r.source_type for r in item.remediation.recommendations}
    assert "knowledge_base_recipe" in kinds
    # KB advice is never presented as a recorded recommendation
    assert not any("knowledge_base" in t for t in item.remediation.recorded_recommendations)


def test_rule_ids_route_to_the_specific_content_category():
    class F:
        evidence = {"rule_id": "POSTURE-NFS-WORLD-READABLE-EXPORT"}
        title, description, remediation, cve_ids = "NFS", "", "", None
    assert content_category(F()) == "nfs_export"
    F.evidence = {"rule_id": "POSTURE-IPMI-CIPHER-ZERO"}
    assert content_category(F()) == "ipmi_cipher_zero"


def test_every_posture_rule_gets_non_generic_content_or_a_known_classifier_category():
    """No rule may fall to a missing content entry (KeyError → generic is the floor)."""
    from app.detection import engine_bridge as EB
    if not EB._ensure_importable():
        import pytest
        pytest.skip("detection_engine not importable in this environment")
    import posture_rules as P
    from app.services.finding_content import _CONTENT, _RULE_CATEGORY
    assert set(_RULE_CATEGORY.values()) <= set(_CONTENT)
    rules = {r.rule_id for r in P.RULES}
    mapped = {r for r in _RULE_CATEGORY if r in rules}
    # the plan's named gaps are covered by a dedicated category
    for rid in ("POSTURE-VNC-NO-AUTH", "POSTURE-NFS-WORLD-READABLE-EXPORT",
                "POSTURE-RSYNC-ANONYMOUS-MODULE", "POSTURE-SNMP-DEFAULT-COMMUNITY",
                "POSTURE-IPMI-CIPHER-ZERO", "POSTURE-MQTT-UNAUTHENTICATED",
                "POSTURE-AI-ENDPOINT-UNAUTHENTICATED", "POSTURE-DB-UNAUTHENTICATED-ACCESS"):
        assert rid in mapped, rid


def test_plan_text_is_ordered_and_includes_verification():
    plan = {"title": "Fix it", "steps": [{"step": 1, "tier": "fix", "title": "Do A"},
                                         {"step": 2, "tier": "hardening", "title": "Do B"}],
            "verification_check": {"check": "re-scan", "expected": "no finding"}}
    text = enrich.plan_text(plan)
    assert text.splitlines()[1].startswith("1. [fix] Do A")
    assert "Verify: re-scan" in text


# ── M1.3: roll findings up to issues ─────────────────────────────────────────

def test_findings_on_one_service_roll_up_to_one_issue():
    eng = _engagement()
    asset = _asset(eng.id)
    base = {"scanner": "x", "port": 161}
    rows = [
        (_posture(eng, asset, title="SNMP default community (port 161)",
                  severity=FindingSeverity.high,
                  evidence={**base, "rule_id": "POSTURE-SNMP-DEFAULT-COMMUNITY"}), asset),
        (_posture(eng, asset, title="SNMP exposed (port 161)", severity=FindingSeverity.medium,
                  evidence={**base, "rule_id": "POSTURE-EXPOSED-ADMIN_UI"}), asset),
        (_posture(eng, asset, title="VNC open (port 5900)", severity=FindingSeverity.critical,
                  evidence={"scanner": "x", "port": 5900, "rule_id": "POSTURE-VNC-NO-AUTH"}), asset),
    ]
    doc = build_report_document(
        engagement=eng, finding_rows=rows, event_rows=[], remediation_plan_rows=[],
        resolution_runs={}, generated_at=NOW, sla_windows=_WINDOWS)
    assert doc.summary.total_findings == 3 and doc.summary.issue_count == 2
    snmp = next(g for g in doc.summary.issue_groups if g.port == 161)
    assert snmp.finding_count == 2 and snmp.severity == "high"
    assert snmp.title == "SNMP default community (port 161)"
    assert snmp.signals == ["SNMP exposed (port 161)"]
    assert doc.summary.issue_groups[0].port == 5900          # critical issue first


def test_finding_without_a_port_is_its_own_issue():
    eng = _engagement()
    asset = _asset(eng.id)
    rows = [(_posture(eng, asset, title=t, evidence={"rule_id": "POSTURE-OS-END-OF-LIFE"}), asset)
            for t in ("OS end-of-life", "Another host-level issue")]
    doc = build_report_document(
        engagement=eng, finding_rows=rows, event_rows=[], remediation_plan_rows=[],
        resolution_runs={}, generated_at=NOW, sla_windows=_WINDOWS)
    assert doc.summary.issue_count == 2


# ── M9: CVSS / EPSS / CVE are "not applicable" with a reason for configuration findings ──

def test_posture_finding_gets_honest_not_applicable_reasons_and_no_score_gaps():
    eng = _engagement()
    asset = _asset(eng.id)
    item = _doc(_posture(eng, asset), asset).findings[0]
    assert {"cve", "cvss", "epss"} <= set(item.not_applicable_reasons)
    assert "EPSS" in item.not_applicable_reasons["epss"]
    for gap in ("cve_reference_or_not_applicable_reason_absent",
                "cvss_score_or_not_applicable_reason_absent"):
        assert gap not in item.readiness_gaps


def test_vulnerability_finding_without_cvss_stays_a_gap():
    eng = _engagement()
    asset = _asset(eng.id)
    finding = _finding(eng.id, asset.id, None, cve_ids=["CVE-2026-0001"], cvss_score=None,
                       cvss_vector=None, evidence={"output": "x"})
    item = _doc(finding, asset).findings[0]
    assert "cvss_score_or_not_applicable_reason_absent" in item.readiness_gaps
    assert "cvss" not in item.not_applicable_reasons


def test_recorded_reason_beats_the_derived_one():
    eng = _engagement()
    asset = _asset(eng.id)
    finding = _posture(eng, asset, evidence={
        "rule_id": "POSTURE-VNC-NO-AUTH", "port": 5900,
        "cvss_not_applicable_reason": "Scored as a policy violation per client SOP-12."})
    item = _doc(finding, asset).findings[0]
    assert item.not_applicable_reasons["cvss"] == "Scored as a policy violation per client SOP-12."


# ── M11: coverage sheet — "not detected" vs "not checked" ────────────────────

def _run_with_verdicts(verdicts):
    from types import SimpleNamespace
    import uuid as _uuid
    return SimpleNamespace(id=_uuid.uuid4(), finished_at=NOW, vuln_db_version="sha256:db",
                           stats={"posture_verdicts": verdicts})


def test_coverage_sheet_tells_clean_from_not_checked():
    from types import SimpleNamespace
    run = _run_with_verdicts({
        "POSTURE-SMB-SIGNING-OFF": {"verdict": "finding_exists", "reasons": []},
        "POSTURE-RDP-NO-NLA": {"verdict": "evaluated_clean", "reasons": []},
        "POSTURE-TLS-WEAK-CIPHER": {"verdict": "schema_drift",
                                    "reasons": ["required fact path absent: data.cipher_analysis"]},
    })
    job = SimpleNamespace(reference="SCAN-7", use_case_id="internal_vuln", intensity="normal",
                          result={"ports_scanned": [443, 22, 22]})
    titles = {"POSTURE-SMB-SIGNING-OFF": "SMB signing off", "POSTURE-RDP-NO-NLA": "RDP without NLA",
              "POSTURE-TLS-WEAK-CIPHER": "Weak cipher", "POSTURE-VNC-NO-AUTH": "VNC no auth"}
    sheet = enrich.coverage_sheet(run, job, titles)
    by_rule = {r["rule_id"]: r["verdict"] for r in sheet["rules"]}
    assert by_rule["POSTURE-VNC-NO-AUTH"] == "no_evidence_collected"      # never ran ≠ clean
    assert by_rule["POSTURE-RDP-NO-NLA"] == "evaluated_clean"
    assert (sheet["rules_total"], sheet["rules_with_finding"], sheet["rules_evaluated_clean"],
            sheet["rules_not_checked"], sheet["rules_could_not_assess"]) == (4, 1, 1, 1, 1)
    assert sheet["ports_scanned"] == [22, 443] and sheet["scan_use_case"] == "internal_vuln"


def test_coverage_sheet_is_honest_when_ports_or_job_are_unrecorded():
    sheet = enrich.coverage_sheet(_run_with_verdicts({"POSTURE-X": {"verdict": "evaluated_clean"}}),
                                  None, {})
    assert sheet["ports_scanned"] is None and "No scan job" in sheet["ports_scanned_note"]


def test_no_recorded_verdicts_means_no_sheet():
    from types import SimpleNamespace
    assert enrich.coverage_sheet(SimpleNamespace(stats={}), None, {}) is None
    assert enrich.coverage_sheet(SimpleNamespace(stats=None), None, {}) is None


def test_report_carries_the_coverage_sheet():
    eng = _engagement()
    asset = _asset(eng.id)
    run = _run_with_verdicts({"POSTURE-RDP-NO-NLA": {"verdict": "evaluated_clean", "reasons": []}})
    doc = build_report_document(
        engagement=eng, finding_rows=[(_posture(eng, asset), asset)], event_rows=[],
        remediation_plan_rows=[], resolution_runs={}, generated_at=NOW, sla_windows=_WINDOWS,
        coverage_run=run)
    assert doc.coverage_sheet is not None and doc.coverage_sheet.rules_evaluated_clean >= 1
    assert build_report_document(
        engagement=eng, finding_rows=[], event_rows=[], remediation_plan_rows=[],
        resolution_runs={}, generated_at=NOW, sla_windows=_WINDOWS).coverage_sheet is None


def test_merged_producers_are_nested_under_the_issue_not_lost():
    eng = _engagement()
    asset = _asset(eng.id)
    merged = _posture(eng, asset, title="NFS export world-readable (port 2049)", evidence={
        "rule_id": "POSTURE-NFS-WORLD-READABLE-EXPORT", "port": 2049,
        "signals": [{"rule_id": "POSTURE-NFS-WORLD-READABLE-EXPORT", "title": "NFS export world-readable (port 2049)", "severity": "high"},
                    {"rule_id": "POSTURE-EXPOSED-CLEARTEXT", "title": "Cleartext protocol exposed on 2049 (NFS)", "severity": "medium"}]})
    doc = build_report_document(
        engagement=eng, finding_rows=[(merged, asset)], event_rows=[], remediation_plan_rows=[],
        resolution_runs={}, generated_at=NOW, sla_windows=_WINDOWS)
    item = doc.findings[0]
    assert [s["rule_id"] for s in item.merged_signals] == ["POSTURE-NFS-WORLD-READABLE-EXPORT", "POSTURE-EXPOSED-CLEARTEXT"]
    group = doc.summary.issue_groups[0]
    assert group.finding_count == 1 and group.signals == ["Cleartext protocol exposed on 2049 (NFS)"]


# ── M10: the report states the role and how far it can be trusted ────────────

def test_report_shows_role_confidence_and_flags_an_os_contradicted_role():
    eng = _engagement()
    router_claim = _asset(eng.id, device_role="network_device", role_confidence=0.9, os="Ubuntu 22.04")
    item = _doc(_posture(eng, router_claim), router_claim).findings[0]
    a = item.asset
    assert (a.device_role, a.resolved_role) == ("network_device", "server")
    assert a.role_trusted is False and a.role_basis == "os_fingerprint_overrides_port_inference"
    real_router = _asset(eng.id, device_role="network_device", role_confidence=0.9, os="Cisco IOS XE")
    b = _doc(_posture(eng, real_router), real_router).findings[0].asset
    assert b.resolved_role == "network_device" and b.role_trusted is True


def test_report_leaves_the_role_out_when_nothing_classified_the_host():
    eng = _engagement()
    plain = _asset(eng.id)
    a = _doc(_posture(eng, plain), plain).findings[0].asset
    assert a.device_role is None and a.role_trusted is None


def test_expired_risk_acceptance_is_a_readiness_gap():
    from datetime import timedelta
    from tests.test_report_document import _event
    eng = _engagement()
    asset = _asset(eng.id)
    finding = _posture(eng, asset, status="accepted")
    ev = _event(finding.id, "accepted", NOW - timedelta(days=40), detail={
        "risk_owner": "CISO", "compensating_controls": "ACL",
        "expires_at": (NOW - timedelta(days=1)).isoformat()})
    doc = build_report_document(
        engagement=eng, finding_rows=[(finding, asset)], event_rows=[ev], remediation_plan_rows=[],
        resolution_runs={}, generated_at=NOW, sla_windows=_WINDOWS)
    assert "risk_acceptance_expired" in doc.findings[0].closure.completeness_gaps


# ── root cause / preconditions / reproduction come from the KB, labelled ─────

def test_root_cause_preconditions_and_reproduction_are_filled_and_labelled():
    eng = _engagement()
    asset = _asset(eng.id)
    item = _doc(_posture(eng, asset), asset).findings[0]
    assert item.root_cause and "VNC" in item.root_cause
    assert isinstance(item.preconditions, list) and item.preconditions
    assert isinstance(item.reproduction_steps, list) and item.reproduction_steps[0].startswith("Re-check:")
    for field in ("root_cause", "preconditions", "reproduction_steps"):
        assert item.narrative_sources[field] == "knowledge_base"
    for gap in ("reproduction_steps_absent",):
        assert gap not in item.readiness_gaps


def test_recorded_root_cause_wins():
    eng = _engagement()
    asset = _asset(eng.id)
    item = _doc(_finding(eng.id, asset.id, None), asset).findings[0]       # evidence records it
    assert item.root_cause == "The server policy still permits a deprecated protocol."
    assert item.narrative_sources["root_cause"] == "recorded"


def test_every_content_category_has_a_cause_entry():
    from app.services.finding_content import _CAUSE, _CONTENT
    assert set(_CONTENT) == set(_CAUSE)
    assert all(v["root_cause"] and v["preconditions"] for v in _CAUSE.values())


def test_fix_plan_is_compact_but_keeps_what_a_reader_acts_on():
    import json
    eng = _engagement()
    asset = _asset(eng.id)
    plan = _doc(_posture(eng, asset), asset).findings[0].remediation.fix_plan
    assert "context" not in plan and "fragile_guard" not in plan
    assert all("commands" not in s and "commands_for_os" in s for s in plan["steps"])
    assert plan["verification_check"]["check"] and plan["provenance"]["recipe_id"] == "POSTURE-VNC-NO-AUTH"
    assert len(json.dumps(plan)) < 3500


def test_no_detection_rule_falls_back_to_generic_content():
    """A rule that reads 'The service exhibits a security weakness' tells a client nothing; every
    posture rule and every exposed-service class must have specific explanatory content AND a
    root cause."""
    from types import SimpleNamespace
    from app.detection.engine_bridge import _ensure_importable
    if not _ensure_importable():
        import pytest
        pytest.skip("detection_engine not importable in this environment")
    import port_intel
    import posture_rules as P
    from app.services.finding_content import _CAUSE, _CONTENT, content_category
    ids = [r.rule_id for r in P.RULES] + [f"POSTURE-EXPOSED-{c.upper()}"
                                           for c in sorted(set(port_intel.catalog_categories().values()))]
    generic = []
    for rid in ids:
        probe = SimpleNamespace(evidence={"rule_id": rid}, title="", description="", remediation="", cve_ids=None)
        cat = content_category(probe)
        if cat == "generic":
            generic.append(rid)
        assert cat in _CONTENT and cat in _CAUSE, (rid, cat)
    assert not generic, f"rules still using the generic explanation: {generic}"


def test_composite_attack_path_findings_get_specific_content_and_a_real_fix_plan():
    """The highest-severity findings are the composites; they must not fall to generic text or the
    generic recipe. They borrow the weakness they are built from."""
    from types import SimpleNamespace
    from app.remediation.context import build_context
    from app.remediation.recipes import CORRELATION_RECIPE, RECIPES, resolve_recipe
    from app.services.finding_content import _CAUSE, _CONTENT, content_category
    for rule_id, target in CORRELATION_RECIPE.items():
        f = SimpleNamespace(evidence={"rule_id": rule_id}, title="x", description="", remediation="",
                            cve_ids=None, severity="high", id=None)
        assert content_category(f) != "generic", rule_id
        assert content_category(f) in _CONTENT and content_category(f) in _CAUSE
        recipe = resolve_recipe(build_context(f), f)
        assert recipe.recipe_id == target and recipe.recipe_id in RECIPES and recipe.recipe_id != "GENERIC"
    ipmi = SimpleNamespace(evidence={"rule_id": "CORR-MGMT-PLANE-EXPOSED", "correlated": ["IPMI-CIPHER-ZERO"]},
                           title="Exposed host management plane", description="IPMI cipher suite 0 accepts ANY password",
                           remediation="", cve_ids=None, severity="critical", id=None)
    assert resolve_recipe(build_context(ipmi), ipmi).recipe_id == "POSTURE-IPMI-CIPHER-ZERO"

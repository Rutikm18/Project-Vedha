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

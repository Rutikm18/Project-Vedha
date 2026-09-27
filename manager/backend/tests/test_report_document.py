"""Canonical report read model: recorded facts in, explicit gaps out."""

from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import HTTPException

from app.models.enums import (
    AssetCriticality,
    AssetType,
    DetectionStatus,
    EngagementStatus,
    FindingSeverity,
    FindingStatus,
)
from app.services.report_document import (
    build_report_document,
    extract_compliance_mappings,
    extract_regulatory_profiles,
    load_report_document,
    normalize_evidence,
)


NOW = datetime(2026, 9, 26, 8, 30, tzinfo=timezone.utc)


def _engagement(**over):
    base = dict(
        id=uuid.uuid4(),
        tenant_id=uuid.uuid4(),
        name="Customer perimeter assessment",
        status=EngagementStatus.completed,
        scope_cidrs=["192.0.2.0/24"],
        excluded_cidrs=[],
        start_time=NOW - timedelta(days=7),
        end_time=NOW - timedelta(days=1),
        rules_of_engagement={
            "client": "Example Corp",
            "assessor": "Vedha Security",
            "description": "External assessment",
            "tags": ["external"],
            "regulatory_profiles": [
                {
                    "profile_id": "cert-in-audit-guidelines-2025",
                    "name": "CERT-In Comprehensive Cyber Security Audit Policy Guidelines",
                    "version": "2025-07",
                    "jurisdiction": "India",
                    "applicability": "applicable",
                    "rationale": "Customer selected the profile for this audit.",
                    "source_url": "https://www.cert-in.org.in/",
                    "scope": {"engagement": "external assessment"},
                    "selected_by": "customer@example.test",
                    "selected_at": "2026-09-18T10:00:00+05:30",
                    "reviewed_by": "reviewer@example.test",
                    "reviewed_at": "2026-09-18T11:00:00+05:30",
                    "limitations": "Applicability is customer-recorded, not a certification.",
                },
                {
                    "profile_id": "sebi-cscrf-2024",
                    "name": "SEBI Cybersecurity and Cyber Resilience Framework",
                    "version": "2024-08",
                    "jurisdiction": "India",
                    "applicability": "customer_asserted",
                    "rationale": "Customer recorded itself as a regulated entity.",
                    "source_url": "https://www.sebi.gov.in/",
                    "scope": {"engagement": "external assessment"},
                    "selected_by": "customer@example.test",
                    "selected_at": "2026-09-18T10:00:00+05:30",
                    "reviewed_by": "reviewer@example.test",
                    "reviewed_at": "2026-09-18T11:00:00+05:30",
                    "limitations": "NSE ASP annexures are not implied by this profile.",
                },
            ],
            "report_metadata": {
                "version": "1.0",
                "document_status": "Draft",
                "classification": "Confidential",
                "prepared_by": "analyst@example.test",
                "prepared_at": "2026-09-26T08:00:00+05:30",
                "reviewed_by": "reviewer@example.test",
                "reviewed_at": "2026-09-26T09:00:00+05:30",
                "approved_by": "approver@example.test",
                "approved_at": "2026-09-26T10:00:00+05:30",
                "issue_date": "2026-09-26T10:00:00+05:30",
                "reporting_period": "2026-09-19/2026-09-25",
                "methodology": "Recorded customer assessment methodology",
                "risk_rating_method": "CVSS v3.1 plus recorded customer context",
                "tools_used": "Authorized Vedha probe and testssl",
                "evidence_retention_policy": "Retain approved evidence for 12 months",
                "report_timezone": "Asia/Kolkata",
                "limitations": "One excluded CIDR was not assessed.",
            },
            "credentials": {"must_not_leak": True},
        },
        created_at=NOW - timedelta(days=8),
        updated_at=NOW - timedelta(hours=2),
    )
    base.update(over)
    return SimpleNamespace(**base)


def _asset(engagement_id, **over):
    base = dict(
        id=uuid.uuid4(),
        engagement_id=engagement_id,
        ip_address="192.0.2.10",
        hostname="edge-01",
        fqdn="edge-01.example.test",
        os="Linux",
        os_version="12",
        asset_type=AssetType.server,
        criticality=AssetCriticality.high,
        owner="Platform",
        environment="production",
        tags={"region": "test"},
        last_seen=NOW - timedelta(hours=1),
    )
    base.update(over)
    return SimpleNamespace(**base)


def _finding(engagement_id, asset_id, run_id, **over):
    base = dict(
        id=uuid.uuid4(),
        engagement_id=engagement_id,
        asset_id=asset_id,
        title="TLS 1.0 enabled",
        description="The service accepts TLS 1.0.",
        severity=FindingSeverity.high,
        status=FindingStatus.remediated,
        cve_ids=["CVE-2026-0001"],
        mitre_techniques=["T1040"],
        cvss_score=Decimal("7.5"),
        cvss_vector="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L",
        epss_score=Decimal("0.1000"),
        risk_score=Decimal("750.00"),
        exploitable=True,
        exploit_validated=False,
        detection_status=DetectionStatus.detected,
        evidence={
            "artifacts": [
                {
                    "label": "Scanner output",
                    "content": "TLSv1 accepted",
                    "tool": "testssl",
                    "timestamp": "2026-09-20T10:00:00+05:30",
                    "sha256": "a" * 64,
                }
            ],
            "technical_details": "The endpoint completed a TLS 1.0 handshake.",
            "impact": "A downgrade may expose session traffic.",
            "business_impact": "Protected customer traffic may lose confidentiality.",
            "exploitation": "An on-path attacker may force weaker protocol negotiation.",
            "reproduction_steps": ["Offer TLS 1.0", "Observe a successful handshake"],
            "root_cause": "The server policy still permits a deprecated protocol.",
            "preconditions": ["Network access to the TLS endpoint"],
            "cwe_ids": ["CWE-326"],
            "recommendations": ["Continuously monitor protocol configuration."],
            "compliance_mappings": [
                {
                    "mapping_id": "MAP-PCI-4.2.1-001",
                    "framework": "PCI DSS",
                    "framework_version": "4.0.1",
                    "control_id": "4.2.1",
                    "control_title": "Strong cryptography",
                    "relationship": "supports",
                    "rationale": "The recorded service permits a weak protocol.",
                    "applicability": "applicable",
                    "assessment_status": "not_satisfied",
                    "result": "fail",
                    "scope": {"asset_ids": ["edge-01"]},
                    "source_url": "https://example.test/pci/4.2.1",
                    "mapping_source": "customer-control-catalog",
                    "mapping_version": "2026.09",
                    "mapped_by": "mapper@example.test",
                    "mapped_at": "2026-09-20T10:05:00+05:30",
                    "reviewed_by": "reviewer@example.test",
                    "reviewed_at": "2026-09-21T10:05:00+05:30",
                    "limitations": "Only the recorded endpoint was tested.",
                    "customer_statement": "Customer confirmed control applicability.",
                    "assessor": "analyst@example.test",
                    "assessed_at": "2026-09-20T10:00:00+05:30",
                    "evidence_references": ["Scanner output"],
                }
            ],
        },
        remediation="Disable TLS 1.0 and enable TLS 1.2 or later.",
        first_seen=NOW - timedelta(days=6),
        last_seen=NOW - timedelta(days=2),
        initial_detection_run_id=None,
        detection_run_id=uuid.uuid4(),
        detected_db_version="sha256:db-v1",
        resolution_miss_count=2,
        resolved_at=NOW - timedelta(days=1),
        resolution_method="auto",
        resolution_run_id=run_id,
        reopened_count=1,
        verification_state="confirmed",
        verification_confidence=95,
        verification_rationale="Two independent observations.",
        verification_method="passive",
        needs_review=False,
        created_at=NOW - timedelta(days=6),
        updated_at=NOW - timedelta(days=1),
    )
    base.update(over)
    return SimpleNamespace(**base)


def _event(finding_id, event_type, occurred_at, **over):
    base = dict(
        id=uuid.uuid4(),
        finding_id=finding_id,
        event_type=event_type,
        actor="operator-1",
        actor_type="user",
        from_status=None,
        to_status=None,
        detail={},
        occurred_at=occurred_at,
    )
    base.update(over)
    return SimpleNamespace(**base)


def _run(run_id, engagement_id, **over):
    base = dict(
        id=run_id,
        engagement_id=engagement_id,
        scan_result_id=uuid.uuid4(),
        trigger="facts_ready",
        status="completed",
        vuln_db_version="sha256:db-v1",
        vuln_db_fetched_at="2026-09-25T00:00:00Z",
        started_at=NOW - timedelta(days=1, minutes=10),
        finished_at=NOW - timedelta(days=1),
        facts_count=25,
        findings_new=0,
        findings_reaffirmed=4,
        findings_current=3,
        stats={
            "coverage": {
                "assets": ["192.0.2.10"],
                "scanners_completed": ["testssl"],
                "scanners_degraded": [],
            },
            "auto_resolved": 1,
        },
    )
    base.update(over)
    return SimpleNamespace(**base)


def _scan_result(scan_result_id, engagement_id, **over):
    base = dict(
        id=scan_result_id,
        engagement_id=engagement_id,
        job_id=uuid.uuid4(),
        attempt_id=uuid.uuid4(),
        agent_id=uuid.uuid4(),
        content_checksum="f" * 64,
        validation_state="accepted",
        scan_type="network_vulnerability",
        created_at=NOW - timedelta(days=6, minutes=1),
    )
    base.update(over)
    return SimpleNamespace(**base)


def _plan(finding_id, reviewed=True, **over):
    base = dict(
        id=uuid.uuid4(),
        finding_id=finding_id,
        os="linux",
        source="ai",
        reviewed=reviewed,
        generated_at=NOW - timedelta(days=2),
        model="reviewed-model",
        plan={
            "summary": "Disable the weak protocol.",
            "effort": "low",
            "remediation_risk": "medium",
            "steps": [{"step": 1, "title": "Update the TLS policy"}],
            "verification": ["Run the authorized TLS scanner again."],
            "long_term_recommendations": ["Baseline cryptographic policy."],
            "compensating_controls": "Restrict network access until patched.",
        },
    )
    base.update(over)
    return SimpleNamespace(**base)


def test_normalized_evidence_preserves_recorded_time_and_never_fabricates_one():
    recorded = [
        {
            "content": "proof",
            "evidence_type": "scanner_output",
            "source": "scanner-a",
            "captured_at": "2026-09-01T12:34:56+05:30",
            "sha256": "b" * 64,
        }
    ]
    out = normalize_evidence(recorded)
    assert out.raw is recorded
    assert out.artifacts[0].captured_at == "2026-09-01T12:34:56+05:30"
    assert out.artifacts[0].evidence_type == "scanner_output"
    assert out.artifacts[0].timestamp is None
    assert out.gaps == []

    missing = normalize_evidence({"output": "proof"})
    assert missing.artifacts[0].timestamp is None
    assert "evidence_capture_time_absent" in missing.gaps


def test_each_evidence_artifact_must_carry_valid_provenance():
    out = normalize_evidence(
        [
            {
                "content": "complete",
                "source": "scanner-a",
                "captured_at": "2026-09-01T12:34:56+05:30",
                "sha256": "c" * 64,
            },
            {
                "content": "incomplete",
                "captured_at": "2026-09-01 12:34:56",
                "sha256": "not-a-sha256",
            },
        ]
    )
    assert "evidence_artifact_2_capture_time_invalid_rfc3339" in out.gaps
    assert "evidence_artifact_2_source_absent" in out.gaps
    assert "evidence_artifact_2_sha256_invalid" in out.gaps
    assert "evidence_capture_time_invalid_rfc3339" in out.gaps
    assert "evidence_integrity_hash_invalid" in out.gaps


def test_scanner_observation_metadata_is_promoted_into_evidence_provenance():
    scan_result_id = uuid.uuid4()
    scan_job_id = uuid.uuid4()
    run_id = uuid.uuid4()
    out = normalize_evidence(
        {
            "content": "TLS protocol observation",
            "scan_provenance": {
                "recorded_by": "vedha_manager",
                "schema_version": 1,
                "initial": {
                    "scan_result_id": str(scan_result_id),
                    "scan_job_id": str(scan_job_id),
                    "detection_run_id": str(run_id),
                    "scan_type": "tls_scan",
                    "source": "probe",
                    "tool": "testssl",
                    "recorded_at": "2026-09-27T08:30:00Z",
                    "timestamp_basis": "manager_recorded",
                },
                "latest": {
                    "scan_result_id": str(scan_result_id),
                    "scan_job_id": str(scan_job_id),
                    "detection_run_id": str(run_id),
                    "scan_type": "tls_scan",
                    "source": "probe",
                    "tool": "testssl",
                    "recorded_at": "2026-09-27T08:30:00Z",
                    "timestamp_basis": "manager_recorded",
                },
            },
        }
    )

    artifact = out.artifacts[0]
    assert artifact.label == "testssl"
    assert artifact.tool == "testssl"
    assert artifact.source == "probe"
    assert artifact.timestamp == "2026-09-27T08:30:00Z"
    assert artifact.timestamp_basis == "manager_recorded"
    assert artifact.scan_result_id == str(scan_result_id)
    assert artifact.scan_job_id == str(scan_job_id)
    assert artifact.detection_run_id == str(run_id)
    assert "evidence_capture_time_absent" not in out.gaps
    assert "evidence_source_absent" not in out.gaps

    untrusted = normalize_evidence(
        {
            "content": "scanner-supplied values",
            "scan_provenance": {
                "latest": {
                    "scan_result_id": str(uuid.uuid4()),
                    "source": "forged-source",
                    "tool": "forged-tool",
                    "recorded_at": "2026-09-27T08:30:00Z",
                }
            },
        }
    ).artifacts[0]
    assert untrusted.scan_result_id is None
    assert untrusted.source is None
    assert untrusted.tool is None


def test_compliance_normalization_preserves_extended_recorded_metadata_exactly():
    recorded = {
        "mapping_id": "MAP-RA-5-001",
        "framework": "NIST SP 800-53",
        "framework_version": "Rev. 5",
        "release": "Release 5.2.0",
        "profile": "Moderate baseline",
        "control_id": "RA-5",
        "assessment_status": "partially_satisfied",
        "result": "fail",
        "test_ids": ["TEST-001", "TEST-009"],
        "scope": {"asset_ids": ["asset-7"], "boundary": "external"},
        "context": {"method": "credentialed", "sample": 12},
        "source_url": "https://example.test/control?rev=5#RA-5",
        "mapping_source": "customer-control-catalog",
        "mapping_version": "2026.09",
        "mapped_by": "mapper@example.test",
        "mapped_at": "2026-09-20T10:00:00+05:30",
        "reviewed_by": "reviewer@example.test",
        "reviewed_at": "2026-09-21T11:02:03-04:00",
        "limitations": ["One network segment was excluded."],
        "customer_statement": "Customer confirmed the control owner on 2026-09-21.",
        "assessor": "assessor@example.test",
        "assessed_at": "2026-09-19T09:08:07Z",
    }

    mapping = extract_compliance_mappings({"compliance_mappings": [recorded]})[0]

    assert mapping.mapping_id == recorded["mapping_id"]
    assert mapping.release == recorded["release"]
    assert mapping.profile == recorded["profile"]
    assert mapping.assessment_status == recorded["assessment_status"]
    assert mapping.result == recorded["result"]
    assert mapping.test_ids == recorded["test_ids"]
    assert mapping.scope == recorded["scope"]
    assert mapping.context == recorded["context"]
    assert mapping.source_url == recorded["source_url"]
    assert mapping.mapping_source == recorded["mapping_source"]
    assert mapping.mapping_version == recorded["mapping_version"]
    assert mapping.mapped_by == recorded["mapped_by"]
    assert mapping.mapped_at == recorded["mapped_at"]
    assert mapping.reviewed_by == recorded["reviewed_by"]
    assert mapping.reviewed_at == recorded["reviewed_at"]
    assert mapping.limitations == recorded["limitations"]
    assert mapping.customer_statement == recorded["customer_statement"]
    assert mapping.assessor == recorded["assessor"]
    assert mapping.assessed_at == recorded["assessed_at"]
    assert mapping.raw is recorded


def test_missing_extended_compliance_metadata_remains_null():
    mapping = extract_compliance_mappings({"compliance_mappings": [{}]})[0]

    for field in (
        "release",
        "mapping_id",
        "profile",
        "assessment_status",
        "test_ids",
        "scope",
        "context",
        "source_url",
        "mapping_source",
        "mapping_version",
        "mapped_by",
        "mapped_at",
        "reviewed_by",
        "reviewed_at",
        "limitations",
        "customer_statement",
        "assessor",
        "assessed_at",
    ):
        assert getattr(mapping, field) is None


def test_regulatory_profiles_are_recorded_only_and_opaque_legacy_values_survive():
    profiles = extract_regulatory_profiles(
        [
            {
                "profile_id": "cert-in-audit-guidelines-2025",
                "name": "CERT-In audit guidelines",
                "version": "2025-07",
                "jurisdiction": "India",
                "applicability": "applicable",
                "rationale": "Customer selected this profile.",
                "source_url": "https://www.cert-in.org.in/",
                "scope": {"engagement": "external"},
                "selected_by": "customer@example.test",
                "selected_at": "2026-09-18T10:00:00+05:30",
                "reviewed_by": "reviewer@example.test",
                "reviewed_at": "2026-09-18T11:00:00+05:30",
                "limitations": "Recorded applicability only.",
            },
            "Legacy profile reference",
        ]
    )

    assert profiles[0].profile_id == "cert-in-audit-guidelines-2025"
    assert profiles[0].scope == {"engagement": "external"}
    assert profiles[1].recorded_reference == "Legacy profile reference"
    assert profiles[1].name is None


def test_report_document_uses_recorded_history_coverage_compliance_and_reviewed_plans_only():
    engagement = _engagement()
    run_id = uuid.uuid4()
    asset = _asset(engagement.id)
    finding = _finding(engagement.id, asset.id, run_id)
    events = [
        _event(
            finding.id,
            "remediated",
            NOW - timedelta(days=3),
            to_status="remediated",
            detail={"reason": "Initial operator closure"},
        ),
        _event(
            finding.id,
            "reopened",
            NOW - timedelta(days=2),
            from_status="remediated",
            to_status="open",
            detail={"reason": "Regression observed"},
        ),
        _event(
            finding.id,
            "resolved",
            NOW - timedelta(days=1),
            actor="auto-resolution",
            actor_type="system",
            from_status="open",
            to_status="remediated",
            detail={
                "method": "auto",
                "run_id": str(run_id),
                "miss_count": 2,
                "reason": "coverage-proven clean for 2 runs",
            },
        ),
    ]
    reviewed = _plan(finding.id, reviewed=True)
    unreviewed = _plan(finding.id, reviewed=False, model="must-not-leak")

    out = build_report_document(
        engagement=engagement,
        finding_rows=[(finding, asset)],
        event_rows=events,
        remediation_plan_rows=[reviewed, unreviewed],
        resolution_runs={run_id: _run(run_id, engagement.id)},
        generated_at=NOW,
        sla_windows={"critical": 24, "high": 72, "medium": 168, "low": 720, "info": 0},
    )

    assert out.document.generated_at == NOW
    assert out.document.timezone == "UTC"
    assert out.document.display_timezone == "Asia/Kolkata"
    assert "credentials" not in out.engagement.recorded_report_metadata
    item = out.findings[0]
    assert item.technical_details == "The endpoint completed a TLS 1.0 handshake."
    assert item.impact == "A downgrade may expose session traffic."
    assert item.business_impact == (
        "Protected customer traffic may lose confidentiality."
    )
    assert item.exploitation == (
        "An on-path attacker may force weaker protocol negotiation."
    )
    assert item.reproduction_steps == [
        "Offer TLS 1.0",
        "Observe a successful handshake",
    ]
    assert item.root_cause == "The server policy still permits a deprecated protocol."
    assert item.preconditions == ["Network access to the TLS endpoint"]
    assert [event.event_type for event in item.closure.terminal_and_reopen_history] == [
        "remediated",
        "reopened",
        "resolved",
    ]
    assert item.closure.auto_resolution_coverage is not None
    assert item.closure.auto_resolution_coverage.recorded_coverage["assets"] == [
        "192.0.2.10"
    ]
    assert item.closure.auto_resolution_coverage.interpretation == (
        "coverage_evidence_not_patch_attestation"
    )
    assert "verified_retest_not_recorded" in item.closure.completeness_gaps
    assert [plan.id for plan in item.remediation.reviewed_plans] == [reviewed.id]
    assert "Baseline cryptographic policy." in item.remediation.recorded_recommendations
    assert item.compliance_mappings[0].control_id == "4.2.1"
    assert out.compliance_rollup.mapping_count == 1
    assert out.compliance_rollup.frameworks[0].framework_version == "4.0.1"
    assert out.compliance_rollup.frameworks[0].controls[0].recorded_results == [
        "not_satisfied"
    ]
    assert "compliance_mapping_assessment_status_absent" not in item.readiness_gaps
    assert item.current_sla.derived is True
    assert item.current_sla.historical is False
    assert item.current_sla.state == "untracked"
    assert "remediation_timestamp_absent" in item.readiness_gaps
    assert out.summary.by_severity_status["high"]["remediated"] == 1
    assert out.summary.terminal_by_severity["high"] == 1
    assert out.summary.open_by_severity["high"] == 0
    assert [
        profile.profile_id for profile in out.compliance_rollup.regulatory_profiles
    ] == ["cert-in-audit-guidelines-2025", "sebi-cscrf-2024"]


def test_report_document_includes_more_than_one_hundred_findings_without_truncation():
    engagement = _engagement()
    asset = _asset(engagement.id)
    findings = [
        _finding(
            engagement.id,
            asset.id,
            uuid.uuid4(),
            id=uuid.uuid5(uuid.NAMESPACE_URL, f"vedha-report-finding-{index}"),
            title=f"Recorded finding {index + 1}",
        )
        for index in range(101)
    ]

    out = build_report_document(
        engagement=engagement,
        finding_rows=[(finding, asset) for finding in findings],
        event_rows=[],
        remediation_plan_rows=[],
        resolution_runs={},
        generated_at=NOW,
        sla_windows={
            "critical": 24,
            "high": 72,
            "medium": 168,
            "low": 720,
            "info": 0,
        },
    )

    assert out.summary.total_findings == 101
    assert len(out.findings) == 101
    assert sum(out.summary.by_severity.values()) == len(out.findings)
    assert sum(out.summary.by_status.values()) == len(out.findings)
    assert out.findings[-1].title == "Recorded finding 101"


def test_report_distinguishes_initial_discovery_from_latest_observation_scan():
    engagement = _engagement()
    asset = _asset(engagement.id)
    initial_run_id = uuid.uuid4()
    latest_run_id = uuid.uuid4()
    initial_scan_id = uuid.uuid4()
    latest_scan_id = uuid.uuid4()
    initial_job_id = uuid.uuid4()
    latest_job_id = uuid.uuid4()
    finding = _finding(
        engagement.id,
        asset.id,
        None,
        status=FindingStatus.open,
        resolved_at=None,
        resolution_method=None,
        resolution_run_id=None,
        reopened_count=0,
        initial_detection_run_id=initial_run_id,
        detection_run_id=latest_run_id,
    )
    finding.evidence = {
        **finding.evidence,
        "action_tracking": {
            "non_closure_reason": "Waiting for the approved maintenance window",
            "planned_closure_at": "2026-10-05T22:00:00+05:30",
            "action_reference": "CHG-2026-1005",
            "recorded_at": "2026-09-27T08:00:00+05:30",
        },
    }
    initial_run = _run(
        initial_run_id,
        engagement.id,
        scan_result_id=initial_scan_id,
        started_at=NOW - timedelta(days=6),
        finished_at=NOW - timedelta(days=6) + timedelta(minutes=2),
        findings_new=1,
        findings_reaffirmed=0,
    )
    latest_run = _run(
        latest_run_id,
        engagement.id,
        scan_result_id=latest_scan_id,
        started_at=NOW - timedelta(days=2),
        finished_at=NOW - timedelta(days=2) + timedelta(minutes=2),
        findings_new=0,
        findings_reaffirmed=1,
    )
    initial_scan = _scan_result(
        initial_scan_id,
        engagement.id,
        job_id=initial_job_id,
        scan_type="network_vulnerability",
    )
    latest_scan = _scan_result(
        latest_scan_id,
        engagement.id,
        job_id=latest_job_id,
        scan_type="tls_configuration",
        created_at=NOW - timedelta(days=2, minutes=1),
    )

    out = build_report_document(
        engagement=engagement,
        finding_rows=[(finding, asset)],
        event_rows=[],
        remediation_plan_rows=[],
        resolution_runs={initial_run_id: initial_run, latest_run_id: latest_run},
        scan_results={initial_scan_id: initial_scan, latest_scan_id: latest_scan},
        generated_at=NOW,
        sla_windows={
            "critical": 24,
            "high": 72,
            "medium": 168,
            "low": 720,
            "info": 0,
        },
    )

    item = out.findings[0]
    assert item.initial_detection_run_id == initial_run_id
    assert item.detection_run_id == latest_run_id
    assert item.initial_detection_provenance is not None
    assert item.initial_detection_provenance.role == "initial_discovery"
    assert item.initial_detection_provenance.scan_result_id == initial_scan_id
    assert item.initial_detection_provenance.scan_job_id == initial_job_id
    assert item.initial_detection_provenance.scan_type == "network_vulnerability"
    assert item.latest_detection_provenance is not None
    assert item.latest_detection_provenance.role == "latest_observation"
    assert item.latest_detection_provenance.scan_result_id == latest_scan_id
    assert item.latest_detection_provenance.scan_job_id == latest_job_id
    assert item.latest_detection_provenance.scan_type == "tls_configuration"
    assert item.action_tracking.owner == "Platform"
    assert item.action_tracking.non_closure_reason == (
        "Waiting for the approved maintenance window"
    )
    assert item.action_tracking.planned_closure_at == (
        "2026-10-05T22:00:00+05:30"
    )
    assert "initial_detection_run_id_absent" not in item.readiness_gaps
    assert "latest_detection_run_id_absent" not in item.readiness_gaps


def test_historical_finding_does_not_mislabel_latest_run_as_discovery_run():
    engagement = _engagement()
    asset = _asset(engagement.id)
    latest_run_id = uuid.uuid4()
    finding = _finding(
        engagement.id,
        asset.id,
        None,
        status=FindingStatus.open,
        resolved_at=None,
        resolution_method=None,
        resolution_run_id=None,
        reopened_count=0,
        initial_detection_run_id=None,
        detection_run_id=latest_run_id,
    )
    latest_scan_id = uuid.uuid4()
    latest_run = _run(
        latest_run_id,
        engagement.id,
        scan_result_id=latest_scan_id,
    )
    latest_scan = _scan_result(latest_scan_id, engagement.id)

    out = build_report_document(
        engagement=engagement,
        finding_rows=[(finding, asset)],
        event_rows=[],
        remediation_plan_rows=[],
        resolution_runs={latest_run_id: latest_run},
        scan_results={latest_scan_id: latest_scan},
        generated_at=NOW,
        sla_windows={
            "critical": 24,
            "high": 72,
            "medium": 168,
            "low": 720,
            "info": 0,
        },
    )

    item = out.findings[0]
    assert item.initial_detection_provenance is None
    assert item.latest_detection_provenance is not None
    assert "initial_detection_run_id_absent" in item.readiness_gaps


def test_missing_compliance_and_manual_closure_proof_are_explicit_gaps():
    engagement = _engagement()
    asset = _asset(engagement.id)
    finding = _finding(
        engagement.id,
        asset.id,
        None,
        evidence={"output": "initial observation"},
        resolution_method="manual",
        resolution_run_id=None,
        reopened_count=0,
    )
    event = _event(
        finding.id,
        "remediated",
        NOW - timedelta(days=1),
        detail={"reason": "Marked fixed"},
    )
    out = build_report_document(
        engagement=engagement,
        finding_rows=[(finding, asset)],
        event_rows=[event],
        remediation_plan_rows=[],
        resolution_runs={},
        generated_at=NOW,
        sla_windows={"critical": 24, "high": 72, "medium": 168, "low": 720, "info": 0},
    )
    item = out.findings[0]
    assert "post_fix_evidence_absent" in item.closure.completeness_gaps
    assert "verified_retest_not_recorded" in item.closure.completeness_gaps
    assert "compliance_mappings_absent" in item.readiness_gaps
    assert out.compliance_rollup.mapping_count == 0
    assert out.compliance_rollup.gap is not None
    assert out.readiness.complete is False


def test_opaque_compliance_reference_is_preserved_but_flagged_as_incomplete():
    engagement = _engagement()
    asset = _asset(engagement.id)
    finding = _finding(
        engagement.id,
        asset.id,
        None,
        status=FindingStatus.open,
        resolved_at=None,
        resolution_method=None,
        resolution_run_id=None,
        reopened_count=0,
        evidence={
            "output": "recorded observation",
            "compliance": ["PCI DSS 4.0.1 requirement 4.2.1"],
        },
    )
    out = build_report_document(
        engagement=engagement,
        finding_rows=[(finding, asset)],
        event_rows=[],
        remediation_plan_rows=[],
        resolution_runs={},
        generated_at=NOW,
        sla_windows={
            "critical": 24,
            "high": 72,
            "medium": 168,
            "low": 720,
            "info": 0,
        },
    )
    item = out.findings[0]
    assert item.compliance_mappings[0].recorded_reference == (
        "PCI DSS 4.0.1 requirement 4.2.1"
    )
    assert "compliance_mapping_framework_absent" in item.readiness_gaps
    assert "compliance_mapping_control_id_absent" in item.readiness_gaps
    assert "compliance_mapping_id_absent" in item.readiness_gaps
    assert "compliance_mapping_assessment_status_absent" in item.readiness_gaps


def test_legacy_result_is_accepted_as_assessment_status_readiness_fallback():
    engagement = _engagement()
    asset = _asset(engagement.id)
    finding = _finding(
        engagement.id,
        asset.id,
        None,
        status=FindingStatus.open,
        resolved_at=None,
        resolution_method=None,
        resolution_run_id=None,
        reopened_count=0,
    )
    recorded_mapping = dict(finding.evidence["compliance_mappings"][0])
    recorded_mapping.pop("assessment_status")
    finding.evidence = {
        **finding.evidence,
        "compliance_mappings": [recorded_mapping],
    }
    out = build_report_document(
        engagement=engagement,
        finding_rows=[(finding, asset)],
        event_rows=[],
        remediation_plan_rows=[],
        resolution_runs={},
        generated_at=NOW,
        sla_windows={
            "critical": 24,
            "high": 72,
            "medium": 168,
            "low": 720,
            "info": 0,
        },
    )
    assert (
        "compliance_mapping_assessment_status_absent"
        not in out.findings[0].readiness_gaps
    )
    assert out.compliance_rollup.frameworks[0].controls[0].recorded_results == ["fail"]


def test_customer_delivery_metadata_gaps_include_all_document_controls():
    engagement = _engagement(
        rules_of_engagement={
            "client": "Example Corp",
            "assessor": "Vedha Security",
            "report_metadata": {
                "version": "1.0",
                "classification": "Confidential",
                "methodology": {"password": "must-not-leak"},
            },
        }
    )
    out = build_report_document(
        engagement=engagement,
        finding_rows=[],
        event_rows=[],
        remediation_plan_rows=[],
        resolution_runs={},
        generated_at=NOW,
        sla_windows={
            "critical": 24,
            "high": 72,
            "medium": 168,
            "low": 720,
            "info": 0,
        },
    )
    assert {
        "report_document_status_absent",
        "report_prepared_by_absent",
        "report_prepared_at_absent",
        "report_reviewed_by_absent",
        "report_reviewed_at_absent",
        "report_approved_by_absent",
        "report_approved_at_absent",
        "report_issue_date_absent",
        "report_reporting_period_absent",
        "report_methodology_absent",
        "report_risk_rating_method_absent",
        "report_tools_used_absent",
        "report_evidence_retention_policy_absent",
        "report_timezone_absent",
        "report_limitations_absent",
        "regulatory_profiles_absent",
    }.issubset(out.readiness.report_gaps)
    assert "methodology" not in out.engagement.recorded_report_metadata


def test_invalid_report_profile_and_mapping_time_metadata_blocks_readiness():
    engagement = _engagement()
    engagement.rules_of_engagement["report_metadata"]["report_timezone"] = (
        "Not/A-Time-Zone"
    )
    engagement.rules_of_engagement["report_metadata"]["issue_date"] = (
        "2026-09-26 10:00:00"
    )
    engagement.rules_of_engagement["regulatory_profiles"][0]["selected_at"] = (
        "2026-09-18 10:00:00"
    )
    engagement.rules_of_engagement["regulatory_profiles"][0]["source_url"] = (
        "javascript:alert(1)"
    )
    asset = _asset(engagement.id)
    finding = _finding(
        engagement.id,
        asset.id,
        None,
        status=FindingStatus.open,
        resolved_at=None,
        resolution_method=None,
        resolution_run_id=None,
        reopened_count=0,
    )
    finding.evidence["compliance_mappings"][0]["mapped_at"] = "not-rfc3339"
    finding.evidence["compliance_mappings"][0]["source_url"] = "file:///tmp/x"

    out = build_report_document(
        engagement=engagement,
        finding_rows=[(finding, asset)],
        event_rows=[],
        remediation_plan_rows=[],
        resolution_runs={},
        generated_at=NOW,
        sla_windows={
            "critical": 24,
            "high": 72,
            "medium": 168,
            "low": 720,
            "info": 0,
        },
    )

    assert "report_timezone_invalid_iana" in out.readiness.report_gaps
    assert "report_issue_date_invalid_rfc3339" in out.readiness.report_gaps
    assert "regulatory_profile_selected_at_invalid_rfc3339" in (
        out.readiness.report_gaps
    )
    assert "regulatory_profile_source_url_invalid" in out.readiness.report_gaps
    assert "compliance_mapping_mapped_at_invalid_rfc3339" in (
        out.findings[0].readiness_gaps
    )
    assert "compliance_mapping_source_url_invalid" in (
        out.findings[0].readiness_gaps
    )


def test_closure_evidence_provenance_gaps_are_not_hidden():
    engagement = _engagement()
    asset = _asset(engagement.id)
    finding = _finding(
        engagement.id,
        asset.id,
        None,
        resolution_method="manual",
        resolution_run_id=None,
        reopened_count=0,
    )
    event = _event(
        finding.id,
        "remediated",
        NOW - timedelta(days=1),
        detail={
            "reason": "Operator marked the issue fixed",
            "post_fix_evidence": {"content": "TLS 1.0 was not offered"},
            "retest_result": "passed",
        },
    )
    out = build_report_document(
        engagement=engagement,
        finding_rows=[(finding, asset)],
        event_rows=[event],
        remediation_plan_rows=[],
        resolution_runs={},
        generated_at=NOW,
        sla_windows={
            "critical": 24,
            "high": 72,
            "medium": 168,
            "low": 720,
            "info": 0,
        },
    )
    gaps = out.findings[0].closure.completeness_gaps
    assert "post_fix_evidence_absent" not in gaps
    assert "closure_evidence_capture_time_absent" in gaps
    assert "closure_evidence_source_absent" in gaps
    assert "closure_evidence_integrity_hash_absent" in gaps


def test_complete_manual_closure_packet_has_no_closure_gaps():
    engagement = _engagement()
    asset = _asset(engagement.id)
    finding = _finding(
        engagement.id,
        asset.id,
        None,
        resolution_method="manual",
        resolution_run_id=None,
        reopened_count=0,
    )
    before = [
        {
            "label": "Before fix",
            "content": "TLS 1.0 accepted",
            "tool": "testssl",
            "captured_at": "2026-09-25T06:30:00Z",
            "sha256": "d" * 64,
        }
    ]
    after = [
        {
            "label": "After fix",
            "content": "TLS 1.0 rejected",
            "tool": "testssl",
            "captured_at": "2026-09-25T07:30:00Z",
            "sha256": "e" * 64,
        }
    ]
    event = _event(
        finding.id,
        "remediated",
        NOW - timedelta(days=1),
        detail={
            "reason": "Authorized retest passed",
            "reviewed_by": "reviewer@example.test",
            "before_evidence": before,
            "post_fix_evidence": after,
            "retest": {
                "passed": True,
                "requested_at": "2026-09-25T07:00:00Z",
                "started_at": "2026-09-25T07:10:00Z",
                "completed_at": "2026-09-25T07:40:00Z",
                "verified_at": "2026-09-25T08:00:00Z",
                "tested_by": "tester@example.test",
                "verified_by": "verifier@example.test",
                "scope": {"asset_ids": [str(asset.id)]},
                "vantage_point": "external-probe-1",
                "authentication_context": "unauthenticated",
                "method": "authorized protocol negotiation",
                "tool_configuration": {"minimum_protocol": "TLS1.0"},
                "expected_result": "TLS 1.0 is rejected",
                "actual_result": "TLS 1.0 was rejected",
                "coverage_comparison": {"before": 1, "after": 0},
                "change_reference": "CHG-2026-0912",
                "residual_risk": "TLS 1.2 remains enabled by design",
            },
        },
    )
    out = build_report_document(
        engagement=engagement,
        finding_rows=[(finding, asset)],
        event_rows=[event],
        remediation_plan_rows=[],
        resolution_runs={},
        generated_at=NOW,
        sla_windows={
            "critical": 24,
            "high": 72,
            "medium": 168,
            "low": 720,
            "info": 0,
        },
    )
    closure = out.findings[0].closure
    assert closure.completeness_gaps == []
    assert closure.reviewed_by == "reviewer@example.test"
    assert closure.retest is not None
    assert closure.retest.passed is True
    assert closure.retest.tested_by == "tester@example.test"
    assert closure.retest.verified_by == "verifier@example.test"
    assert closure.retest.change_reference == "CHG-2026-0912"
    assert closure.retest.before_evidence.artifacts[0].content == "TLS 1.0 accepted"
    assert closure.retest.after_evidence.artifacts[0].content == "TLS 1.0 rejected"


def test_reopened_finding_keeps_prior_auto_resolution_coverage_visible():
    engagement = _engagement()
    run_id = uuid.uuid4()
    asset = _asset(engagement.id)
    finding = _finding(
        engagement.id,
        asset.id,
        run_id,
        status=FindingStatus.open,
        resolved_at=None,
        resolution_method=None,
        resolution_run_id=None,
        reopened_count=1,
    )
    events = [
        _event(
            finding.id,
            "resolved",
            NOW - timedelta(days=2),
            detail={
                "method": "auto",
                "run_id": str(run_id),
                "reason": "coverage-proven clean",
            },
        ),
        _event(
            finding.id,
            "reopened",
            NOW - timedelta(days=1),
            detail={"reason": "Issue observed again"},
        ),
    ]
    out = build_report_document(
        engagement=engagement,
        finding_rows=[(finding, asset)],
        event_rows=events,
        remediation_plan_rows=[],
        resolution_runs={run_id: _run(run_id, engagement.id)},
        generated_at=NOW,
        sla_windows={
            "critical": 24,
            "high": 72,
            "medium": 168,
            "low": 720,
            "info": 0,
        },
    )
    closure = out.findings[0].closure
    assert closure.current_disposition == "open"
    assert closure.is_terminal is False
    assert closure.resolution_method == "auto"
    assert closure.resolution_run_id == run_id
    assert closure.resolved_at == NOW - timedelta(days=2)
    assert closure.auto_resolution_coverage is not None
    assert closure.auto_resolution_coverage.run_id == run_id


@pytest.mark.asyncio
async def test_loader_scopes_engagement_lookup_to_tenant():
    db = MagicMock()
    db.execute = AsyncMock(return_value=MagicMock(scalar_one_or_none=lambda: None))
    tenant_id = uuid.uuid4()
    result = await load_report_document(
        db,
        tenant_id=tenant_id,
        engagement_id=uuid.uuid4(),
        generated_at=NOW,
    )
    assert result is None
    sql = str(db.execute.await_args.args[0])
    assert "engagements.tenant_id" in sql
    assert "engagements.id" in sql


@pytest.mark.asyncio
async def test_route_returns_404_for_cross_tenant_or_missing_engagement(monkeypatch):
    from app.routers import report_document as report_router

    monkeypatch.setattr(
        report_router,
        "load_report_document",
        AsyncMock(return_value=None),
    )
    user = SimpleNamespace(tenant_id=uuid.uuid4())
    with pytest.raises(HTTPException) as exc:
        await report_router.get_report_document(uuid.uuid4(), MagicMock(), user)
    assert exc.value.status_code == 404


@pytest.mark.asyncio
async def test_route_uses_exact_utc_generation_time_and_tenant(monkeypatch):
    from app.routers import report_document as report_router

    document = object()
    loader = AsyncMock(return_value=document)
    monkeypatch.setattr(report_router, "load_report_document", loader)
    user = SimpleNamespace(tenant_id=uuid.uuid4())
    engagement_id = uuid.uuid4()

    result = await report_router.get_report_document(engagement_id, MagicMock(), user)

    assert result is document
    call = loader.await_args.kwargs
    assert call["tenant_id"] == user.tenant_id
    assert call["engagement_id"] == engagement_id
    assert call["generated_at"].tzinfo is timezone.utc


def test_report_document_router_is_mounted():
    from app.main import app

    paths = {getattr(route, "path", None) for route in app.routes}
    assert "/engagements/{engagement_id}/report-document" in paths

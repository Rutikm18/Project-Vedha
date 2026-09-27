"""Build the canonical engagement report from recorded platform data.

This module is intentionally deterministic and read-only.  It may normalize
recorded JSON into a stable shape and calculate clearly-labelled current SLA
projections, but it never generates missing narrative, timestamps, evidence, or
compliance mappings.
"""

from __future__ import annotations

import uuid
from collections import Counter, defaultdict
from datetime import datetime, timezone
import re
from typing import Any, Iterable, Literal
from urllib.parse import urlparse
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.asset import Asset
from app.models.detection_run import DetectionRun
from app.models.engagement import Engagement
from app.models.finding import Finding
from app.models.finding_event import FindingEvent
from app.models.remediation_plan import RemediationPlan
from app.models.scan_result import ScanResult
from app.models.sla_policy import SlaPolicy
from app.schemas.finding import FindingEventOut
from app.schemas.report_document import (
    ReportActionTracking,
    ReportAsset,
    ReportAutoResolutionCoverage,
    ReportClosureProjection,
    ReportComplianceControlRollup,
    ReportComplianceFrameworkRollup,
    ReportComplianceMapping,
    ReportComplianceRollup,
    ReportDocument,
    ReportDocumentControl,
    ReportDetectionRunProvenance,
    ReportEngagement,
    ReportEvidence,
    ReportEvidenceArtifact,
    ReportFinding,
    ReportReadiness,
    ReportRegulatoryProfile,
    ReportRemediation,
    ReportRemediationPlan,
    ReportRetestRecord,
    ReportSlaProjection,
    ReportSummary,
    ReportVerification,
)
from app.services import finding_events, sla
from app.services.finding_scan_provenance import (
    SCAN_PROVENANCE_KEY,
    SCAN_PROVENANCE_RECORDER,
    SCAN_PROVENANCE_VERSION,
)


_TERMINAL_STATUSES = {"remediated", "accepted", "fp"}
_TERMINAL_EVENT_TYPES = {"remediated", "resolved", "accepted", "false_positive"}
_CLOSURE_HISTORY_TYPES = _TERMINAL_EVENT_TYPES | {"reopened"}
_REPORT_METADATA_KEYS = {
    "version",
    "document_status",
    "classification",
    "prepared_by",
    "prepared_at",
    "reviewed_by",
    "reviewed_at",
    "approved_by",
    "approved_at",
    "issue_date",
    "reporting_period",
    "methodology",
    "risk_rating_method",
    "testing_narrative",
    "tools_used",
    "segmentation_results",
    "environment_cleanup",
    "evidence_retention_policy",
    "distribution",
    "report_timezone",
    "limitations",
}
_COMPLIANCE_KEYS = ("compliance_mappings", "framework_mappings", "compliance")
_RFC3339_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$"
)
_SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")


def _value(value: Any) -> Any:
    return getattr(value, "value", value)


def _text(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, (str, int, float, bool)):
        rendered = str(value).strip()
        return rendered or None
    return None


def _recorded_string(value: Any) -> str | None:
    """Return a recorded string byte-for-byte; do not trim or synthesize it."""
    return value if isinstance(value, str) else None


def _recorded_string_list(value: Any) -> list[str] | None:
    if value is None:
        return None
    if isinstance(value, list) and all(isinstance(item, str) for item in value):
        return list(value)
    return None


def _string_list(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value.strip()] if value.strip() else []
    if not isinstance(value, list):
        return []
    return [text for item in value if (text := _text(item))]


def _dedupe(values: Iterable[str]) -> list[str]:
    return list(dict.fromkeys(value for value in values if value))


def _artifact(item: Any, index: int) -> ReportEvidenceArtifact:
    if not isinstance(item, dict):
        return ReportEvidenceArtifact(
            index=index,
            label=f"Evidence artifact {index}",
            content=item,
        )

    provenance = item.get(SCAN_PROVENANCE_KEY)
    provenance = (
        provenance
        if isinstance(provenance, dict)
        and provenance.get("recorded_by") == SCAN_PROVENANCE_RECORDER
        and provenance.get("schema_version") == SCAN_PROVENANCE_VERSION
        else {}
    )
    observation = provenance.get("latest") or provenance.get("initial") or {}
    observation = observation if isinstance(observation, dict) else {}
    source = _text(
        item.get("source")
        or item.get("source_scanner")
        or item.get("scan_type")
        or observation.get("source")
        or observation.get("scan_type")
    )
    tool = _text(
        item.get("tool")
        or item.get("engine")
        or item.get("scanner")
        or observation.get("tool")
    )
    label = _text(item.get("label")) or tool or source or f"Evidence artifact {index}"
    content = item
    for key in ("content", "output", "value"):
        if key in item:
            content = item[key]
            break
    return ReportEvidenceArtifact(
        index=index,
        label=label,
        content=content,
        evidence_type=_text(item.get("evidence_type") or item.get("type")),
        tool=tool,
        source=source,
        command=_text(item.get("command") or item.get("curl_command")),
        timestamp=_text(item.get("timestamp") or observation.get("recorded_at")),
        captured_at=_text(item.get("captured_at") or item.get("capturedAt")),
        captured_by=_text(item.get("captured_by") or item.get("capturedBy")),
        source_host=_text(item.get("source_host") or item.get("sourceHost")),
        sha256=_text(item.get("sha256")),
        scan_result_id=_text(observation.get("scan_result_id")),
        scan_job_id=_text(observation.get("scan_job_id")),
        detection_run_id=_text(observation.get("detection_run_id")),
        timestamp_basis=_text(observation.get("timestamp_basis")),
    )


def _valid_rfc3339(value: str) -> bool:
    if not _RFC3339_RE.fullmatch(value):
        return False
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None and parsed.utcoffset() is not None


def _valid_http_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def _valid_iana_timezone(value: str) -> bool:
    try:
        ZoneInfo(value)
    except (ZoneInfoNotFoundError, ValueError):
        return False
    return True


def normalize_evidence(recorded: Any) -> ReportEvidence:
    """Normalize presentation fields while preserving the exact recorded JSON."""
    candidates: list[Any]
    if isinstance(recorded, list):
        candidates = recorded
    elif isinstance(recorded, dict) and isinstance(recorded.get("artifacts"), list):
        candidates = recorded["artifacts"]
    elif recorded is None or recorded == {} or recorded == []:
        candidates = []
    else:
        candidates = [recorded]

    artifacts = [
        _artifact(item, index) for index, item in enumerate(candidates, start=1)
    ]
    gaps: list[str] = []
    if not artifacts:
        gaps.append("evidence_absent")
    else:
        for artifact in artifacts:
            timestamps = [
                value
                for value in (artifact.timestamp, artifact.captured_at)
                if value is not None
            ]
            if not timestamps:
                gaps.append(f"evidence_artifact_{artifact.index}_capture_time_absent")
            elif not any(_valid_rfc3339(value) for value in timestamps):
                gaps.append(
                    f"evidence_artifact_{artifact.index}_capture_time_invalid_rfc3339"
                )
            if not (artifact.tool or artifact.source):
                gaps.append(f"evidence_artifact_{artifact.index}_source_absent")
            if not artifact.sha256:
                gaps.append(f"evidence_artifact_{artifact.index}_sha256_absent")
            elif not _SHA256_RE.fullmatch(artifact.sha256):
                gaps.append(f"evidence_artifact_{artifact.index}_sha256_invalid")

        if any(gap.endswith("capture_time_absent") for gap in gaps):
            gaps.append("evidence_capture_time_absent")
        if any(gap.endswith("capture_time_invalid_rfc3339") for gap in gaps):
            gaps.append("evidence_capture_time_invalid_rfc3339")
        if any(gap.endswith("source_absent") for gap in gaps):
            gaps.append("evidence_source_absent")
        if any(gap.endswith("sha256_absent") for gap in gaps):
            gaps.append("evidence_integrity_hash_absent")
        if any(gap.endswith("sha256_invalid") for gap in gaps):
            gaps.append("evidence_integrity_hash_invalid")
    return ReportEvidence(raw=recorded, artifacts=artifacts, gaps=gaps)


def _compliance_items(evidence: Any) -> list[tuple[str, Any]]:
    if not isinstance(evidence, dict):
        return []
    out: list[tuple[str, Any]] = []
    for source_key in _COMPLIANCE_KEYS:
        recorded = evidence.get(source_key)
        if recorded is None:
            continue
        if isinstance(recorded, dict) and isinstance(recorded.get("mappings"), list):
            out.extend((source_key, item) for item in recorded["mappings"])
        elif isinstance(recorded, list):
            out.extend((source_key, item) for item in recorded)
        else:
            out.append((source_key, recorded))
    return out


def extract_compliance_mappings(evidence: Any) -> list[ReportComplianceMapping]:
    """Read explicit mapping fields only; strings remain opaque references."""
    mappings: list[ReportComplianceMapping] = []
    for source_key, item in _compliance_items(evidence):
        if not isinstance(item, dict):
            mappings.append(
                ReportComplianceMapping(
                    source_key=source_key,
                    recorded_reference=_text(item),
                    raw=item,
                )
            )
            continue
        mappings.append(
            ReportComplianceMapping(
                source_key=source_key,
                mapping_id=_recorded_string(item.get("mapping_id")),
                framework=_text(item.get("framework") or item.get("standard")),
                framework_version=_text(
                    item.get("framework_version") or item.get("version")
                ),
                release=_recorded_string(item.get("release")),
                profile=_recorded_string(item.get("profile")),
                control_id=_text(
                    item.get("control_id")
                    or item.get("controlId")
                    or item.get("control")
                ),
                control_title=_text(item.get("control_title") or item.get("title")),
                relationship=_text(
                    item.get("relationship") or item.get("mapping_type")
                ),
                rationale=_text(item.get("rationale")),
                applicability=_text(item.get("applicability")),
                assessment_status=_recorded_string(item.get("assessment_status")),
                result=_text(item.get("result") or item.get("status")),
                test_ids=_recorded_string_list(item.get("test_ids")),
                scope=item.get("scope"),
                context=item.get("context"),
                source_url=_recorded_string(item.get("source_url")),
                mapping_source=_recorded_string(item.get("mapping_source")),
                mapping_version=_recorded_string(item.get("mapping_version")),
                mapped_by=_recorded_string(item.get("mapped_by")),
                mapped_at=_recorded_string(item.get("mapped_at")),
                reviewed_by=_recorded_string(item.get("reviewed_by")),
                reviewed_at=_recorded_string(item.get("reviewed_at")),
                limitations=item.get("limitations"),
                customer_statement=item.get("customer_statement"),
                assessor=_text(item.get("assessor")),
                assessed_at=_text(item.get("assessed_at")),
                evidence_references=_string_list(
                    item.get("evidence_references") or item.get("evidence_refs")
                ),
                recorded_reference=_text(item.get("reference")),
                raw=item,
            )
        )
    return mappings


def extract_regulatory_profiles(recorded: Any) -> list[ReportRegulatoryProfile]:
    """Normalize explicitly selected applicability profiles without inferring one."""
    if not isinstance(recorded, list):
        return []
    profiles: list[ReportRegulatoryProfile] = []
    for item in recorded:
        if not isinstance(item, dict):
            profiles.append(ReportRegulatoryProfile(recorded_reference=_text(item)))
            continue
        profiles.append(
            ReportRegulatoryProfile(
                profile_id=_recorded_string(item.get("profile_id")),
                name=_recorded_string(item.get("name")),
                version=_recorded_string(item.get("version")),
                jurisdiction=_recorded_string(item.get("jurisdiction")),
                applicability=_recorded_string(item.get("applicability")),
                rationale=_recorded_string(item.get("rationale")),
                source_url=_recorded_string(item.get("source_url")),
                scope=item.get("scope"),
                selected_by=_recorded_string(item.get("selected_by")),
                selected_at=_recorded_string(item.get("selected_at")),
                reviewed_by=_recorded_string(item.get("reviewed_by")),
                reviewed_at=_recorded_string(item.get("reviewed_at")),
                limitations=item.get("limitations"),
                recorded_reference=_recorded_string(item.get("reference")),
            )
        )
    return profiles


def _compliance_gaps(mappings: list[ReportComplianceMapping]) -> list[str]:
    if not mappings:
        return ["compliance_mappings_absent"]
    required = {
        "mapping_id": "compliance_mapping_id_absent",
        "framework": "compliance_mapping_framework_absent",
        "framework_version": "compliance_mapping_version_absent",
        "control_id": "compliance_mapping_control_id_absent",
        "control_title": "compliance_mapping_control_title_absent",
        "relationship": "compliance_mapping_relationship_absent",
        "rationale": "compliance_mapping_rationale_absent",
        "applicability": "compliance_mapping_applicability_absent",
        "scope": "compliance_mapping_scope_absent",
        "source_url": "compliance_mapping_source_url_absent",
        "mapping_source": "compliance_mapping_source_absent",
        "mapping_version": "compliance_mapping_source_version_absent",
        "mapped_by": "compliance_mapping_mapped_by_absent",
        "mapped_at": "compliance_mapping_mapped_at_absent",
        "reviewed_by": "compliance_mapping_reviewed_by_absent",
        "reviewed_at": "compliance_mapping_reviewed_at_absent",
        "limitations": "compliance_mapping_limitations_absent",
        "customer_statement": "compliance_mapping_customer_statement_absent",
        "assessor": "compliance_mapping_assessor_absent",
        "assessed_at": "compliance_mapping_assessed_at_absent",
        "evidence_references": "compliance_mapping_evidence_references_absent",
    }
    gaps = [
        gap
        for field, gap in required.items()
        if any(not getattr(mapping, field) for mapping in mappings)
    ]
    # assessment_status is canonical; legacy result remains an accepted recorded
    # fallback while older rows are migrated.
    if any(not (mapping.assessment_status or mapping.result) for mapping in mappings):
        gaps.append("compliance_mapping_assessment_status_absent")
    for field in ("mapped_at", "reviewed_at", "assessed_at"):
        if any(
            (value := getattr(mapping, field)) is not None
            and not _valid_rfc3339(value)
            for mapping in mappings
        ):
            gaps.append(f"compliance_mapping_{field}_invalid_rfc3339")
    if any(
        mapping.source_url is not None and not _valid_http_url(mapping.source_url)
        for mapping in mappings
    ):
        gaps.append("compliance_mapping_source_url_invalid")
    return gaps


def _event_dict(row: FindingEvent) -> dict[str, Any]:
    return {
        "id": row.id,
        "event_type": row.event_type,
        "actor": row.actor,
        "actor_type": row.actor_type,
        "from_status": row.from_status,
        "to_status": row.to_status,
        "detail": row.detail,
        "occurred_at": row.occurred_at,
        "synthesized": False,
    }


def _timeline(finding: Finding, rows: list[FindingEvent]) -> list[FindingEventOut]:
    stored = [_event_dict(row) for row in rows]
    merged = finding_events.merge_timeline(
        stored,
        finding_events.synthesize_events(finding),
    )
    return [FindingEventOut(**event) for event in merged]


def _closure_evidence(event: FindingEventOut | None) -> ReportEvidence:
    if event is None or not isinstance(event.detail, dict):
        return normalize_evidence(None)
    detail = event.detail
    for key in ("closure_evidence", "post_fix_evidence", "retest_evidence", "evidence"):
        if key in detail:
            return normalize_evidence(detail[key])
    # A structured retest object is recorded evidence. A reason string alone is
    # deliberately not promoted to evidence.
    if isinstance(detail.get("retest"), (dict, list)):
        return normalize_evidence(detail["retest"])
    return normalize_evidence(None)


def _retest_record(event: FindingEventOut | None) -> ReportRetestRecord | None:
    if event is None or not isinstance(event.detail, dict):
        return None
    detail = event.detail
    retest = detail.get("retest") if isinstance(detail.get("retest"), dict) else {}
    before = (
        detail.get("before_evidence")
        or detail.get("pre_fix_evidence")
        or retest.get("before_evidence")
    )
    after = (
        detail.get("post_fix_evidence")
        or detail.get("after_evidence")
        or detail.get("retest_evidence")
        or retest.get("after_evidence")
    )
    if not retest and before in (None, "", [], {}) and after in (None, "", [], {}):
        return None

    def recorded(*keys: str) -> Any:
        for key in keys:
            if key in retest:
                return retest[key]
            if key in detail:
                return detail[key]
        return None

    passed = recorded("passed", "retest_passed")
    return ReportRetestRecord(
        passed=passed if isinstance(passed, bool) else None,
        requested_at=_text(recorded("requested_at", "retest_requested_at")),
        started_at=_text(recorded("started_at", "retest_started_at")),
        completed_at=_text(recorded("completed_at", "retest_completed_at")),
        verified_at=_text(recorded("verified_at", "retest_verified_at")),
        tested_by=_text(recorded("tested_by", "tester")),
        verified_by=_text(recorded("verified_by", "verifier")),
        scope=recorded("scope", "retest_scope"),
        vantage_point=_text(recorded("vantage_point", "vantage")),
        authentication_context=_text(
            recorded("authentication_context", "auth_context", "authentication")
        ),
        method=_text(recorded("method", "retest_method")),
        tool_configuration=recorded("tool_configuration", "tool_config"),
        expected_result=recorded("expected_result", "expected"),
        actual_result=recorded("actual_result", "retest_result", "actual"),
        coverage_comparison=recorded("coverage_comparison", "coverage"),
        change_reference=_text(recorded("change_reference", "change_ref", "ticket")),
        residual_risk=recorded("residual_risk"),
        before_evidence=normalize_evidence(before),
        after_evidence=normalize_evidence(after),
    )


def _coverage(run: DetectionRun | None) -> ReportAutoResolutionCoverage | None:
    if run is None:
        return None
    stats = run.stats if isinstance(run.stats, dict) else {}
    return ReportAutoResolutionCoverage(
        run_id=run.id,
        scan_result_id=run.scan_result_id,
        trigger=run.trigger,
        status=run.status,
        vuln_db_version=run.vuln_db_version,
        vuln_db_fetched_at=run.vuln_db_fetched_at,
        started_at=run.started_at,
        finished_at=run.finished_at,
        facts_count=run.facts_count,
        findings_new=run.findings_new,
        findings_reaffirmed=run.findings_reaffirmed,
        findings_current=run.findings_current,
        recorded_coverage=stats.get("coverage"),
        recorded_stats=stats,
    )


def _detection_provenance(
    run: DetectionRun | None,
    scan_result: ScanResult | None,
    *,
    role: Literal["initial_discovery", "latest_observation"],
) -> ReportDetectionRunProvenance | None:
    if run is None:
        return None
    stats = run.stats if isinstance(run.stats, dict) else {}
    return ReportDetectionRunProvenance(
        role=role,
        run_id=run.id,
        scan_result_id=run.scan_result_id,
        scan_job_id=scan_result.job_id if scan_result is not None else None,
        scan_attempt_id=scan_result.attempt_id if scan_result is not None else None,
        agent_id=scan_result.agent_id if scan_result is not None else None,
        scan_type=scan_result.scan_type if scan_result is not None else None,
        scan_result_checksum=(
            scan_result.content_checksum if scan_result is not None else None
        ),
        scan_result_validation_state=(
            scan_result.validation_state if scan_result is not None else None
        ),
        scan_result_recorded_at=(
            scan_result.created_at if scan_result is not None else None
        ),
        trigger=run.trigger,
        status=run.status,
        vuln_db_version=run.vuln_db_version,
        vuln_db_fetched_at=run.vuln_db_fetched_at,
        started_at=run.started_at,
        finished_at=run.finished_at,
        facts_count=run.facts_count,
        findings_new=run.findings_new,
        findings_reaffirmed=run.findings_reaffirmed,
        findings_current=run.findings_current,
        recorded_coverage=stats.get("coverage"),
        recorded_stats=stats,
    )


def _detection_provenance_gaps(
    prefix: str,
    run_id: uuid.UUID | None,
    provenance: ReportDetectionRunProvenance | None,
) -> list[str]:
    if run_id is None:
        return [f"{prefix}_detection_run_id_absent"]
    if provenance is None:
        return [f"{prefix}_detection_run_record_unavailable"]
    gaps: list[str] = []
    if provenance.scan_result_id is None:
        gaps.append(f"{prefix}_scan_result_id_absent")
    elif provenance.scan_result_recorded_at is None:
        gaps.append(f"{prefix}_scan_result_record_unavailable")
    if provenance.scan_job_id is None:
        gaps.append(f"{prefix}_scan_job_id_absent")
    if not provenance.scan_type:
        gaps.append(f"{prefix}_scan_type_absent")
    if not provenance.scan_result_checksum:
        gaps.append(f"{prefix}_scan_result_checksum_absent")
    return gaps


def _has_detail(detail: dict[str, Any], *keys: str) -> bool:
    return any(detail.get(key) not in (None, "", [], {}) for key in keys)


def _uuid(value: Any) -> uuid.UUID | None:
    if isinstance(value, uuid.UUID):
        return value
    if not isinstance(value, str):
        return None
    try:
        return uuid.UUID(value)
    except ValueError:
        return None


def _verified_retest_with_before_after(detail: dict[str, Any]) -> bool:
    """Recognize only an explicit passed flag plus both evidence states."""
    retest = detail.get("retest") if isinstance(detail.get("retest"), dict) else {}
    passed = detail.get("retest_passed") is True or retest.get("passed") is True
    before = (
        detail.get("before_evidence")
        or detail.get("pre_fix_evidence")
        or retest.get("before_evidence")
    )
    after = (
        detail.get("after_evidence")
        or detail.get("post_fix_evidence")
        or retest.get("after_evidence")
    )
    return (
        passed
        and before not in (None, "", [], {})
        and after
        not in (
            None,
            "",
            [],
            {},
        )
    )


def _retest_value(detail: dict[str, Any], *keys: str) -> Any:
    retest = detail.get("retest") if isinstance(detail.get("retest"), dict) else {}
    for key in keys:
        if key in detail:
            return detail[key]
        if key in retest:
            return retest[key]
    return None


def _present(value: Any) -> bool:
    return value not in (None, "", [], {})


def _manual_closure_gaps(
    detail: dict[str, Any], closed_at: datetime | None
) -> list[str]:
    gaps: list[str] = []
    if not _present(_retest_value(detail, "before_evidence", "pre_fix_evidence")):
        gaps.append("before_fix_evidence_absent")
    if not _present(
        _retest_value(
            detail,
            "after_evidence",
            "post_fix_evidence",
            "retest_evidence",
        )
    ):
        gaps.append("post_fix_evidence_absent")
    if not _verified_retest_with_before_after(detail):
        gaps.append("verified_retest_not_recorded")

    required = {
        "tester_absent": ("tested_by", "tester"),
        "verifier_absent": ("verified_by", "verifier"),
        "retest_scope_absent": ("retest_scope", "scope"),
        "retest_vantage_point_absent": ("vantage_point", "vantage"),
        "retest_authentication_context_absent": (
            "authentication_context",
            "auth_context",
            "authentication",
        ),
        "retest_method_absent": ("retest_method", "method"),
        "retest_tool_configuration_absent": (
            "tool_configuration",
            "tool_config",
        ),
        "retest_expected_result_absent": ("expected_result", "expected"),
        "retest_actual_result_absent": (
            "actual_result",
            "retest_result",
            "actual",
        ),
        "retest_coverage_comparison_absent": (
            "coverage_comparison",
            "coverage",
        ),
        "change_reference_absent": ("change_reference", "change_ref", "ticket"),
        "residual_risk_absent": ("residual_risk",),
    }
    for gap, keys in required.items():
        if not _present(_retest_value(detail, *keys)):
            gaps.append(gap)

    time_fields = (
        ("retest_requested_at", ("retest_requested_at", "requested_at")),
        ("retest_started_at", ("retest_started_at", "started_at")),
        ("retest_completed_at", ("retest_completed_at", "completed_at")),
        ("retest_verified_at", ("retest_verified_at", "verified_at")),
    )
    parsed_times: list[datetime] = []
    all_times_valid = True
    for label, keys in time_fields:
        recorded = _retest_value(detail, *keys)
        if not isinstance(recorded, str) or not recorded:
            gaps.append(f"{label}_absent")
            all_times_valid = False
            continue
        if not _valid_rfc3339(recorded):
            gaps.append(f"{label}_invalid_rfc3339")
            all_times_valid = False
            continue
        parsed_times.append(datetime.fromisoformat(recorded.replace("Z", "+00:00")))

    if closed_at is None:
        gaps.append("closure_event_time_absent")
        all_times_valid = False
    elif closed_at.tzinfo is None or closed_at.utcoffset() is None:
        gaps.append("closure_event_time_timezone_absent")
        all_times_valid = False
    else:
        parsed_times.append(closed_at)

    if all_times_valid and any(
        later < earlier for earlier, later in zip(parsed_times, parsed_times[1:])
    ):
        gaps.append("retest_timestamp_order_invalid")
    return gaps


def _closure(
    finding: Finding,
    lifecycle: list[FindingEventOut],
    resolution_runs: dict[uuid.UUID, DetectionRun],
) -> ReportClosureProjection:
    status = str(_value(finding.status))
    terminal_history = [
        event for event in lifecycle if event.event_type in _CLOSURE_HISTORY_TYPES
    ]
    terminal_events = [
        event for event in terminal_history if event.event_type in _TERMINAL_EVENT_TYPES
    ]
    expected_types = {
        "remediated": {"remediated", "resolved"},
        "accepted": {"accepted"},
        "fp": {"false_positive"},
    }.get(status)
    matching_terminal_events = (
        [event for event in terminal_events if event.event_type in expected_types]
        if expected_types is not None
        else terminal_events
    )
    latest = matching_terminal_events[-1] if matching_terminal_events else None
    evidence = _closure_evidence(latest)
    retest = _retest_record(latest)
    detail = latest.detail if latest and isinstance(latest.detail, dict) else {}
    referenced_run_id = finding.resolution_run_id or _uuid(detail.get("run_id"))
    recorded_method = finding.resolution_method or _text(
        detail.get("method") or detail.get("resolution_method")
    )
    coverage = (
        _coverage(resolution_runs.get(referenced_run_id))
        if referenced_run_id is not None
        and (recorded_method == "auto" or (latest and latest.event_type == "resolved"))
        else None
    )
    gaps: list[str] = []

    if status in _TERMINAL_STATUSES:
        if latest is None or latest.synthesized:
            gaps.append("stored_terminal_event_absent")
        if latest is None or not latest.actor:
            gaps.append("closure_actor_absent")
        if not _has_detail(detail, "reason", "rationale"):
            gaps.append("closure_reason_absent")
        if not _has_detail(detail, "reviewed_by", "approved_by", "reviewer"):
            gaps.append("closure_review_metadata_absent")
        if evidence.artifacts:
            gaps.extend(
                f"closure_{gap}" for gap in evidence.gaps if gap != "evidence_absent"
            )
        else:
            gaps.append("closure_evidence_absent")

        if status == "remediated":
            if finding.resolved_at is None:
                gaps.append("resolved_at_absent")
            if not finding.resolution_method:
                gaps.append("resolution_method_absent")
            if recorded_method == "auto":
                if referenced_run_id is None:
                    gaps.append("resolution_run_id_absent")
                if coverage is None:
                    gaps.append("resolution_run_record_unavailable")
                elif coverage.recorded_coverage in (None, {}, []):
                    gaps.append("resolution_run_coverage_absent")
                if not _verified_retest_with_before_after(detail):
                    gaps.append("verified_retest_not_recorded")
            else:
                gaps.extend(
                    _manual_closure_gaps(
                        detail,
                        latest.occurred_at if latest is not None else None,
                    )
                )
        elif status == "accepted":
            if not _has_detail(detail, "risk_owner", "owner"):
                gaps.append("risk_acceptance_owner_absent")
            if not _has_detail(detail, "expires_at", "expiry", "review_at"):
                gaps.append("risk_acceptance_expiry_absent")
            if not _has_detail(detail, "compensating_controls"):
                gaps.append("risk_acceptance_compensating_controls_absent")
        elif status == "fp" and not evidence.artifacts:
            gaps.append("false_positive_contradiction_evidence_absent")

    return ReportClosureProjection(
        current_disposition=status,
        is_terminal=status in _TERMINAL_STATUSES,
        resolved_at=(
            finding.resolved_at
            or (
                latest.occurred_at
                if latest and latest.event_type in {"remediated", "resolved"}
                else None
            )
        ),
        resolution_method=recorded_method,
        resolution_run_id=referenced_run_id,
        resolution_miss_count=finding.resolution_miss_count or 0,
        reopened_count=finding.reopened_count or 0,
        reviewed_by=_text(
            detail.get("reviewed_by")
            or detail.get("approved_by")
            or detail.get("reviewer")
        ),
        latest_terminal_event=latest,
        terminal_and_reopen_history=terminal_history,
        recorded_closure_evidence=evidence,
        retest=retest,
        auto_resolution_coverage=coverage,
        completeness_gaps=_dedupe(gaps),
    )


def _plan(row: RemediationPlan) -> ReportRemediationPlan | None:
    # Defence in depth: the DB query filters reviewed rows, and the serializer
    # refuses an unreviewed row even if a caller supplies one directly.
    if not row.reviewed:
        return None
    recorded = row.plan if isinstance(row.plan, dict) else {}
    steps = [item for item in recorded.get("steps", []) if isinstance(item, dict)]
    return ReportRemediationPlan(
        id=row.id,
        os=row.os,
        source=row.source,
        generated_at=row.generated_at,
        model=row.model,
        summary=_text(recorded.get("summary")),
        effort=_text(recorded.get("effort")),
        remediation_risk=_text(recorded.get("remediation_risk")),
        steps=steps,
        verification=_string_list(recorded.get("verification")),
        long_term_recommendations=_string_list(
            recorded.get("long_term_recommendations")
        ),
        compensating_controls=_text(recorded.get("compensating_controls")),
        raw=recorded,
    )


def _recommendations_from_evidence(evidence: Any) -> list[str]:
    if not isinstance(evidence, dict):
        return []
    values: list[str] = []
    for key in ("recommendations", "recommendation", "long_term_recommendations"):
        values.extend(_string_list(evidence.get(key)))
    return _dedupe(values)


def _remediation(finding: Finding, rows: list[RemediationPlan]) -> ReportRemediation:
    plans = [plan for row in rows if (plan := _plan(row)) is not None]
    remediation_updated_at = getattr(finding, "remediation_updated_at", None)
    remediation_updated_by = getattr(finding, "remediation_updated_by", None)
    recommendations = _recommendations_from_evidence(finding.evidence)
    recommendations.extend(
        recommendation
        for plan in plans
        for recommendation in plan.long_term_recommendations
    )
    gaps: list[str] = []
    if not finding.remediation and not plans:
        gaps.append("remediation_absent")
    if finding.remediation and remediation_updated_at is None:
        gaps.append("remediation_timestamp_absent")
    if not recommendations:
        gaps.append("recommendations_absent")
    return ReportRemediation(
        recorded_text=finding.remediation,
        recorded_text_timestamp=remediation_updated_at,
        recorded_text_updated_by=remediation_updated_by,
        timestamp_gap=(
            "no_dedicated_remediation_timestamp_recorded"
            if finding.remediation and remediation_updated_at is None
            else None
        ),
        reviewed_plans=plans,
        recorded_recommendations=_dedupe(recommendations),
        gaps=gaps,
    )


def _asset(asset: Asset | None) -> ReportAsset | None:
    if asset is None:
        return None
    return ReportAsset(
        id=asset.id,
        ip_address=asset.ip_address,
        hostname=asset.hostname,
        fqdn=asset.fqdn,
        os=asset.os,
        os_version=asset.os_version,
        asset_type=str(_value(asset.asset_type)),
        criticality=str(_value(asset.criticality)),
        owner=asset.owner,
        environment=asset.environment,
        tags=asset.tags if isinstance(asset.tags, dict) else {},
        last_seen=asset.last_seen,
    )


def _cwe_ids(evidence: Any) -> list[str]:
    if not isinstance(evidence, dict):
        return []
    values: list[str] = []
    for key in ("cwe_ids", "cwe_id", "cwe"):
        values.extend(_string_list(evidence.get(key)))
    return _dedupe(values)


def _recorded_evidence_value(evidence: Any, *keys: str) -> Any:
    if not isinstance(evidence, dict):
        return None
    for key in keys:
        if key in evidence:
            return evidence[key]
    return None


def _action_tracking(finding: Finding, asset: Asset | None) -> ReportActionTracking:
    evidence = finding.evidence if isinstance(finding.evidence, dict) else {}
    nested = (
        evidence.get("action_tracking")
        if isinstance(evidence.get("action_tracking"), dict)
        else {}
    )

    def recorded(*keys: str) -> Any:
        for key in keys:
            if key in nested:
                return nested[key]
            if key in evidence:
                return evidence[key]
        return None

    return ReportActionTracking(
        owner=(asset.owner if asset is not None else None)
        or _text(recorded("owner", "action_owner")),
        non_closure_reason=recorded(
            "non_closure_reason", "open_reason", "delay_reason"
        ),
        planned_closure_at=_text(
            recorded("planned_closure_at", "planned_remediation_at", "due_at")
        ),
        action_reference=_text(
            recorded("action_reference", "change_reference", "ticket")
        ),
        recorded_at=_text(
            recorded("recorded_at", "tracking_updated_at", "planned_at")
        ),
    )


def _sla_projection(
    finding: Finding,
    generated_at: datetime,
    windows: dict[str, int],
) -> ReportSlaProjection:
    result = sla.compute(finding, now=generated_at, windows=windows)
    return ReportSlaProjection(
        calculated_at=generated_at,
        state=result.state,
        deadline=result.deadline,
        hours_remaining=result.hours_remaining,
        hours_total=result.hours_total,
    )


def _finding(
    finding: Finding,
    asset: Asset | None,
    event_rows: list[FindingEvent],
    plan_rows: list[RemediationPlan],
    resolution_runs: dict[uuid.UUID, DetectionRun],
    scan_results: dict[uuid.UUID, ScanResult],
    generated_at: datetime,
    sla_windows: dict[str, int],
) -> ReportFinding:
    evidence = normalize_evidence(finding.evidence)
    lifecycle = _timeline(finding, event_rows)
    closure = _closure(finding, lifecycle, resolution_runs)
    remediation = _remediation(finding, plan_rows)
    mappings = extract_compliance_mappings(finding.evidence)
    technical_details = _recorded_evidence_value(
        finding.evidence, "technical_details", "technical_detail"
    )
    impact = _recorded_evidence_value(finding.evidence, "impact")
    business_impact = _recorded_evidence_value(finding.evidence, "business_impact")
    exploitation = _recorded_evidence_value(
        finding.evidence, "exploitation", "exploitability"
    )
    reproduction_steps = _recorded_evidence_value(
        finding.evidence, "reproduction_steps", "validation_steps"
    )
    root_cause = _recorded_evidence_value(finding.evidence, "root_cause")
    preconditions = _recorded_evidence_value(
        finding.evidence, "preconditions", "prerequisites"
    )
    action_tracking = _action_tracking(finding, asset)
    initial_run_id = getattr(finding, "initial_detection_run_id", None)
    initial_run = resolution_runs.get(initial_run_id) if initial_run_id else None
    latest_run = (
        resolution_runs.get(finding.detection_run_id)
        if finding.detection_run_id
        else None
    )
    initial_provenance = _detection_provenance(
        initial_run,
        scan_results.get(initial_run.scan_result_id)
        if initial_run is not None and initial_run.scan_result_id is not None
        else None,
        role="initial_discovery",
    )
    latest_provenance = _detection_provenance(
        latest_run,
        scan_results.get(latest_run.scan_result_id)
        if latest_run is not None and latest_run.scan_result_id is not None
        else None,
        role="latest_observation",
    )

    gaps: list[str] = []
    if not finding.description:
        gaps.append("description_absent")
    if asset is None:
        gaps.append("asset_context_absent")
    if finding.first_seen is None:
        gaps.append("first_seen_absent")
    if technical_details is None:
        gaps.append("technical_details_absent")
    if impact is None and business_impact is None:
        gaps.append("impact_absent")
    if business_impact is None:
        gaps.append("business_impact_absent")
    if exploitation is None:
        gaps.append("exploitation_context_absent")
    if reproduction_steps is None:
        gaps.append("reproduction_steps_absent")
    finding_evidence = finding.evidence if isinstance(finding.evidence, dict) else {}
    if not finding.cve_ids and not _text(
        finding_evidence.get("cve_not_applicable_reason")
    ):
        gaps.append("cve_reference_or_not_applicable_reason_absent")
    cwe_ids = _cwe_ids(finding.evidence)
    if not cwe_ids and not _text(finding_evidence.get("cwe_not_applicable_reason")):
        gaps.append("cwe_reference_or_not_applicable_reason_absent")
    if finding.cvss_score is None and not _text(
        finding_evidence.get("cvss_not_applicable_reason")
    ):
        gaps.append("cvss_score_or_not_applicable_reason_absent")
    if finding.cvss_score is not None and not finding.cvss_vector:
        gaps.append("cvss_vector_absent")
    if finding.cve_ids and finding.epss_score is None:
        gaps.append("epss_score_absent_for_cve_finding")
    status = str(_value(finding.status))
    if status in {"open", "confirmed"}:
        if not action_tracking.owner:
            gaps.append("open_finding_owner_absent")
        if action_tracking.non_closure_reason in (None, "", [], {}):
            gaps.append("open_finding_non_closure_reason_absent")
        if not action_tracking.planned_closure_at:
            gaps.append("planned_closure_at_absent")
        elif not _valid_rfc3339(action_tracking.planned_closure_at):
            gaps.append("planned_closure_at_invalid_rfc3339")
    gaps.extend(
        _detection_provenance_gaps(
            "initial", initial_run_id, initial_provenance
        )
    )
    gaps.extend(
        _detection_provenance_gaps(
            "latest", finding.detection_run_id, latest_provenance
        )
    )
    gaps.extend(evidence.gaps)
    gaps.extend(remediation.gaps)
    gaps.extend(_compliance_gaps(mappings))
    gaps.extend(closure.completeness_gaps)

    return ReportFinding(
        id=finding.id,
        title=finding.title,
        description=finding.description,
        technical_details=technical_details,
        impact=impact,
        business_impact=business_impact,
        exploitation=exploitation,
        reproduction_steps=reproduction_steps,
        root_cause=root_cause,
        preconditions=preconditions,
        severity=str(_value(finding.severity)),
        status=str(_value(finding.status)),
        asset=_asset(asset),
        cve_ids=list(finding.cve_ids or []),
        cwe_ids=cwe_ids,
        mitre_techniques=list(finding.mitre_techniques or []),
        cvss_score=finding.cvss_score,
        cvss_vector=finding.cvss_vector,
        epss_score=finding.epss_score,
        risk_score=finding.risk_score,
        exploitable=bool(finding.exploitable),
        exploit_validated=bool(finding.exploit_validated),
        detection_status=str(_value(finding.detection_status)),
        first_seen=finding.first_seen,
        last_seen=finding.last_seen,
        initial_detection_run_id=initial_run_id,
        detection_run_id=finding.detection_run_id,
        initial_detection_provenance=initial_provenance,
        latest_detection_provenance=latest_provenance,
        detected_db_version=finding.detected_db_version,
        created_at=finding.created_at,
        updated_at=finding.updated_at,
        verification=ReportVerification(
            state=finding.verification_state,
            confidence=finding.verification_confidence,
            rationale=finding.verification_rationale,
            method=finding.verification_method,
            needs_review=bool(finding.needs_review),
        ),
        action_tracking=action_tracking,
        evidence=evidence,
        remediation=remediation,
        compliance_mappings=mappings,
        lifecycle=lifecycle,
        closure=closure,
        current_sla=_sla_projection(finding, generated_at, sla_windows),
        readiness_gaps=_dedupe(gaps),
    )


def _engagement(engagement: Engagement) -> ReportEngagement:
    roe = (
        engagement.rules_of_engagement
        if isinstance(engagement.rules_of_engagement, dict)
        else {}
    )
    nested_metadata = roe.get("report_metadata") or roe.get("reporting") or {}
    if not isinstance(nested_metadata, dict):
        nested_metadata = {}
    metadata = {
        key: value
        for key, value in nested_metadata.items()
        if key in _REPORT_METADATA_KEYS and isinstance(value, str)
    }
    if "version" not in metadata and isinstance(roe.get("report_version"), str):
        metadata["version"] = roe["report_version"]
    if "classification" not in metadata and isinstance(roe.get("classification"), str):
        metadata["classification"] = roe["classification"]

    client = _text(roe.get("client"))
    assessor = _text(roe.get("assessor"))
    description = _text(roe.get("description"))
    regulatory_profiles = extract_regulatory_profiles(roe.get("regulatory_profiles"))
    gaps: list[str] = []
    if not client:
        gaps.append("client_metadata_absent")
    if not assessor:
        gaps.append("assessor_metadata_absent")
    if not metadata.get("version"):
        gaps.append("report_version_absent")
    if not metadata.get("classification"):
        gaps.append("report_classification_absent")
    for key in (
        "document_status",
        "prepared_by",
        "prepared_at",
        "reviewed_by",
        "reviewed_at",
        "approved_by",
        "approved_at",
        "issue_date",
        "reporting_period",
        "methodology",
        "risk_rating_method",
        "tools_used",
        "evidence_retention_policy",
        "report_timezone",
        "limitations",
    ):
        if metadata.get(key) in (None, "", [], {}):
            gaps.append(
                f"{key}_absent" if key.startswith("report_") else f"report_{key}_absent"
            )
    if not regulatory_profiles:
        gaps.append("regulatory_profiles_absent")
    else:
        required_profile_fields = {
            "profile_id": "regulatory_profile_id_absent",
            "name": "regulatory_profile_name_absent",
            "version": "regulatory_profile_version_absent",
            "jurisdiction": "regulatory_profile_jurisdiction_absent",
            "applicability": "regulatory_profile_applicability_absent",
            "rationale": "regulatory_profile_rationale_absent",
            "source_url": "regulatory_profile_source_url_absent",
            "scope": "regulatory_profile_scope_absent",
            "selected_by": "regulatory_profile_selected_by_absent",
            "selected_at": "regulatory_profile_selected_at_absent",
            "reviewed_by": "regulatory_profile_reviewed_by_absent",
            "reviewed_at": "regulatory_profile_reviewed_at_absent",
            "limitations": "regulatory_profile_limitations_absent",
        }
        for field, gap in required_profile_fields.items():
            if any(not getattr(profile, field) for profile in regulatory_profiles):
                gaps.append(gap)
        if any(
            profile.source_url is not None
            and not _valid_http_url(profile.source_url)
            for profile in regulatory_profiles
        ):
            gaps.append("regulatory_profile_source_url_invalid")
        for field in ("selected_at", "reviewed_at"):
            if any(
                (value := getattr(profile, field)) is not None
                and not _valid_rfc3339(value)
                for profile in regulatory_profiles
            ):
                gaps.append(f"regulatory_profile_{field}_invalid_rfc3339")

    for field in ("issue_date", "prepared_at", "reviewed_at", "approved_at"):
        value = metadata.get(field)
        if value is not None and not _valid_rfc3339(value):
            gaps.append(f"report_{field}_invalid_rfc3339")
    report_timezone = metadata.get("report_timezone")
    if report_timezone is not None and not _valid_iana_timezone(report_timezone):
        gaps.append("report_timezone_invalid_iana")

    return ReportEngagement(
        id=engagement.id,
        name=engagement.name,
        status=str(_value(engagement.status)),
        scope_cidrs=list(engagement.scope_cidrs or []),
        excluded_cidrs=list(engagement.excluded_cidrs or []),
        start_time=engagement.start_time,
        end_time=engagement.end_time,
        created_at=engagement.created_at,
        updated_at=engagement.updated_at,
        client=client,
        assessor=assessor,
        description=description,
        tags=_string_list(roe.get("tags")),
        recorded_report_metadata=metadata,
        regulatory_profiles=regulatory_profiles,
        metadata_gaps=gaps,
    )


def _summary(findings: list[ReportFinding]) -> ReportSummary:
    severities = Counter(item.severity for item in findings)
    statuses = Counter(item.status for item in findings)
    for value in ("critical", "high", "medium", "low", "info"):
        severities.setdefault(value, 0)
    for value in ("open", "confirmed", "remediated", "accepted", "fp"):
        statuses.setdefault(value, 0)
    severity_status = {
        severity: {
            status: sum(
                item.severity == severity and item.status == status for item in findings
            )
            for status in statuses
        }
        for severity in severities
    }
    open_by_severity = {
        severity: row.get("open", 0) + row.get("confirmed", 0)
        for severity, row in severity_status.items()
    }
    terminal_by_severity = {
        severity: sum(row.get(status, 0) for status in _TERMINAL_STATUSES)
        for severity, row in severity_status.items()
    }
    return ReportSummary(
        total_findings=len(findings),
        by_severity=dict(severities),
        by_status=dict(statuses),
        by_severity_status=severity_status,
        open_by_severity=open_by_severity,
        terminal_by_severity=terminal_by_severity,
        open_or_confirmed=statuses["open"] + statuses["confirmed"],
        terminal=sum(statuses[value] for value in _TERMINAL_STATUSES),
        auto_resolved=sum(
            item.status == "remediated" and item.closure.resolution_method == "auto"
            for item in findings
        ),
        manual_remediated=sum(
            item.status == "remediated" and item.closure.resolution_method == "manual"
            for item in findings
        ),
        findings_with_reopen_history=sum(
            item.closure.reopened_count > 0 for item in findings
        ),
    )


def _compliance_rollup(
    findings: list[ReportFinding],
    regulatory_profiles: list[ReportRegulatoryProfile],
) -> ReportComplianceRollup:
    by_framework: dict[
        tuple[str | None, str | None], list[tuple[uuid.UUID, ReportComplianceMapping]]
    ] = defaultdict(list)
    unmapped: list[uuid.UUID] = []
    mapping_count = 0
    for finding in findings:
        if not finding.compliance_mappings:
            unmapped.append(finding.id)
            continue
        for mapping in finding.compliance_mappings:
            mapping_count += 1
            by_framework[(mapping.framework, mapping.framework_version)].append(
                (finding.id, mapping)
            )

    frameworks: list[ReportComplianceFrameworkRollup] = []
    for (framework, version), entries in sorted(
        by_framework.items(), key=lambda item: ((item[0][0] or ""), (item[0][1] or ""))
    ):
        by_control: dict[
            tuple[str | None, str | None],
            list[tuple[uuid.UUID, ReportComplianceMapping]],
        ] = defaultdict(list)
        for finding_id, mapping in entries:
            by_control[(mapping.control_id, mapping.control_title)].append(
                (finding_id, mapping)
            )
        controls = [
            ReportComplianceControlRollup(
                control_id=control_id,
                control_title=control_title,
                finding_ids=list(dict.fromkeys(fid for fid, _ in control_entries)),
                recorded_results=_dedupe(
                    mapping.assessment_status or mapping.result or ""
                    for _, mapping in control_entries
                ),
            )
            for (control_id, control_title), control_entries in sorted(
                by_control.items(),
                key=lambda item: ((item[0][0] or ""), (item[0][1] or "")),
            )
        ]
        frameworks.append(
            ReportComplianceFrameworkRollup(
                framework=framework,
                framework_version=version,
                mapping_count=len(entries),
                finding_count=len({finding_id for finding_id, _ in entries}),
                controls=controls,
            )
        )

    return ReportComplianceRollup(
        mapping_count=mapping_count,
        regulatory_profiles=regulatory_profiles,
        frameworks=frameworks,
        unmapped_finding_ids=unmapped,
        gap=(
            "No recorded finding-to-control mappings are available; no controls were inferred."
            if mapping_count == 0
            else None
        ),
    )


def _readiness(
    engagement: ReportEngagement,
    findings: list[ReportFinding],
    compliance: ReportComplianceRollup,
) -> ReportReadiness:
    affected: dict[str, list[uuid.UUID]] = defaultdict(list)
    for finding in findings:
        for gap in finding.readiness_gaps:
            affected[gap].append(finding.id)
    report_gaps = list(engagement.metadata_gaps)
    if not findings:
        report_gaps.append("findings_absent")
    if compliance.mapping_count == 0:
        report_gaps.append("compliance_rollup_absent")
    return ReportReadiness(
        complete=not affected and not report_gaps,
        gap_counts={gap: len(ids) for gap, ids in sorted(affected.items())},
        affected_finding_ids=dict(sorted(affected.items())),
        report_gaps=_dedupe(report_gaps),
    )


def build_report_document(
    *,
    engagement: Engagement,
    finding_rows: list[tuple[Finding, Asset | None]],
    event_rows: list[FindingEvent],
    remediation_plan_rows: list[RemediationPlan],
    resolution_runs: dict[uuid.UUID, DetectionRun],
    scan_results: dict[uuid.UUID, ScanResult] | None = None,
    generated_at: datetime,
    sla_windows: dict[str, int],
) -> ReportDocument:
    """Pure report assembly once authoritative rows have been loaded."""
    if generated_at.tzinfo is None:
        raise ValueError("generated_at must be timezone-aware")
    generated_at = generated_at.astimezone(timezone.utc)
    scan_results = scan_results or {}

    events_by_finding: dict[uuid.UUID, list[FindingEvent]] = defaultdict(list)
    for row in event_rows:
        events_by_finding[row.finding_id].append(row)
    for rows in events_by_finding.values():
        rows.sort(key=lambda row: row.occurred_at)

    plans_by_finding: dict[uuid.UUID, list[RemediationPlan]] = defaultdict(list)
    for row in remediation_plan_rows:
        if row.reviewed:
            plans_by_finding[row.finding_id].append(row)
    for rows in plans_by_finding.values():
        rows.sort(key=lambda row: row.generated_at, reverse=True)

    findings = [
        _finding(
            finding,
            asset,
            events_by_finding.get(finding.id, []),
            plans_by_finding.get(finding.id, []),
            resolution_runs,
            scan_results,
            generated_at,
            sla_windows,
        )
        for finding, asset in finding_rows
    ]
    engagement_out = _engagement(engagement)
    compliance = _compliance_rollup(findings, engagement_out.regulatory_profiles)
    display_timezone = engagement_out.recorded_report_metadata.get(
        "report_timezone", "UTC"
    )
    return ReportDocument(
        document=ReportDocumentControl(
            generated_at=generated_at,
            display_timezone=display_timezone,
        ),
        engagement=engagement_out,
        summary=_summary(findings),
        findings=findings,
        compliance_rollup=compliance,
        readiness=_readiness(engagement_out, findings, compliance),
    )


async def load_report_document(
    db: AsyncSession,
    *,
    tenant_id: uuid.UUID,
    engagement_id: uuid.UUID,
    generated_at: datetime,
) -> ReportDocument | None:
    """Load every report row in bounded batched queries, scoped to one tenant."""
    engagement = (
        await db.execute(
            select(Engagement).where(
                Engagement.id == engagement_id,
                Engagement.tenant_id == tenant_id,
            )
        )
    ).scalar_one_or_none()
    if engagement is None:
        return None

    finding_rows = (
        await db.execute(
            select(Finding, Asset)
            .outerjoin(
                Asset,
                and_(
                    Asset.id == Finding.asset_id,
                    Asset.engagement_id == Finding.engagement_id,
                ),
            )
            .where(Finding.engagement_id == engagement_id)
            .order_by(Finding.created_at, Finding.id)
        )
    ).all()
    finding_ids = [finding.id for finding, _ in finding_rows]

    event_rows: list[FindingEvent] = []
    plan_rows: list[RemediationPlan] = []
    resolution_runs: dict[uuid.UUID, DetectionRun] = {}
    scan_results: dict[uuid.UUID, ScanResult] = {}
    if finding_ids:
        event_rows = (
            (
                await db.execute(
                    select(FindingEvent)
                    .where(FindingEvent.finding_id.in_(finding_ids))
                    .order_by(FindingEvent.finding_id, FindingEvent.occurred_at)
                )
            )
            .scalars()
            .all()
        )
        plan_rows = (
            (
                await db.execute(
                    select(RemediationPlan)
                    .where(
                        RemediationPlan.tenant_id == tenant_id,
                        RemediationPlan.engagement_id == engagement_id,
                        RemediationPlan.finding_id.in_(finding_ids),
                        RemediationPlan.reviewed.is_(True),
                    )
                    .order_by(
                        RemediationPlan.finding_id, RemediationPlan.generated_at.desc()
                    )
                )
            )
            .scalars()
            .all()
        )
        run_ids = {
            finding.resolution_run_id
            for finding, _ in finding_rows
            if finding.resolution_run_id is not None
        }
        run_ids.update(
            run_id
            for finding, _ in finding_rows
            if (run_id := getattr(finding, "initial_detection_run_id", None))
            is not None
        )
        run_ids.update(
            finding.detection_run_id
            for finding, _ in finding_rows
            if finding.detection_run_id is not None
        )
        run_ids.update(
            run_id
            for event in event_rows
            if isinstance(event.detail, dict)
            if (run_id := _uuid(event.detail.get("run_id"))) is not None
        )
        if run_ids:
            rows = (
                (
                    await db.execute(
                        select(DetectionRun).where(
                            DetectionRun.id.in_(run_ids),
                            DetectionRun.engagement_id == engagement_id,
                        )
                    )
                )
                .scalars()
                .all()
            )
            resolution_runs = {row.id: row for row in rows}
            scan_result_ids = {
                row.scan_result_id
                for row in rows
                if row.scan_result_id is not None
            }
            if scan_result_ids:
                result_rows = (
                    (
                        await db.execute(
                            select(ScanResult).where(
                                ScanResult.id.in_(scan_result_ids),
                                ScanResult.engagement_id == engagement_id,
                            )
                        )
                    )
                    .scalars()
                    .all()
                )
                scan_results = {row.id: row for row in result_rows}

    policy = (
        await db.execute(select(SlaPolicy).where(SlaPolicy.tenant_id == tenant_id))
    ).scalar_one_or_none()
    windows = (
        {
            "critical": policy.critical_hours,
            "high": policy.high_hours,
            "medium": policy.medium_hours,
            "low": policy.low_hours,
            "info": policy.info_hours,
        }
        if policy is not None
        else sla.default_windows()
    )
    return build_report_document(
        engagement=engagement,
        finding_rows=list(finding_rows),
        event_rows=list(event_rows),
        remediation_plan_rows=list(plan_rows),
        resolution_runs=resolution_runs,
        scan_results=scan_results,
        generated_at=generated_at,
        sla_windows=windows,
    )

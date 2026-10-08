from __future__ import annotations

import uuid
from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.discovery.finding_translator import create_findings_from_probe_result
from app.discovery.service_vuln import create_service_vuln_findings
from app.routers.ad import _ad_finding
from app.routers.vuln_scans import FindingImport, _import_finding, _nuclei_finding
from app.services.finding_scan_provenance import (
    SCAN_PROVENANCE_KEY,
    attach_detection_run_to_scan_findings,
    preserve_trusted_scan_provenance,
    record_scan_observation,
)
from app.services.job_result_service import process_job_result

RECORDED_AT = datetime(2026, 9, 27, 8, 30, tzinfo=timezone.utc)


class _Rows:
    def __init__(self, rows) -> None:
        self.rows = rows

    def scalars(self):
        return self

    def all(self):
        return self.rows


class _NestedTransaction:
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, traceback) -> bool:
        return False


def test_scanner_cannot_forge_the_manager_owned_provenance_block() -> None:
    real_scan_result_id = uuid.uuid4()
    evidence = record_scan_observation(
        {
            "scan_provenance": {
                "initial": {
                    "scan_result_id": str(uuid.uuid4()),
                    "detection_run_id": str(uuid.uuid4()),
                }
            }
        },
        scan_result_id=real_scan_result_id,
        scan_job_id=uuid.uuid4(),
        scan_type="tls_scan",
        source="probe",
        tool="testssl",
        recorded_at=RECORDED_AT,
        initial=True,
    )

    provenance = evidence[SCAN_PROVENANCE_KEY]
    assert provenance["recorded_by"] == "vedha_manager"
    assert provenance["initial"]["scan_result_id"] == str(real_scan_result_id)
    assert provenance["initial"]["detection_run_id"] is None


def test_evidence_replacement_preserves_only_trusted_manager_provenance() -> None:
    trusted = record_scan_observation(
        {"proof": "old"},
        scan_result_id=uuid.uuid4(),
        scan_job_id=uuid.uuid4(),
        scan_type="tls_scan",
        source="probe",
        tool="testssl",
        recorded_at=RECORDED_AT,
        initial=True,
    )
    forged = {
        "recorded_by": "scanner",
        "schema_version": 1,
        "initial": {"scan_result_id": str(uuid.uuid4())},
    }

    replaced = preserve_trusted_scan_provenance(
        {"proof": "new", SCAN_PROVENANCE_KEY: forged},
        previous_evidence=trusted,
    )
    assert replaced["proof"] == "new"
    assert replaced[SCAN_PROVENANCE_KEY] == trusted[SCAN_PROVENANCE_KEY]
    assert replaced[SCAN_PROVENANCE_KEY] is not trusted[SCAN_PROVENANCE_KEY]

    untrusted = preserve_trusted_scan_provenance(
        {"proof": "new", SCAN_PROVENANCE_KEY: forged},
        previous_evidence={SCAN_PROVENANCE_KEY: forged},
    )
    assert SCAN_PROVENANCE_KEY not in untrusted


@pytest.mark.asyncio
async def test_job_ingest_passes_the_persisted_scan_identity_to_all_probe_paths() -> None:
    agent_id = uuid.uuid4()
    job_id = uuid.uuid4()
    engagement_id = uuid.uuid4()
    attempt_id = uuid.uuid4()
    scan_result_id = uuid.uuid4()
    row = SimpleNamespace(
        id=job_id,
        engagement_id=engagement_id,
        agent_id=str(agent_id),
        status="running",
        current_attempt_id=attempt_id,
        current_fence=4,
        result={"_scope_cidrs": ["10.0.0.0/24"]},
        completed_at=None,
        lease_expires_at=RECORDED_AT,
    )
    attempt = SimpleNamespace(
        status="running",
        result_checksum=None,
        ended_at=None,
        error=None,
    )
    db = MagicMock()
    db.execute = AsyncMock(
        side_effect=[
            MagicMock(scalar_one_or_none=lambda: row),
            MagicMock(scalar_one_or_none=lambda: attempt),
        ]
    )

    def add(value) -> None:
        if value.__class__.__name__ == "ScanResult":
            value.id = scan_result_id

    db.add = MagicMock(side_effect=add)
    db.flush = AsyncMock()
    db.begin_nested = MagicMock(side_effect=_NestedTransaction)
    translate = AsyncMock(return_value=1)
    service_vuln = AsyncMock(return_value=1)
    scan_health = AsyncMock(return_value=0)

    with (
        patch(
            "app.discovery.finding_translator.create_findings_from_probe_result",
            translate,
        ),
        patch(
            "app.discovery.service_vuln.create_service_vuln_findings",
            service_vuln,
        ),
        patch(
            "app.discovery.finding_translator.create_scan_health_finding",
            scan_health,
        ),
        patch(
            "app.detection.prioritization.prioritize_engagement_findings",
            AsyncMock(),
        ),
        patch(
            "app.services.result_chunk_service.apply_chunks_to_result",
            AsyncMock(side_effect=lambda _db, _job_id, result: result),
        ),
        patch(
            "app.services.result_chunk_service.discard_chunks",
            AsyncMock(return_value=0),
        ),
    ):
        result = await process_job_result(
            db,
            agent_id,
            job_id,
            True,
            {
                "scan_type": "tls_scan",
                "engine": "testssl",
                "facts": [{"target": "10.0.0.8", "status": "open"}],
                "findings": [{"target": "10.0.0.8:443", "title": "Weak TLS"}],
            },
            None,
            attempt_id,
            4,
        )

    assert result["ok"] is True
    for producer in (translate, service_vuln, scan_health):
        assert producer.await_args.kwargs["scan_result_id"] == scan_result_id
        assert producer.await_args.kwargs["scan_job_id"] == job_id
        assert producer.await_args.kwargs["recorded_at"] == row.completed_at


@pytest.mark.asyncio
async def test_real_runs_link_independent_initial_and_latest_scan_results() -> None:
    engagement_id = uuid.uuid4()
    first_scan_id = uuid.uuid4()
    latest_scan_id = uuid.uuid4()
    first_run_id = uuid.uuid4()
    latest_run_id = uuid.uuid4()
    evidence = record_scan_observation(
        {"proof": "first"},
        scan_result_id=first_scan_id,
        scan_job_id=uuid.uuid4(),
        scan_type="tls_scan",
        source="probe",
        tool="testssl",
        recorded_at=RECORDED_AT,
        initial=True,
    )
    evidence = record_scan_observation(
        {"proof": "latest"},
        scan_result_id=latest_scan_id,
        scan_job_id=uuid.uuid4(),
        scan_type="tls_scan",
        source="probe",
        tool="testssl",
        recorded_at=RECORDED_AT,
        initial=False,
        previous_evidence=evidence,
    )
    finding = SimpleNamespace(
        evidence=evidence,
        initial_detection_run_id=None,
        detection_run_id=None,
    )
    db = MagicMock()
    db.execute = AsyncMock(return_value=_Rows([finding]))
    db.flush = AsyncMock()

    await attach_detection_run_to_scan_findings(
        db, engagement_id, first_scan_id, first_run_id
    )

    assert finding.initial_detection_run_id == first_run_id
    assert finding.detection_run_id is None

    await attach_detection_run_to_scan_findings(
        db, engagement_id, latest_scan_id, latest_run_id
    )

    provenance = finding.evidence[SCAN_PROVENANCE_KEY]
    assert finding.initial_detection_run_id == first_run_id
    assert finding.detection_run_id == latest_run_id
    assert provenance["initial"]["detection_run_id"] == str(first_run_id)
    assert provenance["latest"]["detection_run_id"] == str(latest_run_id)
    assert db.flush.await_count == 2

    # At-least-once outbox delivery may link the same completed run again. The
    # exact ScanResult match makes the replay a true no-op, including no flush.
    relinked = await attach_detection_run_to_scan_findings(
        db, engagement_id, latest_scan_id, latest_run_id
    )
    assert relinked == 0
    assert db.flush.await_count == 2


@pytest.mark.asyncio
async def test_probe_translator_records_exact_result_and_job_before_run_exists() -> None:
    engagement_id = uuid.uuid4()
    scan_result_id = uuid.uuid4()
    scan_job_id = uuid.uuid4()
    db = MagicMock()
    db.add = MagicMock()
    db.flush = AsyncMock()

    with (
        patch(
            "app.discovery.finding_translator._resolve_asset",
            AsyncMock(return_value=None),
        ),
        patch(
            "app.discovery.finding_translator._find_open_duplicate",
            AsyncMock(return_value=None),
        ),
        patch(
            "app.discovery.finding_translator._escalate_by_exposure",
            AsyncMock(side_effect=lambda _db, _asset, _finding, severity: (severity, None)),
        ),
    ):
        created = await create_findings_from_probe_result(
            db,
            engagement_id,
            {
                "scan_type": "tls_scan",
                "engine": "testssl",
                "findings": [{"title": "Weak TLS", "severity": "medium"}],
            },
            scan_result_id=scan_result_id,
            scan_job_id=scan_job_id,
            recorded_at=RECORDED_AT,
        )

    finding = db.add.call_args.args[0]
    observation = finding.evidence[SCAN_PROVENANCE_KEY]["initial"]
    assert created == 1
    assert observation["scan_result_id"] == str(scan_result_id)
    assert observation["scan_job_id"] == str(scan_job_id)
    assert observation["detection_run_id"] is None
    assert finding.initial_detection_run_id is None
    assert finding.detection_run_id is None
    assert finding.first_seen == RECORDED_AT
    assert finding.last_seen == RECORDED_AT


@pytest.mark.asyncio
async def test_service_vulnerability_finding_uses_probe_scan_context() -> None:
    scan_result_id = uuid.uuid4()
    scan_job_id = uuid.uuid4()
    db = MagicMock()
    db.add = MagicMock()
    db.flush = AsyncMock()

    with (
        patch(
            "app.discovery.service_vuln._resolve_asset",
            AsyncMock(return_value=None),
        ),
        patch(
            "app.discovery.service_vuln._find_open_duplicate",
            AsyncMock(return_value=None),
        ),
    ):
        created = await create_service_vuln_findings(
            db,
            uuid.uuid4(),
            {
                "scan_type": "port_scan",
                "engine": "nmap",
                "facts": [
                    {
                        "status": "open",
                        "target": "10.0.0.8",
                        "port": 22,
                        # SSH weak-crypto is a retained service_vuln rule (the
                        # cleartext rule was retired — gap #2); banner advertises
                        # ssh-dss, so exactly one finding is produced.
                        "data": {"service": "ssh",
                                 "banner": "SSH-2.0-OpenSSH_7.4\nkex: ssh-dss"},
                    }
                ],
            },
            scan_result_id=scan_result_id,
            scan_job_id=scan_job_id,
            recorded_at=RECORDED_AT,
        )

    finding = db.add.call_args.args[0]
    observation = finding.evidence[SCAN_PROVENANCE_KEY]["initial"]
    assert created == 1
    assert observation["scan_result_id"] == str(scan_result_id)
    assert observation["scan_job_id"] == str(scan_job_id)
    assert observation["tool"] == "nmap"


@pytest.mark.parametrize("kind", ["nuclei", "import", "ad"])
def test_job_only_scanners_record_real_job_and_keep_run_gap(kind: str) -> None:
    engagement_id = uuid.uuid4()
    job_id = uuid.uuid4()
    if kind == "nuclei":
        finding = _nuclei_finding(
            engagement_id,
            {"title": "Nuclei issue", "severity": "high", "evidence": {"x": 1}},
            scan_job_id=job_id,
            recorded_at=RECORDED_AT,
        )
    elif kind == "import":
        finding = _import_finding(
            engagement_id,
            FindingImport(title="Imported issue", severity="medium", evidence={"x": 1}),
            scan_job_id=job_id,
            recorded_at=RECORDED_AT,
        )
    else:
        finding = _ad_finding(
            engagement_id,
            {"title": "AD issue", "severity": "critical", "evidence": {"x": 1}},
            scan_job_id=job_id,
            recorded_at=RECORDED_AT,
        )

    provenance = finding.evidence[SCAN_PROVENANCE_KEY]
    assert provenance["initial"]["scan_job_id"] == str(job_id)
    assert provenance["initial"]["scan_result_id"] is None
    assert provenance["initial"]["detection_run_id"] is None
    assert provenance["latest"] == provenance["initial"]
    assert finding.initial_detection_run_id is None
    assert finding.detection_run_id is None
    assert finding.first_seen == RECORDED_AT
    assert finding.last_seen == RECORDED_AT

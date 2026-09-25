"""Filter findings by scan, and list the scans that produced findings.

Task 4 of per-scan-findings:
  - GET /findings?scan=<SCN ref | job id | run id> restricts to findings a single
    scan TOUCHED (new + reaffirmed + resolved), via the detection_run_findings
    membership table — not just the latest-run pointer.
  - GET /findings/scans lists scans with a distinct-finding count, newest first,
    to feed the filter control and the compare picker.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.models.enums import ScanJobStatus
from app.routers import findings as findings_router
from app.schemas.auth import CurrentUser

_TENANT = uuid.uuid4()


def _user():
    return CurrentUser(user_id=uuid.uuid4(), tenant_id=_TENANT, role="manager")


def _capturing_db(scalar_rows):
    """A db whose execute records the compiled SQL and returns scalar_rows."""
    captured: dict = {}

    async def fake_execute(stmt):
        captured["sql"] = str(stmt.compile(compile_kwargs={"literal_binds": True}))
        r = MagicMock()
        r.scalars.return_value.all.return_value = scalar_rows
        return r

    db = MagicMock()
    db.execute = fake_execute
    return db, captured


class TestResolveScanRunIds:
    @pytest.mark.asyncio
    async def test_reference_selector_is_upper_cased(self):
        rid = uuid.uuid4()
        db, captured = _capturing_db([rid])
        out = await findings_router._resolve_scan_run_ids(db, "scn-260301-abc123", _TENANT)
        assert out == {rid}
        assert "SCN-260301-ABC123" in captured["sql"]      # reference folded to upper
        assert "scan_jobs" in captured["sql"]              # resolved via the job

    @pytest.mark.asyncio
    async def test_uuid_selector_matches_run_or_job(self):
        val = uuid.uuid4()
        db, captured = _capturing_db([])
        await findings_router._resolve_scan_run_ids(db, str(val), _TENANT)
        # A UUID is accepted as EITHER a run id or a job id.
        assert "detection_runs.id =" in captured["sql"]
        assert "detection_runs.job_id =" in captured["sql"]


class TestScanFilterOnList:
    @pytest.mark.asyncio
    async def test_unknown_scan_returns_empty_page_without_querying(self):
        with patch.object(findings_router, "_resolve_scan_run_ids",
                          new=AsyncMock(return_value=set())), \
             patch.object(findings_router, "paginate_query") as mock_pag:
            out = await findings_router.list_findings(
                db=MagicMock(), current_user=_user(), severity=None, status_filter=None,
                active_only=False, asset_id=None, asset_ip=None, mitre_technique=None,
                engagement_id=None, agent_id=None, scan="SCN-999999-ZZZZZZ", search=None,
                detection_status=None, exploit_validated=None, verification_state=None,
                needs_review=None, sla_breached=False, sort="risk", page=1, page_size=20)
        assert out.total == 0
        assert out.items == []
        mock_pag.assert_not_called()   # short-circuit before the page query

    @pytest.mark.asyncio
    async def test_known_scan_filters_through_membership_table(self):
        captured: dict = {}

        async def fake_paginate(db, q, page, page_size):
            captured["sql"] = str(q.compile(compile_kwargs={"literal_binds": True}))
            return [], 0

        with patch.object(findings_router, "_resolve_scan_run_ids",
                          new=AsyncMock(return_value={uuid.uuid4()})), \
             patch.object(findings_router, "paginate_query", fake_paginate):
            await findings_router.list_findings(
                db=MagicMock(), current_user=_user(), severity=None, status_filter=None,
                active_only=False, asset_id=None, asset_ip=None, mitre_technique=None,
                engagement_id=None, agent_id=None, scan="SCN-260301-ABC123", search=None,
                detection_status=None, exploit_validated=None, verification_state=None,
                needs_review=None, sla_breached=False, sort="risk", page=1, page_size=20)
        # The page query restricts findings to membership rows for the scan's runs.
        assert "detection_run_findings" in captured["sql"]


class TestScanOutcomes:
    @pytest.mark.asyncio
    async def test_collapses_to_most_significant_outcome(self):
        f_new, f_res, f_reaff = uuid.uuid4(), uuid.uuid4(), uuid.uuid4()
        # f_new appears as BOTH reaffirmed and new across a job's runs → new wins.
        rows = [(f_new, "reaffirmed"), (f_new, "new"),
                (f_res, "resolved"), (f_reaff, "reaffirmed")]
        r = MagicMock(); r.all.return_value = rows
        db = MagicMock(); db.execute = AsyncMock(return_value=r)
        out = await findings_router._scan_outcomes(
            db, {uuid.uuid4()}, [f_new, f_res, f_reaff])
        assert out == {f_new: "new", f_res: "resolved", f_reaff: "reaffirmed"}

    @pytest.mark.asyncio
    async def test_empty_page_asks_nothing(self):
        db = MagicMock(); db.execute = AsyncMock()
        out = await findings_router._scan_outcomes(db, {uuid.uuid4()}, [])
        assert out == {}
        assert db.execute.await_count == 0


class TestScansListEndpoint:
    @pytest.mark.asyncio
    async def test_lists_scans_with_finding_counts(self):
        jid = uuid.uuid4()
        when = datetime(2026, 3, 1, 12, 0, tzinfo=timezone.utc)
        result = MagicMock()
        result.all.return_value = [
            (jid, "SCN-260301-ABC123", "uc_network_sweep", "aggressive",
             when, ScanJobStatus.completed, 5),
        ]
        db = MagicMock()
        db.execute = AsyncMock(return_value=result)

        out = await findings_router.finding_scans(
            db=db, current_user=_user(), engagement_id=None)

        assert len(out) == 1
        opt = out[0]
        assert opt.job_id == jid
        assert opt.reference == "SCN-260301-ABC123"
        assert opt.use_case_id == "uc_network_sweep"
        assert opt.intensity == "aggressive"
        assert opt.scanned_at == when
        assert opt.status == "completed"    # enum → its value
        assert opt.findings == 5

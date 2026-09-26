"""test_remediation_export.py — the XLSX/CSV remediation tracker."""
from __future__ import annotations

import asyncio
import csv
import io
import uuid
import zipfile
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from unittest.mock import MagicMock

from openpyxl import load_workbook

from app.models.enums import FindingSeverity, FindingStatus
from app.remediation import export as X
from app.remediation.bundles import build_bundles
from app.remediation.context import build_context

NOW = datetime(2026, 9, 27, 6, 30, tzinfo=timezone.utc)   # 12:00 IST


def _items():
    out = []
    for i, status in ((1, FindingStatus.open), (2, FindingStatus.remediated)):
        f = SimpleNamespace(id=uuid.uuid4(), title="SMBv1 enabled", description="", remediation="",
                            severity=FindingSeverity.critical, status=status,
                            evidence={"rule_id": "POSTURE-SMB-V1-ENABLED", "port": 445}, cve_ids=[],
                            epss_score=None, exploit_validated=False, resolved_at=NOW if i == 2 else None)
        a = SimpleNamespace(ip_address=f"10.0.0.{i}", hostname=f"fs{i}", fqdn=None, os="Windows",
                            os_version="Windows Server 2019", asset_type=SimpleNamespace(value="server"),
                            criticality=SimpleNamespace(value="high"), environment=None, tags=None)
        due = {"at": NOW, "source": "engagement"} if status == FindingStatus.open else {"at": None, "source": None}
        out.append((f, build_context(f, a, None), due))
    return out


def _sheets():
    items = _items()
    ext = SimpleNamespace(status="approved", member_finding_ids=[items[0][0].id],
                          reason="Waiting for the change freeze to end", requested_due_at=NOW + timedelta(days=30),
                          decided_due_at=NOW + timedelta(days=14), requested_at=NOW)
    return X.build_rows(build_bundles(items, now=NOW), items, [ext])


def test_rows_cover_all_views():
    sheets = _sheets()
    assert set(sheets) == set(X.SHEETS)
    fix_h, fix_rows = sheets["By fix"]
    assert len(fix_rows) == 1 and fix_rows[0][0].startswith("FIX-")
    assert fix_rows[0][8:10] == [1, 1]                 # open, closed
    _, host_rows = sheets["By host checklist"]
    assert {r[7] for r in host_rows} == {"open", "closed"}
    find_h, find_rows = sheets["Findings"]
    open_row = next(r for r in find_rows if r[3] == "open")
    assert open_row[13] == "Waiting for the change freeze to end"
    assert open_row[14] == datetime(2026, 10, 11, 12, 0)   # decided date, IST, naive for Excel


def test_xlsx_structure():
    data = X.to_xlsx(_sheets(), title="Remediation tracker — Bank VA")
    wb = load_workbook(io.BytesIO(data))
    assert wb.sheetnames == list(X.SHEETS)
    ws = wb["By fix"]
    assert ws.freeze_panes == "A2"
    assert ws.auto_filter.ref
    due_col = [c.value for c in ws[1]].index("Due (IST)") + 1
    cell = ws.cell(row=2, column=due_col)
    assert isinstance(cell.value, datetime) and cell.value == datetime(2026, 9, 27, 12, 0)
    assert cell.number_format == "yyyy-mm-dd hh:mm"


def test_csv_zip():
    data = X.to_csv_zip(_sheets())
    with zipfile.ZipFile(io.BytesIO(data)) as zf:
        assert sorted(zf.namelist()) == ["by_fix.csv", "by_host_checklist.csv", "findings.csv"]
        rows = list(csv.reader(io.StringIO(zf.read("findings.csv").decode("utf-8-sig"))))
    assert rows[0][0] == "Finding ID" and len(rows) == 3
    assert "2026-10-11 12:00" in {c for r in rows for c in r}


def test_route_returns_attachment(monkeypatch):
    from app.remediation import service as RS
    from app.routers import remediation
    from app.schemas.auth import CurrentUser

    async def fake_bundles(db, engagement, tenant_id):
        items = _items()
        return {"bundles": build_bundles(items, now=NOW), "items": items, "sla_source": "engagement"}

    monkeypatch.setattr(RS, "engagement_bundles", fake_bundles)
    eng = SimpleNamespace(id=uuid.uuid4(), name="Bank VA / Q3")

    class _DB:
        def __init__(self):
            self.n = 0

        async def execute(self, *a, **k):
            self.n += 1
            r = MagicMock()
            r.scalar_one_or_none = MagicMock(return_value=eng)
            r.scalars = MagicMock(return_value=MagicMock(all=MagicMock(return_value=[])))
            return r

    user = CurrentUser(user_id=uuid.uuid4(), tenant_id=uuid.uuid4(), role="analyst")
    resp = asyncio.run(remediation.export_remediation(eng.id, _DB(), user, format="xlsx"))
    assert resp.media_type.endswith("spreadsheetml.sheet")
    disp = resp.headers["content-disposition"]
    assert 'filename="vedha-remediation-Bank-VA-Q3-' in disp and disp.endswith('.xlsx"')

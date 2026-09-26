"""GET /findings/groups (+ the portal delegate).

The grouped view must mean exactly what the list means for the same filters,
so both routes go through one helper (`_filtered_findings`). These tests pin:
  * parity — every filter the list forwards, the groups route forwards identically;
  * tenant scope and lean columns in the compiled SQL;
  * an unknown scan answers empty without querying findings;
  * rows become priority-ordered groups with asset identity and KEV;
  * the row cap is reported, never silent;
  * the portal delegate pins the client's engagement.
"""
from __future__ import annotations

import asyncio
import uuid
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

from app.models.enums import DetectionStatus, FindingSeverity, FindingStatus
from app.routers import findings as findings_router
from app.routers import portal
from app.schemas.auth import CurrentUser
from app.schemas.finding_groups import FindingGroupPage

_TENANT = uuid.uuid4()
_ASSET = uuid.uuid4()
_ENG = uuid.uuid4()

_ALL_FILTERS = dict(
    severity=FindingSeverity.high, status_filter=FindingStatus.open, active_only=True,
    asset_id=uuid.uuid4(), asset_ip="10.0.0.", mitre_technique="T1021",
    engagement_id=uuid.uuid4(), agent_id=uuid.uuid4(), scan="SCN-260927-ABCDEF",
    search="ssh", detection_status=DetectionStatus.detected, exploit_validated=True,
    verification_state="confirmed", needs_review=False, sla_breached=True,
)


def _user():
    return CurrentUser(user_id=uuid.uuid4(), tenant_id=_TENANT, role="manager")


def _row(title, severity="high", status="open", *, rule_id=None, port=None, cpe=None,
         cves=None, kev=None, enrichment_kev=None, risk=None, cvss=None, asset_id=_ASSET):
    return SimpleNamespace(
        id=uuid.uuid4(), engagement_id=_ENG, title=title, severity=FindingSeverity(severity),
        status=FindingStatus(status), cvss_score=Decimal(str(cvss)) if cvss is not None else None,
        risk_score=Decimal(str(risk)) if risk is not None else None, epss_score=None,
        cve_ids=cves, asset_id=asset_id, exploit_validated=False,
        first_seen=None, last_seen=None, created_at=None,
        rule_id=rule_id, port=port, cpe=cpe, kev=kev, enrichment_kev=enrichment_kev,
    )


class _DB:
    """Captures compiled SQL; answers the findings query then the asset query."""
    def __init__(self, rows, assets=()):
        self.rows, self.assets, self.sql = rows, list(assets), []

    async def execute(self, stmt):
        self.sql.append(str(stmt.compile(compile_kwargs={"literal_binds": True})))
        r = MagicMock()
        r.all.return_value = self.rows if len(self.sql) == 1 else self.assets
        return r


def _call_groups(db, **kw):
    return asyncio.run(findings_router.list_finding_groups(db=db, current_user=_user(), **{
        **dict(severity=None, status_filter=None, active_only=False, asset_id=None,
               asset_ip=None, mitre_technique=None, engagement_id=None, agent_id=None,
               scan=None, search=None, detection_status=None, exploit_validated=None,
               verification_state=None, needs_review=None, sla_breached=False,
               page=1, page_size=20), **kw}))


def test_filter_parity_with_list():
    seen = []

    async def spy(base, db, user, **kwargs):
        seen.append(kwargs)
        return None, set()

    with patch.object(findings_router, "_filtered_findings", spy):
        asyncio.run(findings_router.list_findings(
            db=MagicMock(), current_user=_user(), sort="risk", page=1, page_size=20, **_ALL_FILTERS))
        _call_groups(MagicMock(), **_ALL_FILTERS)
    assert len(seen) == 2
    assert seen[0] == seen[1] == _ALL_FILTERS


def test_sql_is_tenant_scoped_filtered_and_lean():
    db = _DB([])
    _call_groups(db, severity=FindingSeverity.high, search="openssh")
    sql = db.sql[0]
    assert f"engagements.tenant_id = '{_TENANT.hex}'" in sql or str(_TENANT) in sql
    assert "findings.severity = 'high'" in sql
    assert "lower(findings.title) LIKE lower('%openssh%')" in sql
    assert "findings.evidence ->> 'rule_id'" in sql or "->> 'rule_id'" in sql
    # Never the whole evidence blob.
    assert "findings.evidence," not in sql and "findings.evidence \nFROM" not in sql
    assert "LIMIT 25001" in sql


def test_unknown_scan_is_empty_without_findings_query():
    db = _DB([])
    with patch.object(findings_router, "_resolve_scan_run_ids", AsyncMock(return_value=set())):
        res = _call_groups(db, scan="SCN-000000-NOPE00")
    assert res.total == 0 and res.items == [] and res.finding_total == 0
    assert db.sql == []


def test_rows_become_priority_ordered_groups():
    rows = [
        _row("SMB signing not required (port 445)", "medium", rule_id="SMB-SIGN", port="445"),
        _row("SMB signing not required (port 139)", "medium", rule_id="SMB-SIGN", port=139),
        _row("CVE-2023-38408 — openssh", "critical", cves=["CVE-2023-38408"],
             cpe="cpe:2.3:a:openbsd:openssh:7.4:*:*:*:*:*:*:*", cvss=9.8),
        _row("CVE-2018-15473 — openssh", "medium", cves=["CVE-2018-15473"],
             cpe="cpe:2.3:a:openbsd:openssh:7.4:*:*:*:*:*:*:*", cvss=5.3, enrichment_kev="true"),
    ]
    db = _DB(rows, assets=[(_ASSET, "10.0.0.7", "web01")])
    res = _call_groups(db)
    FindingGroupPage.model_validate(res.model_dump())
    assert [g.kind for g in res.items] == ["product", "rule"]
    ssh, smb = res.items
    assert ssh.finding_count == 2 and ssh.cve_count == 2 and ssh.kev is True
    assert ssh.max_risk == 980.0          # CVSS 9.8 × 100 — the list's effective risk
    assert smb.ports == [139, 445]
    assert smb.hosts[0].ip == "10.0.0.7" and smb.hosts[0].hostname == "web01"
    assert res.finding_total == 4 and res.total == 2 and res.truncated is False


def test_kev_false_string_is_not_kev():
    db = _DB([_row("X", kev="false")])
    assert _call_groups(db).items[0].kev is False


def test_row_cap_is_reported():
    rows = [_row(f"Issue {i}") for i in range(4)]
    with patch.object(findings_router, "GROUP_ROW_CAP", 3):
        res = _call_groups(_DB(rows))
    assert res.truncated is True
    assert res.finding_total == 3


def test_group_pagination():
    rows = [_row(f"Issue {i}") for i in range(5)]
    res = _call_groups(_DB(rows), page=2, page_size=2)
    assert res.total == 5 and res.pages == 3 and len(res.items) == 2


def test_portal_delegate_pins_engagement():
    engagement = uuid.uuid4()
    client = CurrentUser(user_id=uuid.uuid4(), tenant_id=_TENANT, role="client",
                         client_engagement_id=engagement)
    captured = {}

    async def fake(**kw):
        captured.update(kw)
        return "ok"

    with patch.object(findings_router, "list_finding_groups", fake):
        out = asyncio.run(portal.portal_workspace_finding_groups(
            user=client, db=MagicMock(), severity=None, status_filter=None, active_only=False,
            asset_id=None, asset_ip=None, agent_id=None, mitre_technique=None, scan=None,
            search=None, detection_status=None, exploit_validated=None,
            verification_state=None, needs_review=None, sla_breached=False,
            page=1, page_size=20))
    assert out == "ok"
    assert captured["engagement_id"] == engagement

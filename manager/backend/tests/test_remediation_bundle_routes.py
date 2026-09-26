"""test_remediation_bundle_routes.py — engagement bundle endpoints (operator + portal)."""
from __future__ import annotations

import asyncio
import uuid
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException

from app.models.enums import FindingSeverity, FindingStatus
from app.routers import portal, remediation
from app.schemas.auth import CurrentUser

T0 = datetime.now(timezone.utc) - timedelta(hours=10)


def _scalar(v):
    r = MagicMock()
    r.scalar_one_or_none = MagicMock(return_value=v)
    return r


def _scalars(vals):
    r = MagicMock()
    r.scalars = MagicMock(return_value=MagicMock(all=MagicMock(return_value=list(vals))))
    return r


class _DB:
    def __init__(self, results):
        self.results = list(results)
        self.executed = 0

    async def execute(self, *a, **k):
        self.executed += 1
        return self.results.pop(0)


def _fixture():
    eng = SimpleNamespace(id=uuid.uuid4(), tenant_id=uuid.uuid4(), rules_of_engagement={})
    assets, findings, services = [], [], []
    for i in range(3):
        a = SimpleNamespace(id=uuid.uuid4(), ip_address=f"10.0.0.{i + 1}", hostname=f"fs{i}", fqdn=None,
                            os="Windows", os_version="Windows Server 2019",
                            asset_type=SimpleNamespace(value="server"),
                            criticality=SimpleNamespace(value="medium"), environment=None, tags=None)
        assets.append(a)
        services.append(SimpleNamespace(asset_id=a.id, port=445, protocol="tcp", service_name="smb",
                                        product="SMB", version=None, cpe=None, banner=None, exposure=None))
        findings.append(SimpleNamespace(
            id=uuid.uuid4(), engagement_id=eng.id, asset_id=a.id, title="SMBv1 enabled",
            description="", remediation="", cve_ids=[], evidence={"rule_id": "POSTURE-SMB-V1-ENABLED",
                                                                  "port": 445},
            severity=FindingSeverity.critical, status=FindingStatus.open, first_seen=T0,
            created_at=T0, due_at=None, epss_score=None, exploit_validated=False, resolved_at=None))
    return eng, findings, assets, services


def _results(eng, findings, assets, services):
    # engagement lookup, findings, assets, services, tenant SLA policy
    return [_scalar(eng), _scalars(findings), _scalars(assets), _scalars(services), _scalar(None)]


def _operator():
    return CurrentUser(user_id=uuid.uuid4(), tenant_id=uuid.uuid4(), role="analyst")


def test_routes_mounted():
    from app.main import app
    paths = set(app.openapi()["paths"])
    assert "/engagements/{engagement_id}/remediation/bundles" in paths
    assert "/engagements/{engagement_id}/remediation/bundles/{fix_key}" in paths
    assert "/portal/remediation/bundles" in paths


class TestOperator:
    def test_by_fix(self):
        eng, f, a, s = _fixture()
        db = _DB(_results(eng, f, a, s))
        out = asyncio.run(remediation.get_engagement_bundles(eng.id, db, _operator(), view="fix"))
        assert out["view"] == "fix"
        [b] = out["bundles"]
        assert len(b["hosts"]) == 3 and b["due_source"] == "default"
        assert out["summary"]["open_findings"] == 3 and out["summary"]["hosts"] == 3
        assert db.executed == 5            # fixed cost, no N+1

    def test_by_host(self):
        eng, f, a, s = _fixture()
        out = asyncio.run(remediation.get_engagement_bundles(
            eng.id, _DB(_results(eng, f, a, s)), _operator(), view="host"))
        assert len(out["hosts"]) == 3 and "bundles" not in out

    def test_single_bundle_and_404(self):
        eng, f, a, s = _fixture()
        out = asyncio.run(remediation.get_engagement_bundles(
            eng.id, _DB(_results(eng, f, a, s)), _operator(), view="fix"))
        key = out["bundles"][0]["fix_key"]
        one = asyncio.run(remediation.get_engagement_bundle(eng.id, key, _DB(_results(eng, f, a, s)),
                                                            _operator()))
        assert one["fix_key"] == key
        with pytest.raises(HTTPException) as e:
            asyncio.run(remediation.get_engagement_bundle(eng.id, "nope", _DB(_results(eng, f, a, s)),
                                                          _operator()))
        assert e.value.status_code == 404

    def test_other_tenant_is_404(self):
        with pytest.raises(HTTPException) as e:
            asyncio.run(remediation.get_engagement_bundles(uuid.uuid4(), _DB([_scalar(None)]),
                                                           _operator(), view="fix"))
        assert e.value.status_code == 404


class TestPortal:
    def test_pinned_to_client_engagement(self):
        eng, f, a, s = _fixture()
        user = CurrentUser(user_id=uuid.uuid4(), tenant_id=eng.tenant_id, role="client",
                           client_engagement_id=eng.id)
        out = asyncio.run(portal.portal_remediation_bundles(user, _DB(_results(eng, f, a, s)), view="fix"))
        assert len(out["bundles"]) == 1

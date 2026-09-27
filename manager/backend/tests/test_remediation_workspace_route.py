from __future__ import annotations

import asyncio
import hashlib
import uuid

import pytest
from fastapi import HTTPException

from app.ai.remediation_workspace import FindingContext, OsFamily
from app.routers import remediation
from app.schemas.auth import CurrentUser
from app.schemas.remediation import (
    RemediationWorkspacePreviewOut,
    RemediationWorkspacePreviewRequest,
)
from app.services.remediation_workspace_context import RemediationContextNotFound


class _Db:
    def __init__(self):
        self.flushed = 0

    async def flush(self):
        self.flushed += 1


def _operator(tenant_id: uuid.UUID) -> CurrentUser:
    return CurrentUser(user_id=uuid.uuid4(), tenant_id=tenant_id, role="manager")


def test_workspace_preview_route_is_mounted():
    from app.main import app

    paths = {getattr(route, "path", None) for route in app.routes}
    assert "/findings/remediation-workspaces/preview" in paths


def test_preview_returns_hashed_review_only_artifact_and_audits_metadata(monkeypatch):
    tenant_id = uuid.uuid4()
    engagement_id = uuid.uuid4()
    finding_id = uuid.uuid4()
    context = FindingContext(
        tenant_id=tenant_id,
        engagement_id=engagement_id,
        finding_id=finding_id,
        asset_id=uuid.uuid4(),
        os_family=OsFamily.windows,
        title="SMB signing not required",
        remediation_key="windows.smb_signing.require",
        source_version="source-v1",
    )

    async def load(*_args, **_kwargs):
        return [context]

    audits: list[dict] = []
    monkeypatch.setattr(remediation, "load_workspace_contexts", load)
    monkeypatch.setattr(remediation, "record_audit", lambda _db, **kwargs: audits.append(kwargs))
    db = _Db()

    raw = asyncio.run(remediation.preview_remediation_workspace(
        RemediationWorkspacePreviewRequest(finding_ids=[finding_id]),
        db,
        _operator(tenant_id),
    ))
    response = RemediationWorkspacePreviewOut.model_validate(raw)

    assert response.review_only is True
    assert response.finding_count == 1
    assert response.operation_count == 1
    assert len(response.artifacts) == 1
    artifact = response.artifacts[0]
    assert artifact.format == "powershell"
    assert hashlib.sha256(artifact.content.encode()).hexdigest() == artifact.content_sha256
    assert response.context_sha256 in artifact.content
    assert "-AckContext" in artifact.content
    assert response.advisory is None
    assert db.flushed == 1
    assert audits[0]["action"] == "remediation.workspace_previewed"
    assert "content" not in audits[0]["detail"]
    assert audits[0]["detail"]["artifact_sha256s"] == [artifact.content_sha256]


def test_preview_maps_hidden_or_missing_selection_to_one_404(monkeypatch):
    async def missing(*_args, **_kwargs):
        raise RemediationContextNotFound("One or more findings were not found")

    monkeypatch.setattr(remediation, "load_workspace_contexts", missing)
    tenant_id = uuid.uuid4()
    with pytest.raises(HTTPException) as caught:
        asyncio.run(remediation.preview_remediation_workspace(
            RemediationWorkspacePreviewRequest(finding_ids=[uuid.uuid4()]),
            _Db(),
            _operator(tenant_id),
        ))
    assert caught.value.status_code == 404

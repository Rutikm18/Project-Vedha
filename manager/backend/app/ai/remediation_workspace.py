"""Deterministic, non-executing remediation artifact preparation.

This module is intentionally separate from ``services.remediation_kb``.  The KB
contains human-readable guidance (including strings that merely *look* like
commands); none of those strings are accepted by this module.  Executable bytes
come only from the small, versioned operation catalog below.

The public interface is one deep operation: ``RemediationWorkspace.prepare``.
It validates already-authorized finding contexts, groups them by asset/platform,
maps them to reviewed operation templates, renders guarded artifacts, and hashes
both the input context and output bytes.  It never writes to a database and never
executes a command.

An optional advisory port runs only after artifacts have been rendered and
hashed.  Its response is attached as explanatory metadata, so a model can never
change an operation, artifact byte, or digest.
"""

from __future__ import annotations

import hashlib
import json
import re
import shlex
import unicodedata
import uuid
from collections.abc import Mapping as MappingABC
from dataclasses import dataclass, field, replace
from enum import Enum
from types import MappingProxyType
from typing import Mapping, Protocol, Sequence, TypeAlias


CATALOG_VERSION = "1.0.0"
MAX_FINDINGS = 20

_ARTIFACT_NAMESPACE = uuid.UUID("c728d31c-7aa2-4aac-bf95-b0be9f0d4516")
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_KEY_RE = re.compile(r"^[a-z][a-z0-9_.-]{0,63}$")
_PROGRAM_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_.-]{0,63}$")
_PACKAGE_RE = re.compile(r"^[a-z0-9][a-z0-9+.-]{0,127}$")
_DEBIAN_VERSION_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9.+:~_-]{0,127}$")
_POWERSHELL_SWITCH_RE = re.compile(r"^-[A-Za-z][A-Za-z0-9]*$")
_CONTROL_RE = re.compile(r"[\x00-\x1f\x7f]+")

Scalar: TypeAlias = str | int | bool


class OsFamily(str, Enum):
    linux = "linux"
    windows = "windows"
    macos = "macos"
    generic = "generic"


class OperationKind(str, Enum):
    command = "command"
    manual = "manual"


class ArtifactFormat(str, Enum):
    bash = "bash"
    powershell = "powershell"
    markdown = "markdown"


class RiskLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class RemediationWorkspaceError(ValueError):
    """Base error for an invalid workspace request."""


class InvalidWorkspaceInput(RemediationWorkspaceError):
    """The supplied finding contexts violate a workspace invariant."""


class _TemplateInputError(ValueError):
    """A catalog template cannot safely use the supplied parameters."""


@dataclass(frozen=True)
class FindingContext:
    """Trusted envelope plus bounded, untrusted finding data.

    ``remediation_key`` is a trusted, normalized catalog selector produced by the
    future context adapter.  It is never inferred here from finding prose.
    ``source_version`` must change whenever the source finding/context changes;
    callers can use an updated-at timestamp or their own canonical digest.
    """

    tenant_id: uuid.UUID
    engagement_id: uuid.UUID
    finding_id: uuid.UUID
    asset_id: uuid.UUID | None
    os_family: OsFamily
    title: str
    remediation_key: str
    source_version: str
    os_version: str | None = None
    parameters: Mapping[str, Scalar] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("tenant_id", "engagement_id", "finding_id"):
            if not isinstance(getattr(self, name), uuid.UUID):
                raise InvalidWorkspaceInput(f"{name} must be a UUID")
        if self.asset_id is not None and not isinstance(self.asset_id, uuid.UUID):
            raise InvalidWorkspaceInput("asset_id must be a UUID or None")
        if not isinstance(self.os_family, OsFamily):
            raise InvalidWorkspaceInput("os_family must be an OsFamily")
        _bounded_text(self.title, "title", maximum=500, allow_empty=False)
        _bounded_text(self.source_version, "source_version", maximum=160, allow_empty=False)
        if self.os_version is not None:
            _bounded_text(self.os_version, "os_version", maximum=160, allow_empty=False)
        if not isinstance(self.remediation_key, str):
            raise InvalidWorkspaceInput("remediation_key must be a string")
        if not _KEY_RE.fullmatch(self.remediation_key):
            raise InvalidWorkspaceInput("remediation_key has unsupported characters")
        if not isinstance(self.parameters, MappingABC):
            raise InvalidWorkspaceInput("parameters must be a mapping")
        if len(self.parameters) > 16:
            raise InvalidWorkspaceInput("parameters must contain at most 16 entries")

        copied: dict[str, Scalar] = {}
        for key, value in self.parameters.items():
            if not isinstance(key, str) or not _KEY_RE.fullmatch(key):
                raise InvalidWorkspaceInput("parameter key has unsupported characters")
            if isinstance(value, bool):
                copied[key] = value
            elif isinstance(value, int):
                if not -(2**63) <= value < 2**63:
                    raise InvalidWorkspaceInput(f"parameter {key} integer is out of range")
                copied[key] = value
            elif isinstance(value, str):
                _bounded_text(value, f"parameter {key}", maximum=256, allow_empty=False)
                copied[key] = value
            else:
                raise InvalidWorkspaceInput(
                    f"parameter {key} must be a string, integer, or boolean"
                )
        object.__setattr__(self, "parameters", MappingProxyType(dict(sorted(copied.items()))))


@dataclass(frozen=True)
class CommandSpec:
    """A command represented as argv, never as a shell fragment."""

    program: str
    args: tuple[str | int, ...] = ()

    def __post_init__(self) -> None:
        if not _PROGRAM_RE.fullmatch(self.program):
            raise ValueError("command program has unsupported characters")
        if not isinstance(self.args, tuple):
            raise ValueError("command args must be an immutable tuple")
        if len(self.args) > 32:
            raise ValueError("command has too many arguments")
        for argument in self.args:
            if isinstance(argument, bool) or not isinstance(argument, (str, int)):
                raise ValueError("command arguments must be strings or integers")
            if isinstance(argument, str):
                _bounded_text(argument, "command argument", maximum=512, allow_empty=False)


@dataclass(frozen=True)
class Operation:
    operation_id: str
    template_id: str
    template_version: str
    kind: OperationKind
    asset_id: uuid.UUID | None
    os_family: OsFamily
    finding_ids: tuple[uuid.UUID, ...]
    title: str
    risk: RiskLevel
    requires_admin: bool
    check: tuple[CommandSpec, ...] = ()
    apply: tuple[CommandSpec, ...] = ()
    verify: tuple[CommandSpec, ...] = ()
    rollback_guidance: tuple[str, ...] = ()
    manual_guidance: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not re.fullmatch(r"[0-9a-f]{24}", self.operation_id):
            raise ValueError("operation_id must be a 24-character lowercase digest")
        if not _KEY_RE.fullmatch(self.template_id):
            raise ValueError("template_id has unsupported characters")
        if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", self.template_version):
            raise ValueError("template_version must be semantic version triplet")
        if self.asset_id is not None and not isinstance(self.asset_id, uuid.UUID):
            raise ValueError("operation asset_id must be a UUID or None")
        if not isinstance(self.os_family, OsFamily):
            raise ValueError("operation os_family must be an OsFamily")
        if not isinstance(self.finding_ids, tuple) or any(
            not isinstance(finding_id, uuid.UUID) for finding_id in self.finding_ids
        ):
            raise ValueError("operation finding_ids must be an immutable UUID tuple")
        if not self.finding_ids:
            raise ValueError("operation must reference at least one finding")
        if len(set(self.finding_ids)) != len(self.finding_ids):
            raise ValueError("operation finding_ids must be unique")
        _bounded_text(self.title, "operation title", maximum=240, allow_empty=False)
        for collection_name in ("check", "apply", "verify"):
            collection = getattr(self, collection_name)
            if not isinstance(collection, tuple) or any(
                not isinstance(command, CommandSpec) for command in collection
            ):
                raise ValueError(f"operation {collection_name} must be a CommandSpec tuple")
        if self.kind is OperationKind.command and not self.apply:
            raise ValueError("command operation must have an apply command")
        if self.kind is OperationKind.manual and (self.check or self.apply or self.verify):
            raise ValueError("manual operation cannot contain executable commands")


@dataclass(frozen=True)
class BlockedFinding:
    finding_id: uuid.UUID
    asset_id: uuid.UUID | None
    code: str
    detail: str


@dataclass(frozen=True)
class RemediationArtifact:
    artifact_id: uuid.UUID
    asset_id: uuid.UUID | None
    os_family: OsFamily
    format: ArtifactFormat
    filename: str
    finding_ids: tuple[uuid.UUID, ...]
    context_sha256: str
    content_sha256: str
    content: str

    def __post_init__(self) -> None:
        if not _SHA256_RE.fullmatch(self.context_sha256):
            raise ValueError("context_sha256 must be a lowercase SHA-256 digest")
        if not _SHA256_RE.fullmatch(self.content_sha256):
            raise ValueError("content_sha256 must be a lowercase SHA-256 digest")
        actual = hashlib.sha256(self.content.encode("utf-8")).hexdigest()
        if actual != self.content_sha256:
            raise ValueError("artifact content digest does not match content")
        if not self.finding_ids:
            raise ValueError("artifact must reference at least one finding")


@dataclass(frozen=True)
class AdvisoryRequest:
    tenant_id: uuid.UUID
    engagement_id: uuid.UUID
    context_sha256: str
    finding_ids: tuple[uuid.UUID, ...]
    template_ids: tuple[str, ...]
    artifact_sha256s: tuple[str, ...]


@dataclass(frozen=True)
class Advisory:
    summary: str
    notes: tuple[str, ...] = ()


class AdvisoryPort(Protocol):
    async def advise(self, request: AdvisoryRequest) -> Advisory:
        """Return explanatory text only; there is no executable output field."""


class _ArtifactRenderer(Protocol):
    def __call__(
        self,
        *,
        artifact_id: uuid.UUID,
        asset_id: uuid.UUID | None,
        os_family: OsFamily,
        context_sha256: str,
        operations: Sequence[Operation],
    ) -> str: ...


@dataclass(frozen=True)
class WorkspaceResult:
    tenant_id: uuid.UUID
    engagement_id: uuid.UUID
    catalog_version: str
    context_sha256: str
    operations: tuple[Operation, ...]
    artifacts: tuple[RemediationArtifact, ...]
    blocked: tuple[BlockedFinding, ...]
    advisory: Advisory | None = None
    warnings: tuple[str, ...] = ()


@dataclass(frozen=True)
class _Template:
    template_id: str
    version: str
    os_family: OsFamily


_TEMPLATES: Mapping[str, _Template] = MappingProxyType({
    "linux.apt.package_exact": _Template(
        template_id="linux.apt.package_exact",
        version="1.0.0",
        os_family=OsFamily.linux,
    ),
    "windows.smb_signing.require": _Template(
        template_id="windows.smb_signing.require",
        version="1.0.0",
        os_family=OsFamily.windows,
    ),
})


class RemediationWorkspace:
    """Prepare deterministic remediation artifacts from finding contexts.

    The caller is responsible for loading/authorizing the contexts.  This module
    still enforces that the complete request belongs to exactly one tenant and one
    engagement, and rejects duplicate or oversized selections.
    """

    def __init__(self, advisory: AdvisoryPort | None = None):
        self._advisory = advisory

    async def prepare(self, findings: Sequence[FindingContext]) -> WorkspaceResult:
        ordered = _validate_workspace(findings)
        tenant_id = ordered[0].tenant_id
        engagement_id = ordered[0].engagement_id
        context_sha256 = _context_digest(ordered)

        operations: list[Operation] = []
        blocked: list[BlockedFinding] = []
        grouped_contexts: dict[tuple[str, str], list[FindingContext]] = {}
        for finding in ordered:
            key = (_asset_key(finding.asset_id), finding.os_family.value)
            grouped_contexts.setdefault(key, []).append(finding)

        group_operations: dict[tuple[str, str], list[Operation]] = {}
        for group_key in sorted(grouped_contexts):
            built: dict[str, Operation] = {}
            for finding in grouped_contexts[group_key]:
                operation, problem = _operation_for_finding(finding)
                if problem is not None:
                    blocked.append(problem)
                current = built.get(operation.operation_id)
                if current is None:
                    built[operation.operation_id] = operation
                else:
                    merged_ids = tuple(sorted(
                        {*current.finding_ids, *operation.finding_ids}, key=str
                    ))
                    built[operation.operation_id] = replace(current, finding_ids=merged_ids)
            group = [built[key] for key in sorted(built)]
            group_operations[group_key] = group
            operations.extend(group)

        artifacts: list[RemediationArtifact] = []
        for group_key in sorted(group_operations):
            group = group_operations[group_key]
            command_ops = [op for op in group if op.kind is OperationKind.command]
            manual_ops = [op for op in group if op.kind is OperationKind.manual]
            os_family = group[0].os_family
            asset_id = group[0].asset_id

            if command_ops and os_family is OsFamily.linux:
                artifacts.append(_artifact(
                    asset_id, os_family, ArtifactFormat.bash, command_ops,
                    context_sha256, _render_bash,
                ))
            elif command_ops and os_family is OsFamily.windows:
                artifacts.append(_artifact(
                    asset_id, os_family, ArtifactFormat.powershell, command_ops,
                    context_sha256, _render_powershell,
                ))
            else:
                manual_ops = [*command_ops, *manual_ops]

            if manual_ops:
                artifacts.append(_artifact(
                    asset_id, os_family, ArtifactFormat.markdown, manual_ops,
                    context_sha256, _render_markdown,
                ))

        artifacts.sort(key=lambda item: (
            _asset_key(item.asset_id), item.os_family.value, item.format.value,
        ))
        operations.sort(key=lambda item: (
            _asset_key(item.asset_id), item.os_family.value, item.operation_id,
        ))
        blocked.sort(key=lambda item: str(item.finding_id))

        advisory, advisory_warnings = await self._collect_advisory(
            tenant_id=tenant_id,
            engagement_id=engagement_id,
            context_sha256=context_sha256,
            findings=ordered,
            operations=operations,
            artifacts=artifacts,
        )
        return WorkspaceResult(
            tenant_id=tenant_id,
            engagement_id=engagement_id,
            catalog_version=CATALOG_VERSION,
            context_sha256=context_sha256,
            operations=tuple(operations),
            artifacts=tuple(artifacts),
            blocked=tuple(blocked),
            advisory=advisory,
            warnings=advisory_warnings,
        )

    async def _collect_advisory(
        self,
        *,
        tenant_id: uuid.UUID,
        engagement_id: uuid.UUID,
        context_sha256: str,
        findings: Sequence[FindingContext],
        operations: Sequence[Operation],
        artifacts: Sequence[RemediationArtifact],
    ) -> tuple[Advisory | None, tuple[str, ...]]:
        if self._advisory is None:
            return None, ()
        request = AdvisoryRequest(
            tenant_id=tenant_id,
            engagement_id=engagement_id,
            context_sha256=context_sha256,
            finding_ids=tuple(item.finding_id for item in findings),
            template_ids=tuple(sorted({item.template_id for item in operations})),
            artifact_sha256s=tuple(item.content_sha256 for item in artifacts),
        )
        try:
            response = await self._advisory.advise(request)
            if not isinstance(response, Advisory):
                return None, ("advisory_invalid_response",)
            return _sanitize_advisory(response), ()
        except Exception:  # advisory failure must not affect deterministic artifacts
            return None, ("advisory_unavailable",)


def _validate_workspace(findings: Sequence[FindingContext]) -> list[FindingContext]:
    if not findings:
        raise InvalidWorkspaceInput("at least one finding is required")
    if len(findings) > MAX_FINDINGS:
        raise InvalidWorkspaceInput(f"at most {MAX_FINDINGS} findings are allowed")
    if any(not isinstance(item, FindingContext) for item in findings):
        raise InvalidWorkspaceInput("all items must be FindingContext instances")

    tenant_ids = {item.tenant_id for item in findings}
    engagement_ids = {item.engagement_id for item in findings}
    if len(tenant_ids) != 1:
        raise InvalidWorkspaceInput("all findings must belong to one tenant")
    if len(engagement_ids) != 1:
        raise InvalidWorkspaceInput("all findings must belong to one engagement")
    finding_ids = [item.finding_id for item in findings]
    if len(finding_ids) != len(set(finding_ids)):
        raise InvalidWorkspaceInput("finding_ids must be unique")
    return sorted(findings, key=lambda item: str(item.finding_id))


def _context_digest(findings: Sequence[FindingContext]) -> str:
    payload = {
        "catalog_version": CATALOG_VERSION,
        "findings": [
            {
                "tenant_id": str(item.tenant_id),
                "engagement_id": str(item.engagement_id),
                "finding_id": str(item.finding_id),
                "asset_id": str(item.asset_id) if item.asset_id else None,
                "os_family": item.os_family.value,
                "os_version": item.os_version,
                "title": item.title,
                "remediation_key": item.remediation_key,
                "source_version": item.source_version,
                "parameters": dict(item.parameters),
            }
            for item in findings
        ],
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _operation_for_finding(
    finding: FindingContext,
) -> tuple[Operation, BlockedFinding | None]:
    template = _TEMPLATES.get(finding.remediation_key)
    if template is None:
        detail = "No approved executable template exists for this remediation key."
        return _manual_operation(finding, "no_approved_template", detail), BlockedFinding(
            finding_id=finding.finding_id,
            asset_id=finding.asset_id,
            code="no_approved_template",
            detail=detail,
        )
    if finding.asset_id is None:
        detail = "An asset identity is required before executable remediation can be prepared."
        return _manual_operation(finding, "asset_context_missing", detail), BlockedFinding(
            finding_id=finding.finding_id,
            asset_id=None,
            code="asset_context_missing",
            detail=detail,
        )
    if finding.os_family is not template.os_family:
        detail = "The approved template does not match the asset operating-system family."
        return _manual_operation(finding, "template_platform_mismatch", detail), BlockedFinding(
            finding_id=finding.finding_id,
            asset_id=finding.asset_id,
            code="template_platform_mismatch",
            detail=detail,
        )
    try:
        if template.template_id == "linux.apt.package_exact":
            return _linux_apt_operation(finding, template), None
        if template.template_id == "windows.smb_signing.require":
            return _windows_smb_signing_operation(finding, template), None
    except _TemplateInputError as exc:
        detail = _clean_display(str(exc), maximum=240)
        return _manual_operation(finding, "invalid_template_parameters", detail), BlockedFinding(
            finding_id=finding.finding_id,
            asset_id=finding.asset_id,
            code="invalid_template_parameters",
            detail=detail,
        )
    raise AssertionError(f"unhandled remediation template: {template.template_id}")


def _linux_apt_operation(finding: FindingContext, template: _Template) -> Operation:
    _require_parameter_keys(finding.parameters, {"package", "version"})
    package = str(finding.parameters["package"])
    version = str(finding.parameters["version"])
    if not _PACKAGE_RE.fullmatch(package):
        raise _TemplateInputError("package name is not a safe Debian package identifier")
    if not _DEBIAN_VERSION_RE.fullmatch(version):
        raise _TemplateInputError("package version is not a safe Debian version identifier")

    installed = CommandSpec("dpkg-query", ("-W", "-f=${Version}\\n", package))
    package_spec = f"{package}={version}"
    apply = CommandSpec(
        "apt-get", ("install", "--yes", "--only-upgrade", "--", package_spec)
    )
    operation_id = _operation_digest(
        finding.asset_id, finding.os_family, template.template_id,
        {"package": package, "version": version},
    )
    return Operation(
        operation_id=operation_id,
        template_id=template.template_id,
        template_version=template.version,
        kind=OperationKind.command,
        asset_id=finding.asset_id,
        os_family=finding.os_family,
        finding_ids=(finding.finding_id,),
        title=f"Install exact approved version of {package}",
        risk=RiskLevel.medium,
        requires_admin=True,
        check=(installed,),
        apply=(apply,),
        verify=(installed,),
        rollback_guidance=(
            "Use the package version recorded by the pre-change check and the approved "
            "repository to perform a separate, reviewed rollback.",
        ),
    )


def _windows_smb_signing_operation(
    finding: FindingContext, template: _Template,
) -> Operation:
    _require_parameter_keys(finding.parameters, set())
    path = r"HKLM:\SYSTEM\CurrentControlSet\Services\LanManServer\Parameters"
    check = CommandSpec(
        "Get-ItemPropertyValue", ("-LiteralPath", path, "-Name", "RequireSecuritySignature")
    )
    apply = CommandSpec(
        "Set-ItemProperty",
        (
            "-LiteralPath", path,
            "-Name", "RequireSecuritySignature",
            "-Type", "DWord",
            "-Value", 1,
        ),
    )
    operation_id = _operation_digest(
        finding.asset_id, finding.os_family, template.template_id, {},
    )
    return Operation(
        operation_id=operation_id,
        template_id=template.template_id,
        template_version=template.version,
        kind=OperationKind.command,
        asset_id=finding.asset_id,
        os_family=finding.os_family,
        finding_ids=(finding.finding_id,),
        title="Require SMB server signing",
        risk=RiskLevel.medium,
        requires_admin=True,
        check=(check,),
        apply=(apply,),
        verify=(check,),
        rollback_guidance=(
            "Restore the pre-change RequireSecuritySignature value only through a "
            "separate, reviewed change if compatibility testing requires rollback.",
        ),
    )


def _manual_operation(finding: FindingContext, reason: str, detail: str) -> Operation:
    operation_id = _operation_digest(
        finding.asset_id,
        finding.os_family,
        "manual.review",
        {"finding_id": str(finding.finding_id), "reason": reason},
    )
    return Operation(
        operation_id=operation_id,
        template_id="manual.review",
        template_version=CATALOG_VERSION,
        kind=OperationKind.manual,
        asset_id=finding.asset_id,
        os_family=finding.os_family,
        finding_ids=(finding.finding_id,),
        title=f"Manual review: {_clean_display(finding.title, maximum=120)}",
        risk=RiskLevel.medium,
        requires_admin=False,
        manual_guidance=(
            _clean_display(detail, maximum=240),
            "Review the recorded finding guidance and authoritative vendor documentation; "
            "validate the exact change and rollback plan before execution.",
        ),
    )


def _require_parameter_keys(parameters: Mapping[str, Scalar], expected: set[str]) -> None:
    actual = set(parameters)
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    if missing:
        raise _TemplateInputError(f"missing required parameters: {', '.join(missing)}")
    if extra:
        raise _TemplateInputError(f"unsupported parameters: {', '.join(extra)}")


def _operation_digest(
    asset_id: uuid.UUID | None,
    os_family: OsFamily,
    template_id: str,
    parameters: Mapping[str, Scalar],
) -> str:
    material = json.dumps(
        {
            "asset_id": str(asset_id) if asset_id else None,
            "os_family": os_family.value,
            "template_id": template_id,
            "parameters": dict(parameters),
        },
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(material.encode("utf-8")).hexdigest()[:24]


def _artifact(
    asset_id: uuid.UUID | None,
    os_family: OsFamily,
    artifact_format: ArtifactFormat,
    operations: Sequence[Operation],
    context_sha256: str,
    renderer: _ArtifactRenderer,
) -> RemediationArtifact:
    finding_ids = tuple(sorted(
        {finding_id for operation in operations for finding_id in operation.finding_ids},
        key=str,
    ))
    identity = ":".join((
        context_sha256,
        _asset_key(asset_id),
        os_family.value,
        artifact_format.value,
        ",".join(operation.operation_id for operation in operations),
    ))
    artifact_id = uuid.uuid5(_ARTIFACT_NAMESPACE, identity)
    content = renderer(
        artifact_id=artifact_id,
        asset_id=asset_id,
        os_family=os_family,
        context_sha256=context_sha256,
        operations=operations,
    )
    content_sha256 = hashlib.sha256(content.encode("utf-8")).hexdigest()
    extension = {
        ArtifactFormat.bash: "sh",
        ArtifactFormat.powershell: "ps1",
        ArtifactFormat.markdown: "md",
    }[artifact_format]
    asset_fragment = asset_id.hex[:12] if asset_id else "unassigned"
    filename = f"vedha-remediation-{asset_fragment}-{content_sha256[:12]}.{extension}"
    return RemediationArtifact(
        artifact_id=artifact_id,
        asset_id=asset_id,
        os_family=os_family,
        format=artifact_format,
        filename=filename,
        finding_ids=finding_ids,
        context_sha256=context_sha256,
        content_sha256=content_sha256,
        content=content,
    )


def _render_bash(
    *,
    artifact_id: uuid.UUID,
    asset_id: uuid.UUID | None,
    os_family: OsFamily,
    context_sha256: str,
    operations: Sequence[Operation],
) -> str:
    del os_family
    finding_ids = sorted(
        {item for operation in operations for item in operation.finding_ids}, key=str
    )
    lines = [
        "#!/usr/bin/env bash",
        "# Generated by Vedha RemediationWorkspace from reviewed operation templates.",
        "# Review this artifact before use. It performs no change unless --apply and",
        "# the exact --ack-context value are both supplied.",
        f"# Asset: {_asset_key(asset_id)}",
        f"# Findings: {', '.join(str(item) for item in finding_ids)}",
        f"# Context SHA-256: {context_sha256}",
        "set -Eeuo pipefail",
        "IFS=$'\\n\\t'",
        "",
        f"readonly ARTIFACT_ID={shlex.quote(str(artifact_id))}",
        f"readonly CONTEXT_SHA256={shlex.quote(context_sha256)}",
        'MODE="check"',
        'ACK=""',
        "",
        "usage() {",
        "  printf 'Usage: %s [--check|--dry-run|--apply --ack-context %s]\\n' \"$0\" \"$CONTEXT_SHA256\"",
        "}",
        "",
        'MODE_EXPLICIT="false"',
        "select_mode() {",
        '  [[ "$MODE_EXPLICIT" == "false" ]] || {',
        "    printf 'Choose exactly one mode.\\n' >&2; exit 64",
        "  }",
        '  MODE="$1"; MODE_EXPLICIT="true"',
        "}",
        "",
        "while (($#)); do",
        '  case "$1" in',
        '    --check) select_mode "check"; shift ;;',
        '    --dry-run) select_mode "dry-run"; shift ;;',
        '    --apply) select_mode "apply"; shift ;;',
        "    --ack-context)",
        "      (($# >= 2)) || { printf 'Missing value for --ack-context\\n' >&2; exit 64; }",
        '      ACK="$2"; shift 2 ;;',
        "    -h|--help) usage; exit 0 ;;",
        "    *) printf 'Unknown argument: %s\\n' \"$1\" >&2; usage >&2; exit 64 ;;",
        "  esac",
        "done",
        "",
        'if [[ "$MODE" == "apply" ]]; then',
        '  [[ "$ACK" == "$CONTEXT_SHA256" ]] || {',
        "    printf 'Refusing apply: pass --ack-context %s\\n' \"$CONTEXT_SHA256\" >&2",
        "    exit 65",
        "  }",
        "  ((EUID == 0)) || { printf 'Apply mode requires root.\\n' >&2; exit 77; }",
        "fi",
        "",
        "run_apply() {",
        '  if [[ "$MODE" == "apply" ]]; then',
        '    "$@"',
        '  elif [[ "$MODE" == "dry-run" ]]; then',
        "    printf 'DRY-RUN:'",
        "    printf ' %q' \"$@\"",
        "    printf '\\n'",
        "  else",
        "    printf 'CHECK: planned change not executed. Use --dry-run to preview it.\\n'",
        "  fi",
        "}",
        "",
        "printf 'Vedha remediation artifact %s (%s mode)\\n' \"$ARTIFACT_ID\" \"$MODE\"",
    ]
    for operation in operations:
        lines.extend((
            "",
            f"# Operation {operation.operation_id}: {_shell_comment(operation.title)}",
            "printf '%s\\n' '--- Pre-change check ---'",
        ))
        lines.extend(_bash_command(command) for command in operation.check)
        lines.append("printf '%s\\n' '--- Planned change ---'")
        lines.extend(f"run_apply {_bash_command(command)}" for command in operation.apply)
        lines.append("printf '%s\\n' '--- Current/post-change verification ---'")
        lines.extend(_bash_command(command) for command in operation.verify)
        for guidance in operation.rollback_guidance:
            lines.append(f"# Rollback: {_shell_comment(guidance)}")
    lines.extend(("", "printf '%s\\n' 'Artifact processing complete.'", ""))
    return "\n".join(lines)


def _render_powershell(
    *,
    artifact_id: uuid.UUID,
    asset_id: uuid.UUID | None,
    os_family: OsFamily,
    context_sha256: str,
    operations: Sequence[Operation],
) -> str:
    del os_family
    finding_ids = sorted(
        {item for operation in operations for item in operation.finding_ids}, key=str
    )
    lines = [
        "# Generated by Vedha RemediationWorkspace from reviewed operation templates.",
        "# Review this artifact before use. It performs no change unless -Mode Apply and",
        "# the exact -AckContext value are both supplied.",
        f"# Asset: {_asset_key(asset_id)}",
        f"# Findings: {', '.join(str(item) for item in finding_ids)}",
        f"# Context SHA-256: {context_sha256}",
        "[CmdletBinding(SupportsShouldProcess = $true, ConfirmImpact = 'High')]",
        "param(",
        "    [ValidateSet('Check', 'DryRun', 'Apply')]",
        "    [string]$Mode = 'Check',",
        "    [string]$AckContext = ''",
        ")",
        "Set-StrictMode -Version Latest",
        "$ErrorActionPreference = 'Stop'",
        f"$ArtifactId = '{artifact_id}'",
        f"$ContextSha256 = '{context_sha256}'",
        "",
        "if ($Mode -eq 'Apply' -and $AckContext -ne $ContextSha256) {",
        "    throw \"Refusing apply: pass -AckContext $ContextSha256\"",
        "}",
        "if ($Mode -eq 'Apply') {",
        "    $identity = [Security.Principal.WindowsIdentity]::GetCurrent()",
        "    $principal = [Security.Principal.WindowsPrincipal]::new($identity)",
        "    $isAdmin = $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)",
        "    if (-not $isAdmin) { throw 'Apply mode requires an elevated PowerShell session.' }",
        "}",
        "",
        "Write-Host \"Vedha remediation artifact $ArtifactId ($Mode mode)\"",
    ]
    for operation in operations:
        title = _clean_display(operation.title, maximum=160)
        lines.extend((
            "",
            f"# Operation {operation.operation_id}: {_shell_comment(title)}",
            "Write-Host '--- Pre-change check ---'",
        ))
        lines.extend(_powershell_command(command) for command in operation.check)
        lines.append("Write-Host '--- Planned change ---'")
        lines.append("if ($Mode -eq 'Apply') {")
        lines.append(
            "    if ($PSCmdlet.ShouldProcess('local system', "
            f"'{_powershell_single_quote(title)}')) {{"
        )
        lines.extend(f"        {_powershell_command(command)}" for command in operation.apply)
        lines.extend((
            "    }",
            "} elseif ($Mode -eq 'DryRun') {",
        ))
        for command in operation.apply:
            preview = _powershell_single_quote(_powershell_command(command))
            lines.append(f"    Write-Host 'DRY-RUN: {preview}'")
        lines.extend((
            "} else {",
            "    Write-Host 'CHECK: planned change not executed. Use -Mode DryRun to preview it.'",
            "}",
            "Write-Host '--- Current/post-change verification ---'",
        ))
        lines.extend(_powershell_command(command) for command in operation.verify)
        for guidance in operation.rollback_guidance:
            lines.append(f"# Rollback: {_shell_comment(guidance)}")
    lines.extend(("", "Write-Host 'Artifact processing complete.'", ""))
    return "\n".join(lines)


def _render_markdown(
    *,
    artifact_id: uuid.UUID,
    asset_id: uuid.UUID | None,
    os_family: OsFamily,
    context_sha256: str,
    operations: Sequence[Operation],
) -> str:
    finding_ids = sorted(
        {item for operation in operations for item in operation.finding_ids}, key=str
    )
    lines = [
        "# Vedha remediation runbook",
        "",
        f"- Artifact: `{artifact_id}`",
        f"- Asset: `{_asset_key(asset_id)}`",
        f"- Platform: `{os_family.value}`",
        f"- Context SHA-256: `{context_sha256}`",
        f"- Findings: {', '.join(f'`{item}`' for item in finding_ids)}",
        "",
        "> This runbook contains no executable artifact for these items. Review the",
        "> recorded evidence and authoritative vendor guidance before making a change.",
    ]
    for index, operation in enumerate(operations, start=1):
        lines.extend((
            "",
            f"## {index}. {_markdown_text(operation.title)}",
            "",
            f"Template: `{operation.template_id}@{operation.template_version}`  ",
            f"Risk: `{operation.risk.value}`",
        ))
        guidance = operation.manual_guidance or operation.rollback_guidance
        for item in guidance:
            lines.append(f"- {_markdown_text(item)}")
    lines.append("")
    return "\n".join(lines)


def _bash_command(command: CommandSpec) -> str:
    return shlex.join([command.program, *(str(argument) for argument in command.args)])


def _powershell_command(command: CommandSpec) -> str:
    rendered = [command.program]
    for argument in command.args:
        if isinstance(argument, int):
            rendered.append(str(argument))
        elif _POWERSHELL_SWITCH_RE.fullmatch(argument):
            rendered.append(argument)
        else:
            rendered.append(f"'{_powershell_single_quote(argument)}'")
    return " ".join(rendered)


def _powershell_single_quote(value: str) -> str:
    return value.replace("'", "''")


def _sanitize_advisory(advisory: Advisory) -> Advisory:
    if not isinstance(advisory.summary, str):
        raise ValueError("advisory summary must be a string")
    if not isinstance(advisory.notes, tuple) or any(
        not isinstance(note, str) for note in advisory.notes
    ):
        raise ValueError("advisory notes must be a tuple of strings")
    summary = _clean_display(advisory.summary, maximum=500)
    cleaned_notes = (_clean_display(note, maximum=500) for note in advisory.notes[:10])
    notes = tuple(note for note in cleaned_notes if note)
    return Advisory(summary=summary, notes=notes)


def _bounded_text(value: str, name: str, *, maximum: int, allow_empty: bool) -> None:
    if not isinstance(value, str):
        raise InvalidWorkspaceInput(f"{name} must be a string")
    if not allow_empty and not value.strip():
        raise InvalidWorkspaceInput(f"{name} must not be empty")
    if len(value) > maximum:
        raise InvalidWorkspaceInput(f"{name} exceeds {maximum} characters")
    if _contains_control(value):
        raise InvalidWorkspaceInput(f"{name} contains control characters")


def _clean_display(value: str, *, maximum: int) -> str:
    cleaned = "".join(
        " " if unicodedata.category(character) in {"Cc", "Cf"} else character
        for character in str(value)
    )
    return " ".join(cleaned.split())[:maximum].strip()


def _contains_control(value: str) -> bool:
    return bool(_CONTROL_RE.search(value)) or any(
        unicodedata.category(character) in {"Cc", "Cf"} for character in value
    )


def _shell_comment(value: str) -> str:
    return _clean_display(value, maximum=240).replace("#", "number-sign")


def _markdown_text(value: str) -> str:
    cleaned = _clean_display(value, maximum=500)
    for character in ("\\", "`", "[", "]", "<", ">", "#"):
        cleaned = cleaned.replace(character, f"\\{character}")
    return cleaned


def _asset_key(asset_id: uuid.UUID | None) -> str:
    return str(asset_id) if asset_id is not None else "unassigned"


__all__ = [
    "Advisory",
    "AdvisoryPort",
    "AdvisoryRequest",
    "ArtifactFormat",
    "BlockedFinding",
    "CATALOG_VERSION",
    "CommandSpec",
    "FindingContext",
    "InvalidWorkspaceInput",
    "MAX_FINDINGS",
    "Operation",
    "OperationKind",
    "OsFamily",
    "RemediationArtifact",
    "RemediationWorkspace",
    "RemediationWorkspaceError",
    "RiskLevel",
    "WorkspaceResult",
]

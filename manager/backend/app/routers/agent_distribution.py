"""Agent distribution: how a customer host gets the Vedha agent from this manager.

    GET /agent/install.sh          public   the release's Linux/macOS installer
    GET /agent/install.ps1         public   the Windows installer (PowerShell)
    GET /agent/install.cmd         public   the Windows launcher (cmd.exe / double-click)
    GET /agent/manifest.json       public   what the release contains (+ .sig, .p256.sig)
    GET /agent/image/{arch}        token    the agent image, only for a live
                                            enrolment token (Bearer vet_...)
    GET /agent/package/windows     token    the Windows agent package, same token rule
    GET /agent/release             operator release status for the Fleet page

The installer and manifest are public on purpose: they hold no secret, and the
customer (or their security team) should be able to read and verify them before
running anything. The image is not public — it is handed only to a host that
holds a live, unrevoked, unexpired enrolment token, so the agent never sits on
the open internet and every download is attributable to a token.
"""
from __future__ import annotations

import re
import shlex
from datetime import datetime, timezone
from pathlib import Path
from typing import Annotated

import structlog
from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import FileResponse, PlainTextResponse, Response
from sqlalchemy import select

from app import agent_release
from app.auth.rbac import require_role
from app.config import get_settings
from app.dependencies import AuthUser, DB, RedisConn
from app.models.probe_enrollment import ProbeEnrollmentToken
from app.ratelimit import client_ip
from app.routers.probe_enrollment import ENROLL_TOKEN_PREFIX, _secret_hash, enroll_token_is_usable

router = APIRouter(prefix="/agent", tags=["agent-distribution"])
logger = structlog.get_logger()

_NO_RELEASE_SCRIPT = """#!/bin/sh
# Served by the Vedha manager when no agent release can be handed out.
echo "Vedha: the agent installer is not available on this manager right now." >&2
echo "Ask your Vedha administrator to publish an agent release, then run the command again." >&2
exit 1
"""


def _require_signature() -> bool:
    settings = get_settings()
    return settings.is_production or settings.agent_release_require_signature


_NO_WINDOWS_PS1 = """# Served by the Vedha manager when no Windows agent can be handed out.
Write-Error "Vedha: the Windows agent installer is not available on this manager right now. Ask your Vedha administrator to publish an agent release that includes Windows."
"""

_NO_WINDOWS_CMD = """@echo off
echo Vedha: the Windows agent installer is not available on this manager right now. 1>&2
echo Ask your Vedha administrator to publish an agent release that includes Windows. 1>&2
exit /b 1
"""


def load_current_release() -> agent_release.AgentRelease:
    settings = get_settings()
    return agent_release.current_release(
        Path(settings.agent_release_dir),
        settings.agent_release_public_key,
        require_signature=_require_signature(),
        p256_public_key_b64=settings.agent_release_p256_public_key,
    )


def manager_url_for(request: Request | None = None) -> tuple[str, bool]:
    """(public manager URL, configured?). MANAGER_PUBLIC_URL is authoritative;
    the request's own base URL is only a development fallback (behind Caddy it
    can carry the wrong scheme), so the UI warns when it is used."""
    configured = get_settings().manager_public_url.strip().rstrip("/")
    if configured:
        return configured, True
    if request is not None:
        return str(request.base_url).rstrip("/"), False
    return "", False


def install_commands(manager_url: str, token: str | None = None) -> dict[str, str]:
    """The commands Fleet shows. Built here, once, so the operator console and the
    customer portal can never drift apart. Values are shell-quoted; the token is
    the only secret and it is single-use and short-lived."""
    manager = manager_url.rstrip("/")
    curl = "curl --proto '=https' --tlsv1.2 -fsSL" if manager.startswith("https://") else "curl -fsSL"
    args = f"--manager {shlex.quote(manager)}"
    if token:
        args += f" --token {shlex.quote(token)}"
    script_url = shlex.quote(f"{manager}/agent/install.sh")
    commands = {
        "one_line": f"{curl} {script_url} | sudo sh -s -- {args}",
        "download": f"{curl} -o vedha-install.sh {script_url}",
        "run": f"sudo sh vedha-install.sh {args}",
    }
    commands.update(windows_install_commands(manager, token))
    return commands


# What a value may contain to be pasted inside a PowerShell single-quoted string
# or a cmd.exe argument without any escaping. The manager URL comes from
# configuration and the token is a generated vet_ secret, so this is a guard
# against a surprising value, not a filter on normal input.
_SAFE_ARG = re.compile(r"[A-Za-z0-9:/._~+=@%-]+")


def windows_install_commands(manager_url: str, token: str | None = None) -> dict[str, str]:
    """The Windows one-liners, or {} if a value is not safe to embed unescaped.

    PowerShell (run from an ELEVATED prompt — it installs a service):
      windows_powershell   fetches install.ps1 and runs it with the manager + token
    cmd.exe / double-click:
      windows_cmd          fetches install.cmd (which self-elevates) and runs it
    Both fetch over TLS 1.2; the installer then verifies the signed manifest
    before it trusts anything it downloads."""
    manager = manager_url.rstrip("/")
    if not manager or not _SAFE_ARG.fullmatch(manager) or (token and not _SAFE_ARG.fullmatch(token)):
        return {}
    insecure = manager.startswith("http://")
    ps_args = (f"-Manager '{manager}'" + (f" -Token '{token}'" if token else "")
               + (" -AllowInsecureHttp" if insecure else ""))
    ps = (
        "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; "
        f"& ([scriptblock]::Create((irm '{manager}/agent/install.ps1'))) {ps_args}"
    )
    commands = {"windows_powershell": f'powershell -NoProfile -ExecutionPolicy Bypass -Command "{ps}"'}
    if not insecure:
        # The cmd launcher never forwards -AllowInsecureHttp, so an http:// (lab) manager
        # gets the PowerShell form only; offering a command that refuses to run helps no one.
        cmd_args = f'"{manager}"' + (f' "{token}"' if token else "")
        commands["windows_cmd"] = (
            f'curl.exe --proto =https --tlsv1.2 -fsSL "{manager}/agent/install.cmd" -o "%TEMP%\\vedha-install.cmd" '
            f'&& "%TEMP%\\vedha-install.cmd" {cmd_args}'
        )
    return commands


@router.api_route("/install.sh", methods=["GET", "HEAD"], include_in_schema=False)
async def install_script() -> Response:
    try:
        release = load_current_release()
    except agent_release.ReleaseUnavailable as exc:
        logger.warning("agent_distribution.install_unavailable", reason=exc.reason)
        return PlainTextResponse(
            _NO_RELEASE_SCRIPT,
            media_type="text/x-shellscript",
            headers={"Cache-Control": "no-store", "X-Vedha-Release": "none"},
        )
    return FileResponse(
        release.installer.path,
        media_type="text/x-shellscript",
        headers={
            "Cache-Control": "no-store",
            "X-Vedha-Release": release.version,
            "X-Vedha-Sha256": release.installer.sha256,
        },
    )


@router.api_route("/install.ps1", methods=["GET", "HEAD"], include_in_schema=False)
async def install_ps1() -> Response:
    return _windows_file("install.ps1", "windows_installer", "text/plain; charset=utf-8", _NO_WINDOWS_PS1)


@router.api_route("/install.cmd", methods=["GET", "HEAD"], include_in_schema=False)
async def install_cmd() -> Response:
    return _windows_file("install.cmd", "windows_launcher", "text/plain; charset=utf-8", _NO_WINDOWS_CMD)


def _windows_file(label: str, attr: str, media_type: str, unavailable_body: str) -> Response:
    """A Windows installer file, or a script that explains why there is none.
    Never a 5xx for a release that simply has no Windows package: the one-liner
    pipes this straight into an interpreter."""
    headers = {"Cache-Control": "no-store"}
    try:
        release = load_current_release()
    except agent_release.ReleaseUnavailable as exc:
        logger.warning("agent_distribution.windows_unavailable", file=label, reason=exc.reason)
        return PlainTextResponse(unavailable_body, media_type=media_type,
                                 headers={**headers, "X-Vedha-Release": "none"})
    entry = getattr(release, attr) if release.windows_available else None
    if entry is None:
        logger.info("agent_distribution.windows_not_offered", file=label, version=release.version,
                    reason=release.windows_unavailable or "release has no Windows package")
        return PlainTextResponse(unavailable_body, media_type=media_type,
                                 headers={**headers, "X-Vedha-Release": release.version})
    return FileResponse(entry.path, media_type=media_type,
                        headers={**headers, "X-Vedha-Release": release.version,
                                 "X-Vedha-Sha256": entry.sha256})


def _release_or_503() -> agent_release.AgentRelease:
    try:
        return load_current_release()
    except agent_release.ReleaseUnavailable as exc:
        logger.warning("agent_distribution.release_unavailable", reason=exc.reason)
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "No agent release is available") from exc


@router.api_route("/manifest.json", methods=["GET", "HEAD"], include_in_schema=False)
async def manifest() -> Response:
    release = _release_or_503()
    return FileResponse(
        release.directory / agent_release.MANIFEST_FILE,
        media_type="application/json",
        headers={"Cache-Control": "no-store", "X-Vedha-Release": release.version},
    )


@router.api_route("/manifest.json.sig", methods=["GET", "HEAD"], include_in_schema=False)
async def manifest_signature() -> Response:
    release = _release_or_503()
    if not release.signed:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "This release is not signed")
    return FileResponse(
        release.directory / agent_release.SIGNATURE_FILE,
        media_type="text/plain",
        headers={"Cache-Control": "no-store", "X-Vedha-Release": release.version},
    )


@router.api_route("/manifest.json.p256.sig", methods=["GET", "HEAD"], include_in_schema=False)
async def manifest_p256_signature() -> Response:
    release = _release_or_503()
    if not release.p256_signed:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "This release has no P-256 signature")
    return FileResponse(
        release.directory / agent_release.P256_SIGNATURE_FILE,
        media_type="text/plain",
        headers={"Cache-Control": "no-store", "X-Vedha-Release": release.version},
    )


async def _rate_limit_download(redis, request: Request) -> None:
    key = f"agent-distribution:image:{client_ip(request)}"
    try:
        count = await redis.incr(key)
        if count == 1:
            await redis.expire(key, 60)
    except Exception as exc:
        logger.error("agent_distribution.rate_limit_unavailable", error=str(exc))
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "Download rate limiter unavailable") from exc
    if count > 20:
        raise HTTPException(status.HTTP_429_TOO_MANY_REQUESTS, "Too many agent downloads; wait a minute")


async def _authorize_download(request: Request, db, redis) -> ProbeEnrollmentToken:
    """Rate-limit, then require a live enrolment token. Shared by every route that
    hands out an agent binary, so the Linux image and the Windows package can
    never be gated differently."""
    await _rate_limit_download(redis, request)

    auth = request.headers.get("Authorization", "")
    raw = auth.removeprefix("Bearer ").strip() if auth.startswith("Bearer ") else ""
    if not raw.startswith(ENROLL_TOKEN_PREFIX):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "An enrolment token is required to download the agent")
    token = (await db.execute(
        select(ProbeEnrollmentToken).where(ProbeEnrollmentToken.token_hash == _secret_hash(raw))
    )).scalar_one_or_none()
    if not enroll_token_is_usable(token, datetime.now(timezone.utc)):
        logger.warning("agent_distribution.image_token_rejected", ip=client_ip(request))
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "This enrolment token is invalid, expired, revoked or already used — create a new one in Fleet",
        )
    return token


@router.api_route("/package/{target}", methods=["GET", "HEAD"], include_in_schema=False)
async def agent_package(target: str, request: Request, db: DB, redis: RedisConn) -> Response:
    token = await _authorize_download(request, db, redis)
    if target != "windows":
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Unsupported package")
    release = _release_or_503()
    package = release.packages.get("windows") if release.windows_available else None
    if package is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            release.windows_unavailable or f"Release {release.version} has no Windows package",
        )
    logger.info(
        "agent_distribution.package_served",
        version=release.version, target=target, token_id=str(token.id),
        tenant_id=str(token.tenant_id), ip=client_ip(request),
    )
    headers = {"Cache-Control": "no-store", "X-Vedha-Release": release.version,
               "X-Vedha-Sha256": package.sha256}
    if package.authenticode_thumbprint:
        headers["X-Vedha-Authenticode-Thumbprint"] = package.authenticode_thumbprint
    return FileResponse(package.path, media_type="application/zip", filename=package.name, headers=headers)


@router.api_route("/image/{arch}", methods=["GET", "HEAD"], include_in_schema=False)
async def agent_image(arch: str, request: Request, db: DB, redis: RedisConn) -> Response:
    token = await _authorize_download(request, db, redis)

    if arch not in agent_release.ARCHES:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Unsupported architecture")
    release = _release_or_503()
    image = release.images.get(arch)
    if image is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"Release {release.version} has no {arch} image (available: {', '.join(release.arches)})",
        )
    logger.info(
        "agent_distribution.image_served",
        version=release.version, arch=arch, token_id=str(token.id),
        tenant_id=str(token.tenant_id), ip=client_ip(request),
    )
    return FileResponse(
        image.path,
        media_type="application/gzip",
        filename=image.name,
        headers={
            "Cache-Control": "no-store",
            "X-Vedha-Release": release.version,
            "X-Vedha-Sha256": image.sha256,
            "X-Vedha-Image-Tag": image.tag,
        },
    )


def release_status(*, detailed: bool, request: Request | None = None) -> dict:
    """What Fleet shows about the published release. Operators see why a release
    is unavailable; customers get a neutral message."""
    manager_url, configured = manager_url_for(request)
    body: dict = {"manager_url": manager_url, "manager_url_configured": configured}
    try:
        release = load_current_release()
    except agent_release.ReleaseUnavailable as exc:
        body.update(available=False, reason=exc.reason if detailed else "The agent installer is not available yet")
        return body
    body.update(
        available=True,
        version=release.version,
        created_at=release.created_at,
        arches=release.arches,
        signed=release.signed,
        signing_key_id=release.signing_key_id,
        installer_sha256=release.installer.sha256,
        sbom_sha256=release.sbom.sha256 if release.sbom else None,
        windows={
            "available": release.windows_available,
            "reason": "" if release.windows_available else (
                release.windows_unavailable or "this release has no Windows package"),
            "p256_signed": release.p256_signed,
            "p256_key_id": release.p256_key_id,
            "authenticode_thumbprint": (release.packages["windows"].authenticode_thumbprint or None)
            if release.windows_available else None,
        },
    )
    return body


@router.get("/release", summary="Published agent release (Fleet)")
async def get_release(
    request: Request,
    current_user: Annotated[AuthUser, require_role(["admin", "manager"])],
) -> dict:
    return release_status(detailed=True, request=request)


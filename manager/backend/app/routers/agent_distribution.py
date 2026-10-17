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
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Annotated

import structlog
from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import FileResponse, PlainTextResponse, Response
from pydantic import BaseModel, Field
from sqlalchemy import select

from app import agent_release
from app.auth.rbac import require_role
from app.config import get_settings
from app.dependencies import AuthUser, DB, RedisConn
from app.models.probe_enrollment import AgentInstallCode, ProbeEnrollmentToken
from app.ratelimit import client_ip
from app.services import agent_update_ticket
from app.services.audit import record_audit
from app.routers.probe_enrollment import (
    ENROLL_TOKEN_PREFIX,
    _secret_hash,
    enroll_token_is_usable,
    install_code_is_usable,
    mint_token_for_install_code,
)

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

# A well-formed install code: the vac_ prefix plus a url-safe base64 body
# (>=16 chars → >=128-bit codes). Used to reject junk before any DB lookup.
_INSTALL_CODE_RE = re.compile(r"vac_[A-Za-z0-9_\-]{16,}")


def windows_install_code_command(manager_url: str, code: str) -> str:
    """The ONE line an operator pastes to a Windows client for the zero-knowledge
    install. The only identity in it is the generic facade URL (passed as -Manager
    so the piped script knows where to redeem) and the opaque vac_ code — no
    manager IP/name beyond the facade, no key, no token. Returns '' if a value is
    not safe to embed unescaped (e.g. a plain-http lab manager)."""
    manager = manager_url.rstrip("/")
    if (not manager or not manager.startswith("https://") or not _SAFE_ARG.fullmatch(manager)
            or not _INSTALL_CODE_RE.fullmatch(code)):
        return ""
    return (
        f"& ([scriptblock]::Create((irm '{manager}/agent/install.ps1'))) "
        f"-Manager '{manager}' -Code '{code}'"
    )


def windows_install_commands(manager_url: str, token: str | None = None) -> dict[str, str]:
    """The Windows one-liners, or {} if a value is not safe to embed unescaped.

    windows_powershell   works from ANY window (Command Prompt or an ordinary PowerShell): it fetches
                         install.ps1 and runs it with the manager + token, and when it is not
                         elevated the installer asks Windows for administrator permission (UAC) and
                         continues in a new Administrator window
    cmd.exe / double-click:
      windows_cmd          fetches install.cmd (which self-elevates) and runs it
    Both fetch over TLS 1.2; the installer then verifies the signed manifest
    before it trusts anything it downloads. https:// managers only."""
    manager = manager_url.rstrip("/")
    # The Windows agent only talks to an https:// manager (its installer refuses anything else),
    # so a plain-http lab manager gets Linux commands only rather than a command that cannot run.
    if (not manager or not manager.startswith("https://") or not _SAFE_ARG.fullmatch(manager)
            or (token and not _SAFE_ARG.fullmatch(token))):
        return {}
    ps_args = f"-Manager '{manager}'" + (f" -Token '{token}'" if token else "")
    ps = (
        "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; "
        f"& ([scriptblock]::Create((irm '{manager}/agent/install.ps1'))) {ps_args}"
    )
    cmd_args = f'"{manager}"' + (f' "{token}"' if token else "")
    return {
        "windows_powershell": f'powershell -NoProfile -ExecutionPolicy Bypass -Command "{ps}"',
        "windows_cmd": (
            f'curl.exe --proto =https --tlsv1.2 -fsSL "{manager}/agent/install.cmd" -o "%TEMP%\\vedha-install.cmd" '
            f'&& "%TEMP%\\vedha-install.cmd" {cmd_args}'
        ),
    }


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


async def _rate_limit_tokenless(redis, request: Request) -> None:
    """Stricter than the shared limit: with no token there is nothing else tying a download to a person."""
    key = f"agent-distribution:tokenless:{client_ip(request)}"
    try:
        count = await redis.incr(key)
        if count == 1:
            await redis.expire(key, 60)
    except Exception as exc:
        logger.error("agent_distribution.rate_limit_unavailable", error=str(exc))
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "Download rate limiter unavailable") from exc
    if count > 6:
        raise HTTPException(status.HTTP_429_TOO_MANY_REQUESTS, "Too many tokenless downloads; wait a minute")


async def _authorize_update_ticket(raw: str, request: Request, db, redis):
    """An enrolled agent fetching its own update with the ticket the manager gave it.

    The ticket must be genuine and unexpired, belong to an agent that still exists and is
    active, and be spent now (single use). The manager also re-checks that the release it
    serves is STILL newer than what that agent runs, so a ticket cannot be used to install
    the same version again or to roll an agent back."""
    from types import SimpleNamespace

    from app.models.agent import Agent  # local: keep the router's import graph unchanged

    ticket = agent_update_ticket.verify(raw)
    if ticket is None:
        logger.warning("agent_distribution.update_ticket_rejected", ip=client_ip(request))
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                            "This update ticket is invalid or has expired; the agent will ask for a new one")
    try:
        agent_uuid = uuid.UUID(ticket.agent_id)
    except ValueError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "This update ticket is invalid")
    agent = (await db.execute(select(Agent).where(Agent.id == agent_uuid))).scalar_one_or_none()
    if (agent is None or str(agent.tenant_id) != ticket.tenant_id
            or getattr(agent, "lifecycle_status", "active") != "active"):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "This update ticket is no longer valid")
    release = _release_or_503()
    if not agent_release.agent_version_is_newer(release.agent_version, agent.agent_version):
        raise HTTPException(status.HTTP_409_CONFLICT, "This agent is already up to date")
    try:
        first_use = await redis.set(agent_update_ticket.spend_key(ticket), "1",
                                    nx=True, ex=agent_update_ticket.TTL_SECONDS + 60)
    except Exception as exc:
        logger.error("agent_distribution.update_ticket_unavailable", error=str(exc))
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "Update ticket check unavailable") from exc
    if not first_use:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "This update ticket was already used")
    logger.info("agent_distribution.update_ticket_spent", agent_id=ticket.agent_id,
                from_version=agent.agent_version, to_version=release.agent_version, ip=client_ip(request))
    return SimpleNamespace(id=f"update:{ticket.agent_id}", tenant_id=agent.tenant_id)


async def _authorize_download(request: Request, db, redis) -> ProbeEnrollmentToken:
    """Rate-limit, then require a live enrolment token. Shared by every route that
    hands out an agent binary, so the Linux image and the Windows package can
    never be gated differently."""
    await _rate_limit_download(redis, request)

    auth = request.headers.get("Authorization", "")
    raw = auth.removeprefix("Bearer ").strip() if auth.startswith("Bearer ") else ""
    if not auth.strip() and getattr(get_settings(), "agent_allow_tokenless_install", False):
        # Tokenless install (opt-in): no credential was offered at all. The package is signed and holds
        # no secret; the machine still has to be approved in Fleet with the code it shows before it can
        # do anything. A credential that IS offered but wrong is still refused below, never ignored.
        await _rate_limit_tokenless(redis, request)
        logger.info("agent_distribution.tokenless_download", ip=client_ip(request))
        from types import SimpleNamespace
        return SimpleNamespace(id="tokenless", tenant_id="none")
    if not raw.startswith(ENROLL_TOKEN_PREFIX):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "An enrolment token is required to download the agent")
    if agent_update_ticket.is_ticket(raw):
        return await _authorize_update_ticket(raw, request, db, redis)
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


_REDEEM_OPAQUE = (
    "This install code is not valid, or has already been used. "
    "Ask your Vedha contact for a new command."
)


class RedeemInput(BaseModel):
    code: str = Field(min_length=8, max_length=128)


async def _rate_limit_redeem(redis, request: Request) -> None:
    """The redeem endpoint is public and unauthenticated by design — the client holds
    no credential. Rate-limit it hard, and fail closed if the limiter is down."""
    key = f"agent-distribution:redeem:{client_ip(request)}"
    try:
        count = await redis.incr(key)
        if count == 1:
            await redis.expire(key, 60)
    except Exception as exc:
        logger.error("agent_distribution.rate_limit_unavailable", error=str(exc))
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "Install-code service unavailable") from exc
    if count > 10:
        raise HTTPException(status.HTTP_429_TOO_MANY_REQUESTS, "Too many install-code attempts; wait a minute")


@router.post("/redeem", summary="Redeem a one-command install code (public)")
async def redeem_install_code(body: RedeemInput, request: Request, db: DB, redis: RedisConn) -> dict:
    """Credential-less redeem: the client holds only the opaque vac_ code and no
    manager identity. Verify the code, mint the real vet_ token NOW (nothing was
    stored before this), burn the code single-use, record the redeemer IP, and hand
    the token back over TLS. Every invalid/used/expired/revoked code returns the
    SAME 404, so the endpoint cannot be used to discover which codes exist."""
    await _rate_limit_redeem(redis, request)
    now = datetime.now(timezone.utc)
    raw = body.code.strip()
    if not _INSTALL_CODE_RE.fullmatch(raw):
        raise HTTPException(status.HTTP_404_NOT_FOUND, _REDEEM_OPAQUE)
    code = (await db.execute(
        select(AgentInstallCode).where(AgentInstallCode.code_hash == _secret_hash(raw)).with_for_update()
    )).scalar_one_or_none()
    if not install_code_is_usable(code, now):
        logger.warning("agent_distribution.redeem_rejected", ip=client_ip(request), present=code is not None)
        raise HTTPException(status.HTTP_404_NOT_FOUND, _REDEEM_OPAQUE)
    # Mint the vet_ now. If the engagement/Site can no longer take an agent this
    # raises 404/409; get_db then rolls back and the code is NOT consumed, so a
    # transient problem can be retried once it is fixed.
    token, raw_vet = await mint_token_for_install_code(db, code, now)
    code.redeemed_at = now
    code.redeemed_ip = client_ip(request)[:45]
    code.minted_token_id = token.id
    # The caller is anonymous, so nothing in the request names a tenant: take it
    # from the code, or the entry lands where no organisation can read it.
    record_audit(
        db,
        actor_id=f"install-code:{code.id}",
        actor_type="anonymous",
        actor_label=f"install code {code.code_prefix}",
        action="agent.install_code.redeemed",
        resource_type="agent_install_code",
        resource_id=code.id,
        tenant_id=code.tenant_id,
        engagement_id=code.engagement_id,
        detail={"token_id": str(token.id)},
        ip=code.redeemed_ip,
    )
    manager_url, _ = manager_url_for(request)
    await db.commit()
    logger.info("agent_distribution.redeem_ok", code_id=str(code.id),
                token_id=str(token.id), ip=code.redeemed_ip)
    return {"manager_url": manager_url, "token": raw_vet, "token_expires_in_seconds": 3600}


def tokenless_status(manager_url: str) -> dict:
    """Whether this manager lets a machine install without a token, and the commands for it (no secret in them)."""
    enabled = bool(getattr(get_settings(), "agent_allow_tokenless_install", False))
    return {"enabled": enabled, "commands": install_commands(manager_url, None) if enabled else {}}


def release_status(*, detailed: bool, request: Request | None = None) -> dict:
    """What Fleet shows about the published release. Operators see why a release
    is unavailable; customers get a neutral message."""
    manager_url, configured = manager_url_for(request)
    body: dict = {"manager_url": manager_url, "manager_url_configured": configured}
    try:
        release = load_current_release()
    except agent_release.ReleaseUnavailable as exc:
        body.update(available=False, reason=exc.reason if detailed else "The agent installer is not available yet")
        body["tokenless"] = tokenless_status(manager_url)
        return body
    body["tokenless"] = tokenless_status(manager_url)
    body.update(
        available=True,
        version=release.version,
        agent_version=release.agent_version or None,
        created_at=release.created_at,
        arches=release.arches,
        signed=release.signed,
        signing_key_id=release.signing_key_id,
        installer_sha256=release.installer.sha256,
        sbom_sha256=release.sbom.sha256 if release.sbom else None,
        windows={
            "available": release.windows_available,
            # Operators see why; customers only see whether it is offered.
            "reason": "" if (release.windows_available or not detailed) else (
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


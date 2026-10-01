"""Agent distribution: how a customer host gets the Vedha agent from this manager.

    GET /agent/install.sh          public   the release's installer
    GET /agent/manifest.json       public   what the release contains (+ .sig)
    GET /agent/image/{arch}        token    the agent image, only for a live
                                            enrolment token (Bearer vet_...)
    GET /agent/release             operator release status for the Fleet page

The installer and manifest are public on purpose: they hold no secret, and the
customer (or their security team) should be able to read and verify them before
running anything. The image is not public — it is handed only to a host that
holds a live, unrevoked, unexpired enrolment token, so the agent never sits on
the open internet and every download is attributable to a token.
"""
from __future__ import annotations

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


def load_current_release() -> agent_release.AgentRelease:
    settings = get_settings()
    return agent_release.current_release(
        Path(settings.agent_release_dir),
        settings.agent_release_public_key,
        require_signature=_require_signature(),
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
    return {
        "one_line": f"{curl} {script_url} | sudo sh -s -- {args}",
        "download": f"{curl} -o vedha-install.sh {script_url}",
        "run": f"sudo sh vedha-install.sh {args}",
    }


@router.get("/install.sh", include_in_schema=False)
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


def _release_or_503() -> agent_release.AgentRelease:
    try:
        return load_current_release()
    except agent_release.ReleaseUnavailable as exc:
        logger.warning("agent_distribution.release_unavailable", reason=exc.reason)
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "No agent release is available") from exc


@router.get("/manifest.json", include_in_schema=False)
async def manifest() -> Response:
    release = _release_or_503()
    return FileResponse(
        release.directory / agent_release.MANIFEST_FILE,
        media_type="application/json",
        headers={"Cache-Control": "no-store", "X-Vedha-Release": release.version},
    )


@router.get("/manifest.json.sig", include_in_schema=False)
async def manifest_signature() -> Response:
    release = _release_or_503()
    if not release.signed:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "This release is not signed")
    return FileResponse(
        release.directory / agent_release.SIGNATURE_FILE,
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


@router.get("/image/{arch}", include_in_schema=False)
async def agent_image(arch: str, request: Request, db: DB, redis: RedisConn) -> Response:
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
    )
    return body


@router.get("/release", summary="Published agent release (Fleet)")
async def get_release(
    request: Request,
    current_user: Annotated[AuthUser, require_role(["admin", "manager"])],
) -> dict:
    return release_status(detailed=True, request=request)


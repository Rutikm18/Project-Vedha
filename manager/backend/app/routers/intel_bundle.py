"""
intel_bundle.py — install signed offline intel bundles (sovereign deployments).

  GET  /admin/intel-bundle   installed bundle manifest + whether import is configured
  POST /admin/intel-bundle   upload a .vib bundle → verify signature/hashes → install (admin, audited)
"""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.auth.rbac import require_role
from app.config import get_settings
from app.dependencies import DB, AuthUser
from app.intel.bundle import MAX_TOTAL_BYTES, BundleError, install_bundle, installed_manifest, verify_bundle
from app.services.audit import record_audit

router = APIRouter(prefix="/admin/intel-bundle", tags=["intel-bundle"])
Admin = Annotated[AuthUser, require_role(["admin"])]


def _config() -> tuple[str, list[str]]:
    settings = get_settings()
    keys = [k for k in settings.intel_bundle_public_keys.split(",") if k.strip()]
    return settings.vedha_intel_dir.strip(), keys


@router.get("", summary="Installed offline intel bundle")
async def intel_bundle_status(current_user: Admin):
    del current_user
    target, keys = _config()
    return {"configured": bool(target and keys), "intel_dir": target or None,
            "trusted_keys": len(keys), "installed": installed_manifest(target) if target else None}


@router.post("", summary="Verify and install a signed offline intel bundle")
async def intel_bundle_import(db: DB, current_user: Admin, file: UploadFile = File(...),
                              allow_downgrade: bool = False):
    target, keys = _config()
    if not target:
        raise HTTPException(409, "VEDHA_INTEL_DIR is not configured on this manager")
    data = await file.read(MAX_TOTAL_BYTES + 1)
    if len(data) > MAX_TOTAL_BYTES:
        raise HTTPException(413, "bundle exceeds the maximum size")
    try:
        manifest, files = verify_bundle(data, keys)
        record = install_bundle(manifest, files, target, allow_downgrade=allow_downgrade)
    except BundleError as exc:
        record_audit(db, actor_id=current_user.user_id, action="intel_bundle.rejected",
                     resource_type="intel_bundle", detail={"reason": str(exc), "filename": file.filename})
        await db.flush()
        raise HTTPException(422, str(exc)) from exc
    record_audit(db, actor_id=current_user.user_id, action="intel_bundle.installed",
                 resource_type="intel_bundle",
                 detail={"version": record["version"], "created_at": record["created_at"],
                         "files": record["files"], "allow_downgrade": allow_downgrade})
    await db.flush()
    return {"installed": record}

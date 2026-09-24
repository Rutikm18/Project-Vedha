"""Signed offline intel bundles for sovereign (air-gapped) manager deployments."""
from __future__ import annotations

import io
import json
import zipfile

import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from app.intel.bundle import (
    BundleError,
    build_bundle,
    install_bundle,
    installed_manifest,
    public_key_b64,
    verify_bundle,
)

FILES = {"kev_snapshot.json": b'{"cve_ids": ["CVE-2024-1"], "fetched_at": "2026-09-01"}',
         "epss_snapshot.json": b'{"scores": {}, "fetched_at": "2026-09-01"}'}


@pytest.fixture
def key():
    return Ed25519PrivateKey.generate()


def _trusted(key):
    return [public_key_b64(key.public_key())]


def test_round_trip(key, tmp_path):
    data = build_bundle(FILES, key, version="2026.09.24")
    manifest, files = verify_bundle(data, _trusted(key))
    assert manifest["version"] == "2026.09.24" and files == FILES
    install_bundle(manifest, files, tmp_path)
    assert (tmp_path / "kev_snapshot.json").read_bytes() == FILES["kev_snapshot.json"]
    assert installed_manifest(tmp_path)["version"] == "2026.09.24"


def test_wrong_key_is_rejected(key):
    data = build_bundle(FILES, key, version="1")
    with pytest.raises(BundleError, match="signature"):
        verify_bundle(data, [public_key_b64(Ed25519PrivateKey.generate().public_key())])


def test_no_trusted_keys_fails_closed(key):
    with pytest.raises(BundleError, match="trusted"):
        verify_bundle(build_bundle(FILES, key, version="1"), [])


def _rewrite(data: bytes, mutate) -> bytes:
    src = zipfile.ZipFile(io.BytesIO(data))
    members = {n: src.read(n) for n in src.namelist()}
    mutate(members)
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w") as z:
        for n, b in members.items():
            z.writestr(n, b)
    return out.getvalue()


def test_tampered_file_is_rejected(key):
    data = _rewrite(build_bundle(FILES, key, version="1"),
                    lambda m: m.__setitem__("files/kev_snapshot.json",
                                            FILES["kev_snapshot.json"].replace(b"CVE-2024-1", b"CVE-2024-9")))
    with pytest.raises(BundleError, match="hash"):
        verify_bundle(data, _trusted(key))


def test_tampered_manifest_is_rejected(key):
    def bump(m):
        manifest = json.loads(m["manifest.json"])
        manifest["version"] = "9999"
        m["manifest.json"] = json.dumps(manifest).encode()
    with pytest.raises(BundleError, match="signature"):
        verify_bundle(_rewrite(build_bundle(FILES, key, version="1"), bump), _trusted(key))


def test_extra_or_traversal_members_are_rejected(key):
    data = _rewrite(build_bundle(FILES, key, version="1"),
                    lambda m: m.__setitem__("../../etc/cron.d/x", b"boom"))
    with pytest.raises(BundleError, match="unexpected"):
        verify_bundle(data, _trusted(key))


def test_unknown_snapshot_name_cannot_be_built(key):
    with pytest.raises(BundleError, match="not an intel snapshot"):
        build_bundle({"../evil.json": b"{}"}, key, version="1")


def test_downgrade_is_refused_unless_forced(key, tmp_path):
    # Rollback protection keys on the SIGNED created_at, so build in real order.
    old = verify_bundle(build_bundle(FILES, key, version="2026.09.01"), _trusted(key))
    new = verify_bundle(build_bundle(FILES, key, version="2026.10.01"), _trusted(key))
    install_bundle(*new, tmp_path)
    with pytest.raises(BundleError, match="older"):
        install_bundle(*old, tmp_path)
    install_bundle(*old, tmp_path, allow_downgrade=True)
    assert installed_manifest(tmp_path)["version"] == "2026.09.01"


def test_detection_engine_prefers_installed_bundle(tmp_path, monkeypatch):
    import sys
    from pathlib import Path
    engine = Path(__file__).resolve().parents[2] / "detection_engine"
    monkeypatch.syspath_prepend(str(engine))
    import intel_paths  # type: ignore
    assert intel_paths.resolve("kev_snapshot.json").parent.name == "snapshots"
    (tmp_path / "kev_snapshot.json").write_text("{}")
    monkeypatch.setenv("VEDHA_INTEL_DIR", str(tmp_path))
    assert intel_paths.resolve("kev_snapshot.json") == tmp_path / "kev_snapshot.json"
    # a file the bundle did not ship falls back to the packaged snapshot
    assert intel_paths.resolve("epss_snapshot.json").parent.name == "snapshots"
    sys.modules.pop("intel_paths", None)


@pytest.mark.asyncio
async def test_admin_import_route_installs_and_audits(key, tmp_path, monkeypatch):
    import uuid
    from types import SimpleNamespace
    from unittest.mock import AsyncMock, MagicMock

    from fastapi import HTTPException
    from app.config import get_settings
    from app.models.audit_log import AuditLog
    from app.routers import intel_bundle as route

    settings = get_settings().model_copy(update={
        "vedha_intel_dir": str(tmp_path), "intel_bundle_public_keys": public_key_b64(key.public_key())})
    monkeypatch.setattr(route, "get_settings", lambda: settings)
    db = MagicMock(flush=AsyncMock(), add=MagicMock())
    user = SimpleNamespace(user_id=uuid.uuid4(), tenant_id=uuid.uuid4(), role="admin")

    upload = SimpleNamespace(filename="x.vib", read=AsyncMock(return_value=build_bundle(FILES, key, version="v1")))
    out = await route.intel_bundle_import(db, user, upload)
    assert out["installed"]["version"] == "v1"
    assert (tmp_path / "kev_snapshot.json").exists()
    assert db.add.call_args[0][0].action == "intel_bundle.installed"

    forged = build_bundle(FILES, Ed25519PrivateKey.generate(), version="v2")
    upload = SimpleNamespace(filename="evil.vib", read=AsyncMock(return_value=forged))
    with pytest.raises(HTTPException) as exc:
        await route.intel_bundle_import(db, user, upload)
    assert exc.value.status_code == 422
    assert isinstance(db.add.call_args[0][0], AuditLog) and db.add.call_args[0][0].action == "intel_bundle.rejected"
    assert installed_manifest(tmp_path)["version"] == "v1"

"""test_agent_distribution.py — the signed agent release store and the /agent routes.

The manager hands customers an agent image only from a verified release: the
manifest signature must check out, every file must be a plain name inside the
version directory, and every file must match its manifest hash. The image itself
is released only against a live enrolment token.
"""
from __future__ import annotations

import asyncio
import base64
import hashlib
import json
import os
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from fastapi import HTTPException
from starlette.requests import Request

from app import agent_release
from app.auth.middleware import _is_public_distribution_request
from app.config import Settings
from app.routers import agent_distribution as dist


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _keypair() -> tuple[Ed25519PrivateKey, str]:
    key = Ed25519PrivateKey.generate()
    return key, base64.b64encode(key.public_key().public_bytes_raw()).decode()


def build_release(
    root: Path,
    key: Ed25519PrivateKey | None,
    *,
    version: str = "1.0.400",
    arches: tuple[str, ...] = ("amd64", "arm64"),
    manifest_overrides: dict | None = None,
) -> Path:
    directory = root / version
    directory.mkdir(parents=True)
    installer = b"#!/bin/sh\necho vedha installer\n"
    (directory / "install.sh").write_bytes(installer)
    images = []
    for arch in arches:
        blob = f"image-{arch}".encode() * 100
        name = f"vedha-agent-{version}-{arch}.tar.gz"
        (directory / name).write_bytes(blob)
        images.append({"arch": arch, "file": name, "sha256": _sha(blob), "size": len(blob),
                       "tag": f"vedha-agent:{version}"})
    manifest = {
        "schema": 1, "version": version, "created_at": "2026-10-02T10:00:00+05:30",
        "installer": {"file": "install.sh", "sha256": _sha(installer)},
        "images": images,
    }
    manifest.update(manifest_overrides or {})
    raw = json.dumps(manifest, indent=2).encode()
    (directory / "manifest.json").write_bytes(raw)
    if key is not None:
        (directory / "manifest.json.sig").write_text(base64.b64encode(key.sign(raw)).decode())
    (root / "CURRENT").write_text(version + "\n")
    return directory


@pytest.fixture(autouse=True)
def _fresh_cache():
    agent_release.clear_cache()
    yield
    agent_release.clear_cache()


# ── release store ────────────────────────────────────────────────────────────

class TestLoadRelease:
    def test_signed_release_loads_with_both_arches(self, tmp_path):
        key, pub = _keypair()
        build_release(tmp_path, key)
        release = agent_release.load_release(tmp_path, pub)
        assert release.version == "1.0.400"
        assert release.signed is True
        assert release.arches == ["amd64", "arm64"]
        assert release.images["arm64"].tag == "vedha-agent:1.0.400"
        assert release.signing_key_id == agent_release.key_id(pub)

    def test_no_release_published(self, tmp_path):
        with pytest.raises(agent_release.ReleaseUnavailable, match="no agent release"):
            agent_release.load_release(tmp_path, "")

    def test_signature_from_another_key_is_rejected(self, tmp_path):
        key, _ = _keypair()
        _, other_pub = _keypair()
        build_release(tmp_path, key)
        with pytest.raises(agent_release.ReleaseUnavailable, match="signature"):
            agent_release.load_release(tmp_path, other_pub)

    def test_edited_manifest_breaks_the_signature(self, tmp_path):
        key, pub = _keypair()
        directory = build_release(tmp_path, key)
        manifest = directory / "manifest.json"
        manifest.write_bytes(manifest.read_bytes().replace(b"10:00:00", b"11:00:00"))
        with pytest.raises(agent_release.ReleaseUnavailable, match="signature"):
            agent_release.load_release(tmp_path, pub)

    def test_unsigned_release_refused_when_signature_required(self, tmp_path):
        build_release(tmp_path, None)
        with pytest.raises(agent_release.ReleaseUnavailable, match="AGENT_RELEASE_PUBLIC_KEY"):
            agent_release.load_release(tmp_path, "", require_signature=True)

    def test_unsigned_release_allowed_in_development(self, tmp_path):
        build_release(tmp_path, None)
        release = agent_release.load_release(tmp_path, "", require_signature=False)
        assert release.signed is False

    def test_missing_signature_file_with_a_key_configured(self, tmp_path):
        _, pub = _keypair()
        build_release(tmp_path, None)
        with pytest.raises(agent_release.ReleaseUnavailable, match="not signed"):
            agent_release.load_release(tmp_path, pub)

    def test_swapped_image_on_disk_is_caught(self, tmp_path):
        key, pub = _keypair()
        directory = build_release(tmp_path, key)
        (directory / "vedha-agent-1.0.400-amd64.tar.gz").write_bytes(b"malicious")
        with pytest.raises(agent_release.ReleaseUnavailable, match="checksum"):
            agent_release.load_release(tmp_path, pub)

    @pytest.mark.parametrize("bad", ["../escape", "/etc/passwd", "sub/dir.tar.gz", ".hidden"])
    def test_file_names_cannot_leave_the_release_directory(self, tmp_path, bad):
        key, pub = _keypair()
        build_release(tmp_path, key, manifest_overrides={"installer": {"file": bad, "sha256": "0" * 64}})
        with pytest.raises(agent_release.ReleaseUnavailable, match="invalid file name"):
            agent_release.load_release(tmp_path, pub)

    def test_symlink_out_of_the_release_is_refused(self, tmp_path):
        key, pub = _keypair()
        outside = tmp_path / "outside.sh"
        outside.write_bytes(b"#!/bin/sh\n")
        directory = tmp_path / "store"
        directory.mkdir()
        build_release(directory, key, manifest_overrides={
            "installer": {"file": "link.sh", "sha256": _sha(b"#!/bin/sh\n")}})
        os.symlink(outside, directory / "1.0.400" / "link.sh")
        with pytest.raises(agent_release.ReleaseUnavailable, match="not a regular file"):
            agent_release.load_release(directory, pub)

    @pytest.mark.parametrize("current", ["../1.0.400", "..", "a/b", ""])
    def test_current_must_name_a_plain_version(self, tmp_path, current):
        key, pub = _keypair()
        build_release(tmp_path, key)
        (tmp_path / "CURRENT").write_text(current)
        with pytest.raises(agent_release.ReleaseUnavailable):
            agent_release.load_release(tmp_path, pub)

    def test_manifest_version_must_match_current(self, tmp_path):
        key, pub = _keypair()
        build_release(tmp_path, key, manifest_overrides={"version": "9.9.9"})
        with pytest.raises(agent_release.ReleaseUnavailable, match="does not match CURRENT"):
            agent_release.load_release(tmp_path, pub)

    def test_unsupported_and_duplicate_architectures(self, tmp_path):
        key, pub = _keypair()
        build_release(tmp_path, key, arches=("amd64", "amd64"))
        with pytest.raises(agent_release.ReleaseUnavailable, match="twice"):
            agent_release.load_release(tmp_path, pub)

    def test_bad_public_key_is_reported_as_signature_failure(self, tmp_path):
        key, _ = _keypair()
        build_release(tmp_path, key)
        with pytest.raises(agent_release.ReleaseUnavailable, match="signature"):
            agent_release.load_release(tmp_path, "not-base64!")


class TestCache:
    def test_republish_invalidates_the_cached_release(self, tmp_path):
        key, pub = _keypair()
        build_release(tmp_path, key, version="1.0.1")
        assert agent_release.current_release(tmp_path, pub).version == "1.0.1"
        build_release(tmp_path, key, version="1.0.2")
        assert agent_release.current_release(tmp_path, pub).version == "1.0.2"

    def test_tampering_after_a_good_load_is_noticed(self, tmp_path):
        key, pub = _keypair()
        directory = build_release(tmp_path, key)
        agent_release.current_release(tmp_path, pub)
        image = directory / "vedha-agent-1.0.400-arm64.tar.gz"
        time.sleep(0.01)
        image.write_bytes(b"swapped after verification")
        with pytest.raises(agent_release.ReleaseUnavailable, match="checksum"):
            agent_release.current_release(tmp_path, pub)


# ── routes ───────────────────────────────────────────────────────────────────

def _settings(root: Path, pub: str = "", **kw) -> Settings:
    return Settings(agent_release_dir=str(root), agent_release_public_key=pub, **kw)


def _request(headers: dict[str, str] | None = None) -> Request:
    raw = [(k.lower().encode(), v.encode()) for k, v in (headers or {}).items()]
    return Request({"type": "http", "method": "GET", "path": "/agent/image/amd64", "headers": raw,
                    "client": ("203.0.113.9", 5555), "scheme": "https", "server": ("api", 443),
                    "query_string": b""})


def _redis(count: int = 1):
    redis = MagicMock()
    redis.incr = AsyncMock(return_value=count)
    redis.expire = AsyncMock()
    return redis


def _db(token):
    db = MagicMock()
    result = MagicMock()
    result.scalar_one_or_none = MagicMock(return_value=token)
    db.execute = AsyncMock(return_value=result)
    return db


def _token(**overrides):
    import uuid
    base = dict(id=uuid.uuid4(), tenant_id=uuid.uuid4(), revoked_at=None, uses=0, max_uses=1,
                expires_at=datetime.now(timezone.utc) + timedelta(hours=1))
    base.update(overrides)
    return SimpleNamespace(**base)


class TestRoutes:
    def test_install_script_falls_back_to_a_failing_script(self, tmp_path, monkeypatch):
        monkeypatch.setattr(dist, "get_settings", lambda: _settings(tmp_path))
        response = asyncio.run(dist.install_script())
        assert response.headers["x-vedha-release"] == "none"
        assert b"exit 1" in response.body
        # never leaks the operator-facing reason to the public
        assert b"AGENT_RELEASE" not in response.body

    def test_install_script_serves_the_verified_installer(self, tmp_path, monkeypatch):
        key, pub = _keypair()
        directory = build_release(tmp_path, key)
        monkeypatch.setattr(dist, "get_settings", lambda: _settings(tmp_path, pub))
        response = asyncio.run(dist.install_script())
        assert Path(response.path) == (directory / "install.sh").resolve()
        assert response.headers["x-vedha-release"] == "1.0.400"

    def test_production_refuses_an_unsigned_release(self, tmp_path, monkeypatch):
        build_release(tmp_path, None)
        monkeypatch.setattr(dist, "get_settings", lambda: _settings(tmp_path, app_env="production"))
        with pytest.raises(HTTPException) as exc:
            asyncio.run(dist.manifest())
        assert exc.value.status_code == 503

    def test_image_requires_an_enrolment_token(self, tmp_path, monkeypatch):
        key, pub = _keypair()
        build_release(tmp_path, key)
        monkeypatch.setattr(dist, "get_settings", lambda: _settings(tmp_path, pub))
        with pytest.raises(HTTPException) as exc:
            asyncio.run(dist.agent_image("amd64", _request(), _db(None), _redis()))
        assert exc.value.status_code == 401

    @pytest.mark.parametrize("overrides", [
        {"revoked_at": datetime.now(timezone.utc)},
        {"expires_at": datetime.now(timezone.utc) - timedelta(seconds=1)},
        {"uses": 1},
    ])
    def test_image_refuses_dead_tokens(self, tmp_path, monkeypatch, overrides):
        key, pub = _keypair()
        build_release(tmp_path, key)
        monkeypatch.setattr(dist, "get_settings", lambda: _settings(tmp_path, pub))
        request = _request({"Authorization": "Bearer vet_" + "x" * 40})
        with pytest.raises(HTTPException) as exc:
            asyncio.run(dist.agent_image("amd64", request, _db(_token(**overrides)), _redis()))
        assert exc.value.status_code == 401

    def test_image_is_served_for_a_live_token(self, tmp_path, monkeypatch):
        key, pub = _keypair()
        directory = build_release(tmp_path, key)
        monkeypatch.setattr(dist, "get_settings", lambda: _settings(tmp_path, pub))
        request = _request({"Authorization": "Bearer vet_" + "x" * 40})
        response = asyncio.run(dist.agent_image("arm64", request, _db(_token()), _redis()))
        assert Path(response.path) == (directory / "vedha-agent-1.0.400-arm64.tar.gz").resolve()
        assert response.headers["x-vedha-image-tag"] == "vedha-agent:1.0.400"
        assert len(response.headers["x-vedha-sha256"]) == 64

    def test_image_unknown_arch_and_missing_arch(self, tmp_path, monkeypatch):
        key, pub = _keypair()
        build_release(tmp_path, key, arches=("amd64",))
        monkeypatch.setattr(dist, "get_settings", lambda: _settings(tmp_path, pub))
        request = _request({"Authorization": "Bearer vet_" + "x" * 40})
        for arch in ("mips", "arm64"):
            with pytest.raises(HTTPException) as exc:
                asyncio.run(dist.agent_image(arch, request, _db(_token()), _redis()))
            assert exc.value.status_code == 404

    def test_image_downloads_are_rate_limited(self, tmp_path, monkeypatch):
        monkeypatch.setattr(dist, "get_settings", lambda: _settings(tmp_path))
        with pytest.raises(HTTPException) as exc:
            asyncio.run(dist.agent_image("amd64", _request(), _db(None), _redis(count=21)))
        assert exc.value.status_code == 429

    def test_release_status_hides_the_reason_from_customers(self, tmp_path, monkeypatch):
        monkeypatch.setattr(dist, "get_settings", lambda: _settings(tmp_path, manager_public_url="https://api.vedhasec.com/"))
        operator = dist.release_status(detailed=True)
        customer = dist.release_status(detailed=False)
        assert operator["available"] is False and "no agent release" in operator["reason"]
        assert "no agent release" not in customer["reason"]
        assert customer["manager_url"] == "https://api.vedhasec.com"
        assert customer["manager_url_configured"] is True


class TestInstallCommands:
    def test_https_commands_pin_tls_and_quote_values(self):
        cmds = dist.install_commands("https://api.vedhasec.com/", "vet_abc-DEF_123")
        assert cmds["one_line"] == (
            "curl --proto '=https' --tlsv1.2 -fsSL https://api.vedhasec.com/agent/install.sh"
            " | sudo sh -s -- --manager https://api.vedhasec.com --token vet_abc-DEF_123"
        )
        assert cmds["run"] == "sudo sh vedha-install.sh --manager https://api.vedhasec.com --token vet_abc-DEF_123"
        assert cmds["download"].endswith("-o vedha-install.sh https://api.vedhasec.com/agent/install.sh")

    def test_hostile_values_are_shell_quoted(self):
        cmds = dist.install_commands("https://x.example", "vet_$(id)")
        assert "'vet_$(id)'" in cmds["one_line"]

    def test_http_manager_has_no_proto_pin_and_no_token(self):
        cmds = dist.install_commands("http://10.0.0.5:18080")
        assert cmds["one_line"].startswith("curl -fsSL http://10.0.0.5:18080/agent/install.sh")
        assert "--token" not in cmds["one_line"]


class TestMiddlewareAllowlist:
    @pytest.mark.parametrize("path", ["/agent/install.sh", "/agent/manifest.json",
                                      "/agent/manifest.json.sig", "/agent/image/amd64"])
    def test_public_get_paths(self, path):
        assert _is_public_distribution_request(path, "GET")

    @pytest.mark.parametrize("path,method", [
        ("/agent/install.sh", "POST"),
        ("/agent/release", "GET"),           # operator-only
        ("/agent/image/../x", "GET"),
        ("/agents/heartbeat", "GET"),
    ])
    def test_everything_else_needs_auth(self, path, method):
        assert not _is_public_distribution_request(path, method)

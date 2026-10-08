"""
test_agent_distribution_windows.py — the manager serving a schema-2 release.

Releases are built with the REAL release tool (Docker faked), then loaded and
served by the REAL manager code, so the signer and the verifier cannot drift.
Pins: Windows needs its own signature, a missing P-256 key withholds Windows but
never Linux, a bad second signature rejects the whole release, the package is
gated by the same token rule as the Linux image, and the one-liners are safe.
"""
from __future__ import annotations

import asyncio
import base64
import importlib.util
import re
import shutil
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import HTTPException
from starlette.requests import Request

from app import agent_release
from app.auth.middleware import _is_public_distribution_request
from app.config import Settings
from app.routers import agent_distribution as dist

REPO = Path(__file__).resolve().parents[3]
_spec = importlib.util.spec_from_file_location("agent_release_tool", REPO / "scripts" / "agent_release.py")
tool = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(tool)

PS = "$script:VedhaReleaseP256Spki = ''\r\n$script:VedhaReleaseVersion = ''\r\nWrite-Host 'ok'\r\n"


@pytest.fixture(autouse=True)
def _fresh_cache():
    agent_release.clear_cache()
    yield
    agent_release.clear_cache()


@pytest.fixture
def world(tmp_path):
    """keys + sources + a store root; build() returns (version_dir, ed_pub, p256_pub)."""
    ed = tmp_path / "k" / "ed.pem"
    p256 = tmp_path / "k" / "p256.pem"
    ed_pub, p256_pub = tool.keygen(ed), tool.keygen_p256(p256)
    (tmp_path / "ps").write_bytes(PS.encode())
    (tmp_path / "cmd").write_bytes(b"@echo off\r\n")
    (tmp_path / "pkg.zip").write_bytes(b"PK fake" * 200)
    (tmp_path / "sbom.json").write_text("{}")

    def build(version="3.0.0", windows=True, thumb=None, arches=("amd64", "arm64")):
        return tool.build_release(
            key_path=ed, out=tmp_path / "store", arches=list(arches), version=version,
            builder=lambda *a: None, saver=lambda tag, dest: dest.write_bytes(tag.encode() * 30),
            p256_key_path=p256 if windows else None,
            windows_zip=tmp_path / "pkg.zip" if windows else None,
            authenticode_thumbprint=thumb, sbom_path=tmp_path / "sbom.json",
            windows_installer_source=tmp_path / "ps", windows_launcher_source=tmp_path / "cmd")

    return SimpleNamespace(root=tmp_path / "store", build=build, ed_pub=ed_pub, p256_pub=p256_pub,
                           tmp=tmp_path, p256_key=p256)


def _settings(world, **kw):
    base = dict(agent_release_dir=str(world.root), agent_release_public_key=world.ed_pub,
                agent_release_p256_public_key=world.p256_pub)
    base.update(kw)
    return Settings(**base)


def _request(headers=None):
    raw = [(k.lower().encode(), v.encode()) for k, v in (headers or {}).items()]
    return Request({"type": "http", "method": "GET", "path": "/agent/package/windows", "headers": raw,
                    "client": ("203.0.113.9", 5555), "scheme": "https", "server": ("api", 443),
                    "query_string": b""})


def _redis(count=1):
    r = MagicMock()
    r.incr = AsyncMock(return_value=count)
    r.expire = AsyncMock()
    return r


def _db(token):
    db = MagicMock()
    res = MagicMock()
    res.scalar_one_or_none = MagicMock(return_value=token)
    db.execute = AsyncMock(return_value=res)
    return db


def _token(**kw):
    import uuid
    base = dict(id=uuid.uuid4(), tenant_id=uuid.uuid4(), revoked_at=None, uses=0, max_uses=1,
                expires_at=datetime.now(timezone.utc) + timedelta(hours=1))
    base.update(kw)
    return SimpleNamespace(**base)


AUTH = {"Authorization": "Bearer vet_" + "x" * 40}


# ── loading ──────────────────────────────────────────────────────────────────

class TestLoad:
    def test_full_release_loads_with_windows_and_sbom(self, world):
        world.build(thumb="CD" * 20)
        r = agent_release.load_release(world.root, world.ed_pub, p256_public_key_b64=world.p256_pub)
        assert r.windows_available and r.p256_signed
        assert r.arches == ["amd64", "arm64"]
        pkg = r.packages["windows"]
        assert pkg.name == "vedha-agent-3.0.0-windows-amd64.zip"
        assert pkg.authenticode_thumbprint == "CD" * 20
        assert r.windows_installer.name == "install.ps1" and r.windows_launcher.name == "install.cmd"
        assert r.sbom is not None
        assert r.p256_key_id == agent_release.p256_key_id(world.p256_pub)

    def test_linux_only_release_is_unchanged(self, world):
        world.build(windows=False)
        r = agent_release.load_release(world.root, world.ed_pub)
        assert not r.windows_available and r.packages == {} and r.windows_unavailable == ""
        assert r.sbom is not None                           # SBOM alone is fine

    def test_no_p256_key_withholds_windows_but_serves_linux(self, world):
        world.build()
        r = agent_release.load_release(world.root, world.ed_pub, require_signature=True)
        assert r.arches == ["amd64", "arm64"]
        assert not r.windows_available
        assert "AGENT_RELEASE_P256_PUBLIC_KEY is not configured" in r.windows_unavailable

    def test_dev_mode_without_p256_key_offers_windows_unverified(self, world):
        world.build()
        r = agent_release.load_release(world.root, world.ed_pub, require_signature=False)
        assert r.windows_available and not r.p256_signed

    def test_missing_p256_signature_rejects_the_whole_release(self, world):
        d = world.build()
        (d / "manifest.json.p256.sig").unlink()
        with pytest.raises(agent_release.ReleaseUnavailable, match="no P-256 signature"):
            agent_release.load_release(world.root, world.ed_pub, p256_public_key_b64=world.p256_pub)

    def test_forged_p256_signature_rejects_the_whole_release(self, world):
        d = world.build()
        attacker = tool.keygen_p256(world.tmp / "attacker.pem")
        forged = tool.sign_manifest_p256(tool.load_p256_private_key(world.tmp / "attacker.pem"),
                                         (d / "manifest.json").read_bytes())
        (d / "manifest.json.p256.sig").write_text(forged)
        with pytest.raises(agent_release.ReleaseUnavailable, match="P-256 signature"):
            agent_release.load_release(world.root, world.ed_pub, p256_public_key_b64=world.p256_pub)
        assert attacker                                      # (key exists; it is just not trusted)

    def test_wrong_manager_p256_key_rejects(self, world):
        world.build()
        other = tool.keygen_p256(world.tmp / "other.pem")
        with pytest.raises(agent_release.ReleaseUnavailable, match="P-256 signature"):
            agent_release.load_release(world.root, world.ed_pub, p256_public_key_b64=other)

    def test_a_swapped_windows_package_is_caught(self, world):
        d = world.build()
        (d / "vedha-agent-3.0.0-windows-amd64.zip").write_bytes(b"evil")
        with pytest.raises(agent_release.ReleaseUnavailable, match="checksum"):
            agent_release.load_release(world.root, world.ed_pub, p256_public_key_b64=world.p256_pub)

    def test_a_swapped_windows_installer_is_caught(self, world):
        d = world.build()
        (d / "install.ps1").write_text("evil")
        with pytest.raises(agent_release.ReleaseUnavailable, match="checksum"):
            agent_release.load_release(world.root, world.ed_pub, p256_public_key_b64=world.p256_pub)

    def test_p256_key_must_be_a_p256_key(self):
        with pytest.raises(ValueError):
            agent_release.decode_p256_public_key(base64.b64encode(b"x" * 91).decode())
        from cryptography.hazmat.primitives import serialization
        from cryptography.hazmat.primitives.asymmetric import ec
        p384 = ec.generate_private_key(ec.SECP384R1()).public_key().public_bytes(
            serialization.Encoding.DER, serialization.PublicFormat.SubjectPublicKeyInfo)
        with pytest.raises(ValueError, match="P-256"):
            agent_release.decode_p256_public_key(base64.b64encode(p384).decode())

    def test_windows_only_release_with_no_linux_images(self, world):
        world.build(arches=())
        r = agent_release.load_release(world.root, world.ed_pub, p256_public_key_b64=world.p256_pub)
        assert r.images == {} and r.windows_available

    def test_unsupported_package_target_is_refused(self, world):
        # re-sign a hand-edited manifest so only the target check can fail
        d = world.build()
        import json
        m = json.loads((d / "manifest.json").read_text())
        m["packages"][0]["os"] = "plan9"
        raw = (json.dumps(m, indent=2, sort_keys=True) + "\n").encode()
        (d / "manifest.json").write_bytes(raw)
        (d / "manifest.json.sig").write_text(tool.sign_manifest(tool.load_private_key(world.tmp / "k" / "ed.pem"), raw))
        (d / "manifest.json.p256.sig").write_text(tool.sign_manifest_p256(tool.load_p256_private_key(world.p256_key), raw))
        with pytest.raises(agent_release.ReleaseUnavailable, match="unsupported package target"):
            agent_release.load_release(world.root, world.ed_pub, p256_public_key_b64=world.p256_pub)


# ── routes ───────────────────────────────────────────────────────────────────

class TestRoutes:
    def test_install_ps1_and_cmd_are_the_verified_release_files(self, world, monkeypatch):
        d = world.build()
        monkeypatch.setattr(dist, "get_settings", lambda: _settings(world))
        ps = asyncio.run(dist.install_ps1())
        cmd = asyncio.run(dist.install_cmd())
        assert Path(ps.path) == (d / "install.ps1").resolve()
        assert Path(cmd.path) == (d / "install.cmd").resolve()
        assert ps.headers["x-vedha-release"] == "3.0.0"
        assert "utf-8" in ps.headers["content-type"]

    def test_install_ps1_explains_when_there_is_no_windows_package(self, world, monkeypatch):
        world.build(windows=False)
        monkeypatch.setattr(dist, "get_settings", lambda: _settings(world))
        ps = asyncio.run(dist.install_ps1())
        cmd = asyncio.run(dist.install_cmd())
        assert b"Write-Error" in ps.body and b"not available" in ps.body
        assert b"exit /b 1" in cmd.body
        assert ps.status_code == 200 and cmd.status_code == 200      # never a 5xx into an interpreter

    def test_install_ps1_without_any_release(self, world, monkeypatch):
        monkeypatch.setattr(dist, "get_settings", lambda: _settings(world))
        ps = asyncio.run(dist.install_ps1())
        assert ps.headers["x-vedha-release"] == "none"
        assert b"AGENT_RELEASE" not in ps.body                       # no operator detail to the public

    def test_unconfigured_p256_key_is_not_leaked_to_the_public_but_stays_findable(self, world, monkeypatch):
        world.build()
        monkeypatch.setattr(dist, "get_settings",
                            lambda: _settings(world, agent_release_p256_public_key="", app_env="production"))
        ps = asyncio.run(dist.install_ps1())
        assert b"AGENT_RELEASE" not in ps.body and b"not available" in ps.body

    def test_p256_signature_route(self, world, monkeypatch):
        d = world.build()
        monkeypatch.setattr(dist, "get_settings", lambda: _settings(world))
        resp = asyncio.run(dist.manifest_p256_signature())
        assert Path(resp.path) == (d / "manifest.json.p256.sig").resolve()

    def test_p256_signature_404_for_a_linux_only_release(self, world, monkeypatch):
        world.build(windows=False)
        monkeypatch.setattr(dist, "get_settings", lambda: _settings(world))
        with pytest.raises(HTTPException) as exc:
            asyncio.run(dist.manifest_p256_signature())
        assert exc.value.status_code == 404

    def test_package_requires_a_token(self, world, monkeypatch):
        world.build()
        monkeypatch.setattr(dist, "get_settings", lambda: _settings(world))
        with pytest.raises(HTTPException) as exc:
            asyncio.run(dist.agent_package("windows", _request(), _db(None), _redis()))
        assert exc.value.status_code == 401

    @pytest.mark.parametrize("overrides", [
        {"revoked_at": datetime.now(timezone.utc)},
        {"expires_at": datetime.now(timezone.utc) - timedelta(seconds=1)},
        {"uses": 1},
    ])
    def test_package_refuses_dead_tokens_exactly_like_the_image(self, world, monkeypatch, overrides):
        world.build()
        monkeypatch.setattr(dist, "get_settings", lambda: _settings(world))
        with pytest.raises(HTTPException) as exc:
            asyncio.run(dist.agent_package("windows", _request(AUTH), _db(_token(**overrides)), _redis()))
        assert exc.value.status_code == 401

    def test_package_is_served_for_a_live_token_with_integrity_headers(self, world, monkeypatch):
        d = world.build(thumb="AB" * 20)
        monkeypatch.setattr(dist, "get_settings", lambda: _settings(world))
        resp = asyncio.run(dist.agent_package("windows", _request(AUTH), _db(_token()), _redis()))
        assert Path(resp.path) == (d / "vedha-agent-3.0.0-windows-amd64.zip").resolve()
        assert resp.headers["x-vedha-authenticode-thumbprint"] == "AB" * 20
        assert len(resp.headers["x-vedha-sha256"]) == 64
        assert resp.media_type == "application/zip"

    def test_package_unknown_target_404(self, world, monkeypatch):
        world.build()
        monkeypatch.setattr(dist, "get_settings", lambda: _settings(world))
        with pytest.raises(HTTPException) as exc:
            asyncio.run(dist.agent_package("macos", _request(AUTH), _db(_token()), _redis()))
        assert exc.value.status_code == 404

    def test_package_404_when_windows_is_withheld(self, world, monkeypatch):
        world.build()
        monkeypatch.setattr(dist, "get_settings",
                            lambda: _settings(world, agent_release_p256_public_key="", app_env="production"))
        with pytest.raises(HTTPException) as exc:
            asyncio.run(dist.agent_package("windows", _request(AUTH), _db(_token()), _redis()))
        assert exc.value.status_code == 404 and "P256" in exc.value.detail

    def test_package_downloads_are_rate_limited(self, world, monkeypatch):
        world.build()
        monkeypatch.setattr(dist, "get_settings", lambda: _settings(world))
        with pytest.raises(HTTPException) as exc:
            asyncio.run(dist.agent_package("windows", _request(AUTH), _db(_token()), _redis(count=21)))
        assert exc.value.status_code == 429

    def test_release_status_reports_windows(self, world, monkeypatch):
        world.build(thumb="EF" * 20)
        monkeypatch.setattr(dist, "get_settings", lambda: _settings(world))
        status = dist.release_status(detailed=True)
        assert status["windows"]["available"] is True and status["windows"]["p256_signed"] is True
        assert status["windows"]["authenticode_thumbprint"] == "EF" * 20
        assert status["sbom_sha256"]

    def test_release_status_explains_withheld_windows_to_operators(self, world, monkeypatch):
        world.build()
        monkeypatch.setattr(dist, "get_settings",
                            lambda: _settings(world, agent_release_p256_public_key="", app_env="production"))
        status = dist.release_status(detailed=True)
        assert status["available"] is True and status["windows"]["available"] is False
        assert "P256" in status["windows"]["reason"]
        customer = dist.release_status(detailed=False)
        assert customer["windows"]["available"] is False and customer["windows"]["reason"] == ""


# ── public-path allowlist ────────────────────────────────────────────────────

class TestPublicPaths:
    @pytest.mark.parametrize("path", ["/agent/install.ps1", "/agent/install.cmd",
                                      "/agent/manifest.json.p256.sig", "/agent/package/windows"])
    def test_new_routes_are_reachable_without_a_jwt(self, path):
        assert _is_public_distribution_request(path, "GET")
        assert _is_public_distribution_request(path, "HEAD")

    @pytest.mark.parametrize("path,method", [
        ("/agent/install.ps1", "POST"), ("/agent/install.exe", "GET"),
        ("/agent/package/../x", "GET"), ("/agent/package/windows/extra", "GET"),
        ("/agent/manifest.json.p256.sig.bak", "GET"),
    ])
    def test_nothing_else_is_opened(self, path, method):
        assert not _is_public_distribution_request(path, method)


# ── the one-liners ───────────────────────────────────────────────────────────

class TestWindowsCommands:
    def test_commands_for_https_manager_and_token(self):
        c = dist.install_commands("https://api.vedhasec.com/", "vet_abc123")
        ps, cmd = c["windows_powershell"], c["windows_cmd"]
        assert "irm 'https://api.vedhasec.com/agent/install.ps1'" in ps
        assert "-Manager 'https://api.vedhasec.com' -Token 'vet_abc123'" in ps
        assert "Tls12" in ps and ps.startswith("powershell -NoProfile")
        assert "--proto =https --tlsv1.2" in cmd and "install.cmd" in cmd
        assert cmd.endswith('"https://api.vedhasec.com" "vet_abc123"')
        assert c["one_line"].startswith("curl --proto '=https'")        # Linux commands unchanged

    def test_a_plain_http_manager_gets_linux_commands_only(self):
        c = dist.install_commands("http://10.0.0.5:18080", "vet_x")
        assert "windows_powershell" not in c and "windows_cmd" not in c      # the Windows agent needs https
        assert "one_line" in c

    def test_without_a_token_the_arguments_are_omitted(self):
        ps = dist.install_commands("https://m.example.com")["windows_powershell"]
        assert "-Token" not in ps and "-Manager 'https://m.example.com'" in ps

    @pytest.mark.parametrize("bad", ["https://m.example.com/'; calc; '", 'https://m"x', "https://m x",
                                     "https://m`n", "https://m$x", "https://m&calc", "https://m|calc"])
    def test_an_unsafe_manager_url_yields_no_windows_command(self, bad):
        c = dist.install_commands(bad, "vet_ok")
        assert "windows_powershell" not in c and "windows_cmd" not in c
        assert "one_line" in c                                          # Linux still produced

    @pytest.mark.parametrize("bad", ["vet_a'b", "vet_a b", 'vet_a"b', "vet_a;b", "vet_a$b", "vet_a`b"])
    def test_an_unsafe_token_yields_no_windows_command(self, bad):
        assert dist.windows_install_commands("https://m.example.com", bad) == {}

    def test_real_generated_tokens_are_accepted(self):
        import secrets
        token = "vet_" + secrets.token_urlsafe(32)
        assert "windows_powershell" in dist.install_commands("https://m.example.com", token)

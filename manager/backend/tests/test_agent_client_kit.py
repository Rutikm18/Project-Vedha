"""test_agent_client_kit.py — scripts/agent_client_kit.py packages what a client may receive.

The kit is the only thing sent to a client by email, so these tests pin what it
contains (installer, guide, checksums; never the agent image), and that it
refuses anything unsafe: an unverifiable release, a development installer, or a
plain-http manager.
"""
from __future__ import annotations

import hashlib
import importlib.util
import sys
import zipfile
from datetime import date
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]


def _load(name: str, file: str):
    spec = importlib.util.spec_from_file_location(name, REPO / "scripts" / file)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


release_tool = _load("agent_release", "agent_release.py")
kit_tool = _load("agent_client_kit", "agent_client_kit.py")


@pytest.fixture
def release(tmp_path):
    key = tmp_path / "keys" / "release.pem"
    public = release_tool.keygen(key)
    out = tmp_path / "releases"
    release_tool.build_release(
        key_path=key, out=out, arches=["amd64"], version="1.2.3",
        builder=lambda tag, arch, ctx: None,
        saver=lambda tag, dest: dest.write_bytes(b"fake image " * 100),
    )
    return out, public


def _kit(tmp_path, release, **kw):
    out, public = release
    args = dict(release=out, public_key_b64=public, customer="ACME Bank Ltd.",
                manager="https://api.vedhasec.com", contact="Asha, +91 00000", out=tmp_path / "kit",
                today=date(2026, 10, 3))
    args.update(kw)
    return kit_tool.build_kit(**args)


def test_kit_holds_only_installer_guide_and_checksums(tmp_path, release):
    kit = _kit(tmp_path, release)
    assert kit.name == "vedha-agent-kit-acme-bank-ltd-1.2.3"
    assert sorted(p.name for p in kit.iterdir()) == ["INSTALL.md", "SHA256SUMS", "vedha-agent-install.sh"]
    with zipfile.ZipFile(kit.parent / f"{kit.name}.zip") as zf:
        names = sorted(zf.namelist())
    assert names == [f"{kit.name}/{n}" for n in ("INSTALL.md", "SHA256SUMS", "vedha-agent-install.sh")]
    assert not any(n.endswith((".tar.gz", ".tar", ".py")) for n in names)


def test_checksums_and_guide_match_the_files(tmp_path, release):
    kit = _kit(tmp_path, release)
    for line in (kit / "SHA256SUMS").read_text().splitlines():
        digest, name = line.split("  ")
        assert hashlib.sha256((kit / name).read_bytes()).hexdigest() == digest
    guide = (kit / "INSTALL.md").read_text()
    installer_sha = hashlib.sha256((kit / "vedha-agent-install.sh").read_bytes()).hexdigest()
    _, public = release
    assert installer_sha in guide
    assert release_tool.key_id(public) in guide
    assert "--manager https://api.vedhasec.com --token-file" in guide
    assert "Prepared for:** ACME Bank Ltd." in guide and "2026-10-03" in guide
    assert "{{" not in guide


def test_installer_in_the_kit_is_the_signed_one(tmp_path, release):
    kit = _kit(tmp_path, release)
    _, public = release
    text = (kit / "vedha-agent-install.sh").read_text()
    assert f'VEDHA_RELEASE_SPKI="{release_tool.spki_b64_from_raw(public)}"' in text


def test_refuses_a_release_signed_with_another_key(tmp_path, release):
    other = release_tool.keygen(tmp_path / "other.pem")
    with pytest.raises(kit_tool.KitError, match="failed verification"):
        _kit(tmp_path, release, public_key_b64=other)


@pytest.mark.parametrize("manager", ["http://api.vedhasec.com", "https://api.vedhasec.com/path", "api.vedhasec.com"])
def test_refuses_a_manager_that_is_not_a_plain_https_origin(tmp_path, release, manager):
    with pytest.raises(kit_tool.KitError, match="--manager"):
        _kit(tmp_path, release, manager=manager)


def test_refuses_a_development_installer(tmp_path, release, monkeypatch):
    out, public = release
    version_dir = out / "1.2.3"
    installer = version_dir / "install.sh"
    # A tampered installer fails the release verification before anything is written.
    installer.write_text(installer.read_text().replace(
        f'VEDHA_RELEASE_SPKI="{release_tool.spki_b64_from_raw(public)}"', 'VEDHA_RELEASE_SPKI=""'))
    with pytest.raises(kit_tool.KitError):
        _kit(tmp_path, release)
    assert not (tmp_path / "kit").exists()


def test_customer_name_is_made_safe_for_file_names():
    assert kit_tool.slug("  ACME / Bank (India) ") == "acme-bank-india"
    with pytest.raises(kit_tool.KitError):
        kit_tool.slug("///")

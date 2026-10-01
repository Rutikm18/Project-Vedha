"""test_agent_release_tool.py — scripts/agent_release.py builds what the manager serves.

The release tool (build machine) and app.agent_release (manager) are two halves of
one contract. These tests build a release with the real tool — Docker replaced by
a fake builder/saver — and load it with the manager's verifier, so the two can
never drift apart silently. They also pin the installer embedding the tool does.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

from app import agent_release

REPO = Path(__file__).resolve().parents[3]
_spec = importlib.util.spec_from_file_location("agent_release_tool", REPO / "scripts" / "agent_release.py")
tool = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(tool)


def _fake_builder(calls):
    def build(tag, arch, context):
        calls.append((tag, arch))
    return build


def _fake_saver(tag, dest: Path):
    dest.write_bytes(f"fake docker save of {tag}".encode() * 50)


@pytest.fixture
def key(tmp_path):
    path = tmp_path / "keys" / "vedha.release-key.pem"
    public = tool.keygen(path)
    return path, public


def _build(tmp_path, key_path, version="1.0.500", arches=("amd64", "arm64"), calls=None):
    return tool.build_release(
        key_path=key_path, out=tmp_path / "out", arches=list(arches), version=version,
        builder=_fake_builder(calls if calls is not None else []), saver=_fake_saver,
    )


@pytest.fixture(autouse=True)
def _fresh_cache():
    agent_release.clear_cache()
    yield
    agent_release.clear_cache()


def test_keygen_writes_a_private_key_with_owner_only_permissions(key):
    path, public = key
    assert oct(path.stat().st_mode & 0o777) == "0o600"
    assert len(tool.key_id(public)) == 16
    with pytest.raises(tool.ReleaseError, match="refusing to overwrite"):
        tool.keygen(path)


def test_manager_accepts_what_the_tool_builds(tmp_path, key):
    key_path, public = key
    calls = []
    final = _build(tmp_path, key_path, calls=calls)

    assert calls == [("vedha-agent:1.0.500-amd64", "amd64"), ("vedha-agent:1.0.500-arm64", "arm64")]
    assert (tmp_path / "out" / "CURRENT").read_text().strip() == "1.0.500"
    release = agent_release.load_release(tmp_path / "out", public, require_signature=True)
    assert release.version == "1.0.500" and release.signed
    assert release.arches == ["amd64", "arm64"]
    assert release.images["amd64"].tag == "vedha-agent:1.0.500-amd64"
    assert release.directory == final.resolve()
    # no staging leftovers next to the release
    assert sorted(p.name for p in (tmp_path / "out").iterdir()) == ["1.0.500", "CURRENT"]


def test_installer_gets_the_release_key_and_version_embedded(tmp_path, key):
    key_path, public = key
    final = _build(tmp_path, key_path)
    text = (final / "install.sh").read_text()
    assert f'VEDHA_RELEASE_SPKI="{tool.spki_b64_from_raw(public)}"' in text
    assert 'VEDHA_RELEASE_VERSION="1.0.500"' in text
    assert 'VEDHA_RELEASE_SPKI=""' not in text
    # the SPKI is a real DER Ed25519 public key (what openssl reads)
    from cryptography.hazmat.primitives.serialization import load_der_public_key
    import base64
    loaded = load_der_public_key(base64.b64decode(tool.spki_b64_from_raw(public)))
    assert base64.b64encode(loaded.public_bytes_raw()).decode() == public


def test_installer_parser_reads_the_manifest_the_tool_writes(tmp_path, key):
    """install.sh reads image fields with awk from sorted, indented JSON. Run that
    exact awk program against a real manifest."""
    import subprocess

    key_path, _ = key
    final = _build(tmp_path, key_path)
    installer = (REPO / "probe" / "install.sh").read_text()
    start = installer.index("manifest_image_field() {")
    end = installer.index("\n}\n", start) + 3
    script = installer[start:end] + '\nmanifest_image_field "$1" "$2" "$3"\n'
    manifest = json.loads((final / "manifest.json").read_text())
    for image in manifest["images"]:
        for field in ("file", "sha256", "tag"):
            out = subprocess.run(["sh", "-c", script, "sh", str(final / "manifest.json"), image["arch"], field],
                                 capture_output=True, text=True, check=True).stdout.strip()
            assert out == image[field], (image["arch"], field)
    missing = subprocess.run(["sh", "-c", script, "sh", str(final / "manifest.json"), "riscv64", "file"],
                             capture_output=True, text=True, check=True).stdout.strip()
    assert missing == ""


def test_releases_are_immutable(tmp_path, key):
    key_path, _ = key
    _build(tmp_path, key_path)
    with pytest.raises(tool.ReleaseError, match="immutable"):
        _build(tmp_path, key_path)


def test_unknown_arch_and_bad_version_are_refused(tmp_path, key):
    key_path, _ = key
    with pytest.raises(tool.ReleaseError, match="unsupported architecture"):
        _build(tmp_path, key_path, arches=("s390x",))
    with pytest.raises(tool.ReleaseError, match="invalid version"):
        _build(tmp_path, key_path, version="../1.0")


def test_installer_without_markers_is_refused(tmp_path, key):
    key_path, _ = key
    bad = tmp_path / "install.sh"
    bad.write_text("#!/bin/sh\necho no markers\n")
    with pytest.raises(tool.ReleaseError, match="VEDHA_RELEASE_SPKI"):
        tool.build_release(key_path=key_path, out=tmp_path / "out", arches=["amd64"], version="1.0.1",
                           builder=_fake_builder([]), saver=_fake_saver, installer_source=bad)
    assert not (tmp_path / "out" / "1.0.1").exists()


def test_verify_catches_tampering_and_the_wrong_key(tmp_path, key):
    key_path, public = key
    final = _build(tmp_path, key_path)
    assert tool.verify_release_dir(final, public)["version"] == "1.0.500"

    other = tool.keygen(tmp_path / "other.pem")
    with pytest.raises(tool.ReleaseError, match="signature"):
        tool.verify_release_dir(final, other)

    (final / "vedha-agent-1.0.500-arm64.tar.gz").write_bytes(b"tampered")
    with pytest.raises(tool.ReleaseError, match="checksum"):
        tool.verify_release_dir(final, public)


def test_publish_to_a_local_store_flips_current_last(tmp_path, key):
    key_path, public = key
    _build(tmp_path, key_path, version="1.0.1")
    store = tmp_path / "manager-store"
    tool.publish(tmp_path / "out", str(store))
    assert (store / "CURRENT").read_text().strip() == "1.0.1"
    assert agent_release.load_release(store, public).version == "1.0.1"

    _build(tmp_path, key_path, version="1.0.2")
    tool.publish(tmp_path / "out" / "1.0.2", str(store))
    assert agent_release.load_release(store, public).version == "1.0.2"
    assert (store / "1.0.1").is_dir()  # previous release kept for rollback

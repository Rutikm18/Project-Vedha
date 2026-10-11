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
    assert oct(final.stat().st_mode & 0o777) == "0o755"  # readable by a non-root manager
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


# ── the agent's own version ──────────────────────────────────────────────────

def test_release_carries_the_agents_own_version_in_the_signed_manifest(tmp_path, key):
    """`version` names the platform release; `agent_version` is the agent's own
    number (probe/agent/version.py). They are different on purpose."""
    key_path, public = key
    final = _build(tmp_path, key_path, version="1.0.501")
    manifest = json.loads((final / "manifest.json").read_text())
    assert manifest["agent_version"] == tool.read_agent_version()
    assert manifest["version"] == "1.0.501" != manifest["agent_version"]
    release = agent_release.load_release(tmp_path / "out", public, require_signature=True)
    assert release.agent_version == tool.read_agent_version()
    assert tool.verify_release_dir(final, public)["agent_version"] == tool.read_agent_version()


def test_an_explicit_agent_version_wins_over_the_file(tmp_path, key):
    key_path, public = key
    tool.build_release(
        key_path=key_path, out=tmp_path / "out", arches=["amd64"], version="1.0.502",
        builder=_fake_builder([]), saver=_fake_saver, agent_version="7.8.9",
    )
    assert agent_release.load_release(tmp_path / "out", public).agent_version == "7.8.9"


@pytest.mark.parametrize("bad", ["", "v2.1", "two", "2.1 0", "2.1;x"])
def test_a_bad_agent_version_is_refused_before_anything_is_built(tmp_path, key, bad):
    key_path, _ = key
    calls = []
    with pytest.raises(tool.ReleaseError, match="agent version"):
        tool.build_release(
            key_path=key_path, out=tmp_path / "out", arches=["amd64"], version="1.0.503",
            builder=_fake_builder(calls), saver=_fake_saver, agent_version=bad,
        )
    assert calls == []


def test_read_agent_version_reads_text_and_refuses_a_missing_value(tmp_path):
    good = tmp_path / "version.py"
    good.write_text('"""doc"""\n\nAGENT_VERSION = "3.4.5"\n')
    assert tool.read_agent_version(good) == "3.4.5"
    bad = tmp_path / "bad.py"
    bad.write_text("nothing = 1\n")
    with pytest.raises(tool.ReleaseError, match="AGENT_VERSION"):
        tool.read_agent_version(bad)


def test_the_tool_reads_the_real_agent_version_file():
    text = (REPO / "probe" / "agent" / "version.py").read_text()
    assert f'AGENT_VERSION = "{tool.read_agent_version()}"' in text


# ── publishing from a machine without rsync (Windows) ────────────────────────

@pytest.mark.parametrize("dest, remote", [
    ("ubuntu@10.0.0.5:/opt/vedha/agent-releases", True),
    ("host:/srv/releases", True),
    ("C:\\agent-releases", False),            # a Windows drive is a local path, not host "C"
    ("D:/agent-releases", False),
    ("/var/lib/vedha/agent-releases", False),
])
def test_remote_destinations_are_told_apart_from_windows_and_local_paths(dest, remote):
    assert tool.is_remote_dest(dest) is remote


def test_publish_without_rsync_uses_ssh_and_scp_and_flips_current_last(tmp_path, key, monkeypatch):
    key_path, _ = key
    _build(tmp_path, key_path, version="1.0.7")
    calls: list[tuple[list[str], Path | None]] = []
    monkeypatch.setattr(tool, "_run", lambda cmd, cwd=None: calls.append((cmd, cwd)))
    monkeypatch.setattr(tool.shutil, "which", lambda name: None if name == "rsync" else f"/usr/bin/{name}")

    tool.publish(tmp_path / "out", "ubuntu@10.0.0.5:/opt/vedha/agent releases")

    kinds = [c[0][0] for c in calls]
    assert kinds == ["ssh", "scp", "ssh"]
    check, copy, finish = (c[0] for c in calls)
    assert "test ! -e" in check[2] and "immutable" in check[2]            # an existing version is refused
    assert copy[:2] == ["scp", "-r"] and copy[2] == "1.0.7"               # relative name: C:\... would read as a host
    assert calls[1][1] == (tmp_path / "out")
    assert copy[3] == "ubuntu@10.0.0.5:/opt/vedha/agent releases/"
    assert "mv -f" in finish[2] and finish[2].rstrip().endswith("agent releases'/CURRENT")  # CURRENT switched last, atomically
    assert "'/opt/vedha/agent releases'" in finish[2]                      # paths with spaces are quoted


def test_publish_without_rsync_or_ssh_says_what_to_install(tmp_path, key, monkeypatch):
    key_path, _ = key
    _build(tmp_path, key_path, version="1.0.8")
    monkeypatch.setattr(tool.shutil, "which", lambda name: None)
    with pytest.raises(tool.ReleaseError, match="OpenSSH Client"):
        tool.publish(tmp_path / "out", "ubuntu@10.0.0.5:/opt/vedha/agent-releases")


def test_publish_with_rsync_is_unchanged(tmp_path, key, monkeypatch):
    key_path, _ = key
    _build(tmp_path, key_path, version="1.0.9")
    calls: list[list[str]] = []
    monkeypatch.setattr(tool, "_run", lambda cmd, cwd=None: calls.append(cmd))
    monkeypatch.setattr(tool.shutil, "which", lambda name: f"/usr/bin/{name}")
    tool.publish(tmp_path / "out", "ubuntu@10.0.0.5:/opt/vedha/agent-releases")
    assert [c[0] for c in calls] == ["rsync", "rsync"]
    assert calls[1][-1].endswith("/agent-releases/CURRENT")


# ── pubkey: the public values of keys that already exist ─────────────────────

def test_pubkey_prints_the_same_values_keygen_printed(tmp_path, capsys):
    ed, p256 = tmp_path / "ed.pem", tmp_path / "p256.pem"
    ed_pub, p256_pub = tool.keygen(ed), tool.keygen_p256(p256)
    assert tool.main(["pubkey", "--key", str(ed), "--p256-key", str(p256)]) == 0
    out = capsys.readouterr().out.splitlines()
    assert out == [f"AGENT_RELEASE_PUBLIC_KEY={ed_pub}", f"AGENT_RELEASE_P256_PUBLIC_KEY={p256_pub}"]


def test_pubkey_needs_a_key_and_refuses_the_wrong_kind(tmp_path, capsys):
    assert tool.main(["pubkey"]) != 0
    ed, p256 = tmp_path / "ed.pem", tmp_path / "p256.pem"
    tool.keygen(ed), tool.keygen_p256(p256)
    assert tool.main(["pubkey", "--key", str(p256)]) != 0       # a P-256 file is not an Ed25519 key
    assert tool.main(["pubkey", "--p256-key", str(ed)]) != 0

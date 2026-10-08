"""
test_agent_release_windows.py — the Windows half of scripts/agent_release.py.

Windows PowerShell 5.1 cannot verify Ed25519, so a release that ships a Windows
package carries a SECOND signature over the same manifest: ECDSA P-256, in the
IEEE P1363 (r||s) form .NET expects. These tests pin that signature against
OpenSSL (an independent implementation), pin the exact key-blob construction the
installer performs, and pin that adding Windows does not disturb Linux installs.
"""
from __future__ import annotations

import base64
import importlib.util
import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
_spec = importlib.util.spec_from_file_location("agent_release_tool", REPO / "scripts" / "agent_release.py")
tool = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(tool)

PS_FIXTURE = (
    "# fixture installer\r\n"
    "$script:VedhaReleaseP256Spki = ''\r\n"
    "$script:VedhaReleaseVersion = ''\r\n"
    "Write-Host 'hi'\r\n"
)


def _fake_builder(tag, arch, context):
    return None


def _fake_saver(tag, dest: Path):
    dest.write_bytes(f"fake docker save of {tag}".encode() * 40)


@pytest.fixture
def keys(tmp_path):
    ed = tmp_path / "k" / "ed.pem"
    p256 = tmp_path / "k" / "p256.pem"
    ed_pub = tool.keygen(ed)
    p256_pub = tool.keygen_p256(p256)
    return ed, ed_pub, p256, p256_pub


@pytest.fixture
def sources(tmp_path):
    ps = tmp_path / "install-remote.ps1"
    ps.write_bytes(PS_FIXTURE.encode())
    cmd = tmp_path / "install-remote.cmd"
    cmd.write_bytes(b"@echo off\r\nrem launcher\r\n")
    zip_ = tmp_path / "agent-win.zip"
    zip_.write_bytes(b"PK\x03\x04 fake zip" * 100)
    sbom = tmp_path / "sbom.json"
    sbom.write_text('{"bomFormat": "CycloneDX"}')
    return ps, cmd, zip_, sbom


def _build(tmp_path, keys, sources, *, version="2.0.1", windows=True, sbom=False, thumb=None,
           out_name="out"):
    ed, _, p256, _ = keys
    ps, cmd, zip_, sbom_p = sources
    return tool.build_release(
        key_path=ed, out=tmp_path / out_name, arches=["amd64"], version=version,
        builder=_fake_builder, saver=_fake_saver,
        p256_key_path=p256 if windows else None,
        windows_zip=zip_ if windows else None,
        authenticode_thumbprint=thumb,
        sbom_path=sbom_p if sbom else None,
        windows_installer_source=ps, windows_launcher_source=cmd,
    )


# ── P-256 keys and signatures ────────────────────────────────────────────────

def test_p256_key_is_owner_only_and_never_overwritten(keys):
    _, _, p256, spki = keys
    assert oct(p256.stat().st_mode & 0o777) == "0o600"
    assert len(tool.p256_key_id(spki)) == 16
    with pytest.raises(tool.ReleaseError, match="refusing to overwrite"):
        tool.keygen_p256(p256)


def test_p256_loader_rejects_an_ed25519_key(keys):
    ed, *_ = keys
    with pytest.raises(tool.ReleaseError, match="not a P-256"):
        tool.load_p256_private_key(ed)


def test_signature_is_64_byte_p1363_and_round_trips(keys):
    _, _, p256, spki = keys
    key = tool.load_p256_private_key(p256)
    sig = tool.sign_manifest_p256(key, b"manifest bytes")
    assert len(base64.b64decode(sig)) == 64
    tool.verify_manifest_p256(spki, sig, b"manifest bytes")
    with pytest.raises(tool.ReleaseError):
        tool.verify_manifest_p256(spki, sig, b"manifest bytes!")


def test_signature_from_another_key_is_rejected(keys, tmp_path):
    _, _, p256, _ = keys
    other_spki = tool.keygen_p256(tmp_path / "other.pem")
    sig = tool.sign_manifest_p256(tool.load_p256_private_key(p256), b"m")
    with pytest.raises(tool.ReleaseError):
        tool.verify_manifest_p256(other_spki, sig, b"m")


def test_malformed_signature_inputs_are_rejected_not_crashed(keys):
    _, _, _, spki = keys
    for bad in ("", "not base64!!", base64.b64encode(b"\x00" * 63).decode(),
                base64.b64encode(b"\x00" * 65).decode()):
        with pytest.raises(tool.ReleaseError):
            tool.verify_manifest_p256(spki, bad, b"m")


@pytest.mark.skipif(shutil.which("openssl") is None, reason="openssl not installed")
def test_signature_verifies_with_openssl(keys, tmp_path):
    """Independent check: convert r||s back to DER and let OpenSSL verify it."""
    from cryptography.hazmat.primitives.asymmetric.utils import encode_dss_signature
    _, _, p256, spki = keys
    data = b'{"schema": 2}\n'
    raw = base64.b64decode(tool.sign_manifest_p256(tool.load_p256_private_key(p256), data))
    (tmp_path / "m.json").write_bytes(data)
    (tmp_path / "sig.der").write_bytes(encode_dss_signature(
        int.from_bytes(raw[:32], "big"), int.from_bytes(raw[32:], "big")))
    pem = "-----BEGIN PUBLIC KEY-----\n" + spki + "\n-----END PUBLIC KEY-----\n"
    (tmp_path / "pub.pem").write_text(pem)
    result = subprocess.run(
        ["openssl", "dgst", "-sha256", "-verify", str(tmp_path / "pub.pem"),
         "-signature", str(tmp_path / "sig.der"), str(tmp_path / "m.json")],
        capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert "Verified OK" in result.stdout


def test_cng_public_blob_matches_the_installers_construction(keys):
    """install-remote.ps1 turns the embedded SPKI into a BCRYPT_ECCPUBLIC_BLOB:
    strip the fixed 26-byte P-256 SPKI prefix, then 'ECS1' | 32 | X | Y. This
    mirrors that arithmetic and checks it against the key's real coordinates."""
    from cryptography.hazmat.primitives import serialization
    _, _, _, spki = keys
    der = base64.b64decode(spki)
    assert len(der) == 91
    assert der[:26] == bytes.fromhex("3059301306072a8648ce3d020106082a8648ce3d030107034200")
    point = der[26:]
    assert point[0] == 0x04 and len(point) == 65
    blob = (0x31534345).to_bytes(4, "little") + (32).to_bytes(4, "little") + point[1:]
    public = serialization.load_der_public_key(der).public_numbers()
    assert blob[8:40] == public.x.to_bytes(32, "big")
    assert blob[40:72] == public.y.to_bytes(32, "big")
    assert blob[:4] == b"ECS1"


# ── building a release with a Windows package ────────────────────────────────

def test_windows_release_is_schema_2_with_both_signatures(tmp_path, keys, sources):
    final = _build(tmp_path, keys, sources, sbom=True)
    manifest = json.loads((final / "manifest.json").read_text())
    assert manifest["schema"] == 2
    pkg = manifest["packages"][0]
    assert (pkg["os"], pkg["cpu"]) == ("windows", "amd64")
    assert "arch" not in pkg                       # install.sh's awk keys on "arch"
    assert pkg["file"] == "vedha-agent-2.0.1-windows-amd64.zip"
    assert manifest["windows_installer"]["file"] == "install.ps1"
    assert manifest["windows_launcher"]["file"] == "install.cmd"
    assert manifest["sbom"]["file"] == "sbom.cdx.json"
    assert manifest["p256_key_id"] == tool.p256_key_id(keys[3])
    for name in ("manifest.json.sig", "manifest.json.p256.sig", "install.ps1", "install.cmd",
                 "sbom.cdx.json", pkg["file"]):
        assert (final / name).is_file(), name
    tool.verify_release_dir(final, keys[1], p256_public_key_b64=keys[3])


def test_windows_installer_has_key_and_version_embedded(tmp_path, keys, sources):
    final = _build(tmp_path, keys, sources)
    raw = (final / "install.ps1").read_bytes()          # bytes: read_text() would hide CRLF
    text = raw.decode()
    assert f"$script:VedhaReleaseP256Spki = '{keys[3]}'" in text
    assert "$script:VedhaReleaseVersion = '2.0.1'" in text
    assert b"\r\n" in raw and b"\n" not in raw.replace(b"\r\n", b"")   # CRLF throughout


def test_release_without_windows_is_unchanged_schema_1(tmp_path, keys, sources):
    final = _build(tmp_path, keys, sources, windows=False)
    manifest = json.loads((final / "manifest.json").read_text())
    assert manifest["schema"] == 1
    # schema 1 is the original shape plus the agent version (an additive field older readers ignore)
    assert set(manifest) == {"schema", "version", "agent_version", "created_at", "installer", "images", "signing_key_id"}
    assert not (final / "manifest.json.p256.sig").exists()
    assert not (final / "install.ps1").exists()
    tool.verify_release_dir(final, keys[1])               # no P-256 key needed


def test_sbom_alone_is_schema_2_without_windows_files(tmp_path, keys, sources):
    final = _build(tmp_path, keys, sources, windows=False, sbom=True)
    manifest = json.loads((final / "manifest.json").read_text())
    assert manifest["schema"] == 2 and "packages" not in manifest
    assert (final / "sbom.cdx.json").is_file()
    tool.verify_release_dir(final, keys[1])


def test_windows_package_requires_the_p256_key(tmp_path, keys, sources):
    ed, _, _, _ = keys
    ps, cmd, zip_, _ = sources
    with pytest.raises(tool.ReleaseError, match="needs --p256-key"):
        tool.build_release(key_path=ed, out=tmp_path / "o", arches=["amd64"], version="1.0.0",
                           builder=_fake_builder, saver=_fake_saver, windows_zip=zip_,
                           windows_installer_source=ps, windows_launcher_source=cmd)


def test_missing_windows_zip_is_a_clear_error(tmp_path, keys, sources):
    ed, _, p256, _ = keys
    with pytest.raises(tool.ReleaseError, match="not found"):
        tool.build_release(key_path=ed, out=tmp_path / "o", arches=["amd64"], version="1.0.0",
                           builder=_fake_builder, saver=_fake_saver, p256_key_path=p256,
                           windows_zip=tmp_path / "nope.zip")


def test_authenticode_thumbprint_is_validated_and_normalised(tmp_path, keys, sources):
    with pytest.raises(tool.ReleaseError, match="40-hex"):
        _build(tmp_path, keys, sources, thumb="not-a-thumbprint", out_name="a")
    final = _build(tmp_path, keys, sources, thumb="ab" * 20, out_name="b")
    assert json.loads((final / "manifest.json").read_text())["packages"][0]["authenticode_thumbprint"] == "AB" * 20


def test_installer_without_markers_is_refused(tmp_path, keys, sources):
    ps, cmd, zip_, _ = sources
    ps.write_text("# no markers here\r\n")
    with pytest.raises(tool.ReleaseError, match="exactly one"):
        _build(tmp_path, keys, sources)


# ── tamper detection ─────────────────────────────────────────────────────────

def test_a_swapped_windows_package_is_caught(tmp_path, keys, sources):
    final = _build(tmp_path, keys, sources)
    pkg = final / "vedha-agent-2.0.1-windows-amd64.zip"
    pkg.write_bytes(pkg.read_bytes() + b"x")
    with pytest.raises(tool.ReleaseError, match="checksum"):
        tool.verify_release_dir(final, keys[1], p256_public_key_b64=keys[3])


def test_a_swapped_windows_installer_is_caught(tmp_path, keys, sources):
    final = _build(tmp_path, keys, sources)
    (final / "install.ps1").write_text("Write-Host 'evil'\r\n")
    with pytest.raises(tool.ReleaseError, match="checksum"):
        tool.verify_release_dir(final, keys[1], p256_public_key_b64=keys[3])


def test_a_removed_p256_signature_is_caught(tmp_path, keys, sources):
    final = _build(tmp_path, keys, sources)
    (final / "manifest.json.p256.sig").unlink()
    with pytest.raises(tool.ReleaseError, match="no manifest.json.p256.sig"):
        tool.verify_release_dir(final, keys[1], p256_public_key_b64=keys[3])


def test_a_forged_p256_signature_is_caught(tmp_path, keys, sources):
    final = _build(tmp_path, keys, sources)
    attacker = tool.load_p256_private_key(_make_key(tmp_path / "attacker.pem"))
    (final / "manifest.json.p256.sig").write_text(
        tool.sign_manifest_p256(attacker, (final / "manifest.json").read_bytes()) + "\n")
    with pytest.raises(tool.ReleaseError, match="P-256 signature"):
        tool.verify_release_dir(final, keys[1], p256_public_key_b64=keys[3])


def _make_key(path: Path) -> Path:
    tool.keygen_p256(path)
    return path


def test_verifying_a_windows_release_needs_the_p256_key(tmp_path, keys, sources):
    final = _build(tmp_path, keys, sources)
    with pytest.raises(tool.ReleaseError, match="pass the P-256 public key"):
        tool.verify_release_dir(final, keys[1])


# ── Linux installs are not disturbed by the new manifest keys ────────────────

def _awk_reader() -> str:
    text = (REPO / "probe" / "install.sh").read_text()
    match = re.search(r"^manifest_image_field\(\) \{.*?^\}\n", text, re.S | re.M)
    assert match, "manifest_image_field not found in install.sh"
    return match.group(0)


@pytest.mark.skipif(shutil.which("sh") is None or shutil.which("awk") is None, reason="needs sh + awk")
def test_install_sh_still_reads_the_docker_image_from_a_schema_2_manifest(tmp_path, keys, sources):
    """The shell installer reads the manifest with awk, keyed on `"arch":`. A
    Windows entry that reused that key would be picked up for an amd64 Linux
    host and its .zip handed to `docker load`."""
    final = _build(tmp_path, keys, sources, sbom=True)
    script = tmp_path / "reader.sh"
    script.write_text(_awk_reader() + '\nmanifest_image_field "$1" amd64 "$2"\n')
    for key, expected in (("file", "vedha-agent-2.0.1-amd64.tar.gz"),
                          ("tag", "vedha-agent:2.0.1-amd64")):
        out = subprocess.run(["sh", str(script), str(final / "manifest.json"), key],
                             capture_output=True, text=True, check=True).stdout.strip()
        assert out == expected
    absent = subprocess.run(["sh", str(script), str(final / "manifest.json"), "file"],
                            capture_output=True, text=True)
    assert "windows" not in absent.stdout


def test_keygen_can_add_the_p256_key_to_an_existing_ed25519_key(tmp_path, capsys):
    ed = tmp_path / "ed.pem"
    assert tool.main(["keygen", "--out", str(ed)]) == 0
    ed_bytes = ed.read_bytes()
    p256 = tmp_path / "p256.pem"
    assert tool.main(["keygen", "--p256-out", str(p256)]) == 0           # Windows added later
    assert ed.read_bytes() == ed_bytes and p256.exists()
    assert "AGENT_RELEASE_P256_PUBLIC_KEY=" in capsys.readouterr().out
    assert tool.main(["keygen", "--p256-out", str(p256)]) == 1           # never overwritten


def test_keygen_needs_something_to_generate(capsys):
    assert tool.main(["keygen"]) == 1
    assert "--out and/or --p256-out" in capsys.readouterr().err

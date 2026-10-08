#!/usr/bin/env python3
"""agent_release.py — build, sign, verify and publish the Vedha agent release.

Vedha is centrally hosted, so customers never pull the agent from a public
registry: the manager serves it (manager/backend/app/routers/agent_distribution.py)
from a signed release built here.

    keygen  --out FILE [--p256-out FILE]   new Ed25519 release key (+ P-256 key for Windows)
    build   --key FILE [--arch amd64,arm64] [--out DIR] [--from-image TAG]
            [--p256-key FILE --windows-zip ZIP [--authenticode-thumbprint HEX]] [--sbom FILE]
    verify  DIR --public-key B64 [--p256-public-key B64]
    publish DIR --to DEST              DEST = local dir or user@host:/path (rsync)

A release directory looks like:

    <out>/CURRENT                      the version to serve
    <out>/<version>/manifest.json      files, sizes, SHA-256, image tags
    <out>/<version>/manifest.json.sig  base64 Ed25519 signature of manifest.json
    <out>/<version>/install.sh         probe/install.sh with the release key embedded
    <out>/<version>/vedha-agent-<version>-<arch>.tar.gz
    # Windows (only when --windows-zip is given; schema 2):
    <out>/<version>/manifest.json.p256.sig   ECDSA P-256 signature of manifest.json
    <out>/<version>/install.ps1 + install.cmd   the Windows installer + launcher
    <out>/<version>/vedha-agent-<version>-windows-amd64.zip
    <out>/<version>/sbom.cdx.json

Why two signatures: install.sh verifies Ed25519 with OpenSSL. Windows PowerShell
5.1 / .NET Framework cannot verify Ed25519, but can verify ECDSA P-256 through
CNG, so Windows installs check the same manifest against a P-256 signature.

Signing needs Python's `cryptography` (the backend venv has it). macOS's
LibreSSL cannot do Ed25519, which is why this is Python and not openssl.
"""
from __future__ import annotations

import argparse
import base64
import gzip
import hashlib
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PROBE_DIR = REPO / "probe"
INSTALLER = PROBE_DIR / "install.sh"
WIN_INSTALLER = PROBE_DIR / "windows" / "install-remote.ps1"
WIN_LAUNCHER = PROBE_DIR / "windows" / "install-remote.cmd"
P256_SIG_FILE = "manifest.json.p256.sig"
WIN_PACKAGE_OS, WIN_PACKAGE_CPU = "windows", "amd64"
P256_MARKER = re.compile(r"^\$script:VedhaReleaseP256Spki = ''(.*)$", re.MULTILINE)
WIN_VERSION_MARKER = re.compile(r"^\$script:VedhaReleaseVersion = ''(.*)$", re.MULTILINE)
_THUMBPRINT_RE = re.compile(r"[0-9A-Fa-f]{40}")
ARCHES = ("amd64", "arm64")
IMAGE_REPO = "vedha-agent"
SPKI_MARKER = re.compile(r'^VEDHA_RELEASE_SPKI=""(.*)$', re.MULTILINE)
VERSION_MARKER = re.compile(r'^VEDHA_RELEASE_VERSION=""(.*)$', re.MULTILINE)
# DER prefix of an Ed25519 SubjectPublicKeyInfo; + the 32 raw key bytes.
_ED25519_SPKI_PREFIX = bytes.fromhex("302a300506032b6570032100")
_CHUNK = 1024 * 1024


class ReleaseError(Exception):
    pass


def _crypto():
    try:
        from cryptography.hazmat.primitives import serialization
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
    except ImportError as exc:  # pragma: no cover - environment dependent
        raise ReleaseError(
            "Python 'cryptography' is required to sign releases.\n"
            "  Fix: use the backend venv (manager/backend/.venv/bin/python) or `pip install cryptography`."
        ) from exc
    return serialization, Ed25519PrivateKey, Ed25519PublicKey


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(_CHUNK), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_version() -> str:
    return (REPO / "VERSION").read_text(encoding="utf-8").strip()


# ── keys ─────────────────────────────────────────────────────────────────────

def load_private_key(path: Path):
    serialization, Ed25519PrivateKey, _ = _crypto()
    data = path.read_bytes()
    key = serialization.load_pem_private_key(data, password=None)
    if not isinstance(key, Ed25519PrivateKey):
        raise ReleaseError(f"{path} is not an Ed25519 private key")
    return key


def public_raw_b64(private_key) -> str:
    serialization, _, _ = _crypto()
    # Encoding.Raw rather than public_bytes_raw(): that needs cryptography >= 40,
    # and Debian 12 / older build machines ship 38.
    raw = private_key.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    return base64.b64encode(raw).decode()


def spki_b64_from_raw(raw_b64: str) -> str:
    raw = base64.b64decode(raw_b64, validate=True)
    if len(raw) != 32:
        raise ReleaseError("public key must be 32 bytes")
    return base64.b64encode(_ED25519_SPKI_PREFIX + raw).decode()


def key_id(raw_b64: str) -> str:
    return hashlib.sha256(base64.b64decode(raw_b64, validate=True)).hexdigest()[:16]


def keygen(out: Path) -> str:
    serialization, Ed25519PrivateKey, _ = _crypto()
    if out.exists():
        raise ReleaseError(f"{out} already exists — refusing to overwrite a release key")
    key = Ed25519PrivateKey.generate()
    pem = key.private_bytes(
        serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption(),
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(out, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "wb") as handle:
        handle.write(pem)
    return public_raw_b64(key)



# ── P-256 key (Windows verification) ─────────────────────────────────────────

def _ec():
    try:
        from cryptography.hazmat.primitives import hashes, serialization
        from cryptography.hazmat.primitives.asymmetric import ec
        from cryptography.hazmat.primitives.asymmetric.utils import (
            decode_dss_signature, encode_dss_signature,
        )
    except ImportError as exc:  # pragma: no cover - environment dependent
        raise ReleaseError("Python 'cryptography' is required to sign releases.") from exc
    return hashes, serialization, ec, decode_dss_signature, encode_dss_signature


def load_p256_private_key(path: Path):
    _, serialization, ec, _, _ = _ec()
    key = serialization.load_pem_private_key(path.read_bytes(), password=None)
    if not isinstance(key, ec.EllipticCurvePrivateKey) or not isinstance(key.curve, ec.SECP256R1):
        raise ReleaseError(f"{path} is not a P-256 (secp256r1) private key")
    return key


def p256_spki_b64(private_key) -> str:
    """Base64 DER SubjectPublicKeyInfo — the form installers embed and the manager
    is configured with (AGENT_RELEASE_P256_PUBLIC_KEY)."""
    _, serialization, _, _, _ = _ec()
    der = private_key.public_key().public_bytes(
        serialization.Encoding.DER, serialization.PublicFormat.SubjectPublicKeyInfo)
    return base64.b64encode(der).decode()


def p256_key_id(spki_b64: str) -> str:
    return hashlib.sha256(base64.b64decode(spki_b64, validate=True)).hexdigest()[:16]


def keygen_p256(out: Path) -> str:
    _, serialization, ec, _, _ = _ec()
    if out.exists():
        raise ReleaseError(f"{out} already exists — refusing to overwrite a release key")
    key = ec.generate_private_key(ec.SECP256R1())
    pem = key.private_bytes(
        serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption())
    out.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(out, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "wb") as handle:
        handle.write(pem)
    return p256_spki_b64(key)


def sign_manifest_p256(private_key, manifest_bytes: bytes) -> str:
    """ECDSA-SHA256 as base64 of the 64-byte IEEE P1363 form (r || s). That is the
    encoding .NET's ECDsa.VerifyData expects; OpenSSL/Python emit ASN.1 DER."""
    hashes, _, ec, decode_dss_signature, _ = _ec()
    r, s = decode_dss_signature(private_key.sign(manifest_bytes, ec.ECDSA(hashes.SHA256())))
    return base64.b64encode(r.to_bytes(32, "big") + s.to_bytes(32, "big")).decode()


def verify_manifest_p256(spki_b64: str, signature_b64: str, manifest_bytes: bytes) -> None:
    hashes, serialization, ec, _, encode_dss_signature = _ec()
    try:
        raw = base64.b64decode(signature_b64.strip(), validate=True)
        if len(raw) != 64:
            raise ValueError("signature must be 64 bytes")
        public = serialization.load_der_public_key(base64.b64decode(spki_b64, validate=True))
        if not isinstance(public, ec.EllipticCurvePublicKey) or not isinstance(public.curve, ec.SECP256R1):
            raise ValueError("not a P-256 key")
        public.verify(encode_dss_signature(int.from_bytes(raw[:32], "big"), int.from_bytes(raw[32:], "big")),
                      manifest_bytes, ec.ECDSA(hashes.SHA256()))
    except Exception as exc:
        raise ReleaseError("manifest P-256 signature does not verify with this public key") from exc


# ── build ────────────────────────────────────────────────────────────────────

def embed_installer(source: Path, dest: Path, *, spki_b64: str, version: str) -> None:
    """Copy install.sh with the release public key and version baked in. The
    markers must each appear exactly once so a refactor can't silently ship an
    installer that verifies nothing."""
    text = source.read_text(encoding="utf-8")
    for marker, label in ((SPKI_MARKER, "VEDHA_RELEASE_SPKI"), (VERSION_MARKER, "VEDHA_RELEASE_VERSION")):
        if len(marker.findall(text)) != 1:
            raise ReleaseError(f"{source} must contain exactly one `{label}=\"\"` line")
    text = SPKI_MARKER.sub(lambda m: f'VEDHA_RELEASE_SPKI="{spki_b64}"{m.group(1)}', text, count=1)
    text = VERSION_MARKER.sub(lambda m: f'VEDHA_RELEASE_VERSION="{version}"{m.group(1)}', text, count=1)
    dest.write_text(text, encoding="utf-8")
    dest.chmod(0o755)



def embed_windows_installer(source: Path, dest: Path, *, p256_spki: str, version: str) -> None:
    """Copy install-remote.ps1 with the P-256 release key and version baked in.
    Exactly-one-marker rule, same as embed_installer."""
    if not source.is_file():
        raise ReleaseError(f"Windows installer source {source} not found")
    text = source.read_text(encoding="utf-8")
    for marker, label in ((P256_MARKER, "VedhaReleaseP256Spki"), (WIN_VERSION_MARKER, "VedhaReleaseVersion")):
        if len(marker.findall(text)) != 1:
            raise ReleaseError(f"{source} must contain exactly one `$script:{label} = ''` line")
    text = P256_MARKER.sub(lambda m: f"$script:VedhaReleaseP256Spki = '{p256_spki}'{m.group(1)}", text, count=1)
    text = WIN_VERSION_MARKER.sub(lambda m: f"$script:VedhaReleaseVersion = '{version}'{m.group(1)}", text, count=1)
    dest.write_text(text, encoding="utf-8", newline="\r\n")


def host_arch() -> str:
    machine = platform.machine().lower()
    return {"x86_64": "amd64", "amd64": "amd64", "aarch64": "arm64", "arm64": "arm64"}.get(machine, machine)


def _run(cmd: list[str]) -> None:
    print("  $ " + " ".join(cmd), flush=True)
    result = subprocess.run(cmd, check=False)
    if result.returncode != 0:
        raise ReleaseError(f"command failed ({result.returncode}): {' '.join(cmd)}")


def build_image(tag: str, arch: str, context: Path) -> None:
    """Build the agent image for one architecture. buildx cross-builds through
    QEMU (Docker Desktop ships it); the native arch uses a plain build."""
    if arch == host_arch():
        _run(["docker", "build", "--platform", f"linux/{arch}", "-t", tag, str(context)])
    else:
        _run(["docker", "buildx", "build", "--platform", f"linux/{arch}", "-t", tag, "--load", str(context)])


def save_image(tag: str, dest: Path) -> None:
    """`docker save | gzip` with a fixed gzip mtime so identical images give
    identical bytes."""
    proc = subprocess.Popen(["docker", "save", tag], stdout=subprocess.PIPE)
    assert proc.stdout is not None
    with dest.open("wb") as raw, gzip.GzipFile(fileobj=raw, mode="wb", compresslevel=6, mtime=0) as gz:
        for chunk in iter(lambda: proc.stdout.read(_CHUNK), b""):
            gz.write(chunk)
    if proc.wait() != 0:
        raise ReleaseError(f"docker save {tag} failed")


def image_arch(tag: str) -> str:
    out = subprocess.run(["docker", "image", "inspect", "--format", "{{.Architecture}}", tag],
                         capture_output=True, text=True, check=False)
    if out.returncode != 0:
        raise ReleaseError(f"image {tag} not found locally")
    return out.stdout.strip()


def sign_manifest(private_key, manifest_bytes: bytes) -> str:
    return base64.b64encode(private_key.sign(manifest_bytes)).decode()


def build_release(
    *,
    key_path: Path,
    out: Path,
    arches: list[str],
    version: str,
    from_images: dict[str, str] | None = None,
    builder=build_image,
    saver=save_image,
    installer_source: Path = INSTALLER,
    p256_key_path: Path | None = None,
    windows_zip: Path | None = None,
    authenticode_thumbprint: str | None = None,
    sbom_path: Path | None = None,
    windows_installer_source: Path = WIN_INSTALLER,
    windows_launcher_source: Path = WIN_LAUNCHER,
) -> Path:
    if windows_zip is not None:
        if p256_key_path is None:
            raise ReleaseError("a Windows package needs --p256-key: Windows verifies the P-256 signature")
        if not windows_zip.is_file():
            raise ReleaseError(f"Windows package {windows_zip} not found")
    if authenticode_thumbprint is not None and not _THUMBPRINT_RE.fullmatch(authenticode_thumbprint):
        raise ReleaseError("--authenticode-thumbprint must be the 40-hex SHA-1 thumbprint of the signing certificate")
    if authenticode_thumbprint is not None and windows_zip is None:
        raise ReleaseError("--authenticode-thumbprint only applies with --windows-zip")
    for arch in arches:
        if arch not in ARCHES:
            raise ReleaseError(f"unsupported architecture {arch!r} (supported: {', '.join(ARCHES)})")
    if not re.fullmatch(r"[0-9A-Za-z][0-9A-Za-z._-]{0,63}", version):
        raise ReleaseError(f"invalid version {version!r}")
    private_key = load_private_key(key_path)
    raw_b64 = public_raw_b64(private_key)
    p256_key = load_p256_private_key(p256_key_path) if p256_key_path else None
    p256_spki = p256_spki_b64(p256_key) if p256_key else ""

    out.mkdir(parents=True, exist_ok=True)
    final = out / version
    if final.exists():
        raise ReleaseError(f"{final} already exists — releases are immutable; bump VERSION")
    staging = Path(tempfile.mkdtemp(prefix=f".{version}-", dir=out))
    # mkdtemp is 0700; the manager may read the store as a non-root user.
    staging.chmod(0o755)
    try:
        installer = staging / "install.sh"
        embed_installer(installer_source, installer, spki_b64=spki_b64_from_raw(raw_b64), version=version)

        images = []
        for arch in arches:
            tag = (from_images or {}).get(arch) or f"{IMAGE_REPO}:{version}-{arch}"
            if not from_images or arch not in from_images:
                print(f"Building {tag} for linux/{arch} ...", flush=True)
                builder(tag, arch, PROBE_DIR)
            name = f"{IMAGE_REPO}-{version}-{arch}.tar.gz"
            print(f"Saving {tag} -> {name} ...", flush=True)
            saver(tag, staging / name)
            images.append({
                "arch": arch,
                "file": name,
                "sha256": sha256_file(staging / name),
                "size": (staging / name).stat().st_size,
                "tag": tag,
            })

        manifest = {
            "schema": 1,
            "version": version,
            "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "installer": {"file": "install.sh", "sha256": sha256_file(installer)},
            "images": images,
            "signing_key_id": key_id(raw_b64),
        }

        # ── schema 2 additions (Windows package, SBOM). Without them the manifest
        # stays exactly the schema-1 shape older managers and install.sh expect.
        if windows_zip is not None:
            win_installer = staging / "install.ps1"
            embed_windows_installer(windows_installer_source, win_installer,
                                    p256_spki=p256_spki, version=version)
            launcher = staging / "install.cmd"
            if not windows_launcher_source.is_file():
                raise ReleaseError(f"Windows launcher source {windows_launcher_source} not found")
            launcher.write_bytes(windows_launcher_source.read_bytes())
            pkg_name = f"{IMAGE_REPO}-{version}-{WIN_PACKAGE_OS}-{WIN_PACKAGE_CPU}.zip"
            shutil.copyfile(windows_zip, staging / pkg_name)
            # Entries use "cpu", never "arch": install.sh's awk reader keys on
            # `"arch":` to find a Docker image and must not see these.
            package = {
                "os": WIN_PACKAGE_OS, "cpu": WIN_PACKAGE_CPU, "file": pkg_name,
                "sha256": sha256_file(staging / pkg_name),
                "size": (staging / pkg_name).stat().st_size,
            }
            if authenticode_thumbprint:
                package["authenticode_thumbprint"] = authenticode_thumbprint.upper()
            manifest["packages"] = [package]
            manifest["windows_installer"] = {"file": "install.ps1", "sha256": sha256_file(win_installer)}
            manifest["windows_launcher"] = {"file": "install.cmd", "sha256": sha256_file(launcher)}
            manifest["p256_key_id"] = p256_key_id(p256_spki)
        if sbom_path is not None:
            if not sbom_path.is_file():
                raise ReleaseError(f"SBOM {sbom_path} not found")
            shutil.copyfile(sbom_path, staging / "sbom.cdx.json")
            manifest["sbom"] = {"file": "sbom.cdx.json", "sha256": sha256_file(staging / "sbom.cdx.json")}
        if "packages" in manifest or "sbom" in manifest:
            manifest["schema"] = 2

        manifest_bytes = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode()
        (staging / "manifest.json").write_bytes(manifest_bytes)
        (staging / "manifest.json.sig").write_text(sign_manifest(private_key, manifest_bytes) + "\n")
        if p256_key is not None:
            (staging / P256_SIG_FILE).write_text(sign_manifest_p256(p256_key, manifest_bytes) + "\n")
        verify_release_dir(staging, raw_b64, expect_version=version,
                           p256_public_key_b64=p256_spki or None)
        staging.rename(final)
    except BaseException:
        shutil.rmtree(staging, ignore_errors=True)
        raise
    _write_current(out, version)
    return final


def _write_current(root: Path, version: str) -> None:
    tmp = root / ".CURRENT.tmp"
    tmp.write_text(version + "\n", encoding="utf-8")
    tmp.replace(root / "CURRENT")


# ── verify ───────────────────────────────────────────────────────────────────

def verify_release_dir(directory: Path, public_key_b64: str, *, expect_version: str | None = None,
                       p256_public_key_b64: str | None = None) -> dict:
    """Signature(s), file names and hashes — the same checks the manager runs.
    A manifest that lists a Windows package must also carry a P-256 signature,
    and the caller must supply the P-256 key to check it against."""
    _, _, Ed25519PublicKey = _crypto()
    manifest_bytes = (directory / "manifest.json").read_bytes()
    signature = base64.b64decode((directory / "manifest.json.sig").read_bytes().strip(), validate=True)
    raw = base64.b64decode(public_key_b64, validate=True)
    try:
        Ed25519PublicKey.from_public_bytes(raw).verify(signature, manifest_bytes)
    except Exception as exc:
        raise ReleaseError("manifest signature does not verify with this public key") from exc
    manifest = json.loads(manifest_bytes)
    if expect_version is not None and manifest.get("version") != expect_version:
        raise ReleaseError("manifest version mismatch")
    entries = [("installer", manifest["installer"])] + [(f"{i['arch']} image", i) for i in manifest["images"]]
    has_windows = bool(manifest.get("packages"))
    if has_windows:
        if not p256_public_key_b64:
            raise ReleaseError("release has a Windows package: pass the P-256 public key to verify it")
        p256_sig = directory / P256_SIG_FILE
        if not p256_sig.is_file():
            raise ReleaseError(f"release has a Windows package but no {P256_SIG_FILE}")
        verify_manifest_p256(p256_public_key_b64, p256_sig.read_text(encoding="utf-8"), manifest_bytes)
        entries += [("windows installer", manifest["windows_installer"]),
                    ("windows launcher", manifest["windows_launcher"])]
        entries += [(f"{p['os']}/{p['cpu']} package", p) for p in manifest["packages"]]
    if manifest.get("sbom"):
        entries.append(("sbom", manifest["sbom"]))
    for label, entry in entries:
        name = entry["file"]
        if "/" in name or name.startswith("."):
            raise ReleaseError(f"{label}: invalid file name {name!r}")
        path = directory / name
        if not path.is_file() or path.is_symlink():
            raise ReleaseError(f"{label}: {name} missing")
        if sha256_file(path) != entry["sha256"]:
            raise ReleaseError(f"{label}: {name} does not match its checksum")
    installer_text = (directory / manifest["installer"]["file"]).read_text(encoding="utf-8")
    if f'VEDHA_RELEASE_SPKI="{spki_b64_from_raw(public_key_b64)}"' not in installer_text:
        raise ReleaseError("installer does not embed this release key")
    if has_windows:
        win_text = (directory / manifest["windows_installer"]["file"]).read_text(encoding="utf-8")
        if f"$script:VedhaReleaseP256Spki = '{p256_public_key_b64}'" not in win_text:
            raise ReleaseError("Windows installer does not embed this release key")
        if f"$script:VedhaReleaseVersion = '{manifest['version']}'" not in win_text:
            raise ReleaseError("Windows installer does not embed this release version")
    return manifest


def resolve_release_dir(path: Path) -> Path:
    """Accept either a version directory or a store root holding CURRENT."""
    if (path / "manifest.json").is_file():
        return path
    current = path / "CURRENT"
    if current.is_file():
        return path / current.read_text(encoding="utf-8").strip()
    raise ReleaseError(f"{path} is neither a release directory nor a store with CURRENT")


# ── publish ──────────────────────────────────────────────────────────────────

def publish(release_dir: Path, dest: str) -> None:
    """Copy one version into the manager's release store, then flip CURRENT —
    in that order, so the manager never points at a half-copied release."""
    release_dir = resolve_release_dir(release_dir)
    version = release_dir.name
    if ":" in dest and not dest.startswith("/") and not Path(dest).exists():
        host, _, remote = dest.partition(":")
        remote = remote.rstrip("/") or "."
        if shutil.which("rsync") is None:
            raise ReleaseError("rsync is required to publish to a remote host")
        _run(["rsync", "-a", "--chmod=Du=rwx,Dgo=rx,Fu=rw,Fgo=r", f"{release_dir}/", f"{host}:{remote}/{version}/"])
        with tempfile.TemporaryDirectory() as tmp:
            current = Path(tmp) / "CURRENT"
            current.write_text(version + "\n", encoding="utf-8")
            current.chmod(0o644)
            _run(["rsync", "-a", str(current), f"{host}:{remote}/CURRENT"])
        return
    root = Path(dest)
    root.mkdir(parents=True, exist_ok=True)
    target = root / version
    if target.exists():
        if target.resolve() != release_dir.resolve():
            raise ReleaseError(f"{target} already exists — releases are immutable")
    else:
        staging = root / f".{version}.partial"
        shutil.rmtree(staging, ignore_errors=True)
        shutil.copytree(release_dir, staging)
        staging.rename(target)
    _write_current(root, version)


# ── CLI ──────────────────────────────────────────────────────────────────────

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)

    kg = sub.add_parser("keygen", help="create a new Ed25519 release signing key")
    kg.add_argument("--out", required=True, type=Path)
    kg.add_argument("--p256-out", type=Path, help="also create the P-256 key Windows installs verify")

    bd = sub.add_parser("build", help="build + sign a release")
    bd.add_argument("--key", required=True, type=Path)
    bd.add_argument("--out", type=Path, default=REPO / "dist" / "agent-release")
    bd.add_argument("--arch", default=",".join(ARCHES))
    bd.add_argument("--version", default=None)
    bd.add_argument("--from-image", action="append", default=[], metavar="ARCH=TAG",
                    help="package an existing local image instead of building (repeatable)")
    bd.add_argument("--p256-key", type=Path, help="P-256 key (needed with --windows-zip)")
    bd.add_argument("--windows-zip", type=Path, help="built Windows agent package to include")
    bd.add_argument("--authenticode-thumbprint", default=None,
                    help="SHA-1 thumbprint of the cert the Windows exe is Authenticode-signed with")
    bd.add_argument("--sbom", type=Path, help="CycloneDX SBOM to include")

    vf = sub.add_parser("verify", help="verify a release directory")
    vf.add_argument("path", type=Path)
    vf.add_argument("--public-key", required=True)
    vf.add_argument("--p256-public-key", default=None, help="base64 SPKI; needed for releases with a Windows package")

    pb = sub.add_parser("publish", help="copy a release into the manager's store")
    pb.add_argument("path", type=Path)
    pb.add_argument("--to", required=True)

    args = parser.parse_args(argv)
    try:
        if args.cmd == "keygen":
            pub = keygen(args.out)
            print(f"Release key written to {args.out} (mode 600). Keep it off the manager server.")
            print("Add this line to the manager's .env, then restart the api:")
            print(f"AGENT_RELEASE_PUBLIC_KEY={pub}")
            print(f"(key id {key_id(pub)})")
            if args.p256_out:
                spki = keygen_p256(args.p256_out)
                print(f"\nP-256 key (Windows) written to {args.p256_out} (mode 600).")
                print(f"AGENT_RELEASE_P256_PUBLIC_KEY={spki}")
                print(f"(key id {p256_key_id(spki)})")
        elif args.cmd == "build":
            arches = [a.strip() for a in args.arch.split(",") if a.strip()]
            from_images = {}
            for item in args.from_image:
                arch, _, tag = item.partition("=")
                if not tag:
                    raise ReleaseError("--from-image takes ARCH=TAG")
                from_images[arch] = tag
                if arch in ARCHES and image_arch(tag) not in (arch, ""):
                    raise ReleaseError(f"{tag} is {image_arch(tag)}, not {arch}")
            final = build_release(key_path=args.key, out=args.out, arches=arches,
                                  version=args.version or read_version(), from_images=from_images,
                                  p256_key_path=args.p256_key, windows_zip=args.windows_zip,
                                  authenticode_thumbprint=args.authenticode_thumbprint,
                                  sbom_path=args.sbom)
            print(f"\nRelease ready: {final}")
            print(f"Publish:  python3 scripts/agent_release.py publish {final} --to <user@manager:/path or dir>")
        elif args.cmd == "verify":
            manifest = verify_release_dir(resolve_release_dir(args.path), args.public_key,
                                          p256_public_key_b64=args.p256_public_key)
            arches = ", ".join([i["arch"] for i in manifest["images"]]
                               + [f"{p['os']}/{p['cpu']}" for p in manifest.get("packages", [])])
            print(f"OK: release {manifest['version']} ({arches}) is signed by key {key_id(args.public_key)} and intact")
        elif args.cmd == "publish":
            publish(args.path, args.to)
            print(f"Published {resolve_release_dir(args.path).name} to {args.to}")
    except ReleaseError as exc:
        print(f"agent-release: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

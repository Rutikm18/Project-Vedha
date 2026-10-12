#!/usr/bin/env python3
"""agent_release.py — build, sign, verify and publish the Vedha agent release.

Vedha is centrally hosted, so customers never pull the agent from a public
registry: the manager serves it (manager/backend/app/routers/agent_distribution.py)
from a signed release built here.

    keygen  --out FILE [--p256-out FILE]   new Ed25519 release key (+ P-256 key for Windows)
    pubkey  --key FILE [--p256-key FILE]   print the public key(s) of existing keys as .env lines
    build   --key FILE [--arch amd64,arm64] [--out DIR] [--from-image TAG]
            [--p256-key FILE --windows-zip ZIP [--authenticode-thumbprint HEX]] [--sbom FILE]
    verify  DIR --public-key B64 [--p256-public-key B64]
    publish DIR --to DEST              DEST = local dir or user@host:/path (rsync, or ssh+scp on Windows)
    pull    --repo OWNER/REPO --to DIR  download a published release from its GitHub Release,
            [--tag agent-vX.Y.Z]        re-verify BOTH signatures against your pinned keys, and
            [--env-file .env]           only then install it into the manager's release store
                                        and make it current (run on the manager host)

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
import shlex
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
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


AGENT_VERSION_FILE = REPO / "probe" / "agent" / "version.py"
_AGENT_VERSION_LINE = re.compile(r'^AGENT_VERSION\s*=\s*["\']([0-9][0-9A-Za-z.+-]{0,63})["\']\s*$', re.MULTILINE)


def read_agent_version(path: Path = AGENT_VERSION_FILE) -> str:
    """The agent's own version (probe/agent/version.py), read as text so the release
    tool never imports the agent. This is separate from the platform release
    version above, which only names the release directory."""
    match = _AGENT_VERSION_LINE.search(path.read_text(encoding="utf-8"))
    if not match:
        raise ReleaseError(f"could not find AGENT_VERSION in {path}")
    return match.group(1)


def windows_package_info(zip_path: Path) -> dict | None:
    """What package-zip.ps1 wrote about this build, from `<zip name>.release.json` beside the zip
    (agent version, SHA-256, size). None when the file is absent or unreadable."""
    info_path = zip_path.with_name(zip_path.stem + ".release.json")
    try:
        info = json.loads(info_path.read_text(encoding="utf-8-sig"))
    except (OSError, ValueError):
        return None
    return info if isinstance(info, dict) else None


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


def _run(cmd: list[str], cwd: Path | None = None) -> None:
    print("  $ " + " ".join(cmd), flush=True)
    result = subprocess.run(cmd, check=False, cwd=str(cwd) if cwd else None)
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
    agent_version: str | None = None,
    expires_days: int | None = None,
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
    # The manifest tells every agent what "the latest agent" is, so it must name the agent that is actually in
    # the zip. The zip's own record (written when it was built) is the truth, not whatever checkout this
    # tool happens to run from: a 2.2.3 package released from a 2.2.7 checkout would be labelled 2.2.7.
    if windows_zip is not None:
        info = windows_package_info(windows_zip)
        if info is None:
            print(f"warning: no {windows_zip.stem}.release.json beside {windows_zip.name}, so the manifest records "
                  f"this checkout's agent version ({read_agent_version()}). Make sure the zip was built from "
                  "this checkout.", flush=True)
        else:
            recorded_hash = str(info.get("sha256") or "").lower()
            if recorded_hash and recorded_hash != sha256_file(windows_zip):
                raise ReleaseError(f"{windows_zip.name} does not match its {windows_zip.stem}.release.json "
                                   "(different SHA-256): the zip was changed, or this is another build")
            recorded = str(info.get("version") or "")
            if re.fullmatch(r"[0-9][0-9A-Za-z.+-]{0,63}", recorded):
                if agent_version is not None and agent_version != recorded:
                    raise ReleaseError(f"--agent-version {agent_version} contradicts the package's own record "
                                       f"({recorded}, from {windows_zip.stem}.release.json)")
                agent_version = recorded
                tree = read_agent_version()
                if tree != recorded:
                    print(f"note: this checkout is agent {tree}, the package is agent {recorded}; the manifest "
                          f"records {recorded} (from the package).", flush=True)
    agent_version = agent_version if agent_version is not None else read_agent_version()
    if not re.fullmatch(r"[0-9][0-9A-Za-z.+-]{0,63}", agent_version):
        raise ReleaseError(f"invalid agent version {agent_version!r}")
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

        if expires_days is not None and not 1 <= expires_days <= 3650:
            raise ReleaseError("--expires-days must be between 1 and 3650")
        manifest = {
            "schema": 1,
            "version": version,
            # The agent's own version, so a manager can tell a running agent
            # whether a newer one exists. Signed with the rest of the manifest.
            "agent_version": agent_version,
            "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "installer": {"file": "install.sh", "sha256": sha256_file(installer)},
            "images": images,
            "signing_key_id": key_id(raw_b64),
        }

        if expires_days is not None:
            # Signed with the rest of the manifest. An agent that has pinned the release key refuses
            # to update from a release past this date, so a manager (or a mirror) that keeps serving
            # an old signed release cannot hold agents on it forever: the owner must sign a fresh one.
            manifest["expires"] = (datetime.now(timezone.utc) + timedelta(days=expires_days)).isoformat(timespec="seconds")

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

def verify_manifest_ed25519(public_key_b64: str, signature_b64: bytes | str, manifest_bytes: bytes) -> None:
    _, _, Ed25519PublicKey = _crypto()
    try:
        signature = base64.b64decode(signature_b64.strip(), validate=True)
        raw = base64.b64decode(public_key_b64, validate=True)
        Ed25519PublicKey.from_public_bytes(raw).verify(signature, manifest_bytes)
    except Exception as exc:
        raise ReleaseError("manifest signature does not verify with this public key") from exc


def verify_release_dir(directory: Path, public_key_b64: str, *, expect_version: str | None = None,
                       p256_public_key_b64: str | None = None) -> dict:
    """Signature(s), file names and hashes — the same checks the manager runs.
    A manifest that lists a Windows package must also carry a P-256 signature,
    and the caller must supply the P-256 key to check it against."""
    manifest_bytes = (directory / "manifest.json").read_bytes()
    verify_manifest_ed25519(public_key_b64, (directory / "manifest.json.sig").read_bytes(), manifest_bytes)
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

_WINDOWS_DRIVE = re.compile(r"^[A-Za-z]:[\\/]")


def is_remote_dest(dest: str) -> bool:
    """`user@host:/path` is remote; `C:\\releases` (a Windows drive) and existing local paths are not."""
    return (":" in dest and not dest.startswith("/") and not _WINDOWS_DRIVE.match(dest)
            and not Path(dest).exists())


def _publish_with_scp(release_dir: Path, host: str, remote: str, version: str) -> None:
    """Remote publish for machines without rsync (Windows ships OpenSSH's ssh and scp).

    Same guarantees as the rsync path: the version is copied completely first and CURRENT is
    switched last, atomically, so the manager never points at a half-copied release; and a
    published version is immutable, so an existing one is refused rather than overwritten."""
    qremote = shlex.quote(remote)
    qdir = shlex.quote(f"{remote}/{version}")
    _run(["ssh", host, f"mkdir -p {qremote} && {{ test ! -e {qdir} || "
                       f"{{ echo 'release {version} already exists on the manager - releases are immutable' >&2; exit 1; }}; }}"])
    # Relative name + cwd: a Windows path such as C:\\x would be read by scp as "host C".
    _run(["scp", "-r", release_dir.name, f"{host}:{remote}/"], cwd=release_dir.parent)
    _run(["ssh", host, f"chmod -R u=rwX,go=rX {qdir} && printf '%s\\n' {shlex.quote(version)} > {qremote}/.CURRENT.tmp "
                       f"&& chmod 644 {qremote}/.CURRENT.tmp && mv -f {qremote}/.CURRENT.tmp {qremote}/CURRENT"])


def publish(release_dir: Path, dest: str) -> None:
    """Copy one version into the manager's release store, then flip CURRENT —
    in that order, so the manager never points at a half-copied release."""
    release_dir = resolve_release_dir(release_dir)
    version = release_dir.name
    if is_remote_dest(dest):
        host, _, remote = dest.partition(":")
        remote = remote.rstrip("/") or "."
        if shutil.which("rsync") is None:
            if shutil.which("ssh") and shutil.which("scp"):
                _publish_with_scp(release_dir, host, remote, version)
                return
            raise ReleaseError("publishing to a remote host needs rsync, or ssh and scp "
                               "(Windows 10/11: Settings > Optional features > OpenSSH Client)")
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


# ── pull: GitHub Release -> the manager's release store ─────────────────────

GITHUB_API = "https://api.github.com"
TAG_PREFIX = "agent-v"
# GitHub: owners are alphanumerics and hyphens; repository names also allow _ and . ("." / ".." are not names).
_REPO_RE = re.compile(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})/(?!\.{1,2}$)[A-Za-z0-9_.-]{1,100}")
_ASSET_NAME_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,200}")
_VERSION_RE = re.compile(r"[0-9A-Za-z][0-9A-Za-z._-]{0,63}")
_MAX_MANIFEST_BYTES = 1024 * 1024
_MAX_ASSET_BYTES = 4 * 1024 ** 3
_HTTP_TIMEOUT = 60


class _KeepTokenOnItsHost(urllib.request.HTTPRedirectHandler):
    """GitHub serves release assets from object storage behind a redirect. Follow it, but
    never hand the GitHub token to a different host, and never follow https -> http."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        new = super().redirect_request(req, fp, code, msg, headers, newurl)
        if new is None:
            return None
        before, after = urllib.parse.urlsplit(req.full_url), urllib.parse.urlsplit(newurl)
        if before.scheme == "https" and after.scheme != "https":
            raise ReleaseError(f"refusing a redirect from https to {after.scheme}")
        if before.netloc.lower() != after.netloc.lower():
            new.remove_header("Authorization")
        return new


def _gh_open(url: str, token: str | None, accept: str, opener):
    req = urllib.request.Request(url, headers={
        "Accept": accept, "User-Agent": "vedha-agent-release", "X-GitHub-Api-Version": "2022-11-28"})
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        return opener.open(req, timeout=_HTTP_TIMEOUT)
    except urllib.error.HTTPError as exc:
        hint = {401: "the token was refused", 403: "access denied or rate limited",
                404: "not found - for a private repository set GITHUB_TOKEN to a token that can read it"}.get(exc.code, "")
        raise ReleaseError(f"GitHub answered {exc.code} for {urllib.parse.urlsplit(url).path}: {hint}") from exc
    except urllib.error.URLError as exc:
        raise ReleaseError(f"cannot reach {urllib.parse.urlsplit(url).netloc}: {exc.reason}") from exc


def _gh_json(url: str, token: str | None, opener):
    with _gh_open(url, token, "application/vnd.github+json", opener) as resp:
        return json.loads(resp.read(8 * 1024 * 1024))


def _gh_download(asset: dict, dest: Path, token: str | None, opener, *, limit: int) -> None:
    """Stream one release asset to `dest`, refusing anything larger than GitHub says it is."""
    size = int(asset.get("size") or 0)
    if size <= 0 or size > limit:
        raise ReleaseError(f"asset {asset['name']}: unreasonable size {size}")
    total = 0
    with _gh_open(asset["url"], token, "application/octet-stream", opener) as resp, dest.open("xb") as out:
        for chunk in iter(lambda: resp.read(_CHUNK), b""):
            total += len(chunk)
            if total > size:
                raise ReleaseError(f"asset {asset['name']}: more data than the {size} bytes GitHub lists")
            out.write(chunk)
    if total != size:
        raise ReleaseError(f"asset {asset['name']}: got {total} of {size} bytes")
    dest.chmod(0o644)


def select_release(repo: str, tag: str | None, token: str | None, api_url: str, opener) -> dict:
    """The GitHub release to pull: the named tag, or the newest published agent release."""
    base = f"{api_url}/repos/{repo}/releases"
    if tag:
        if not tag.startswith(TAG_PREFIX):
            raise ReleaseError(f"tag must look like {TAG_PREFIX}<version> (got {tag!r})")
        return _gh_json(f"{base}/tags/{urllib.parse.quote(tag)}", token, opener)
    for release in _gh_json(f"{base}?per_page=50", token, opener):
        if (release.get("tag_name", "").startswith(TAG_PREFIX)
                and not release.get("draft") and not release.get("prerelease")):
            return release
    raise ReleaseError(f"{repo} has no published release tagged {TAG_PREFIX}<version>")


def manifest_file_names(manifest: dict) -> list[str]:
    """Every file a release's manifest vouches for (besides the manifest and its signatures)."""
    entries = [manifest.get("installer")] + list(manifest.get("images") or [])
    for key in ("windows_installer", "windows_launcher", "sbom"):
        entries.append(manifest.get(key))
    entries += list(manifest.get("packages") or [])
    names = [e["file"] for e in entries if e]
    for name in names:
        if not _ASSET_NAME_RE.fullmatch(name):
            raise ReleaseError(f"manifest lists an unsafe file name {name!r}")
    return names


def _version_tuple(version: str):
    try:
        return tuple(int(part) for part in version.split("."))
    except ValueError:
        return None


def pull(*, repo: str, dest: Path, public_key_b64: str, p256_public_key_b64: str | None = None,
         tag: str | None = None, token: str | None = None, api_url: str = GITHUB_API,
         make_current: bool = True, opener=None, log=print) -> Path:
    """Download a release from GitHub, verify it exactly as the manager will, and install it.

    Nothing reaches the release store unless BOTH signatures verify against the keys the caller
    pins (the manager's AGENT_RELEASE_PUBLIC_KEY / AGENT_RELEASE_P256_PUBLIC_KEY), every file
    matches its signed SHA-256 and the version matches the tag. The manifest signature is
    checked before the large files are fetched. Only files the signed manifest lists are
    taken; any other asset on the GitHub release is ignored."""
    if not _REPO_RE.fullmatch(repo):
        raise ReleaseError(f"--repo must be OWNER/REPO (got {repo!r})")
    dest = Path(dest)
    if ":" in str(dest) and not dest.is_absolute() and not dest.exists() and sys.platform != "win32":
        raise ReleaseError("pull installs into a local directory: run it on the manager host")
    api_url = api_url.rstrip("/")
    opener = opener or urllib.request.build_opener(_KeepTokenOnItsHost())

    release = select_release(repo, tag, token, api_url, opener)
    tag_name = release.get("tag_name") or ""
    version = tag_name[len(TAG_PREFIX):] if tag_name.startswith(TAG_PREFIX) else ""
    if not _VERSION_RE.fullmatch(version):
        raise ReleaseError(f"release tag {tag_name!r} is not {TAG_PREFIX}<version>")
    if release.get("draft"):
        raise ReleaseError(f"{tag_name} is a draft release")
    assets = {a["name"]: a for a in release.get("assets", [])
              if _ASSET_NAME_RE.fullmatch(a.get("name", "")) and a.get("state", "uploaded") == "uploaded"}
    for needed in ("manifest.json", "manifest.json.sig"):
        if needed not in assets:
            raise ReleaseError(f"{tag_name} has no {needed} asset: not a signed agent release")
    log(f"Pulling {repo} {tag_name} ...")

    dest.mkdir(parents=True, exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix=f".pull-{version}-", dir=dest))
    try:
        staging = work / version
        staging.mkdir()
        staging.chmod(0o755)
        for name in ("manifest.json", "manifest.json.sig", P256_SIG_FILE):
            if name in assets:
                _gh_download(assets[name], staging / name, token, opener,
                             limit=_MAX_MANIFEST_BYTES)

        manifest_bytes = (staging / "manifest.json").read_bytes()
        verify_manifest_ed25519(public_key_b64, (staging / "manifest.json.sig").read_bytes(), manifest_bytes)
        manifest = json.loads(manifest_bytes)
        if manifest.get("version") != version:
            raise ReleaseError(f"manifest is version {manifest.get('version')!r} but the tag says {version!r}")
        log("  manifest signature OK - fetching the files it lists")

        for name in manifest_file_names(manifest):
            if name not in assets:
                raise ReleaseError(f"{tag_name} is missing {name}, which its signed manifest lists")
            log(f"  {name} ({int(assets[name].get('size') or 0) / 1e6:.1f} MB)")
            _gh_download(assets[name], staging / name, token, opener, limit=_MAX_ASSET_BYTES)

        verify_release_dir(staging, public_key_b64, expect_version=version,
                           p256_public_key_b64=p256_public_key_b64)
        log("  all signatures and checksums verify")

        target = dest / version
        if target.exists():
            if (target / "manifest.json").read_bytes() != manifest_bytes:
                raise ReleaseError(f"{target} already exists with different content - releases are immutable")
            log(f"  {version} is already installed")
        else:
            staging.rename(target)
        previous = (dest / "CURRENT").read_text(encoding="utf-8").strip() if (dest / "CURRENT").is_file() else ""
        if make_current:
            _write_current(dest, version)
            old, new = _version_tuple(previous), _version_tuple(version)
            if previous and old and new and new < old:
                log(f"  WARNING: this ROLLS BACK the served agent from {previous} to {version}")
            log(f"  {version} is now the release the manager serves")
        else:
            log(f"  installed as {target}; CURRENT left at {previous or 'unset'}")
        return target
    finally:
        shutil.rmtree(work, ignore_errors=True)


def read_env_file(path: Path) -> dict[str, str]:
    """KEY=VALUE lines of a manager .env (comments and quotes tolerated)."""
    values: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        values[key.strip()] = value.strip().strip("\"'")
    return values


# ── CLI ──────────────────────────────────────────────────────────────────────

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)

    kg = sub.add_parser("keygen", help="create a new Ed25519 release signing key (and/or the P-256 key for Windows)")
    kg.add_argument("--out", type=Path, help="Ed25519 key file (Linux installs)")
    kg.add_argument("--p256-out", type=Path, help="P-256 key file (Windows installs); may be given alone "
                                                   "to add Windows to an existing Ed25519 key")

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
    bd.add_argument("--expires-days", type=int, default=None,
                    help="sign an expiry date this many days ahead; agents refuse to update from an expired release "
                         "(you must then publish a fresh one before it passes). Default: no expiry")

    pk = sub.add_parser("pubkey", help="print the public key(s) of existing signing keys, as .env lines")
    pk.add_argument("--key", type=Path, help="Ed25519 private key file")
    pk.add_argument("--p256-key", type=Path, help="P-256 private key file")

    vf = sub.add_parser("verify", help="verify a release directory")
    vf.add_argument("path", type=Path)
    vf.add_argument("--public-key", required=True)
    vf.add_argument("--p256-public-key", default=None, help="base64 SPKI; needed for releases with a Windows package")

    pb = sub.add_parser("publish", help="copy a release into the manager's store")
    pb.add_argument("path", type=Path)
    pb.add_argument("--to", required=True)

    pl = sub.add_parser("pull", help="download a release from GitHub, verify it, install it into the store")
    pl.add_argument("--repo", required=True, help="OWNER/REPO that publishes the agent releases")
    pl.add_argument("--to", required=True, type=Path, help="the manager's AGENT_RELEASE_DIR")
    pl.add_argument("--tag", default=None, help=f"{TAG_PREFIX}<version> (default: the newest published agent release)")
    pl.add_argument("--env-file", type=Path, default=None,
                    help="manager .env holding AGENT_RELEASE_PUBLIC_KEY and AGENT_RELEASE_P256_PUBLIC_KEY")
    pl.add_argument("--public-key", default=None, help="Ed25519 release public key (default: AGENT_RELEASE_PUBLIC_KEY)")
    pl.add_argument("--p256-public-key", default=None,
                    help="P-256 release public key (default: AGENT_RELEASE_P256_PUBLIC_KEY)")
    pl.add_argument("--no-current", action="store_true", help="install the release but do not make it the served one")
    pl.add_argument("--api-url", default=GITHUB_API, help="GitHub API base (GitHub Enterprise Server)")
    # The GitHub token comes from GITHUB_TOKEN / GH_TOKEN, never from the command line.

    args = parser.parse_args(argv)
    try:
        if args.cmd == "keygen":
            if not args.out and not args.p256_out:
                raise ReleaseError("keygen needs --out and/or --p256-out")
            if args.out:
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
        elif args.cmd == "pubkey":
            if not args.key and not args.p256_key:
                raise ReleaseError("pubkey needs --key and/or --p256-key")
            if args.key:
                print(f"AGENT_RELEASE_PUBLIC_KEY={public_raw_b64(load_private_key(args.key))}")
            if args.p256_key:
                print(f"AGENT_RELEASE_P256_PUBLIC_KEY={p256_spki_b64(load_p256_private_key(args.p256_key))}")
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
                                  sbom_path=args.sbom, expires_days=args.expires_days)
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
        elif args.cmd == "pull":
            env = dict(os.environ)
            if args.env_file:
                env.update(read_env_file(args.env_file))
            public_key = args.public_key or env.get("AGENT_RELEASE_PUBLIC_KEY")
            if not public_key:
                raise ReleaseError("no release public key: pass --public-key, --env-file, or set AGENT_RELEASE_PUBLIC_KEY")
            pull(repo=args.repo, dest=args.to, public_key_b64=public_key,
                 p256_public_key_b64=args.p256_public_key or env.get("AGENT_RELEASE_P256_PUBLIC_KEY") or None,
                 tag=args.tag, token=os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN"),
                 api_url=args.api_url, make_current=not args.no_current)
    except ReleaseError as exc:
        print(f"agent-release: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

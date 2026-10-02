#!/usr/bin/env python3
"""agent_release.py — build, sign, verify and publish the Vedha agent release.

Vedha is centrally hosted, so customers never pull the agent from a public
registry: the manager serves it (manager/backend/app/routers/agent_distribution.py)
from a signed release built here.

    keygen  --out FILE                 new Ed25519 release key (keep it OFF the server)
    build   --key FILE [--arch amd64,arm64] [--out DIR] [--from-image TAG]
    verify  DIR --public-key B64       what the manager checks, before you ship
    publish DIR --to DEST              DEST = local dir or user@host:/path (rsync)

A release directory looks like:

    <out>/CURRENT                      the version to serve
    <out>/<version>/manifest.json      files, sizes, SHA-256, image tags
    <out>/<version>/manifest.json.sig  base64 Ed25519 signature of manifest.json
    <out>/<version>/install.sh         probe/install.sh with the release key embedded
    <out>/<version>/vedha-agent-<version>-<arch>.tar.gz

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
) -> Path:
    for arch in arches:
        if arch not in ARCHES:
            raise ReleaseError(f"unsupported architecture {arch!r} (supported: {', '.join(ARCHES)})")
    if not re.fullmatch(r"[0-9A-Za-z][0-9A-Za-z._-]{0,63}", version):
        raise ReleaseError(f"invalid version {version!r}")
    private_key = load_private_key(key_path)
    raw_b64 = public_raw_b64(private_key)

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
        manifest_bytes = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode()
        (staging / "manifest.json").write_bytes(manifest_bytes)
        (staging / "manifest.json.sig").write_text(sign_manifest(private_key, manifest_bytes) + "\n")
        verify_release_dir(staging, raw_b64, expect_version=version)
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

def verify_release_dir(directory: Path, public_key_b64: str, *, expect_version: str | None = None) -> dict:
    """Signature, file names and hashes — the same checks the manager runs."""
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

    bd = sub.add_parser("build", help="build + sign a release")
    bd.add_argument("--key", required=True, type=Path)
    bd.add_argument("--out", type=Path, default=REPO / "dist" / "agent-release")
    bd.add_argument("--arch", default=",".join(ARCHES))
    bd.add_argument("--version", default=None)
    bd.add_argument("--from-image", action="append", default=[], metavar="ARCH=TAG",
                    help="package an existing local image instead of building (repeatable)")

    vf = sub.add_parser("verify", help="verify a release directory")
    vf.add_argument("path", type=Path)
    vf.add_argument("--public-key", required=True)

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
                                  version=args.version or read_version(), from_images=from_images)
            print(f"\nRelease ready: {final}")
            print(f"Publish:  python3 scripts/agent_release.py publish {final} --to <user@manager:/path or dir>")
        elif args.cmd == "verify":
            manifest = verify_release_dir(resolve_release_dir(args.path), args.public_key)
            arches = ", ".join(i["arch"] for i in manifest["images"])
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

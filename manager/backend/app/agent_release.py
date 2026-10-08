"""agent_release.py — the signed agent release the manager hands to customer hosts.

Vedha is centrally hosted: customers never pull from a public registry. A release
is built and signed on a build machine (scripts/agent-release.sh), copied into the
manager's release store, and served by app.routers.agent_distribution:

    <AGENT_RELEASE_DIR>/
      CURRENT                         one line: the version being served
      <version>/
        manifest.json                 what is in the release (schema below)
        manifest.json.sig             base64 Ed25519 signature over manifest.json
        install.sh                    the installer, release public key embedded
        vedha-agent-<v>-amd64.tar.gz  `docker save | gzip` per architecture
        vedha-agent-<v>-arm64.tar.gz

Schema 2 adds an optional Windows package, installer + launcher and an SBOM,
and a second signature over the same manifest — ECDSA P-256 — because Windows
PowerShell 5.1 cannot verify Ed25519:

      manifest.json.p256.sig         base64 of the 64-byte r||s ECDSA signature
      install.ps1 / install.cmd      the Windows installer and its launcher
      vedha-agent-<v>-windows-amd64.zip
      sbom.cdx.json
    packages: [{"os": "windows", "cpu": "amd64", "file", "sha256", "size",
                "authenticode_thumbprint"?}]   (NB "cpu": install.sh keys on "arch")

manifest.json (schema 1):
    {"schema": 1, "version": "1.0.335", "created_at": "...",
     "installer": {"file": "install.sh", "sha256": "<hex>"},
     "images": [{"arch": "amd64", "file": "...tar.gz", "sha256": "<hex>",
                 "size": 123, "tag": "vedha-agent:1.0.335"}],
     "signing_key_id": "<first 16 hex of sha256(public key)>"}

Nothing is served unless it checks out: the signature verifies against the
manager's configured AGENT_RELEASE_PUBLIC_KEY, every file name is a plain name
inside the version directory, and every file's SHA-256 matches the manifest. A
swapped or truncated file on disk is caught here, not on the customer's host. The
result is cached until any of the files changes (stat-based), so the hashing cost
is paid once per release per worker.
"""
from __future__ import annotations

import base64
import hashlib
import json
import re
import threading
from dataclasses import dataclass, field
from pathlib import Path

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from cryptography.hazmat.primitives.asymmetric.utils import encode_dss_signature

ARCHES = ("amd64", "arm64")
CURRENT_FILE = "CURRENT"
MANIFEST_FILE = "manifest.json"
SIGNATURE_FILE = "manifest.json.sig"
SCHEMA_VERSION = 1                 # what a Linux-only release is written as
SUPPORTED_SCHEMAS = (1, 2)
P256_SIGNATURE_FILE = "manifest.json.p256.sig"
# (os, cpu) targets the manager will hand out. Anything else in a manifest is
# refused rather than served: the download route names the target in its URL.
PACKAGE_TARGETS = (("windows", "amd64"),)

_VERSION_RE = re.compile(r"[0-9A-Za-z][0-9A-Za-z._-]{0,63}")
_FILE_RE = re.compile(r"[0-9A-Za-z][0-9A-Za-z._-]{0,127}")
_SHA256_RE = re.compile(r"[0-9a-f]{64}")
_TAG_RE = re.compile(r"[a-z0-9][a-z0-9._/-]{0,127}:[0-9A-Za-z][0-9A-Za-z._-]{0,127}")
_THUMBPRINT_RE = re.compile(r"[0-9A-F]{40}")
_HASH_CHUNK = 1024 * 1024


class ReleaseUnavailable(Exception):
    """No servable release. `reason` is safe to show an operator."""

    def __init__(self, reason: str):
        super().__init__(reason)
        self.reason = reason


@dataclass(frozen=True)
class ReleaseFile:
    name: str
    path: Path
    sha256: str
    size: int


@dataclass(frozen=True)
class ReleaseImage(ReleaseFile):
    arch: str = ""
    tag: str = ""


@dataclass(frozen=True)
class ReleasePackage(ReleaseFile):
    os: str = ""
    cpu: str = ""
    authenticode_thumbprint: str = ""


@dataclass(frozen=True)
class AgentRelease:
    version: str
    directory: Path
    created_at: str
    installer: ReleaseFile
    images: dict[str, ReleaseImage] = field(default_factory=dict)
    signed: bool = False
    signing_key_id: str = ""
    # Schema 2 (Windows). `packages` is keyed by os ("windows"). When the
    # release has a Windows package but this manager cannot vouch for it,
    # `packages` is empty and `windows_unavailable` says why — Linux is unaffected.
    packages: dict[str, ReleasePackage] = field(default_factory=dict)
    windows_installer: ReleaseFile | None = None
    windows_launcher: ReleaseFile | None = None
    sbom: ReleaseFile | None = None
    p256_signed: bool = False
    p256_key_id: str = ""
    windows_unavailable: str = ""

    @property
    def windows_available(self) -> bool:
        return "windows" in self.packages and self.windows_installer is not None \
            and self.windows_launcher is not None

    @property
    def arches(self) -> list[str]:
        return [arch for arch in ARCHES if arch in self.images]


def decode_public_key(value: str) -> Ed25519PublicKey:
    """AGENT_RELEASE_PUBLIC_KEY: base64 of the raw 32-byte Ed25519 public key."""
    try:
        raw = base64.b64decode(value.strip(), validate=True)
    except Exception as exc:
        raise ValueError("AGENT_RELEASE_PUBLIC_KEY must be base64") from exc
    if len(raw) != 32:
        raise ValueError("AGENT_RELEASE_PUBLIC_KEY must encode exactly 32 bytes")
    return Ed25519PublicKey.from_public_bytes(raw)


def key_id(public_key_b64: str) -> str:
    raw = base64.b64decode(public_key_b64.strip(), validate=True)
    return hashlib.sha256(raw).hexdigest()[:16]


def decode_p256_public_key(value: str) -> ec.EllipticCurvePublicKey:
    """AGENT_RELEASE_P256_PUBLIC_KEY: base64 DER SubjectPublicKeyInfo of a P-256 key."""
    try:
        key = serialization.load_der_public_key(base64.b64decode(value.strip(), validate=True))
    except Exception as exc:
        raise ValueError("AGENT_RELEASE_P256_PUBLIC_KEY must be a base64 DER P-256 public key") from exc
    if not isinstance(key, ec.EllipticCurvePublicKey) or not isinstance(key.curve, ec.SECP256R1):
        raise ValueError("AGENT_RELEASE_P256_PUBLIC_KEY must be a P-256 (secp256r1) key")
    return key


def p256_key_id(public_key_b64: str) -> str:
    return hashlib.sha256(base64.b64decode(public_key_b64.strip(), validate=True)).hexdigest()[:16]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(_HASH_CHUNK), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _plain_file(directory: Path, name: object, label: str) -> Path:
    """A manifest file name must be a bare name that resolves inside the release
    directory — never a path, never a symlink out of it."""
    if not isinstance(name, str) or not _FILE_RE.fullmatch(name) or ".." in name:
        raise ReleaseUnavailable(f"manifest {label} has an invalid file name")
    path = directory / name
    try:
        resolved = path.resolve(strict=True)
    except FileNotFoundError as exc:
        raise ReleaseUnavailable(f"{label} file {name} is missing from the release") from exc
    if resolved.parent != directory.resolve() or not resolved.is_file():
        raise ReleaseUnavailable(f"{label} file {name} is not a regular file in the release")
    return resolved


def _checked_file(directory: Path, entry: object, label: str) -> ReleaseFile:
    if not isinstance(entry, dict):
        raise ReleaseUnavailable(f"manifest {label} entry is malformed")
    path = _plain_file(directory, entry.get("file"), label)
    expected = entry.get("sha256")
    if not isinstance(expected, str) or not _SHA256_RE.fullmatch(expected):
        raise ReleaseUnavailable(f"manifest {label} sha256 is malformed")
    actual = sha256_file(path)
    if actual != expected:
        raise ReleaseUnavailable(f"{label} file {path.name} does not match its manifest checksum")
    return ReleaseFile(name=path.name, path=path, sha256=actual, size=path.stat().st_size)


def verify_manifest_signature(manifest: bytes, signature_b64: bytes, public_key_b64: str) -> None:
    try:
        public_key = decode_public_key(public_key_b64)
        signature = base64.b64decode(signature_b64.strip(), validate=True)
        public_key.verify(signature, manifest)
    except (InvalidSignature, ValueError, TypeError) as exc:
        raise ReleaseUnavailable("release signature does not verify against AGENT_RELEASE_PUBLIC_KEY") from exc


def verify_manifest_p256(manifest: bytes, signature_b64: bytes, public_key_b64: str) -> None:
    """ECDSA-SHA256 over the manifest; signature is base64 of the 64-byte r||s."""
    try:
        public_key = decode_p256_public_key(public_key_b64)
        raw = base64.b64decode(signature_b64.strip(), validate=True)
        if len(raw) != 64:
            raise ValueError("P-256 signature must be 64 bytes")
        der = encode_dss_signature(int.from_bytes(raw[:32], "big"), int.from_bytes(raw[32:], "big"))
        public_key.verify(der, manifest, ec.ECDSA(hashes.SHA256()))
    except (InvalidSignature, ValueError, TypeError) as exc:
        raise ReleaseUnavailable(
            "release P-256 signature does not verify against AGENT_RELEASE_P256_PUBLIC_KEY") from exc


def load_release(root: Path, public_key_b64: str = "", *, require_signature: bool = True,
                 p256_public_key_b64: str = "") -> AgentRelease:
    """Read, verify and return the release named by <root>/CURRENT."""
    root = Path(root)
    try:
        version = (root / CURRENT_FILE).read_text(encoding="utf-8").strip()
    except FileNotFoundError as exc:
        raise ReleaseUnavailable("no agent release has been published to this manager") from exc
    except OSError as exc:
        raise ReleaseUnavailable("the agent release store is not readable") from exc
    if not _VERSION_RE.fullmatch(version) or ".." in version:
        raise ReleaseUnavailable("CURRENT does not name a valid release version")

    directory = root / version
    if not directory.is_dir() or directory.resolve().parent != root.resolve():
        raise ReleaseUnavailable(f"release directory {version} is missing")

    try:
        manifest_bytes = (directory / MANIFEST_FILE).read_bytes()
    except FileNotFoundError as exc:
        raise ReleaseUnavailable(f"release {version} has no manifest") from exc

    signed = False
    if public_key_b64.strip():
        try:
            signature = (directory / SIGNATURE_FILE).read_bytes()
        except FileNotFoundError as exc:
            raise ReleaseUnavailable(f"release {version} is not signed") from exc
        verify_manifest_signature(manifest_bytes, signature, public_key_b64)
        signed = True
    elif require_signature:
        raise ReleaseUnavailable(
            "AGENT_RELEASE_PUBLIC_KEY is not configured, so the release cannot be verified"
        )

    try:
        manifest = json.loads(manifest_bytes)
    except ValueError as exc:
        raise ReleaseUnavailable(f"release {version} manifest is not valid JSON") from exc
    if not isinstance(manifest, dict) or manifest.get("schema") not in SUPPORTED_SCHEMAS:
        raise ReleaseUnavailable(f"release {version} manifest has an unsupported schema")
    if manifest.get("version") != version:
        raise ReleaseUnavailable(f"manifest version does not match CURRENT ({version})")

    installer = _checked_file(directory, manifest.get("installer"), "installer")

    images: dict[str, ReleaseImage] = {}
    entries = manifest.get("images")
    raw_packages = manifest.get("packages")
    if not isinstance(entries, list) or (not entries and not raw_packages):
        raise ReleaseUnavailable(f"release {version} lists no agent images")
    for entry in entries:
        arch = entry.get("arch") if isinstance(entry, dict) else None
        if arch not in ARCHES:
            raise ReleaseUnavailable(f"release {version} lists an unsupported architecture")
        if arch in images:
            raise ReleaseUnavailable(f"release {version} lists {arch} twice")
        tag = entry.get("tag")
        if not isinstance(tag, str) or not _TAG_RE.fullmatch(tag):
            raise ReleaseUnavailable(f"release {version} {arch} image tag is malformed")
        checked = _checked_file(directory, entry, f"{arch} image")
        images[arch] = ReleaseImage(
            name=checked.name, path=checked.path, sha256=checked.sha256,
            size=checked.size, arch=arch, tag=tag,
        )

    sbom = _checked_file(directory, manifest["sbom"], "sbom") if manifest.get("sbom") else None
    windows = _load_windows(directory, manifest, version, raw_packages, manifest_bytes,
                            p256_public_key_b64, require_signature)

    return AgentRelease(
        version=version,
        directory=directory.resolve(),
        created_at=str(manifest.get("created_at") or ""),
        installer=installer,
        images=images,
        signed=signed,
        signing_key_id=key_id(public_key_b64) if signed else "",
        sbom=sbom,
        **windows,
    )


def _load_windows(directory: Path, manifest: dict, version: str, raw_packages: object,
                  manifest_bytes: bytes, p256_public_key_b64: str,
                  require_signature: bool) -> dict:
    """The Windows half of a schema-2 release.

    Fail-closed on tampering, soft on configuration: a P-256 signature that is
    present but does not verify (or is missing while a key is configured) rejects
    the WHOLE release — the Ed25519 signature passing means the build was
    authentic, so a bad second signature is a sign of tampering or a broken
    build. A manager that simply has no P-256 key configured withholds Windows
    only; Linux keeps working."""
    if not raw_packages:
        return {}
    if not isinstance(raw_packages, list):
        raise ReleaseUnavailable(f"release {version} packages entry is malformed")

    soft_off = {"windows_unavailable": ""}
    p256_signed = False
    if p256_public_key_b64.strip():
        try:
            signature = (directory / P256_SIGNATURE_FILE).read_bytes()
        except FileNotFoundError as exc:
            raise ReleaseUnavailable(f"release {version} has a Windows package but no P-256 signature") from exc
        verify_manifest_p256(manifest_bytes, signature, p256_public_key_b64)
        p256_signed = True
    elif require_signature:
        return {"windows_unavailable":
                "AGENT_RELEASE_P256_PUBLIC_KEY is not configured, so the Windows package cannot be verified"}

    packages: dict[str, ReleasePackage] = {}
    for entry in raw_packages:
        if not isinstance(entry, dict):
            raise ReleaseUnavailable(f"release {version} packages entry is malformed")
        target = (entry.get("os"), entry.get("cpu"))
        if target not in PACKAGE_TARGETS:
            raise ReleaseUnavailable(f"release {version} lists an unsupported package target")
        if target[0] in packages:
            raise ReleaseUnavailable(f"release {version} lists {target[0]} twice")
        thumb = entry.get("authenticode_thumbprint", "")
        if thumb and not (isinstance(thumb, str) and _THUMBPRINT_RE.fullmatch(thumb)):
            raise ReleaseUnavailable(f"release {version} Authenticode thumbprint is malformed")
        checked = _checked_file(directory, entry, f"{target[0]} package")
        packages[target[0]] = ReleasePackage(
            name=checked.name, path=checked.path, sha256=checked.sha256, size=checked.size,
            os=target[0], cpu=target[1], authenticode_thumbprint=thumb or "")

    installer = _checked_file(directory, manifest.get("windows_installer"), "windows installer")
    launcher = _checked_file(directory, manifest.get("windows_launcher"), "windows launcher")
    return {**soft_off, "packages": packages, "windows_installer": installer,
            "windows_launcher": launcher, "p256_signed": p256_signed,
            "p256_key_id": p256_key_id(p256_public_key_b64) if p256_signed else ""}


# ── stat-keyed cache ─────────────────────────────────────────────────────────

_cache_lock = threading.Lock()
_cache: dict[tuple, AgentRelease | ReleaseUnavailable] = {}


def _stamp(root: Path, public_key_b64: str, require_signature: bool, p256_public_key_b64: str = "") -> tuple:
    """Cheap fingerprint of everything load_release reads. Any edit, swap or
    republish changes an mtime/size, which invalidates the cached verdict."""
    parts: list = [str(root), public_key_b64.strip(), require_signature, p256_public_key_b64.strip()]
    current = root / CURRENT_FILE
    try:
        stat = current.stat()
        parts.append((stat.st_mtime_ns, stat.st_size))
        version = current.read_text(encoding="utf-8").strip()
    except OSError:
        return tuple(parts + ["no-current"])
    directory = root / version if _VERSION_RE.fullmatch(version) and ".." not in version else None
    if directory is not None and directory.is_dir():
        for child in sorted(directory.iterdir()):
            try:
                stat = child.stat()
            except OSError:
                continue
            parts.append((child.name, stat.st_mtime_ns, stat.st_size))
    return tuple(parts)


def current_release(root: Path | str, public_key_b64: str = "", *, require_signature: bool = True,
                    p256_public_key_b64: str = "") -> AgentRelease:
    """load_release, cached until the release store changes. Raises
    ReleaseUnavailable (also cached) when nothing servable is published."""
    root = Path(root)
    stamp = _stamp(root, public_key_b64, require_signature, p256_public_key_b64)
    with _cache_lock:
        hit = _cache.get(stamp)
    if hit is None:
        try:
            hit = load_release(root, public_key_b64, require_signature=require_signature,
                               p256_public_key_b64=p256_public_key_b64)
        except ReleaseUnavailable as exc:
            hit = exc
        with _cache_lock:
            _cache.clear()
            _cache[stamp] = hit
    if isinstance(hit, ReleaseUnavailable):
        raise hit
    return hit


def clear_cache() -> None:
    with _cache_lock:
        _cache.clear()

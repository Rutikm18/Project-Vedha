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
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

ARCHES = ("amd64", "arm64")
CURRENT_FILE = "CURRENT"
MANIFEST_FILE = "manifest.json"
SIGNATURE_FILE = "manifest.json.sig"
SCHEMA_VERSION = 1

_VERSION_RE = re.compile(r"[0-9A-Za-z][0-9A-Za-z._-]{0,63}")
_FILE_RE = re.compile(r"[0-9A-Za-z][0-9A-Za-z._-]{0,127}")
_SHA256_RE = re.compile(r"[0-9a-f]{64}")
_TAG_RE = re.compile(r"[a-z0-9][a-z0-9._/-]{0,127}:[0-9A-Za-z][0-9A-Za-z._-]{0,127}")
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
class AgentRelease:
    version: str
    directory: Path
    created_at: str
    installer: ReleaseFile
    images: dict[str, ReleaseImage] = field(default_factory=dict)
    signed: bool = False
    signing_key_id: str = ""
    # The agent's OWN version (probe/agent/version.py), distinct from `version`,
    # which names the platform release. "" for a release built before the field
    # existed: such a release offers no update.
    agent_version: str = ""

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


def load_release(root: Path, public_key_b64: str = "", *, require_signature: bool = True) -> AgentRelease:
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
    if not isinstance(manifest, dict) or manifest.get("schema") != SCHEMA_VERSION:
        raise ReleaseUnavailable(f"release {version} manifest has an unsupported schema")
    if manifest.get("version") != version:
        raise ReleaseUnavailable(f"manifest version does not match CURRENT ({version})")

    installer = _checked_file(directory, manifest.get("installer"), "installer")

    images: dict[str, ReleaseImage] = {}
    entries = manifest.get("images")
    if not isinstance(entries, list) or not entries:
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

    agent_version = manifest.get("agent_version", "")
    if agent_version != "" and (
        not isinstance(agent_version, str) or parse_agent_version(agent_version) is None
    ):
        raise ReleaseUnavailable(f"release {version} manifest has an invalid agent_version")

    return AgentRelease(
        version=version,
        directory=directory.resolve(),
        created_at=str(manifest.get("created_at") or ""),
        installer=installer,
        images=images,
        signed=signed,
        signing_key_id=key_id(public_key_b64) if signed else "",
        agent_version=agent_version,
    )


# ── agent version comparison ─────────────────────────────────────────────────

_AGENT_VERSION_RE = re.compile(r"\d+(\.\d+){0,3}")


def parse_agent_version(text: object) -> tuple[int, ...] | None:
    """'2.1.0' -> (2, 1, 0). Tolerates a leading 'v' and a '-rc1'/'+build' suffix
    (ignored). Anything else is None, never a guess. Mirrors the agent's own
    parser (probe/agent/update_check.py) so both sides agree on what is newer."""
    if not isinstance(text, str):
        return None
    core = re.split(r"[-+]", text.strip().lstrip("vV"), maxsplit=1)[0]
    if not _AGENT_VERSION_RE.fullmatch(core):
        return None
    return tuple(int(part) for part in core.split("."))


def agent_version_is_newer(latest: object, current: object) -> bool:
    """True only when both parse and `latest` is strictly greater."""
    a, b = parse_agent_version(latest), parse_agent_version(current)
    if a is None or b is None:
        return False
    width = max(len(a), len(b))
    return a + (0,) * (width - len(a)) > b + (0,) * (width - len(b))


# ── stat-keyed cache ─────────────────────────────────────────────────────────

_cache_lock = threading.Lock()
_cache: dict[tuple, AgentRelease | ReleaseUnavailable] = {}


def _stamp(root: Path, public_key_b64: str, require_signature: bool) -> tuple:
    """Cheap fingerprint of everything load_release reads. Any edit, swap or
    republish changes an mtime/size, which invalidates the cached verdict."""
    parts: list = [str(root), public_key_b64.strip(), require_signature]
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


def current_release(root: Path | str, public_key_b64: str = "", *, require_signature: bool = True) -> AgentRelease:
    """load_release, cached until the release store changes. Raises
    ReleaseUnavailable (also cached) when nothing servable is published."""
    root = Path(root)
    stamp = _stamp(root, public_key_b64, require_signature)
    with _cache_lock:
        hit = _cache.get(stamp)
    if hit is None:
        try:
            hit = load_release(root, public_key_b64, require_signature=require_signature)
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


_AGENT_VERSION_TEXT_RE = re.compile(r"[0-9A-Za-z][0-9A-Za-z._+-]{0,63}")


def clean_agent_version(text: object) -> str | None:
    """A version string an agent reported, or None if it is not a plain, short
    version-like token. Stored as given; never interpreted as anything else."""
    if not isinstance(text, str):
        return None
    text = text.strip()
    return text if _AGENT_VERSION_TEXT_RE.fullmatch(text) else None


def update_offer(release: "AgentRelease | None", current: object) -> dict:
    """What to tell an agent that asks "is there a newer agent than mine?".

    Always a normal answer, never an error: an agent must be able to ask whenever
    it likes. A manager with no release, or a release that predates the
    agent_version field, simply offers nothing.
    """
    current_text = current if isinstance(current, str) else ""
    offer = {
        "update_available": False,
        "current": current_text,
        "latest": None,
        "manager_release": release.version if release else None,
        "message": "",
    }
    if release is None:
        offer["message"] = "No agent release is published on this manager."
    elif not release.agent_version:
        offer["message"] = "This manager's release does not state an agent version."
    elif agent_version_is_newer(release.agent_version, current_text):
        offer.update(
            update_available=True,
            latest=release.agent_version,
            message=f"Agent {release.agent_version} is available on this manager.",
        )
    else:
        offer["latest"] = release.agent_version
    return offer

"""release_trust.py — decide whether a downloaded installer may be run, using a key pinned on this machine.

Why this exists. The automatic update downloads the installer script from the manager and runs it as
SYSTEM. TLS to the manager protects that download, but a manager that has been broken into (or a
mistaken proxy) could serve a different script and every agent that updates would run it. The
release manifest is signed with a key the manager does not hold, and it lists the SHA-256 of the
installer, so the agent can check the script against it — provided the key it checks with did NOT
come from the same manager at the same moment. That key is therefore PINNED: the one-command
installer stores it in ProgramData\\vedha-agent\\release\\trust.json (administrators only) the first
time it installs, and this module only ever trusts that stored key.

verify_update() answers one question: "is this installer the one the key holder signed for a newer
release, and is the release still valid?". Every refusal has a short reason code so Fleet, the log
and the tests can say exactly why.

Checks, in order:
  bad-signature    the manifest is not signed by the pinned key (P-256, ECDSA-SHA256)
  malformed        the manifest is not the shape a release has (no installer entry, unreadable dates)
  installer-mismatch  the script's SHA-256 is not the one the signed manifest lists
  key-mismatch     the script does not carry the pinned key (a release signed for another key)
  older-release    the manifest's release is older than the newest this machine has installed
  expired          the manifest has an `expires` date and it has passed
  not-newer        the signed manifest does not offer an agent newer than this one

Not covered (be honest): this protects against a changed installer and against replaying an old or
expired release. It does not protect against the key holder signing something bad, and it cannot
help a machine that was installed from a hostile manager in the first place (the first install is
trusted on first use).
"""
from __future__ import annotations

import base64
import hashlib
import json
import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

LOG = logging.getLogger("agent.release_trust")

MAX_MANIFEST_BYTES = 1024 * 1024
MAX_SIGNATURE_BYTES = 4096


@dataclass(frozen=True)
class Pin:
    spki: str
    release_version: str = ""


@dataclass(frozen=True)
class Verdict:
    ok: bool
    reason: str          # "ok" or one of the codes above
    message: str
    manifest: dict[str, Any] | None = None


def trust_path(base: Path) -> Path:
    return base / "release" / "trust.json"


def load_pin(base: Path) -> Pin | None:
    """The pinned key, or None when there is none (or it cannot be read; never guessed)."""
    try:
        data = json.loads(trust_path(base).read_text(encoding="utf-8-sig"))
        spki = data.get("p256_spki")
        if not isinstance(spki, str) or not spki:
            return None
        version = data.get("release_version")
        return Pin(spki=spki, release_version=version if isinstance(version, str) else "")
    except (OSError, ValueError, AttributeError):
        return None


def _signature_ok(spki_b64: str, signature_text: str, manifest: bytes) -> bool:
    try:
        from cryptography.hazmat.primitives import hashes, serialization
        from cryptography.hazmat.primitives.asymmetric import ec
        from cryptography.hazmat.primitives.asymmetric.utils import encode_dss_signature

        raw = base64.b64decode(signature_text.strip(), validate=True)
        if len(raw) != 64:
            return False
        public = serialization.load_der_public_key(base64.b64decode(spki_b64, validate=True))
        if not isinstance(public, ec.EllipticCurvePublicKey) or not isinstance(public.curve, ec.SECP256R1):
            return False
        public.verify(encode_dss_signature(int.from_bytes(raw[:32], "big"), int.from_bytes(raw[32:], "big")),
                      manifest, ec.ECDSA(hashes.SHA256()))
        return True
    except Exception:  # noqa: BLE001 — any failure to verify is "not verified"
        return False


def _parse_time(text: Any) -> datetime | None:
    if not isinstance(text, str):
        return None
    try:
        value = datetime.fromisoformat(text.strip().replace("Z", "+00:00"))
    except ValueError:
        return None
    return value if value.tzinfo else value.replace(tzinfo=timezone.utc)


def _refuse(reason: str, message: str) -> Verdict:
    return Verdict(False, reason, message)


def verify_update(pin: Pin, manifest_bytes: bytes, signature_text: str, installer: bytes,
                  *, current_agent_version: str, now: datetime | None = None) -> Verdict:
    from agent import update_check

    now = now or datetime.now(timezone.utc)
    if len(manifest_bytes) > MAX_MANIFEST_BYTES or len(signature_text) > MAX_SIGNATURE_BYTES:
        return _refuse("malformed", "The release manifest or its signature is larger than expected.")
    if not _signature_ok(pin.spki, signature_text, manifest_bytes):
        return _refuse("bad-signature", "The release manifest is not signed by the release key pinned on this computer.")
    try:
        manifest = json.loads(manifest_bytes.decode("utf-8"))
        entry = manifest["windows_installer"]
        listed = str(entry["sha256"]).lower()
        version = str(manifest["version"])
    except (ValueError, KeyError, TypeError):
        return _refuse("malformed", "The signed manifest does not list a Windows installer.")
    if hashlib.sha256(installer).hexdigest() != listed:
        return _refuse("installer-mismatch", "The installer the manager served is not the one the signed release lists.")
    if f"$script:VedhaReleaseP256Spki = '{pin.spki}'".encode("ascii") not in installer:
        return _refuse("key-mismatch", "The installer does not carry the release key pinned on this computer.")

    release = update_check.parse_version(version)
    if release is None:
        return _refuse("malformed", "The signed manifest has a release version that cannot be read.")
    newest = update_check.parse_version(pin.release_version) if pin.release_version else None
    if newest is not None:
        width = max(len(release), len(newest))
        if release + (0,) * (width - len(release)) < newest + (0,) * (width - len(newest)):
            return _refuse("older-release", f"Release {version} is older than {pin.release_version}, which is already installed here.")

    if "expires" in manifest:
        expires = _parse_time(manifest.get("expires"))
        if expires is None:
            return _refuse("malformed", "The signed manifest has an expiry date that cannot be read.")
        if now >= expires:
            return _refuse("expired", f"The signed release expired on {expires.isoformat()}; ask your Vedha administrator to publish a fresh one.")

    if not update_check.is_newer(manifest.get("agent_version"), current_agent_version):
        return _refuse("not-newer", "The signed release does not offer an agent newer than this one.")
    return Verdict(True, "ok", f"Release {version} verified against the pinned key.", manifest)

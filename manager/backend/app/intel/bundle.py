"""
bundle.py — signed offline intel bundles for sovereign (air-gapped) managers.

A sovereign manager never reaches the internet, so KEV / EPSS / OSV / NVD-CPE
snapshots arrive on removable media through the bank's one-way transfer
process. The bundle must prove WHO produced it and that nothing changed since:

  bundle.vib (zip)
    manifest.json   {"format", "version", "created_at", "files": [{name, sha256, size}]}
    manifest.sig    base64 Ed25519 signature over manifest.json's exact bytes
    files/<name>    the snapshot files

Import verifies, in order: a trusted key signed the manifest → the member set
is exactly the manifest's files (no extras, no traversal) → each file's size and
SHA-256 match → the bundle is not older than the installed one (rollback
protection). Only then is each file atomically replaced in VEDHA_INTEL_DIR,
which the detection engine prefers over its packaged snapshots.

CLI (run on the connected build host / inside the air-gapped manager):
  python -m app.intel.bundle keygen  --out signing.key          # prints the public key
  python -m app.intel.bundle export  --key signing.key --snapshots DIR --version V --out x.vib
  python -m app.intel.bundle import  x.vib --dir $VEDHA_INTEL_DIR  (keys from INTEL_BUNDLE_PUBLIC_KEYS)
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import io
import json
import os
import sys
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey

FORMAT = "vedha-intel-bundle/1"
SNAPSHOT_NAMES = frozenset({
    "osv_debian_snapshot.json", "nvd_cpe_snapshot.json", "kev_snapshot.json", "epss_snapshot.json",
})
MAX_FILE_BYTES = 256 * 1024 * 1024
MAX_TOTAL_BYTES = 512 * 1024 * 1024
INSTALLED_MANIFEST = "bundle_manifest.json"


class BundleError(ValueError):
    """The bundle is not trustworthy or cannot be installed."""


def public_key_b64(key: Ed25519PublicKey) -> str:
    raw = key.public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    return base64.b64encode(raw).decode()


def _load_public(b64: str) -> Ed25519PublicKey:
    try:
        return Ed25519PublicKey.from_public_bytes(base64.b64decode(b64.strip()))
    except Exception as exc:  # noqa: BLE001
        raise BundleError(f"invalid trusted public key: {exc}") from exc


def build_bundle(files: dict[str, bytes], key: Ed25519PrivateKey, *, version: str) -> bytes:
    for name in files:
        if name not in SNAPSHOT_NAMES:
            raise BundleError(f"{name!r} is not an intel snapshot ({sorted(SNAPSHOT_NAMES)})")
    manifest = {
        "format": FORMAT, "version": version,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "files": [{"name": n, "sha256": hashlib.sha256(b).hexdigest(), "size": len(b)}
                  for n, b in sorted(files.items())],
    }
    manifest_bytes = json.dumps(manifest, sort_keys=True, indent=2).encode()
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("manifest.json", manifest_bytes)
        z.writestr("manifest.sig", base64.b64encode(key.sign(manifest_bytes)))
        for name, body in sorted(files.items()):
            z.writestr(f"files/{name}", body)
    return out.getvalue()


def verify_bundle(data: bytes, trusted_keys: Iterable[str]) -> tuple[dict, dict[str, bytes]]:
    keys = [_load_public(k) for k in trusted_keys if k and k.strip()]
    if not keys:
        raise BundleError("no trusted intel-bundle public keys are configured (INTEL_BUNDLE_PUBLIC_KEYS)")
    try:
        z = zipfile.ZipFile(io.BytesIO(data))
    except zipfile.BadZipFile as exc:
        raise BundleError("not a valid bundle archive") from exc
    with z:
        infos = {i.filename: i for i in z.infolist()}
        if "manifest.json" not in infos or "manifest.sig" not in infos:
            raise BundleError("bundle is missing manifest.json or manifest.sig")
        manifest_bytes = z.read("manifest.json")
        signature = base64.b64decode(z.read("manifest.sig"))
        if not any(_verifies(k, signature, manifest_bytes) for k in keys):
            raise BundleError("manifest signature does not match any trusted key")
        manifest = json.loads(manifest_bytes)
        if manifest.get("format") != FORMAT:
            raise BundleError(f"unsupported bundle format {manifest.get('format')!r}")
        declared = {f["name"]: f for f in manifest.get("files", [])}
        expected = {"manifest.json", "manifest.sig", *(f"files/{n}" for n in declared)}
        if set(infos) != expected or any(n not in SNAPSHOT_NAMES for n in declared):
            raise BundleError(f"unexpected bundle members: {sorted(set(infos) ^ expected)}")
        total = 0
        files: dict[str, bytes] = {}
        for name, meta in declared.items():
            info = infos[f"files/{name}"]
            if info.file_size != meta["size"] or info.file_size > MAX_FILE_BYTES:
                raise BundleError(f"{name}: size does not match the manifest")
            total += info.file_size
            if total > MAX_TOTAL_BYTES:
                raise BundleError("bundle exceeds the maximum total size")
            body = z.read(info)
            if hashlib.sha256(body).hexdigest() != meta["sha256"]:
                raise BundleError(f"{name}: hash does not match the signed manifest")
            files[name] = body
    return manifest, files


def _verifies(key: Ed25519PublicKey, signature: bytes, payload: bytes) -> bool:
    try:
        key.verify(signature, payload)
        return True
    except InvalidSignature:
        return False


def installed_manifest(target_dir: str | Path) -> dict | None:
    path = Path(target_dir) / INSTALLED_MANIFEST
    return json.loads(path.read_text()) if path.is_file() else None


def install_bundle(manifest: dict, files: dict[str, bytes], target_dir: str | Path, *,
                   allow_downgrade: bool = False) -> dict:
    target = Path(target_dir)
    target.mkdir(parents=True, exist_ok=True)
    current = installed_manifest(target)
    if current and not allow_downgrade and manifest["created_at"] < current.get("created_at", ""):
        raise BundleError(f"bundle {manifest['version']} is older than the installed "
                          f"{current.get('version')} (rollback refused)")
    for name, body in files.items():
        _atomic_write(target / name, body)
    record = {**manifest, "installed_at": datetime.now(timezone.utc).isoformat()}
    _atomic_write(target / INSTALLED_MANIFEST, json.dumps(record, indent=2).encode())
    return record


def _atomic_write(path: Path, body: bytes) -> None:
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.")
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(body)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp, path)
    except BaseException:
        Path(tmp).unlink(missing_ok=True)
        raise


# ── CLI ──────────────────────────────────────────────────────────────────────

def _cli(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m app.intel.bundle")
    sub = ap.add_subparsers(dest="cmd", required=True)
    kg = sub.add_parser("keygen"); kg.add_argument("--out", required=True)
    ex = sub.add_parser("export")
    ex.add_argument("--key", required=True); ex.add_argument("--snapshots", required=True)
    ex.add_argument("--version", required=True); ex.add_argument("--out", required=True)
    im = sub.add_parser("import")
    im.add_argument("bundle"); im.add_argument("--dir", default=os.environ.get("VEDHA_INTEL_DIR", ""))
    im.add_argument("--allow-downgrade", action="store_true")
    args = ap.parse_args(argv)

    if args.cmd == "keygen":
        key = Ed25519PrivateKey.generate()
        pem = key.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8,
                                serialization.NoEncryption())
        fd = os.open(args.out, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "wb") as fh:
            fh.write(pem)
        print(f"public key (put in INTEL_BUNDLE_PUBLIC_KEYS): {public_key_b64(key.public_key())}")
        return 0
    if args.cmd == "export":
        key = serialization.load_pem_private_key(Path(args.key).read_bytes(), password=None)
        if not isinstance(key, Ed25519PrivateKey):
            raise SystemExit("signing key must be Ed25519")
        src = Path(args.snapshots)
        files = {n: (src / n).read_bytes() for n in sorted(SNAPSHOT_NAMES) if (src / n).is_file()}
        Path(args.out).write_bytes(build_bundle(files, key, version=args.version))
        print(f"wrote {args.out}: {sorted(files)}")
        return 0
    if not args.dir:
        raise SystemExit("--dir (or VEDHA_INTEL_DIR) is required")
    keys = os.environ.get("INTEL_BUNDLE_PUBLIC_KEYS", "").split(",")
    manifest, files = verify_bundle(Path(args.bundle).read_bytes(), keys)
    record = install_bundle(manifest, files, args.dir, allow_downgrade=args.allow_downgrade)
    print(f"installed intel bundle {record['version']} ({len(files)} files) into {args.dir}")
    return 0


if __name__ == "__main__":
    sys.exit(_cli())

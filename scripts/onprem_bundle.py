#!/usr/bin/env python3
"""onprem_bundle.py — hand an on-prem customer the Vedha platform images, securely.

Vedha is centrally hosted; only customers who must run the manager on their own
premises get platform images, on request. Nothing is pushed to a registry. Each
bundle is made for ONE customer:

    build  --customer ACME --recipient age1... --key release-key.pem
           [--agent-release dist/agent-release] [--out dist/onprem]

produces, in <out>/:

    vedha-onprem-<customer>-<version>.tar.age   the bundle, encrypted with age to
                                                the customer's public key(s): only
                                                their private key can open it
    vedha-onprem-load.sh                        the loader, with the Vedha vendor
                                                public key embedded
    vedha-onprem-<customer>-<version>.sha256    checksum to confirm out of band
    ledger.jsonl                                one line per bundle ever issued

Inside the encrypted tar:

    manifest.json / manifest.json.sig   files + SHA-256 + images, Ed25519-signed
    images.tar.gz                       `docker save` of every platform image
    compose/docker-compose.yml          the manager stack
    compose/.env.example                image tags pinned to this release
    agent-release/                      (optional) the signed agent release, so
                                        the on-prem manager can serve agents too

The customer runs `sh vedha-onprem-load.sh <bundle>.tar.age --identity key.txt`.
The loader refuses to load anything unless the signature verifies with the key
embedded in it and every file matches the manifest.

The manifest carries a per-bundle id and the customer name, and the ledger
records which bundle went to whom, so a copy that turns up elsewhere is
traceable.
"""
from __future__ import annotations

import argparse
import base64
import gzip
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
COMPOSE = REPO / "manager" / "docker-compose.yml"
ENV_TEMPLATE = REPO / ".env.docker.example"
LOADER_TEMPLATE = REPO / "deploy" / "onprem" / "vedha-onprem-load.sh"
THIRD_PARTY_IMAGES = ("postgres:16-alpine", "redis:7-alpine", "caddy:2-alpine")
VENDOR_MARKER = re.compile(r'^VEDHA_VENDOR_SPKI=""(.*)$', re.MULTILINE)
_CHUNK = 1024 * 1024

_spec = importlib.util.spec_from_file_location("agent_release", REPO / "scripts" / "agent_release.py")
release = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(release)
ReleaseError = release.ReleaseError


def slug(value: str) -> str:
    out = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    if not out or len(out) > 48:
        raise ReleaseError("customer name must give a 1-48 character slug")
    return out


def validate_recipient(value: str) -> str:
    """An age X25519 recipient (age1...) or an SSH ed25519/RSA public key."""
    value = value.strip()
    if re.fullmatch(r"age1[0-9a-z]{58}", value) or value.startswith(("ssh-ed25519 ", "ssh-rsa ")):
        return value
    raise ReleaseError(f"not an age recipient: {value[:20]}… (expected age1… from `age-keygen`)")


# ── images ───────────────────────────────────────────────────────────────────

def platform_images(version: str) -> dict[str, str]:
    return {
        "backend": f"vedha-backend:{version}",
        "frontend": f"vedha-frontend:{version}",
        **{name.split(":")[0]: name for name in THIRD_PARTY_IMAGES},
    }


def build_platform_images(version: str) -> None:
    env = {
        **os.environ,
        "VEDHA_BACKEND_IMAGE": f"vedha-backend:{version}",
        "VEDHA_FRONTEND_IMAGE": f"vedha-frontend:{version}",
        "VEDHA_VERSION": version,
        # build-time only: compose refuses to render without these
        "POSTGRES_PASSWORD": "build", "JWT_SECRET": "build", "SEED_ADMIN_PASSWORD": "build",
        "NEO4J_PASSWORD": "build",
    }
    cmd = ["docker", "compose", "-p", f"vedha-onprem-build", "-f", str(COMPOSE),
           "--profile", "ui", "build", "api", "frontend"]
    print("  $ " + " ".join(cmd), flush=True)
    if subprocess.run(cmd, env=env, check=False).returncode != 0:
        raise ReleaseError("building the platform images failed")
    for image in THIRD_PARTY_IMAGES:
        if subprocess.run(["docker", "image", "inspect", image], capture_output=True).returncode != 0:
            print(f"  $ docker pull {image}", flush=True)
            if subprocess.run(["docker", "pull", image], check=False).returncode != 0:
                raise ReleaseError(f"could not pull {image}")


def image_ids(tags: list[str]) -> dict[str, str]:
    out = {}
    for tag in tags:
        result = subprocess.run(["docker", "image", "inspect", "--format", "{{.Id}}", tag],
                                capture_output=True, text=True, check=False)
        if result.returncode != 0:
            raise ReleaseError(f"image {tag} is not available locally")
        out[tag] = result.stdout.strip()
    return out


def save_images(tags: list[str], dest: Path) -> None:
    proc = subprocess.Popen(["docker", "save", *tags], stdout=subprocess.PIPE)
    assert proc.stdout is not None
    with dest.open("wb") as raw, gzip.GzipFile(fileobj=raw, mode="wb", compresslevel=6, mtime=0) as gz:
        for chunk in iter(lambda: proc.stdout.read(_CHUNK), b""):
            gz.write(chunk)
    if proc.wait() != 0:
        raise ReleaseError("docker save failed")


def age_encrypt(source: Path, dest: Path, recipients: list[str]) -> None:
    if shutil.which("age") is None:
        raise ReleaseError("`age` is required to encrypt the bundle (macOS: brew install age; "
                           "Debian/Ubuntu: apt install age)")
    cmd = ["age", "--encrypt", "--output", str(dest)]
    for recipient in recipients:
        cmd += ["--recipient", recipient]
    cmd.append(str(source))
    if subprocess.run(cmd, check=False).returncode != 0:
        raise ReleaseError("age encryption failed")


# ── bundle ───────────────────────────────────────────────────────────────────

def env_example(version: str) -> str:
    base = ENV_TEMPLATE.read_text(encoding="utf-8") if ENV_TEMPLATE.is_file() else ""
    return (
        "# Vedha on-prem — copy to .env next to docker-compose.yml and fill in every\n"
        "# secret (scripts in the bundle README explain each one).\n"
        f"VEDHA_BACKEND_IMAGE=vedha-backend:{version}\n"
        f"VEDHA_FRONTEND_IMAGE=vedha-frontend:{version}\n"
        "# The on-prem manager serves agents from ./agent-releases; set the key that\n"
        "# signed them (printed in agent-release/PUBLIC_KEY).\n"
        "AGENT_RELEASE_PUBLIC_KEY=\n"
        "AGENT_RELEASE_REQUIRE_SIGNATURE=true\n"
        "APP_ENV=production\n\n" + base
    )


def write_loader(dest: Path, vendor_raw_b64: str, template: Path = LOADER_TEMPLATE) -> None:
    text = template.read_text(encoding="utf-8")
    if len(VENDOR_MARKER.findall(text)) != 1:
        raise ReleaseError(f"{template} must contain exactly one `VEDHA_VENDOR_SPKI=\"\"` line")
    spki = release.spki_b64_from_raw(vendor_raw_b64)
    text = VENDOR_MARKER.sub(lambda m: f'VEDHA_VENDOR_SPKI="{spki}"{m.group(1)}', text, count=1)
    dest.write_text(text, encoding="utf-8")
    dest.chmod(0o755)


def build_bundle(
    *,
    customer: str,
    recipients: list[str],
    key_path: Path,
    out: Path,
    version: str,
    agent_release_dir: Path | None = None,
    build_images: bool = True,
    builder=build_platform_images,
    saver=save_images,
    ids=image_ids,
    encryptor=age_encrypt,
) -> dict:
    customer_slug = slug(customer)
    recipients = [validate_recipient(r) for r in recipients]
    if not recipients:
        raise ReleaseError("at least one --recipient (the customer's age public key) is required")
    private_key = release.load_private_key(key_path)
    vendor_pub = release.public_raw_b64(private_key)
    images = platform_images(version)
    tags = list(images.values())

    if build_images:
        builder(version)
    image_id_map = ids(tags)

    out.mkdir(parents=True, exist_ok=True)
    name = f"vedha-onprem-{customer_slug}-{version}"
    encrypted = out / f"{name}.tar.age"
    if encrypted.exists():
        raise ReleaseError(f"{encrypted} already exists")
    bundle_id = str(uuid.uuid4())

    with tempfile.TemporaryDirectory(prefix="vedha-onprem-") as tmp:
        stage = Path(tmp) / name
        (stage / "compose").mkdir(parents=True)
        print("Saving platform images ...", flush=True)
        saver(tags, stage / "images.tar.gz")
        shutil.copy2(COMPOSE, stage / "compose" / "docker-compose.yml")
        (stage / "compose" / ".env.example").write_text(env_example(version), encoding="utf-8")
        if agent_release_dir is not None:
            release_dir = release.resolve_release_dir(agent_release_dir)
            release.verify_release_dir(release_dir, vendor_pub)
            target = stage / "agent-release"
            shutil.copytree(release_dir, target / release_dir.name)
            (target / "CURRENT").write_text(release_dir.name + "\n")
            (target / "PUBLIC_KEY").write_text(vendor_pub + "\n")

        files = []
        for path in sorted(p for p in stage.rglob("*") if p.is_file()):
            rel = path.relative_to(stage).as_posix()
            files.append({"path": rel, "sha256": release.sha256_file(path), "size": path.stat().st_size})
        manifest = {
            "schema": 1,
            "kind": "vedha-onprem-bundle",
            "bundle_id": bundle_id,
            "customer": customer,
            "version": version,
            "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "images": [{"role": role, "tag": tag, "id": image_id_map[tag]} for role, tag in images.items()],
            "files": files,
            "signing_key_id": release.key_id(vendor_pub),
        }
        manifest_bytes = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode()
        (stage / "manifest.json").write_bytes(manifest_bytes)
        (stage / "manifest.json.sig").write_text(release.sign_manifest(private_key, manifest_bytes) + "\n")

        plain = Path(tmp) / f"{name}.tar"
        with tarfile.open(plain, "w") as tar:
            tar.add(stage, arcname=name)
        encryptor(plain, encrypted, recipients)
        plain.unlink()

    encrypted.chmod(0o644)
    digest = release.sha256_file(encrypted)
    (out / f"{name}.sha256").write_text(f"{digest}  {encrypted.name}\n")
    write_loader(out / "vedha-onprem-load.sh", vendor_pub)
    entry = {
        "bundle_id": bundle_id, "customer": customer, "version": version,
        "created_at": manifest["created_at"], "file": encrypted.name, "sha256": digest,
        "recipients": [hashlib.sha256(r.encode()).hexdigest()[:16] for r in recipients],
        "signing_key_id": manifest["signing_key_id"],
    }
    with (out / "ledger.jsonl").open("a", encoding="utf-8") as ledger:
        ledger.write(json.dumps(entry, sort_keys=True) + "\n")
    return entry


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)
    bd = sub.add_parser("build", help="build one customer's encrypted, signed on-prem bundle")
    bd.add_argument("--customer", required=True)
    bd.add_argument("--recipient", action="append", default=[], help="customer age public key (repeatable)")
    bd.add_argument("--key", required=True, type=Path, help="vendor Ed25519 key (scripts/agent_release.py keygen)")
    bd.add_argument("--out", type=Path, default=REPO / "dist" / "onprem")
    bd.add_argument("--version", default=None)
    bd.add_argument("--agent-release", type=Path, default=None, help="include this signed agent release")
    bd.add_argument("--skip-build", action="store_true", help="use already-built vedha-*:<version> images")
    args = parser.parse_args(argv)
    try:
        entry = build_bundle(
            customer=args.customer, recipients=args.recipient, key_path=args.key, out=args.out,
            version=args.version or release.read_version(), agent_release_dir=args.agent_release,
            build_images=not args.skip_build,
        )
    except ReleaseError as exc:
        print(f"onprem-bundle: {exc}", file=sys.stderr)
        return 1
    print(f"\nBundle {entry['bundle_id']} for {entry['customer']}:")
    print(f"  {args.out / entry['file']}")
    print(f"  {args.out / 'vedha-onprem-load.sh'}")
    print(f"  SHA-256 {entry['sha256']}")
    print("Send the bundle and loader by a time-limited link; give the SHA-256 over a")
    print("different channel (phone, Signal). Only the customer's age key can decrypt it.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

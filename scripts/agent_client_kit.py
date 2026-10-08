#!/usr/bin/env python3
"""agent_client_kit.py — the folder you send a client so they can install the agent.

    python3 scripts/agent_client_kit.py --customer "ACME Bank" \\
        --manager https://api.vedhasec.com --public-key <AGENT_RELEASE_PUBLIC_KEY> \\
        [--release dist/agent-release] [--contact "Name, phone, email"] [--out dist/client-kit]

The kit holds only:

    vedha-agent-install.sh   the signed release's installer (release key embedded)
    INSTALL.md               the client guide, filled in for this customer
    SHA256SUMS               checksums of the two files above

It never holds the agent image: the installer downloads that from the manager
with a single-use install token, and checks its signature and checksum first.
So the kit can travel by email; the token and the installer checksum go by a
different channel (phone, Signal).

Before writing anything the kit verifies the release against the public key you
pass (the manager's AGENT_RELEASE_PUBLIC_KEY), not against the key inside the
installer, and refuses a development installer or a plain-http manager.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import importlib.util
import re
import shutil
import sys
import zipfile
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

REPO = Path(__file__).resolve().parent.parent
TEMPLATE = REPO / "docs" / "probe" / "client-kit" / "INSTALL.template.md"
INSTALLER_NAME = "vedha-agent-install.sh"


class KitError(Exception):
    pass


def _release_tool():
    spec = importlib.util.spec_from_file_location("agent_release", REPO / "scripts" / "agent_release.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules.setdefault("agent_release", mod)
    spec.loader.exec_module(mod)
    return mod


def slug(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    if not s:
        raise KitError("customer name must contain letters or digits")
    return s[:48]


def check_manager(url: str) -> tuple[str, str]:
    url = url.rstrip("/")
    parsed = urlparse(url)
    if parsed.scheme != "https" or not parsed.hostname:
        raise KitError("--manager must be an https:// URL (the agent never talks to a plain-http manager in production)")
    if parsed.path not in ("", "/") or parsed.query or parsed.fragment:
        raise KitError("--manager must be just the scheme and host, e.g. https://api.vedhasec.com")
    return url, parsed.netloc


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def render(template: str, values: dict[str, str]) -> str:
    out = template
    for key, value in values.items():
        out = out.replace("{{" + key + "}}", value)
    left = sorted(set(re.findall(r"\{\{[A-Z_]+\}\}", out)))
    if left:
        raise KitError(f"guide template has unfilled placeholders: {', '.join(left)}")
    return out


def build_kit(*, release: Path, public_key_b64: str, customer: str, manager: str,
              contact: str, out: Path, today: date | None = None) -> Path:
    tool = _release_tool()
    release_dir = tool.resolve_release_dir(release)
    try:
        manifest = tool.verify_release_dir(release_dir, public_key_b64.strip())
    except tool.ReleaseError as exc:
        raise KitError(f"release {release_dir} failed verification: {exc}") from exc

    installer_src = release_dir / manifest["installer"]["file"]
    text = installer_src.read_text(encoding="utf-8")
    if 'VEDHA_RELEASE_SPKI=""' in text:
        raise KitError("the installer has no release key embedded (development copy); build a signed release")

    manager_url, manager_host = check_manager(manager)
    version = manifest["version"]
    kit_name = f"vedha-agent-kit-{slug(customer)}-{version}"
    kit_dir = out / kit_name
    if kit_dir.exists():
        shutil.rmtree(kit_dir)
    kit_dir.mkdir(parents=True)

    installer = kit_dir / INSTALLER_NAME
    shutil.copyfile(installer_src, installer)
    installer.chmod(0o755)
    installer_sha = _sha256(installer)

    guide = render(TEMPLATE.read_text(encoding="utf-8"), {
        "CUSTOMER": customer.strip(),
        "VERSION": version,
        "MANAGER": manager_url,
        "MANAGER_HOST": manager_host,
        "DATE": (today or date.today()).isoformat(),
        "INSTALLER_SHA256": installer_sha,
        "KEY_ID": tool.key_id(public_key_b64.strip()),
        "CONTACT": contact.strip() or "your Vedha account contact",
    })
    (kit_dir / "INSTALL.md").write_text(guide, encoding="utf-8")

    sums = "".join(f"{_sha256(kit_dir / n)}  {n}\n" for n in (INSTALLER_NAME, "INSTALL.md"))
    (kit_dir / "SHA256SUMS").write_text(sums, encoding="utf-8")

    archive = out / f"{kit_name}.zip"
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as zf:
        for name in (INSTALLER_NAME, "INSTALL.md", "SHA256SUMS"):
            info = zipfile.ZipInfo(f"{kit_name}/{name}", date_time=(1980, 1, 1, 0, 0, 0))
            info.external_attr = (0o755 if name == INSTALLER_NAME else 0o644) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, (kit_dir / name).read_bytes())
    return kit_dir


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--customer", required=True)
    ap.add_argument("--manager", required=True, help="https://api.<your domain>")
    ap.add_argument("--public-key", required=True, help="AGENT_RELEASE_PUBLIC_KEY from the manager's .env")
    ap.add_argument("--release", default=str(REPO / "dist" / "agent-release"),
                    help="release store (uses CURRENT) or one version directory")
    ap.add_argument("--contact", default="")
    ap.add_argument("--out", default=str(REPO / "dist" / "client-kit"))
    args = ap.parse_args(argv)
    try:
        kit = build_kit(release=Path(args.release), public_key_b64=args.public_key, customer=args.customer,
                        manager=args.manager, contact=args.contact, out=Path(args.out))
    except KitError as exc:
        print(f"agent-client-kit: {exc}", file=sys.stderr)
        return 2
    sha = (kit / "SHA256SUMS").read_text().splitlines()[0].split()[0]
    print(f"Client kit: {kit}  (and {kit}.zip)")
    print("Send the zip by email or file share. Separately (phone / Signal), give the client:")
    print("  1. the install token  (Fleet → Add agent → Generate install command; copy only vet_…)")
    print(f"  2. the installer checksum  {sha}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

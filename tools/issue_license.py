#!/usr/bin/env python3
"""
issue_license.py — VENDOR-SIDE tool. Keep the private key OFF client machines.

  # one-time: make a keypair. Embed the printed PUBLIC key in agent/license.py
  # (VENDOR_PUBLIC_KEY_HEX); keep vendor_private.key secret.
  python3 tools/issue_license.py keygen

  # issue a host-locked license for a client (get their Host ID from the probe:
  #   docker run ... vedha-probe hostid   →  prints the Host ID)
  python3 tools/issue_license.py issue --hostid <id> --customer "Acme" --days 365

  # floating (any-machine) license:
  python3 tools/issue_license.py issue --hostid '*' --customer "Acme" --days 30
"""
from __future__ import annotations

import argparse
import base64
import json
import sys
from datetime import date, timedelta
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization

KEY_FILE = Path(__file__).parent / "vendor_private.key"   # gitignore this!


def _b64(b: bytes) -> str:
    return base64.urlsafe_b64encode(b).decode().rstrip("=")


def keygen() -> None:
    if KEY_FILE.exists():
        print(f"refusing to overwrite existing {KEY_FILE}", file=sys.stderr); sys.exit(1)
    priv = Ed25519PrivateKey.generate()
    KEY_FILE.write_bytes(priv.private_bytes(
        serialization.Encoding.Raw, serialization.PrivateFormat.Raw,
        serialization.NoEncryption()))
    pub = priv.public_key().public_bytes(
        serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    print(f"private key written to {KEY_FILE} (KEEP SECRET, do not commit/ship)")
    print(f"\nEmbed this in agent/license.py VENDOR_PUBLIC_KEY_HEX:\n  {pub.hex()}")


def issue(hostid: str, customer: str, days: int) -> None:
    if not KEY_FILE.exists():
        print("no vendor key — run 'keygen' first", file=sys.stderr); sys.exit(1)
    priv = Ed25519PrivateKey.from_private_bytes(KEY_FILE.read_bytes())
    payload = json.dumps({
        "customer": customer, "hostid": hostid,
        "issued": date.today().isoformat(),
        "expires": (date.today() + timedelta(days=days)).isoformat(),
    }, separators=(",", ":")).encode()
    sig = priv.sign(payload)
    print(f"{_b64(payload)}.{_b64(sig)}")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("keygen")
    iss = sub.add_parser("issue")
    iss.add_argument("--hostid", required=True)
    iss.add_argument("--customer", required=True)
    iss.add_argument("--days", type=int, default=365)
    a = p.parse_args()
    if a.cmd == "keygen":
        keygen()
    else:
        issue(a.hostid, a.customer, a.days)


if __name__ == "__main__":
    main()

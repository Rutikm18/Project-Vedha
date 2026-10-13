#!/usr/bin/env python3
"""
make_test_release.py — wrap a Windows package in a THROWAWAY-keyed release, with placeholder
Linux images, using the real installer sources and the real release builder.

For CI and local experiments only: the keys are generated on the spot and printed, nothing
here can be mistaken for (or substituted for) a production release. CI uses it to exercise
the installer's Authenticode path with a self-signed test certificate, which would otherwise
stay untested until a real certificate exists.

    python scripts/ci/make_test_release.py --windows-zip vedha-agent-win.zip --out rel \
        [--version 0.0.0-ci] [--thumbprint <40 hex>]

Prints the release directory on the last line.
"""
from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]


def _tool():
    spec = importlib.util.spec_from_file_location("agent_release_tool", REPO / "scripts" / "agent_release.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--windows-zip", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--version", default="0.0.0-ci")
    ap.add_argument("--thumbprint", default=None, help="pin this Authenticode certificate thumbprint")
    args = ap.parse_args(argv)

    tool = _tool()
    keys = args.out / "_throwaway-keys"
    keys.mkdir(parents=True, exist_ok=True)
    tool.keygen(keys / "ed25519.pem")
    tool.keygen_p256(keys / "p256.pem")
    final = tool.build_release(
        key_path=keys / "ed25519.pem", out=args.out / "release", arches=["amd64"], version=args.version,
        builder=lambda tag, arch, ctx: None,
        saver=lambda tag, dest: dest.write_bytes(b"placeholder image for a test release\n"),
        p256_key_path=keys / "p256.pem", windows_zip=args.windows_zip,
        authenticode_thumbprint=args.thumbprint,
    )
    print(final)
    return 0


if __name__ == "__main__":
    sys.exit(main())

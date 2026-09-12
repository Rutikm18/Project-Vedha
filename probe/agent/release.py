"""release.py — release integrity + SBOM (Phase 10).

The checksum manifest is the counterpart to Phase 7's strict-security
`verify_download`: CI produces it, the installer verifies against it. The SBOM
(CycloneDX) is the CRA/EO-14028 procurement artifact. Pure; `main()` lets CI emit
both.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_manifest(base_dir: str, relpaths: list[str]) -> dict[str, str]:
    return {rel: sha256_file(os.path.join(base_dir, rel)) for rel in relpaths}


def verify_manifest(base_dir: str, manifest: dict[str, str]) -> tuple[bool, list[str]]:
    bad: list[str] = []
    for rel, want in manifest.items():
        p = os.path.join(base_dir, rel)
        if not os.path.exists(p) or sha256_file(p) != want:
            bad.append(rel)
    return (not bad), bad


def parse_requirements(text: str) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    for line in text.splitlines():
        s = line.split("#", 1)[0].strip()
        if not s:
            continue
        m = re.match(r"^([A-Za-z0-9_.\-]+)\s*(.*)$", s)
        if m:
            out.append((m.group(1), m.group(2).strip()))
    return out


def sbom_from_requirements(text: str, *, component_name: str = "vedha-agent",
                           version: str = "0.0.0") -> dict:
    components = [
        {"type": "library", "name": name, "version": (spec or "*")}
        for name, spec in parse_requirements(text)
    ]
    return {
        "bomFormat": "CycloneDX",
        "specVersion": "1.5",
        "version": 1,
        "metadata": {"component": {"type": "application", "name": component_name, "version": version}},
        "components": components,
    }


def main(argv: list[str] | None = None) -> int:
    import argparse
    p = argparse.ArgumentParser(prog="vedha-release")
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("sbom")
    s.add_argument("--reqs", default="requirements-runtime.txt")
    s.add_argument("--out", default="sbom.cdx.json")
    s.add_argument("--version", default="0.0.0")
    args = p.parse_args(argv)
    if args.cmd == "sbom":
        with open(args.reqs, encoding="utf-8") as fh:
            sbom = sbom_from_requirements(fh.read(), version=args.version)
        with open(args.out, "w", encoding="utf-8") as fh:
            json.dump(sbom, fh, indent=2)
        print(f"SBOM ({len(sbom['components'])} components) → {args.out}")
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

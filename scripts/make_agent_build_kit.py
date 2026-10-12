#!/usr/bin/env python3
"""make_agent_build_kit.py - a small zip with ONLY what is needed to build, sign and publish the Windows agent.

The whole repository holds the manager (API, console, detection engine) as well. A Windows PC that only
builds the agent has no business holding that, so this packs the minimum:

  VERSION                          the release number
  scripts/agent_release.py         the release tool (build, sign, verify, publish, pull)
  probe/install.sh                 the Linux installer the release tool embeds
  probe/requirements-runtime.txt   what the compiled agent needs
  probe/tools/agent_closure.py     computes which agent modules are compiled (and refuses the rest)
  probe/windows/                   the build, package, install and publish scripts (no tests)
  probe/agent, scanner, workflow   ONLY the modules the agent can load (agent_closure.py's list)

NOT in it: the manager, the console, the detection engine, the vulnerability-judgement rules
(scanner/findings.py), the campaign runner, the accuracy gates, tests, docs, any .env or key.

    python scripts/make_agent_build_kit.py [--out DIR]       -> DIR/vedha-agent-build-kit-<VERSION>.zip

On the Windows PC: unzip, open PowerShell in the unzipped folder, and run
    powershell -ExecutionPolicy Bypass -File probe\\windows\\publish-release.ps1 -Server user@host -ManagerUrl https://api.example.com -ConfigureManager
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import sys
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PROBE = REPO / "probe"

# Paths (relative to the repo) that must never be in the kit, whatever a future change adds.
FORBIDDEN_PREFIXES = ("manager/", "docs/", ".github/", ".git/", "deploy/", "frontend/")
FORBIDDEN_NAMES = ("findings.py", ".env", "-key.pem", ".pem", ".pfx")
WINDOWS_EXCLUDED_DIRS = {"tests", "hosting", "dist", ".venv-win", "__pycache__"}


def _closure():
    spec = importlib.util.spec_from_file_location("agent_closure_for_kit", PROBE / "tools" / "agent_closure.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module            # dataclasses resolve their own module through sys.modules
    spec.loader.exec_module(module)
    return module


def kit_files() -> dict[str, Path]:
    """archive path -> source file, for everything that goes into the kit."""
    files: dict[str, Path] = {
        "VERSION": REPO / "VERSION",
        "scripts/agent_release.py": REPO / "scripts" / "agent_release.py",
        "probe/install.sh": PROBE / "install.sh",
        "probe/requirements-runtime.txt": PROBE / "requirements-runtime.txt",
        "probe/tools/agent_closure.py": PROBE / "tools" / "agent_closure.py",
    }
    for path in sorted((PROBE / "windows").rglob("*")):
        rel = path.relative_to(PROBE / "windows")
        if path.suffix == ".md":
            continue                                           # developer notes: not needed to build
        if path.is_file() and not (set(rel.parts[:-1]) & WINDOWS_EXCLUDED_DIRS):
            files[f"probe/windows/{rel.as_posix()}"] = path
    closure = _closure().compute(PROBE)
    for path in sorted(closure.files):
        files[f"probe/{path.relative_to(PROBE).as_posix()}"] = path
    return files


def check_clean(names) -> None:
    """Refuse to build a kit that carries anything it must not."""
    for name in names:
        low = name.lower()
        if low.startswith(FORBIDDEN_PREFIXES) or any(low.endswith(n) for n in FORBIDDEN_NAMES):
            raise SystemExit(f"refusing to build the kit: {name} must not be in it")


README = """Vedha agent build kit {version}
=================================

What this is: the minimum needed to build, sign and publish the Windows agent from this PC.
It holds the agent's own code and the build scripts. It does not hold the manager, the console, the
detection engine, the vulnerability rules, tests, or any key or password.

You need on this PC: Windows 10/11 or Server 2016+, Python 3.10, 3.11 or 3.12 (tick "Add Python to PATH"),
and ssh that already logs in to your manager server with a key.

1. Unzip this folder somewhere with a short path and no spaces, for example C:\\VedhaKit
2. Open PowerShell in that folder and run (use your own server and manager address):

   powershell -ExecutionPolicy Bypass -File probe\\windows\\publish-release.ps1 -Server ubuntu@YOUR_SERVER -ManagerUrl https://api.your-domain -ConfigureManager

   Add -AllowTokenlessInstall to let machines install without a token (you approve them in Fleet).
   Add -DryRun first to see the plan without doing anything.
3. The first run takes 15-35 minutes (it builds the agent). It creates your signing keys in
   %USERPROFILE%\\.vedha : copy that folder somewhere safe and offline, and never send it to anyone.

Files in this kit and their SHA-256 are listed in KIT-FILES.txt.
"""


def build(out_dir: Path) -> Path:
    version = (REPO / "VERSION").read_text(encoding="utf-8").strip()
    files = kit_files()
    check_clean(files)
    listing = "".join(f"{hashlib.sha256(src.read_bytes()).hexdigest()}  {name}\n" for name, src in sorted(files.items()))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / f"vedha-agent-build-kit-{version}.zip"
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as zf:
        for name, src in sorted(files.items()):
            info = zipfile.ZipInfo(name, date_time=(2020, 1, 1, 0, 0, 0))     # reproducible: no timestamps
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            zf.writestr(info, src.read_bytes())
        for name, text in (("KIT-README.txt", README.format(version=version)), ("KIT-FILES.txt", listing)):
            info = zipfile.ZipInfo(name, date_time=(2020, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            zf.writestr(info, text.replace("\n", "\r\n").encode("utf-8"))
    return target


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out", type=Path, default=REPO / "dist")
    args = parser.parse_args(argv)
    target = build(args.out)
    size = target.stat().st_size
    with zipfile.ZipFile(target) as zf:
        count = len(zf.namelist())
    print(f"{target}  ({count} files, {size / 1e6:.2f} MB)")
    print("sha256", hashlib.sha256(target.read_bytes()).hexdigest())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

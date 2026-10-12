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


# ---- the one-line bootstrap: download the kit from a private link, check it, unpack it, publish -------------

_URL_RE = __import__("re").compile(r"https://[^\s'\"`<>^|\\]{8,2000}")
_SHA_RE = __import__("re").compile(r"[0-9a-fA-F]{64}")
_SERVER_RE = __import__("re").compile(r"([A-Za-z0-9._-]+@)?[A-Za-z0-9.-]+")
_MANAGER_RE = __import__("re").compile(r"https://[A-Za-z0-9.-]+(:[0-9]{1,5})?")
_DIR_RE = __import__("re").compile(r"[A-Za-z]:\\[A-Za-z0-9_.\\-]{1,120}")

PYTHON_BLOCK = (
    "$py = try { (& python --version 2>&1 | Out-String) } catch { '' }; "
    "if ($py -notmatch '^Python 3\\.(10|11|12)\\.') { "
    "Write-Host 'Python 3.10-3.12 not found: installing Python 3.12 with winget'; "
    "winget install -e --id Python.Python.3.12 --silent --accept-package-agreements --accept-source-agreements; "
    "$env:Path = [Environment]::GetEnvironmentVariable('Path','Machine') + ';' + [Environment]::GetEnvironmentVariable('Path','User'); "
    "$py = try { (& python --version 2>&1 | Out-String) } catch { '' }; "
    "if ($py -notmatch '^Python 3\\.(10|11|12)\\.') { throw 'Python 3.10-3.12 is needed and could not be installed automatically: install it from python.org (tick Add Python to PATH) and run this again.' } }"
)


def bootstrap_command(url: str, sha256: str, *, server: str, manager_url: str, allow_tokenless: bool = False,
                      install_dir: str = "C:\\VedhaKit", powershell: str = "powershell", ensure_python: bool = True,
                      extra_args: str = "") -> str:
    """The ONE command to paste into PowerShell on the publishing PC.

    It downloads the kit from `url` (any private, time-limited link: an S3 pre-signed URL, an Azure SAS URL, a GCS
    signed URL), refuses it unless its SHA-256 equals `sha256`, unpacks it OVER `install_dir` (an existing build
    environment, built agent and keys folder are never deleted), installs Python 3.12 with winget when no usable
    Python is there, and runs publish-release.ps1. Every value is checked against a strict pattern first, because
    each one ends up inside a single-quoted PowerShell string."""
    if not _URL_RE.fullmatch(url):
        raise ValueError("the kit link must be an https:// address with no spaces or quote characters")
    if not _SHA_RE.fullmatch(sha256):
        raise ValueError("the SHA-256 must be 64 hex characters")
    if not _SERVER_RE.fullmatch(server):
        raise ValueError("the server must look like user@host")
    if not _MANAGER_RE.fullmatch(manager_url.rstrip("/")):
        raise ValueError("the manager address must look like https://host")
    if not _DIR_RE.fullmatch(install_dir):
        raise ValueError("the install folder must be a plain Windows path such as C:\\VedhaKit")
    if extra_args and not __import__("re").fullmatch(r"(-[A-Za-z]+ ?)+", extra_args):
        raise ValueError("extra arguments must be plain switches such as -DryRun")
    publish = (f"& {powershell} -NoProfile -ExecutionPolicy Bypass -File (Join-Path $dir 'probe\\windows\\publish-release.ps1') "
               f"-Server '{server}' -ManagerUrl '{manager_url.rstrip('/')}' -ConfigureManager"
               + (" -AllowTokenlessInstall" if allow_tokenless else "") + (f" {extra_args.strip()}" if extra_args else ""))
    parts = [
        "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12",
        "$ErrorActionPreference = 'Stop'",
        f"$dir = '{install_dir}'",
        "$zip = Join-Path ([IO.Path]::GetTempPath()) 'vedha-agent-build-kit.zip'",
        f"Invoke-WebRequest -UseBasicParsing -Uri '{url}' -OutFile $zip",
        f"if ((Get-FileHash -LiteralPath $zip -Algorithm SHA256).Hash -ne '{sha256.lower()}') "
        "{ Remove-Item -LiteralPath $zip -Force; throw 'The downloaded kit does not match its checksum: nothing was unpacked.' }",
        "Expand-Archive -LiteralPath $zip -DestinationPath $dir -Force",
        "Remove-Item -LiteralPath $zip -Force",
        "try { Get-ChildItem -LiteralPath $dir -Recurse -File | Unblock-File } catch { }",
    ]
    if ensure_python:
        parts.append(PYTHON_BLOCK)
    parts.append(publish)
    return "; ".join(parts)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out", type=Path, default=REPO / "dist")
    parser.add_argument("--url", help="private, time-limited https link the kit will be downloaded from; "
                                      "prints the one command to paste into PowerShell")
    parser.add_argument("--server", default="ubuntu@YOUR_SERVER", help="user@host of the manager server (ssh)")
    parser.add_argument("--manager-url", default="https://api.your-domain", help="https address of the manager")
    parser.add_argument("--allow-tokenless", action="store_true", help="add -AllowTokenlessInstall")
    args = parser.parse_args(argv)
    target = build(args.out)
    size = target.stat().st_size
    with zipfile.ZipFile(target) as zf:
        count = len(zf.namelist())
    print(f"{target}  ({count} files, {size / 1e6:.2f} MB)")
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    print("sha256", digest)
    if args.url:
        command = bootstrap_command(args.url, digest, server=args.server, manager_url=args.manager_url,
                                    allow_tokenless=args.allow_tokenless)
        print("\nPaste this into PowerShell on the publishing PC (the link inside it is a secret until it expires):\n")
        print(command)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

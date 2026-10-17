#!/usr/bin/env python3
"""airgap_package.py — build the self-contained air-gapped Windows agent zip, on ANY OS.

Approach #1 (the fallback to the one-command download): a client that cannot, or will
not, run the `irm | iex` installer gets a self-contained zip instead. This assembles
that zip from a PRE-BUILT compiled agent (the Windows-once build) plus the repo's
installer scripts, baking in the generic facade URL. It runs on macOS / Linux / Windows,
so you never need a Windows box just to repackage — only to compile the agent once.

The output is byte-compatible with `probe/windows/package-zip.ps1 -Manager <url>`:
the same files, the same placeholder substitutions, and a SHA256SUMS.txt in exactly the
form the packaged `install.ps1` verifies (`<64-hex>  <relative/path>`, forward slashes,
order-independent). So an air-gapped zip built here installs identically to one built on
Windows.

What the client does with it:

    install.cmd -Token vet_XXXXXXXX

The `vet_` token is created in Fleet and handed over on a separate channel; the facade
URL is baked in, so the client is never given a manager IP, key or internal name — only
the generic facade address and a single-use token.

Usage:

    python3 scripts/airgap_package.py --agent dist/vedha-agent-win.zip \\
        --manager https://get.vedhasec.com

    python3 scripts/airgap_package.py --agent /path/to/vedha-agent \\
        --manager https://get.vedhasec.com --version 1.0.404 --out dist/vedha-agent-airgap.zip

`--agent` is either the `vedha-agent-win.zip` from the Windows build (its `vedha-agent/`
folder is used) or a `vedha-agent` folder that contains `vedha-agent.exe`.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
WIN_DIR = REPO_ROOT / "probe" / "windows"

# The installer scripts copied into every package (plain text; no proprietary logic).
PACKAGE_SCRIPTS = ("run.cmd", "install.ps1", "install.cmd", "uninstall.ps1", "uninstall.cmd")

_HTTPS_RE = re.compile(r"^https://[A-Za-z0-9.-]+(:[0-9]{1,5})?$")


class AirgapError(Exception):
    """A clear, actionable packaging failure."""


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def clean_manager(url: str) -> tuple[str, str]:
    """(normalized url, host). The Windows installer refuses anything but https://host[:port]."""
    manager = url.strip().rstrip("/")
    if not _HTTPS_RE.fullmatch(manager):
        raise AirgapError(
            f"--manager must be an https:// address such as https://get.vedhasec.com (got '{url}')"
        )
    host = manager.split("://", 1)[1].split("/", 1)[0]
    return manager, host


def resolve_agent_dir(agent: Path, workdir: Path) -> Path:
    """Return a folder that holds vedha-agent.exe, extracting the win zip if needed.

    Accepts the vedha-agent-win.zip (uses its vedha-agent/ folder) or a vedha-agent
    folder directly. Rejects anything without the compiled exe, loudly."""
    if agent.is_file() and agent.suffix.lower() == ".zip":
        extracted = workdir / "agent_zip"
        with zipfile.ZipFile(agent) as archive:
            # Guard against path traversal in a tampered zip before extracting.
            for name in archive.namelist():
                if name.startswith("/") or ".." in Path(name).parts:
                    raise AirgapError(f"the agent zip contains an unsafe path: {name}")
            archive.extractall(extracted)
        candidate = extracted / "vedha-agent"
        if not (candidate / "vedha-agent.exe").is_file():
            # Some builds may place the exe at the zip root instead of under vedha-agent/.
            if (extracted / "vedha-agent.exe").is_file():
                candidate = extracted
            else:
                raise AirgapError(
                    f"{agent} does not contain vedha-agent/vedha-agent.exe — is it a Windows agent package?"
                )
        return candidate
    if agent.is_dir():
        if (agent / "vedha-agent.exe").is_file():
            return agent
        if (agent / "vedha-agent" / "vedha-agent.exe").is_file():
            return agent / "vedha-agent"
        raise AirgapError(f"{agent} does not contain vedha-agent.exe")
    raise AirgapError(f"--agent must be a vedha-agent-win.zip or a vedha-agent folder (got {agent})")


def _read_version() -> str:
    version_file = REPO_ROOT / "VERSION"
    if version_file.is_file():
        return version_file.read_text(encoding="utf-8").splitlines()[0].strip() or "dev"
    return "dev"


def _agent_version() -> str:
    """The agent's own version, read from version.py so the release info is accurate."""
    version_py = REPO_ROOT / "probe" / "agent" / "version.py"
    if version_py.is_file():
        match = re.search(r'AGENT_VERSION\s*=\s*"([^"]+)"', version_py.read_text(encoding="utf-8"))
        if match:
            return match.group(1)
    return ""


def _bake(path: Path, replacements: dict[str, str]) -> None:
    """Exact byte-level substitution so CRLF line endings survive untouched (the
    scripts must stay valid Windows text and hash deterministically)."""
    data = path.read_bytes()
    for token, value in replacements.items():
        data = data.replace(token.encode("utf-8"), value.encode("utf-8"))
    path.write_bytes(data)


def _write_sha256sums(stage: Path) -> None:
    """One line per file, `<sha256>  <relative/path>` with forward slashes, sorted for
    reproducibility. Order-independent for the installer, but stable here on purpose."""
    lines = []
    for file in sorted(p for p in stage.rglob("*") if p.is_file() and p.name != "SHA256SUMS.txt"):
        relative = file.relative_to(stage).as_posix()
        lines.append(f"{_sha256(file)}  {relative}")
    (stage / "SHA256SUMS.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_airgap_zip(
    *,
    agent: Path,
    manager_url: str,
    version: str | None = None,
    out_zip: Path | None = None,
    win_dir: Path = WIN_DIR,
) -> dict:
    """Assemble the air-gapped customer zip. Returns a small summary dict."""
    manager, host = clean_manager(manager_url)
    package_version = version or _read_version()
    out_zip = out_zip or (REPO_ROOT / "dist" / "vedha-agent-airgap.zip")

    for name in (*PACKAGE_SCRIPTS, "README-CUSTOMER.txt", "ALLOWLIST.template.txt"):
        if not (win_dir / name).is_file():
            raise AirgapError(f"missing installer file {win_dir / name}")

    with tempfile.TemporaryDirectory(prefix="vedha-airgap-") as tmp:
        workdir = Path(tmp)
        agent_dir = resolve_agent_dir(agent, workdir)
        stage = workdir / "stage"
        stage.mkdir()

        # 1) the compiled agent (no source), then the plain installer scripts.
        shutil.copytree(agent_dir, stage / "vedha-agent")
        for name in PACKAGE_SCRIPTS:
            shutil.copy2(win_dir / name, stage / name)
        shutil.copy2(win_dir / "README-CUSTOMER.txt", stage / "README.txt")

        # 2) bake the facade URL + version into the scripts (byte-level; CRLF preserved).
        _bake(stage / "install.ps1", {"__VEDHA_MANAGER_URL__": manager, "__VEDHA_PACKAGE_VERSION__": package_version})
        _bake(stage / "run.cmd", {"__VEDHA_MANAGER_URL__": manager})

        # 3) the allow-list the customer's security team uses (host, version, exe hash).
        exe_sha = _sha256(stage / "vedha-agent" / "vedha-agent.exe")
        allowlist = (win_dir / "ALLOWLIST.template.txt").read_text(encoding="utf-8")
        allowlist = (allowlist.replace("{{MANAGER_HOST}}", host)
                              .replace("{{VERSION}}", package_version)
                              .replace("{{EXE_SHA256}}", exe_sha))
        (stage / "ALLOWLIST.txt").write_text(allowlist, encoding="utf-8")

        # 4) a checksum of every file; the installer re-checks these before it installs.
        _write_sha256sums(stage)

        # 5) zip the staged contents at the root (matches Compress-Archive -Path stage/*).
        out_zip.parent.mkdir(parents=True, exist_ok=True)
        if out_zip.exists():
            out_zip.unlink()
        with zipfile.ZipFile(out_zip, "w", zipfile.ZIP_DEFLATED) as archive:
            for file in sorted(p for p in stage.rglob("*") if p.is_file()):
                archive.write(file, file.relative_to(stage).as_posix())

    zip_sha = _sha256(out_zip)
    out_zip.with_suffix(out_zip.suffix + ".sha256").write_text(
        f"{zip_sha}  {out_zip.name}\n", encoding="utf-8"
    )
    info = {
        "schema": 1,
        "version": _agent_version(),          # the agent's own version (the binary matches the checked-out code)
        "package_version": package_version,
        "manager": manager,
        "zip": out_zip.name,
        "sha256": zip_sha,
        "exe_sha256": exe_sha,
        "size": out_zip.stat().st_size,
        "built_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    out_zip.with_suffix(".release.json").write_text(json.dumps(info), encoding="utf-8")
    return info


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build the air-gapped Windows agent zip (any OS).")
    parser.add_argument("--agent", required=True, type=Path,
                        help="the vedha-agent-win.zip from the Windows build, or a vedha-agent folder")
    parser.add_argument("--manager", required=True,
                        help="the facade https:// address baked into the package, e.g. https://get.vedhasec.com")
    parser.add_argument("--version", default=None, help="package version (default: the VERSION file)")
    parser.add_argument("--out", type=Path, default=None, help="output zip path (default: dist/vedha-agent-airgap.zip)")
    args = parser.parse_args(argv)
    try:
        info = build_airgap_zip(agent=args.agent, manager_url=args.manager, version=args.version, out_zip=args.out)
    except AirgapError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    out = args.out or (REPO_ROOT / "dist" / "vedha-agent-airgap.zip")
    print(f"Packaged (air-gapped): {out}")
    print(f"  Manager baked in : {info['manager']}")
    print(f"  Package version  : {info['package_version']}")
    print(f"  vedha-agent.exe  : {info['exe_sha256']}")
    print(f"  ZIP SHA-256      : {info['sha256']}")
    print("")
    print("  Send the ZIP + its SHA-256 to the customer, and the one-time vet_ token on a")
    print("  DIFFERENT channel. They run:  install.cmd -Token vet_XXXXXXXX")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

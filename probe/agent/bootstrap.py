"""bootstrap.py — Layer-1 (Python runtime) install + optional installer verification.

Pure logic used by the sh/ps1 shims and the brain. The strict-security controls
are OPTIONAL in this initial phase: `security_mode` defaults to *permissive*
(verify-and-warn) and `--strict` turns on fail-closed verification. Strict should
become the default at GA (see the architecture doc's signing/hardening phase).
"""
from __future__ import annotations

import hashlib


def python_install_cmd(os_name: str, pm: str) -> list[str]:
    """The per-OS command that installs Python 3 + the venv module. Empty list
    means 'no supported package manager — instruct the user to install manually'."""
    if os_name == "linux":
        if pm == "apt":
            return ["apt-get", "install", "-y", "python3", "python3-venv", "python3-pip"]
        if pm == "dnf":
            return ["dnf", "install", "-y", "python3", "python3-pip"]
        if pm == "pacman":
            return ["pacman", "-S", "--noconfirm", "python", "python-pip"]
    if os_name == "macos" and pm == "brew":
        return ["brew", "install", "python@3.12"]
    if os_name == "windows" and pm == "winget":
        return ["winget", "install", "-e", "--id", "Python.Python.3.12", "--silent",
                "--accept-source-agreements", "--accept-package-agreements"]
    return []


def security_mode(strict: bool, insecure: bool) -> str:
    """strict wins a conflict (safer). Otherwise permissive — the initial-phase
    default that verifies-and-warns but does not block the install."""
    if strict:
        return "strict"
    return "permissive"


def verify_download(data: bytes, expected_sha256: str | None, mode: str) -> tuple[bool, str]:
    """Verify a fetched installer. strict = fail-closed; permissive = warn+continue."""
    actual = hashlib.sha256(data).hexdigest()
    if expected_sha256 is None:
        if mode == "strict":
            return False, "no checksum provided and --strict requires one"
        return True, "WARNING: no checksum available to verify the installer (permissive mode)"
    if actual == expected_sha256:
        return True, ""
    if mode == "strict":
        return False, f"checksum mismatch (strict): got {actual[:12]}…, refusing to run"
    return True, f"WARNING: checksum mismatch, continuing anyway (permissive): got {actual[:12]}…"

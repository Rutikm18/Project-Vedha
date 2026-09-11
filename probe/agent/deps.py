"""deps.py — Layer-2 dependency install (Phase 7).

Create the venv and pip-install the runtime deps, wheel-first so the common path
needs no C toolchain. In `strict` security mode it is wheel-ONLY (never compiles
untrusted source); permissive mode allows a source-build fallback for rare arches.
Idempotent via a requirements-hash stamp.
"""
from __future__ import annotations

import hashlib
import os
import subprocess
import sys


def venv_dir(probe_dir: str) -> str:
    return os.path.join(probe_dir, ".venv")


def venv_python(probe_dir: str) -> str:
    v = venv_dir(probe_dir)
    if os.name == "nt":
        return os.path.join(v, "Scripts", "python.exe")
    return os.path.join(v, "bin", "python")


def reqs_hash(path: str) -> str:
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def pip_install_argsets(venv_py: str, reqs_path: str, strict: bool = False) -> list[list[str]]:
    base = [venv_py, "-m", "pip", "install", "-r", reqs_path]
    wheel_only = base + ["--only-binary=:all:"]
    if strict:
        return [wheel_only]           # never build from source in strict mode
    return [wheel_only, base]         # wheel-first, then allow a source build


def ensure_venv(probe_dir: str) -> str:
    vpy = venv_python(probe_dir)
    if not os.path.exists(vpy):
        subprocess.run([sys.executable, "-m", "venv", venv_dir(probe_dir)], check=True)
        subprocess.run([vpy, "-m", "pip", "install", "-q", "--upgrade", "pip"], check=True)
    return vpy


def install_requirements(probe_dir: str, reqs_path: str, strict: bool = False) -> None:
    vpy = ensure_venv(probe_dir)
    stamp = os.path.join(venv_dir(probe_dir), ".reqs-stamp")
    want = reqs_hash(reqs_path)
    if os.path.exists(stamp):
        with open(stamp) as fh:
            if fh.read().strip() == want:
                return
    last: subprocess.CalledProcessError | None = None
    for args in pip_install_argsets(vpy, reqs_path, strict):
        try:
            subprocess.run(args, check=True)
            with open(stamp, "w") as fh:
                fh.write(want)
            return
        except subprocess.CalledProcessError as exc:
            last = exc
    raise RuntimeError(f"pip install failed for {reqs_path}") from last

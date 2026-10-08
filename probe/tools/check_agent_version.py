#!/usr/bin/env python3
"""check_agent_version.py — a change to the agent's shipped code needs a version bump.

The agent has its own version (agent/version.py), separate from the platform
release. Fleet, the manager's "is there a newer agent?" answer and the release
manifest all rely on that number meaning "this exact agent code". So if a change
alters any file the agent ships (its import closure, see agent_closure.py), the
version must go up in the same change — otherwise two different agents carry the
same number and an update can never be offered.

    python tools/check_agent_version.py --base origin/main

Exit 0: fine. Exit 1: shipped code changed without a higher AGENT_VERSION.
Exit 2: could not compare (bad base ref) — fail loudly rather than pass silently.
"""
from __future__ import annotations

import argparse
import importlib.util
import re
import subprocess
import sys
from pathlib import Path
from typing import Iterable

PROBE_ROOT = Path(__file__).resolve().parent.parent
REPO_ROOT = PROBE_ROOT.parent
VERSION_FILE = "probe/agent/version.py"
_LINE = re.compile(r'^AGENT_VERSION\s*=\s*["\']([^"\']+)["\']\s*$', re.MULTILINE)


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module  # dataclasses resolve their module by name
    spec.loader.exec_module(module)
    return module


def read_agent_version(text: str) -> str | None:
    match = _LINE.search(text)
    return match.group(1) if match else None


def shipped_files(root: Path = PROBE_ROOT) -> set[str]:
    """Repo-relative paths of every file that decides what the agent is: its code and its dependency list."""
    closure_tool = _load("agent_closure", root / "tools" / "agent_closure.py")
    closure = closure_tool.compute(root)
    prefix = root.relative_to(root.parent).as_posix()
    files = {f"{prefix}/{path.relative_to(root).as_posix()}" for path in closure.files}
    # The libraries the agent runs on change what ships just as much as its code.
    files.add(f"{prefix}/requirements-runtime.txt")
    return files


def evaluate(
    changed: Iterable[str],
    shipped: set[str],
    base_version: str | None,
    head_version: str | None,
    parse=None,
) -> list[str]:
    """Problems with this change; empty means it is fine."""
    if parse is None:
        parse = _load("update_check", PROBE_ROOT / "agent" / "update_check.py").parse_version
    touched = sorted(f for f in set(changed) if f in shipped and f != VERSION_FILE)
    if not touched:
        return []
    if base_version is None:
        return []  # the version file is being introduced by this very change
    base, head = parse(base_version), parse(head_version) if head_version else None
    if head is None:
        return [f"{VERSION_FILE} has no readable AGENT_VERSION, but shipped agent code changed."]
    if base is not None and not _newer(head, base):
        shown = ", ".join(touched[:8]) + (f" (+{len(touched) - 8} more)" if len(touched) > 8 else "")
        return [
            f"Shipped agent code changed ({shown}) but AGENT_VERSION is still {head_version} "
            f"(base {base_version}). Bump it in {VERSION_FILE}."
        ]
    return []


def _newer(a: tuple[int, ...], b: tuple[int, ...]) -> bool:
    width = max(len(a), len(b))
    return a + (0,) * (width - len(a)) > b + (0,) * (width - len(b))


def _git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=REPO_ROOT, capture_output=True, text=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--base", default="origin/main", help="git ref to compare against")
    args = parser.parse_args(argv)

    diff = _git("diff", "--name-only", f"{args.base}...HEAD")
    if diff.returncode != 0:
        print(f"check-agent-version: cannot diff against {args.base}: {diff.stderr.strip()}", file=sys.stderr)
        return 2
    changed = [line for line in diff.stdout.splitlines() if line]

    shown = _git("show", f"{args.base}:{VERSION_FILE}")
    base_version = read_agent_version(shown.stdout) if shown.returncode == 0 else None
    head_version = read_agent_version((REPO_ROOT / VERSION_FILE).read_text(encoding="utf-8"))

    problems = evaluate(changed, shipped_files(), base_version, head_version)
    if problems:
        for problem in problems:
            print(f"check-agent-version: FAIL — {problem}", file=sys.stderr)
        return 1
    print(f"check-agent-version: OK (agent {head_version}, base {base_version or 'none'})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

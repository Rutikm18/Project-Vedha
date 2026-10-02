#!/usr/bin/env python3
"""agent_closure.py — exactly which of our modules the agent needs, and nothing else.

What we hand a customer must be the agent's own code, never the rest of the
repository. This walks the imports of `agent/agent.py` (including imports inside
functions) through our local packages and returns the closure: every module the
agent can load at runtime, plus the package `__init__` files Python loads on the
way. Everything else — `scanner/findings.py` (the vulnerability judgement rules
that live on the manager), the campaign runner, the accuracy gates,
`main_scripts/`, `cve/`, tests, dev tooling — stays behind.

    python tools/agent_closure.py --list            the modules, one per line
    python tools/agent_closure.py --check           fail on a blocked module or a
                                                    dynamic import in the closure
    python tools/agent_closure.py --export DIR      copy just the closure (for images)
    python tools/agent_closure.py --write-module    refresh agent/_closure.py (the list
                                                    `vedha-agent runtime-check` imports)

Builds (Linux image, Windows/Linux compiled agent) take their file list from here
and run --check first, so a future import can't quietly ship sensitive code, and
a dynamic import (which a compiler can't see) fails the build instead of crashing
in the field.

Stdlib only: it runs inside a bare `python:3.12-slim` build stage.
"""
from __future__ import annotations

import argparse
import ast
import fnmatch
import shutil
import sys
from dataclasses import dataclass, field
from pathlib import Path

PROBE_ROOT = Path(__file__).resolve().parent.parent
ENTRY = "agent.agent"
LOCAL_PACKAGES = ("agent", "scanner", "workflow", "main_scripts", "cve")

# Modules that must never ship, even if a future change imports them. The
# closure already leaves out what the agent doesn't use; this is the guard
# against the agent starting to use something it must not carry.
BLOCKED = (
    "scanner.findings",          # judgement rules — live on the manager
    "scanner.run_all",           # shells out to main_scripts
    "scanner.va_campaign",
    "scanner.accuracy*",         # accuracy corpus / merge gate
    "main_scripts", "main_scripts.*",
    "cve", "cve.*",
    "tests", "tests.*",
    "agent.setup", "agent.deps", "agent.bootstrap", "agent.cli",   # dev / pip tooling
)

_DYNAMIC_CALLS = {"import_module", "__import__", "spec_from_file_location", "find_spec"}
# A dynamic import whose names come from this verified closure list (the
# runtime check) is marked on its line and is not a finding.
ALLOW_PRAGMA = "agent-closure: verified-names"
CLOSURE_MODULE = "agent._closure"


@dataclass
class Closure:
    modules: list[str]
    files: list[Path]
    blocked: list[str] = field(default_factory=list)
    dynamic: list[str] = field(default_factory=list)
    third_party: list[str] = field(default_factory=list)


def _module_file(root: Path, module: str) -> Path | None:
    base = root.joinpath(*module.split("."))
    if base.with_suffix(".py").is_file():
        return base.with_suffix(".py")
    if (base / "__init__.py").is_file():
        return base / "__init__.py"
    return None


def _is_package(path: Path) -> bool:
    return path.name == "__init__.py"


def _imports(tree: ast.AST, module: str, is_package: bool,
             lines: list[str] | None = None) -> tuple[list[str], list[str]]:
    """(imported module names, dynamic-import call sites) for one module."""
    names: list[str] = []
    dynamic: list[str] = []
    package = module if is_package else module.rpartition(".")[0]
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                parts = package.split(".")
                base_parts = parts[: len(parts) - (node.level - 1)] if node.level > 1 else parts
                base = ".".join(p for p in base_parts if p)
                target = f"{base}.{node.module}" if node.module else base
            else:
                target = node.module or ""
            if target:
                names.append(target)
                names.extend(f"{target}.{alias.name}" for alias in node.names if alias.name != "*")
        elif isinstance(node, ast.Call):
            func = node.func
            called = func.attr if isinstance(func, ast.Attribute) else getattr(func, "id", "")
            line = lines[node.lineno - 1] if lines and node.lineno <= len(lines) else ""
            if called in _DYNAMIC_CALLS and ALLOW_PRAGMA not in line:
                dynamic.append(f"{module}:{node.lineno}: {called}(...)")
    return names, dynamic


def compute(root: Path = PROBE_ROOT, entry: str = ENTRY) -> Closure:
    stdlib = set(getattr(sys, "stdlib_module_names", ()))
    seen: set[str] = set()
    third_party: set[str] = set()
    dynamic: list[str] = []
    stack = [entry]
    while stack:
        module = stack.pop()
        if module in seen:
            continue
        path = _module_file(root, module)
        if path is None:
            continue  # `from pkg import name` where name is an attribute, not a module
        seen.add(module)
        # Python imports every parent package's __init__ on the way in.
        parts = module.split(".")
        for i in range(1, len(parts)):
            stack.append(".".join(parts[:i]))
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
        names, calls = _imports(tree, module, _is_package(path), source.splitlines())
        dynamic.extend(calls)
        for name in names:
            top = name.split(".")[0]
            if top in LOCAL_PACKAGES:
                stack.append(name)
            elif top and top not in stdlib and top != "__future__":
                third_party.add(top)
    modules = sorted(seen)
    files = sorted({_module_file(root, m) for m in modules})
    blocked = [m for m in modules if any(fnmatch.fnmatchcase(m, pat) for pat in BLOCKED)]
    return Closure(modules=modules, files=files, blocked=blocked,
                   dynamic=sorted(dynamic), third_party=sorted(third_party))


def check(closure: Closure) -> list[str]:
    problems = [f"blocked module in the agent closure: {m}" for m in closure.blocked]
    problems += [f"dynamic import (a compiler can't follow it): {d}" for d in closure.dynamic]
    return problems


def export(closure: Closure, dest: Path, root: Path = PROBE_ROOT) -> int:
    """Copy just the closure's files to dest, keeping the package layout."""
    for path in closure.files:
        target = dest / path.relative_to(root)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
    return len(closure.files)


def render_module(modules: list[str]) -> str:
    body = "".join(f"    {m!r},\n" for m in modules)
    return (
        '"""Generated by tools/agent_closure.py --write-module — do not edit.\n\n'
        "Every module of ours the agent can load. `vedha-agent runtime-check` imports\n"
        "each one, so a compiled build that dropped a module fails before it ships.\n"
        'tests/test_agent_closure.py keeps this list equal to the computed closure."""\n'
        f"MODULES = (\n{body})\n"
    )


def write_module(root: Path = PROBE_ROOT) -> Path:
    modules = sorted(set(compute(root).modules) | {CLOSURE_MODULE})
    target = root / "agent" / "_closure.py"
    target.write_text(render_module(modules), encoding="utf-8")
    return target


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--list", action="store_true")
    group.add_argument("--check", action="store_true")
    group.add_argument("--export", type=Path, metavar="DIR")
    group.add_argument("--write-module", action="store_true")
    parser.add_argument("--root", type=Path, default=PROBE_ROOT)
    args = parser.parse_args(argv)

    if args.write_module:
        print(f"agent-closure: wrote {write_module(args.root)}")
        return 0
    closure = compute(args.root)
    problems = check(closure)
    if args.list:
        print("\n".join(closure.modules))
        return 0
    if problems:
        for problem in problems:
            print(f"agent-closure: {problem}", file=sys.stderr)
        return 1
    if args.check:
        print(f"agent-closure: OK — {len(closure.modules)} modules, "
              f"third-party: {', '.join(closure.third_party)}")
        return 0
    count = export(closure, args.export, args.root)
    print(f"agent-closure: exported {count} files to {args.export}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""
test_two_tree_parity.py — the guard the architecture review (#4) demanded.

`scanner/` and `main_scripts/` are hand-mirrored, byte-identical duplicates: the
same scanner source exists twice so `workflow/`+tests can import `scanner.*` while
`run_all`/`accuracy` import `main_scripts.*`. The existing wiring gate catches
*routing* drift (a branch wired in one orchestrator but not another); it does NOT
catch *logic* drift — a bug fixed in `scanner/ftp_scanner.py` but not its
`main_scripts` twin diverges silently and the two orchestrator families then
behave differently on the same host.

This test closes that hole: every mirrored pair must be byte-identical. If a pair
legitimately must differ, add it to `_ALLOWED_DIVERGENCE` with a reason — never
weaken the assertion. The real fix (collapse to one tree) is tracked separately;
until then this makes divergence a failing test instead of a field surprise.
"""

from __future__ import annotations

from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parent.parent
_SCANNER = _ROOT / "scanner"
_MAIN = _ROOT / "main_scripts"

# Files that are intentionally NOT byte-identical across the two trees.
# Keep this empty; every entry is a documented, reviewed exception.
_ALLOWED_DIVERGENCE: set[str] = set()


def _mirrored_py_files() -> list[str]:
    """Every .py present in BOTH trees (the mirrored set), excluding caches."""
    scanner_files = {p.name for p in _SCANNER.glob("*.py")}
    main_files = {p.name for p in _MAIN.glob("*.py")}
    return sorted((scanner_files & main_files) - _ALLOWED_DIVERGENCE)


def test_mirrored_set_is_nonempty():
    # Guards against a glob/path regression silently making the parity check vacuous.
    assert len(_mirrored_py_files()) >= 40


@pytest.mark.parametrize("name", _mirrored_py_files())
def test_scanner_and_main_scripts_are_byte_identical(name):
    a = (_SCANNER / name).read_bytes()
    b = (_MAIN / name).read_bytes()
    assert a == b, (
        f"{name} DIVERGED between scanner/ and main_scripts/. "
        f"Mirror the change (cp scanner/{name} main_scripts/{name}) or, if the "
        f"divergence is intentional, add it to _ALLOWED_DIVERGENCE with a reason."
    )


def test_no_unmirrored_scanner_files():
    """A scanner that exists in only one tree is a wiring bug: one orchestrator
    family can reach it and the other can't. Fail loudly (allow-list if truly
    tree-specific)."""
    scanner_only = {p.name for p in _SCANNER.glob("*.py")} - \
        {p.name for p in _MAIN.glob("*.py")} - _ALLOWED_DIVERGENCE
    main_only = {p.name for p in _MAIN.glob("*.py")} - \
        {p.name for p in _SCANNER.glob("*.py")} - _ALLOWED_DIVERGENCE
    assert not scanner_only, f"present only in scanner/: {sorted(scanner_only)}"
    assert not main_only, f"present only in main_scripts/: {sorted(main_only)}"

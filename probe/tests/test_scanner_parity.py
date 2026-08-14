"""
test_scanner_parity.py — the no-drift guard.

Decision (probe_next plan, Phase 1): main_scripts/ is the AUTHORITATIVE source of
truth for the scanning layer ("scanner was not accurate — do all according
main_scripts"). The live probe runtime (workflow_engine, agent/engine) imports
`scanner.*`, so scanner/ is kept byte-identical to main_scripts/ instead of
repointing hundreds of imports. This test fails the moment the two trees diverge,
forcing every future scanner change to land in BOTH (or, better, land in
main_scripts and be re-synced) so the probe can never silently run stale code.

Sync command (from probe/):  cp main_scripts/*.py scanner/
"""
from __future__ import annotations

from pathlib import Path

import pytest

_PROBE = Path(__file__).resolve().parent.parent
_MAIN = _PROBE / "main_scripts"
_SCANNER = _PROBE / "scanner"


def _py_files(root: Path) -> set[str]:
    return {p.name for p in root.glob("*.py")}


def test_scanner_is_superset_of_no_missing_files():
    """Every scanner module authored in main_scripts must exist in scanner/."""
    missing = _py_files(_MAIN) - _py_files(_SCANNER)
    assert not missing, (
        f"scanner/ is missing modules present in main_scripts/: {sorted(missing)}. "
        "Re-sync with: cp main_scripts/*.py scanner/"
    )


def test_no_extra_scanner_files():
    """scanner/ must not carry modules that main_scripts/ does not — otherwise the
    probe could run code with no authoritative counterpart."""
    extra = _py_files(_SCANNER) - _py_files(_MAIN)
    assert not extra, (
        f"scanner/ has modules with no main_scripts/ source of truth: {sorted(extra)}."
    )


@pytest.mark.parametrize("name", sorted(_py_files(_MAIN)))
def test_scanner_module_matches_main_scripts(name: str):
    """Each scanner/<mod>.py is byte-identical to main_scripts/<mod>.py."""
    main_bytes = (_MAIN / name).read_bytes()
    scanner_path = _SCANNER / name
    assert scanner_path.exists(), (
        f"scanner/{name} is absent. Re-sync with: cp main_scripts/*.py scanner/"
    )
    assert scanner_path.read_bytes() == main_bytes, (
        f"scanner/{name} has drifted from main_scripts/{name}. main_scripts/ is "
        "authoritative — re-sync with: cp main_scripts/*.py scanner/"
    )

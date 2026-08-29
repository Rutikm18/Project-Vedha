"""
test_trust_alignment.py — cross-tree invariant: the manager's VALIDATED_SCANNERS
(which sensors it will CONFIRM findings from) MUST equal the probe's VERIFIED
registry (which scanners the probe presents as trusted). If they drift, the manager
would confirm findings from a scanner the probe calls experimental, or vice-versa —
a silent trust mismatch. Guarded: skips cleanly when the probe tree isn't present
(the manager can be deployed on its own).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

from posture_rules import VALIDATED_SCANNERS

# probe/ lives at <repo>/probe relative to manager/detection_engine/tests/
_PROBE = Path(__file__).resolve().parents[3] / "probe"


def test_manager_and_probe_trust_sets_match():
    if not (_PROBE / "main_scripts" / "scanner_registry.py").exists():
        pytest.skip("probe tree not present — manager deployed standalone")
    sys.path.insert(0, str(_PROBE))
    try:
        from main_scripts.scanner_registry import VERIFIED  # type: ignore
    except Exception as exc:  # pragma: no cover - import env issue, not a logic fail
        pytest.skip(f"probe registry not importable here: {exc}")
    only_manager = VALIDATED_SCANNERS - VERIFIED
    only_probe = VERIFIED - VALIDATED_SCANNERS
    assert VALIDATED_SCANNERS == VERIFIED, (
        f"trust sets diverged — manager-only={sorted(only_manager)}, "
        f"probe-only={sorted(only_probe)}")
